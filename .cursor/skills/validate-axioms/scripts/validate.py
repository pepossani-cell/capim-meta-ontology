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
        'fail': [],
        'error': [],
        'skip': []
    }
    
    for axiom in axioms:
        axiom_id = axiom.get('id', 'UNKNOWN')
        validation_query = axiom.get('validation_query')
        
        if not validation_query:
            results['skip'].append({
                'axiom_id': axiom_id,
                'reason': 'No validation_query defined'
            })
            continue
        
        result = validate_axiom(axiom_id, validation_query)
        
        if result['status'] == 'PASS':
            results['pass'].append(result)
        elif result['status'] == 'FAIL':
            results['fail'].append(result)
        else:
            results['error'].append(result)
    
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
    total = len(results['pass']) + len(results['fail']) + len(results['error']) + len(results['skip'])
    print(f"\nSummary: {len(results['pass'])} PASS, {len(results['fail'])} FAIL, {len(results['error'])} ERROR, {len(results['skip'])} SKIP")
    print("=" * 50)
    
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
