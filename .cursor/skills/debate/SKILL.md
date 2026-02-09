---
name: Debate
description: Structured decision-making for complex topics with multiple options. Use when (1) user asks "what do you think about X vs Y?", (2) topic has 2+ viable options with trade-offs, (3) decision affects multiple files or systems, (4) user seems uncertain about direction, (5) agent identifies multiple valid approaches, (6) ambiguity is detected that requires explicit decision. Can be auto-invoked when agent detects ambiguity. Updates DECISIONS_IN_PROGRESS.md atomically after each confirmed decision.
version: 2.0
auto_invoke: ask_first
migrated_from: .agent/workflows/debate.md
---

# Debate Skill

Facilita decisões estruturadas quando há múltiplas opções, trade-offs complexos, ou incerteza sobre a direção.

## Quando Usar

Ative esta skill quando:
- Usuário pergunta "o que você acha de X vs Y?"
- Tópico tem mais de 2 opções viáveis
- Decisão afetará múltiplos arquivos ou sistemas
- Usuário parece incerto sobre a direção
- Trade-offs precisam ser explicitados
- Você (agent) identificar múltiplas abordagens válidas

**Auto-detecção**: Esta skill pode ser invocada automaticamente quando o agent detecta ambiguidade ou múltiplas opções.

## Modelo de Decisão

**Decision-centric**: Cada decisão confirmada é um **checkpoint atômico**.

**⚠️ CRÍTICO**: Atualizar `DECISIONS_IN_PROGRESS.md` IMEDIATAMENTE após confirmação, não ao final do debate.

## Pré-requisitos

- Contexto suficiente sobre o tópico em debate
- Acesso de escrita a `_memory/DECISIONS_IN_PROGRESS.md`

## Passos de Execução

### 1. Frame the Question

Claramente declarar o que está sendo decidido:

```markdown
**Decision Required**: [Statement claro do que precisa ser decidido]

**Context**: [Por que esta decisão importa? Qual é o problema ou oportunidade?]

**Constraints**: [Limitações ou requisitos que restringem as opções]
```

**Exemplo**:
```markdown
**Decision Required**: Como estruturar a documentação de entidades no projeto ontologia-cf?

**Context**: Atualmente há documentação duplicada entre SAAS e FINTECH. Precisamos consolidar sem perder contexto específico de cada domínio.

**Constraints**: 
- Deve ser compatível com ferramentas de indexação existentes
- Não pode quebrar scripts que dependem de paths atuais
- Deve facilitar federation cross-domain
```

### 2. Present Options

Usar tabela estruturada para comparação:

```markdown
## Options

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | {Brief description} | • {Pro 1}<br>• {Pro 2}<br>• {Pro 3} | • {Con 1}<br>• {Con 2} |
| **B** | {Brief description} | • {Pro 1}<br>• {Pro 2} | • {Con 1}<br>• {Con 2}<br>• {Con 3} |
| **C** | {Brief description} | • {Pro 1}<br>• {Pro 2}<br>• {Pro 3} | • {Con 1}<br>• {Con 2} |
```

**Guidelines**:
- **Mínimo 2 opções**, máximo 5 (mais que isso = simplificar)
- **Pros/Cons honestos**: Não omitir downsides
- **Descrição concisa**: 1-2 frases por opção
- **Comparáveis**: Facilitar side-by-side comparison

### 3. Make a Recommendation

**SEMPRE** fornecer uma recomendação com rationale:

```markdown
## Recommendation

**Opção recomendada**: {Option X}

**Rationale**:
- {Reason 1: Por que esta opção é preferível}
- {Reason 2: Como ela resolve o problema central}
- {Reason 3: Trade-offs que valem a pena}

**Alternative acceptable**: {Option Y} se {condition}
```

**Importante**: 
- Seja decisivo (não "talvez A ou B")
- Justifique baseado em constraints e context
- Admita se não tiver informação suficiente

### 4. Wait for Confirmation

**NÃO proceder** com execução sem confirmação explícita do usuário.

**Trigger words que indicam confirmação**:
- ✅ "sim", "ok", "confirmado", "aprovado"
- ✅ "vamos com X", "let's go with X"
- ✅ "agreed", "concordo", "I choose X"

**Trigger words que pedem mais discussão**:
- 🔄 "e se...", "what if...", "mas..."
- 🔄 "tenho dúvidas sobre...", "I'm concerned about..."
- 🔄 "discuss more", "discutir mais"

**Se dúvida**: Perguntar explicitamente "Confirma esta decisão?"

### 5. Document Decision — IMMEDIATELY

**⚠️ CRITICAL**: Fazer isto ANTES de continuar com próxima pergunta ou tópico.

Uma vez que decisão é confirmada:

1. **STOP** o fluxo do debate
2. **UPDATE** `_memory/DECISIONS_IN_PROGRESS.md` com a decisão específica
3. **THEN** retomar discussão

**Formato de documentação**:

