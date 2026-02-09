---
name: EDA Workflow
description: Finite-state workflow for exploratory data analysis with integrated debate. Use when (1) starting a new EDA/study from scratch, (2) iterating hypotheses with data (Snowflake-first), (3) user mentions "explorar dados", "análise exploratória", "investigar hipótese", (4) building classes/buckets/axes and encountering ambiguity, (5) transitioning findings from scratchpad to stable artifacts, (6) agent detects need to systematically explore data patterns. Implements FST-based state machine with guardrails that trigger @debate on ambiguity.
version: 1.0
auto_invoke: ask_first
composes: [investigate-entity, debate, formalize-saas-finding, formalize-fintech-finding, validate-saas-contracts]
based_on:
  - ontologia-saas/docs/how_to/EDA_PLAYBOOK.md
  - ontologia-saas/docs/how_to/PROGRESSIVE_FORMALIZATION.md
references:
  - "OpenAI: A Practical Guide to Building Agents (2025)"
  - "DatawiseAgent: FST-Based Framework (EMNLP 2025)"
---

# EDA Workflow Skill

Workflow estruturado para Análise Exploratória de Dados (EDA) usando uma **máquina de estados finitos (FST)** com **debate integrado** para decisões críticas.

## Quando Usar

Invoque esta skill quando:
- Começar uma EDA/estudo do zero
- Iterar hipóteses com dados (Snowflake-first)
- Montar classes/buckets/eixos e perceber ambiguidades
- Transicionar achados de scratchpad para artefatos estáveis
- Precisar de estrutura para exploração que é "errática, volátil, cíclica"

**Invocação**: `@eda-workflow` ou menção natural ("explorar dados", "análise exploratória")

---

## Conceitos Fundamentais

### EDA é Cíclico e Volátil

**Princípio**: Exploração boa é iterativa — corrigir premissas faz parte.

O que deve estabilizar **NÃO** é o caminho investigativo, e sim:
- ✅ **Invariantes verificáveis** (microtests)
- ✅ **Contratos de saída** (grão, chaves, classes/eixos)
- ✅ **Decisões de semântica** (quando a interpretação muda)

### FST: Finite-State Transducer

Esta skill modela EDA como uma **máquina de estados** com transições claras:

```
┌──────────┐    promote    ┌──────────┐    stabilize   ┌──────────┐
│ TATEANTE │──────────────>│ CALIBRAR │───────────────>│ ESTÁVEL  │
└────┬─────┘               └────┬─────┘                └────┬─────┘
     │                          │                           │
     │<─────── rollback ────────┘                           │
     │                                                      │
     │<──────────────── new cycle ──────────────────────────┘
     │
     ▼
  [GUARDRAIL: Ambiguidade detectada?]
     │
     └──> invoke @debate ──> decisão ──> continua
```

---

## Estados do Workflow

### Estado 1: TATEANTE (Transitório)

**Meta**: Derrubar hipóteses erradas rápido.

**Artefatos**:
- `eda/<estudo>/scratchpad.sql` — Queries exploratórias
- `eda/<estudo>/README.md` — Incertezas e perguntas abertas
- `_scratch/` — CSVs/PNGs temporários (gitignored)

**Ações permitidas**:
- Executar queries no Snowflake
- Iterar filtros/segmentações
- Testar hipóteses
- Registrar incertezas no README

**Ferramentas disponíveis**:
- `@investigate-entity` — Para profiling de entidades desconhecidas
- Snowflake connection — Para queries ad-hoc

**Transições de saída**:

| Condição | Próximo Estado |
|----------|----------------|
| Achado vai ser reutilizado | → CALIBRAR |
| Achado virou afirmação estável | → CALIBRAR |
| Hipótese invalidada | → (loop em TATEANTE) |
| **Ambiguidade detectada** | → **invoke @debate** |

---

### Estado 2: CALIBRAR (Semântica e Invariantes)

**Meta**: Transformar achados em afirmações estáveis e rastreáveis.

**Artefatos**:
- `queries/audit/<dominio>/` — Microtests e validações
- `docs/reference/<ENTIDADE>.md` — Semântica de entidade

**Ações permitidas**:
- Criar microtests
- Documentar semântica de entidade
- Validar invariantes no Snowflake

**Ferramentas disponíveis**:
- `@investigate-entity` — Para documentação formal
- `@validate-*-axioms` — Para validar microtests
- `@formalize-*-finding` — Para promoção de artefatos

**Transições de saída**:

| Condição | Próximo Estado |
|----------|----------------|
| Semântica documentada | → ESTÁVEL |
| Microtest criado e passando | → ESTÁVEL |
| Precisa mais investigação | → TATEANTE (rollback) |
| **Ambiguidade em semântica** | → **invoke @debate** |

---

### Estado 3: ESTÁVEL (Consumo Repetível)

