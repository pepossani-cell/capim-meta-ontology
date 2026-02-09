# DECISIONS IN PROGRESS

> **Purpose**: Track ongoing architectural decisions, debates, and action items.
> **Status**: Living document — updated as decisions are made or change.
> **Last Updated**: 2026-02-05


---

## 📋 DECISION TRACKER

### Legend
- ✅ **Decided**: Agreement reached, ready for execution
- ✅➡️ **Executed**: Decided AND implemented — ready to archive
- ⏳ **Pending**: Awaiting confirmation or more information
- 🔄 **In Debate**: Actively discussing options
- ❌ **Rejected**: Decided against this option — ready to archive

> **Archive Rule**: Items marked ✅➡️ or ❌ are moved to `DECISIONS_ARCHIVE/` during `/session-end`

---

## 1. Data Layer Architecture

> **Archived**: 2.1 (PG Hot layer), 2.2 (Snowflake Cold layer), 2.3 (Hybrid queries) → `DECISIONS_ARCHIVE/2026-02_archived_decisions.md`

## 2. Tooling & Agents

> **Archived**: 3.2 (Skills), 3.3 (Workflows), 3.4 (Session model) → `DECISIONS_ARCHIVE/2026-02_archived_decisions.md`

---

## 3. Client-Voice Improvements

| ID | Topic | Status | Decision | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 4.1 | Optimize existing Streamlit code | ⏳ Pending | User to provide list of improvements | Agent can refactor once priorities are defined |

---

## 4. Ontology Architecture (2026-02-02 Debate)

| ID | Topic | Status | Decision | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 5.9 | Entity tier strategy | 🔄 In Debate | Tier 1: consumo, Tier 2: contexto, Tier 3: auxiliar | Dependente da definição de rubricas de qualidade |
| 5.9 | Entity tier strategy | 🔄 In Debate | Tier 1: consumo, Tier 2: contexto, Tier 3: auxiliar | Dependente da definição de rubricas de qualidade |
| 6.2 | Pre-Analysis Linkage Strategy | ⏳ Pending Debate | **Adopted V8 (Hybrid)**: Link via ID (New) + CPF (Legacy). | **Finding**: Legacy flow holds 77% of debt value (R$ 28M). <br> **Action**: We MUST revisit this rule to formalize the CPF-based linkage in the Data Engineering layer (it currently relies on ad-hoc matching). |

> **Archived**: 5.7 (Naming convention), 5.8 (Migration timing) → `DECISIONS_ARCHIVE/2026-02-02_zendesk_investigation.md`

## 5. Zendesk Bifurcation & Federation (2026-02-03)

> **Archived**: 7.1, 7.2, 7.3 → `DECISIONS_ARCHIVE/2026-02-03_zendesk_deep_dive.md`
> **Archived**: Priority 1, H4 → `DECISIONS_ARCHIVE/2026-02-03_zendesk_b2c.md`

---

## 4b. Hipóteses e Investigações Abertas (2026-02-02)

> **Premissa base**: Documentar a versão enriquecida (CAPIM_ANALYTICS) é preferível, MAS só se ela for confiável.

| ID | Hipótese / Investigação | Status | Achado | Conclusão |
| :--- | :--- | :--- | :--- | :--- |
| H4 | Lógica de `droz_template` está duplicada e pode divergir | ⚠️ Risco | Já divergiu! `horario_atendimento_ccc` | Alertar Data Eng |
| H6 | Inferência de clinic via NLP no conteúdo | 💡 Oportunidade | Não investigado ainda | Futuro |

> **Archived**: H2 (Rejeitado) → `DECISIONS_ARCHIVE/2026-02-02_zendesk_investigation.md`

### Detalhamento H4: Risco de Divergência droz_template

**Problema**: O mapeamento tags → droz_template está duplicado em:
- `zendesk_tickets_raw.sql` (linhas 41-105)
- `zendesk_tickets.sql` (linhas 38-94)

**Divergência já existente**:
```sql
-- APENAS em ZENDESK_TICKETS (não existe em _RAW):
when t.tags like ('%horario_atendimento_ccc%') then 'horario_atendimento_ccc'
```

**Impacto**: Análises usando `_RAW` vs `_TICKETS` mostrarão totais diferentes.
**Ação recomendada**: Extrair CASE WHEN para uma macro dbt ou CTE compartilhada.



