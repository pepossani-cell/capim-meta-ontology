---
name: Materialize View
description: Materialize views to tables with validation, scheduling, and incremental support. Use when (1) view performance is slow, (2) need to snapshot data for historical analysis, (3) creating aggregated tables for BI/reporting, (4) downstream processes require table instead of view, (5) user mentions "materializar", "criar tabela", "snapshot", "incremental load". Generic workflow for all domains.
version: 1.0
auto_invoke: ask_first
composes: [investigate-entity, validate-axioms]
used_by: [saas, fintech, client_voice]
---

# Materialize View Skill

Workflow genérico para materialização de views em tabelas no Snowflake, com validação, scheduling e suporte a incremental loads.

## Quando Usar

Invoque esta skill quando:
- View está lenta (muitos JOINs, agregações complexas)
- Precisa de snapshot histórico (dados mudam e quer preservar estado)
- Criando tabelas agregadas para BI/reporting
- Processo downstream requer tabela (não suporta view)
- Migração de view para tabela materializada

**Invocação**: `@materialize-view` ou menção natural ("materializar view", "criar tabela de...")

---

## Decisão: Materializar ou Não?

### Quando Materializar ✅

| Cenário | Justificativa |
|---------|---------------|
| Query time > 30s | Performance inaceitável para uso interativo |
| View usada por múltiplos consumers | Compute duplicado desnecessário |
| Precisa de histórico | View só mostra estado atual |
| BI tool não suporta views complexas | Limitação técnica |
| Agregações pesadas | Pré-computar economiza resources |

### Quando NÃO Materializar ❌

| Cenário | Alternativa |
|---------|-------------|
| Query time < 5s | View é suficiente |
| Dados mudam frequentemente | Manter view, aceitar refresh |
| Uso ocasional (< 1x/dia) | View on-demand é ok |
| Precisa de dados real-time | View é melhor |

**Se em dúvida**: invoke `@debate` para decidir.

---

## Tipos de Materialização

### 1. Full Refresh (CTAS)

```sql
-- Mais simples, reconstrói toda a tabela
CREATE OR REPLACE TABLE <schema>.<tabela_mat>
AS SELECT * FROM <schema>.<view>;
```

**Usar quando**:
- Volume pequeno (< 1M rows)
- Não precisa de histórico incremental
- Dados fonte são imutáveis ou substituíveis

---

### 2. Incremental (MERGE)

```sql
-- Mais eficiente, atualiza apenas delta
MERGE INTO <schema>.<tabela_mat> AS target
USING (
    SELECT * FROM <schema>.<view>
    WHERE updated_at >= DATEADD(day, -1, CURRENT_DATE)
) AS source
ON target.<pk> = source.<pk>
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

**Usar quando**:
- Volume grande (> 1M rows)
- Dados têm `updated_at` ou `created_at` confiável
- Precisa de eficiência em refresh diário

---

### 3. Snapshot Histórico

```sql
-- Preserva estado em cada snapshot
INSERT INTO <schema>.<tabela_snapshots>
SELECT 
    CURRENT_TIMESTAMP AS snapshot_at,
    *
FROM <schema>.<view>;
```

**Usar quando**:
- Precisa de time-travel analítico
- Dados mudam e quer preservar estados anteriores
- Análises de cohort/evolução temporal

---

## Workflow de Materialização

### Passo 1: Avaliar View Candidata

```sql
-- Verificar complexidade
DESCRIBE VIEW <schema>.<view>;

-- Testar performance atual
SELECT COUNT(*) FROM <schema>.<view>;
-- Anotar: tempo de execução, rows retornadas

-- Verificar dependências
SELECT * FROM INFORMATION_SCHEMA.VIEW_TABLE_USAGE
WHERE VIEW_NAME = '<view>';
```

**Invoke `@investigate-entity`** se view é desconhecida.

---

### Passo 2: Definir Estratégia

| Pergunta | Impacto na Estratégia |
|----------|----------------------|
| Volume da view? | < 1M = CTAS; > 1M = MERGE |
| Tem PK clara? | Sim = MERGE possível; Não = CTAS only |
| Tem timestamp confiável? | Sim = incremental; Não = full refresh |
| Precisa de histórico? | Sim = snapshot; Não = CTAS/MERGE |
| Frequência de refresh? | Alta = incremental; Baixa = CTAS |

**Se estratégia não clara**: invoke `@debate`.

---

### Passo 3: Criar Tabela Materializada

#### Nomenclatura

```
<schema>.<view_name>_MAT_V<version>

