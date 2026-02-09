# LESSONS LEARNED

> **Purpose**: Consolidated patterns and insights extracted from past decisions.
> **Status**: Living document — updated when decisions are archived.
> **Last Updated**: 2026-02-01

---

## 🏗️ Architecture & Structure

### Naming Conventions
- **Underscore prefix** (`_domain/`, `_memory/`, `_docs/`) indicates meta/system folders
- **No temporal suffixes** (`_REFACTOR`, `_V2`) in file names — use Git for versioning
- **UPPERCASE** for concept files (ENTITY_INDEX.yaml), **lowercase** for code (connection.py)
- **Descriptive names** over abbreviations (DECISIONS_IN_PROGRESS.md not DIP.md)

### Project Organization
- Each domain should have a `_domain/` folder with local ontology
- Shared/global ontology lives in `capim-meta-ontology`
- `START_HERE.md` is the canonical entry point for any domain

---

## 💾 Data Layer

### Hot vs Cold Pattern
- **PostgreSQL (Hot)**: Operational data, low latency, real-time writes
- **Snowflake (Cold)**: Analytics, cross-domain joins, historical data
- ETL responsibility: Data Engineering team mirrors PG → Snowflake

### Cross-Domain Joins
- `clinic_id` is the universal join key between SAAS and FINTECH
- `cpf` (not patient_id) for joining patient data across domains
- Time-based joins require window logic (e.g., ±15 days for bureau association)

### Zendesk Tables Hierarchy (2026-02-02)
**Descoberta durante investigação de entidades CLIENT_VOICE:**

| Tabela | Rows | clinic_id | Propósito |
|:---|---:|:---:|:---|
| SOURCE_ZENDESK_TICKETS | 430K | ❌ | Raw tickets via Hevo (17 cols) |
| SOURCE_ZENDESK_COMMENTS | 3.9M | ❌ | Raw comments via Hevo (13 cols, ~9/ticket) |
| ZENDESK_TICKETS_RAW | 430K | ✅ (46%) | Tickets enriquecidos (63 cols) |
| ZENDESK_TICKETS | 431K | ❌ | Métricas CX consolidadas (44 cols) |

**Lições**:
- Para análise **por clínica**: usar `ZENDESK_TICKETS_RAW` — única com `clinic_id`
- Para **classificação de conteúdo**: usar `SOURCE_ZENDESK_TICKETS` + `SOURCE_ZENDESK_COMMENTS` (raw text)
- O JOIN é via `TICKET_ID` entre tickets e comments
- 72% dos comments são públicos (visíveis ao cliente), 28% são privados (internos)

### ZENDESK_TICKETS vs ZENDESK_TICKETS_RAW (2026-02-02)
**Análise das queries dbt revelou propósitos distintos:**

| Aspecto | ZENDESK_TICKETS_RAW | ZENDESK_TICKETS |
|:---|:---|:---|
| **Foco** | Agent performance & satisfaction | CX metrics & templates |
| **clinic_id** | ✅ Via COALESCE de 3 fontes | ❌ Usa external_id via user_type |
| **Métricas principais** | Tempo Claudia vs analista, satisfaction changes | Reopens, template timing, contact |
| **Colunas** | 63 (mais detalhado) | 44 (mais consolidado) |

**Quando usar qual**:
- `_RAW`: Análise de performance de agentes, satisfação, atribuição por clínica
- `_TICKETS`: Análise de templates Droz, taxa de contato, reabertura

### clinic_id Inference — Limitações Estruturais (2026-02-02)
**Investigação revelou:**

- **37.8%** vem de `org_external_id` (organização Zendesk)
- **8.6%** vem de `lu_clinic_id` (via source_requests)
- **0%** vem de `dash_clinic_id` — **código morto!**
- **92.4%** dos tickets sem clinic_id não têm org NEM user_id válido

**Por que `dash_clinic_id` não contribui:**
O campo `user_email` em `source_dash_users` está **HASHEADO (SHA-256)** por razões de privacidade/LGPD. O JOIN compara emails reais com hashes, logo nunca encontra match.

**🟢 SOLUÇÃO: Usar RESTRICTED.USERS_SENSITIVE_INFORMATION**
- Tabela com `user_email` **NÃO hasheado** + `clinic_id`
- Potencial de melhoria: **46% → 50%** fill rate (+17K tickets)
- Proposta: substituir `source_dash_users` por `RESTRICTED.USERS_SENSITIVE_INFORMATION` no dbt

**Conclusão**: O fill rate atual é uma **limitação estrutural do Zendesk**, mas pode ser melhorado em +4pp com a tabela RESTRICTED.

