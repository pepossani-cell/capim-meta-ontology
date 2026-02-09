# ARCHITECTURE PRINCIPLES — Capim Ecosystem

> **Purpose**: Document core architectural tensions and resolution strategies  
> **Audience**: Architects, contributors, AI agents  
> **Last Updated**: 2026-02-04  
> **Status**: CANONICAL (reference for all projects)

---

## 📐 Core Architectural Tensions

### Tension 1: Centralization vs Autonomy

**The Dilemma**:

```
Centralization (DRY)                    Autonomy (Independence)
↓                                       ↓
Single source of truth                  Local ownership
Consistency across projects             Fast iteration
Coordinated changes                     Isolated changes
Efficiency                              Flexibility
```

**Our Resolution**: **3-Tier Hybrid Architecture**

We balance both forces through a tiered system that allows:
- ✅ Core capabilities remain centralized (consistency)
- ✅ Domain-specific features remain local (autonomy)
- ✅ Composition enables reuse without coupling (flexibility)

---

## 🏗️ 3-Tier Skill Architecture

### Tier 1: Core Skills (Global, Immutable)

**Location**: `capim-meta-ontology/.cursor/skills/`

**Characteristics**:
- Absolutely generic (no domain customization)
- Stable API (breaking changes are rare and communicated)
- Cross-cutting concerns (memory, sessions, debates)
- Used by ALL projects

**Current Skills**:
- `@session-start` - Session initialization
- `@session-end` - Archival and consolidation
- `@debate` - Structured decision-making
- `@curate-memory` - Memory governance

**Ownership**: Architecture team (global)

**Change Policy**: 
- Breaking changes require RFC and migration plan
- Backwards compatibility preferred
- Version bumps follow semantic versioning

---

### Tier 2: Shared Skills (Global, Extensible)

**Location**: `capim-meta-ontology/.cursor/skills/`

**Characteristics**:
- Generic base with extension points
- Can be composed with domain-specific logic
- Provide common patterns but allow customization

**Current Skills**:
- `@investigate-entity` - Entity profiling (extensible via references)
- `@validate-axioms` - Axiom validation (each domain has own AXIOMS.yaml)
- `@clinic-health-check` - Cross-domain diagnostic (uses domain-specific queries)

**Planned Skills**:
- `@eda-workflow` - EDA base pattern (domain-specific steps in references)
- `@detect-drift` - Drift detection framework (domain-specific thresholds)

**Ownership**: Shared (changes discussed cross-team)

**Change Policy**:
- New extension points can be added (backwards compatible)
- Breaking changes to base workflow require consensus
- Domain-specific extensions managed locally

---

### Tier 3: Domain Skills (Local, Autonomous)

**Location**: `<project>/.cursor/skills/`

