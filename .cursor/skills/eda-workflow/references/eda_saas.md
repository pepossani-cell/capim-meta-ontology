# EDA Extensions — SAAS Domain

> **Purpose**: Padrões específicos de EDA para o domínio SAAS  
> **Base Skill**: `@eda-workflow` (Tier 2)  
> **Domain**: ontologia-saas

---

## Estrutura de Estudos SAAS

```
ontologia-saas/
├── eda/
│   └── <nome_estudo>/
│       ├── README.md           # Incertezas, perguntas abertas
│       ├── scratchpad.sql      # Queries exploratórias
│       ├── *CONTRATO*.md       # Contrato de saída (quando ESTÁVEL)
│       └── DECISION_TREE.md    # Árvore de decisões (quando ESTÁVEL)
├── queries/
│   ├── studies/<estudo>/       # Queries promovidas (BI-safe)
│   └── audit/saas/             # Microtests e validações
└── docs/
    └── reference/              # Semântica de entidades
```

---

## Entidades Frequentes em EDA SAAS

| Entidade | Tabela/View | Grain | Doc Semântica |
|----------|-------------|-------|---------------|
| Clinic | `CLINICS` | clinic_id | `docs/reference/CLINICS.md` |
| Subscription | `SUBSCRIPTIONS` | subscription_id | `docs/reference/SUBSCRIPTIONS.md` |
| Budget | `BUDGETS` | budget_id | `docs/reference/BUDGETS.md` |
| Procedure | `PROCEDURES` | procedure_id | `docs/reference/PROCEDURES.md` |
| Cancellation | `SUBSCRIPTION_CANCELLATION_REQUESTS` | id | `docs/reference/SUBSCRIPTION_CANCELLATION_REQUESTS.md` |

---

## Padrões de Análise SAAS

### 1. Análise de Churn

**Universo típico**:
```sql
-- Clinics com subscription ativa em algum momento do período
SELECT DISTINCT clinic_id
FROM subscriptions
WHERE status IN ('active', 'past_due', 'cancelled')
  AND (cancelled_at IS NULL OR cancelled_at >= @start_date)
  AND created_at <= @end_date
```

**Métricas**:
- Churn rate = cancelled / total no início
- MRR churn = MRR perdido / MRR início
- Tempo de vida médio

**Debate triggers comuns**:
- "Incluir past_due como ativo?"
- "cancelled_at é confiável para todos os períodos?"

---

### 2. Análise de Orçamentos

**Universo típico**:
```sql
-- Orçamentos criados no período
SELECT *
FROM budgets
WHERE created_at BETWEEN @start_date AND @end_date
  AND clinic_id IN (SELECT id FROM clinics WHERE status = 'active')
```

**Métricas**:
- Volume de orçamentos por clínica
- Valor médio de orçamento
- Taxa de conversão (orçamento → procedimento)

**Debate triggers comuns**:
- "Orçamento cancelado conta?"
- "Clínica de teste entra no universo?"

---

### 3. Análise de Tiers

**Universo típico**:
```sql
-- Clinics classificadas por volume
WITH clinic_volume AS (
  SELECT 
    clinic_id,
    COUNT(*) as budget_count,
    SUM(total_value) as total_value
  FROM budgets
  WHERE created_at >= DATEADD(month, -3, CURRENT_DATE)
  GROUP BY clinic_id
)
SELECT 
  CASE 
    WHEN budget_count >= 50 THEN 'large'
    WHEN budget_count >= 10 THEN 'medium'
    ELSE 'small'
  END as tier,
  *
FROM clinic_volume
```

**Debate triggers comuns**:
- "Thresholds de tier são fixos ou percentis?"
- "Volume por contagem ou valor?"

---

## CLI Específico (Opcional)

Se o estudo requer execução repetida:

```python
# scripts/eda/<estudo>/run_analysis.py

from src.utils.snowflake_connection import run_query
import argparse

def main(start_date, end_date, output_dir):
    # Carregar queries do scratchpad
    # Executar e salvar outputs em _scratch/
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-date', required=True)
    parser.add_argument('--end-date', required=True)
    parser.add_argument('--output-dir', default='_scratch/')
    args = parser.parse_args()
    main(args.start_date, args.end_date, args.output_dir)
```

---

## Promoção de Achados SAAS

### Para Microtest

```sql
-- queries/audit/saas/audit_<achado>_v1.sql
-- Invariante: [descrição]
-- Esperado: 0 rows (ou threshold)

SELECT ...
WHERE <condição_de_violação>
```

### Para Semântica

```markdown
# docs/reference/<ENTIDADE>.md

## Descoberto em EDA

| Campo | Semântica | Descoberto em |
|-------|-----------|---------------|
| `cancelled_at` | Confiável apenas após 2024-03 | eda/churn_2025h2 |
```

### Para Contrato

```markdown
# eda/<estudo>/<ESTUDO>_CONTRATO.md

## Grão
- Uma linha por: [clinic_id, month]

## Chaves
- PK: clinic_id + month

## Classes/Eixos
| Eixo | Definição | Classes |
|------|-----------|---------|
| tier | volume 3 meses | small/medium/large |

## Caveats
- [limitações conhecidas]
```

---

## Skills Relacionadas (SAAS)

| Situação | Skill |
|----------|-------|
| Validar contrato | `@validate-saas-contracts` |
| Promover achado | `@formalize-saas-finding` |
| Drift intra-SAAS | `@detect-saas-drift` (planned) |
| Health check cross | `@clinic-health-check` |

---

## Referências

- `docs/how_to/EDA_PLAYBOOK.md` — Guia original
- `docs/how_to/PROGRESSIVE_FORMALIZATION.md` — Critérios de promoção
- `_domain/_docs/ENTITY_INDEX.yaml` — Índice de entidades