### droz_template Divergence Risk (2026-02-02)
**Problema**: A lógica de mapeamento `tags → droz_template` está duplicada em:
- `zendesk_tickets_raw.sql` (linhas 41-105)
- `zendesk_tickets.sql` (linhas 38-94)

**Divergência já existe!** O template `horario_atendimento_ccc` só existe em `ZENDESK_TICKETS`.

**Impacto**: Contagens de `is_ticket_from_template` diferem entre tabelas.

**Ao documentar entidades**: Incluir seção de ⚠️ Caveats alertando sobre esta divergência.

---

## 🤖 Agent Behavior

### Proactiveness
- Agent should propose optimizations when patterns emerge
- Agent should suggest memory consolidation after complex debates
- Agent should reference Constitution before modifying ontology

### Communication
- Be honest about limitations
- Ask for confirmation before large changes
- Use structured formats (tables, diagrams) for complex topics

---

## 📝 Decision-Making

### Debate Process
1. Present options with trade-offs (pros/cons table)
2. Make a recommendation with rationale
3. Wait for user confirmation
4. **IMMEDIATELY** document decision in DECISIONS_IN_PROGRESS.md ← CRITICAL
5. Continue debate or archive when complete

### ⚠️ Lesson: Immediate Decision Tracking (2026-02-02)
**Problem:** Durante debates longos com múltiplas questões (Q1, Q2, Q3...), o agente tende a "esquecer" de atualizar DECISIONS_IN_PROGRESS.md após cada confirmação, focando no fluxo da discussão.

**Solução:**
- Quando usuário confirma ("sim", "ok", "confirmado"), **parar** e atualizar o arquivo ANTES de continuar
- Não esperar o fim do debate para consolidar — cada decisão individual é um checkpoint
- Se o debate se ramificar (Q2 → Q2b → Q2c), cada sub-decisão também deve ser registrada

**Trigger words que indicam confirmação:**
- "sim", "ok", "confirmado", "aprovado", "pode fazer", "vamos com X"

### What Makes a Good Decision Record
- **Context**: Why are we deciding this?
- **Options**: What alternatives exist?
- **Decision**: What did we choose?
- **Rationale**: Why this option?
- **Consequences**: What follows from this?

---

## 🔧 Tooling

### n8n vs Local Agents
- Use n8n for **batch, scheduled, autonomous** processing
- Use local agents for **interactive, ad-hoc, exploratory** tasks
- Hybrid approach: n8n processes, agents analyze

### Antigravity Features
- **Workflows** (`.agent/workflows/`): Reproducible multi-step procedures
- **Skills** (`.agent/skills/`): Specialized capabilities with scripts
- **User Rules**: Persistent behavioral instructions (if available in IDE settings)

### Session Model (Decision-Centric)
- **Don't wait for "session end"** to save decisions — save immediately when confirmed
- **Start conversations** by loading `_memory/DECISIONS_IN_PROGRESS.md`
- **Session-end workflow** is optional, for consolidation only
- **Rationale**: Agent doesn't remember previous conversations; saving immediately reduces context loss risk

---

### Snowflake-First Investigation (2026-02-03)
**Context:** During Zendesk analysis, samples of 50 or 200 tickets failed to show the "B2C Debt Collection" pattern. Only increasing to 2000+ or running aggregations on the full 100k+ dataset revealed the truth.
**Lesson:**
- **Local Sampling is biased/insufficient** for spotting "long-tail" phenomena that accumulate massive volume (like B2C tickets masked as ghosts).
- **Process**: Always run `SELECT ... GROUP BY` on Snowflake to profile the FULL POPULATION before downloading samples.
- **Rule**: "If you didn't query the population, you don't know the distribution."

### Federated Ontology Awareness (2026-02-03)
**Context:** Agents working in `client-voice` were unaware of entities defined in `bnpl-funil` or `ontologia-cf` because they only looked at local files.
**Lesson:**
- Renaming `ONTOLOGY_INDEX.yaml` to `ONTOLOGY_INDEX_DOMAIN.yaml` forces the agent to realize it's looking at a PARTIAL view.
- Explicit headers (`# ⚠️ PARTIAL INDEX`) prevent "context myopia".

### Identity Resolution in Zendesk (2026-02-03)
**Context:** Identifying "Ghost tickets" (tickets with no Clinic ID).
**Lessons:**
- **Role Clarity**: `ticket.end_user_id` is ALWAYS the Customer (Patient/Staff). `ticket.assignee_id` is ALWAYS the Agent. Matches against `SOURCE_ZENDESK_USERS` confirmed this 100%.
- **Indirect Linkage**: B2C tickets often lack explicit keys (like `clinic_id`). The "Golden Path" requires a multi-hop join: `Ticket -> ZendeskUser -> PlatformUser -> DebtContext`.
- **Optimization**: Splitting complex OR conditions (Match by ID OR Match by CPF) into separate LEFT JOINs + COALESCE reduced query time from >14m to ~1m.

