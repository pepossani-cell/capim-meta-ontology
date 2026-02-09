# 📁 Decision Archive: Workspace Cleanup & Standardization (2026-02-03)

## Archived: 2026-02-03

> **Context**: Final phase of workspace standardization and hygiene improvements following the migration from Antigravity to Cursor.

---

## 8.1 Workspace Structure Standardization

**Status**: ✅➡️ Executed

**Decision**: Hierarchical cursorrules (global + project-specific)

**Rationale**:
- Eliminate duplication across projects
- Establish single source of truth for shared protocols
- Allow project-specific extensions without full duplication
- Improve maintainability

**Implementation**:
- Created global `.cursorrules` in `capim-meta-ontology/`
- Updated project-specific cursorrules to extend global rules
- Each project adds only domain-specific context
- Header format: `> **EXTENDS**: ../capim-meta-ontology/.cursorrules`

**Executed On**: 2026-02-03

**Related Files**:
- `capim-meta-ontology/.cursorrules` (global)
- `bnpl-funil/.cursorrules` (extends global)
- `ontologia-saas/.cursorrules` (extends global)
- `client-voice-data/.cursorrules` (extends global)
- `client-voice/.cursorrules` (extends global)
- `docs/WORKSPACE_STRUCTURE.md` (documentation)

---

## 8.2 Client-Voice Classification

**Status**: ✅➡️ Executed

**Decision**: Application Layer (not ontological project)

**Rationale**:
- Separates concerns: data ontology vs UI application
- Aligns with MEMORY_ARCHITECTURE_CONSTITUTION
- `client-voice-data/` = ontology (queries, ETL, semantic docs)
- `client-voice/` = Streamlit app (to be renamed to `client-voice-app/`)

**Implementation**:
- Created separate cursorrules for each project
- Updated `federation/DOMAIN_REGISTRY.yaml` with CLIENT_VOICE path
- Clarified that app layer does NOT duplicate queries from data layer

**Executed On**: 2026-02-03

**Related Files**:
- `client-voice-data/_domain/START_HERE.md`
- `client-voice/.cursorrules`
- `federation/DOMAIN_REGISTRY.yaml`

---

## 8.3 Visualization Standards Centralization

**Status**: ✅➡️ Executed

**Decision**: Extract to shared doc

**Rationale**:
- 30+ lines of visualization code duplicated across projects
- Changes require updating 4+ files
- Central doc = single source of truth

**Implementation**:
- Created `capim-meta-ontology/docs/VISUALIZATION_STANDARDS.md`
- All project cursorrules now reference this doc
- Includes: theme, layout, annotations, export standards

**Executed On**: 2026-02-03

**Related Files**:
- `docs/VISUALIZATION_STANDARDS.md` (canonical)
- All project cursorrules (reference only)

---

## 8.4 Rules Language Standardization

**Status**: ✅➡️ Executed

**Decision**: English for `.cursor/rules/`, Portuguese for `.cursorrules`

**Rationale**:
- Rules = technical protocols (machine-first) → English
- Cursorrules = business context (human-first) → Portuguese
- Global cursorrules = bilingual (serves both audiences)
- Consistency across Cursor ecosystem

**Implementation**:
- Created 7 rules in `.cursor/rules/` (all English)
- Kept cursorrules in Portuguese (with bilingual global)
- Documented in `docs/WORKSPACE_STRUCTURE.md`

**Executed On**: 2026-02-03

**Related Files**:
- `.cursor/rules/*.mdc` (all English)
- `.cursorrules` (Portuguese)

---

## 11.1 capim-meta-ontology Cleanup

**Status**: ✅➡️ Executed

**Decision**: Limpeza cirúrgica - deletar temporários, manter `.agent/` e `_archive/` como referência histórica

**Rationale**:
- Alinhado com §RULE:REFLECTIVE_CHECKOUT (RETAIN utility vs PURGE noise)
- Alinhado com §DIRECTIVE:ACTIVE_FORGETTING (preserve core docs)
- Remove noise sem perder contexto histórico valioso

**Implementation**:

**DELETED (5 files)**:
- `queries/audit/output.txt` — Temporary output
- `queries/audit/scratchpad.py` — Temporary script
- `skill_skill_creator.md` — Duplicate (exists in `.codex/`)
- `PROJECT_RENAME_SUMMARY.md` — Temporary summary
- `WORKSPACE_STANDARDIZATION_SUMMARY.md` — Temporary summary

**MOVED (5 files)**:
- `queries/audit/*_profile.md` → `_archive/audit_profiles_legacy/`
- Created README in archive explaining historical context

**PRESERVED**:
- `.agent/` — Historical reference with deprecation notice
- `_archive/legacy_ontology_structure/` — Old entity structure

**Executed On**: 2026-02-03

**Related Files**:
- `_archive/audit_profiles_legacy/README.md` (created)
- `.agent/README.md` (deprecation notice exists)

---

## Summary

**Total Items Archived**: 5  
**Date Range**: 2026-02-03  
**Theme**: Workspace standardization and hygiene

**Impact**:
- ✅ Eliminated duplication across 5 projects
- ✅ Established clear hierarchy (global → project-specific)
- ✅ Centralized shared standards (visualization, Snowflake protocols)
- ✅ Cleaned up temporary files and noise
- ✅ Preserved historical context appropriately

**Next Steps**:
- 8.5 still pending: Rename `client-voice/` → `client-voice-app/` (low priority)
- Continue using standardized structure for new projects
- Document any new patterns in global cursorrules
