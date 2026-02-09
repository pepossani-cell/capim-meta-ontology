# Debate Questions for Semantic Documentation

> **Purpose**: Structured questions to extract business context from user during entity investigation  
> **Used by**: `@investigate-entity` skill (Step 2: Debate)  
> **Output**: Content for SEMANTIC doc (`<ENTITY>_SEMANTIC.md`)

---

## Why These Questions Matter

**Profiling gives you**: "49.7% null" (fact)  
**Debate gives you**: "WHY it's null and WHY that's OK" (context)

These questions extract the **semantic layer** that profiling cannot discover.

---

## Business Definition

**Goal**: One-sentence definition of what this entity represents

**Questions**:
- "What does this entity represent in one sentence?"
- "Why does this entity exist? What problem does it solve?"
- "If you had to explain this entity to a new team member, what would you say?"

**Example answer**:
> "ZENDESK_TICKETS_ENHANCED_V1 tracks customer support interactions with LLM-enhanced categorization and sentiment analysis."

---

## Use Cases

**Goal**: Understand who uses this and for what

**Questions**:
- "What business questions does this entity answer?"
- "Who uses this entity and for what purpose?"
- "Give me 3 example queries this entity powers."
- "What dashboards or reports consume this data?"

**Example answer**:
> Used by CX team for support volume analysis, by product team for feature pain points identification, and by exec team for NPS correlation.

---

## Semantic Nuances

**Goal**: Understand meaning beyond data types

**Questions**:
- "What's the business meaning of status values?" (not just "open/closed", but WHY)
- "Why do certain fields have high null rates?" (business reason, not just stats)
- "Are there different 'universes' or contexts within this entity?" (e.g., B2B vs B2C)
- "What do timestamps represent?" (event time vs ingestion time vs processing time?)
- "Are there special cases or edge cases that affect interpretation?"

**Example answer**:
> High null rate on `clinic_id` (49.7%) is expected: B2C tickets (debt collection) are patient-centric, not clinic-centric. This is the "Ghost phenomenon" - not a data quality issue.

---

## Grain & Uniqueness

**Goal**: Validate business understanding of grain

**Questions**:
- "Is the grain correct? (1 row per what?)"
- "What makes each row unique from a business perspective?"
- "Are there legitimate duplicates?" (e.g., reprocessing, versioning)
- "Should there be deduplication logic when querying?"

**Example answer**:
> 1 row per support ticket. `ticket_id` is unique. No legitimate duplicates - if found, indicates data quality issue.

---

## Relationships

**Goal**: Understand upstream dependencies and downstream consumers

**Questions**:
- "What are the upstream source systems?" (Where does data come from?)
- "What entities does this JOIN with most frequently?"
- "Are the FK relationships documented accurate?"
- "What entities depend on this one?" (Downstream consumers)
- "Is this entity Tier 1 (core), Tier 2 (derived), or Tier 3 (aggregated)?"

**Example answer**:
> Upstream: Zendesk API via n8n. JOINs with CLINICS (via clinic_id), PATIENTS (via CPF - rare). Consumed by: VoC Dashboard, CX Weekly Reports, Churn Analysis Pipeline. Tier 1 (core source).

---

## Limitations & Caveats

**Goal**: Document what this entity CANNOT answer

**Questions**:
- "What are KNOWN LIMITATIONS? What can this entity NOT answer?"
- "Are there critical caveats users must know?"
- "What common mistakes do people make with this entity?"
- "What questions does this entity seem to answer but actually doesn't?"
- "Are there historical periods where data is unreliable?"

**Example answer**:
> - Cannot track ticket resolution quality (no satisfaction survey)
> - Cannot link to financial impact (no revenue attribution)
> - B2C tickets before 2024-06 lack CPF linkage
> - Common mistake: treating NULL clinic_id as error (it's expected for B2C)

---

## Privacy & Sensitivity

**Goal**: Classify PII risk and handling requirements

**Questions**:
- "Is this PII sensitive? What's the privacy context?"
- "Are there columns that require special handling?" (masking, encryption, access control)
- "What is the data retention policy?"
- "Can this data be used in training data for ML?"
- "Are there LGPD/GDPR considerations?"

**Example answer**:
> PII: `requester_email`, `description` (may contain personal details), `cpf` (when present). Retention: 2 years. Cannot be used in ML training without anonymization. Access: Restricted to CX and Product teams.

---

## Temporal Characteristics

**Goal**: Understand time-based behavior

**Questions**:
- "Is this entity append-only or can rows be updated?"
- "What does the primary timestamp represent?" (event time, ingestion time, processing time)
- "Are there temporal drifts or rollout dates?"
- "Is there seasonality or expected patterns?"
- "Are historical records backfilled or only recent?"

**Example answer**:
> Append-only. `created_at` is ticket creation time (Zendesk event time). Enhanced daily via n8n. Data available from 2023-01 (backfilled). Seasonality: peak in January (New Year resolutions) and July (mid-year reviews).

---

## Technical Validation Confirmation

**Goal**: Validate technical findings against business expectations

**Questions**:
- "Does the row count match expectations?" (order of magnitude check)
- "Are the null percentages expected or concerning?"
- "Are categorical domains complete?" (missing expected values?)
- "Are there unexpected values in categorical columns?"

**Example answer**:
> ~45k tickets expected (matches). 49.7% null clinic_id is expected (B2C). Categorical domains complete. Unexpected: 2 tickets with categoria='UNKNOWN' (investigation needed).

---

## Documentation Confidence

**Goal**: Assess confirmation level of documentation

**Questions**:
- "Is this documentation confirmed by source system owner or heuristic?"
- "Are there unknowns that require follow-up?"
- "What's the confidence level?" (High = validated, Medium = inferred, Low = assumed)

**Example answer**:
> Confidence: High (validated with CX team lead). Unknown: exact LLM model used for categorization (n8n config not documented). Follow-up: confirm data retention policy with legal.

---

## Output Format

Answers to these questions should be synthesized into the SEMANTIC doc sections:

1. **Business Definition** → from "Business Definition" questions
2. **Grain (Business Perspective)** → from "Grain & Uniqueness" questions
3. **Key Relationships** → from "Relationships" questions
4. **Common Questions This Answers** → from "Use Cases" questions
5. **Status Semantics** → from "Semantic Nuances" questions
6. **Limitations & Caveats** → from "Limitations & Caveats" questions
7. **PII & Sensitivity** → from "Privacy & Sensitivity" questions
8. **Source & Confirmation** → from "Documentation Confidence" questions

---

**Note**: Not all questions are mandatory. Tailor to entity context. Prioritize questions that resolve ambiguity or prevent common mistakes.
