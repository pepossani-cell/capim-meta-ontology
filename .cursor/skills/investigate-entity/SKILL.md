---
name: Investigate Entity
description: Automatically investigate and profile a Snowflake table or view following the Zero Assumptions protocol. Use when (1) documenting a new entity in the ontology, (2) validating quality of a source table (nulls, duplicates, domains), (3) understanding temporal drift and population status, (4) identifying PII or sensitive columns before documentation, (5) investigating unknown schema before creating views/queries, (6) user says "@investigate-entity <TABLE>" or "investigate <TABLE>". Generates BOTH semantic and agentic documentation per Dual Documentation Protocol. Involves debate with user and write operations.
version: 2.1
auto_invoke: ask_first
migrated_from: .agent/skills/investigate-entity/SKILL.md
last_updated: 2026-02-05
---

# Investigate Entity Skill

Automatiza a descoberta e profiling inicial de qualquer tabela ou view no Snowflake, seguindo o protocolo **Zero Assumptions**.

**🎯 PROTOCOLO CRÍTICO: ZERO ASSUMPTIONS**

**Nunca documente uma entidade baseado em suposições**. Se este tool não puder rodar, PARE e peça dados ao usuário.

**Referência**: Esta skill implementa o protocolo definido em `ontologia-cf/docs/how_to/INVESTIGATE_ENTITY.md` (quando aplicável) e integra com a Rule `snowflake_protocol.mdc`.

## Quando Usar

Invoque esta skill quando:
- Documentar uma nova entidade na ontologia
- Validar qualidade de uma tabela source (nulls, duplicates, domains)
- Entender temporal drift e status populacional de uma entidade
- Identificar PII ou colunas sensíveis antes de documentação
- Investigar schema desconhecido antes de criar views ou queries

**Invocação**: `@investigate-entity <SCHEMA.TABLE_NAME>` ou menção natural

## Execution Process (Mandatory)

**⚠️ CRITICAL**: This skill MUST generate BOTH documents (Semantic + Agentic) per the Dual Documentation Protocol.

**Reference**: `.cursor/rules/entity_documentation.mdc` (enforces naming and structure)

### Step 1: Investigate (Technical Profiling)

Run profiling script or manual queries to gather **technical facts**:
- Schema (columns, types, nullable)
- Volume (row count, date range)
- Nullability (% null per column)
- Categorical domains (top values, distributions)
- Temporal drift (monthly volume)
- Grain validation (duplicates check)

**Output**: Technical facts for AGENTIC doc.

### Step 2: Debate (Semantic Extraction)

Present technical findings to user, then **extract business context** via debate.

**Comprehensive debate questions** available in: [DEBATE_QUESTIONS.md](references/DEBATE_QUESTIONS.md)

**Key areas to cover**:
- **Business Definition**: What is this? Why does it exist?
- **Use Cases**: Who uses this and for what?
- **Semantic Nuances**: Why high nulls? Different universes (B2B vs B2C)?
- **Limitations & Caveats**: What can this NOT answer? Common mistakes?
- **Privacy & Sensitivity**: PII classification and handling
- **Technical Validation**: Grain, relationships, tier classification

**Output**: Business context and strategic insights for SEMANTIC doc.

### Step 3: Document (Dual Output — SEPARATE LOCATIONS)

Generate BOTH files in correct **LOCATIONS**:

**⚠️ CRITICAL PATH RULES**:
```
docs/reference/<ENTITY>.md                    ← Data dictionary (schema)
_domain/_docs/reference/<ENTITY>_SEMANTIC.md  ← Semantic (business context)
```

**3A. Generate DATA DICTIONARY FIRST** (`docs/reference/<ENTITY>.md`):
- Use profiling results directly (data-driven)
- Structure: Schema → Profile → Relationships → Queries
- Tone: Precise, technical, query-ready
- **DO NOT include**: Business narrative, "why" explanations