```markdown
| ID | Topic | Status | Decision | Notes |
| :--- | :--- | :--- | :--- | :--- |
| X.Y | {Topic} | ✅ Decided | {Option chosen} | {Rationale summary} + Related: {files if applicable} |
```

**Não esperar** todas as perguntas serem respondidas. Cada decisão = checkpoint atômico.

### 6. Consolidate (End of Debate)

Quando todas as questões do debate forem resolvidas:

```markdown
## Debate Summary

**Decisions Made**: {count}
- {Decision 1} (ID: X.Y) — ✅ Decided
- {Decision 2} (ID: X.Z) — ✅ Decided

**Next Actions**:
- {Action 1 to implement decision 1}
- {Action 2 to implement decision 2}

**Documentation Updated**:
- ✅ DECISIONS_IN_PROGRESS.md updated with {count} decisions

Proceed with implementation? [Yes/Wait]
```

**Se pattern emergir**: Adicionar a `LESSONS_LEARNED.md`

**Se decisões executáveis agora**: Marcar como "ready for execution"

## Exemplo Completo

```
User: Como devemos estruturar as rules no Cursor? Centralizar tudo em uma rule ou separar por domínio?

Agent: [ativa @debate skill]

**Decision Required**: Estrutura das Cursor Rules para o workspace capim-meta-ontology

**Context**: Migrando workflows do Antigravity. Precisamos definir se rules devem ser monolíticas ou modulares.

**Constraints**:
- Cursor aplica rules baseado em glob patterns
- Devem ser fáceis de manter
- Não podem conflitar entre si

## Options

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Monolítica** | Uma rule grande com todas as regras | • Simples de encontrar<br>• Não há conflito de precedência | • Difícil de manter<br>• Carrega desnecessariamente<br>• Menos granular |
| **B: Por Domínio** | Rules separadas por área (memory, snowflake, ontology) | • Contexto específico<br>• Carrega só quando relevante<br>• Fácil de editar | • Múltiplos arquivos<br>• Pode haver overlap |
| **C: Híbrido** | Core rules + domain-specific rules | • Melhor dos dois mundos<br>• Flexível | • Mais complexo inicialmente |

## Recommendation

**Opção recomendada**: B (Por Domínio)

**Rationale**:
- Glob patterns do Cursor permitem aplicação contextual eficiente
- Manutenção mais fácil: editar memory rules não afeta snowflake rules
- Alinhado com arquitetura modular do projeto

**Alternative acceptable**: C (Híbrido) se houver muitas regras cross-cutting

Confirma esta decisão?

User: Sim, vamos com B

Agent: [STOP e atualiza DECISIONS_IN_PROGRESS.md]

✅ Decision documented in DECISIONS_IN_PROGRESS.md

| ID | Topic | Status | Decision | Notes |
| 7.1 | Cursor Rules Structure | ✅ Decided | Domain-separated (memory, snowflake, ontology) | Better maintainability, contextual loading via globs |

Debate concluído! Próximo passo é implementar as 3 rules. Deseja que eu prossiga?
```

## Fluxo de Auto-Detecção

Quando agent detecta ambiguidade **sem** usuário invocar explicitamente:

```
User: Acho que devemos documentar as entidades...

Agent: [detecta ambiguidade]

Vejo que há diferentes abordagens possíveis. Posso estruturar um debate para decidirmos a melhor opção?

[Yes/No]

User: Yes

Agent: [ativa @debate skill e segue os 6 passos]
```

## Integração com Memory Governance

Esta skill **depende** da Rule `memory_governance.mdc`:

- **Status markers** vêm da rule
- **Atomic tracking** é enforced pela rule
- **Archive readiness** segue protocol da rule

## Anti-Patterns

❌ **Don't**:
- Apresentar opções sem recommendation
- Executar antes de confirmação (para mudanças estruturais)
- Usar linguagem vaga ("maybe", "could be", "talvez")
- Skip análise de trade-offs
- Batch documentação de múltiplas decisões

✅ **Do**:
- Ser honesto sobre incerteza (quando aplicável)
- Apresentar trade-offs claramente
- Fazer recommendation decisiva
- Atualizar tracking documents atomicamente
- Confirmar antes de executar mudanças grandes

## Variações

### Debate Rápido (1-2 opções)

Para decisões menores:

```markdown
**Quick Decision**: {Topic}

**Options**: A (current) vs B (proposed)

**Recommendation**: B because {reason}

Confirma?
```

### Debate Profundo (Pesquisa Necessária)

Se precisar investigar antes de opções:

```markdown
**Decision Required**: {Topic}

**Current Understanding**: {What we know}

**Information Needed**: {What's missing}

**Proposed Approach**:
1. Investigate {X}
2. Reconvene with options
3. Decide

Proceed with investigation?
```

## Referências

- **Rule**: `.cursor/rules/memory_governance.mdc` (atomic tracking protocol)
- **Skill**: `@session-start` (carrega decisões pendentes)
- **Skill**: `@session-end` (arquiva decisões executadas)
- **Antigravity original**: `.agent/workflows/debate.md` (legacy reference)
