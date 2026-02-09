# Strategy Decision Tree — Materialize View

> **Purpose**: Árvore de decisão para escolher estratégia de materialização

---

## Decision Tree

```
                    [View Candidata]
                          │
                          ▼
                ┌─────────────────────┐
                │ Volume > 1M rows?   │
                └─────────┬───────────┘
                    │           │
                   Não         Sim
                    │           │
                    ▼           ▼
            ┌───────────┐  ┌───────────────────┐
            │ CTAS OK   │  │ Tem PK clara?     │
            └───────────┘  └─────────┬─────────┘
                               │           │
                              Não         Sim
                               │           │
                               ▼           ▼
                       ┌───────────┐  ┌───────────────────┐
                       │ CTAS      │  │ Tem timestamp     │
                       │ (aceitar  │  │ updated_at?       │
                       │ custo)    │  └─────────┬─────────┘
                       └───────────┘        │           │
                                           Não         Sim
                                            │           │
                                            ▼           ▼
                                    ┌───────────┐  ┌───────────┐
                                    │ CTAS      │  │ MERGE     │
                                    │ com       │  │ incremental│
                                    │ clustering│  └───────────┘
                                    └───────────┘
```

---

## Decision Matrix

| Volume | PK Clara | Timestamp | Estratégia Recomendada |
|--------|----------|-----------|------------------------|
| < 1M | - | - | CTAS (simples) |
| > 1M | Não | - | CTAS com clustering |
| > 1M | Sim | Não | CTAS com clustering |
| > 1M | Sim | Sim | MERGE incremental |
| Any | - | - + histórico | Snapshot append |

---

## Estratégias Detalhadas

### CTAS (Create Table As Select)

```sql
CREATE OR REPLACE TABLE <target>
AS SELECT * FROM <source_view>;
```

**Prós**:
- Simples de implementar
- Sempre consistente (full refresh)
- Não requer PK

**Contras**:
- Reconstrói tudo a cada refresh
- Custo proporcional ao volume
- Sem histórico de mudanças

**Usar quando**: Volume pequeno OU não tem PK OU simplicidade > eficiência

---

### MERGE Incremental

```sql
MERGE INTO <target> AS t
USING (
    SELECT * FROM <source_view>
    WHERE updated_at >= @last_run
) AS s
ON t.pk = s.pk
WHEN MATCHED AND s.updated_at > t.updated_at 
    THEN UPDATE SET ...
WHEN NOT MATCHED 
    THEN INSERT ...;
```

**Prós**:
- Eficiente para grandes volumes
- Processa apenas delta
- Preserva dados não modificados

**Contras**:
- Requer PK clara
- Requer timestamp confiável
- Mais complexo de implementar

**Usar quando**: Volume grande E tem PK E tem timestamp

---

### Snapshot Append

```sql
INSERT INTO <target_snapshots>
SELECT 
    CURRENT_TIMESTAMP AS snapshot_at,
    *
FROM <source_view>;
```

**Prós**:
- Preserva histórico completo
- Time-travel analítico
- Simples de implementar

**Contras**:
- Cresce indefinidamente
- Requer gestão de retenção
- Queries precisam filtrar por snapshot

**Usar quando**: Precisa de histórico de estados

---

## Clustering Keys

### Quando Usar

Use clustering quando:
- Volume > 10M rows
- Queries frequentes filtram por colunas específicas
- Dados são inseridos em ordem diferente da query

### Como Escolher Keys

1. **Colunas de filtro frequente** (WHERE clauses)
2. **Colunas de JOIN frequente**
3. **Cardinalidade média** (nem muito alta, nem muito baixa)

```sql
-- Bom: filtros frequentes
CLUSTER BY (clinic_id, event_month)

-- Ruim: cardinalidade muito alta
CLUSTER BY (transaction_id)  -- unique, não ajuda

-- Ruim: cardinalidade muito baixa
CLUSTER BY (status)  -- só 3 valores
```

---

## Validation Checklist por Estratégia

### CTAS

- [ ] Contagem view = contagem tabela
- [ ] Sample de PKs batem
- [ ] Agregações principais batem
- [ ] `materialized_at` presente

### MERGE

- [ ] Contagem final esperada
- [ ] Registros atualizados corretos
- [ ] Registros novos inseridos
- [ ] Sem duplicatas por PK
- [ ] `updated_at` reflete mudanças

### Snapshot

- [ ] Novo snapshot criado
- [ ] `snapshot_at` correto
- [ ] Contagem do snapshot = view atual
- [ ] Snapshots antigos não modificados

---

## Performance Baseline Template

```markdown
## Performance Baseline — <view_name>

**Data**: <date>
**View**: <schema>.<view_name>

### Query Time

| Query | View | Tabela Mat | Melhoria |
|-------|------|------------|----------|
| COUNT(*) | Xs | Xs | X% |
| SELECT WHERE pk=X | Xs | Xs | X% |
| Aggregation | Xs | Xs | X% |

### Resource Usage

| Metric | View | Tabela Mat |
|--------|------|------------|
| Bytes scanned | X GB | X GB |
| Credits used | X | X |

### Decisão

[ ] Materializar (ganho > 50%)
[ ] Manter view (ganho < 50%)
```
