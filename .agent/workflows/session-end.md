---
description: How to properly end a work session on the Capim Ecosystem
---

# Session End Workflow

**Optional** workflow for consolidating session notes and archiving completed decisions.

> **Model**: Decision-centric — decisions are saved immediately during conversation. This workflow is for *archiving* and *consolidation*.

## When to Use

- End of work day
- Completing a major milestone
- When DECISIONS_IN_PROGRESS.md has many ✅ items that were executed
- Before a long break (vacation, etc.)
- User says `/session-end` or "let's wrap up"

## Steps

### 1. Review DECISIONS_IN_PROGRESS.md
// turbo
Read the current state:
```
View file: capim-meta-ontology/_memory/DECISIONS_IN_PROGRESS.md
```

### 2. Identify Items to Archive
Look for items that are BOTH:
- Status: ✅ Decided (or ❌ Rejected)
- AND: Already executed/implemented

Ask user to confirm which items should be archived:
```
📦 **Items Ready to Archive:**

The following decisions have been executed:
- [1.1] Cenário C (Híbrido) — files created
- [1.4] Folder naming convention — structure implemented

Move these to archive? [Yes/No/Select specific]
```

### 3. Create/Update Archive File
Create `_memory/DECISIONS_ARCHIVE/YYYY-MM_topic.md`:

```markdown
# 📁 Decision Archive: {Topic} ({YYYY-MM})

## Archived: {date}

### {ID} {Title}
- **Status**: ✅ Decided + Executed
- **Decision**: {decision text}
- **Rationale**: {why this was chosen}
- **Executed On**: {date}
- **Related Files**: {list of files affected}
```

### 4. Remove from DECISIONS_IN_PROGRESS.md
Remove the archived items from the active tracker, keeping only:
- 🔄 In Debate
- ⏳ Pending (not yet executed)

### 5. Create/Update Session Note
Create `_memory/SESSION_NOTES/YYYY-MM-DD.md` with:
- What was accomplished
- What was archived
- What remains pending

### 6. Reflective Checkout
```
🧘 **Reflective Checkout**

**Archived:** {count} decisions moved to archive
**Still Pending:** {count} items remain in progress

**Knowledge Harvested:**
- {patterns discovered}

**Next Session:**
- Start with `/session-start` or read DECISIONS_IN_PROGRESS.md
```

---

## Archive File Naming Convention

| Type | File Name | Example |
| :--- | :--- | :--- |
| By topic | `YYYY-MM_topic.md` | `2026-02_architecture.md` |
| By month (general) | `YYYY-MM.md` | `2026-02.md` |

---

## Example Full Flow

```
User: /session-end

Agent: 📦 **Items Ready to Archive:**

✅ Executed:
- [1.1] Cenário C (Híbrido)
- [3.4] Session model (decision-centric)

⏳ Still Pending:
- [1.2] Rename project_refactor → _domain
- [2.4] Add client_voice PG credentials

Move executed items to archive? [Yes/No]

User: Yes

Agent: ✅ Archived 2 items to `_memory/DECISIONS_ARCHIVE/2026-02_architecture.md`
✅ Updated DECISIONS_IN_PROGRESS.md (2 items removed)
✅ Created session note: `_memory/SESSION_NOTES/2026-02-01.md`

🧘 **Reflective Checkout**
- Archived: 2 decisions
- Pending: 4 items
- Next: `/session-start` to continue

See you next time! 👋
```