> **See Archive**: `DECISIONS_ARCHIVE/2026-02_archived_decisions.md` for full breakdown.

---

---

## 6. Workspace Structure Standardization (2026-02-03)

> **Archived**: 8.1, 8.2, 8.3, 8.4 → `DECISIONS_ARCHIVE/2026-02-03_workspace_cleanup.md`

| ID | Topic | Status | Decision | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 8.5 | client-voice Rename | ⏳ Pending | Rename to client-voice-app/ | Manual git operation required. Cursorrules created, functional. Low priority. |

---

## 7. Project Rename (2026-02-03)

> **Archived**: 9.1 â†’ DECISIONS_ARCHIVE/2026-02-03_workspace_standards.md

---

## 8. Entity Documentation Standards (2026-02-03)

> **Archived**: 10.1, 10.2, 10.3 â†’ DECISIONS_ARCHIVE/2026-02-03_workspace_standards.md

---

## 9. Project Hygiene & Cleanup (2026-02-03)

> **Archived**: 11.1 → `DECISIONS_ARCHIVE/2026-02-03_workspace_cleanup.md`

---

## 10. Visualization Standards Distribution (2026-02-04)

> **Archived**: 12.1, 12.2 → `DECISIONS_ARCHIVE/2026-02-04_project_autonomy.md`

---

## 11. Skills Architecture (2026-02-04)

> **Archived**: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6 → `DECISIONS_ARCHIVE/2026-02-04_skills_architecture.md`

**Summary**: Implementada 3-Tier Skill Architecture com 5 novas skills (3 Tier 2, 2 Tier 3) e 9 domain extensions.

**Related**: 
- `SKILL_REGISTRY.yaml` — Catálogo de skills (12 active, 3 planned)
- `SKILLS_PLAYBOOK.md` — Guia de criação
- `ARCHITECTURE_PRINCIPLES.md` — 3-Tier Architecture

---

## 12. BNPL-Funil Refactoring (2026-02-04 Debate)

> **Archived (Phase A)**: 14.2, 14.4, 14.5, A1, A2, A3, A4, A5 → `DECISIONS_ARCHIVE/2026-02-04_bnpl_funil_phase_a.md`

| ID | Topic | Status | Decision | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 14.1 | Documentation Classification Strategy | ✅ Decided | **Opção A: Reclassificar + Criar Agênticos** | 3-tier strategy established. Ready for execution on remaining entities. |
| 14.3 | Entity Debate Order (Tier-1) | ✅ Decided | Fase A (SOURCE) ✅ → Fase B (SANDBOX) ✅ | **Phase A COMPLETE**. **Phase B COMPLETE**: B1 ✅ C1_ENRICHED_BORROWER (gender investigation), B2 ✅ C2_ENRICHED_REQUESTS (payment gap → `payment_status_expected`), **B3 ✅ C1_LIFECYCLE (2026-02-05)**. |
> **Archived**: 14.6 (Dual Doc Organization Pattern) → `DECISIONS_ARCHIVE/2026-02-05_documentation_standards.md`

**Phase A Summary** (archived):
- 5 SOURCE entities documented: CREDIT_SIMULATIONS, PRE_ANALYSES, REQUESTS, CREDIT_CHECKS, SCR_CHECKS
- Created 5 AGENTIC docs + updated 5 SEMANTIC docs
- Key findings: ID collision, transitional states, deprecated sources, polymorphic structures

**Related**:
- Archive: `DECISIONS_ARCHIVE/2026-02-04_bnpl_funil_phase_a.md`
- Dual Documentation Protocol: `.cursor/skills/investigate-entity/SKILL.md`

---

## 15. Skills Improvements (2026-02-05)

> **Archived**: 15.1 → `DECISIONS_ARCHIVE/2026-02-05_bnpl_funil_phase_b.md`

---

## 16. C1_LIFECYCLE Debate & Decisions (2026-02-05)

> **Archived**: 16.1, 16.2 → `DECISIONS_ARCHIVE/2026-02-05_bnpl_funil_phase_b.md`

**Summary**: Phase B complete. Renamed `patient_entity_id` → `borrower_entity_id`, added AX-FINTECH-006 and RULE-FINTECH-002.

---

## 17. Clinic Business Rules (2026-02-05 Debate)

