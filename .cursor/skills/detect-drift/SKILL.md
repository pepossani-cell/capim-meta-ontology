---
name: Detect Drift
description: Detect CROSS-DOMAIN drift in federation axioms and shared entities. Use when (1) validating cross-domain consistency, (2) clinic/entity exists in one domain but not another, (3) metrics diverge between domains, (4) after major data pipeline changes, (5) user mentions "drift", "divergência", "inconsistência cross-domain". Validates semantic consistency across domains. For INTRA-domain drift, use domain-specific skills (@detect-saas-drift, @detect-fintech-drift).
version: 1.0
auto_invoke: silent
composes: [investigate-entity]
used_by: [saas, fintech, client_voice]
scope: cross-domain
---

# Detect Drift Skill

Detecta drift **CROSS-DOMAIN** em axiomas de federação e entidades compartilhadas entre domínios (SAAS, FINTECH, CLIENT_VOICE).

## Escopo

### Esta Skill Cobre (Cross-Domain)

- Entidades que **devem existir** em múltiplos domínios (ex: clinic_id)
- Métricas que **devem concordar** entre domínios
- Axiomas de **federação** (CROSS_DOMAIN_GLUE.yaml)
- Consistência de **timestamps** entre eventos cross-domain

### NÃO Cobre (Use Skills de Domínio)

- Drift **intra-domínio** (ex: score normalization em FINTECH)
- Thresholds **específicos** de um domínio
- Validações que não envolvem cruzamento

**Para drift intra-domínio**, use:
- `@detect-saas-drift` (Tier 3)
- `@detect-fintech-drift` (Tier 3)
- `@detect-client-voice-drift` (Tier 3)

---

## Quando Usar

Invoque esta skill quando:
- Validando consistência cross-domain periodicamente
- Entidade aparece em um domínio mas não em outro
- Métricas divergem entre domínios sem explicação
- Após mudanças em pipelines de dados
- Debugging de análises cross-domain

**Invocação**: `@detect-drift` ou menção natural ("verificar drift", "divergência entre domínios")

---

## Axiomas de Federação

### Entidades Compartilhadas

| Entidade | Domínios | Axioma |
|----------|----------|--------|
| `clinic_id` | SAAS, FINTECH, CLIENT_VOICE | Deve existir em SAAS se existir em qualquer outro |
| `CPF` | SAAS (pacientes), FINTECH (borrowers) | Join via clinic_id, não direto |

### Regras de Glue

```yaml
# _federation/CROSS_DOMAIN_GLUE.yaml

glue_rules:
  - name: "Clinic exists in SAAS if has FINTECH activity"
    left: FINTECH.credit_simulations.clinic_id
    right: SAAS.clinics.id
    type: LEFT_MUST_EXIST_IN_RIGHT
    tolerance: 0%  # Hard axiom
    
  - name: "Clinic exists in SAAS if has tickets"
    left: CLIENT_VOICE.tickets.clinic_id
    right: SAAS.clinics.id
    type: LEFT_MUST_EXIST_IN_RIGHT
    tolerance: 0%  # Hard axiom
```

---

## Tipos de Drift

### 1. Entity Presence Drift

**Sintoma**: Entidade existe em domínio A mas não em B.

```sql
-- Clinics com atividade FINTECH mas sem registro SAAS
SELECT DISTINCT cs.clinic_id
FROM FINTECH.credit_simulations cs
LEFT JOIN SAAS.clinics c ON cs.clinic_id = c.id
WHERE c.id IS NULL;

-- Se retornar rows: DRIFT DETECTADO
```

**Severidade**: 🔴 Alta (viola axioma hard)

---

### 2. Metric Consistency Drift

**Sintoma**: Mesma métrica calculada diferente em domínios distintos.

