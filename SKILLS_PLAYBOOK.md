# SKILLS PLAYBOOK — Capim Ecosystem

> **Purpose**: Lightweight guide for creating and maintaining skills in the Capim workspace  
> **Audience**: AI agents and human contributors  
> **Last Updated**: 2026-02-04  
> **Reference**: Based on Anthropic's `SKILL_CREATOR.md` with Capim-specific adaptations

---

## 📖 What are Skills?

**Skills** são módulos autocontidos que estendem as capacidades do agente com workflows especializados, conhecimento de domínio, e integração de ferramentas.

**Diferença chave**:
- **Skill** = Workflow interativo e multi-step (ex: "como fazer EDA", "como debater decisões")
- **Rule** = Enforcement automático baseado em globs (ex: "sempre use Snowflake-first", "sempre atualize DECISIONS_IN_PROGRESS atomicamente")

---

## 🎯 Quando Criar uma Skill?

✅ **Crie uma skill quando**:
- É um **workflow multi-step** que requer decisões ou debates
- É **reutilizável** em múltiplos projetos do workspace
- Tem **decision points** ou **conditional logic**
- Beneficia de **progressive disclosure** (core workflow + references opcionais)
- Precisa de **scripts executáveis** ou **assets bundled**

❌ **Use uma rule quando**:
- É um **enforcement de convenção** (ex: naming, estrutura de pastas)
- Aplica **automaticamente** baseado em globs de arquivo (ex: `**/*.sql`, `**/*.py`)
- É uma **constraint** ou **protocol** que deve sempre ser seguido
- Não requer interação ou decisão do usuário

**Exemplos**:
- ✅ Skill: `@investigate-entity` (workflow interativo com debate)
- ❌ Rule: `snowflake_data.mdc` (enforcement de Zero Assumptions protocol)
- ✅ Skill: `@debate` (decision-making estruturado)
- ❌ Rule: `entity_documentation.mdc` (Dual Documentation Pattern enforcement)

---

## 📂 Anatomia de uma Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, version, auto_invoke)
│   └── Markdown body (workflow, passos, exemplos)
└── Bundled Resources (optional)
    ├── scripts/          - Código executável (Python/Bash)
    ├── references/       - Docs de referência carregados sob demanda
    └── assets/           - Templates, imagens, boilerplate
```

**Critical**: SKILL.md deve ser < 500 linhas. Se exceder, split em `references/`.

---

## 📝 YAML Frontmatter (Required Fields)

```yaml
---
name: Skill Name
description: Complete description including WHEN TO USE with explicit triggers. This is the primary discovery mechanism.
version: 2.0
auto_invoke: silent | ask_first | explicit_only
migrated_from: .agent/workflows/original.md  # (optional)
---
```

### Campo `description` (CRITICAL)

**Deve incluir**:
1. **O que faz** (1 frase)
2. **Quando usar** (5-7 triggers explícitos)
3. **Outputs/side-effects** (se aplicável)

**Exemplo ruim** (vago):
```yaml
description: Structured decision-making for complex topics
```

**Exemplo bom** (triggers explícitos):
```yaml
description: Structured decision-making for complex topics with multiple options. Use when (1) user asks "what do you think about X vs Y?", (2) topic has 2+ viable options with trade-offs, (3) decision affects multiple files or systems, (4) user seems uncertain about direction, (5) agent identifies multiple valid approaches, (6) ambiguity is detected that requires explicit decision. Updates DECISIONS_IN_PROGRESS.md atomically after each confirmed decision.
```

### Campo `auto_invoke` (NEW)

Define como a skill é invocada:

| Valor | Comportamento | Quando Usar |
|-------|--------------|-------------|
| **silent** | Auto-invoca sem avisar | Read-only, lightweight, setup (ex: `@session-start`, `@validate-axioms`) |
| **ask_first** | Detecta e pergunta "Posso usar @skill-name?" | Write operations, cross-domain queries, token-intensive (ex: `@debate`, `@clinic-health-check`) |
| **explicit_only** | Só roda se usuário invocar `@skill-name` | Operações destrutivas ou muito específicas (use raramente) |

**Default se omitido**: `ask_first` (behavior seguro)

---

## 🌐 Convenção de Idioma (Híbrido EN/PT-BR)

**Princípio**: Estrutura técnica em inglês + conteúdo de negócio em português.

### O Que Vai em Inglês 🇬🇧

| Elemento | Exemplo | Razão |
|----------|---------|-------|
| `name` (YAML) | `Analyze Conversion Funnel` | Discovery por LLM |
| `description` (YAML) | `Use when (1) analyzing...` | Discovery por LLM |
| SQL keywords | `SELECT`, `WHERE`, `GROUP BY` | Padrão universal |
| Python/code | `def calculate_metrics():` | Padrão universal |
| YAML fields | `start_date`, `clinic_id` | Padrão técnico |
| Technical terms | `Snowflake-first`, `progressive disclosure` | Jargão técnico |

### O Que Vai em Português 🇧🇷

| Elemento | Exemplo | Razão |
|----------|---------|-------|
| Section headers | `## Processo de Execução` | Legibilidade do time |
| Step headers | `### Passo 1: Definir Escopo` | Legibilidade |
| Workflow content | `Invoque esta skill quando...` | Contexto brasileiro |
| Business terms | `clínica`, `orçamento`, `simulação de crédito` | Precisão semântica |
| Examples descriptions | `Todas as clínicas ativas com...` | Contexto brasileiro |
| Comments em SQL | `-- Exemplo: B2B only` | Clareza |
| Caveats/Notes | `⚠️ Limitação: dados de POS são snapshot` | Clareza |

