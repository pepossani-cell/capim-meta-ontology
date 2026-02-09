# Migração Antigravity → Cursor

> **Data da Migração**: 2026-02-03  
> **Status**: ✅ Concluída  
> **Versão**: 2.0

---

## 📋 Resumo Executivo

O sistema de workflows e skills desenvolvido para o Antigravity (`.agent/`) foi **completamente migrado** para o sistema de Rules e Skills do Cursor (`.cursor/`).

**Resultado**: Funcionalidade mantida e aprimorada com:
- ✅ Protocolo de decisões sempre ativo (Rules)
- ✅ Interatividade melhorada (AskQuestion tool)
- ✅ Scripts Python reutilizados sem modificação
- ✅ Persistência entre conversas
- ✅ Modularidade e extensibilidade

---

## 🎯 Motivação da Migração

### Por Que Migrar?

1. **Antigravity → Cursor**: Mudança de IDE/plataforma
2. **Protocol enforcement**: Rules garantem comportamento consistente
3. **Interatividade**: Cursor oferece tools superiores (AskQuestion, etc.)
4. **Persistência**: Rules aplicam automaticamente em todas as conversas
5. **Modularidade**: Skills independentes vs workflows hardcoded

### O Que Foi Migrado?

**Workflows** → **Skills**:
- `session-start.md` → `@session-start` skill
- `session-end.md` → `@session-end` skill
- `debate.md` → `@debate` skill

**Skills** → **Skills** (1:1):
- `clinic-health-check/` → Migrado com scripts
- `investigate-entity/` → Migrado com scripts
- `curate-memory/` → Migrado com scripts
- `validate-axioms/` → Migrado com scripts

**Protocolos** → **Rules** (novo):
- Protocol atômico → `memory_governance.mdc`
- Snowflake-first → `snowflake_data.mdc` (atualizado)
- Ontology reasoning → `ontology_reasoning.mdc`

---

## 🗺️ Mapa de Migração

### Estrutura de Arquivos

```
ANTES (Antigravity):
.agent/
├── workflows/
│   ├── session-start.md
│   ├── session-end.md
│   └── debate.md
└── skills/
    ├── clinic-health-check/
    ├── investigate-entity/
    ├── curate-memory/
    └── validate-axioms/

DEPOIS (Cursor):
.cursor/
├── rules/
│   ├── memory_governance.mdc      ← NOVO
│   ├── snowflake_data.mdc         ← ATUALIZADO
│   └── ontology_reasoning.mdc     ← NOVO
└── skills/
    ├── session-start/             ← Workflow migrado
    ├── session-end/               ← Workflow migrado
    ├── debate/                    ← Workflow migrado
    ├── clinic-health-check/       ← Migrado com scripts
    ├── investigate-entity/        ← Migrado com scripts
    ├── curate-memory/             ← Migrado com scripts
    └── validate-axioms/           ← Migrado com scripts
```

### Compatibilidade

| Componente | Antigravity | Cursor | Compatível? |
|------------|-------------|--------|-------------|
| **Scripts Python** | `.agent/skills/*/scripts/` | `.cursor/skills/*/scripts/` | ✅ Sim (paths ajustados) |
| **Invocação** | `/session-start` | `@session-start` | ⚠️ Sintaxe diferente |
| **Protocolo** | Manual acknowledge | Rule sempre ativa | ✅ Melhorado |
| **Escolha de domínio** | Entrada manual | AskQuestion tool | ✅ Melhorado |

---

## 📖 Guia de Uso

### Como Usar os Novos Skills

#### 1. Iniciar Sessão

**Antigravity**:
```
User: /session-start
```

**Cursor**:
```
User: @session-start
```

**Ou menção natural**:
```
User: Vamos começar a trabalhar, carrega o contexto por favor
Agent: [detecta intenção e executa @session-start]
```

#### 2. Debate/Decisão

**Antigravity**:
```
User: /debate
[Manual workflow]
```

**Cursor**:
```
User: @debate

Ou auto-detecção:
User: O que você acha de X vs Y?
Agent: [auto-invoca @debate skill]
```

#### 3. Finalizar Sessão

**Antigravity**:
```
User: /session-end
```

**Cursor**:
```
User: @session-end
```

#### 4. Skills Especializadas