```sql
-- Contagem de clínicas ativas por domínio
SELECT 'SAAS' as domain, COUNT(DISTINCT clinic_id) as n
FROM SAAS.clinics WHERE status = 'active'
UNION ALL
SELECT 'FINTECH' as domain, COUNT(DISTINCT clinic_id) as n
FROM FINTECH.credit_simulations 
WHERE created_at >= DATEADD(month, -3, CURRENT_DATE)
UNION ALL
SELECT 'CLIENT_VOICE' as domain, COUNT(DISTINCT clinic_id) as n
FROM CLIENT_VOICE.tickets
WHERE created_at >= DATEADD(month, -3, CURRENT_DATE);

-- Divergência > 10%: investigar
```

**Severidade**: 🟡 Média (pode ter explicação legítima)

---

### 3. Temporal Consistency Drift

**Sintoma**: Eventos cross-domain fora de ordem esperada.

```sql
-- Simulações de crédito antes da clínica existir em SAAS
SELECT 
    cs.clinic_id,
    cs.created_at as simulation_at,
    c.created_at as clinic_created_at,
    DATEDIFF(day, c.created_at, cs.created_at) as days_diff
FROM FINTECH.credit_simulations cs
JOIN SAAS.clinics c ON cs.clinic_id = c.id
WHERE cs.created_at < c.created_at;

-- Se days_diff < -1: possível problema de timestamp
```

**Severidade**: 🟡 Média (pode ser timezone ou backfill)

---

### 4. Semantic Drift

**Sintoma**: Mesmo campo tem significado diferente entre domínios.

```sql
-- 'status' em SAAS vs 'status' em FINTECH
SELECT DISTINCT status, COUNT(*) FROM SAAS.clinics GROUP BY 1;
SELECT DISTINCT status, COUNT(*) FROM FINTECH.credit_simulations GROUP BY 1;

-- Se domínios de valores divergem: documentar mapeamento
```

**Severidade**: 🟠 Média-Alta (requer documentação de mapeamento)

---

## Workflow de Detecção

### Passo 1: Identificar Entidades Cross-Domain

```sql
-- Listar entidades que aparecem em múltiplos domínios
-- Usar ENTITY_INDEX.yaml de cada domínio
```

**Invoke `@investigate-entity`** para profiling se necessário.

---

### Passo 2: Executar Checks de Presença

```sql
-- Template: Entity Presence Check
WITH domain_a AS (
    SELECT DISTINCT <entity_id> FROM <DOMAIN_A>.<table>
),
domain_b AS (
    SELECT DISTINCT <entity_id> FROM <DOMAIN_B>.<table>
)
SELECT 
    'A_not_in_B' as drift_type,
    COUNT(*) as drift_count
FROM domain_a a
LEFT JOIN domain_b b ON a.<entity_id> = b.<entity_id>
WHERE b.<entity_id> IS NULL
UNION ALL
SELECT 
    'B_not_in_A' as drift_type,
    COUNT(*) as drift_count
FROM domain_b b
LEFT JOIN domain_a a ON b.<entity_id> = a.<entity_id>
WHERE a.<entity_id> IS NULL;
```

---

### Passo 3: Executar Checks de Consistência

```sql
-- Template: Metric Consistency Check
SELECT 
    '<metric_name>' as metric,
    domain,
    value,
    AVG(value) OVER () as avg_value,
    ABS(value - AVG(value) OVER ()) / NULLIF(AVG(value) OVER (), 0) as pct_deviation
FROM (
    SELECT 'DOMAIN_A' as domain, <metric_calc> as value FROM <DOMAIN_A>.<table>
    UNION ALL
    SELECT 'DOMAIN_B' as domain, <metric_calc> as value FROM <DOMAIN_B>.<table>
) metrics;

-- pct_deviation > 0.1 (10%): investigar
```

---

### Passo 4: Classificar e Documentar

| Drift Encontrado | Severidade | Ação |
|------------------|------------|------|
| Entity Presence (hard axiom) | 🔴 Alta | Escalar imediatamente |
| Metric > 20% divergência | 🟠 Média-Alta | Investigar causa |
| Metric 10-20% divergência | 🟡 Média | Documentar e monitorar |
| Metric < 10% divergência | 🟢 Baixa | Aceitar como variação |

---

### Passo 5: Criar Audit Query

Se drift é significativo, criar query permanente:

