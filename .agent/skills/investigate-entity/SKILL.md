---
name: Investigate Entity
description: Automatically investigate and profile a Snowflake table or view following the Snowflake-first protocol.
---

# Investigate Entity Skill

This skill automates the initial discovery and profiling of any table or view in Snowflake. It follows the protocol defined in `ontologia-cf/docs/how_to/INVESTIGATE_ENTITY.md` to ensure data-driven documentation.

> **CRITICAL RULE**: "Zero Assumptions". Never document an entity based on guesswork. If this tool cannot run, STOP and ask the user for data.

## When to Use

- When documenting a new entity in the ontology.
- To validate the quality of a source table (nulls, duplicates).
- To understand the temporal drift and population status of an entity.
- To identify PII or sensitive columns before documentation.

## Execution Process (Mandatory)

1.  **Investigate**: Run the script to gather technical facts (schema, volume, nulls).
2.  **DEBATE (Sessions)**: Present the findings to the User. Discuss:
    *   *What does this data represent logically?*
    *   *Why are these columns null?*
    *   *Is this entity Tier 1, 2, or 3?*
3.  **Document (Dual Output)**:
    *   **Agentic Doc**: Technical schema, nullability, data types (The "Body").
    *   **Semantic Doc**: Business rules, context, usage warnings (The "Soul").

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

1. **Schema & Grain**: Basic structure and volume.
2. **Column Profile**: Null percentages and data types.
3. **Domains (Text/Boolean)**: Top values and distributions.
4. **Temporal Drift**: Monthly volume analysis to detect rollout/cutoff dates.
5. **Proposal for Semantics**: (After debate) Business meaning of key columns.


## Files

- `scripts/investigate.py`: Core profiling logic.
- `SKILL.md`: This documentation.