**Investigar Entidade**:
```
User: @investigate-entity SCHEMA.TABLE_NAME

Ou:
User: Preciso entender a estrutura da tabela CREDIT_SIMULATIONS
Agent: [auto-invoca @investigate-entity]
```

**Validar Axioms**:
```
User: @validate-axioms

Ou:
User: Valida a integridade dos dados conforme a ontologia
Agent: [auto-invoca @validate-axioms]
```

**Clinic Health Check**:
```
User: @clinic-health-check 12345

Ou:
User: O que há de errado com a clínica 12345?
Agent: [auto-invoca @clinic-health-check]
```

---

## 🔄 Mudanças Comportamentais

### Protocolo de Decisões (Memory Governance)

**Antigravity** (Manual):
```
- Agent precisava "lembrar" de atualizar DECISIONS_IN_PROGRESS.md
- Risk: Batch updates no final (esquecimento)
- Acknowledge manual no início da sessão
```

**Cursor** (Automático):
```
- Rule memory_governance.mdc SEMPRE ativa quando edita _memory/
- Impossível esquecer protocolo
- Updates atômicos enforced automaticamente
```

**Exemplo**:
```
User: Sim, vamos com a opção B

Antigravity:
Agent: Ok! [continua trabalhando]
[Esquece de atualizar DECISIONS_IN_PROGRESS.md]

Cursor:
Agent: [PARA imediatamente]
Agent: [ATUALIZA DECISIONS_IN_PROGRESS.md]
Agent: ✅ Decision documented (ID: 7.3)
Agent: [ENTÃO continua trabalhando]
```

### Escolha de Domínio (Session Start)

**Antigravity** (Manual):
```
Agent: Qual domínio?
User: FINTECH [digita manualmente]
```

**Cursor** (Interactive):
```
Agent: Qual domínio você quer focar hoje?

[Botões interativos via AskQuestion]
○ FINTECH — BNPL Risk & Credit
○ SAAS — Clinic Operations
○ CLIENT_VOICE — Customer Voice
○ ECOSYSTEM — Meta-Ontology

User: [clica no botão]
```

---

## 🆕 Novas Capacidades

### 1. Rules Sempre Ativas

**Benefício**: Comportamento consistente sem depender de "lembrar"

**Exemplo**:
```yaml
# .cursor/rules/memory_governance.mdc
globs: ["_memory/**/*.md"]
alwaysApply: true

→ Qualquer edição em _memory/ automaticamente aplica protocolo
```

### 2. Auto-Detecção de Skills

**Benefício**: Agent pode invocar skills proativamente

**Exemplo**:
```
User: Como devemos estruturar isso? X ou Y?

Agent: [detecta ambiguidade]
Agent: [auto-invoca @debate skill]
Agent: **Decision Required**: Estrutura de...
```

### 3. Integração com Ontology

**Benefício**: Validação automática contra axioms

**Exemplo**:
```
Agent: [antes de responder query cross-domain]
Agent: [carrega ontology_reasoning.mdc]
Agent: [valida contra AXIOMS.yaml]
Agent: [se violation → revisa resposta]
```

### 4. Subagents para Tarefas Complexas

**Benefício**: Pode delegar investigações profundas

**Exemplo**:
```
User: @investigate-entity COMPLEX_TABLE

Agent: [profile básico completado]
Agent: Quer que eu explore arquivos relacionados para contexto adicional?

User: Sim

Agent: [lança explore subagent]
Agent: [busca docs, queries, referências]
Agent: [sintetiza: Profile + Context]
```

---

## 🔍 Comparação Detalhada

### Session Start

| Aspecto | Antigravity | Cursor |
|---------|------------|--------|
| **Carregamento de contexto** | Manual, hardcoded | Dinâmico, baseado em escolha |
| **Protocolo** | Acknowledge manual | Rule ativa automaticamente |
| **Escolha de domínio** | Texto livre | AskQuestion (buttons) |
| **Persistência** | Por sessão | Across conversas |

### Session End

| Aspecto | Antigravity | Cursor |
|---------|------------|--------|
| **Archive** | Manual parsing | Script Python + manual fallback |
| **Session notes** | Template manual | Gerado dinamicamente |
| **Confirmação** | Via texto | AskQuestion (se necessário) |

### Debate

