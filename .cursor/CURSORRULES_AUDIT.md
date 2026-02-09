# Cursorrules Audit - Common Sections Analysis

> **Purpose**: Identify common sections across project cursorrules to extract global rules
> **Date**: 2026-02-03

---

## Projects Analyzed

1. [`bnpl-funil/.cursorrules`](c:\Users\pedro.possani_capim\bnpl-funil\.cursorrules) - 81 lines
2. [`ontologia-cf/.cursorrules`](c:\Users\pedro.possani_capim\ontologia-cf\.cursorrules) - 103 lines
3. [`capim-meta-ontology/.cursorrules`](c:\Users\pedro.possani_capim\capim-meta-ontology\.cursorrules) - 31 lines (current, references `.agent/`)

---

## Common Sections Identified

### 1. Language & Communication (IDENTICAL)

**bnpl-funil**:
```markdown
## 1. Comportamento e Comunicação
- **Idioma:** Sempre responda em **Português**.
```

**ontologia-cf**:
```markdown
## 1) Regras globais (sempre)
- Responda sempre em **Português (pt-BR)**.
```

**Verdict**: ✅ **EXTRACT TO GLOBAL**
- Both enforce Portuguese language
- Should be in global cursorrules

---

### 2. Snowflake Access & Protocol (NEARLY IDENTICAL)

**bnpl-funil**:
```markdown
- **Contexto:** Você está operando em um ambiente **AI-first** com acesso direto ao banco de dados Snowflake.
- **Acesso ao Snowflake:**
  - Você TEM permissão e CAPACIDADE para executar SQL.
  - Para executar DDL/Views (CREATE/UPDATE): use `python outputs/execute_sql_view.py <arquivo.sql>`.
  - Para executar Auditorias/Investigação (SELECT com retorno): use `python outputs/run_audit_query.py <arquivo.sql>`.
  - **Nunca** assuma que não pode acessar os dados; se precisar investigar, crie uma query e execute.
```

**ontologia-cf**:
```markdown
## 2) Execução e método (Snowflake-first + EDA-first)
- **Snowflake-first (execução)**:
  - Você **pode e deve** executar queries diretamente no **Snowflake** para validar hipóteses (Worksheet ou conexão local, ex.: `src/utils/snowflake_connection.py`).
  - Prefira validar hipóteses "onde os dados estão" (Snowflake) em vez de reimplementar lógica em Python.
```

**Verdict**: ✅ **EXTRACT TO GLOBAL** (with parameters)
- Core principle: Snowflake-first
- Implementation details vary by project (runners differ)
- Global: Protocol reference to `.cursor/rules/snowflake_data.mdc`
- Local: Specific runners (execute_sql_view.py vs run_scratchpad_block)

---

### 3. Windows/PowerShell Best Practices (IDENTICAL)

**bnpl-funil** (not present explicitly)

**ontologia-cf**:
```markdown
- **Runner único (evitar `python -c`)**:
  - Em Windows/PowerShell, **evite** `python -c "..."` com scripts longos (aspas/`\n`/escape quebram fácil).
  - Para rodar blocos de um scratchpad, prefira o runner versionado
- **Windows/PowerShell**:
  - Evite `&&` no terminal; use `;` para encadear comandos.
```

**Verdict**: ✅ **EXTRACT TO GLOBAL**
- Applies to all Python projects on Windows
- Should be in global cursorrules

---

### 4. Visualization Standards (NEARLY IDENTICAL)

**bnpl-funil**:
```markdown
## 6. Diretrizes para gráficos (Seaborn/Matplotlib) — padrão do repositório:
- Objetivo: gráficos **legíveis**, **sem sobreposição**, com **mensagem clara** e **rastreabilidade** (período/fonte).

Padrão visual (tema):
- Use `seaborn.set_theme(style="whitegrid", context="talk", palette="pastel")`.
- Ajustes recomendados em `rc`: `grid.alpha≈0.25`, `axes.edgecolor="0.85"`, `axes.linewidth=1.0`, `xtick.color/ytick.color="0.25"`.

[... 27 more lines of detailed chart rules]
```

**ontologia-cf**:
```markdown
## 4) Diretrizes para gráficos (Seaborn/Matplotlib) — padrão do repositório
- Objetivo: gráficos **legíveis**, **sem sobreposição**, com **mensagem clara** e **rastreabilidade** (período/fonte).

[... IDENTICAL content for ~30 lines]
```

**Verdict**: ✅ **EXTRACT TO SEPARATE DOC** → `docs/VISUALIZATION_STANDARDS.md`
- Completely duplicated (30+ lines)
- Should be centralized and referenced
- Both cursorrules link to shared doc

---

### 5. Project Structure & File Hygiene (DOMAIN-SPECIFIC)

**bnpl-funil**:
```markdown
## 2. Mapa do Código (Estrutura)
- `queries/enrich/`: Lógica de transformação e enriquecimento (ETL pesado).
- `queries/views/`: Views de consumo final (analytics/reporting).
- `queries/audit/`: Queries de investigação, sanidade e inventory.
- `docs/`: Fonte da verdade de negócio. LEIA antes de perguntar.
```

**ontologia-cf**:
```markdown
[Similar but different paths - eda/, queries/audit/, etc.]
```

**Verdict**: ❌ **KEEP LOCAL**
- Project-specific structure
- Different folder conventions

---

### 6. Entity Investigation Protocol (DOMAIN-SPECIFIC)

**bnpl-funil**:
```markdown
[Not present]
```

