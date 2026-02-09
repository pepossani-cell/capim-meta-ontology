# 📁 Decision Archive: Documentation Standards (2026-02-05)

## Archived: 2026-02-05

---

### 14.6 Dual Doc Organization Pattern

**Status**: ✅➡️ Executed

**Decision**: Apply `_domain/_docs/reference/` for SEMANTIC docs and `docs/reference/` for Data Dictionary docs across all ontology projects.

**Rationale**: 
- Mixing semantic (business context) and agentic (data dictionary) docs in the same folder caused confusion
- Semantic docs are for AI reasoning (why, relationships, caveats)
- Data dictionaries are for query execution (schema, columns, types)
- Separation enables focused loading (agents load only what they need)

**Executed On**: 2026-02-05

**Related Files**:

**Rule Updates**:
- `.cursor/rules/entity_documentation.mdc` — Updated with new paths and Quick Reference Card
- `.cursor/skills/investigate-entity/SKILL.md` — Updated with correct output locations

**Migrations Performed**:

| Project | Docs Moved | From | To |
|:--------|:-----------|:-----|:---|
| `bnpl-funil` | 14 data dictionaries | `_domain/_docs/reference/*.md` | `docs/reference/*.md` |
| `client-voice-data` | 5 data dictionaries | `_domain/_docs/reference/*.md` | `docs/reference/*.md` |
| `ontologia-saas` | 2 data dictionaries | `_domain/_docs/reference/*.md` | `docs/reference/*.md` |

**New Folders Created**:
- `client-voice-data/_domain/_docs/decisions/` (with README + template)
- `client-voice-data/docs/reference/` (with README)

**Cross-References Updated**:
- All `*_SEMANTIC.md` files now point to `../../../docs/reference/<ENTITY>.md`
- All data dictionary files now point to `../../_domain/_docs/reference/<ENTITY>_SEMANTIC.md`

**Enforcement Mechanisms**:
1. Cursor Rule auto-applies on relevant globs
2. `@investigate-entity` skill generates both files in correct locations
3. PowerShell validation script added to rule
4. LESSONS_LEARNED.md updated with pattern

**Standard Structure (Final)**:
```
<project>/
├── _domain/
│   └── _docs/
│       ├── decisions/           # ADRs
│       └── reference/           # SEMANTIC docs (*_SEMANTIC.md)
└── docs/
    └── reference/               # Data dictionaries (*.md)
```

---

## Archive Metadata

- **Source**: `DECISIONS_IN_PROGRESS.md` § 12
- **Session**: 2026-02-05 (second part)
- **Archived by**: @session-end skill
