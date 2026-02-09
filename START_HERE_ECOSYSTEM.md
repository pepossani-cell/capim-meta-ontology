# CAPIM ECOSYSTEM META-ONTOLOGY

> **Status**: Active / Federation Layer  
> **Version**: 2.2 (Workspace Standardization)  
> **Last Updated**: 2026-02-03  
> **Role**: The "Micro-OS" for cross-domain reasoning in the Capim Ecosystem.

---

## 1. What is this?

This is the **Federation Layer** of the Capim Ecosystem. It does not contain code itself; rather, it acts as a **Router**, **Validator**, and **Orchestrator** between specialized domains.

**This workspace enables agents to:**
*   Answer cross-domain questions (e.g., *"Does using the SaaS Schedule feature improve BNPL conversion?"*)
*   Validate reasoning against logical constraints (Axioms)
*   Route queries to the correct domain without hallucinating capabilities
*   Synthesize multi-domain data into unified insights

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CAPIM META-ONTOLOGY                             │
│                    (This Workspace)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐    ┌──────────────────┐                       │
│  │  ontology/      │    │  federation/    │                       │
│  │  ┌────────────┐  │    │  ┌────────────┐  │                       │
│  │  │ TAXONOMY   │  │    │  │ DOMAIN_    │  │                       │
│  │  │ .yaml      │  │    │  │ REGISTRY   │  │                       │
│  │  ├────────────┤  │    │  ├────────────┤  │                       │
│  │  │ AXIOMS     │  │    │  │ CROSS_     │  │                       │
│  │  │ .yaml      │  │    │  │ DOMAIN_GLUE│  │                       │
│  │  ├────────────┤  │    │  ├────────────┤  │                       │
│  │  │ INFERENCE_ │  │    │  │ CAPABILITY_│  │                       │
│  │  │ RULES.yaml │  │    │  │ MATRIX.yaml│  │                       │
│  │  └────────────┘  │    │  └────────────┘  │                       │
│  └──────────────────┘    └──────────────────┘                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  MEMORY_ARCHITECTURE_CONSTITUTION.md                         │   │
│  │  (The "Soul" - Governing Principles for All Agents)          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
┌────────────────────────────┐  ┌────────────────────────────┐
│       FINTECH DOMAIN       │  │        SAAS DOMAIN         │
│    (bnpl-funil/project_    │  │    (ontologia-saas/_domain)  │
│         refactor)          │  │                            │
│                            │  │  • Schedules/Appointments  │
│  • Credit Simulations      │  │  • Budgets                 │
│  • Risk Analysis           │  │  • Clinic Operations       │
│  • Bureau Data             │  │  • Churn Risk              │
│  • Conversion Funnel       │  │                            │
└────────────────────────────┘  └────────────────────────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                 ┌────────────────────────────┐
                 │     CLIENT_VOICE DOMAIN    │
                 │        (client-voice/)     │
                 │                            │
                 │  • Support Tickets         │
                 │  • Sentiment Analysis      │
                 │  • Feedback Themes         │
                 │  [STATUS: DRAFT]           │
                 └────────────────────────────┘
