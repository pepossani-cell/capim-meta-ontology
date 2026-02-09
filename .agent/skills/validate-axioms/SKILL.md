---
name: Validate Axioms
description: Validate ontology axioms against Snowflake data
---

# Validate Axioms Skill

This skill validates the logical constraints defined in `ontology/AXIOMS.yaml` by executing their `validation_query` against Snowflake.

## When to Use

- After modifying AXIOMS.yaml
- Before merging ontology changes
- As part of regular governance review
- When user asks "validate axioms" or "check data integrity"

## Prerequisites

1. Snowflake credentials in `.env` file
2. `snowflake-connector-python` installed
3. `python-dotenv` and `pandas` installed

## How to Execute

### Option 1: Use the Script
```bash
cd capim-meta-ontology
python .agent/skills/validate-axioms/scripts/validate.py
```

### Option 2: Inline Execution
```python
import sys
sys.path.append('src/utils')
from snowflake_connection import validate_axiom

# Example: Validate a single axiom
result = validate_axiom(
    axiom_id="AX-CROSS-001",
    validation_query="SELECT COUNT(*) FROM ... WHERE ..."
)
print(result)
```

## Expected Output

```
Axiom Validation Report
=======================
Date: 2026-02-01

✅ AX-FINTECH-001: PASS (0 violations)
✅ AX-FINTECH-002: PASS (0 violations)
❌ AX-CROSS-001: FAIL (15 violations)
⚠️ AX-SAAS-001: ERROR (Query execution failed)

Summary: 2 PASS, 1 FAIL, 1 ERROR
```

## Handling Failures

If an axiom fails:
1. Check if the axiom definition is correct
2. Check if the data has a genuine integrity issue
3. Update `_memory/DECISIONS_IN_PROGRESS.md` with the finding
4. Propose remediation (fix data or update axiom)

## Files

- `scripts/validate.py` - Main validation script
- `../../ontology/AXIOMS.yaml` - Source of axiom definitions
- `../../src/utils/snowflake_connection.py` - Connection utilities
