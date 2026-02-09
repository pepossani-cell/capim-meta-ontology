
### Archived on 2026-02-02
| ID | Topic/Hypothesis | Status | Decision/Finding | Notes |
| :--- | :--- | :--- | :--- | :--- |
| H1 | `clinic_id` em ZENDESK_TICKETS_RAW é confiável | ✅ Validado | 46% preenchido, tendência de melhora | Confiável para análise, mas limitado |
| H2b | Usar RESTRICTED.USERS_SENSITIVE_INFORMATION | ✅ Validado | +17K tickets (+4pp) | 46% → 50% fill rate |
| SOURCE_ZENDESK_TICKETS | 430,815 | 17 | ❌ | Raw Hevo sync |
| SOURCE_ZENDESK_COMMENTS | 3,885,507 | 13 | ❌ | Comments (BODY_COMMENT, ~9 per ticket) |
| ZENDESK_TICKETS | 431,237 | 44 | ❌ | Métricas CX |

### Archived on 2026-02-02
| ID | Topic/Hypothesis | Status | Decision/Finding | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2.1 | PostgreSQL as "Hot" layer | ✅ Decided | Client-Voice BD (PostgreSQL) is source of truth for VoC data | Low latency, operational |
| 2.2 | Snowflake as "Cold" layer | ✅ Decided | Snowflake receives mirror from PG (managed by Data Eng team) | Cross-domain analytics |
| 2.3 | Hybrid queries in Streamlit | ✅ Decided | Streamlit can query both PG and Snowflake concurrently | Use PG for operational, Snowflake for analytics |
| 3.2 | Add Antigravity Skills for analysis | ✅ Decided | Created validate-axioms and clinic-health-check skills | In `.agent/skills/` |
| 3.3 | Create Antigravity Workflows | ✅ Decided | Created session-start, session-end, debate | In `.agent/workflows/` |
| 3.4 | Session model | ✅ Decided | Decision-centric: save immediately, not at session end | Reduces risk of lost context |
| 4.3 | Add CAPABILITY_MATRIX capabilities | ✅ Decided | 5 capabilities defined for CLIENT_VOICE | Done on 2026-01-31 |
| 5.1 | Skill `investigate-entity` | ✅ Decided | Add generic skill to `capim-meta-ontology/.agent/skills/` | Based on `ontologia-cf/docs/how_to/INVESTIGATE_ENTITY.md` |
| 5.2 | Entity docs location | ✅ Decided | Centralize in `capim-meta-ontology/ontology/entities/<DOMAIN>/` | Enables cross-domain access for agentic features |
| 5.3 | Storage for runtime access | ✅ Decided | PostgreSQL `vox_popular.ontology_entities` | Master: git; Cache: PG; Sync: pending |
| 5.5 | Workflow artifacts trust | ✅ Decided | Preserve queries; DO NOT trust classified data | Classifications may be contaminated by bad prompts |
| 5.6 | Investigation-first approach | ✅ Decided | Document raw entities BEFORE restructuring workflow | Avoid "adivinhar semântica" |
| H3 | ZENDESK_TICKETS e ZENDESK_TICKETS_RAW têm propósitos diferentes | ✅ Confirmado | RAW: agent metrics; TICKETS: CX metrics | Documentar ambas |
| H5 | dash_clinic_id contribui para o COALESCE | 🟢 Solução | Via RESTRICTED ao invés de dash_users | Propor mudança no dbt |

### Archived on 2026-02-02
| ID | Topic/Hypothesis | Status | Decision/Finding | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 0 | ✅ **Resolver debate workaround clinic_id** | User + Agent | DONE |
| 1 | ✅ **Investigate & document Zendesk source tables** | Agent | DONE |
| 2 | ✅ **Create skill `investigate-entity`** | Agent | DONE |

### Archived on 2026-02-02
| ID | Topic/Hypothesis | Status | Decision/Finding | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 5.4 | Sync mechanism | ✅➡️ Executed | Script syncs meta-ontology → PostgreSQL (`vox_popular`) | Usar `ontology_documents` como tabela central |
| 5.10| Ontology Store Location | ✅➡️ Executed | Store docs in `vox_popular` (PostgreSQL) | Melhor performance e acessibilidade para apps cloud |
| 5.11| Entity Mapping Strategy | ✅➡️ Executed | Use `ONTOLOGY_INDEX.yaml` as abstraction layer | Map logical IDs to legacy/physical file paths |
| 5.12| Postgres Schema Design | ✅➡️ Executed | Table `ontology_entities` with JSONB and TEXT[] | Support for multiple domains and temporal tracking |
| 5.13| Shared Entity Promotion | ✅➡️ Executed | Promote common entities to `ECOSYSTEM.` scope | Unified view for PATIENTS, CLINICS across domains |
| 5.14| Axiom Extraction | ✅➡️ Executed | Extract callouts and rules into `axioms_json` | Automated logic capture from markdown docs |
| 3 | **Define `ontology_documents` table in vox_popular** | Agent | ✅➡️ Executed |
| 4 | **Create `sync_ontology_to_pg.py` script** | Agent | ✅➡️ Executed |