**Characteristics**:
- Domain-specific workflows
- Independent evolution (doesn't affect other projects)
- Clear ownership (domain team)
- Can compose Tier 1 and 2 skills

**Examples** (by domain):

#### FINTECH (`bnpl-funil/.cursor/skills/`)
- `@analyze-conversion-funnel` - C1→C2 conversion analysis
- `@validate-fintech-axioms` - Risk-specific axiom validation
- `@bridge-temporal-events` - Time-window joins (C1-C2-Bureaus)
- `@detect-fintech-drift` - Credit score drift detection

#### SAAS (`ontologia-saas/.cursor/skills/`)
- `@validate-saas-contracts` - Budget/procedure contract validation
- `@formalize-saas-finding` - Progressive formalization workflow
- `@analyze-financial-ops` - Financial operations deep dive
- `@detect-saas-drift` - Clinic activity drift detection

#### CLIENT_VOICE (`client-voice-data/.cursor/skills/`)
- `@analyze-voc-sentiment` - Sentiment analysis workflows
- `@correlate-tickets-events` - Cross-domain ticket correlation
- `@classify-support-issues` - LLM-enhanced classification
- `@detect-voice-drift` - Support volume/category drift

**Ownership**: Domain team

**Change Policy**:
- Full autonomy (no cross-project coordination needed)
- Can break/refactor freely
- Can be promoted to Tier 2 if useful cross-domain

---

## 🔄 Composition Pattern

**Key principle**: Domain skills can **compose** Core and Shared skills.

### Example: `@formalize-saas-finding`

```yaml
---
name: Formalize SAAS Finding
description: Progressive formalization for SAAS domain EDA findings
version: 1.0
auto_invoke: ask_first
composes:
  - @debate (Tier 1)
  - @session-end (Tier 1)
---

## Workflow

1. Classify finding (SAAS-specific logic)
2. **Invoke @debate** to decide formalization strategy
3. Execute formalization (SAAS-specific logic)
4. **Update DECISIONS_IN_PROGRESS.md** (via memory governance)
```

**Benefits**:
- ✅ Reuses core decision-making (`@debate`)
- ✅ Follows memory governance (atomic updates)
- ✅ SAAS-specific logic remains in domain skill
- ✅ No duplication of debate/memory logic

---

## 📊 Decision Matrix: Which Tier?

| Criterion | Core (T1) | Shared (T2) | Domain (T3) |
|-----------|-----------|-------------|-------------|
| **Used in 3+ projects?** | ✅ All | ⚠️ 2-3 | ❌ 1 |
| **Domain-agnostic?** | ✅ Yes | ⚠️ With extensions | ❌ Domain-specific |
| **Breaking changes affect?** | 🔴 All projects | 🟡 Some projects | 🟢 None |
| **Ownership** | 👑 Architect | 🤝 Shared | 🎯 Domain team |
| **Evolution speed** | 🐢 Slow (stable) | 🐇 Medium | 🚀 Fast (agile) |
| **Customization** | ❌ No | ✅ Via extensions | ✅ Full |

---

## 🎯 Promotion Path (Tier 3 → Tier 2 → Tier 1)

Skills can be promoted when patterns emerge:

```
Domain Skill (T3)
  ↓
  Used in 2nd project → Generalize → Candidate for Shared (T2)
  ↓
  Identify generic core → Extract → Shared Skill (T2)
  ↓
  Ultra-stable, used everywhere → Promote → Core Skill (T1)
```

**Example progression**:

1. **Initial**: `ontologia-saas/.cursor/skills/@detect-saas-drift` (domain-specific)
2. **Reuse**: `bnpl-funil` needs drift detection → copy and adapt
3. **Generalize**: Extract common pattern → `@detect-drift` (Tier 2)
4. **Extend**: Each domain adds `references/<domain>_thresholds.md`
5. **Stabilize**: After 6 months, if unchanged → Consider Tier 1

---

## 🛡️ Governance Model

### Core Skills (T1)

**Change Process**:
1. Propose change via RFC (Request for Comments)
2. Impact analysis (all projects)
3. Migration plan if breaking
4. Consensus approval
5. Coordinated rollout

**Review Frequency**: Quarterly

### Shared Skills (T2)

**Change Process**:
1. Propose in shared channel
2. Impact analysis (affected projects only)
3. Backwards compatibility preferred
4. Approval from affected domain teams
5. Phased rollout

**Review Frequency**: Monthly

### Domain Skills (T3)

**Change Process**:
1. Domain team decides
2. No cross-project coordination needed
3. Can break/refactor freely
4. Document in domain's `.cursorrules`

**Review Frequency**: As needed (domain team's discretion)

---

## 📋 Skill Registry

**Purpose**: Centralized catalog of all skills across tiers

**Location**: `capim-meta-ontology/SKILL_REGISTRY.yaml`

**Structure**:
```yaml
core_skills:
  - name: session-start
    tier: 1
    owner: architecture
    status: stable
  - name: debate
    tier: 1
    owner: architecture
    status: stable

shared_skills:
  - name: investigate-entity
    tier: 2
    owner: shared
    status: stable
    extensions:
      - saas: references/saas_specifics.md
      - fintech: references/fintech_specifics.md

domain_skills:
  saas:
    - name: validate-saas-contracts
      tier: 3
      owner: saas-team
      status: active
    - name: formalize-saas-finding
      tier: 3
      owner: saas-team
      status: active
  
  fintech:
    - name: analyze-conversion-funnel
      tier: 3
      owner: fintech-team
      status: active
  
  client_voice:
    - name: analyze-voc-sentiment
      tier: 3
      owner: cx-team
      status: active
```

---

## 🔍 Discovery Mechanism

### How Agent Discovers Skills

**Tier 1 (Core)**:
- Listed in `capim-meta-ontology/.cursorrules` (always loaded)
- Metadata always in context

**Tier 2 (Shared)**:
- Listed in `capim-meta-ontology/.cursorrules` (always loaded)
- Body loaded on trigger
- References loaded on demand

**Tier 3 (Domain)**:
- Listed in `<project>/.cursorrules` (loaded when in project context)
- Metadata loaded when in project
- Body loaded on trigger

### Project `.cursorrules` Pattern

Each project should document local skills:

```markdown
## Domain-Specific Skills

This project has domain skills in `.cursor/skills/`:

- **@validate-saas-contracts**: Budget/procedure validation
- **@formalize-saas-finding**: Progressive formalization
- **@analyze-financial-ops**: Financial operations analysis

**Core skills** (from `capim-meta-ontology`):
- @session-start, @session-end, @debate, @curate-memory

**Shared skills** (from `capim-meta-ontology`):
- @investigate-entity, @validate-axioms, @clinic-health-check
```

---

## ⚖️ Trade-offs Summary

### Why NOT Fully Centralized?

❌ **Problems with full centralization**:
- Breaking changes affect all projects simultaneously
- Slow iteration (coordination overhead)
- One-size-fits-all doesn't work for domain-specific needs
- Loss of team autonomy and ownership

### Why NOT Fully Decentralized?

❌ **Problems with full decentralization**:
- Massive code duplication
- Drift between implementations
- Loss of cross-project learnings
- Maintenance multiplied

### Why 3-Tier Hybrid?

✅ **Benefits**:
- Core capabilities remain consistent
- Domain teams have autonomy
- Reuse without coupling
- Clear ownership model
- Promotion path for good patterns
- Composition enables flexibility

---

## 📚 Related Documents

| Document | Purpose |
|----------|---------|
| `SKILLS_PLAYBOOK.md` | How to create and maintain skills |
| `SKILL_REGISTRY.yaml` | Catalog of all skills (T1, T2, T3) |
| `.cursorrules` | Global rules and core skill listing |
| `<project>/.cursorrules` | Domain-specific rules and skill listing |
| `MEMORY_ARCHITECTURE_CONSTITUTION.md` | Memory patterns and governance |

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation (DONE)

- ✅ Core skills (T1) in capim-meta-ontology
- ✅ SKILLS_PLAYBOOK.md created
- ✅ Auto-invoke mechanism (`silent` | `ask_first` | `explicit_only`)
- ✅ Progressive disclosure (investigate-entity refactored)

### Phase 2: Domain Skills (CURRENT)

- [ ] Create `.cursor/skills/` in each domain project
- [ ] Migrate domain-specific workflows from `docs/how_to/` to domain skills
- [ ] Update each project's `.cursorrules` with skill listing
- [ ] Create SKILL_REGISTRY.yaml

### Phase 3: Shared Skills (NEXT)

- [ ] Migrate `EDA_PLAYBOOK.md` → `@eda-workflow` (T2)
- [ ] Migrate `DETECT_DRIFT.md` → `@detect-drift` (T2)
- [ ] Add extension points for domain-specific logic
- [ ] Create references for each domain

### Phase 4: Governance (ONGOING)

- [ ] Quarterly review of Core skills stability
- [ ] Monthly sync on Shared skills evolution
- [ ] Document promotion criteria (T3 → T2 → T1)
- [ ] Establish RFC process for breaking changes

---

## 🎓 Principles Summary

1. **Autonomy First**: Default to domain skills (T3) unless proven need for sharing
2. **Composition Over Inheritance**: Domain skills compose core/shared, don't extend
3. **Stable Core**: Tier 1 changes are rare and coordinated
4. **Extensible Shared**: Tier 2 provides patterns, domains provide specifics
5. **Fast Domain**: Tier 3 evolves independently, no coordination needed
6. **Promote When Proven**: Wait for 2+ uses before promoting to higher tier
7. **Ownership Clarity**: Each skill has clear owner (architect | shared | domain)

---

**Version**: 1.0  
**Last Updated**: 2026-02-04  
**Contributors**: Architecture team (based on debate and ecosystem analysis)  
**Status**: CANONICAL (all projects must follow)
