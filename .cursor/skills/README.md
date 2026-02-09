# Cursor Skills - Capim Ecosystem

> **Version**: 2.0  
> **Last Updated**: 2026-02-03  
> **Migrated From**: `.agent/workflows/` and `.agent/skills/`

---

## 📚 Skills Index

### Core Workflows

Gerenciamento de sessões e decisões.

| Skill | Description | Invocation |
|-------|-------------|------------|
| **[session-start](session-start/SKILL.md)** | Initialize work session with memory context and domain selection | `@session-start` |
| **[session-end](session-end/SKILL.md)** | Archive executed decisions and create session notes | `@session-end` |
| **[debate](debate/SKILL.md)** | Structured decision-making for complex topics with trade-offs | `@debate` or auto-detect |

### Specialized Skills

Tarefas específicas do domínio e ontologia.

| Skill | Description | Invocation |
|-------|-------------|------------|
| **[clinic-health-check](clinic-health-check/SKILL.md)** | Multi-domain health diagnostic for specific clinic | `@clinic-health-check <clinic_id>` |
| **[investigate-entity](investigate-entity/SKILL.md)** | Profile Snowflake tables following Zero Assumptions protocol | `@investigate-entity <SCHEMA.TABLE>` |
| **[validate-axioms](validate-axioms/SKILL.md)** | Validate ontology axioms against Snowflake data | `@validate-axioms` |
| **[curate-memory](curate-memory/SKILL.md)** | Housekeeping for memory files (archive, cleanup) | `@curate-memory` |

---

## 🚀 Quick Start

### Starting a Work Session

```
User: @session-start

Agent: 
📋 **Context Loaded**

**Pending (3 items):**
- [Priority 2]: Investigate SaaS patients → ⏳ Pending
- [Priority 5]: Populate vox_popular → ⚠️ Blocked
...

Qual domínio você quer focar hoje?

[Interactive selection]
○ FINTECH (bnpl-funil)
○ SAAS (ontologia-cf)
○ CLIENT_VOICE (client-voice)
○ ECOSYSTEM (meta-ontology)
```

### During Work

Skills are **auto-detected** when appropriate:

```
User: Como devemos estruturar isso? X ou Y?

Agent: [auto-invokes @debate]
**Decision Required**: Estrutura de...

[Presents options, makes recommendation, waits for confirmation]
```

### Ending a Session

```
User: @session-end

Agent:
📦 **Items Ready to Archive:**
- [X.Y] Decision topic — Executed
- [A.B] Another decision — Rejected

Move to archive? [Yes/No]

[Creates session notes, reflective checkout]
```

---

## 🎯 Integration with Rules

Skills work seamlessly with Cursor Rules:

| Rule | Enforces | Applies When |
|------|----------|--------------|
| **[memory_governance.mdc](../rules/memory_governance.mdc)** | Atomic decision tracking | Editing `_memory/**/*.md` |
| **[snowflake_data.mdc](../rules/snowflake_data.mdc)** | Snowflake-first, Zero Assumptions | Working with `**/*.sql`, `**/*.py` |
| **[ontology_reasoning.mdc](../rules/ontology_reasoning.mdc)** | Cross-domain reasoning, axiom validation | Ontology queries |

**Benefit**: Protocol enforcement is **automatic**. No need to "remember" to follow rules.

---

## 📂 Skill Structure

Each skill follows this structure:

```
<skill-name>/
├── SKILL.md              # Main documentation
└── scripts/              # Optional: Python automation scripts
    └── <script>.py
```

**SKILL.md sections**:
1. **Quando Usar** — When to invoke the skill
2. **Pré-requisitos** — Prerequisites
3. **Passos de Execução** — Step-by-step execution
4. **Integração** — How it integrates with Rules/other skills
5. **Referências** — Links to related docs

---

## 🆕 Creating New Skills

To create a new skill:

1. **Create folder**: `.cursor/skills/<skill-name>/`
2. **Create SKILL.md** following template of existing skills
3. **Add scripts** (optional) in `scripts/` subfolder
4. **Update this README** to index the new skill
5. **Test** the skill end-to-end
6. **Document** in migration notes if replacing legacy workflow

