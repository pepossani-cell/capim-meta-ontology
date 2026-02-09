# MEMORY SYSTEM

> **Purpose**: Organizational memory for the Capim Ecosystem project.
> **Reference**: [MEMORY_ARCHITECTURE_CONSTITUTION.md](../MEMORY_ARCHITECTURE_CONSTITUTION.md) §DIRECTIVE:SLEEP_TIME_COMPUTE

---

## 📁 Structure

```
_memory/
├── README.md                    # This file
├── DECISIONS_IN_PROGRESS.md     # Active decisions tracker
├── LESSONS_LEARNED.md           # Consolidated patterns
├── SESSION_NOTES/               # Per-session working notes
│   └── YYYY-MM-DD.md
└── DECISIONS_ARCHIVE/           # Completed decision records
    └── YYYY-MM_topic.md
```

---

## 🔄 Lifecycle

| Stage | Location | Duration | Trigger to Move |
| :--- | :--- | :--- | :--- |
| **Active Debate** | SESSION_NOTES/ | 1 session | — |
| **Tracking** | DECISIONS_IN_PROGRESS.md | Until executed | Decision confirmed |
| **Archive** | DECISIONS_ARCHIVE/ | Permanent | `/session-end` (when ✅➡️) |
| **Consolidate** | LESSONS_LEARNED.md | Permanent | Pattern emerges |

### Archive Rule
- **✅ Decided** items stay in DECISIONS_IN_PROGRESS.md
- **✅➡️ Executed** items are archived during `/session-end`
- **❌ Rejected** items are archived during `/session-end`
- This keeps DECISIONS_IN_PROGRESS.md focused on **current** work

---

## 📝 When to Create Notes

- **SESSION_NOTES**: Start of every substantial work session
- **DECISIONS_IN_PROGRESS**: When a decision needs tracking across sessions
- **DECISIONS_ARCHIVE**: When a decision is fully implemented
- **LESSONS_LEARNED**: When a pattern emerges that should inform future work

---

## 🧹 Maintenance

- **Weekly**: Review DECISIONS_IN_PROGRESS, update statuses
- **Monthly**: Archive completed decisions, extract lessons
- **Quarterly**: Review LESSONS_LEARNED, prune obsolete patterns
