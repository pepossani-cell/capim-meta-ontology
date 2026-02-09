# Materialize Extensions — FINTECH Domain

> **Purpose**: Padrões específicos de materialização para FINTECH (BNPL)  
> **Base Skill**: `@materialize-view` (Tier 2)  
> **Domain**: bnpl-funil

---

## Views Candidatas à Materialização

| View | Volume | Estratégia | Prioridade |
|------|--------|------------|------------|
| `C1_ENRICHED_BORROWER_V1` | ~500K | CTAS + Clustering | Alta |
| `CLINIC_DIM_V1` | ~5K | CTAS simples | Média |
| `BNPL_CLINIC_MONTHLY_FUNNEL_V1` | ~50K | CTAS + Clustering | Alta |

---

## Exemplo: C1_ENRICHED_BORROWER_V1

### Justificativa

- View com múltiplos JOINs (C1 + bureaus + clinic dim)
- Query time atual: ~45s
- Usada por 3+ análises diferentes
- Não muda frequentemente (refresh diário ok)

### DDL

```sql
-- queries/materialize/fintech/materialize_c1_enriched_borrower_v1.sql

/*
=============================================================================
MATERIALIZATION: C1_ENRICHED_BORROWER_V1
=============================================================================
Source View: CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_V1
Target Table: CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_MAT_V1
Strategy: CTAS (Full Refresh)
Schedule: Daily 6h BRT
Owner: fintech-team
Created: 2026-02-04
=============================================================================
*/

CREATE OR REPLACE TABLE CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_MAT_V1
CLUSTER BY (clinic_id, simulation_month)
AS 
SELECT 
    CURRENT_TIMESTAMP AS materialized_at,
    *
FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_V1;
```

### Task de Refresh

```sql
CREATE OR REPLACE TASK CAPIM_DATA_DEV.POSSANI_SANDBOX.task_refresh_c1_enriched_borrower_mat
    WAREHOUSE = COMPUTE_WH
    SCHEDULE = 'USING CRON 0 6 * * * America/Sao_Paulo'
AS
    CREATE OR REPLACE TABLE CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_MAT_V1
    CLUSTER BY (clinic_id, simulation_month)
    AS SELECT CURRENT_TIMESTAMP AS materialized_at, * 
    FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_V1;

ALTER TASK CAPIM_DATA_DEV.POSSANI_SANDBOX.task_refresh_c1_enriched_borrower_mat RESUME;
```

---

## Exemplo: CLINIC_DIM_V1

### Justificativa

- Dimensão usada em múltiplos JOINs
- Volume pequeno (~5K clinics)
- Melhora performance de queries downstream

### DDL

```sql
-- queries/materialize/fintech/materialize_clinic_dim_v1.sql

CREATE OR REPLACE TABLE CAPIM_DATA_DEV.POSSANI_SANDBOX.CLINIC_DIM_MAT_V1
AS 
SELECT 
    CURRENT_TIMESTAMP AS materialized_at,
    *
FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.CLINIC_DIM_V1;
```

---

## Scripts Existentes

O domínio FINTECH já tem scripts de materialização em `bnpl-funil/src/cli/`:

```
src/cli/
├── materialize_enriched_credit_simulations_borrower.py
└── ...
```

**Recomendação**: Migrar para o padrão da skill `@materialize-view` com:
- DDL em `queries/materialize/fintech/`
- Task Snowflake ou script padronizado
- Documentação em `docs/reference/*_MAT.md`

---

## Clustering Keys Recomendados

| View | Clustering Key | Razão |
|------|----------------|-------|
| C1_ENRICHED_BORROWER | `(clinic_id, simulation_month)` | Filtros frequentes |
| BNPL_CLINIC_MONTHLY_FUNNEL | `(clinic_id, month)` | Agregações por clinic+month |
| CLINIC_DIM | N/A | Volume pequeno |

---

## Validação Específica FINTECH

Após materialização, validar:

```sql
-- 1. Contagem de simulações por mês deve bater
SELECT simulation_month, COUNT(*) 
FROM <view> GROUP BY 1
EXCEPT
SELECT simulation_month, COUNT(*) 
FROM <mat> GROUP BY 1;

-- 2. Métricas de conversão devem bater
SELECT 
    SUM(CASE WHEN has_c2 THEN 1 ELSE 0 END) / COUNT(*) as conversion_rate
FROM <view>
UNION ALL
SELECT 
    SUM(CASE WHEN has_c2 THEN 1 ELSE 0 END) / COUNT(*) as conversion_rate
FROM <mat>;
```

---

## Referências

- `docs/reference/C1_ENRICHED_BORROWER_V1.md`
- `docs/reference/CLINIC_DIM_V1.md`
- `src/cli/` — Scripts legados de materialização
