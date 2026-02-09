"""
Axiom Validation Script
Validates all axioms defined in AXIOMS.yaml against Snowflake.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
# validate.py lives in: <repo>/.cursor/skills/validate-axioms/scripts/validate.py
# so repo root is 5 levels up from this file.
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root / "src" / "utils"))

import yaml
from snowflake_connection import validate_axiom, run_query


def load_axioms(axioms_path: Path) -> list:
    """Load axioms from YAML file."""
    with open(axioms_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('axioms', [])


def validate_all_axioms(axioms: list) -> dict:
    """Validate all axioms and return results."""
    results = {
        'pass': [],
        'warn': [],
        'info': [],
        'fail': [],
        'error': [],
        'skip': []
    }
    
    for axiom in axioms:
        axiom_id = axiom.get('id', 'UNKNOWN')
        validation_query = axiom.get('validation_query')
        severity = (axiom.get('severity') or '').upper()
        
        if not validation_query:
            results['skip'].append({
                'axiom_id': axiom_id,
                'reason': 'No validation_query defined'
            })
            continue

        # Execute query and interpret first cell as "violations count"
        try:
            df = run_query(validation_query)
            if df is None or df.empty:
                count = 0
            else:
                count = df.iloc[0, 0]
                if count is None:
                    count = 0
                count = int(count)
        except Exception as e:
            results['error'].append({
                'axiom_id': axiom_id,
                'status': 'ERROR',
                'count': -1,
                'message': f"Failed to execute query: {e}"
            })
            continue

        # Classify based on severity
        if count == 0:
            results['pass'].append({'axiom_id': axiom_id, 'status': 'PASS', 'count': 0, 'severity': severity})
        else:
            if severity == 'HARD':
                results['fail'].append({'axiom_id': axiom_id, 'status': 'FAIL', 'count': count, 'severity': severity})
            elif severity == 'TEMPORAL':
                results['info'].append({'axiom_id': axiom_id, 'status': 'INFO', 'count': count, 'severity': severity})
            else:
                # Default: SOFT and unknown severities are treated as warnings
                results['warn'].append({'axiom_id': axiom_id, 'status': 'WARN', 'count': count, 'severity': severity or 'SOFT'})
    
    return results


def print_report(results: dict):
    """Print formatted validation report."""
    print("\n" + "=" * 50)
    print("AXIOM VALIDATION REPORT")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Print PASS
    for r in results['pass']:
        print(f"[PASS] {r['axiom_id']}: {r['count']} violations")

    # Print WARN
    for r in results['warn']:
        print(f"[WARN] {r['axiom_id']}: {r['count']} violations (severity={r.get('severity')})")

    # Print INFO
    for r in results['info']:
        print(f"[INFO] {r['axiom_id']}: {r['count']} (severity={r.get('severity')})")
    
    # Print FAIL
    for r in results['fail']:
        print(f"[FAIL] {r['axiom_id']}: {r['count']} violations")
    
    # Print ERROR
    for r in results['error']:
        print(f"[ERROR] {r['axiom_id']}: {r['message']}")
    
    # Print SKIP
    for r in results['skip']:
        print(f"[SKIP] {r['axiom_id']}: {r['reason']}")
    
    # Summary
    total = (
        len(results['pass'])
        + len(results['warn'])
        + len(results['info'])
        + len(results['fail'])
        + len(results['error'])
        + len(results['skip'])
    )
    print(
        f"\nSummary: {len(results['pass'])} PASS, {len(results['warn'])} WARN, {len(results['info'])} INFO, "
        f"{len(results['fail'])} FAIL, {len(results['error'])} ERROR, {len(results['skip'])} SKIP"
    )
    print("=" * 50)
    
    # Only HARD failures and execution errors should fail the process
    return len(results['fail']) == 0 and len(results['error']) == 0


def main():
    """Main entry point."""
    # Path to AXIOMS.yaml
    axioms_path = project_root / "ontology" / "AXIOMS.yaml"
    
    if not axioms_path.exists():
        print(f"Error: AXIOMS.yaml not found at {axioms_path}")
        sys.exit(1)
    
    print(f"Loading axioms from: {axioms_path}")
    axioms = load_axioms(axioms_path)
    print(f"Found {len(axioms)} axioms to validate")
    
    print("\nConnecting to Snowflake and running validations...")
    results = validate_all_axioms(axioms)
    
    success = print_report(results)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
