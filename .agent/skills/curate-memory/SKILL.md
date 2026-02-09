---
name: Curate Memory
description: Automates the governance and housekeeping of ontology memory files (DECISIONS_IN_PROGRESS, SESSION_NOTES).
---

# Curate Memory Skill

This skill ensures that memory files remain concise and actionable by moving completed or rejected items to permanent archives.

## When to Use

- At the end of every work session (`/session-end`).
- When `DECISIONS_IN_PROGRESS.md` becomes too large or cluttered.
- To formalize the transition from "active debate" to "permanent record".

## How to Execute

### CLI
```bash
cd capim-meta-ontology
python .agent/skills/curate-memory/scripts/curate.py
```

## Logic Rules

1. **Auto-Archive**: Items in `DECISIONS_IN_PROGRESS.md` marked with `✅➡️` (Executed) or `❌` (Rejected) are extracted.
2. **Permanent Storage**: Extracted items are appended to `_memory/DECISIONS_ARCHIVE/YYYY-MM_archived_decisions.md`.
3. **Session Notes**: Moves the "(In Progress)" section of session notes to `_memory/SESSION_NOTES/YYYY-MM-DD.md`.
4. **Cleanup**: Removes archived items from the active tracker while preserving headers and pending items.

## Files

- `scripts/curate.py`: The automation engine.
- `SKILL.md`: This manual.
