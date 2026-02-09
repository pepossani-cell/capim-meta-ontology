---
name: Session End
description: Archive executed decisions and consolidate session notes. Use when (1) ending the work day, (2) completing an important milestone, (3) DECISIONS_IN_PROGRESS.md has many executed/rejected items, (4) before a long break, (5) user says "@session-end", "finalizar sessão", "let's wrap up", or similar. This skill archives completed decisions and creates session notes for traceability. Involves write operations.
version: 2.0
auto_invoke: ask_first
migrated_from: .agent/workflows/session-end.md
---

# Session End Skill

Consolida o trabalho da sessão, arquivando decisões executadas e criando notas de sessão para rastreabilidade.

## Quando Usar

Invoque esta skill quando:
- Terminar o dia de trabalho
- Completar um marco importante
- `DECISIONS_IN_PROGRESS.md` tiver muitos itens ✅➡️ (Executed) ou ❌ (Rejected)
- Antes de um break longo (férias, etc.)
- Usuário dizer "@session-end", "finalizar sessão", ou "let's wrap up"

## Modelo de Trabalho

**Decision-centric**: Decisões já foram salvas IMEDIATAMENTE durante a conversa (protocolo atômico).

Esta skill é para **ARQUIVAMENTO** e **CONSOLIDAÇÃO**, não para tracking em tempo real.

## Pré-requisitos

- `_memory/DECISIONS_IN_PROGRESS.md` deve existir
- Acesso de escrita aos arquivos de memória

## Passos de Execução

### 1. Revisar DECISIONS_IN_PROGRESS.md

Ler o estado atual:

```
📂 Arquivo a revisar:
- capim-meta-ontology/_memory/DECISIONS_IN_PROGRESS.md
```

**Identificar**:
- Itens com status ✅➡️ (Executed) — prontos para arquivar
- Itens com status ❌ (Rejected) — prontos para arquivar
- Itens com outros status — mantêm-se no tracker

### 2. Apresentar Itens para Arquivar

Mostrar ao usuário o que pode ser arquivado:

```markdown
📦 **Items Ready to Archive:**

**Executed (ready to move):**
- [X.Y] {Topic} — {Decision summary}
- [X.Z] {Topic} — {Decision summary}

**Rejected (ready to move):**
- [A.B] {Topic} — {Why rejected}

**Still Active (will remain in tracker):**
- ⏳ Pending: {count} items
- 🔄 In Debate: {count} items

Move executed/rejected items to archive? [Yes/No/Select specific]
```

### 3. Confirmar com Usuário

Aguardar confirmação explícita antes de mover.

**Opções**:
- **Yes**: Arquivar todos os itens Executed + Rejected
- **No**: Cancelar operação (manter tudo no tracker)
- **Select specific**: Usuário escolhe quais itens arquivar

**Usar AskQuestion tool** para confirmação interativa se necessário.

### 4. Criar/Atualizar Arquivo de Archive

Quando confirmado, mover itens para:

```
📂 Destino:
- capim-meta-ontology/_memory/DECISIONS_ARCHIVE/YYYY-MM_topic.md
```

**Formato do arquivo de archive**:

```markdown
# 📁 Decision Archive: {Topic} ({YYYY-MM})

## Archived: {YYYY-MM-DD}

### {ID} {Title}

**Status**: ✅➡️ Executed (ou ❌ Rejected)

**Decision**: {decision text}

**Rationale**: {why this was chosen}

**Executed On**: {date}

**Related Files**: 
- {file1}
- {file2}

---

### {Next ID} {Next Title}
...
```

**Naming convention**:
- Por tópico: `YYYY-MM_topic.md` (ex: `2026-02_architecture.md`)
- Geral: `YYYY-MM.md` (quando não há tópico específico)

**Se arquivo já existir**: Append ao final (não sobrescrever)

### 5. Remover do DECISIONS_IN_PROGRESS.md

Após mover para archive, remover os itens arquivados do tracker ativo.

**Manter**:
- Headers das seções
- Itens com status: ⏳ Pending, 🔄 In Debate, ✅ Decided (ainda não executados)
- Referências a archives anteriores

**Importante**: Preservar a estrutura do documento (tabelas, sections, etc.)

### 6. Criar/Atualizar Session Note

Criar ou atualizar a nota da sessão:

