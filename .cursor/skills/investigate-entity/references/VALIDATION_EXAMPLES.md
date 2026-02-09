# Validation Examples & Checklists

> **Purpose**: Practical examples and validation checklists for Dual Documentation Protocol  
> **Used by**: `@investigate-entity` skill (Steps 3-5: Document, Link, Validate)  
> **Reference**: `.cursor/rules/entity_documentation.mdc`

---

## Critical Distinction: What Goes Where?

### Example Scenario: Profiling `ZENDESK_TICKETS_ENHANCED_V1`

#### Profiling Output (Raw Facts)

```
Column: clinic_id_enhanced
Type: NUMBER
Nullable: Yes
% Null: 49.7%
Distinct Values: 12,084
Top 10 Values:
  - 1234: 324 occurrences
  - 5678: 289 occurrences
  - ...
```

---

### How This Appears in AGENTIC Doc

**File**: `ZENDESK_TICKETS.md`

```markdown
## Column Profile

| Column | Type | % Null | Distinct | Notes |
|--------|------|--------|----------|-------|
| clinic_id_enhanced | NUMBER | 49.7% | 12,084 | Improved from 53.6% null in raw table |

## Domain Analysis: clinic_id_enhanced

**Type**: NUMBER (FK to CLINICS.clinic_id)

**Null Pattern**: 49.7% null (22,389 of 45,123 rows)

**Distinct Values**: 12,084 clinics represented

**Top 10 Clinics by Ticket Volume**:
- 1234: 324 tickets
- 5678: 289 tickets
- ...
```

**Tone**: Data-driven, no interpretation. Stats as-is from profiling.

---

### How This Appears in SEMANTIC Doc

**File**: `ZENDESK_TICKETS_ENHANCED_SEMANTIC.md`

```markdown
## The "Ghost" Phenomenon

**High Null Rate on `clinic_id` is Expected**

B2C Tickets (debt collection, patient support) have near-zero identification 
with `clinic_id` (0.08% linkage rate for B2C tickets).

**This is NOT a data quality error.** B2C tickets belong to the Patient/Debtor 
Ontology, not the Clinic Ontology.

### Why This Matters

**Common Mistake**: Treating NULL `clinic_id` as "bad data" leads to incorrect 
assumptions about data completeness.

**Correct Interpretation**: 
- ~50% of tickets are B2C (patient-centric) → NULL clinic_id is expected
- ~50% of tickets are B2B (clinic-centric) → clinic_id should be populated

### Querying Implications

When analyzing clinic-related support:
```sql
-- WRONG: Includes B2C tickets as "unlinked" (inflates error rate)
SELECT COUNT(*) FROM tickets WHERE clinic_id IS NULL

-- RIGHT: Filter to B2B persona first
SELECT COUNT(*) FROM tickets 
WHERE persona = 'B2B' AND clinic_id IS NULL  -- Now this IS an error
```
```

**Tone**: Explanatory, provides "Why" and strategic context. No raw stats (uses "~50%" instead of "49.7%").

---

## Key Takeaway

**Profiling gives you**: "49.7% null" (fact)  
**Debate gives you**: "WHY it's null and WHY that's OK" (context)

**AGENTIC doc** = Facts from profiling  
**SEMANTIC doc** = Interpretation from debate

**Never mix**:
- ❌ Don't put "49.7%" in SEMANTIC (use qualitative descriptions like "high", "~50%")
- ❌ Don't put "This is expected because..." in AGENTIC (stick to facts)

---

## Validation Checklist

### Structure Validation

After generating both docs, validate structure:

- [ ] **Both files exist**:
  - `<ENTITY>.md` (AGENTIC)
  - `<ENTITY>_SEMANTIC.md` (SEMANTIC)

- [ ] **Naming is correct**:
  - Follows pattern: `<ENTITY>.md` and `<ENTITY>_SEMANTIC.md`
  - Uses UPPERCASE for entity name (e.g., `ZENDESK_TICKETS.md`, not `zendesk_tickets.md`)

- [ ] **Cross-references in headers**:
  ```markdown
  > **Related Reference**: [<ENTITY>.md](./<ENTITY>.md)
  > **Related Reference**: [<ENTITY>_SEMANTIC.md](./<ENTITY>_SEMANTIC.md)
  ```

- [ ] **Domain identified**:
  ```markdown
  > **Domain**: <DOMAIN_ID>
  ```

- [ ] **ENTITY_INDEX.yaml updated**:
  ```yaml
  <ENTITY_NAME>:
    documentation:
      semantic: "reference/<ENTITY>_SEMANTIC.md"
      agentic: "reference/<ENTITY>.md"
  ```

---

### Content Validation (AGENTIC Doc)

- [ ] **All stats are DATA-DRIVEN**:
  - No guesses, only profiling results
  - Exact percentages (e.g., "49.7% null", not "~50%")
  - Exact counts and distributions

- [ ] **No business narrative**:
  - Avoid phrases like "This is expected because..."
  - Avoid "Why" explanations
  - Stick to "What" (facts)