**Meta**: Produzir "produto analítico" consumível sem ambiguidade.

**Artefatos**:
- `queries/studies/<estudo>/` — Queries BI-safe, reexecutáveis
- `eda/<estudo>/*CONTRATO*.md` — Contrato de saída
- `eda/<estudo>/DECISION_TREE.md` — Árvore de decisões

**Ações permitidas**:
- Finalizar contratos
- Publicar queries de consumo
- Documentar limitações e caveats

**Ferramentas disponíveis**:
- `@validate-saas-contracts` — Para validar contratos
- `@formalize-*-finding` — Para promoção final

**Transições de saída**:

| Condição | Próximo Estado |
|----------|----------------|
| Novo ciclo de análise necessário | → TATEANTE |
| EDA concluído | → END |

---

## Guardrails: Regra de Incerteza

**⚠️ CRÍTICO**: Se surgir ambiguidade que pode mudar **qualquer** item abaixo, **PARAR** e invocar `@debate`:

| Tipo de Ambiguidade | Exemplo | Ação |
|---------------------|---------|------|
| **População/Universo** | "Incluo clinics canceladas?" | `@debate`: definir quem entra/sai |
| **Âncora temporal** | "Mês parcial conta?" | `@debate`: definir janela |
| **Definição de "ativo"** | "Por login ou orçamento?" | `@debate`: definir métrica |
| **Classes/Buckets** | "Top 10% por volume ou valor?" | `@debate`: definir eixos |
| **Semântica de timestamp** | "`created_at` é evento ou cadastro?" | `@debate` + `@investigate-entity` |
| **"no mês" vs "ever"** | "Teve orçamento no mês ou alguma vez?" | `@debate`: definir escopo temporal |

**Anti-pattern**: Assumir e seguir "para ver no que dá" quando isso muda contagens/interpretação.

**Formato de invocação do debate**:
```markdown
@debate

**Ambiguidade detectada**: [descrição]
**Impacto se errado**: [o que muda se a premissa estiver errada]
**Opções identificadas**: A, B, C...
```

---

## Ritual Mínimo (Passo a Passo)

### Passo 1: Definir Universo

**Antes de qualquer análise**, responda:

```markdown
## Universo da Análise

**Quem entra**: [critérios de inclusão]
**Quem sai**: [critérios de exclusão]
**Justificativa**: [por que esses critérios]
```

**Se ambíguo**: invoke `@debate`

---

### Passo 2: Definir Período e Âncora

```markdown
## Período e Âncora

**Período**: [data início] a [data fim]
**Âncora temporal**: [qual timestamp define "no período"]
**Tratamento de mês parcial**: [inclui/exclui/pro-rata]
```

**Cuidado com**:
- Meses parciais (ex: análise em 15/jan inclui janeiro?)
- Timezone (normalizar para BRT)
- `created_at` vs `updated_at` vs `event_date`

---

### Passo 3: Definir Eixos e Classes Provisórias

```markdown
## Eixos de Análise (Provisórios)

| Eixo | Definição | Classes |
|------|-----------|---------|
| Tamanho | volume de orçamentos/mês | small (<10), medium (10-50), large (>50) |
| Região | UF da clínica | SP, RJ, MG, outros |
| ... | ... | ... |
```

**Objetivo**: Descobrir onde a classificação **quebra** (outliers, edge cases).

---

### Passo 4: Executar Snowflake-First

```sql
-- Sempre validar no Snowflake antes de sintetizar
-- NÃO assumir que coluna existe ou tem valor esperado

-- 1. Verificar schema
DESCRIBE TABLE <tabela>;

-- 2. Sample dos dados
SELECT * FROM <tabela> LIMIT 5;

-- 3. Distribuições básicas
SELECT <eixo>, COUNT(*) FROM <tabela> GROUP BY 1 ORDER BY 2 DESC;

-- 4. Verificar nulls e edge cases
SELECT COUNT(*) as total, COUNT(<campo>) as non_null FROM <tabela>;
```

**Invoke `@investigate-entity`** se entidade é desconhecida.

---

## Critérios de Promoção (Anti-Inchaço)

### Quando Promover

✅ **Promova** quando:
- Vai ser reutilizado (reexecutado por você/outros)
- Virou argumento/afirmação estável no estudo

### Quando NÃO Promover

❌ **Não promova** quando:
- É variação temporária de filtro/segmentação ("só para ver")
- É tentativa intermediária sem valor reexecutável
- Hipótese ainda não validada

### Destinos de Promoção

| Tipo de Achado | Destino |
|----------------|---------|
| Validação/guardrail | `queries/audit/<dominio>/` |
| Análise de consumo | `queries/studies/<estudo>/` |
| Semântica de entidade | `docs/reference/<ENTIDADE>.md` |
| Decisão estrutural | `docs/adr/` |
| Contrato de estudo | `eda/<estudo>/*CONTRATO*.md` |

