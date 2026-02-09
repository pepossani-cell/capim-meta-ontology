---
name: Curate Memory
description: Automate governance and housekeeping of memory files (DECISIONS_IN_PROGRESS, SESSION_NOTES). Use when (1) at end of work session (normally via @session-end), (2) DECISIONS_IN_PROGRESS.md became too large or disorganized, (3) formalizing transition from active debate to permanent record, (4) periodic maintenance (weekly/monthly), (5) before important milestone (release, presentation). Archives completed/rejected decisions and moves session notes to permanent storage. Involves write operations.
version: 2.0
auto_invoke: ask_first
migrated_from: .agent/skills/curate-memory/SKILL.md
---

# Curate Memory Skill

Garante que arquivos de memória permaneçam concisos e acionáveis, movendo itens completados ou rejeitados para archives permanentes.

**Integração**: Esta skill complementa o workflow `@session-end`, podendo ser usada de forma standalone para manutenção ad-hoc.

## Quando Usar

Invoque esta skill quando:
- No final de cada sessão de trabalho (normalmente via `@session-end`)
- `DECISIONS_IN_PROGRESS.md` ficou muito grande ou desorganizado
- Formalizar transição de "active debate" para "permanent record"
- Manutenção periódica (semanal/mensal) dos arquivos de memória
- Antes de um marco importante (release, apresentação, etc.)

**Invocação**: `@curate-memory` ou como parte de `@session-end`

## How to Execute

### CLI
```bash
cd capim-meta-ontology
python .agent/skills/curate-memory/scripts/curate.py
```

## Logic Rules

1. **Auto-Archive**: Items in `DECISIONS_IN_PROGRESS.md` marked with `✅➡️` (Executed) or `❌` (Rejected) are extracted.
2. **Permanent Storage**: Extracted items are appended to `_memory/DECISIONS_ARCHIVE/YYYY-MM_archived_decisions.md`.
3. **Session Notes**: Moves the "(In Progress)" section of session notes to `_memory/SESSION_NOTES/YYYY-MM-DD.md`.
4. **Cleanup**: Removes archived items from the active tracker while preserving headers and pending items.

## Arquivos e Integração

**Scripts**:
- `scripts/curate.py` - Engine de automação (migrado do Antigravity)

**Integração com Rules**:
- **Enforced by**: Rule `memory_governance.mdc` (status markers e archive rules)
- **Works with**: Skill `@session-end` (workflow completo de finalização)
- **Updates**: `_memory/DECISIONS_IN_PROGRESS.md`, `_memory/DECISIONS_ARCHIVE/`, `_memory/SESSION_NOTES/`

## Uso do Script

### Opção 1: CLI

```bash
cd capim-meta-ontology
python .cursor/skills/curate-memory/scripts/curate.py
```

**Output**:
- Lista itens que serão arquivados
- Pede confirmação
- Move itens para ARCHIVE
- Limpa DECISIONS_IN_PROGRESS.md

### Opção 2: Como Parte de @session-end

O workflow `@session-end` pode invocar este script automaticamente:

```
User: @session-end

Agent: [executa session-end skill]
  → Identifica itens ✅➡️ e ❌
  → Chama curate.py (ou faz manualmente)
  → Cria session notes
  → Apresenta reflective checkout
```

## Notas Técnicas

- **Performance**: < 1s para processar arquivo típico
- **Safety**: Sempre pede confirmação antes de mover
- **Backup**: Itens nunca são deletados, apenas movidos
- **Idempotência**: Pode rodar múltiplas vezes sem problemas

## Referências

- **Rule**: `.cursor/rules/memory_governance.mdc` (archive protocol)
- **Skill**: `.cursor/skills/session-end/SKILL.md` (workflow completo)
- **Antigravity original**: `.agent/skills/curate-memory/` (legacy reference)
