---
name: Validate Axioms
description: Validate ontology axioms against Snowflake data to ensure data integrity. Use when (1) after modifying AXIOMS.yaml, (2) before merge of ontology changes, (3) as part of governance review (weekly/monthly), (4) user asks "validate axioms", "check data integrity", "verificar integridade", (5) before important releases, (6) after structural data changes (migrations, new sources). Read-only validation that flags violations of HARD axioms.
version: 2.0
auto_invoke: silent
migrated_from: .agent/skills/validate-axioms/SKILL.md
---

# Validate Axioms Skill

Valida constraints lógicos definidos em `ontology/AXIOMS.yaml` executando suas `validation_query` contra Snowflake.

**Integração**: Esta skill implementa a validação prática do protocolo definido em `ontology_reasoning.mdc`.

## Quando Usar

Invoque esta skill quando:
- Após modificar `AXIOMS.yaml` (adicionar/editar axioms)
- Antes de merge de mudanças na ontologia
- Como parte de governance review regular (semanal/mensal)
- Usuário pede "validate axioms", "check data integrity", ou "verificar integridade"
- Antes de releases importantes
- Após mudanças estruturais nos dados (migrations, new sources)

**Invocação**: `@validate-axioms` ou como parte de CI/CD pipeline (futuro)

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

## Arquivos e Integração

**Scripts**:
- `scripts/validate.py` - Script de validação principal (migrado do Antigravity)

**Referências de Ontologia**:
- `../../ontology/AXIOMS.yaml` - Source de definições de axioms
- `../../src/utils/snowflake_connection.py` - Connection utilities

**Integração com Rules**:
- **Implements**: Rule `ontology_reasoning.mdc` (validation protocol)
- **Uses**: Rule `snowflake_protocol.mdc` (query execution)
- **Updates**: `_memory/DECISIONS_IN_PROGRESS.md` quando violations são encontrados

## Uso do Script

### Opção 1: Validar Todos os Axioms

```bash
cd capim-meta-ontology
python .cursor/skills/validate-axioms/scripts/validate.py
```

### Opção 2: Validar Axiom Específico

```python
import sys
sys.path.append('src/utils')
from snowflake_connection import validate_axiom

result = validate_axiom(
    axiom_id="AX-CROSS-001",
    validation_query="SELECT COUNT(*) FROM ... WHERE ..."
)
print(result)
```

## Tipos de Axioms

Conforme definido em `ontology/AXIOMS.yaml`:

| Tipo | Descrição | Ação em Violação |
|------|-----------|------------------|
| **HARD** | Nunca deve ser violado (integridade de dados) | ERRO - Requer correção imediata |
| **SOFT** | Deveria valer, mas exceções existem (business rules) | WARNING - Documentar exceção |
| **TEMPORAL** | Constraints baseados em tempo | INFO - Pode ser válido em certos períodos |

## Enhanced Workflow (Cursor)

**Integração com Git Pre-Commit** (futuro):

```yaml
# .git/hooks/pre-commit
- run: python .cursor/skills/validate-axioms/scripts/validate.py
- if: failures > 0
  action: reject commit
  message: "Axiom violations detected. Fix before committing."
```

**Auto-Documentation de Violations**:

Quando violations são encontrados, skill pode:
1. Criar issue em `DECISIONS_IN_PROGRESS.md`
2. Gerar relatório em `_memory/SESSION_NOTES/`
3. Sugerir remediation actions

## Notas Técnicas

- **Performance**: Depende da complexidade das validation queries (~5-30s total)
- **Caching**: Considerar cache de resultados (5min) para re-runs rápidos
- **Parallel execution**: Queries podem rodar em paralelo (futuro enhancement)

## Referências

- **Rule**: `.cursor/rules/ontology_reasoning.mdc` (validation protocol)
- **Rule**: `.cursor/rules/snowflake_protocol.mdc` (query execution)
- **Axioms**: `ontology/AXIOMS.yaml` (definições de constraints)
- **Antigravity original**: `.agent/skills/validate-axioms/` (legacy reference)