Exemplos:
- C1_ENRICHED_BORROWER_V1 → C1_ENRICHED_BORROWER_MAT_V1
- CLINIC_DIM_V1 → CLINIC_DIM_MAT_V1
```

#### DDL Template (CTAS)

```sql
-- queries/materialize/<dominio>/materialize_<view_name>.sql

/*
=============================================================================
MATERIALIZATION: <view_name>
=============================================================================
Source View: <schema>.<view_name>
Target Table: <schema>.<view_name>_MAT_V1
Strategy: CTAS (Full Refresh)
Schedule: [Daily/Weekly/On-demand]
Owner: <team>
Created: <date>
=============================================================================
*/

CREATE OR REPLACE TABLE <schema>.<view_name>_MAT_V1
CLUSTER BY (<cluster_keys>)  -- opcional, para performance
AS 
SELECT 
    CURRENT_TIMESTAMP AS materialized_at,
    *
FROM <schema>.<view_name>;

-- Validação pós-materialização
SELECT 
    (SELECT COUNT(*) FROM <schema>.<view_name>) AS view_count,
    (SELECT COUNT(*) FROM <schema>.<view_name>_MAT_V1) AS mat_count,
    CASE 
        WHEN view_count = mat_count THEN 'OK'
        ELSE 'DIVERGENCE'
    END AS validation_status;
```

---

### Passo 4: Validar Materialização

```sql
-- 1. Contagem deve bater
SELECT 
    'view' AS source, COUNT(*) AS n FROM <view>
UNION ALL
SELECT 
    'mat' AS source, COUNT(*) AS n FROM <view>_MAT_V1;

-- 2. Sample de registros deve bater (PK)
SELECT v.*, m.*
FROM <view> v
FULL OUTER JOIN <view>_MAT_V1 m ON v.<pk> = m.<pk>
WHERE v.<pk> IS NULL OR m.<pk> IS NULL
LIMIT 10;

-- 3. Agregações devem bater
SELECT 
    'view' AS source, SUM(<metric>) AS total FROM <view>
UNION ALL
SELECT 
    'mat' AS source, SUM(<metric>) AS total FROM <view>_MAT_V1;
```

**Invoke `@validate-axioms`** para validar invariantes pós-materialização.

---

### Passo 5: Configurar Refresh

#### Opção A: Task Snowflake

```sql
CREATE OR REPLACE TASK <schema>.task_refresh_<view_name>_mat
    WAREHOUSE = <warehouse>
    SCHEDULE = 'USING CRON 0 6 * * * America/Sao_Paulo'  -- 6h BRT diário
AS
    CREATE OR REPLACE TABLE <schema>.<view_name>_MAT_V1
    AS SELECT CURRENT_TIMESTAMP AS materialized_at, * FROM <schema>.<view_name>;

-- Ativar task
ALTER TASK <schema>.task_refresh_<view_name>_mat RESUME;
```

#### Opção B: Script Python + Scheduler

```python
# scripts/materialize/<view_name>.py
from src.utils.snowflake_connection import run_query

def materialize_view():
    query = open('queries/materialize/<dominio>/materialize_<view>.sql').read()
    run_query(query)
    
    # Validação
    validation = run_query("""
        SELECT COUNT(*) as view_n FROM <view>
        UNION ALL
        SELECT COUNT(*) as mat_n FROM <view>_MAT_V1
    """)
    assert validation.iloc[0]['view_n'] == validation.iloc[1]['mat_n']

if __name__ == '__main__':
    materialize_view()
```

---

### Passo 6: Documentar

Criar/atualizar `docs/reference/<VIEW_NAME>_MAT.md`:

```markdown
# <VIEW_NAME>_MAT_V1