```sql
-- queries/audit/federation/audit_<drift_name>_v1.sql

/*
=============================================================================
DRIFT AUDIT: <drift_name>
=============================================================================
Detected: <date>
Domains: <DOMAIN_A>, <DOMAIN_B>
Axiom: <axiom_violated>
Severity: <HIGH/MEDIUM/LOW>
Expected: <expected_behavior>
Threshold: <tolerance>
=============================================================================
*/

<query>

-- Expected result: 0 rows (or value within threshold)
```

---

## Thresholds Cross-Domain

```yaml
# references/cross_domain_thresholds.yaml

entity_presence:
  clinic_id:
    tolerance: 0%  # Hard axiom
    domains: [SAAS, FINTECH, CLIENT_VOICE]
    
metric_consistency:
  active_clinic_count:
    tolerance: 10%
    check_frequency: weekly
    domains: [SAAS, FINTECH]
    
  ticket_volume:
    tolerance: 20%  # Higher due to support seasonality
    check_frequency: monthly
    domains: [CLIENT_VOICE]

temporal_consistency:
  event_order:
    tolerance: 1 day  # Timezone buffer
    domains: [all]
```

---

## Output Format

### Drift Report

```markdown
# Drift Report — <date>

## Summary

| Check | Status | Count | Severity |
|-------|--------|-------|----------|
| Clinic Presence SAAS↔FINTECH | ✅ OK | 0 | - |
| Clinic Presence SAAS↔CLIENT_VOICE | ⚠️ DRIFT | 15 | 🟡 Medium |
| Active Count Consistency | ✅ OK | 3% dev | - |

## Details

### Clinic Presence SAAS↔CLIENT_VOICE

**Drift detectado**: 15 clinic_ids em CLIENT_VOICE sem correspondente em SAAS.

**Sample**:
| clinic_id | first_ticket_at | ticket_count |
|-----------|-----------------|--------------|
| 12345 | 2025-06-01 | 3 |
| 67890 | 2025-07-15 | 1 |

**Possíveis causas**:
1. Clinics deletadas em SAAS mas com histórico de tickets
2. Dados de teste não limpos
3. Bug em pipeline de sync

**Próximos passos**:
- [ ] Investigar sample de clinic_ids
- [ ] Verificar se são clinics de teste
- [ ] Criar exclusão se legítimo

## Actions

- [ ] Investigar drift CLIENT_VOICE
- [ ] Agendar próximo check: <date + 1 week>
```

---

## Composição com Outras Skills

| Situação | Skill a Invocar |
|----------|-----------------|
| Entidade desconhecida | `@investigate-entity` |
| Precisa de mais contexto | `@eda-workflow` (estado TATEANTE) |
| Decisão sobre threshold | `@debate` |
| Drift intra-SAAS | `@detect-saas-drift` |
| Drift intra-FINTECH | `@detect-fintech-drift` |

---

## Anti-Patterns

❌ **Não faça**:
- Ignorar drift "pequeno" sem documentar
- Assumir que drift é bug sem investigar
- Criar audit queries sem threshold claro
- Misturar checks cross-domain com intra-domain

✅ **Faça**:
- Documentar TODO drift encontrado
- Investigar antes de escalar
- Definir thresholds explícitos
- Usar skills de domínio para drift intra

---

## Scheduled Checks

### Semanal (Recomendado)

```sql
-- Run every Monday 9h BRT
-- queries/audit/federation/weekly_drift_check.sql

SELECT * FROM audit_clinic_presence_saas_fintech_v1;
SELECT * FROM audit_clinic_presence_saas_client_voice_v1;
SELECT * FROM audit_metric_consistency_active_clinics_v1;
```

### Pós-Deploy

Após mudanças em pipelines, executar todos os checks.

---

## Referências

- `_federation/CROSS_DOMAIN_GLUE.yaml` — Regras de glue
- `_federation/CAPABILITY_MATRIX.yaml` — O que cada domínio responde
- `.cursor/rules/ontology_reasoning.mdc` — Protocolo de raciocínio
- `@investigate-entity` skill — Para profiling
- `@detect-*-drift` skills (Tier 3) — Para drift intra-domínio