### Exemplo de SKILL.md Bem Padronizada

```yaml
---
name: Validate SAAS Contracts  # 🇬🇧 Inglês (discovery)
description: Validate budget/procedure contracts... Use when (1)...  # 🇬🇧 Inglês (discovery)
version: 1.0
auto_invoke: ask_first
---

# Validate SAAS Contracts Skill  # 🇬🇧 Inglês (título principal)

Valida contratos de estudos e especificações...  # 🇧🇷 Português (body)

## Quando Usar  # 🇧🇷 Português (header)

Invoque esta skill quando:  # 🇧🇷 Português (content)
- Documentar novo estudo ou entidade
- Validar outputs de EDA para consumo downstream

## Processo de Execução  # 🇧🇷 Português (header)

### Passo 1: Identificar Tipo de Contrato  # 🇧🇷 Português (header)

```sql
-- Exemplo: verificar grão  # 🇧🇷 Português (comment)
SELECT clinic_id, COUNT(*)  # 🇬🇧 Inglês (SQL)
FROM entity
GROUP BY clinic_id
```
```

### Por Quê Híbrido?

| Aspecto | Impacto | Justificativa |
|---------|---------|---------------|
| **LLM Performance** | Mínimo | Claude/GPT-4 performam bem em PT-BR |
| **Tokenização** | +20-30% tokens | Aceitável dado o contexto |
| **Precisão semântica** | **Melhora** | "orçamento" > "budget" no contexto Capim |
| **Legibilidade do time** | **Melhora** | Time brasileiro lê mais rápido |
| **Descoberta** | Mantém | `name` e `description` em inglês para LLM |

---

## 🏗️ Naming Conventions

**Skill directory**: `kebab-case` (ex: `investigate-entity`, `session-start`)  
**Invocação**: `@skill-name` (ex: `@investigate-entity`, `@session-start`)  
**Rule files**: `snake_case.mdc` (ex: `snowflake_data.mdc`, `memory_governance.mdc`)

**Anti-pattern**: Não usar espaços ou CamelCase em nomes de skills.

---

## 🔀 Progressive Disclosure Pattern

**Princípio**: Context window é um bem público. Minimize token usage.

**3 níveis de carregamento**:
1. **Metadata** (name + description) — sempre no contexto (~100 palavras)
2. **SKILL.md body** — quando skill é triggered (< 500 linhas)
3. **References** — quando agente decide que precisa (sob demanda)

**Quando split em references**:

```
skill-name/
├── SKILL.md (< 500 linhas: core workflow + navigation)
└── references/
    ├── domain_a.md (domain-specific patterns)
    ├── domain_b.md (domain-specific patterns)
    └── advanced_features.md (optional deep dives)
```

**Exemplo**: `investigate-entity` poderia ter:

```
investigate-entity/
├── SKILL.md (workflow principal)
├── scripts/
│   └── investigate.py (profiling script)
└── references/
    ├── AGENTIC_DOC_TEMPLATE.md (template completo)
    └── SEMANTIC_DOC_TEMPLATE.md (template completo)
```

**Link em SKILL.md**:
```markdown
## Advanced: Full Templates

Para templates completos:
- **Agentic doc**: Ver [AGENTIC_DOC_TEMPLATE.md](references/AGENTIC_DOC_TEMPLATE.md)
- **Semantic doc**: Ver [SEMANTIC_DOC_TEMPLATE.md](references/SEMANTIC_DOC_TEMPLATE.md)
```

---

## ✅ Pre-Merge Review Checklist

Antes de commitar uma nova skill ou update:

**Estrutura**:
- [ ] SKILL.md existe e tem frontmatter YAML válido
- [ ] `name` e `description` estão presentes
- [ ] `description` inclui **5+ triggers explícitos**
- [ ] `auto_invoke` está definido (`silent`, `ask_first`, ou `explicit_only`)
- [ ] SKILL.md tem < 500 linhas (se > 500, split em `references/`)

**Conteúdo**:
- [ ] Usa **imperative form** ("Execute", "Validate", não "Executes", "This skill does")
- [ ] Seção "Quando Usar" no body complementa a description
- [ ] Workflow é claro e step-by-step
- [ ] Exemplos concretos estão presentes (quando aplicável)
- [ ] Cross-references para outras skills ou rules (quando aplicável)

**Bundled Resources** (se aplicável):
- [ ] Scripts em `scripts/` foram testados
- [ ] References em `references/` são linkados do SKILL.md
- [ ] Assets em `assets/` são usados no output (não apenas docs)

**Token Efficiency**:
- [ ] Não duplica conteúdo que já existe em rules ou docs
- [ ] Usa references para conteúdo opcional/avançado
- [ ] Description é concisa mas completa

**Integration**:
- [ ] Skill está listada no README ou index apropriado
- [ ] Menciona quais rules enforce ou complementam a skill
- [ ] Documenta outputs/side-effects (ex: "Updates DECISIONS_IN_PROGRESS.md")

---

## 🎓 Capim-Specific Patterns

### Pattern 1: Ontology-Aware Skills

Skills que interagem com ontologia devem:
- Citar **axioms** quando validar constraints (ex: `@validate-axioms`)
- Referenciar **INFERENCE_RULES.yaml** quando aplicar reasoning (ex: `@clinic-health-check`)
- Usar **CAPABILITY_MATRIX.yaml** para routing cross-domain

**Exemplo**:
```markdown
**Implementa**: `ontology/INFERENCE_RULES.yaml` → RULE-CROSS-001 (Clinic Health Diagnostic)
```

### Pattern 2: Snowflake-First Skills

Skills que fazem profiling ou queries devem:
- Sempre usar `src/utils/snowflake_connection.py` (não direct connector)
- Seguir **Zero Assumptions protocol** (nunca assumir schema sem profiling)
- Integrar com rule `snowflake_data.mdc`

**Exemplo**:
```markdown
**⚠️ CRITICAL**: This skill MUST follow Zero Assumptions protocol.
**Reference**: `.cursor/rules/snowflake_data.mdc`
```

---

## 🧪 Validação Snowflake-First (Obrigatória para Skills de Dados)

**Antes de marcar uma skill como `active`**, valide no Snowflake:

### Cenário A: Queries Existem

Se a skill referencia queries já existentes (em `queries/audit/`, `queries/views/`, etc.):

1. **Identificar queries críticas** da skill
2. **Executar no Snowflake** via `src/utils/snowflake_connection.py`
3. **Validar**:
   - Tabelas mencionadas existem
   - Queries retornam dados esperados
   - Exemplos funcionam

```python
from src.utils.snowflake_connection import run_query
df = run_query("SELECT COUNT(*) FROM <tabela_da_skill>")
assert df is not None, "Tabela não existe ou sem permissão"
```

### Cenário B: Queries Precisam Ser Construídas

Se a skill descreve um **workflow de raciocínio** (ex: investigação, correlação, análise exploratória):