## Overview

Tabela materializada da view `<VIEW_NAME>`.

## Metadados

| Campo | Valor |
|-------|-------|
| Source View | `<schema>.<view_name>` |
| Target Table | `<schema>.<view_name>_MAT_V1` |
| Strategy | CTAS / MERGE / Snapshot |
| Schedule | Daily 6h BRT / On-demand |
| Owner | <team> |
| Created | <date> |

## Schema Adicional

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `materialized_at` | TIMESTAMP_NTZ | Momento da materialização |

## Validações

- [ ] Contagem view = contagem mat
- [ ] PKs sem divergência
- [ ] Métricas agregadas batem

## Caveats

- [listar limitações conhecidas]
```

---

## Checklist de Materialização

```markdown
## Pre-Materialization

- [ ] View identificada e testada
- [ ] Performance baseline medido
- [ ] Estratégia definida (CTAS/MERGE/Snapshot)
- [ ] PK identificada (se MERGE)
- [ ] Timestamp identificado (se incremental)

## Materialization

- [ ] DDL criado em queries/materialize/
- [ ] Tabela criada no Snowflake
- [ ] Validação executada (contagem, sample, agregações)

## Post-Materialization

- [ ] Refresh configurado (Task ou script)
- [ ] Documentação criada/atualizada
- [ ] Consumers notificados (se substituindo view)
```

---

## Domain Extensions

Para patterns específicos de cada domínio:

- **SAAS**: `references/materialize_saas.md` — Clinic dim, budget aggregates
- **FINTECH**: `references/materialize_fintech.md` — Credit simulations enriched, bridges
- **CLIENT_VOICE**: `references/materialize_client_voice.md` — Ticket aggregates

---

## Anti-Patterns

❌ **Não faça**:
- Materializar sem medir performance baseline
- Criar tabela sem documentar schedule de refresh
- Usar MERGE sem PK clara
- Materializar view que muda frequentemente sem justificativa
- Esquecer de validar pós-materialização

✅ **Faça**:
- Medir antes e depois
- Documentar estratégia e schedule
- Validar sempre após refresh
- Notificar consumers de mudanças
- Usar naming convention consistente

---

## Exemplo Completo

```sql
/*
=============================================================================
MATERIALIZATION: C1_ENRICHED_BORROWER_V1
=============================================================================
Source View: CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_V1
Target Table: CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_MAT_V1
Strategy: CTAS (Full Refresh)
Schedule: Daily 6h BRT
Owner: fintech-team
Created: 2026-02-04
=============================================================================
*/

-- Step 1: Criar tabela materializada
CREATE OR REPLACE TABLE CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_MAT_V1
CLUSTER BY (clinic_id, simulation_month)
AS 
SELECT 
    CURRENT_TIMESTAMP AS materialized_at,
    *
FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_V1;

-- Step 2: Validar
SELECT 
    (SELECT COUNT(*) FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_V1) AS view_count,
    (SELECT COUNT(*) FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_MAT_V1) AS mat_count;

-- Step 3: Criar task de refresh
CREATE OR REPLACE TASK CAPIM_DATA_DEV.POSSANI_SANDBOX.task_refresh_c1_enriched_borrower_mat
    WAREHOUSE = COMPUTE_WH
    SCHEDULE = 'USING CRON 0 6 * * * America/Sao_Paulo'
AS
    CREATE OR REPLACE TABLE CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_MAT_V1
    CLUSTER BY (clinic_id, simulation_month)
    AS SELECT CURRENT_TIMESTAMP AS materialized_at, * 
    FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.C1_ENRICHED_BORROWER_V1;

ALTER TASK CAPIM_DATA_DEV.POSSANI_SANDBOX.task_refresh_c1_enriched_borrower_mat RESUME;
```

---

## Referências

- Snowflake Tasks Documentation
- `@investigate-entity` skill (para profiling)
- `@validate-axioms` skill (para validação)
- `docs/runbooks/EXECUTION_IN_SNOWFLAKE.md`