**ontologia-cf**:
```markdown
## 3) "Se informar" sobre uma entidade (não inferir sem ler)
- Objetivo: maximizar **assertividade** e **rastreabilidade** (canônico vs derivado).
- Protocolo padrão (ordem de leitura/checagem):
  - **1) `docs/reference/<ENTIDADE>.md` (se existir)**
  - **2) `queries/origin/*<entidade>*`**
  - **3) `queries/views/**`**
  - **4) `queries/audit/**`**
  - **5) Busca ampla no repo**
```

**Verdict**: ⚠️ **GENERALIZE & EXTRACT**
- Principle applies to all ontology projects
- Specific paths vary
- Extract protocol, parameterize paths

---

### 7. Business Rules (DOMAIN-SPECIFIC)

**bnpl-funil**:
```markdown
## 4. Regras de Negócio (Mandatórias)
- **C1 (Simulação):** Entidade `credit_simulation` (novo) ou `pre_analysis` (legado).
- **C2 (Pedido):** Entidade `request`.
- **Risk Score:** Campo `SCORE` em `CREDIT_SIMULATIONS` é TEXT (ex: '9,00').
```

**ontologia-cf**:
```markdown
[Not present - has different business rules related to SAAS]
```

**Verdict**: ❌ **KEEP LOCAL**
- Completely domain-specific
- No overlap

---

### 8. Prompt Engineering (DOMAIN-SPECIFIC)

**ontologia-cf ONLY**:
```markdown
## 5) Como escrever prompts
- Use o formato **TC‑EBC** (Task, Context, Elements/Behavior, Constraints)
- Prefira **prompts curtos** para iteração
- Evite termos internos como **"ontologia"** visíveis na UI
```

**Verdict**: ⚠️ **POTENTIALLY EXTRACT**
- Useful globally for UI/UX projects
- But very specific to ontologia-cf's Figma Make workflow
- **Decision**: Keep local for now, extract if other projects need

---

## Summary: Extraction Map

### To Global Cursorrules

| Section | Source | Lines | Priority |
|---------|--------|-------|----------|
| **Language (PT-BR)** | Both | ~2 | HIGH |
| **Snowflake-first protocol** | Both | ~5 | HIGH |
| **Windows/PowerShell tips** | ontologia-cf | ~5 | HIGH |
| **Entity investigation protocol** | ontologia-cf | ~10 | MEDIUM |

### To Shared Documentation

| Document | Content | Source | Lines |
|----------|---------|--------|-------|
| **VISUALIZATION_STANDARDS.md** | Seaborn/Matplotlib guidelines | Both (duplicated) | ~30 |

### Keep in Local Cursorrules

| Section | Project | Reason |
|---------|---------|--------|
| **Project structure map** | Both | Different folder conventions |
| **Business rules** | Both | Domain-specific |
| **SQL conventions** | Both | Some overlap, but domain nuances |
| **Prompt engineering** | ontologia-cf | Figma Make specific |
| **File hygiene** | bnpl-funil | Project-specific cleanup rules |
| **EDA protocols** | ontologia-cf | SAAS-specific investigation flow |

---

## Recommended Global Structure

```markdown
# CAPIM ECOSYSTEM - CURSOR ROOT RULES (GLOBAL)

## Language & Communication
- **Language**: Always respond in **Portuguese (pt-BR)**
- **Context**: AI-first environment with direct Snowflake access

## Core Protocols

### 1. Cursor Skills & Rules System
- Reference: `.cursor/skills/README.md`
- Reference: `.cursor/rules/memory_governance.mdc`
- Reference: `.cursor/rules/snowflake_data.mdc`  
- Reference: `.cursor/rules/ontology_reasoning.mdc`

### 2. Snowflake-First Protocol
- **Applied via**: `.cursor/rules/snowflake_data.mdc`
- **Key Principle**: Validate WHERE THE DATA LIVES
- **Connection**: Use `snowflake_connection.py` utility (never direct connector)

### 3. Windows/PowerShell Best Practices
- **Avoid**: `python -c` with long scripts (escaping issues)
- **Chain commands**: Use `;` not `&&`
- **Encoding**: Be careful with Portuguese accents in paths

### 4. Visualization Standards
- **Reference**: `docs/VISUALIZATION_STANDARDS.md`
- **Theme**: Seaborn whitegrid, talk, pastel
- **Key Rule**: No overlapping legends, always include period/source

### 5. Entity Investigation Protocol
When documenting entities:
1. Check `docs/reference/<ENTITY>.md` (if exists)
2. Read `queries/origin/*<entity>*` (canonical source)
3. Review `queries/views/**` (if applicable)
4. Check `queries/audit/**` (validations done)
5. Broad search only if above not sufficient

**Never infer semantics without reading documentation first**

## Project-Specific Rules

Each project EXTENDS these rules in its own `.cursorrules`:
- `bnpl-funil/.cursorrules` — FINTECH domain rules
- `ontologia-cf/.cursorrules` — SAAS domain rules
- `client-voice-data/.cursorrules` — CLIENT_VOICE data rules
- `client-voice-app/.cursorrules` — CLIENT_VOICE frontend rules
```

---

## Action Items

1. ✅ Create global cursorrules with sections above
2. ✅ Extract VISUALIZATION_STANDARDS.md to docs/
3. ✅ Refactor bnpl-funil/.cursorrules (remove duplicates, add reference)
4. ✅ Refactor ontologia-cf/.cursorrules (remove duplicates, add reference)
5. ✅ Create client-voice-data/.cursorrules (new)
6. ✅ Create client-voice-app/.cursorrules (new)
