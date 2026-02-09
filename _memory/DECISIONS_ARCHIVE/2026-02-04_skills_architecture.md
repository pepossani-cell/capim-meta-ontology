# 📁 Decision Archive: Skills Architecture (2026-02-04)

> **Archived**: 2026-02-04  
> **Session Focus**: Debate e implementação da arquitetura 3-Tier de Skills  
> **Related Files**: `SKILL_REGISTRY.yaml`, `SKILLS_PLAYBOOK.md`, `ARCHITECTURE_PRINCIPLES.md`

---

## Contexto

Debate iniciado a partir da análise do documento `SKILL_CREATOR.md` da Anthropic, questionando:
1. Se as skills atuais seguiam as recomendações
2. Se fazia sentido criar uma "constituição de skills"
3. Se os `docs/how_to` do ontologia-saas deveriam virar skills
4. Como funcionava a invocação (explícita vs espontânea)

O debate evoluiu para uma discussão arquitetural sobre **autonomia de projetos vs centralização**, resultando na **3-Tier Skill Architecture**.

---

## Decisões Arquivadas

### 13.1 Drift Skills Composition

- **Status**: ✅ Decided + Executed
- **Decision**: **Opção C (Composição)** — Tier 3 `@detect-*-drift` compõe Tier 2 `@investigate-entity`
- **Rationale**: Preserva autonomia: cada domínio define thresholds locais enquanto reutiliza profiling genérico
- **Executed On**: 2026-02-04
- **Related Files**:
  - `ontologia-saas/.cursor/skills/detect-saas-drift/SKILL.md`
  - `bnpl-funil/.cursor/skills/detect-fintech-drift/SKILL.md`
  - `capim-meta-ontology/.cursor/skills/detect-drift/SKILL.md`

---

### 13.2 Drift Cross vs Intra-Domain

- **Status**: ✅ Decided + Executed
- **Decision**: Tier 2 `@detect-drift` = cross-domain axioms; Tier 3 `@detect-*-drift` = intra-domain thresholds
- **Rationale**: Two-layer architecture separa responsabilidades: federação (Tier 2) vs domínio (Tier 3)
- **Executed On**: 2026-02-04
- **Related Files**:
  - `capim-meta-ontology/.cursor/skills/detect-drift/references/cross_domain_thresholds.yaml`
  - `ontologia-saas/.cursor/skills/detect-saas-drift/references/SAAS_DRIFT_THRESHOLDS.yaml`
  - `bnpl-funil/.cursor/skills/detect-fintech-drift/references/FINTECH_DRIFT_THRESHOLDS.yaml`

---

### 13.3 Materialize Skill Tier

- **Status**: ✅ Decided + Executed
- **Decision**: **Promover para Tier 2 (Shared)**: `@materialize-view` genérico
- **Rationale**: Todos os projetos de data/ontology precisam materializar views; skill fornece o HOW, domínio decide o WHAT
- **Executed On**: 2026-02-04
- **Related Files**:
  - `capim-meta-ontology/.cursor/skills/materialize-view/SKILL.md`
  - `capim-meta-ontology/.cursor/skills/materialize-view/references/strategy_decision_tree.md`

---

### 13.4 Materialize Extensions

- **Status**: ✅ Decided + Executed
- **Decision**: Extensions por domínio em `references/materialize_<domain>.md`
- **Rationale**: Preserva autonomia arquitetural — cada domínio lista suas views candidatas e padrões específicos
- **Executed On**: 2026-02-04
- **Related Files**:
  - `capim-meta-ontology/.cursor/skills/materialize-view/references/materialize_saas.md`
  - `capim-meta-ontology/.cursor/skills/materialize-view/references/materialize_fintech.md`
  - `capim-meta-ontology/.cursor/skills/materialize-view/references/materialize_client_voice.md`

---

### 13.5 Snowflake Validation for Skills

- **Status**: ✅ Decided + Executed
- **Decision**: Incluído no `SKILLS_PLAYBOOK.md` — Seção "Validação Snowflake-First"
- **Rationale**: Skills de dados devem ser validadas no Snowflake antes de marcar como `active`. Dois cenários: (A) queries existem, (B) agente precisa construir queries usando ontologia.
- **Executed On**: 2026-02-04
- **Related Files**:
  - `capim-meta-ontology/SKILLS_PLAYBOOK.md` (seção 🧪 Validação Snowflake-First)

---

### 13.6 EDA Workflow Scope

- **Status**: ✅ Decided + Executed
- **Decision**: **Opção C Refinada (FST + Debate)** — Core FST com 3 estados (TATEANTE → CALIBRAR → ESTÁVEL) + guardrails de ambiguidade + extensions por domínio
- **Rationale**: 
  - EDA é "errático, volátil, cíclico" por natureza
  - FST (Finite-State Transducer) modela estados e transições
  - Debate integrado como guardrail quando ambiguidade detectada
  - Baseado em: OpenAI Agents Guide (2025), DatawiseAgent FST (EMNLP 2025)
- **Executed On**: 2026-02-04
- **Related Files**:
  - `capim-meta-ontology/.cursor/skills/eda-workflow/SKILL.md`
  - `capim-meta-ontology/.cursor/skills/eda-workflow/references/fst_transitions.md`
  - `capim-meta-ontology/.cursor/skills/eda-workflow/references/debate_triggers.md`
  - `capim-meta-ontology/.cursor/skills/eda-workflow/references/eda_saas.md`
  - `capim-meta-ontology/.cursor/skills/eda-workflow/references/eda_fintech.md`
  - `capim-meta-ontology/.cursor/skills/eda-workflow/references/eda_client_voice.md`

---

## Arquitetura Resultante

### 3-Tier Skill Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIER 1: CORE (Immutable)                      │
│  session-start │ session-end │ debate │ curate-memory           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TIER 2: SHARED (Extensible)                     │
│  investigate-entity │ validate-axioms │ clinic-health-check     │
│  eda-workflow       │ detect-drift    │ materialize-view        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  TIER 3: SAAS │     │ TIER 3: FINTECH│     │TIER 3: CLIENT │
│  (4 skills)   │     │  (5 skills)    │     │  (3 skills)   │
└───────────────┘     └───────────────┘     └───────────────┘
```

### Status Final

| Status | Count |
|--------|-------|
| stable | 7 |
| active | 12 |
| planned | 3 (P4 only) |

---

## Padrões Descobertos

1. **Composição > Herança**: Skills Tier 3 compõem Tier 2, não herdam
2. **Extensions preservam autonomia**: Domínio decide thresholds/candidatos
3. **FST para workflows iterativos**: Estados explícitos + transições + guardrails
4. **Debate como guardrail**: Ambiguidade → invocar @debate automaticamente
5. **Hybrid EN/PT-BR**: YAML em inglês, conteúdo em português

---

## Pendências Remanescentes (P4)

- `@analyze-financial-ops` (SAAS)
- `@classify-support-issues` (CLIENT_VOICE)

---

## Referências

- `SKILL_REGISTRY.yaml` — Catálogo completo
- `SKILLS_PLAYBOOK.md` — Guia de criação
- `ARCHITECTURE_PRINCIPLES.md` — Tensão autonomia vs globalismo
- OpenAI: A Practical Guide to Building Agents (2025)
- DatawiseAgent: FST-Based Framework (EMNLP 2025)
