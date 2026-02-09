# Domain Skills Analysis — Capim Ecosystem

> **Purpose**: Consolidated analysis of domain-specific skills across all projects  
> **Date**: 2026-02-04  
> **Status**: PROPOSAL (pending implementation)

---

## 📊 Executive Summary

Analysis of 4 domain projects to identify Tier 3 skills (domain-specific workflows):

| Domain | Project | Current How-To Docs | Proposed Domain Skills | Scripts to Bundle |
|--------|---------|---------------------|----------------------|-------------------|
| **SAAS** | `ontologia-saas` | 8 docs | 4 skills | 3 scripts |
| **FINTECH** | `bnpl-funil` | 0 docs | 5 skills | 5 scripts |
| **CLIENT_VOICE** | `client-voice-data` | 0 docs | 3 skills | 2 scripts |
| **META** | `capim-meta-ontology` | - | 4 core + 3 shared | 2 scripts |

**Total**: 15 domain skills proposed + 7 skills already implemented

---

## 1. SAAS Domain (`ontologia-saas`)

### Current State

**Existing docs**:
- `docs/how_to/` (8 files)
  - EDA_PLAYBOOK.md ⚠️ → Promote to Tier 2 (generic)
  - DETECT_DRIFT.md ⚠️ → Promote to Tier 2 (generic)
  - CONTRACTS_AND_DECISIONS.md ✅ → Domain skill
  - PROGRESSIVE_FORMALIZATION.md ✅ → Domain skill
  - WORKING_WITH_QUERIES.md ⚠️ → Rule (enforcement, not workflow)
  - POPULATION_STATUS.md ❌ → Reference doc (classification guide)
  - NOTION_PRIVATE_IMAGE_UPLOAD.md ❌ → Reference doc (tool-specific)

**Existing scripts**:
- `_utils/eda_*.py` (4 scripts for EDA automation)
- `src/cli/materialize_views_financial_ops.py`
- `scripts/plot_utils.py`

### Proposed Domain Skills

#### 1. `@validate-saas-contracts`

**Purpose**: Validate budget/procedure contracts for semantic consistency

**Based on**: `docs/how_to/CONTRACTS_AND_DECISIONS.md`

**Workflow**:
1. Select contract type (budget, procedure, financial_op)
2. Validate grain and keys
3. Check semantic constraints (e.g., finished budget must have procedures)
4. Detect drift or violations
5. Document findings

**Bundled resources**:
- `scripts/validate_contracts.py` (validation logic)
- `references/CONTRACT_SCHEMAS.md` (expected schemas)
- `references/SEMANTIC_RULES.md` (business rules)

**Auto-invoke**: `ask_first` (validation can be token-intensive)

---

#### 2. `@formalize-saas-finding`

**Purpose**: Progressive formalization of EDA findings specific to SAAS

**Based on**: `docs/how_to/PROGRESSIVE_FORMALIZATION.md`

**Workflow**:
1. Classify finding type (semantic, drift, linkage, contract violation)
2. **Compose @debate** to decide formalization strategy:
   - A. Promote to audit query (`queries/audit/`)
   - B. Document in reference (`docs/reference/`)
   - C. Create ADR if architectural
3. Execute formalization (SAAS-specific paths)
4. Update ENTITY_INDEX.yaml or DECISIONS_IN_PROGRESS.md

**Bundled resources**:
- `references/FORMALIZATION_CRITERIA.md` (decision tree)
- `references/SAAS_AUDIT_PATTERNS.md` (common audit queries)

**Auto-invoke**: `ask_first` (involves write operations)

**Composes**: `@debate` (Tier 1)

---

#### 3. `@analyze-financial-ops`

**Purpose**: Deep dive analysis of financial operations (budgets, procedures, transactions)

**Based on**: Domain expertise + `docs/reference/FINANCIAL_OPS_CORE.md`