**3B. Generate SEMANTIC doc SECOND** (`_domain/_docs/reference/<ENTITY>_SEMANTIC.md`):
- Use debate insights (context-driven)
- Structure: Definition → Relationships → Questions → Caveats
- Tone: Narrative, explanatory, context-rich
- **DO NOT include**: Profiling stats, technical schemas

### Step 4: Link Files (Cross-Folder References)

Add cross-references in headers with **correct relative paths**:

```markdown
# In _domain/_docs/reference/<ENTITY>_SEMANTIC.md:
> **Related Reference**: [<ENTITY>.md](../../../docs/reference/<ENTITY>.md)

# In docs/reference/<ENTITY>.md:
> **Related Reference**: [<ENTITY>_SEMANTIC.md](../../_domain/_docs/reference/<ENTITY>_SEMANTIC.md)
```

### Step 5: Update Index

Add/update entity in `ENTITY_INDEX.yaml` with documentation references (note different base paths):
```yaml
documentation:
  semantic: "_docs/reference/<ENTITY>_SEMANTIC.md"     # relative to _domain/
  agentic: "../docs/reference/<ENTITY>.md"             # relative to _domain/
```

### Step 6: Cross-Attribute Correlation Analysis (NEW)

**Purpose**: Automatically detect hidden dependencies between attributes that would otherwise require manual investigation.

**When to apply**: 
- Tables with > 5 boolean/categorical columns
- Tables with coverage/fill rate variations
- Entities with lifecycle states

**Process**:

1. **Identify candidate pairs**: All boolean columns + categorical columns with cardinality < 10

2. **Run cross-tabulation queries** for each pair (A, B):

```sql
-- Template: Cross-coverage analysis
SELECT 
    A_column,
    COUNT(*) as total,
    COUNT(B_column) as b_filled,
    ROUND(100.0 * COUNT(B_column) / NULLIF(COUNT(*), 0), 2) as b_coverage_pct
FROM {TABLE}
WHERE {FILTER}
GROUP BY 1
ORDER BY 1;
```

3. **Calculate correlation metrics**:
   - **Coverage Delta**: `|coverage(B|A=TRUE) - coverage(B|A=FALSE)|`
   - **Lift**: `P(B_null|A) / P(B_null)` — values > 2 indicate strong dependency
   - **Conditional Rule**: If coverage delta > 20%, flag as dependency

4. **Flag and document strong correlations**:

| Threshold | Action |
|:---|:---|
| Lift > 2.0 | ⚠️ Document as caveat |
| Coverage delta > 50% | 🔴 Document as functional dependency |
| Perfect correlation (100%) | 📌 May indicate redundancy or derived field |

5. **Output example** (add to Caveats section of AGENTIC doc):

```markdown
### X.X. Cross-Attribute Dependencies (Auto-detected)

| Attribute A | Attribute B | Relationship | Lift |
|:---|:---|:---|---:|
| is_canceled_after_signing=TRUE | payments_as_of_date IS NULL | Functional dependency | 7.3 |
| is_bnpl_contract=FALSE | payment_status coverage | 99.3% gap | 50+ |
| c1_origin_type=NULL | c1_is_synthetic=TRUE | Perfect correlation | ∞ |
```

**Query templates**: See [CORRELATION_QUERIES.md](references/CORRELATION_QUERIES.md)

**Key insight**: This step catches issues like the payment status gap (discovered in C2_ENRICHED_REQUESTS investigation, 2026-02-05) **automatically** during profiling.

## How to Execute

### Option 1: CLI (Recommended)
```bash
cd capim-meta-ontology
python .agent/skills/investigate-entity/scripts/investigate.py --table "SCHEMA.TABLE_NAME"
```

### Option 2: Python Inline
```python
import sys
sys.path.append('.agent/skills/investigate-entity/scripts')
from investigate import profile_entity

report = profile_entity("CAPIM_DATA.CAPIM_ANALYTICS.ZENDESK_TICKETS_RAW")
print(report)
```

