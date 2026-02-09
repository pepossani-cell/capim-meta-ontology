# 📁 Decision Archive: BNPL-Funil Phase B (2026-02-05)

## Archived: 2026-02-05

This archive contains decisions executed during Phase B of the BNPL-Funil Refactoring project, focusing on SANDBOX entities documentation and improvements.

---

### 15.1 @investigate-entity Cross-Correlation

**Status**: ✅➡️ Executed

**Decision**: Add Step 6: Cross-Attribute Correlation Analysis to `@investigate-entity` skill

**Rationale**: During C2_ENRICHED_REQUESTS investigation, we discovered that `is_canceled_after_signing = TRUE` was functionally dependent on `payments_as_of_date IS NULL`. This correlation was not obvious and required manual investigation. Automating correlation detection helps agents discover hidden dependencies.

**Executed On**: 2026-02-05

**Changes Made**:
- Updated `.cursor/skills/investigate-entity/SKILL.md` (v2.0 → v2.1)
- Created `references/CORRELATION_QUERIES.md` with query templates
- Added section 7 to AGENTIC doc template: "Cross-Attribute Dependencies"

**Impact**: Future `@investigate-entity` runs will auto-detect coverage gaps and functional dependencies.

---

### 16.1 patient_entity_id Nomenclature

**Status**: ✅➡️ Executed

**Decision**: Rename `patient_entity_id` to `borrower_entity_id` in C1_LIFECYCLE view

**Rationale**: 
- "Patient" in FINTECH context means "credit requester/borrower", not "clinical patient"
- Agents confused `patient_entity_id` with `dash_patient_id` (SaaS patient record)
- "Borrower" is semantically accurate: the individual requesting credit (potential debtor)

**Executed On**: 2026-02-05

**Changes Made**:
- `create_view_c1_lifecycle.sql`:
  - `patient_entity_id` → `borrower_entity_id`
  - `patient_n_c1_in_lifecycle` → `borrower_n_c1_in_lifecycle`
  - `patient_n_clinics_in_lifecycle` → `borrower_n_clinics_in_lifecycle`
  - `patient_c1_sequence_in_lifecycle` → `borrower_c1_sequence_in_lifecycle`
  - CTE `patient_stats` → `borrower_stats`
- `create_view_c1_lifecycle_slim.sql`: Same column renames
- Catalog documentation files updated
- Investigation script updated

**Related Files**:
- `bnpl-funil/queries/views/create_view_c1_lifecycle.sql`
- `bnpl-funil/queries/views/create_view_c1_lifecycle_slim.sql`
- `bnpl-funil/queries/catalog/c1_lifecycle_*.sql`
- `bnpl-funil/_domain/_docs/reference/C1_LIFECYCLE.md`

---

### 16.2 C1 Approval → C2 Conversion Logic

**Status**: ✅➡️ Executed

**Decision**: Implement BOTH Axiom and Inference Rule for C1→C2 conversion logic

**Rationale**:
- Agents need to understand that `c2_count = 0` for approved C1 is EXPECTED behavior (conversion rate ~12-15%)
- Not all approved C1s convert to C2 (patient choice is the main filter)
- C1 approval is NECESSARY but NOT SUFFICIENT for C2 existence

**Executed On**: 2026-02-05

**Changes Made**:
- Added `AX-FINTECH-006` to `ontology/AXIOMS.yaml`:
  ```
  formal: "HAS_C2(c1) => WAS_APPROVED(c1)"
  ```
- Added `RULE-FINTECH-002` to `ontology/INFERENCE_RULES.yaml`:
  - Reasoning chain for C1→C2 conversion logic
  - Common misconceptions section for agent guidance
  - Example scenarios with interpretations
- Updated `C1_LIFECYCLE.md`:
  - Section 7.5: C1 Approval → C2 Conversion Logic
  - Section 7.6: Nomenclatura borrower vs patient

**Related Files**:
- `capim-meta-ontology/ontology/AXIOMS.yaml`
- `capim-meta-ontology/ontology/INFERENCE_RULES.yaml`
- `bnpl-funil/_domain/_docs/reference/C1_LIFECYCLE.md`

---

## Phase B Summary

**Entities Documented (SANDBOX)**:
1. **B1**: C1_ENRICHED_BORROWER — Gender fill rate investigation (15% PA vs 48% CS explained by historical lack of enrichment)
2. **B2**: C2_ENRICHED_REQUESTS — Payment status gap investigation (13.7% gap = canceled contracts, added `payment_status_expected` flag)
3. **B3**: C1_LIFECYCLE — Nomenclature debate, C1→C2 conversion axiom

**Key Findings**:
- Temporal drift in data enrichment (gender fill rate 0% in 2024 for pre_analysis)
- Functional dependency: `is_canceled_after_signing` → `payments_as_of_date IS NULL`
- Semantic confusion: "patient" in FINTECH ≠ "patient" in SaaS

**Improvements**:
- Cross-correlation analysis added to @investigate-entity skill
- Formal axiom for C1→C2 conversion logic
- Standardized borrower nomenclature across views

---

## Related Archives

- `2026-02-04_bnpl_funil_phase_a.md` — Phase A (SOURCE entities)
- `2026-02-04_skills_architecture.md` — Skills system implementation
