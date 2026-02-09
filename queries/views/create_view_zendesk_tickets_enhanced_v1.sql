-- create_view_zendesk_tickets_enhanced_v1.sql
--
-- View enriquecida dos tickets Zendesk com múltiplas fontes de clinic_id expostas
-- Grão: zendesk_ticket_id (1:1 com ZENDESK_TICKETS_RAW)
--
-- Problema resolvido:
--   - source_dash_users tem user_email hasheado (SHA-256) → JOIN nunca funciona
--   - Solução: usar RESTRICTED.USERS_SENSITIVE_INFORMATION (email não hasheado)
--   - Ganho esperado: 46% → 50% fill rate (+4pp, ~17K tickets)
--
-- Referência: capim-meta-ontology/_memory/DECISIONS_IN_PROGRESS.md (H5/H2b)
-- Data: 2026-02-02
-- Autor: Antigravity Agent + User

CREATE OR REPLACE VIEW CAPIM_DATA_DEV.POSSANI_SANDBOX.ZENDESK_TICKETS_ENHANCED_V1 AS

WITH 
/* ========================================================================== */
/* RESTRICTED: emails não hasheados com clinic_id                              */
/* ========================================================================== */
restricted_clinic AS (
    SELECT 
        LOWER(TRIM(user_email)) AS email,
        clinic_id AS restricted_clinic_id
    FROM CAPIM_DATA.RESTRICTED.USERS_SENSITIVE_INFORMATION
    WHERE user_email IS NOT NULL
    -- Deduplica emails (pega qualquer clinic_id se houver duplicata)
    QUALIFY ROW_NUMBER() OVER (PARTITION BY LOWER(TRIM(user_email)) ORDER BY user_email) = 1
),

/* ========================================================================== */
/* Base: ZENDESK_TICKETS_RAW com fontes individuais                            */
/* ========================================================================== */
base AS (
    SELECT 
        t.*,
        
        /* Normaliza email para match */
        LOWER(TRIM(t.end_user_external_id)) AS email_normalized
        
    FROM CAPIM_DATA.CAPIM_ANALYTICS.ZENDESK_TICKETS_RAW t
),

/* ========================================================================== */
/* Enriquecido: todas as fontes expostas + consolidado                         */
/* ========================================================================== */
enriched AS (
    SELECT 
        b.*,
        
        /* ====== FONTES INDIVIDUAIS DE CLINIC_ID ====== */
        b.org_external_id AS clinic_id_from_org,
        b.lu_clinic_id AS clinic_id_from_requests,
        r.restricted_clinic_id AS clinic_id_from_restricted,
        
        /* ====== CLINIC_ID CONSOLIDADO (hierarquia: org > restricted > requests) ====== */
        COALESCE(
            b.org_external_id, 
            r.restricted_clinic_id, 
            b.lu_clinic_id
        ) AS clinic_id_enhanced,
        
        /* ====== DIAGNÓSTICO: de onde veio o clinic_id ====== */
        CASE 
            WHEN b.org_external_id IS NOT NULL THEN 'org'
            WHEN r.restricted_clinic_id IS NOT NULL THEN 'restricted'
            WHEN b.lu_clinic_id IS NOT NULL THEN 'requests'
            ELSE 'none'
        END AS clinic_id_source,
        
        /* ====== FLAGS DE QUALIDADE ====== */
        -- Divergência entre org e restricted
        CASE 
            WHEN b.org_external_id IS NOT NULL 
                 AND r.restricted_clinic_id IS NOT NULL 
                 AND b.org_external_id != r.restricted_clinic_id 
            THEN TRUE 
            ELSE FALSE 
        END AS has_org_restricted_divergence,
        
        -- Divergência entre org e requests
        CASE 
            WHEN b.org_external_id IS NOT NULL 
                 AND b.lu_clinic_id IS NOT NULL 
                 AND b.org_external_id != b.lu_clinic_id 
            THEN TRUE 
            ELSE FALSE 
        END AS has_org_requests_divergence,
        
        -- Ticket que ganhou clinic_id graças ao RESTRICTED
        CASE 
            WHEN b.org_external_id IS NULL 
                 AND r.restricted_clinic_id IS NOT NULL 
            THEN TRUE 
            ELSE FALSE 
        END AS clinic_id_from_restricted_only
        
    FROM base b
    LEFT JOIN restricted_clinic r 
        ON b.email_normalized = r.email
        AND b.end_user_external_id LIKE '%@%'  -- Só tenta match se parece email
)

SELECT * FROM enriched
;

/* ========================================================================== */
/* DOCUMENTAÇÃO                                                                 */
/* ========================================================================== */
/*
CAMPOS ADICIONADOS (em relação a ZENDESK_TICKETS_RAW):

| Campo                          | Tipo    | Descrição                                      |
|--------------------------------|---------|------------------------------------------------|
| clinic_id_from_org             | NUMBER  | clinic_id via organização Zendesk              |
| clinic_id_from_requests        | NUMBER  | clinic_id via último request (source_requests) |
| clinic_id_from_restricted      | NUMBER  | clinic_id via USERS_SENSITIVE_INFORMATION      |
| clinic_id_enhanced             | NUMBER  | COALESCE(org, restricted, requests)            |
| clinic_id_source               | TEXT    | 'org', 'restricted', 'requests', ou 'none'     |
| has_org_restricted_divergence  | BOOLEAN | TRUE se org != restricted (quando ambos exist) |
| has_org_requests_divergence    | BOOLEAN | TRUE se org != requests (quando ambos exist)   |
| clinic_id_from_restricted_only | BOOLEAN | TRUE se clinic_id veio SÓ do RESTRICTED        |

EXPECTATIVA:
- Fill rate: 46% → 50% (+4pp)
- Tickets com clinic_id: 199K → 217K (+17K)

USO:
- Para análise padrão: usar clinic_id_enhanced
- Para debug/auditoria: usar campos individuais + flags de divergência
*/
