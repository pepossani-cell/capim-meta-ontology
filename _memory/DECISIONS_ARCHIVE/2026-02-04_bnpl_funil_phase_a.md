# 📁 Decision Archive: BNPL-Funil Refactoring — Phase A (2026-02-04)

## Archived: 2026-02-04

> **Context**: Debate session for reorganizing bnpl-funil project documentation. Phase A focused on SOURCE entities (Tier 1-2).
> 
> **Session Focus**: Entity documentation using Dual Documentation Protocol (AGENTIC + SEMANTIC)

---

## 14.2 ENTITY_INDEX.yaml Path Correction

**Status**: ✅➡️ Executed

**Decision**: Fix `project_refactor/` → `_domain/` paths in ENTITY_INDEX.yaml

**Rationale**: Paths were outdated after folder restructuring. Also added new fields: `tier`, `documentation.agentic/semantic`, `investigations`.

**Executed On**: 2026-02-04

**Related Files**: 
- `bnpl-funil/_domain/_docs/ENTITY_INDEX.yaml`

---

## 14.4 Data Layer Awareness Standard

**Status**: ✅➡️ Executed

**Decision**: Cross-project standard for distinguishing SOURCE vs SANDBOX layers + FINTECH-specific mapping

**Rationale**: Agent needs machine-readable way to distinguish official sources from project-owned sandbox views without explicit prompting.

**Executed On**: 2026-02-04

**Related Files**: 
- `capim-meta-ontology/.cursorrules` (global standard)
- `bnpl-funil/.cursorrules` (FINTECH mapping)
- `bnpl-funil/_domain/_docs/ENTITY_INDEX.yaml` (fields: layer, ownership, trust_level, known_issues, corrects)

---

## 14.5 Data Layers Quick Fix (Other Projects)

**Status**: ✅➡️ Executed

**Decision**: Add `data_layers` section to ontologia-saas and client-voice-data `.cursorrules`

**Rationale**: Quick fix to propagate the standard. ENTITY_INDEX.yaml updates deferred to project-specific refactoring.

**Executed On**: 2026-02-04

**Related Files**: 
- `ontologia-saas/.cursorrules`
- `client-voice-data/.cursorrules`

---

## A1 CREDIT_SIMULATIONS Documentation

**Status**: ✅➡️ Executed

**Decision**: Create AGENTIC doc + update SEMANTIC for CREDIT_SIMULATIONS

**Key Findings**:
1. 274k rows, 1:1 grain (2024-05 → 2026-02)
2. State machine: `approved` (44%), `rejected` (50%), `expired` (6%)
3. `appealable=TRUE` only for `rejected` state
4. Terminology corrected: `state` (not `status`), `rejection_reason` (not `reason`)

**Executed On**: 2026-02-04

**Related Files**: 
- `bnpl-funil/_domain/_docs/reference/CREDIT_SIMULATIONS.md` (AGENTIC - created)
- `bnpl-funil/_domain/_docs/reference/CREDIT_SIMULATIONS_SEMANTIC.md` (updated)

---

## A2 PRE_ANALYSES Documentation

**Status**: ✅➡️ Executed

**Decision**: Create AGENTIC doc + update SEMANTIC for PRE_ANALYSES

**Key Findings**:
1. 3.5M rows, polymorphic entity (type='pre_analysis' + type='credit_simulation')
2. `rejected` state is **TRANSITIONAL** — becomes `expired` in 7-30 days
3. `rejection_reason` is preserved even after state transition
4. **8.48% ID collision** in Analytics layer — use compound key `(type, id)`
5. Analytics layer missing CPF and other critical columns
6. `eligible` ≠ `approved` — needs financing signal

**Executed On**: 2026-02-04

**Related Files**: 
- `bnpl-funil/_domain/_docs/reference/PRE_ANALYSES.md` (AGENTIC - created)
- `bnpl-funil/_domain/_docs/reference/PRE_ANALYSES_SEMANTIC.md` (updated)

---

## A3 REQUESTS Documentation

**Status**: ✅➡️ Executed

