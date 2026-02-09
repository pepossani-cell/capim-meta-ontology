# 📁 Decision Archive: Crivo Ecosystem Architecture (2026-02-05)

## Archived: 2026-02-05

---

### 18.1 Three Crivo Entities Confirmed

**Status**: ✅➡️ Executed

**Discovery**: Crivo data lives in 3 distinct tables with different schemas, purposes, and coverage:
1. `CREDIT_CRIVO_CREDIT_CHECKS` (2.1M rows, CAPIM_ANALYTICS) — Main curated source for risk analysis
2. `SOURCE_CRIVO_CHECKS` (208K rows, SOURCE_STAGING) — Raw staging with FK to simulations
3. `CRIVO_PF_PJ_PRODUCTION_FULL_CSVS` (2.3M rows, RESTRICTED) — Legacy pre-analysis only

**Decision**: Document all three entities with distinct purposes instead of treating as duplicates.

**Rationale**:
- Each serves different use case (analytics vs staging vs legacy)
- Different schemas and coverage patterns
- Cannot be used interchangeably

**Executed On**: 2026-02-05

**Related Files**:
- `bnpl-funil/_domain/_docs/reference/CREDIT_CRIVO_CREDIT_CHECKS_SEMANTIC.md`
- `bnpl-funil/_domain/_docs/reference/SOURCE_CRIVO_CHECKS_SEMANTIC.md`
- `bnpl-funil/_domain/_docs/ENTITY_INDEX.yaml` (updated with all 3 entities)

**Impact**: 
- Clarified Crivo ecosystem architecture
- Prevented incorrect joins/assumptions
- Enabled proper bridge queries per use case

---

### 18.2 hash_cpf = SHA256(digits_only_cpf)

**Status**: ✅➡️ Executed

**Discovery**: Confirmed hash_cpf formula via empirical validation:
- Sample test: 5/5 CPFs matched
- Bulk test: 97.3% match rate (Patient CPF) + 2.7% (Financial Responsible CPF)

**Decision**: Adopt `SHA256(REGEXP_REPLACE(cpf, '[^0-9]', ''))` as canonical bridge formula.

**Rationale**:
- High match rate validates formula
- Remaining 2.7% explained by Financial Responsible CPF (expected)
- Enables deterministic linkage without FK dependency

**Executed On**: 2026-02-05

**Related Files**:
- `bnpl-funil/queries/enrich/bridges/map_credit_simulations_to_credit_crivo_analytics.sql`
- `bnpl-funil/_domain/_docs/reference/CREDIT_CRIVO_CREDIT_CHECKS_SEMANTIC.md`

**Impact**:
- Unlocked CREDIT_SIMULATIONS → CRIVO linkage
- 97.3% coverage for credit risk analysis
- Documented formula for future bridge queries

---

## Summary

**Items Archived**: 2  
**Domain**: FINTECH (bnpl-funil)  
**Theme**: Crivo ecosystem clarification and bridge validation

**Key Outcomes**:
- 3 distinct Crivo entities documented
- hash_cpf bridge formula validated and operationalized
- Enabled credit risk analysis with deterministic linkage
