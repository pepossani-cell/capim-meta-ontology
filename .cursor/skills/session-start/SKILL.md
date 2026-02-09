---
name: Session Start
description: Initialize work session by loading memory context and domain-specific documentation. Use when (1) starting a new conversation, (2) resuming work after a break, (3) user says "@session-start", "iniciar sessão", "let's start", or similar, (4) beginning any work session in the Capim ecosystem. This skill loads pending decisions, lessons learned, and domain-specific context.
version: 2.0
auto_invoke: silent
migrated_from: .agent/workflows/session-start.md
---

# Session Start Skill

Carrega o contexto da sessão de trabalho no ecossistema Capim, incluindo decisões pendentes, lições aprendidas e documentação específica do domínio.

## Quando Usar

Invoque esta skill ao:
- Iniciar uma nova conversa
- Retomar trabalho após uma pausa
- Usuário dizer "@session-start", "iniciar sessão", ou "let's start"

## Pré-requisitos

Nenhum. Esta skill é auto-contida e pode ser executada a qualquer momento.

## Passos de Execução

### 1. Carregar Contexto de Memória

Ler os arquivos de estado atual:

```
📂 Arquivos a carregar:
- capim-meta-ontology/_memory/DECISIONS_IN_PROGRESS.md
- capim-meta-ontology/_memory/LESSONS_LEARNED.md
```

**Objetivo**: Entender o que está pendente, em debate, ou bloqueado.

### 2. Aplicar Protocolo Comportamental

A Rule `memory_governance.mdc` já está ativa automaticamente quando trabalhamos com arquivos de memória.

**Protocolo principal**: 
> **ATOMIC DECISION TRACKING**: Atualizar `DECISIONS_IN_PROGRESS.md` IMEDIATAMENTE após qualquer decisão confirmada. Não fazer batch updates no final da sessão.

### 3. Apresentar Resumo ao Usuário

Gerar um resumo compacto e interativo:

```markdown
📋 **Context Loaded**

**Pending (X items):**
- [Priority N]: {item} — {status}
- [Priority N]: {item} — {status}
...

**Last Activity:** {date} — {focus area}

Qual domínio você quer focar hoje?
```

**Formato**:
- Listar apenas itens com status: ⏳ Pending, 🔄 In Debate, ⚠️ Blocked
- Ordenar por prioridade (se disponível)
- Mostrar data e foco da última atividade (extrair de SESSION_NOTES mais recente)

### 4. Escolha de Domínio (Interativa)

Usar a ferramenta `AskQuestion` para permitir escolha visual:

```python
# Usar AskQuestion tool com estas opções:
questions = [{
    "id": "domain_choice",
    "prompt": "Qual domínio você quer focar hoje?",
    "options": [
        {"id": "fintech", "label": "FINTECH — BNPL Risk & Credit (bnpl-funil)"},
        {"id": "saas", "label": "SAAS — Clinic Operations (ontologia-saas)"},
        {"id": "client_voice", "label": "CLIENT_VOICE — Customer Voice (client-voice)"},
        {"id": "ecosystem", "label": "ECOSYSTEM — Meta-Ontology (capim-meta-ontology)"},
        {"id": "skip", "label": "Pular escolha de domínio (continuar sem contexto específico)"}
    ],
    "allow_multiple": false
}]
```

### 5. Carregar Contexto do Domínio

Com base na escolha do usuário, carregar o `START_HERE.md` correspondente:

| Domínio | Arquivo a Carregar |
|---------|-------------------|
| **FINTECH** | `bnpl-funil/_domain/START_HERE.md` |
| **SAAS** | `ontologia-saas/_domain/START_HERE.md` |
| **CLIENT_VOICE** | `client-voice/START_HERE.md` |
| **ECOSYSTEM** | `capim-meta-ontology/START_HERE_ECOSYSTEM.md` |
| **skip** | (não carregar nada adicional) |

**Importante**: Ler o arquivo completo e apresentar um resumo de 2-3 parágrafos ao usuário sobre:
- Foco do domínio
- Principais entidades
- Onde encontrar documentação adicional

### 6. Confirmação de Prontidão

Finalizar com mensagem de confirmação:

```markdown
✅ Contexto {DOMAIN} carregado. Pronto para trabalhar!

Como posso ajudar?
```

## Diferenças vs Antigravity

| Aspecto | Antigravity | Cursor (Esta Skill) |
|---------|------------|-------------------|
| **Invocação** | `/session-start` | `@session-start` ou menção natural |
| **Protocolo** | "Acknowledge" manual | Rule `memory_governance.mdc` sempre ativa |
| **Escolha de domínio** | Entrada de texto manual | `AskQuestion` tool (botões interativos) |
| **Carregamento** | Hardcoded no workflow | Dinâmico baseado em escolha |

## Outputs

**Sucesso**:
- Contexto de memória carregado
- Resumo de pending items apresentado
- Domínio escolhido e contexto carregado
- Usuário pronto para trabalhar

**Falha** (rara):
- Se `DECISIONS_IN_PROGRESS.md` não existir: criar arquivo base
- Se domínio escolhido não tiver START_HERE.md: avisar usuário

## Integração com Outras Skills

- **Complementado por**: `@debate` (para decisões complexas)
- **Seguido por**: Trabalho normal no domínio
- **Finalizado com**: `@session-end` (para arquivar e consolidar)

## Exemplo de Uso

```
User: @session-start

Agent: [executa esta skill]

📋 **Context Loaded**

**Pending (3 items):**
- [Priority 2]: Investigate SaaS patients identification → ⏳ Pending
- [Priority 5]: Populate vox_popular with ETL data → ⚠️ Blocked (DB Connection)
- [Priority 9]: Meta-Architecture Review → 🔄 Ongoing

**Last Activity:** 2026-02-03 — Zendesk bifurcation investigation

Qual domínio você quer focar hoje?

[Botões interativos via AskQuestion]
○ FINTECH — BNPL Risk & Credit (bnpl-funil)
○ SAAS — Clinic Operations (ontologia-saas)
○ CLIENT_VOICE — Customer Voice (client-voice)
○ ECOSYSTEM — Meta-Ontology (capim-meta-ontology)
○ Pular escolha de domínio

User: [selects FINTECH]

Agent: [loads bnpl-funil/_domain/START_HERE.md]

O domínio FINTECH foca em análise de risco de crédito e conversão do funil BNPL. 
As principais entidades são: Credit Simulations, Pre-Analyses, Risk Scores, e Bureau Data.

Documentação adicional em: bnpl-funil/_domain/_docs/

✅ Contexto FINTECH carregado. Pronto para trabalhar! 🚀

Como posso ajudar?
```

## Notas Técnicas

- **Performance**: Leitura de arquivos é rápida (< 1s para todos os arquivos)
- **Fallback**: Se algum arquivo não existir, continuar com o que está disponível
- **Extensibilidade**: Novos domínios podem ser adicionados facilmente no AskQuestion options

## Referências

- **Rule**: `.cursor/rules/memory_governance.mdc` (protocolo atômico)
- **Antigravity original**: `.agent/workflows/session-start.md` (legacy reference)
- **Arquitetura**: `START_HERE_ECOSYSTEM.md` (visão geral do ecossistema)
