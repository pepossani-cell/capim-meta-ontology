# Materialize Extensions — CLIENT_VOICE Domain

> **Purpose**: Padrões específicos de materialização para CLIENT_VOICE (VoC)  
> **Base Skill**: `@materialize-view` (Tier 2)  
> **Domain**: client-voice-data

---

## Views Candidatas à Materialização

| View | Volume | Estratégia | Prioridade |
|------|--------|------------|------------|
| `TICKET_ANALYSIS_V3` | ~50K | Não recomendado | N/A |
| Aggregates de sentiment | ~1K | CTAS simples | Média |
| Category summary | ~100 | Não necessário | N/A |

---

## Especificidade CLIENT_VOICE

O domínio CLIENT_VOICE tem **baixo volume** comparado a SAAS/FINTECH. Materialização raramente é necessária.

### Quando Materializar

✅ **Sim**:
- Agregações complexas cross-domain
- Views que combinam tickets + SAAS + FINTECH

❌ **Não**:
- Views simples de tickets
- Queries < 5s
- Dados que mudam frequentemente (tickets novos)

---

## Exemplo: Sentiment Aggregate by Clinic

### Justificativa

- Agregação usada em health check de clinic
- Combina múltiplas métricas de sentiment
- Pode ser materializada para performance

### DDL

```sql
-- queries/materialize/client_voice/materialize_clinic_sentiment_agg_v1.sql

CREATE OR REPLACE TABLE <schema>.CLINIC_SENTIMENT_AGG_MAT_V1
AS 
SELECT 
    CURRENT_TIMESTAMP AS materialized_at,
    clinic_id,
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as ticket_count,
    AVG(sentiment_score) as avg_sentiment,
    SUM(CASE WHEN sentiment_score <= 2 THEN 1 ELSE 0 END) as negative_count,
    SUM(CASE WHEN sentiment_score >= 4 THEN 1 ELSE 0 END) as positive_count
FROM TICKET_ANALYSIS_V3
WHERE clinic_id IS NOT NULL
GROUP BY 1, 2, 3;
```

---

## Cross-Domain Materialização

O caso mais comum de materialização em CLIENT_VOICE é para views cross-domain:

```sql
-- View que combina tickets + clinic info
CREATE OR REPLACE VIEW TICKET_WITH_CLINIC_INFO AS
SELECT 
    t.*,
    c.name as clinic_name,
    c.tier as clinic_tier,
    c.region as clinic_region
FROM TICKET_ANALYSIS_V3 t
LEFT JOIN SAAS.CLINICS c ON t.clinic_id = c.id;

-- Se performance é problema, materializar
CREATE OR REPLACE TABLE TICKET_WITH_CLINIC_INFO_MAT
AS SELECT CURRENT_TIMESTAMP AS materialized_at, *
FROM TICKET_WITH_CLINIC_INFO;
```

---

## Validação Específica CLIENT_VOICE

```sql
-- 1. Contagem por categoria deve bater
SELECT category, COUNT(*)
FROM <view>
GROUP BY 1
EXCEPT
SELECT category, COUNT(*)
FROM <mat>
GROUP BY 1;

-- 2. Sentiment médio deve bater
SELECT AVG(sentiment_score) FROM <view>
UNION ALL
SELECT AVG(sentiment_score) FROM <mat>;
```

---

## Recomendação

Para CLIENT_VOICE, **prefira manter views** e materializar apenas quando:
1. Query time > 10s
2. View é usada em múltiplos contextos
3. Refresh diário é aceitável

Volume baixo = materialização geralmente desnecessária.

---

## Referências

- `docs/reference/TICKET_ANALYSIS.md`
- `queries/zendesk/` — Queries de análise
