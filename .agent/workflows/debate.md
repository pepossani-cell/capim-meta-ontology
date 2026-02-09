---
description: How to structure and track debates on complex topics
---

# Debate Workflow

Use this workflow when a discussion involves multiple options, trade-offs, or requires formal decision-making.

## Triggers

Activate this workflow when:
- User asks "what do you think about X vs Y?"
- Topic has more than 2 viable options
- Decision will affect multiple files or systems
- User seems uncertain about direction

## Steps

### 1. Frame the Question
Clearly state what is being decided:
```
**Decision Required:** [Clear statement of what needs to be decided]
**Context:** [Why this decision matters]
**Constraints:** [Any limitations or requirements]
```

### 2. Present Options
Use a structured table:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A | ... | ... | ... |
| B | ... | ... | ... |
| C | ... | ... | ... |

### 3. Make a Recommendation
Always provide a recommendation with rationale:
```
**Recommendation:** Option [X]
**Rationale:** [Why this option is preferred]
```

### 4. Wait for Confirmation
Do NOT proceed to execution without explicit user confirmation.

**Trigger words that indicate confirmation:** "sim", "ok", "confirmado", "aprovado", "vamos com X"

### 5. Document Decision — IMMEDIATELY
// turbo
**⚠️ CRITICAL: Do this BEFORE continuing with the next question or topic.**

Once a decision is confirmed:
1. **STOP** the debate flow
2. Update `_memory/DECISIONS_IN_PROGRESS.md` with the specific decision
3. Then resume discussion

Do NOT wait for all questions to be answered. Each decision is an atomic checkpoint.

### 6. Consolidate (End of Debate)
Once all questions are resolved:
- Add session summary to session notes
- If pattern emerges, add to `LESSONS_LEARNED.md`
- Mark decisions as "ready for execution" if applicable

---

## Anti-Patterns

❌ **Don't:**
- Present options without a recommendation
- Execute before confirmation on structural changes
- Use vague language ("maybe", "could be")
- Skip the trade-offs analysis

✅ **Do:**
- Be honest about uncertainty
- Present clear trade-offs
- Make a decisive recommendation
- Update tracking documents

---

## Example

```
**Decision Required:** How to structure ontology across multiple projects?

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A | Centralize in meta-ontology | Single source of truth | Far from code |
| B | Keep in each project | Close to code | Duplication risk |
| C | Hybrid | Best of both | More complex |

**Recommendation:** Option C (Hybrid)
**Rationale:** Balances proximity to code with federation benefits.

Confirm to proceed? [Yes/No/Discuss more]
```