1. **Documentar na skill** que o agente precisará construir queries
2. **Referenciar recursos de ontologia** para guiar o raciocínio:
   - `docs/reference/<ENTIDADE>.md` — Semântica e schema
   - `_domain/_docs/ENTITY_INDEX.yaml` — Índice de entidades disponíveis
   - `CAPABILITY_MATRIX.yaml` — O que cada domínio pode responder
3. **Incluir na skill**:
   ```markdown
   ## Construção de Queries
   
   Esta skill requer construção dinâmica de queries. O agente deve:
   1. Consultar documentação semântica em `docs/reference/`
   2. Verificar schema via profiling (`DESCRIBE TABLE`, `LIMIT 5`)
   3. Aplicar Zero Assumptions protocol
   
   **Recursos de ontologia disponíveis**:
   - Entity Index: `_domain/_docs/ENTITY_INDEX.yaml`
   - Capability Matrix: `_federation/CAPABILITY_MATRIX.yaml`
   ```

### Output Temporário

- Use `_scratch/` para CSVs e outputs de teste (gitignored)
- **Nunca commite** artefatos de validação
- Remova `_scratch/` após validação concluída

### Pattern 3: Memory-Aware Skills

Skills que atualizam memória devem:
- Usar **atomic updates** (não batch)
- Referenciar rule `memory_governance.mdc`
- Documentar status markers usados (✅, ⏳, 🔄, ❌)

**Exemplo**:
```markdown
**Integration**: Esta skill complementa o workflow `@session-end`, 
podendo ser usada de forma standalone para manutenção ad-hoc.
**Enforced by**: Rule `memory_governance.mdc`
```

---

## 📚 Reference Skills (Well-Structured Examples)

Use estas skills como referência de boa estrutura:

| Skill | Por Quê É Boa | Destaque |
|-------|--------------|----------|
| **@debate** | Description rica em triggers, workflow estruturado, atomic updates | Decision-making pattern |
| **@investigate-entity** | Dual Documentation Protocol, debate integrado, script bundled | Snowflake-first pattern |
| **@session-start** | Progressive disclosure (metadata → body → domain context), AskQuestion integration | Setup pattern |

---

## 🚫 Anti-Patterns (Avoid These)

❌ **Don't**:
- Criar README.md ou CHANGELOG.md extras na skill folder (só SKILL.md)
- Colocar business logic em rules (rules são enforcement, não workflow)
- Duplicar conteúdo que já existe em docs de referência (link, não copie)
- Criar skills muito específicas de 1 projeto (use how_to docs instead)
- Description vaga sem triggers (ex: "Helps with database tasks")
- SKILL.md > 500 linhas sem split em references

✅ **Do**:
- Manter skills focadas e reutilizáveis
- Usar progressive disclosure para manage context
- Cross-referenciar skills e rules
- Documentar side-effects claramente
- Testar scripts antes de commit

---

## 🔄 Skill Lifecycle

1. **Draft**: Skill proposta mas não testada
2. **Active**: Skill em produção, listada no index
3. **Deprecated**: Skill obsoleta, mantida para referência histórica

**Deprecation process**:
- Adicionar `deprecated: true` no frontmatter
- Mover para `.cursor/skills/_deprecated/`
- Atualizar index com nota de deprecation

---

## 🛠️ Creating a New Skill (Quick Start)

**Via init script** (recomendado):
```bash
cd capim-meta-ontology
python scripts/init_skill.py skill-name --path .cursor/skills/
```

**Manual**:
1. Criar pasta `.cursor/skills/skill-name/`
2. Criar `SKILL.md` com frontmatter YAML
3. (Opcional) Adicionar `scripts/`, `references/`, `assets/`
4. Testar skill com invocação real
5. Executar checklist de review
6. Commit

---

## 📖 External References

- **Anthropic Skill Creator**: `docs/SKILL_CREATOR.md` (original guide)
- **Root cursorrules**: `.cursorrules` (skill invocation protocol)
- **Rule system**: `.cursor/rules/` (complementary to skills)
- **Memory Constitution**: `MEMORY_ARCHITECTURE_CONSTITUTION.md` (memory patterns)

---

**Version**: 1.0  
**Last Updated**: 2026-02-04  
**Contributors**: AI Agent (based on debate and Anthropic guidelines)
