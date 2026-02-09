---
description: How to start a work session on the Capim Ecosystem
---

# Session Start Workflow

Execute these steps at the beginning of each new conversation or work block.

> **Model**: Decision-centric (save immediately after each decision, not at session end)

## When to Use

- Starting a new conversation in Antigravity
- Resuming work after a break
- User says "let's start" or `/session-start`

## Steps

### 1. Load Context
// turbo
Read the current state of decisions:
```
View file: capim-meta-ontology/_memory/DECISIONS_IN_PROGRESS.md
View file: capim-meta-ontology/_memory/LESSONS_LEARNED.md
```

### 2. Enforce Protocol
Acknowledge the following behavioral rule to yourself:
> **PROTOCOL: ATOMIC DECISION TRACKING**
> I will update `DECISIONS_IN_PROGRESS.md` **IMMEDIATELY** after any confirmed decision or significant discovery. I will not batch updates at the end.

### 2. Summarize Pending Items
Present to the user in a compact format:

```
📋 **Context Loaded**

**Pending (X items):**
- [Priority 1]: {item} — {status}
- [Priority 2]: {item} — {status}
...

**Last Activity:** {date} — {focus}

What would you like to focus on?
```

### 3. Load Domain Context (If Needed)
Based on user's choice, read the relevant START_HERE:
- SAAS: `ontologia-cf/_domain/START_HERE.md`
- FINTECH: `bnpl-funil/_domain/START_HERE.md`
- CLIENT_VOICE: `client-voice/START_HERE.md`
- ECOSYSTEM: `capim-meta-ontology/START_HERE_ECOSYSTEM.md`

### 4. Proceed
Once context is loaded, proceed with work.

**Important:** During the conversation, update DECISIONS_IN_PROGRESS.md immediately after any decision is confirmed. Do NOT wait for session end.

---

## Alternative: Quick Start

User can also just say:
> "Leia `_memory/DECISIONS_IN_PROGRESS.md` e me diga o que está pendente."

This achieves the same effect without invoking the full workflow.