| ID | Topic | Status | Decision | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 17.1 | BNPL requires SaaS (by segment) | ✅ Decided | **Independente: YES**, Independente-Legado: NO, Rede Homologada: NO | Critical rule: explains `never_subscribed` clinics with BNPL activity |
| 17.2 | SaaS lifecycle reactivation tracking | ✅ Decided | **23% of current_subscribers are reactivations** | Use `most_recent_subscription_number > 1` to identify. Gap: bucket doesn't distinguish. |
| 17.3 | BNPL eligibility criteria | ✅ Decided | Credit Score + Verified Documentation | Score alone is not sufficient |
| 17.4 | BNPL activity window | ✅ Decided | 30 days (C1 or C2) | For "active clinic" classification |
| 17.5 | Interest category source | ✅ Decided | Declared at signup (aggregated) | Intention ≠ actual behavior |
| 17.6 | Cross-sell SaaS ↔ BNPL direction | ✅ Decided | Bidirectional (depends on segment) | Both SaaS→BNPL and BNPL→SaaS occur |
| 17.7 | Taxonomy: Independente vs Grupo | ✅ Decided | **NOT mutually exclusive**. 10,661 "Independente" clinics have group_id. | Use `business_segmentation` for reliable separation, not `is_independent_clinic`. |

**Proposed Axioms**:

```yaml
# AX-FINTECH-007: BNPL-SaaS Dependency by Segment
- name: AX-FINTECH-007
  type: SOFT
  scope: CLINIC
  rule: "IF business_segmentation = 'Independente' AND is_subscriber = FALSE THEN is_bnpl_eligible SHOULD BE FALSE"
  note: "Independente clinics require active SaaS for BNPL. Legado and Rede are exempt."

# AX-FINTECH-008: Active BNPL Window
- name: AX-FINTECH-008
  type: SOFT
  scope: CLINIC
  rule: "clinic_is_bnpl_active := last_bnpl_activity_at >= CURRENT_DATE - 30"
  note: "30-day recency window for active classification"
```

**Investigation Results (2026-02-05)**:
- ✅ 17.2 Investigated: 23% of current subscribers are reactivations (sub_number > 1)
- ✅ 17.7 Investigated: 10,661 "Independente" clinics have group_id — NOT mutually exclusive
- ✅ 17.1 Validated: Independente never_subscribed = 4% BNPL eligible; Legado/Rede = 62-71%

**New Axioms to Add**:

```yaml
# AX-FINTECH-009: Reactivation Definition
- name: AX-FINTECH-009
  type: SOFT
  scope: CLINIC
  rule: "clinic_is_reactivated := most_recent_subscription_number > 1"
  note: "23% of current_subscribers are reactivations"

# AX-FINTECH-010: Taxonomy Caveat
- name: AX-FINTECH-010
  type: SOFT
  scope: CLINIC
  rule: "is_independent_clinic does NOT exclude group membership"
  note: "Use business_segmentation = 'Rede Homologada' to identify networks"
```

**Next Steps**:
- [ ] Add axioms to `AXIOMS.yaml`
- [ ] Update CLINIC_DIM_V1_SEMANTIC.md with new findings

---

## 18. ECOSYSTEM.CLINICS Governance (2026-02-09)

| ID | Topic | Status | Decision | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 18.1 | Governança de `ECOSYSTEM.CLINICS` | ✅➡️ Executed | **Opção B (estrita)**: contrato canônico mínimo é **SAAS-owned**; FINTECH documenta apenas projeções locais (`FINTECH.CLINICS.*`) | Reduz acoplamento semântico e mantém autonomia. `ECOSYSTEM.CLINICS` deve conter apenas invariantes + join key (`clinic_id`) + caveats cross-domain. |

## 5. Workflow / Next Steps

| Priority | Action | Owner | Status |
| :--- | :--- | :--- | :--- |

| 2 | Investigate "SaaS App Patients" identification | Agent | ⏳ Pending | How to ID patients who are NOT debtors but use the app? (Match against `PATIENTS`?). |
| 5 | **Populate vox_popular with initial data (ETL)** | Agent | ⚠️ Blocked (DB Connection) | Script fixed + Dry-run success. FINTECH index repaired. Waiting for DB access. |
| 7 | Optimize Streamlit code (client-voice) | Agent | ⏳ Pending | Agent can refactor once priorities are defined |
| 9 | **Meta-Architecture Review & Recalibration** | User/Agent | 🔄 Ongoing | Track project evolution, documentation drift, and refactoring needs as new findings emerge from investigations. |
| P6.3 | **Prompt Engineering Specialist Agents** | User/Agent | ⏳ Pending | Define guardrails for Finance, Support, and POS agents in n8n. |
| P6.4 | **Assignee Traceability Logic** | Agent | ⏳ Pending | Fully map and automate attendee ID tracking (Claudinha vs Humans). |

