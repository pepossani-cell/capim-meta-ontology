# EDA Extensions — CLIENT_VOICE Domain

> **Purpose**: Padrões específicos de EDA para o domínio CLIENT_VOICE (VoC)  
> **Base Skill**: `@eda-workflow` (Tier 2)  
> **Domain**: client-voice-data

---

## Estrutura de Estudos CLIENT_VOICE

```
client-voice-data/
├── eda/
│   └── <nome_estudo>/
│       ├── README.md           # Incertezas, perguntas abertas
│       ├── scratchpad.sql      # Queries exploratórias
│       ├── *CONTRATO*.md       # Contrato de saída (quando ESTÁVEL)
│       └── DECISION_TREE.md    # Árvore de decisões (quando ESTÁVEL)
├── queries/
│   ├── zendesk/                # Queries de extração/análise
│   └── audit/                  # Microtests
└── docs/
    └── reference/              # Semântica de entidades
```

---

## Entidades Frequentes em EDA CLIENT_VOICE

| Entidade | Tabela/View | Grain | Doc Semântica |
|----------|-------------|-------|---------------|
| Ticket | `TICKET_ANALYSIS_V3` | ticket_id | `docs/reference/TICKET_ANALYSIS.md` |
| Category | (derivado) | category | LLM-classified |
| Subcategory | (derivado) | subcategory | LLM-classified |
| Sentiment | (derivado) | sentiment_score | 1-5 scale |

---

## Padrões de Análise CLIENT_VOICE

### 1. Análise de Sentiment Trends

**Universo típico**:
```sql
-- Tickets no período, excluindo spam/test
SELECT *
FROM TICKET_ANALYSIS_V3
WHERE created_at BETWEEN @start_date AND @end_date
  AND category NOT IN ('spam', 'test')
  AND clinic_id IS NOT NULL
```

**Métricas**:
- Sentiment médio por categoria
- Volume de tickets por categoria
- Trend de sentiment ao longo do tempo

**Debate triggers comuns**:
- "Ticket sem categoria entra na análise?"
- "Sentiment NULL — assumir neutro ou excluir?"

**Skill relacionada**: `@analyze-voc-sentiment`

---

### 2. Análise por Persona (B2B vs B2C)

**Universo típico**:
```sql
-- Separar tickets por tipo de requester
SELECT 
    CASE 
        WHEN requester_type = 'clinic' THEN 'B2B'
        WHEN requester_type = 'patient' THEN 'B2C'
        ELSE 'unknown'
    END as persona,
    category,
    AVG(sentiment_score) as avg_sentiment,
    COUNT(*) as ticket_count
FROM TICKET_ANALYSIS_V3
WHERE created_at >= @start_date
GROUP BY 1, 2
```

**Debate triggers comuns**:
- "Requester_type confiável? Como classificado?"
- "'Unknown' entra em qual grupo?"

---

### 3. Correlação com Eventos SAAS/FINTECH

**Universo típico**:
```sql
-- Tickets de clinics que tiveram evento específico
SELECT 
    t.*,
    e.event_type,
    e.event_date
FROM TICKET_ANALYSIS_V3 t
JOIN SAAS.clinic_events e ON t.clinic_id = e.clinic_id
  AND t.created_at BETWEEN e.event_date AND DATEADD(day, 7, e.event_date)
WHERE e.event_type IN ('subscription_cancelled', 'payment_failed')
```

**Debate triggers comuns**:
- "Janela de correlação — 7 dias é adequado?"
- "Causalidade vs correlação — como documentar?"

**Skill relacionada**: `@correlate-tickets-events`

---

## Thresholds CLIENT_VOICE

```yaml
# Thresholds específicos do domínio CLIENT_VOICE

sentiment:
  scale: [1, 2, 3, 4, 5]
  neutral_range: [2.5, 3.5]
  negative_threshold: 2.5
  positive_threshold: 3.5
  
volume:
  high_volume_clinic: 10  # tickets/mês
  crisis_threshold: 5  # tickets negativos/semana
  
correlation:
  event_window_days: 7  # dias após evento
  min_tickets_for_pattern: 3  # mínimo para considerar padrão
  
classification:
  confidence_threshold: 0.7  # LLM confidence mínima
  categories_expected: [
    "billing", "technical", "product", "support", 
    "cancellation", "onboarding", "feature_request"
  ]
```

---

## Promoção de Achados CLIENT_VOICE

### Para Microtest (Axiom)

```sql
-- queries/audit/client_voice/audit_sentiment_range_v1.sql
-- Axiom: AX-CV-002 (sentiment in [1,5])
-- Esperado: 0 rows

SELECT ticket_id, sentiment_score
FROM TICKET_ANALYSIS_V3
WHERE sentiment_score NOT BETWEEN 1 AND 5
  OR sentiment_score IS NULL
```

### Para Taxonomia

```markdown
# docs/reference/CATEGORY_TAXONOMY.md

## Categorias de Tickets

| Categoria | Descrição | Volume Esperado |
|-----------|-----------|-----------------|
| billing | Problemas de cobrança | 15-25% |
| technical | Bugs e erros técnicos | 20-30% |
| product | Dúvidas sobre produto | 10-20% |
| ...

## Descobertas em EDA

- [data]: "billing" inclui tanto B2B (clínica) quanto B2C (paciente)
- [data]: "cancellation" tem sentiment médio de 1.8
```

---

## Skills Relacionadas (CLIENT_VOICE)

| Situação | Skill |
|----------|-------|
| Análise de sentiment | `@analyze-voc-sentiment` |
| Correlação cross-domain | `@correlate-tickets-events` |
| Health check de clinic | `@clinic-health-check` |
| Classificação manual | `@classify-support-issues` (planned) |

---

## Especificidades de Dados

### Timezone

Zendesk retorna timestamps em **America/Sao_Paulo** (BRT). Não precisa converter.

```sql
-- Verificar: já está em BRT
SELECT created_at, 
       CONVERT_TIMEZONE('UTC', 'America/Sao_Paulo', created_at) as converted
FROM TICKET_ANALYSIS_V3
LIMIT 5;
-- Se iguais, já está em BRT
```

### LLM Classification

- Classificação é feita por LLM no pipeline n8n
- Confidence score disponível em algumas colunas
- Re-classificação manual possível via `@classify-support-issues`

---

## Referências

- `docs/reference/TICKET_ANALYSIS.md` — Semântica da tabela principal
- `_domain/_docs/ENTITY_INDEX.yaml` — Índice de entidades
- `workflows/v3_*.json` — Pipelines de ETL