**Invoke `@formalize-*-finding`** para processo de promoção completo.

---

## Registro de Incertezas

Durante fase TATEANTE, manter no `eda/<estudo>/README.md`:

```markdown
## Incertezas / Perguntas Abertas

| # | Incerteza | Impacto se Falso | Status |
|---|-----------|------------------|--------|
| 1 | "Clínica ativa" = teve orçamento no mês? | Muda N de 5k para 3k | 🔄 Em debate |
| 2 | settlement_date é confiável para X? | Invalida métrica Y | ✅ Resolvido (ver ADR-005) |
```

**Só promova para artefato "core"** quando incerteza virar:
- Invariante verificável (microtest) e/ou
- Mudança de semântica/contrato (doc reference + ADR)

---

## Composição com Outras Skills

### Durante TATEANTE

| Situação | Skill a Invocar |
|----------|-----------------|
| Entidade desconhecida | `@investigate-entity` |
| Ambiguidade detectada | `@debate` |
| Precisa validar axioma | `@validate-*-axioms` |

### Durante CALIBRAR

| Situação | Skill a Invocar |
|----------|-----------------|
| Documentar semântica | `@investigate-entity` (modo doc) |
| Criar microtest | `@validate-*-axioms` |
| Promover achado | `@formalize-*-finding` |

### Durante ESTÁVEL

| Situação | Skill a Invocar |
|----------|-----------------|
| Validar contrato | `@validate-saas-contracts` |
| Finalizar promoção | `@formalize-*-finding` |

---

## Anti-Patterns

❌ **Não faça**:
- Assumir semântica sem validar no Snowflake
- Pular definição de universo/período
- Promover query "para ver se usa depois"
- Continuar quando há ambiguidade não resolvida
- Commitar CSVs/PNGs temporários

✅ **Faça**:
- Snowflake-first sempre
- Registrar incertezas explicitamente
- Invocar @debate quando ambíguo
- Promover apenas o que será reutilizado
- Usar `_scratch/` para artefatos temporários

---

## Domain Extensions

Para patterns específicos de cada domínio, consulte:

- **SAAS**: `references/eda_saas.md` — Estrutura `eda/<estudo>/`, CLI específico
- **FINTECH**: `references/eda_fintech.md` — Bridges como foco, thresholds
- **CLIENT_VOICE**: `references/eda_client_voice.md` — Tickets, sentiment

---

## Exemplo de Fluxo Completo

```
User: Quero analisar o churn de clínicas nos últimos 6 meses

Agent: [invoca @eda-workflow]

=== ESTADO: TATEANTE ===

1. Definir universo:
   - Quem entra: clínicas com subscription ativa em algum momento nos 6 meses
   - Quem sai: clínicas de teste, clínicas internas
   
   ⚠️ Ambiguidade: "subscription ativa" = status='active' ou teve pagamento?
   
   [invoca @debate]
   → Decisão: status='active' OR status='past_due' (incluir inadimplentes)
   
2. Definir período: 2025-08-01 a 2026-01-31
   - Âncora: subscription.cancelled_at para churn
   
3. Eixos provisórios:
   - Tamanho: por volume de orçamentos
   - Tempo de vida: meses desde onboarding
   
4. Executar Snowflake-first:
   [queries no scratchpad.sql]
   
   Achado: 15% das clínicas não têm cancelled_at preenchido
   
   [invoca @investigate-entity SUBSCRIPTION_CANCELLATION_REQUESTS]

=== TRANSIÇÃO: TATEANTE → CALIBRAR ===

Achado estável: "cancelled_at é confiável apenas para cancellations após 2024-03"

5. Criar microtest:
   [invoca @formalize-saas-finding tipo B]
   → queries/audit/saas/audit_cancelled_at_reliability.sql

6. Documentar semântica:
   → docs/reference/SUBSCRIPTION_CANCELLATION_REQUESTS.md atualizado

=== TRANSIÇÃO: CALIBRAR → ESTÁVEL ===

7. Criar queries de consumo:
   → queries/studies/churn_2025h2/churn_by_tenure.sql
   
8. Criar contrato:
   → eda/churn_2025h2/CHURN_CONTRATO.md
   
=== ESTADO: END ===

EDA concluído. Artefatos prontos para consumo.
```

---

## Referências

- **Base**: `docs/how_to/EDA_PLAYBOOK.md`, `docs/how_to/PROGRESSIVE_FORMALIZATION.md`
- **Patterns**: OpenAI Agents Guide (2025), DatawiseAgent FST (EMNLP 2025)
- **Skills relacionadas**: `@investigate-entity`, `@debate`, `@formalize-*-finding`
- **Rules**: `.cursor/rules/snowflake_data.mdc` (Zero Assumptions)