```
📂 Destino:
- capim-meta-ontology/_memory/SESSION_NOTES/YYYY-MM-DD.md
```

**Formato**:

```markdown
# Session Notes: {YYYY-MM-DD}

## Focus
{What was the main focus of this session?}

## Accomplishments
- {Achievement 1}
- {Achievement 2}
- {Achievement 3}

## Decisions Made
- {Decision 1} (ID: X.Y)
- {Decision 2} (ID: A.B)

## Decisions Archived
- {count} items moved to DECISIONS_ARCHIVE/{file}

## Pending Items
- {count} items remain in DECISIONS_IN_PROGRESS.md

## Knowledge Harvested
{Any patterns, learnings, or insights from this session}

## Next Steps
- {Next action 1}
- {Next action 2}
```

**Gerar dinamicamente** com base no que foi feito na sessão.

### 7. Reflective Checkout

Apresentar resumo final ao usuário:

```markdown
🧘 **Reflective Checkout**

**Archived**: {count} decisions moved to archive
**Archive file**: _memory/DECISIONS_ARCHIVE/{filename}

**Still Pending**: {count} items remain in progress
- ⏳ Pending: {count}
- 🔄 In Debate: {count}

**Session Note Created**: _memory/SESSION_NOTES/{date}.md

**Knowledge Harvested**:
- {pattern 1}
- {pattern 2}

**Next Session**:
- Use `@session-start` to load context and continue
- Focus areas: {suggested focus based on pending items}

See you next time! 👋
```

## Fluxo Completo (Exemplo)

```
User: @session-end

Agent: [lê DECISIONS_IN_PROGRESS.md]

📦 **Items Ready to Archive:**

**Executed:**
- [5.7] Naming convention for entity docs — Adopted _SEMANTIC.md pattern
- [6.2] Pre-Analysis Linkage Strategy — V8 (Hybrid) implemented

**Rejected:**
- [H2] Use droz_template as primary classifier — Rejected (too fragile)

**Still Active:**
- ⏳ Pending: 2 items
- 🔄 In Debate: 1 item

Move executed/rejected items to archive? [Yes/No]

User: Yes

Agent: [executa arquivamento]

✅ Archived 3 items to `_memory/DECISIONS_ARCHIVE/2026-02-03_zendesk.md`
✅ Updated DECISIONS_IN_PROGRESS.md (3 items removed)
✅ Created session note: `_memory/SESSION_NOTES/2026-02-03.md`

🧘 **Reflective Checkout**

**Archived**: 3 decisions
**Still Pending**: 3 items

**Knowledge Harvested**:
- Entity naming patterns stabilized across domains
- Hybrid linkage strategies work better than pure approaches

**Next Session**: Use `@session-start` to continue

See you next time! 👋
```

## Script Auxiliar (Opcional)

Um script Python pode automatizar o parsing e movimentação:

```
📂 Script (futuro):
- .cursor/skills/session-end/scripts/archive_decisions.py
```

**Funcionalidade**:
- Parse DECISIONS_IN_PROGRESS.md (markdown table)
- Identificar itens com status ✅➡️ ou ❌
- Gerar arquivo de archive formatado
- Remover itens do tracker
- Criar session note template

**Por enquanto**: Fazer manualmente com StrReplace/Read/Write tools.

## Integração com Outras Skills

- **Precedido por**: `@session-start` e trabalho durante a sessão
- **Complementa**: Rule `memory_governance.mdc` (decisões já rastreadas atomicamente)
- **Seguido por**: Nova sessão com `@session-start`

## Anti-Patterns

❌ **Don't**:
- Arquivar itens que ainda estão ⏳ Pending ou 🔄 In Debate
- Arquivar decisões ✅ Decided mas não executadas
- Deletar itens em vez de arquivar
- Skip a criação de session notes

✅ **Do**:
- Confirmar com usuário antes de arquivar
- Preservar contexto completo no archive
- Criar session notes mesmo para sessões curtas
- Manter DECISIONS_IN_PROGRESS.md limpo e focado

## Referências

- **Rule**: `.cursor/rules/memory_governance.mdc` (protocolo de status)
- **Antigravity original**: `.agent/workflows/session-end.md` (legacy reference)
- **Arquitetura**: `MEMORY_ARCHITECTURE_CONSTITUTION.md` (governance principles)