- [ ] **Schema section complete**:
  - Column names, types, nullable status
  - Row count, date range (if temporal)

- [ ] **Column profile section**:
  - Null percentages per column
  - Distinct value counts
  - Data types

- [ ] **Domain analysis** (for categorical/boolean):
  - Top values with counts
  - Distributions

- [ ] **Relationships section**:
  - FK mappings (if applicable)
  - Cardinality (1:1, 1:many, many:many)

- [ ] **Query Optimization Tips**:
  - Indexed columns (if known)
  - Join strategies
  - Partitioning (if applicable)

---

### Content Validation (SEMANTIC Doc)

- [ ] **All "Why" statements come from DEBATE**:
  - Not inferred from profiling alone
  - Validated with user or domain expert

- [ ] **No profiling stats**:
  - Use qualitative descriptions ("high null rate", not "49.7%")
  - Use approximate values ("~12k clinics", not "12,084 clinics")
  - Focus on meaning, not numbers

- [ ] **Business Definition section**:
  - 1-2 sentence definition
  - Why entity exists

- [ ] **Grain (Business Perspective)**:
  - What does one row represent?
  - Business uniqueness criteria

- [ ] **Key Relationships**:
  - Upstream sources (where data comes from)
  - Downstream consumers (who uses this)
  - Join patterns

- [ ] **Common Questions This Answers**:
  - 3-5 example use cases
  - Business value

- [ ] **Limitations & Caveats**:
  - What this entity CANNOT answer
  - Common mistakes
  - Known gaps

- [ ] **PII & Sensitivity** (if applicable):
  - Privacy classification
  - Handling requirements

- [ ] **Source & Confirmation**:
  - Source system
  - Confidence level (High/Medium/Low)

---

### Tone Validation

**AGENTIC Doc**:
- [ ] Precise, technical, query-ready
- [ ] Sounds like database schema documentation
- [ ] No storytelling or explanation of "why"

**SEMANTIC Doc**:
- [ ] Narrative, explanatory, context-rich
- [ ] Sounds like a user guide or business glossary
- [ ] Explains "why" and "what it means"

---

## Common Pitfalls (Anti-Patterns)

### ❌ Mixing Concerns

**Bad** (AGENTIC with narrative):
```markdown
## Column Profile

| Column | Type | % Null |
|--------|------|--------|
| clinic_id | NUMBER | 49.7% |

**Note**: This high null rate is expected because B2C tickets are patient-centric 
and don't belong to a specific clinic.
```

**Good** (AGENTIC stays factual):
```markdown
## Column Profile

| Column | Type | % Null | Notes |
|--------|------|--------|-------|
| clinic_id | NUMBER | 49.7% | FK to CLINICS.clinic_id |
```

---

**Bad** (SEMANTIC with exact stats):
```markdown
## Null Patterns

The `clinic_id` column has 49.7% null rate (22,389 of 45,123 rows), 
with 12,084 distinct clinics represented.
```

**Good** (SEMANTIC uses qualitative):
```markdown
## Null Patterns

Approximately half of tickets have no `clinic_id` linkage. This is expected 
for B2C tickets (patient-centric support) which don't belong to a clinic.
```

---

### ❌ Generating SEMANTIC Without Debate

**Bad** (guessing business context):
```markdown
## Business Definition

This entity probably tracks support tickets from customers who contact us 
through various channels.
```

**Good** (debate-confirmed):
```markdown
## Business Definition

ZENDESK_TICKETS_ENHANCED_V1 tracks customer support interactions from both 
clinics (B2B) and individual patients/debtors (B2C), enhanced with LLM-based 
categorization and sentiment analysis.

**Source**: Confirmed with CX team lead (2024-12-15)
```

---

### ❌ Skipping Cross-References

**Bad** (files are isolated):
- `ZENDESK_TICKETS.md` exists
- `ZENDESK_TICKETS_SEMANTIC.md` exists
- No links between them

**Good** (bidirectional links):

In `ZENDESK_TICKETS.md`:
```markdown
> **Related Reference**: [ZENDESK_TICKETS_SEMANTIC.md](./ZENDESK_TICKETS_SEMANTIC.md)
```

In `ZENDESK_TICKETS_SEMANTIC.md`:
```markdown
> **Related Reference**: [ZENDESK_TICKETS.md](./ZENDESK_TICKETS.md)
```

---

## Post-Documentation Actions

After generating both docs:

1. **Validate using checklist above**
2. **Update ENTITY_INDEX.yaml** with documentation paths
3. **(Optional) Launch explore subagent** for related context
4. **Commit with descriptive message**:
   ```bash
   git add docs/reference/<ENTITY>*.md _domain/_docs/ENTITY_INDEX.yaml
   git commit -m "docs: add dual documentation for <ENTITY>
   
   - AGENTIC: schema, profiling, queries
   - SEMANTIC: business context, caveats, use cases
   - Source: profiling + debate with <DOMAIN EXPERT>
   - Confidence: High"
   ```

---

**Reference**: Full templates available in `.cursor/rules/entity_documentation.mdc`
