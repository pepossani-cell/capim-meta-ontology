# 📁 Decision Archive: Zendesk Routing & Taxonomy (2026-02)

## Archived: 2026-02-03

### [6] Investigate Zendesk Value Extraction (n8n migration)
- **Status**: ✅ Decided + Executed
- **Decision**: Adopted **Hybrid Routing Strategy**. 80% of volume (B2C Finance, B2B Support) is routed via deterministic metadata (Tags, Group ID). Only the remaining ~20% "Undefined" cluster goes to the LLM Broker.
- **Rationale**: Reduces token costs by 80% while maintaining high accuracy for known business flows.
- **Executed On**: 2026-02-03
- **Related Files**: `client-voice/scripts/sync_zendesk_enhanced_view.py`, `client-voice/_docs/ontology/ZENDESK_TICKETS_ENHANCED.md`

### [6.0] Zendesk Taxonomy Approach
- **Status**: ❌ Rejected
- **Decision**: Replaced the legacy "3 Groups" taxonomy (Loss, Pay, Machine) with a semantic ontology-driven model.
- **Rationale**: Legacy groups were ambiguous and didn't cover the full B2B (SaaS) vs B2C (Fintech) split.
- **Executed On**: 2026-02-03

### [6.1] Agent Definition Strategy
- **Status**: ✅ Decided + Executed
- **Decision**: "The Golden Path" — Combining Identity (Assignee ID), Intent (Tags), and Affiliation (Clinic ID) to route tickets.
- **Rationale**: Empirical investigation showed that no single attribute is perfectly reliable. A multi-attribute hierarchy minimizes "Context Blindness".
- **Executed On**: 2026-02-03

### [8] Update skill workflow to use ECOSYSTEM.PATIENTS
- **Status**: ✅ Decided
- **Decision**: Unify patient investigation through the federated `ECOSYSTEM.PATIENTS` view instead of project-specific local matches.
- **Rationale**: Improves consistency across SAAS and FINTECH domains.
- **Executed On**: 2026-02-03