| Aspecto | Antigravity | Cursor |
|---------|------------|--------|
| **Invocação** | Manual `/debate` | Auto-detect + manual `@debate` |
| **Documentação** | End of debate | Atomic (após cada decisão) |
| **Format** | Hardcoded template | Adaptável por contexto |

---

## 📦 Legacy Support

### O Que Fazer com `.agent/`?

**Status**: ⚠️ **DEPRECATED** (mantido para referência)

**README criado** em `.agent/README.md`:
```markdown
# ⚠️ DEPRECATED: Migration to Cursor

This folder is kept for **reference only**.

**Active system**: `.cursor/skills/` and `.cursor/rules/`

See migration guide: `docs/ANTIGRAVITY_TO_CURSOR_MIGRATION.md`
```

**Não deletar** porque:
- Referência histórica
- Scripts podem ser úteis como base
- Documentação de design decisions

**Não usar** porque:
- Workflows descontinuados
- Skills movidos para `.cursor/`
- Rules implementam protocolos

---

## 🚀 Próximos Passos

### Pós-Migração

1. **Testar em produção**: Usar `@session-start` em sessões reais
2. **Refinar scripts**: Melhorar `curate.py`, `validate.py` conforme uso
3. **Adicionar novos skills**: Seguir template estabelecido
4. **CI/CD integration**: Validate-axioms em pre-commit hooks

### Futuras Melhorias

1. **Automation**:
   - Script `archive_decisions.py` para session-end
   - Validação automática de axioms em CI/CD
   - Health checks agendados para clínicas críticas

2. **Enhanced UX**:
   - Dashboard de pending decisions
   - Visualização de session history
   - Metrics sobre decision velocity

3. **Integration**:
   - Slack notifications para violations
   - Auto-sync com project management tools
   - Observability dashboards

---

## 📚 Recursos Adicionais

### Documentação

- **Rules**:
  - `.cursor/rules/memory_governance.mdc`
  - `.cursor/rules/snowflake_data.mdc`
  - `.cursor/rules/ontology_reasoning.mdc`

- **Skills**:
  - `.cursor/skills/*/SKILL.md` (cada skill documentado)

- **Testing**:
  - `.cursor/skills/TEST_WORKFLOW.md` (validação end-to-end)

- **Arquitetura**:
  - `START_HERE_ECOSYSTEM.md` (visão geral atualizada)
  - `MEMORY_ARCHITECTURE_CONSTITUTION.md` (governance)

### FAQ

**Q: Posso usar comandos antigos do Antigravity (`/session-start`)?**  
A: Não diretamente, mas mencionar "session-start" deve invocar a skill automaticamente.

**Q: Scripts Python ainda funcionam?**  
A: Sim! Scripts foram copiados intactos, apenas paths mudaram (`.agent/` → `.cursor/`).

**Q: Rules aplicam automaticamente?**  
A: Sim. Baseado em glob patterns. Ex: editar `_memory/*.md` → `memory_governance.mdc` ativa.

**Q: Posso adicionar novos skills?**  
A: Sim! Seguir template dos skills migrados. Ver `.cursor/skills/*/SKILL.md` como exemplos.

**Q: E se eu quiser voltar para Antigravity?**  
A: `.agent/` ainda existe como legacy reference. Mas não recomendado (protocolo manual).

---

## ✅ Checklist de Migração Completa

- [x] Todas as Rules criadas e configuradas
- [x] Todos os workflows migrados para Skills
- [x] Todos os skills especializados migrados
- [x] Scripts Python copiados e funcionais
- [x] Documentação completa criada
- [x] `.agent/` marcado como deprecated
- [x] `START_HERE_ECOSYSTEM.md` atualizado
- [x] `.cursorrules` atualizado com referências
- [x] Test workflow validado
- [x] Guia de migração criado

---

## 🎉 Conclusão

Migração do Antigravity para Cursor **concluída com sucesso**.

O novo sistema é:
- ✅ **Mais robusto**: Protocol enforcement via Rules
- ✅ **Mais interativo**: AskQuestion tool, auto-detecção
- ✅ **Mais modular**: Skills independentes, composíveis
- ✅ **Mais rastreável**: Git-tracked, versionado
- ✅ **Mais extensível**: Fácil adicionar domains/skills

**Next**: Usar `@session-start` e começar a trabalhar! 🚀
