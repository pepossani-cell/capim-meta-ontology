---
name: Clinic Health Check
description: Execute comprehensive health diagnostic for a specific clinic across all domains (CLIENT_VOICE, SAAS, FINTECH). Use when (1) user asks about problems with specific clinic, (2) user asks "what's wrong with clinic X?" or "o que há de errado com a clínica X?", (3) user requests clinic health status, (4) proactive health monitoring (scheduled/periodic), (5) investigating churn or metric deterioration. Implements RULE-CROSS-001 from INFERENCE_RULES.yaml. Cross-domain query that may be token-intensive.
version: 2.0
auto_invoke: ask_first
migrated_from: .agent/skills/clinic-health-check/SKILL.md
---

# Clinic Health Check Skill

Executa diagnóstico completo de saúde de uma clínica, sintetizando dados de múltiplos domínios (CLIENT_VOICE, SAAS, FINTECH).

**Implementa**: `ontology/INFERENCE_RULES.yaml` → RULE-CROSS-001 (Clinic Health Diagnostic)

## Quando Usar

Invoque esta skill quando:
- Usuário pergunta sobre problemas com uma clínica específica
- Usuário pergunta "what's wrong with clinic X?" ou "o que há de errado com a clínica X?"
- Usuário pede status de saúde de uma clínica
- Monitoramento proativo de saúde (agendado ou periódico)
- Investigação de churn ou deterioração de métricas

**Invocação**: `@clinic-health-check <clinic_id ou nome>` ou menção natural

## Prerequisites

1. `clinic_id` must be known or resolvable
2. Snowflake access configured
3. PostgreSQL access configured (for CLIENT_VOICE data)

## Reference

This skill implements: `ontology/INFERENCE_RULES.yaml` → RULE-CROSS-001

## Execution Steps

### 1. Resolve Clinic ID
If user provides clinic name, resolve to ID:
```sql
SELECT clinic_id FROM CLINICS WHERE name ILIKE '%{clinic_name}%'
```

### 2. Query CLIENT_VOICE (Support Health)
```sql
SELECT 
    COUNT(ticket_id) as ticket_count_90d,
    AVG(sentimento_score) as avg_sentiment,
    LISTAGG(DISTINCT categoria, ', ') as top_issues
FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.TICKET_ANALYSIS_V3
WHERE clinic_id = {clinic_id}
  AND event_date >= CURRENT_DATE() - 90
```

### 3. Query SAAS (Schedule Volume)
```sql
SELECT 
    COUNT(*) as appointment_count,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) as cancellation_rate
FROM SCHEDULES
WHERE clinic_id = {clinic_id}
  AND created_at >= CURRENT_DATE() - 90
```

### 4. Query FINTECH (Rejection Rate)
```sql
SELECT 
    COUNT(*) as total_simulations,
    SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) / COUNT(*) as rejection_rate
FROM CREDIT_SIMULATIONS
WHERE clinic_id = {clinic_id}
  AND created_at >= CURRENT_DATE() - 90
```

### 5. Synthesize Findings
Apply synthesis logic from RULE-CROSS-001:
- If ticket_count_90d > 5 AND avg_sentiment < 2.5: SUPPORT_CRISIS
- If churn_probability > 0.7: HIGH_CHURN_RISK
- If rejection_rate increased > 10pp: CREDIT_ISSUE

## Output Format

```markdown
## 🏥 Clinic Health Report: {clinic_name} (ID: {clinic_id})

### Overall Status: [CRITICAL / WARNING / HEALTHY]

### Support Health (CLIENT_VOICE)
- Tickets (90d): {count}
- Avg Sentiment: {score}/5
- Top Issues: {issues}

### Operational Health (SAAS)
- Appointments (90d): {count}
- Cancellation Rate: {rate}%
- Activity Trend: {trend}

### Credit Health (FINTECH)
- Simulations (90d): {count}
- Rejection Rate: {rate}%
- Top Rejection Reasons: {reasons}

### Recommendations
1. {recommendation_1}
2. {recommendation_2}
```

## Arquivos e Integração

**Scripts** (opcional, futuro):
- `scripts/check.py` - Script de execução automatizada (a implementar)

**Referências de Ontologia**:
- `../../ontology/INFERENCE_RULES.yaml` - Definição de RULE-CROSS-001
- `../../federation/CAPABILITY_MATRIX.yaml` - Mapeamento de capabilities por domínio

**Integração com Rules**:
- Usa Rule `ontology_reasoning.mdc` para validar resultados contra axioms
- Usa Rule `snowflake_protocol.mdc` para queries nos domínios
- Segue protocolo de multi-domain query routing

## Implementação Atual

Por enquanto, executar manualmente seguindo os passos acima usando:
- `run_query()` do `src/utils/snowflake_connection.py` para queries
- Síntese manual baseada em RULE-CROSS-001
- Future: Script Python automatizado

## Notas Técnicas

- **Performance**: ~3-5s para queries completas (3 domínios)
- **Fallback**: Se domínio não tiver dados, continuar com os outros
- **Cache**: Considerar cache de 5min para mesma clínica

## Referências

- **Rule**: `.cursor/rules/ontology_reasoning.mdc` (cross-domain protocol)
- **Rule**: `.cursor/rules/snowflake_protocol.mdc` (query execution)
- **Inference Rule**: `ontology/INFERENCE_RULES.yaml` → RULE-CROSS-001
- **Antigravity original**: `.agent/skills/clinic-health-check/` (legacy reference)