**Template** (minimal SKILL.md):

```markdown
---
name: My Skill
description: What this skill does
version: 1.0
---

# My Skill

Brief description.

## Quando Usar
- Situation 1
- Situation 2

## Pré-requisitos
- Requirement 1

## Passos de Execução

### 1. Step One
...

### 2. Step Two
...

## Integração
- Works with: Rule X, Skill Y
```

---

## 🔄 Migration Notes

**From Antigravity** (`.agent/`):

All workflows and skills have been migrated:

| Antigravity | Cursor | Status |
|-------------|--------|--------|
| `workflows/session-start.md` | `session-start/SKILL.md` | ✅ Migrated |
| `workflows/session-end.md` | `session-end/SKILL.md` | ✅ Migrated |
| `workflows/debate.md` | `debate/SKILL.md` | ✅ Migrated |
| `skills/clinic-health-check/` | `clinic-health-check/` | ✅ Migrated |
| `skills/investigate-entity/` | `investigate-entity/` | ✅ Migrated |
| `skills/curate-memory/` | `curate-memory/` | ✅ Migrated |
| `skills/validate-axioms/` | `validate-axioms/` | ✅ Migrated |

**See full migration guide**: [`../../docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md`](../../docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md)

---

## 📊 Skill Usage Patterns

### Common Workflows

**Daily Work Session**:
```
@session-start
  → Work on tasks
  → @debate (when needed)
  → @investigate-entity (when needed)
@session-end
```

**Governance Review**:
```
@validate-axioms
  → Fix violations
  → Update DECISIONS_IN_PROGRESS.md
@curate-memory
```

**Clinic Investigation**:
```
@clinic-health-check <clinic_id>
  → Deep dive into issues
  → @debate remediation options
  → Document in session notes
```

---

## 🛠️ Troubleshooting

### Skill Not Invoking?

**Check**:
1. Syntax: `@skill-name` (with `@` prefix)
2. Spelling: Exact match to folder name
3. Auto-detection: Try explicit invocation first

### Scripts Not Working?

**Check**:
1. **Path**: Scripts use relative paths from workspace root
2. **Dependencies**: `snowflake-connector-python`, `pandas`, etc. installed
3. **Credentials**: `.env` file configured for Snowflake

### Rules Not Applying?

**Check**:
1. **Glob patterns**: File matches pattern in Rule's `globs` field
2. **File location**: Working in correct directory
3. **Rule syntax**: `.mdc` format correct (YAML frontmatter + markdown)

---

## 📚 Additional Resources

**Documentation**:
- [Migration Guide](../../docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md) — Full Antigravity → Cursor migration details
- [Test Workflow](TEST_WORKFLOW.md) — End-to-end validation tests
- [START_HERE_ECOSYSTEM.md](../../START_HERE_ECOSYSTEM.md) — Architecture overview
- [MEMORY_ARCHITECTURE_CONSTITUTION.md](../../MEMORY_ARCHITECTURE_CONSTITUTION.md) — Governance principles

**Rules**:
- [memory_governance.mdc](../rules/memory_governance.mdc) — Atomic decision tracking
- [snowflake_data.mdc](../rules/snowflake_data.mdc) — Snowflake-first protocol
- [ontology_reasoning.mdc](../rules/ontology_reasoning.mdc) — Cross-domain reasoning

---

## ✅ Checklist for New Skills

When creating a new skill:

- [ ] Folder created in `.cursor/skills/<skill-name>/`
- [ ] `SKILL.md` documented with all sections
- [ ] Scripts (if any) added to `scripts/` subfolder
- [ ] Integration with Rules documented
- [ ] Tested end-to-end
- [ ] Added to this README index
- [ ] If migrating: Legacy reference added to SKILL.md frontmatter

---

**Last Updated**: 2026-02-03  
**Total Skills**: 7 (3 core workflows + 4 specialized)