**Workflow**:
1. Select analysis type (volume, distribution, anomaly, drift)
2. Query financial_ops data (Snowflake-first)
3. Generate visualizations (dual panels: volume + share)
4. Detect anomalies or drift
5. Document findings

**Bundled resources**:
- `scripts/analyze_financial_ops.py` (analysis logic)
- `references/FINANCIAL_OPS_METRICS.md` (standard metrics)
- `assets/financial_ops_template.py` (visualization templates)

**Auto-invoke**: `ask_first` (can be token-intensive)

---

#### 4. `@detect-saas-drift`

**Purpose**: Detect drift in SAAS entities (clinic activity, budgets, procedures)

**Based on**: `docs/how_to/DETECT_DRIFT.md` (SAAS-specific thresholds)

**Workflow**:
1. Select entity and drift type (volume, domain, semantic, relationship)
2. Run profiling queries (temporal analysis)
3. Compare against expected patterns
4. Flag drift if threshold exceeded
5. Document in audit query or reference doc

**Bundled resources**:
- `scripts/detect_drift.py` (profiling logic)
- `references/SAAS_DRIFT_THRESHOLDS.yaml` (expected ranges)
- `references/SAAS_DRIFT_PATTERNS.md` (known patterns)

**Auto-invoke**: `silent` (read-only profiling)

**Extends**: Future `@detect-drift` (Tier 2)

---

## 2. FINTECH Domain (`bnpl-funil`)

### Current State

**Existing docs**:
- `docs/` (18 reference docs, no how_to folder)
- `docs/enrichment/*_CORE.md` (enrichment logic documentation)
- `docs/adr/*.md` (architectural decisions)

**Existing scripts**:
- `scripts/studies/autopsia_bnpl/*.py` (15 analysis scripts)
- `scripts/studies/financial_ops/*.py` (4 analysis scripts)
- `src/cli/materialize_*.py` (enrichment materializers)
- `outputs/execute_sql_view.py` (SQL execution)

### Proposed Domain Skills

#### 1. `@analyze-conversion-funnel`

**Purpose**: Analyze C1→C2 conversion funnel with BNPL-specific logic

**Workflow**:
1. Define period and cohort
2. Query C1 (simulations) and C2 (requests) data
3. Apply bridge logic (time windows, entity matching)
4. Calculate conversion rates and velocity
5. Segment by clinic, risk profile, bureau scores
6. Generate visualizations (funnel + Lorenz curves)
7. Document findings

**Bundled resources**:
- `scripts/analyze_conversion.py` (funnel logic)
- `references/BRIDGE_LOGIC.md` (C1-C2-Bureaus linkage)
- `references/CONVERSION_METRICS.md` (standard KPIs)
- `assets/funnel_viz_template.py`

**Auto-invoke**: `ask_first` (cross-entity, token-intensive)

---

#### 2. `@validate-fintech-axioms`

**Purpose**: Validate FINTECH-specific axioms (risk rules, bureau constraints)

**Workflow**:
1. Load `_domain/_docs/AXIOMS_FINTECH.yaml`
2. Execute validation queries for each axiom
3. Flag violations (HARD axioms = errors, SOFT = warnings)
4. Generate validation report
5. Update axiom health metrics

**Bundled resources**:
- `scripts/validate_axioms.py` (validation engine)
- `references/FINTECH_AXIOMS.yaml` (risk-specific axioms)

**Auto-invoke**: `silent` (read-only validation)

**Extends**: `@validate-axioms` (Tier 2)

---

#### 3. `@bridge-temporal-events`

**Purpose**: Execute time-window joins for C1-C2-Bureaus-Crivo (FINTECH-specific)

**Workflow**:
1. Select entities to bridge (C1, C2, credit_checks, crivo_checks)
2. Apply time-window heuristics (e.g., C2 within 30 days of C1)
3. Validate cardinality (1:1, 1:many, many:many)
4. Flag orphans or ambiguous matches
5. Return bridged dataset

