# 📁 Decision Archive: Zendesk Deep Dive (2026-02-03)

## Archived: 2026-02-03

### 7.1 "Ghost Ticket" Strategy (60% Missing ID)
- **Status**: ✅ Decided + Executed
- **Decision**: Adopted Bifurcated Ontology (B2B SaaS vs B2C Fintech).
- **Rationale**: 30% of tickets are B2C Debt Collection and naturally do not have a `clinic_id`. Forcing a clinic ID was "ontology blindness".
- **Execution**:
    - Created `capim-meta-ontology/_domain/_docs/ECOSYSTEM/ZENDESK_TICKETS.md`.
    - Defined "Golden Path" for B2C Identification using `C1_ENRICHED_BORROWER`.

### 7.2 Federated Ontology Indexing
- **Status**: ✅ Decided + Executed
- **Decision**: Renamed `ONTOLOGY_INDEX.yaml` to `ONTOLOGY_INDEX_DOMAIN.yaml` with explicit scope headers.
- **Rationale**: Agents were suffering from "context myopia", thinking local files were the whole truth.
- **Execution**: Renamed files in `ontologia-cf` and `bnpl-funil`. Updated `migrate_indexes.py`.

### 7.3 Investigation Methodology
- **Status**: ✅ Decided + Executed
- **Decision**: Mandated Snowflake-First profiling (100k+ rows) over local sampling.
- **Rationale**: Small samples (50-200) failed to reveal the macro-pattern of B2C tickets masked as ghosts.
- **Execution**: Added to `LESSONS_LEARNED.md` and enforced in `session-start` workflow.