## Generated Sections

### For AGENTIC Doc (`<ENTITY>.md`)

1. **Schema & Grain**: Basic structure and volume
2. **Column Profile**: Null percentages and data types
3. **Domains (Text/Boolean)**: Top values and distributions
4. **Temporal Drift**: Monthly volume analysis to detect rollout/cutoff dates
5. **Relationships**: FK mappings and cardinality
6. **Population Status**: Active/Deprecated/Backfilling evidence
7. **Cross-Attribute Dependencies** (NEW): Auto-detected correlations between boolean/categorical columns

### For SEMANTIC Doc (`<ENTITY>_SEMANTIC.md`)

1. **Business Definition**: What is this entity? (1-2 sentences)
2. **Grain (Business Perspective)**: What does one row represent?
3. **Key Relationships**: Upstream dependencies and downstream consumers
4. **Common Questions This Answers**: Use cases this entity powers
5. **Status Semantics**: Business meaning of status values (if applicable)
6. **Scale & Units**: Measurement units for numeric fields (if applicable)
7. **Limitations & Caveats**: What this entity CANNOT answer
8. **PII & Sensitivity**: Privacy classification (if applicable)
9. **Source & Confirmation**: Source system and confirmation level

**Templates**: See `.cursor/rules/entity_documentation.mdc` for full section templates.

---

## Critical Distinction: What Goes Where?

**Quick principle**:
- **AGENTIC doc** = Facts from profiling (data-driven, exact stats)
- **SEMANTIC doc** = Interpretation from debate (narrative, "why" explanations)

**Detailed examples and validation checklist**: [VALIDATION_EXAMPLES.md](references/VALIDATION_EXAMPLES.md)


## Arquivos e Integração

**Scripts**:
- `scripts/investigate.py` - Lógica de profiling automatizado (migrado do Antigravity)

**Integração com Rules**:
- **Enforced by**: 
  - Rule `snowflake_data.mdc` (Zero Assumptions protocol, Snowflake-first validation)
  - Rule `entity_documentation.mdc` (Dual Documentation Pattern)
- **Uses**: `src/utils/snowflake_connection.py` (connection utility)
- **Validates**: Nullability, grain, domains, temporal drift

**Workflow com outras skills**:
- Pode ser usado por `@clinic-health-check` para contextualizar entidades
- Resultados podem alimentar `@debate` sobre decisões de tier/semântica
- Findings devem ser documentados seguindo `memory_governance.mdc`

## Implementação Atual

### Opção 1: CLI (Recomendado)

```bash
cd capim-meta-ontology
python .cursor/skills/investigate-entity/scripts/investigate.py --table "SCHEMA.TABLE_NAME"
```

### Opção 2: Python Inline

```python
import sys
sys.path.append('.cursor/skills/investigate-entity/scripts')
from investigate import profile_entity

report = profile_entity("CAPIM_DATA.CAPIM_ANALYTICS.ZENDESK_TICKETS_RAW")
print(report)
```

### Opção 3: Agent Execution (Manual)

Seguir passos de profiling manualmente usando `run_query()`:

1. Schema discovery
2. Null analysis
3. Domain profiling (categorical columns)
4. Temporal drift analysis
5. Grain validation

## Enhanced Workflow (Cursor)

**Complete workflow** with Dual Documentation:

```
1. @investigate-entity SCHEMA.TABLE
2. [Run profiling script or manual profiling]
3. [Present technical findings]
4. **Debate with user**: Clarify business semantics
   - What does this represent?
   - Why these nulls?
   - What questions does it answer?
5. **Generate AGENTIC doc** (<ENTITY>.md):
   - Use profiling results
   - Follow template from entity_documentation.mdc
6. **Generate SEMANTIC doc** (<ENTITY>_SEMANTIC.md):
   - Use debate insights
   - Follow template from entity_documentation.mdc
7. **Link files**: Add cross-references in headers
8. **Update ENTITY_INDEX.yaml**: Register entity
9. [OPTIONAL] Launch explore subagent for related context
10. **Validation**: Run checklist from entity_documentation.mdc
```

