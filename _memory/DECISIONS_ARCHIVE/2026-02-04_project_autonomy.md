# 📁 Decision Archive: Project Autonomy (2026-02-04)

## Archived: 2026-02-04

---

### 12.1 — Visualization Standards Autonomy

**Status**: ✅➡️ Executed

**Decision**: Hybrid (Doc + Script), distributed to each project

**Context**: 
Multi-repo setup with independent teams (bnpl-funil, ontologia-saas, client-voice-data, client-voice). Teams operating independently need autonomy without external dependencies.

**Decision Details**:
Refactored `VISUALIZATION_STANDARDS.md` (decisions only) + created `scripts/plot_utils.py` (reusable code). Copied both to all 4 projects. Updated cursorrules to reference local copies.

**Rationale**: 
- Teams operating independently need full autonomy (no external dependencies)
- Hybrid approach balances DRY (within project) with autonomy (between projects)
- **Rejected alternatives**: 
  - Skills (wrong abstraction for code reuse)
  - Package (over-engineering for 4 projects)

**Executed On**: 2026-02-04

**Files Created/Modified**:
- `docs/VISUALIZATION_STANDARDS.md` (v2.0: refactored, 200 lines) → copied to 4 projects
- `scripts/plot_utils.py` (new, 240 lines) → copied to 4 projects
- Updated `.cursorrules` in all 4 projects to reference local copies

**Impact**:
- ✅ Each project now has local visualization standards
- ✅ Teams can customize without affecting others
- ✅ Zero external dependencies for visualization code

---

### 12.2 — Core Infrastructure Autonomy

**Status**: ✅➡️ Executed

**Decision**: Copy critical utilities + rules to all projects

**Context**: 
Teams in multi-repo setup need zero external dependencies. Snowflake utilities are CRITICAL for data work (11+ scripts in bnpl-funil, 26+ in ontologia-saas).

**Decision Details**:
Copied 3 critical components:
1. **`snowflake_connection.py`** → client-voice-data (bnpl/ontologia already had)
2. **`snowflake_data.mdc`** rule → all 4 projects
3. **`workspace_hygiene.mdc`** rule → 3 data projects (not client-voice app)

Added fork headers and READMEs to document autonomy model.

**Kept SHARED** (cross-project standards):
- `memory_governance.mdc` — Organizational decision tracking protocol
- `ontology_reasoning.mdc` — Cross-domain federation reasoning
- `agent_protocol.mdc` — General agent behavior

**Rationale**:
- **Technical rules** (Snowflake, workspace) can diverge per team
- **Organizational standards** (memory, ontology, agent protocol) benefit from consistency
- Snowflake connection utility is mission-critical and should be self-contained per project

**Executed On**: 2026-02-04

**Files Created/Modified**:
- `src/utils/snowflake_connection.py` → copied to client-voice-data
- `.cursor/rules/snowflake_data.mdc` → copied to all 4 projects (with fork headers)
- `.cursor/rules/workspace_hygiene.mdc` → copied to 3 data projects (with fork headers)
- `.cursor/rules/README.md` → created in all 4 projects

**Fork Documentation**:
Each copied file includes header:
```markdown
---
# LOCAL COPY - Forked from capim-meta-ontology @ 2026-02-04
# Teams can customize locally if needed.
---
```

**Impact**:
- ✅ All 4 projects are now 100% autonomous
- ✅ Zero external dependencies for critical utilities
- ✅ Teams can customize technical rules locally
- ✅ Organizational standards remain consistent
- ⚠️ Trade-off: Updates NOT automatic (intentional for autonomy)

**Metrics**:
- **Files distributed**: 17 total (averaging 7 per project)
- **Projects 100% autonomous**: 4/4
- **External dependencies**: 0
- **Rules localized**: 2-3 per project

---

## Summary

**Session Focus**: Project Autonomy in Multi-Repo Setup

**Key Theme**: Balancing DRY principle with team independence

**Decisions Executed**: 2  
**Files Created**: 17 (distributed across 4 projects)  
**Architecture Shift**: From shared utilities (dependency) → forked utilities (autonomy)

**Outcome**: 
All 4 projects (bnpl-funil, ontologia-saas, client-voice-data, client-voice) can now operate **completely independently** without external dependencies on capim-meta-ontology.

---

**Related Archives**:
- `2026-02-03_workspace_cleanup.md` — Previous autonomy work (visualization)
- `2026-02-03_workspace_standards.md` — Documentation standards

**Next Steps**:
- Teams can customize local copies as needed
- Optional: Teams can re-sync with master if they want updates
- Monitor if any other shared components emerge as autonomy blockers