> **Archived**: Priority 1 (Create entity structure) → `DECISIONS_ARCHIVE/2026-02-02_zendesk_investigation.md`

---

## 📝 Recent Session Notes

### 2026-02-02 (In Progress)
**Focus**: Federated Ontology Sync, Shared Entity Promotion, Axiom Extraction.
- ✅ Created `ONTOLOGY_INDEX.yaml` for SAAS, FINTECH, CLIENT_VOICE.
- ✅ Implemented `sync_ontology_to_pg.py` with multi-domain merging.
- ✅ Implemented automated Axiom extraction from Markdown callouts.
- ✅ Defined "Map vs X-Ray" terminology for agent reasoning optimization.
- ✅ Promoted `PATIENTS`, `CLINICS` to `ECOSYSTEM.` scope.

> **Full History**: [SESSION_NOTES/2026-02-02.md](./SESSION_NOTES/2026-02-02.md)

---

### 2026-02-01 (Completed)
**Focus**: Project restructuring, folder naming, credential setup

**Archived 7 items** → `DECISIONS_ARCHIVE/2026-02_architecture.md`

**Key Accomplishments**:
- Renamed `project_refactor/` → `_domain/` in SAAS + FINTECH
- Renamed 48 files (`*_REFACTOR.md` → `*_SEMANTIC.md`)
- Tested PostgreSQL connection (`vox_popular`)

---

## 18. Crivo Ecosystem Architecture (2026-02-05)

> **Archived**: 18.1, 18.2 → `DECISIONS_ARCHIVE/2026-02-05_crivo_ecosystem.md`

### 18.3. Coverage Drop from Sep/2025 ⏳
**Finding**: Bridge coverage dropped from ~95% (May 2025) to ~38% (Oct 2025+).
- 30% of CS have NO Crivo record (rejected before engine ran: negativation, age, clinic_rating)
- Sep 2025+ volume drop visible in BOTH SOURCE_CRIVO_CHECKS and ANALYTICS
- Root cause likely a **pipeline or product change** — needs confirmation from Data Eng

### 18.4. PRE_ANALYSES: Coverage is NOT zero in ANALYTICS ❌ Rejected
**Revision (new evidence)**:
- The canonical legacy source `CAPIM_DATA.RESTRICTED.SOURCE_PRE_ANALYSIS_API` does **not** expose `crivo_id`
  (only `CRIVO_PROFILE_VERIFICATION`), so canonical legacy linkage still relies on the legacy CSV system.
- However, the analytics entity `CAPIM_DATA.CAPIM_ANALYTICS.PRE_ANALYSES` **does** contain `CRIVO_ID`
  for `PRE_ANALYSIS_TYPE='pre_analysis'` (legacy type) with ~46.6% fill rate, enabling a direct join to
  `CAPIM_ANALYTICS.CREDIT_CRIVO_CREDIT_CHECKS` by `crivo_id`.

**What remains true**:
- The `hash_cpf` bridge in `bnpl-funil/queries/enrich/bridges/map_credit_simulations_to_credit_crivo_analytics.sql`
  is still **CREDIT_SIMULATIONS-specific** (it solves “no FK in analytics” for CS).

---

## 🔗 References

- [MEMORY_ARCHITECTURE_CONSTITUTION.md](../MEMORY_ARCHITECTURE_CONSTITUTION.md) — Governance
- [START_HERE_ECOSYSTEM.md](../START_HERE_ECOSYSTEM.md) — Entry point
- [federation/DOMAIN_REGISTRY.yaml](../federation/DOMAIN_REGISTRY.yaml) — Domain paths
- [federation/CAPABILITY_MATRIX.yaml](../federation/CAPABILITY_MATRIX.yaml) — What each domain can answer
- [LESSONS_LEARNED.md](LESSONS_LEARNED.md) — Consolidated patterns
- [SESSION_NOTES/](SESSION_NOTES/) — Per-session notes
- [DECISIONS_ARCHIVE/](DECISIONS_ARCHIVE/) — Completed decisions
