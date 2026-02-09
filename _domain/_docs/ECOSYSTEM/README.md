# ECOSYSTEM Entities

> **Purpose**: Cross-domain entities that are TRULY shared across multiple domains.
> **Last Updated**: 2026-02-03

---

## What Belongs in ECOSYSTEM?

**ONLY entities that meet ALL criteria**:

1. ✅ Referenced by 2+ domains (SAAS, FINTECH, CLIENT_VOICE)
2. ✅ Entity semantics are IDENTICAL across domains
3. ✅ No single domain "owns" the entity exclusively

**Examples of valid ECOSYSTEM entities**:
- `CLINICS` — Shared across SAAS (operations), FINTECH (credit), CLIENT_VOICE (support)
- `PATIENTS` — Shared across SAAS (appointments), FINTECH (borrowers), CLIENT_VOICE (tickets)

---

## What Does NOT Belong Here?

**Domain-specific entities** should live in the domain project's `_domain/_docs/reference/`:

### CLIENT_VOICE Domain

❌ **Moved to**: `client-voice-data/_domain/_docs/reference/`

**Entities**:
- `ZENDESK_TICKETS` (was in ECOSYSTEM, moved on 2026-02-03)
- `ZENDESK_USERS` (was in ECOSYSTEM, moved on 2026-02-03)
- `ZENDESK_COMMENTS` (was in ECOSYSTEM, moved on 2026-02-03)
- `TICKET_ANALYSIS`

**Rationale**: These are CLIENT_VOICE domain entities, not cross-domain. Even though they reference CLINICS, they are owned and managed by CLIENT_VOICE.

### SAAS Domain

**Location**: `ontologia-saas/_domain/_docs/reference/`

**Entities**:
- `APPOINTMENTS`
- `USERS` (SaaS platform users, NOT Zendesk users)
- `CLINIC_CONFIGS`

### FINTECH Domain

**Location**: `bnpl-funil/_domain/_docs/reference/`

**Entities**:
- `CREDIT_SIMULATIONS`
- `CREDIT_CHECKS`
- `PRE_ANALYSES`
- `BORROWERS`

---

## Decision Log

### 2026-02-03: ZENDESK Entities Moved to CLIENT_VOICE

**Decision**: Moved `ZENDESK_TICKETS`, `ZENDESK_USERS`, `ZENDESK_COMMENTS` from ECOSYSTEM to `client-voice-data`.

**Rationale**:
- ZENDESK is exclusively owned by CLIENT_VOICE domain
- Other domains may JOIN to ZENDESK, but they don't define its semantics
- Violates "no single domain owns" criterion
- Aligns with Dual Documentation Pattern (DECISIONS_IN_PROGRESS § 10.2)

**Reference**: `_memory/DECISIONS_IN_PROGRESS.md` § 10.2

---

## Promotion Criteria (When to Add to ECOSYSTEM)

Before adding an entity to ECOSYSTEM, verify:

1. **Multi-domain usage**:
   ```sql
   -- Can you answer this from 2+ domains?
   SELECT * FROM <ENTITY> 
   WHERE domain_context IN ('SAAS', 'FINTECH', 'CLIENT_VOICE')
   ```

2. **Semantic consistency**:
   - Does "active" mean the same thing in all domains?
   - Are the grain and keys consistent?

3. **No exclusive ownership**:
   - Which team updates this entity?
   - If answer is "only SaaS team" → NOT ecosystem

4. **Federation benefit**:
   - Would centralizing documentation reduce confusion?
   - Or would it make domain-specific knowledge harder to find?

---

## Current ECOSYSTEM Entities

*As of 2026-02-03, ECOSYSTEM is EMPTY after ZENDESK migration.*

**TODO**: Evaluate promotion of:
- `CLINICS` (currently in SAAS, but used by all domains)
- `PATIENTS` (currently in SAAS, but used by all domains)

---

## Dual Documentation Pattern

**All ECOSYSTEM entities MUST follow** the Dual Documentation Pattern:

- `<ENTITY>_SEMANTIC.md` — Business context (Why/Map)
- `<ENTITY>.md` — Technical details (How/X-Ray)

**Reference**: `.cursor/rules/entity_documentation.mdc`

---

## Questions?

If uncertain whether an entity belongs in ECOSYSTEM:

1. **Start with domain project** (default)
2. **Debate promotion** after observing cross-domain usage patterns
3. **Use `@debate` skill** to evaluate trade-offs

**Better to start domain-specific** and promote later than to start ECOSYSTEM and create confusion.