```

---

## 3. The Domains

| Domain ID | Name | Focus | Entry Point |
| :--- | :--- | :--- | :--- |
| **FINTECH** | BNPL Risk & Credit | Simulations, Risk, Bureaus, Conversion | `bnpl-funil/_domain/START_HERE.md` |
| **SAAS** | Clinic Operations | Schedules, Budgets, Churn, Activity | `ontologia-saas/_domain/START_HERE.md` |
| **CLIENT_VOICE** | Customer Voice (Active) | Tickets, Sentiment, Feedback | `client-voice/START_HERE.md` |

> **Machine-readable registry**: [`_federation/DOMAIN_REGISTRY.yaml`](_federation/DOMAIN_REGISTRY.yaml)

---

## 4. Key Files (For Agents)

### 4.1. Governance (The "Soul")
| File | Purpose |
| :--- | :--- |
| [`MEMORY_ARCHITECTURE_CONSTITUTION.md`](MEMORY_ARCHITECTURE_CONSTITUTION.md) | The master document. All agent behavior, memory patterns, and ontology rules are defined here. **Read this FIRST.** |

### 4.2. Ontology (The "Knowledge")
| File | Purpose |
| :--- | :--- |
| [`_ontology/TAXONOMY.yaml`](_ontology/TAXONOMY.yaml) | Hierarchical classification of all entities (Classes, Subclasses, Instances). Enables IS_A reasoning. |
| [`_ontology/AXIOMS.yaml`](_ontology/AXIOMS.yaml) | Logical constraints that MUST hold. Use to validate reasoning. |
| [`_ontology/INFERENCE_RULES.yaml`](_ontology/INFERENCE_RULES.yaml) | Predefined reasoning patterns (playbooks) for common query types. |
| [`_ontology/REVIEW_QUEUE.yaml`](_ontology/REVIEW_QUEUE.yaml) | Pending ontology changes awaiting human review. |

### 4.3. Federation (The "Router")
| File | Purpose |
| :--- | :--- |
| [`_federation/DOMAIN_REGISTRY.yaml`](_federation/DOMAIN_REGISTRY.yaml) | Maps domain IDs to physical file paths. |
| [`_federation/CROSS_DOMAIN_GLUE.yaml`](_federation/CROSS_DOMAIN_GLUE.yaml) | Defines join rules between domains (e.g., how to link SAAS.Patient to FINTECH.Patient via CPF). |
| [`_federation/CAPABILITY_MATRIX.yaml`](_federation/CAPABILITY_MATRIX.yaml) | Specifies what each domain can answer. Used for intelligent routing. |

### 4.4. Cursor Integration (The "Automation") 🆕

**Rules** (Behavioral protocols applied automatically):
| File | Purpose | When Applied |
| :--- | :--- | :--- |
| [`.cursor/rules/memory_governance.mdc`](.cursor/rules/memory_governance.mdc) | Atomic decision tracking protocol | Editing `_memory/**/*.md` |
| [`.cursor/rules/snowflake_data.mdc`](.cursor/rules/snowflake_data.mdc) | Snowflake-first protocol, Zero Assumptions | Working with `**/*.sql`, `**/*.py` |
| [`.cursor/rules/ontology_reasoning.mdc`](.cursor/rules/ontology_reasoning.mdc) | Cross-domain reasoning, axiom validation | Ontology queries, cross-domain work |

**Skills** (Invocable workflows):
| Skill | Purpose | Invocation |
| :--- | :--- | :--- |
| `@session-start` | Load memory context and domain docs | Start of work session |
| `@session-end` | Archive decisions, create session notes | End of work session |
| `@debate` | Structured decision-making | Complex decisions, auto-detect |
| `@clinic-health-check` | Multi-domain clinic diagnostic | Clinic health investigations |
| `@investigate-entity` | Profile Snowflake tables | New entity documentation |
| `@validate-axioms` | Validate data integrity against ontology | Governance reviews, pre-merge |
| `@curate-memory` | Housekeeping for memory files | Memory maintenance |

**See**: `.cursor/skills/*/SKILL.md` for detailed documentation

**⚠️ Note**: `.agent/` folder is **deprecated**. Use `.cursor/` instead. See [`docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md`](docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md) for migration guide.

---

## 5. How to Navigate (For Agents)

### Quick Start: Session Management 🆕

**Starting a work session**:
```
1. Invoke: @session-start
2. Select domain (interactive)
3. Begin work with full context loaded
```

**During work**:
- Skills auto-detect when needed (e.g., @debate for complex decisions)
- Rules enforce protocols automatically (e.g., atomic decision tracking)
- Memory updated immediately (no batch at end)

**Ending session**:
```
1. Invoke: @session-end
2. Review items to archive
3. Confirm archival
4. Session notes created automatically
```

### Detailed Navigation (For Complex Queries)

**Step 1: Load the Constitution**
```yaml
reference: MEMORY_ARCHITECTURE_CONSTITUTION.md
sections_to_prioritize:
  - META_INSTRUCTIONS
  - DIRECTIVE:ONTOLOGY_FORMALIZATION
  - DIRECTIVE:CAPABILITY_ROUTING
  - DIRECTIVE:RESPONSE_CONTRACT
```

**Step 2: Read the Capability Matrix**
```yaml
reference: _federation/CAPABILITY_MATRIX.yaml
purpose: "Understand what each domain can answer. Find the right capability for the query."
```

**Step 3: Load Relevant Taxonomy/Axioms**
```yaml
reference: _ontology/TAXONOMY.yaml, _ontology/AXIOMS.yaml
purpose: "Understand entity hierarchies. Validate reasoning against constraints."
note: "Use @validate-axioms skill for automated validation"
```

**Step 4: Apply Inference Rules (If Applicable)**
```yaml
reference: _ontology/INFERENCE_RULES.yaml
purpose: "For complex queries, follow predefined reasoning patterns."
example: "RULE-CROSS-001 for clinic health diagnostics (@clinic-health-check skill)"
```

**Step 5: Deep Dive into Domain**
```yaml
action: "Navigate to the domain's START_HERE file for entity-specific documentation."
automation: "@session-start skill handles this based on user selection"
```

---

## 6. Critical Rules (Do Not Violate)

1.  **Never assume IDs match** across domains, **except** `clinic_id` and `CPF`.
2.  **Time is fuzzy**: Events propagate asynchronously. Use Time Windows when linking cross-domain events.
3.  **Validate against Axioms**: If your response violates a HARD axiom, revise before returning.
4.  **Cite Sources**: Every factual claim must reference a SOURCE (table, document, memory).
5.  **Abstain if uncertain**: Confidence < 0.4 → Return "I don't know" with explanation.

---

## 7. Example Query Flow

**User asks**: *"What are the problems with clinic 12345?"*

**Agent workflow**:
1.  **Parse**: Extract `clinic_id = 12345`, intent = "problems/issues".
2.  **Route**: Check `CAPABILITY_MATRIX.yaml` → Multi-domain query → Trigger `RULE-CROSS-001`.
3.  **Execute**:
    *   Query SAAS.SupportTickets(12345, last_90_days)
    *   Query SAAS.ScheduleVolume(12345, last_90_days)
    *   Query FINTECH.RejectionRate(12345, last_90_days)
4.  **Synthesize**: Correlate ticket dates with activity drops per `INFERENCE_RULES.yaml`.
5.  **Validate**: Check response against `AXIOMS.yaml`.
6.  **Respond**: Follow `RESPONSE_CONTRACT` schema (answer, sources, confidence, caveats).

---

## 8. Version History

| Version | Date | Changes |
| :--- | :--- | :--- |
| 2.2 | 2026-02-03 | **Workspace Standardization**: Implemented hierarchical cursorrules (global + project-specific). Separated client-voice into client-voice-data (ontology) + client-voice-app (Streamlit). Centralized VISUALIZATION_STANDARDS.md. Standardized rules to English, cursorrules to Portuguese. Created WORKSPACE_STRUCTURE.md. |
| 2.1 | 2026-02-03 | **Cursor Integration**: Migrated all workflows/skills from Antigravity to Cursor. Added Rules (memory_governance, snowflake_data, ontology_reasoning) and Skills (@session-start, @session-end, @debate, specialized skills). Deprecated `.agent/` folder. |
| 2.0 | 2026-01-31 | Added executable ontology layer (TAXONOMY, AXIOMS, INFERENCE_RULES, CAPABILITY_MATRIX). Upgraded Constitution to v3.0. |
| 1.0 | 2026-01-30 | Initial federation layer with DOMAIN_REGISTRY and CROSS_DOMAIN_GLUE. |

---

## 9. Workspace Standardization (2026-02-03)

**Complete workspace restructuring** implemented to eliminate duplication and improve modularity.

### Changes Implemented

**Cursorrules Hierarchy**:
- ✅ Global cursorrules created with shared protocols
- ✅ Project cursorrules refactored to extend global
- ✅ ~90+ lines of duplication eliminated

**Client-Voice Separation**:
- ✅ `client-voice-data/` created (data ontology)
- ✅ `client-voice/` becomes pure application (Streamlit)
- ✅ Aligned with MEMORY_ARCHITECTURE_CONSTITUTION separation of concerns

**Centralized Documentation**:
- ✅ `docs/VISUALIZATION_STANDARDS.md` (eliminates 30+ line duplication)
- ✅ `docs/WORKSPACE_STRUCTURE.md` (complete organization guide)

**Language Standardization**:
- ✅ Rules (`.cursor/rules/*.mdc`): English
- ✅ Cursorrules (`.cursorrules`): Portuguese (business context)

### Hierarchy

```
Global (.cursorrules)
├── extends → bnpl-funil/.cursorrules (FINTECH)
├── extends → ontologia-saas/.cursorrules (SAAS)
├── extends → client-voice-data/.cursorrules (CLIENT_VOICE data)
└── extends → client-voice/.cursorrules (CLIENT_VOICE app)
```

**Full details**: [`docs/WORKSPACE_STRUCTURE.md`](docs/WORKSPACE_STRUCTURE.md)

---

## 10. Documentation Index

| Guide | Purpose |
| :--- | :--- |
| [`docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md`](docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md) | Antigravity → Cursor migration (workflows, skills, rules) |
| [`docs/WORKSPACE_STRUCTURE.md`](docs/WORKSPACE_STRUCTURE.md) | Complete workspace organization and cursorrules hierarchy |
| [`docs/VISUALIZATION_STANDARDS.md`](docs/VISUALIZATION_STANDARDS.md) | Shared Seaborn/Matplotlib guidelines |
| [`.cursor/INTEGRATION_TEST.md`](.cursor/INTEGRATION_TEST.md) | Validation tests for standardization |
| [`WORKSPACE_STANDARDIZATION_SUMMARY.md`](WORKSPACE_STANDARDIZATION_SUMMARY.md) | Implementation summary (this migration) |