**Bundled resources**:
- `scripts/bridge_events.py` (bridge logic)
- `references/TIME_WINDOWS.yaml` (canonical windows)
- `references/BRIDGE_PATTERNS.md` (known patterns)

**Auto-invoke**: `ask_first` (complex logic, can be slow)

**Reference**: `_domain/_docs/reference/BRIDGE_C1_C2_BUREAUS_CRIVO_SEMANTIC.md`

---

#### 4. `@detect-fintech-drift`

**Purpose**: Detect drift in credit scores, rejection rates, bureau availability

**Workflow**:
1. Select entity (credit_simulations, credit_checks, requests)
2. Run temporal profiling (monthly aggregates)
3. Detect drift in:
   - Score distributions (should be stable)
   - Rejection rates (sudden changes flag policy shifts)
   - Bureau availability (Serasa outages)
4. Flag drift if threshold exceeded
5. Document in audit or ADR

**Bundled resources**:
- `scripts/detect_drift.py`
- `references/FINTECH_DRIFT_THRESHOLDS.yaml`
- `references/SCORE_NORMALIZATION.md` (ADR-0004)

**Auto-invoke**: `silent` (read-only)

**Extends**: Future `@detect-drift` (Tier 2)

---

#### 5. `@materialize-enriched-entity`

**Purpose**: Execute materialization of enriched views (C1, C2, borrower profiles)

**Workflow**:
1. Select entity to materialize (C1_ENRICHED_BORROWER, C2_ENRICHED_REQUESTS)
2. Execute enrichment logic (joins with bureaus, clinics, patients)
3. Validate row counts and grain
4. Create or replace table in Snowflake
5. Document refresh timestamp

**Bundled resources**:
- `scripts/materialize.py` (CLI wrapper)
- Reuses existing: `src/cli/materialize_*.py`

**Auto-invoke**: `ask_first` (write operations, can be slow)

---

## 3. CLIENT_VOICE Domain (`client-voice-data`)

### Current State

**Existing docs**:
- Minimal (no how_to folder)
- Entity docs in `_domain/_docs/reference/` (7 files)

**Existing scripts**:
- `scripts/sync_zendesk_enhanced_view.py` (ETL from n8n)
- `scripts/plot_utils.py` (visualization utilities)

### Proposed Domain Skills

#### 1. `@analyze-voc-sentiment`

**Purpose**: Analyze Voice of Customer sentiment trends and patterns

**Workflow**:
1. Select analysis type (sentiment, category, volume, clinic)
2. Query Zendesk tickets (TICKET_ANALYSIS_V3)
3. Aggregate by period and persona (B2B vs B2C)
4. Detect sentiment trends (improving, declining, stable)
5. Correlate with events (e.g., product launches, incidents)
6. Generate visualizations (time series + heatmaps)

**Bundled resources**:
- `scripts/analyze_sentiment.py`
- `references/VOC_METRICS.md` (NPS, CSAT, sentiment scores)
- `references/CATEGORY_TAXONOMY.md` (LLM classification categories)

**Auto-invoke**: `ask_first` (cross-entity queries)

---

#### 2. `@correlate-tickets-events`

**Purpose**: Correlate support tickets with SAAS/FINTECH events (cross-domain)

**Workflow**:
1. Load tickets for clinic and period
2. Query SAAS domain for clinic events (churn signals, activity drops)
3. Query FINTECH domain for rejection events
4. Apply time-window correlation (7-14 days)
5. Flag likely causal relationships (ticket → event or event → ticket)
6. Generate correlation report

**Bundled resources**:
- `scripts/correlate_events.py`
- `references/CORRELATION_HEURISTICS.md` (time windows, patterns)

**Auto-invoke**: `ask_first` (cross-domain, token-intensive)

**Composes**: `@clinic-health-check` (Tier 2)

---