**Decision**: Create AGENTIC doc + update SEMANTIC for REQUESTS

**Key Findings**:
1. 212k rows, 1:1 grain (2021-03 → 2026-02)
2. State distribution: `rejected` (44%), `finished` (35%), `expired` (11%), `canceled` (10%)
3. **10.5% orphan requests** (no C1 link) — concentrated in 2021-2022 self-serve flow
4. `finished` + `rejection_reason` is **EXPECTED behavior** (backoffice override)
5. Analytics layer has `c1_origin` collision — use SOURCE
6. `REQUEST_CREATED_BY` = `user`/`capim` correlates with 100% orphans
7. Derived logic documented as "Recommended" section in AGENTIC doc

**Executed On**: 2026-02-04

**Related Files**: 
- `bnpl-funil/_domain/_docs/reference/REQUESTS.md` (AGENTIC - created)
- `bnpl-funil/_domain/_docs/reference/REQUESTS_SEMANTIC.md` (updated)

---

## A4 CREDIT_CHECKS Documentation

**Status**: ✅➡️ Executed

**Decision**: Create AGENTIC doc + update SEMANTIC for CREDIT_CHECKS

**Key Findings**:
1. 6.3M rows, 1:1 grain (2021-07 → 2026-02)
2. **Highly polymorphic** by SOURCE + KIND + NEW_DATA_FORMAT
3. SERASA format drift: `ARRAY` → `OBJECT` (2024-12+)
4. `source='scr'` in this table is **DEPRECATED** — active SCR is in SRC_API
5. `KIND=NULL` in 27% of records (legacy pre-2024-04)
6. `NEW_DATA_FORMAT` flag unreliable — always check `TYPEOF(DATA)` also
7. No FK to C1 — bridge via CPF + time window

**Executed On**: 2026-02-04

**Related Files**: 
- `bnpl-funil/_domain/_docs/reference/CREDIT_CHECKS.md` (AGENTIC - created)
- `bnpl-funil/_domain/_docs/reference/CREDIT_CHECKS_SEMANTIC.md` (updated)

---

## A5 SCR_CHECKS Documentation

**Status**: ✅➡️ Executed

**Decision**: Create AGENTIC doc (compact, referencing investigation) + update SEMANTIC for SCR_CHECKS

**Key Findings**:
1. 486k rows, 1:1 grain (2021-07 → 2026-02)
2. JSON contract drift: PascalCase (v1, pre-2023) → camelCase (v2, post-2023)
3. `riscoTotal` has **100% fill rate** (excellent data quality)
4. **5x volume growth** in 2025-Q2+ (5k → 35k+/month)
5. No `SOURCE`/`KIND` columns — semantics from JSON contract only
6. Coverage drop in 2026-01 noted but **NOT documented as known_issue** (pending reinvestigation)

**Executed On**: 2026-02-04

**Related Files**: 
- `bnpl-funil/_domain/_docs/reference/SCR_CHECKS.md` (AGENTIC - created, compact)
- `bnpl-funil/_domain/_docs/reference/SCR_CHECKS_SEMANTIC.md` (updated)

---

## Summary

| Debate | Entity | Docs Created | Key Insight |
|:---|:---|:---|:---|
| A1 | CREDIT_SIMULATIONS | AGENTIC + SEMANTIC | `appealable` only for rejected |
| A2 | PRE_ANALYSES | AGENTIC + SEMANTIC | `rejected` is transitional; 8.48% ID collision |
| A3 | REQUESTS | AGENTIC + SEMANTIC | 10.5% orphans; `finished`+`rejection_reason` expected |
| A4 | CREDIT_CHECKS | AGENTIC + SEMANTIC | Polymorphic; `source='scr'` deprecated |
| A5 | SCR_CHECKS | AGENTIC + SEMANTIC | Contract drift validated; 100% riscoTotal fill |

**Phase A Complete**: All Tier-1 SOURCE entities documented with Dual Documentation Protocol.

**Next**: Phase B (SANDBOX entities) — C1_ENRICHED_BORROWER, C2_ENRICHED_REQUESTS, C1_LIFECYCLE
