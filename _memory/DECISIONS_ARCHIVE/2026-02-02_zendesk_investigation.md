# 📁 Decision Archive: Zendesk Investigation & Ontology (2026-02-02)

> **Archived**: 2026-02-02
> **Session**: Zendesk table investigation, clinic_id analysis, entity documentation structure

---

## 1. Ontology Structure Decisions

### 5.7 Naming Convention for Entity Docs
- **Status**: ✅ Decided + Executed
- **Decision**: `<ENTITY>.md` + `<ENTITY>_SEMANTIC.md`
- **Rationale**: Separates technical reference from business context; consistent pattern
- **Executed On**: 2026-02-02
- **Related Files**:
  - `ontology/entities/_TEMPLATE.md`
  - `ontology/entities/_TEMPLATE_SEMANTIC.md`

### 5.8 Migration Timing
- **Status**: ✅ Decided + Executed
- **Decision**: Do migration NOW (create structure + docs before continuing other work)
- **Rationale**: Foundation needed before documenting entities
- **Executed On**: 2026-02-02
- **Related Files**:
  - Created `ontology/entities/SAAS/`
  - Created `ontology/entities/FINTECH/`
  - Created `ontology/entities/CLIENT_VOICE/`
  - Created `ontology/entities/README.md`

### Priority 1: Create Entity Structure
- **Status**: ✅➡️ Executed
- **Decision**: Create centralized entity documentation folders
- **Executed On**: 2026-02-02
- **Related Files**: All folders in `ontology/entities/`

---

## 2. Hypothesis Rejections

### H2: Aumentar fill rate via fontes atuais (source_dash_users)
- **Status**: ❌ Rejected
- **Hypothesis**: source_dash_users could improve clinic_id fill rate
- **Finding**: user_email field is HASHED (SHA-256) — JOIN never matches
- **Rejected On**: 2026-02-02
- **Evidence**:
  - 0% match rate between Zendesk emails and dash_users
  - user_email avg length = 64 chars (exactly SHA-256 hash)
  - Likely LGPD/privacy decision
- **Resolution**: Use `RESTRICTED.USERS_SENSITIVE_INFORMATION` instead (H2b)

---

## 3. Key Discoveries from Investigation

### Zendesk Table Hierarchy
| Table | Rows | clinic_id | Purpose |
|:---|:---:|:---:|:---|
| SOURCE_ZENDESK_TICKETS | 430K | ❌ | Raw Hevo sync |
| SOURCE_ZENDESK_COMMENTS | 3.9M | ❌ | Comments (~9/ticket) |
| ZENDESK_TICKETS_RAW | 430K | ✅ (46%) | Enriched, agent metrics |
| ZENDESK_TICKETS | 431K | ❌ | CX metrics |

### clinic_id Inference Analysis
- **37.8%** from org_external_id (Zendesk organization)
- **8.6%** from lu_clinic_id (via source_requests)
- **0%** from dash_clinic_id (broken JOIN — emails hashed)

### Fill Rate Trend (Improving)
- Mar/2025: 30% → Jan/2026: 44% (+14pp)

### droz_template Divergence (Risk Found)
- Same CASE WHEN logic duplicated in two dbt models
- Already diverged: `horario_atendimento_ccc` only in ZENDESK_TICKETS
- Recommendation: Extract to macro or shared CTE

---

## 4. Patterns Learned

1. **Check for hashed fields**: Before assuming JOIN will work, verify data formats
2. **RESTRICTED tables**: May have unhashed PII when staging tables are anonymized
3. **COALESCE hierarchy matters**: First non-null wins, even if less accurate
4. **droz_template centralization**: Duplicated business logic creates divergence risk
5. **Immediate decision tracking**: Update DECISIONS_IN_PROGRESS after each confirmation, not at end of debate

---

## Session Accomplishments (2026-02-02)

### Structures Created
- `ontology/entities/{SAAS,FINTECH,CLIENT_VOICE}/` folders
- `_TEMPLATE.md` and `_TEMPLATE_SEMANTIC.md`
- `README.md` documenting entity structure

### Knowledge Harvested
- Complete understanding of 4 Zendesk tables
- clinic_id inference mechanism and limitations
- Solution for improving fill rate (+4pp via RESTRICTED)
- Identified code debt in dbt (droz_template duplication)

### Updated Memory Files
- `DECISIONS_IN_PROGRESS.md` — Added hypotheses section, debate checkpoint
- `LESSONS_LEARNED.md` — Added Zendesk hierarchy, clinic_id findings, droz_template risk