### Value of Legacy Data (2026-02-03)
**Context:** Debate on whether to ignore `PRE_ANALYSES` (Legacy) in favor of cleanliness.
**Finding:**
- A hybrid matching strategy (New Flow via ID + Legacy Flow via CPF) revealed **R$ 36.2M** in debt exposure in support tickets.
- **R$ 28M (77%)** of this value came from the "Legacy" flow.
**Lesson:**
- "Legacy" does not mean "Obsolete". In Fintech, legacy cohorts often hold the highest operational risk/value (e.g., long-tail debt).
- **Rule**: Never deprecate a data source without quantifying the value at risk (VAR) residing in it. Pre-Analyses must remain a First-Class Citizen in our Ontology.

### Crivo Ecosystem — Three Distinct Entities (2026-02-05)
**Context:** Profiling `SOURCE_CRIVO_CHECKS` (208K rows) as the canonical Crivo source.
**Finding:**
- `CREDIT_CRIVO_CREDIT_CHECKS` (CAPIM_ANALYTICS, 2.1M rows, 74 cols) is the **main** curated table — 10x larger, since 2022, with full risk classification.
- `SOURCE_CRIVO_CHECKS` (SOURCE_STAGING, 208K rows, 30 cols) is **raw staging** — only since Jan/2025, but has direct FK to CREDIT_SIMULATIONS.
- `CRIVO_PF_PJ_PRODUCTION_FULL_CSVS` (RESTRICTED, 2.3M rows) covers **legacy pre-analyses** — completely separate system.
**Lessons:**
- **Never assume a single table name corresponds to a single entity.** Always search for related tables across all schemas before documenting.
- The entity name in documentation ("CRIVO_CHECKS") masked an entire ecosystem of 3+ distinct tables with different purposes, schemas, and coverage.
- **Rule**: When investigating any SOURCE entity, run `ILIKE '%<keyword>%'` across INFORMATION_SCHEMA first.

### hash_cpf Reversal Pattern (2026-02-05)
**Context:** `CREDIT_CRIVO_CREDIT_CHECKS.hash_cpf` appeared to be an irreversible hash, blocking linkage to credit_simulations.
**Finding:**
- `hash_cpf = SHA2(digits_only_cpf, 256)` — confirmed 97.3% match via PATIENTS CPF.
- The 2.7% "mismatches" are **financial_responsible** CPF (not patient). The Crivo engine evaluates the FR when present.
- Coverage via ±24h window: 65% overall, but **95% in peak months** (Feb-May 2025) and **~38% from Sep 2025+** (pipeline change).
- 30% of CS have **no Crivo record at all** because they were rejected before the engine ran (negativation, age, clinic_rating).
**Lessons:**
- **"Hash reversal" is really "hash reproduction"**: when you have the source data (PATIENTS.cpf), you can reproduce the hash and join.
- **Effective person logic matters**: always check BOTH patient_id and financial_responsible_id when bridging person-level data.
- **Coverage drops can be pipeline changes, not data quality issues.** The Sep 2025 drop correlates in both SOURCE_CRIVO_CHECKS volume and ANALYTICS coverage.

### Entity Documentation — Dual Location Pattern (2026-02-05)
**Context:** Projects had inconsistent documentation structure — some with both doc types in `_domain/_docs/reference/`, others split differently.
**Finding:**
- Mixing **semantic** (business context) and **agentic** (data dictionary) docs in the same folder causes confusion about file purpose.
- Semantic docs are for **AI reasoning** (why, relationships, caveats). Data dictionaries are for **query execution** (schema, columns, types).
**Decision:**
| Doc Type | Location | Suffix | Audience |
|:---------|:---------|:-------|:---------|
| Semantic | `_domain/_docs/reference/` | `*_SEMANTIC.md` | AI agents, analysts |
| Data Dictionary | `docs/reference/` | `*.md` (no suffix) | Developers, data engineers |

**Enforcement:**
1. **Cursor Rule**: `.cursor/rules/entity_documentation.mdc` auto-applies on relevant globs
2. **Skill**: `@investigate-entity` generates both files in correct locations
3. **Validation Script**: PowerShell script checks pairing completeness

**Applied to:** `bnpl-funil`, `client-voice-data`, `ontologia-saas`

*This document is updated as new patterns are identified.*