#### 3. `@classify-support-issues`

**Purpose**: LLM-enhanced classification of support tickets (manual/ad-hoc)

**Workflow**:
1. Select unclassified or misclassified tickets
2. Extract ticket content (subject + description)
3. Invoke LLM for classification (category, subcategory, sentiment)
4. Validate classification quality (confidence scores)
5. Update Snowflake table (if approved)

**Bundled resources**:
- `scripts/classify_tickets.py`
- `references/LLM_PROMPTS.md` (classification prompts)
- `references/CATEGORY_DEFINITIONS.md` (taxonomy)

**Auto-invoke**: `ask_first` (LLM invocation, write operations)

---

## 4. Shared Skills (Tier 2) - Planned Migrations

### From `ontologia-saas/docs/how_to/`

#### 1. `@eda-workflow` (Tier 2)

**Migrate from**: `EDA_PLAYBOOK.md`

**Why Tier 2**: EDA pattern is generic (SAAS, FINTECH, CLIENT_VOICE all do EDAs)

**Extension points**:
- `references/eda_saas.md` (SAAS-specific: financial_ops patterns)
- `references/eda_fintech.md` (FINTECH-specific: risk cohorts)
- `references/eda_client_voice.md` (CLIENT_VOICE-specific: sentiment analysis)

**Workflow** (generic):
1. Define universe (population) and anchor period
2. Define provisional axes and classes
3. Distinguish historical vs snapshot signals
4. Execute in Snowflake (Snowflake-first)
5. Handle ambiguity (invoke `@debate` if needed)
6. Formalize finding (invoke domain-specific formalization skill)

---

#### 2. `@detect-drift` (Tier 2)

**Migrate from**: `DETECT_DRIFT.md`

**Why Tier 2**: Drift detection is generic (all domains have temporal entities)

**Extension points**:
- `references/drift_saas_thresholds.yaml` (clinic activity patterns)
- `references/drift_fintech_thresholds.yaml` (score distributions)
- `references/drift_client_voice_thresholds.yaml` (support volume patterns)

**Workflow** (generic):
1. Select entity and drift type (volume, domain, semantic, relationship)
2. Run temporal profiling (monthly/weekly aggregates)
3. Compare against expected patterns (domain-specific thresholds)
4. Flag drift if threshold exceeded
5. Document finding (audit query or reference doc)

---

## 5. Implementation Priority

### Phase 1: High-Value, Low-Complexity

**Priority 1** (implement first):
1. `@validate-saas-contracts` (SAAS) - High business value, clear workflow
2. `@analyze-conversion-funnel` (FINTECH) - High business value, existing scripts
3. `@analyze-voc-sentiment` (CLIENT_VOICE) - High business value, simple

**Effort**: 2-3 days per skill

---

### Phase 2: Medium Complexity

**Priority 2** (implement after Phase 1):
4. `@formalize-saas-finding` (SAAS) - Medium value, composes `@debate`
5. `@bridge-temporal-events` (FINTECH) - High technical value, complex logic
6. `@correlate-tickets-events` (CLIENT_VOICE) - Medium value, cross-domain

**Effort**: 3-5 days per skill

---

### Phase 3: Shared Skills (Tier 2)

**Priority 3** (after domain skills stabilize):
7. `@eda-workflow` (Tier 2) - Migrate from EDA_PLAYBOOK.md
8. `@detect-drift` (Tier 2) - Migrate from DETECT_DRIFT.md

**Effort**: 5-7 days per skill (requires generalization + extension points)

---

### Phase 4: Specialized/Lower Priority

**Priority 4** (as needed):
9. `@analyze-financial-ops` (SAAS) - Specialized, overlaps with ad-hoc analysis
10. `@materialize-enriched-entity` (FINTECH) - Automation of existing CLI
11. `@classify-support-issues` (CLIENT_VOICE) - Manual process, low frequency