**Key Checkpoints**:

**Structure**:
- ✅ Both files created with correct naming
- ✅ Cross-references added in headers (bidirectional)
- ✅ Domain identified, ENTITY_INDEX.yaml updated

**Content**:
- ✅ **AGENTIC**: Data-driven stats only (no "why" narrative)
- ✅ **SEMANTIC**: Debate-sourced context only (no exact stats)
- ✅ No mixing between docs

**Full validation checklist**: [VALIDATION_EXAMPLES.md](references/VALIDATION_EXAMPLES.md)

## Post-Profiling Guidance

### After Running Profiling Script

The profiling script generates **technical facts only** (AGENTIC material).

**Agent MUST then**:

1. **Present findings** to user (schema, nulls, drift)
2. **Conduct debate** using questions from Step 2 above
3. **Generate AGENTIC first** (easy: structure profiling output)
4. **Generate SEMANTIC second** (harder: synthesize debate insights)

**Critical**: SEMANTIC **cannot** be auto-generated from profiling alone.

**Why**: Profiling tells you "what is" (facts). Semantic tells you "why it matters" (context).

### Common Pitfalls

❌ **Don't**: Copy profiling stats into SEMANTIC doc
❌ **Don't**: Add business narrative to DATA DICTIONARY doc
❌ **Don't**: Generate SEMANTIC without debate
❌ **Don't**: Skip cross-references in headers
❌ **Don't**: Put both docs in same folder (WRONG!)
❌ **Don't**: Put data dictionary in `_domain/_docs/reference/` (WRONG LOCATION!)

✅ **Do**: Keep each doc focused on its purpose
✅ **Do**: Put SEMANTIC in `_domain/_docs/reference/`
✅ **Do**: Put DATA DICTIONARY in `docs/reference/`
✅ **Do**: Link files bidirectionally with correct relative paths
✅ **Do**: Update ENTITY_INDEX.yaml

---

## Notas Técnicas

- **Performance**: ~5-10s para tabelas pequenas, ~30s para tabelas grandes (com SAMPLE)
- **Limitações**: Não acessa iframes, tabelas externas requerem permissões
- **Output**: Profiling script generates AGENTIC material only (debate required for SEMANTIC)

## Referências

- **Rule**: `.cursor/rules/snowflake_data.mdc` (Zero Assumptions enforcement)
- **Rule**: `.cursor/rules/entity_documentation.mdc` (Dual Documentation Pattern + Location Rules)
- **Utility**: `src/utils/snowflake_connection.py` (connection helper)
- **Examples** (note split locations):
  - `bnpl-funil/docs/reference/CREDIT_SIMULATIONS.md` + `_domain/_docs/reference/CREDIT_SIMULATIONS_SEMANTIC.md`
  - `client-voice-data/docs/reference/ZENDESK_TICKETS.md` + `_domain/_docs/reference/ZENDESK_TICKETS_SEMANTIC.md`
- **Correlation Queries**: `references/CORRELATION_QUERIES.md` (Step 6 templates)
- **Antigravity original**: `.agent/skills/investigate-entity/` (legacy reference)

---

## Changelog

| Version | Date | Change |
|:---|:---|:---|
| 2.1 | 2026-02-05 | Added Step 6: Cross-Attribute Correlation Analysis. Detects hidden dependencies between boolean/categorical columns automatically. Inspired by C2_ENRICHED_REQUESTS payment gap investigation. |
| 2.0 | 2026-01-XX | Migrated from .agent/skills, added Dual Documentation Protocol |
| 1.0 | 2025-XX-XX | Original Antigravity version |
