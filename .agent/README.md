# ⚠️ DEPRECATED: Migration to Cursor

> **Status**: Legacy Reference Only  
> **Migration Date**: 2026-02-03  
> **Replaced By**: `.cursor/skills/` and `.cursor/rules/`

---

## ⚠️ IMPORTANT NOTICE

**This folder is NO LONGER ACTIVE.**

All workflows and skills have been **migrated to Cursor** and are now located in:

- **`.cursor/skills/`** — All skills (workflows + specialized)
- **`.cursor/rules/`** — Behavioral protocols (memory governance, snowflake, ontology)

---

## 🔄 Migration Summary

### What Was Migrated

**Workflows** → `.cursor/skills/`:
- `workflows/session-start.md` → `.cursor/skills/session-start/SKILL.md`
- `workflows/session-end.md` → `.cursor/skills/session-end/SKILL.md`
- `workflows/debate.md` → `.cursor/skills/debate/SKILL.md`

**Skills** → `.cursor/skills/`:
- `skills/clinic-health-check/` → `.cursor/skills/clinic-health-check/`
- `skills/investigate-entity/` → `.cursor/skills/investigate-entity/`
- `skills/curate-memory/` → `.cursor/skills/curate-memory/`
- `skills/validate-axioms/` → `.cursor/skills/validate-axioms/`

**Protocolos** → `.cursor/rules/`:
- Session protocol → `memory_governance.mdc`
- Snowflake-first → `snowflake_data.mdc`
- Ontology reasoning → `ontology_reasoning.mdc`

---

## 🚫 Do NOT Use This Folder

**Why?**

1. **Outdated**: Workflows hardcoded for Antigravity
2. **Duplicated**: Scripts já migrados para `.cursor/`
3. **No enforcement**: Protocols não aplicam automaticamente
4. **Incomplete**: Missing integration with Cursor tools (AskQuestion, etc.)

**Instead, use**:
- `@session-start` instead of `/session-start`
- `@debate` instead of manually following `workflows/debate.md`
- `.cursor/skills/` for all active skills

---

## 📚 Why Keep This Folder?

**Historical reference**:
- Original design decisions documented
- Scripts podem servir como base para futuras melhorias
- Useful para entender evolution do sistema

**NOT for production use**.

---

## 📖 Migration Guide

For full details on the migration and how to use the new system:

**See**: `docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md`

**Quick links**:
- `.cursor/skills/` — All active skills
- `.cursor/rules/` — Behavioral protocols
- `.cursor/skills/TEST_WORKFLOW.md` — Validation tests
- `START_HERE_ECOSYSTEM.md` — Updated architecture overview

---

## ✅ Action Required

If you're still using workflows from this folder:

1. **Stop** using `/session-start`, `/session-end`, etc.
2. **Start** using `@session-start`, `@session-end`, etc.
3. **Read** the migration guide: `docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md`
4. **Update** bookmarks/habits to reference `.cursor/` instead

---

## 🎯 Summary

| Old (Antigravity) | New (Cursor) | Status |
|-------------------|--------------|--------|
| `.agent/workflows/` | `.cursor/skills/` | ✅ Migrated |
| `.agent/skills/` | `.cursor/skills/` | ✅ Migrated |
| Manual protocols | `.cursor/rules/` | ✅ Automated |

**Active system**: `.cursor/`  
**Deprecated system**: `.agent/` (this folder)

---

**For questions or issues with the new system**, see:
- Migration guide: `docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md`
- Test workflow: `.cursor/skills/TEST_WORKFLOW.md`
- Rules documentation: `.cursor/rules/*.mdc`