**Effort**: 2-4 days per skill

---

## 6. Migration Path: How-To → Skill

### Example: `ontologia-saas/docs/how_to/CONTRACTS_AND_DECISIONS.md`

**Step 1: Create structure**
```bash
mkdir -p ontologia-saas/.cursor/skills/validate-saas-contracts
mkdir -p ontologia-saas/.cursor/skills/validate-saas-contracts/scripts
mkdir -p ontologia-saas/.cursor/skills/validate-saas-contracts/references
```

**Step 2: Create SKILL.md**
```yaml
---
name: Validate SAAS Contracts
description: Validate budget/procedure contracts for semantic consistency. Use when...
version: 1.0
auto_invoke: ask_first
---

# Validate SAAS Contracts Skill

[Workflow from CONTRACTS_AND_DECISIONS.md]
```

**Step 3: Bundle scripts** (if applicable)
```bash
cp scripts/validate_contracts.py .cursor/skills/validate-saas-contracts/scripts/
```

**Step 4: Create references** (split detailed content)
```bash
# Extract schemas, rules, examples to references/
```

**Step 5: Update `.cursorrules`**
```markdown
## Domain-Specific Skills

- **@validate-saas-contracts**: Budget/procedure validation
```

**Step 6: Archive or deprecate original how_to doc**
```bash
# Add deprecation notice to CONTRACTS_AND_DECISIONS.md
# Point to skill: "Migrated to `.cursor/skills/validate-saas-contracts/`"
```

---

## 7. Success Metrics

### Adoption Metrics

- **Skill invocations**: Track usage frequency per skill
- **Auto-invoke success rate**: % of times auto-invoke was appropriate
- **Composition rate**: % of domain skills that compose Tier 1/2 skills

### Quality Metrics

- **Error rate**: % of skill executions that fail or produce incorrect results
- **Refactor frequency**: How often domain skills need updates (agility indicator)
- **Promotion rate**: % of domain skills promoted to Tier 2 (pattern emergence)

### Efficiency Metrics

- **Time saved**: Estimated time saved vs manual execution
- **Token efficiency**: Tokens consumed per skill execution
- **Code duplication**: Reduction in duplicated code cross-project

---

## 8. Risks & Mitigations

### Risk 1: Over-fragmentation

**Risk**: Too many small skills, hard to discover

**Mitigation**: 
- Maintain SKILL_REGISTRY.yaml (centralized catalog)
- Enforce minimum skill size (< 100 lines → merge into larger skill)
- Use `references/` for detailed content, keep SKILL.md concise

### Risk 2: Drift between domains

**Risk**: Similar skills in different domains diverge (e.g., drift detection)

**Mitigation**:
- Quarterly cross-domain sync meetings
- Promotion path (T3 → T2) when patterns emerge
- Document shared patterns in Tier 2 early

### Risk 3: Stale skills

**Risk**: Domain skills become outdated as domain evolves

**Mitigation**:
- Owner accountability (domain team responsible)
- Version bumps enforce review
- Deprecation path (mark deprecated, archive, delete after grace period)

---

## 9. Next Steps

**Immediate**:
1. Review this analysis with domain teams
2. Prioritize Phase 1 skills (3 high-value skills)
3. Create SKILL_REGISTRY.yaml
4. Set up `.cursor/skills/` folders in each domain project

**Short-term** (next 2 weeks):
5. Implement Phase 1 skills (one per domain)
6. Update `.cursorrules` in each project
7. Test skill discovery and invocation

**Medium-term** (next 1-2 months):
8. Implement Phase 2 and Phase 3 skills
9. Extract shared patterns → Tier 2 skills
10. Document learnings in ARCHITECTURE_PRINCIPLES.md

---

**Version**: 1.0  
**Last Updated**: 2026-02-04  
**Contributors**: Architecture team (based on project analysis)  
**Status**: PROPOSAL (pending team review and approval)
