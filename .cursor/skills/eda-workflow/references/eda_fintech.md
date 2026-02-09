# EDA Extensions — FINTECH Domain

> **Purpose**: Padrões específicos de EDA para o domínio FINTECH (BNPL)  
> **Base Skill**: `@eda-workflow` (Tier 2)  
> **Domain**: bnpl-funil

---

## Estrutura de Estudos FINTECH

```
bnpl-funil/
├── eda/
│   └── <nome_estudo>/
│       ├── README.md           # Incertezas, perguntas abertas
│       ├── scratchpad.sql      # Queries exploratórias
│       ├── *CONTRATO*.md       # Contrato de saída (quando ESTÁVEL)
│       └── DECISION_TREE.md    # Árvore de decisões (quando ESTÁVEL)
├── queries/
│   ├── studies/<estudo>/       # Queries promovidas (BI-safe)
│   │   └── autopsia_bnpl/      # Exemplo: estudo existente
│   └── audit/                  # Microtests por categoria
│       ├── bridges/            # Audits de bridge tables
│       ├── semantics/          # Audits de semântica
│       └── pre_analyses/       # Audits de pré-análises
└── docs/
    ├── reference/              # Semântica de entidades
    └── adr/                    # Decisões arquiteturais
```

---

## Entidades Frequentes em EDA FINTECH

| Entidade | Tabela/View | Grain | Doc Semântica |
|----------|-------------|-------|---------------|
| Credit Simulation (C1) | `CREDIT_SIMULATIONS` | id | `docs/reference/CREDIT_SIMULATIONS*.md` |
| Credit Check (C2) | `CREDIT_CHECKS_*` | id | `docs/reference/CREDIT_CHECKS*.md` |
| Crivo Check | `CRIVO_CHECKS` | id | `docs/reference/CRIVO_CHECKS*.md` |
| Pre-Analysis | `PRE_ANALYSES_*` | id | `docs/reference/PRE_ANALYSIS*.md` |
| Clinic Dim | `CLINIC_DIM_V1` | clinic_id | `docs/reference/CLINIC_DIM_V1.md` |

---

## Padrões de Análise FINTECH

### 1. Análise de Funil C1→C2

**Universo típico**:
```sql
-- Simulações de crédito no período
SELECT 
    cs.*,
    cc.id as credit_check_id,
    cc.status as c2_status
FROM CREDIT_SIMULATIONS cs
LEFT JOIN bridge_c1_c2 b ON cs.id = b.simulation_id
LEFT JOIN CREDIT_CHECKS cc ON b.credit_check_id = cc.id
WHERE cs.created_at BETWEEN @start_date AND @end_date
```

**Métricas**:
- Conversão C1→C2 = C2 / C1
- Taxa de aprovação = approved / total C2
- Valor médio por simulação

**Debate triggers comuns**:
- "C1 sem C2 é recusa ou abandono?"
- "Múltiplos C2 para mesmo C1 — como contar?"

**Skill relacionada**: `@analyze-conversion-funnel`

---

### 2. Análise de Bridges

**Universo típico**:
```sql
-- Cruzamento C1 ↔ Bureaus ↔ Crivo
SELECT 
    cs.id as simulation_id,
    scr.id as scr_id,
    serasa.id as serasa_id,
    crivo.id as crivo_id
FROM CREDIT_SIMULATIONS cs
LEFT JOIN bridge_c1_scr b1 ON cs.id = b1.simulation_id
LEFT JOIN SCR_AFTER_EVENT scr ON b1.scr_id = scr.id
LEFT JOIN bridge_c1_serasa b2 ON cs.id = b2.simulation_id
LEFT JOIN SERASA_NEW serasa ON b2.serasa_id = serasa.id
LEFT JOIN bridge_c1_crivo b3 ON cs.id = b3.simulation_id
LEFT JOIN CRIVO_CHECKS crivo ON b3.crivo_id = crivo.id
```

**Debate triggers comuns**:
- "Janela de tempo para bridge — 24h ou 48h?"
- "Crivo ausente é erro ou não chamado?"

**Skill relacionada**: `@bridge-temporal-events`

---

### 3. Análise de Score/Risk

**Universo típico**:
```sql
-- Distribuição de scores por fonte
SELECT 
    'SCR' as source,
    CASE 
        WHEN score < 300 THEN 'very_low'
        WHEN score < 500 THEN 'low'
        WHEN score < 700 THEN 'medium'
        ELSE 'high'
    END as score_bucket,
    COUNT(*)
FROM SCR_AFTER_EVENT
GROUP BY 1, 2
```

**Debate triggers comuns**:
- "Score -1 ou NULL — como tratar?"
- "Thresholds de bucket são de negócio ou percentis?"

**Skill relacionada**: `@validate-fintech-axioms` (AX-FINTECH-004: score normalization)

---

## Thresholds FINTECH

```yaml
# Thresholds específicos do domínio FINTECH

time_windows:
  c1_to_c2: 24h  # Máximo entre C1 e C2
  c1_to_bureau: 48h  # Máximo entre C1 e consulta bureau
  c1_to_crivo: 72h  # Máximo entre C1 e Crivo

score_normalization:
  invalid_values: [-1, 0, null]
  valid_range: [1, 1000]
  
rejection_rate:
  expected_range: [0.3, 0.7]  # 30-70% é normal
  alert_if_above: 0.8
  alert_if_below: 0.2

conversion_rate:
  c1_to_c2_expected: [0.4, 0.8]
  c2_approval_expected: [0.3, 0.6]
```

---

## Promoção de Achados FINTECH

### Para Microtest (Bridge)

```sql
-- queries/audit/bridges/audit_<bridge>_v1.sql
-- Invariante: C1 com C2 deve ter Crivo
-- Esperado: 0 rows (ou threshold)

SELECT cs.id, cc.id
FROM CREDIT_SIMULATIONS cs
JOIN CREDIT_CHECKS cc ON cs.clinic_id = cc.clinic_id
  AND cc.created_at BETWEEN cs.created_at AND DATEADD(hour, 24, cs.created_at)
LEFT JOIN CRIVO_CHECKS cr ON cc.id = cr.credit_check_id
WHERE cr.id IS NULL
  AND cc.status IN ('approved', 'rejected')
```

### Para ADR

```markdown
# docs/adr/000X-<decisao>.md

## Status
Aceito

## Contexto
Durante EDA de [estudo], identificamos que...

## Decisão
Adotamos [decisão] porque...

## Consequências
- [positivas]
- [negativas]
```

---

## Skills Relacionadas (FINTECH)

| Situação | Skill |
|----------|-------|
| Análise de funil | `@analyze-conversion-funnel` |
| Validar axiomas | `@validate-fintech-axioms` |
| Bridge temporal | `@bridge-temporal-events` |
| Drift intra-FINTECH | `@detect-fintech-drift` (planned) |
| Materializar view | `@materialize-view` |

---

## Referências

- `docs/reference/BRIDGE_C1_C2_BUREAUS_CRIVO.md` — Mapa de bridges
- `docs/enrichment/` — Documentação de enriquecimento
- `docs/adr/` — Decisões arquiteturais
- `_domain/_docs/ENTITY_INDEX.yaml` — Índice de entidades
