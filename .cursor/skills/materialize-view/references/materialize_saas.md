# Materialize Extensions — SAAS Domain

> **Purpose**: Padrões específicos de materialização para SAAS  
> **Base Skill**: `@materialize-view` (Tier 2)  
> **Domain**: ontologia-saas

---

## Views Candidatas à Materialização

| View | Volume | Estratégia | Prioridade |
|------|--------|------------|------------|
| `SOURCE_DASH_*` (corrigidas) | ~100K | CTAS simples | Média |
| Aggregates de orçamento | ~500K | CTAS + Clustering | Alta |
| Clinic Activity Summary | ~5K | CTAS simples | Baixa |

---

## Padrão SAAS: Views de Dashboard

Muitas views SAAS são criadas para dashboards Metabase/BI. Materialização pode melhorar performance.

### Quando Materializar Dashboard Views

✅ **Sim**:
- Dashboard usado diariamente
- Query time > 10s
- Múltiplos usuários acessam

❌ **Não**:
- Dashboard de uso ocasional
- Precisa de dados real-time
- View simples (< 5s)

---

## Exemplo: SOURCE_DASH_CANCELLATION_REQUESTS_CORRECTED_V1

### Justificativa

- View corrigida com lógica de negócio
- Usada em dashboard de churn
- Refresh diário é suficiente

### DDL

```sql
-- queries/materialize/saas/materialize_source_dash_cancellation_requests_v1.sql

CREATE OR REPLACE TABLE <schema>.SOURCE_DASH_CANCELLATION_REQUESTS_MAT_V1
AS 
SELECT 
    CURRENT_TIMESTAMP AS materialized_at,
    *
FROM <schema>.SOURCE_DASH_CANCELLATION_REQUESTS_CORRECTED_V1;
```

---

## Aggregates de Orçamento

Views agregadas por clinic+mês são candidatas frequentes.

### Padrão

```sql
-- Aggregate: orçamentos por clínica por mês
CREATE OR REPLACE VIEW CLINIC_BUDGET_MONTHLY_AGG AS
SELECT 
    clinic_id,
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as budget_count,
    SUM(total_value) as total_value,
    AVG(total_value) as avg_value
FROM BUDGETS
GROUP BY 1, 2;

-- Materializar se performance < threshold
CREATE OR REPLACE TABLE CLINIC_BUDGET_MONTHLY_AGG_MAT
CLUSTER BY (clinic_id, month)
AS SELECT CURRENT_TIMESTAMP AS materialized_at, * 
FROM CLINIC_BUDGET_MONTHLY_AGG;
```

---

## Validação Específica SAAS

Após materialização, validar:

```sql
-- 1. Totais por mês devem bater
SELECT DATE_TRUNC('month', created_at) as month, COUNT(*)
FROM <source_table>
GROUP BY 1
EXCEPT
SELECT month, SUM(budget_count)
FROM <mat_aggregate>
GROUP BY 1;

-- 2. Valores totais devem bater
SELECT SUM(total_value) FROM <view>
UNION ALL
SELECT SUM(total_value) FROM <mat>;
```

---

## Clustering Keys Recomendados

| View | Clustering Key | Razão |
|------|----------------|-------|
| Budget aggregates | `(clinic_id, month)` | Filtros frequentes |
| Cancellation requests | `(cancelled_at)` | Filtros temporais |
| Clinic activity | N/A | Volume pequeno |

---

## Referências

- `docs/reference/SOURCE_DASH_*.md` — Documentação de views
- `queries/views/` — DDL das views fonte
