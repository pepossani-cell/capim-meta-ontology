# FST Transitions — EDA Workflow States

> **Purpose**: Detalhamento das transições entre estados do EDA workflow  
> **Based on**: DatawiseAgent FST Architecture (EMNLP 2025)

---

## State Machine Formal Definition

```yaml
FST:
  name: EDA_WORKFLOW
  initial_state: TATEANTE
  final_states: [END]
  
  states:
    TATEANTE:
      type: exploratory
      max_iterations: unbounded  # Pode loopar indefinidamente
      
    CALIBRAR:
      type: stabilization
      max_iterations: 3  # Se não estabilizar em 3, revisar premissas
      
    ESTÁVEL:
      type: production
      max_iterations: 1  # Estado final, não loopa
      
    END:
      type: terminal
```

---

## Transition Table

### From TATEANTE

| Trigger | Condition | Target | Action |
|---------|-----------|--------|--------|
| `promote` | Achado será reutilizado | CALIBRAR | Iniciar documentação |
| `stabilize` | Achado é afirmação estável | CALIBRAR | Criar microtest |
| `invalidate` | Hipótese invalidada | TATEANTE | Registrar no README |
| `ambiguity` | Ambiguidade detectada | TATEANTE | Invoke @debate, aguardar |
| `abort` | EDA cancelado | END | Limpar scratchpad |

### From CALIBRAR

| Trigger | Condition | Target | Action |
|---------|-----------|--------|--------|
| `document` | Semântica documentada | ESTÁVEL | Atualizar docs/reference |
| `validate` | Microtest passando | ESTÁVEL | Registrar em audit/ |
| `rollback` | Precisa mais investigação | TATEANTE | Voltar ao scratchpad |
| `ambiguity` | Ambiguidade em semântica | CALIBRAR | Invoke @debate, aguardar |

### From ESTÁVEL

| Trigger | Condition | Target | Action |
|---------|-----------|--------|--------|
| `new_cycle` | Novo ciclo necessário | TATEANTE | Criar novo scratchpad |
| `complete` | EDA concluído | END | Finalizar contratos |

---

## Transition Guards (Pré-condições)

### Para entrar em CALIBRAR

```python
def can_enter_calibrar(context):
    return (
        context.has_reusable_finding() or
        context.has_stable_assertion()
    ) and not context.has_unresolved_ambiguity()
```

### Para entrar em ESTÁVEL

```python
def can_enter_estavel(context):
    return (
        context.has_documented_semantics() or
        context.has_passing_microtest()
    ) and context.all_invariants_validated()
```

### Para fazer rollback

```python
def should_rollback(context):
    return (
        context.calibration_attempts > 3 or
        context.found_new_uncertainty()
    )
```

---

## Ambiguity Detection Rules

```python
AMBIGUITY_TRIGGERS = [
    # População
    {"pattern": r"(inclui|exclui|entra|sai)\?", "type": "population"},
    {"pattern": r"universo.*\?", "type": "population"},
    
    # Temporal
    {"pattern": r"mês parcial", "type": "temporal"},
    {"pattern": r"(no mês|ever|alguma vez)", "type": "temporal"},
    
    # Definições
    {"pattern": r"o que significa.*\?", "type": "definition"},
    {"pattern": r"(ativo|inativo).*\?", "type": "definition"},
    
    # Eixos
    {"pattern": r"(bucket|classe|eixo).*\?", "type": "classification"},
    {"pattern": r"(top|bottom).*%", "type": "classification"},
    
    # Semântica
    {"pattern": r"created_at.*(evento|cadastro)", "type": "semantics"},
    {"pattern": r"timestamp.*significa", "type": "semantics"},
]

def detect_ambiguity(text):
    for trigger in AMBIGUITY_TRIGGERS:
        if re.search(trigger["pattern"], text, re.IGNORECASE):
            return trigger["type"]
    return None
```

---

## State Artifacts Mapping

| State | Artifacts Created | Artifacts Consumed |
|-------|-------------------|-------------------|
| TATEANTE | scratchpad.sql, README.md | - |
| CALIBRAR | audit/*.sql, reference/*.md | scratchpad.sql |
| ESTÁVEL | studies/*.sql, *CONTRATO*.md | audit/*.sql, reference/*.md |

---

## Recovery Strategies

### On Execution Error

```python
def handle_execution_error(state, error):
    if state == "TATEANTE":
        # Erros em TATEANTE são esperados (exploração)
        log_to_readme(error)
        return "TATEANTE"  # Continua no mesmo estado
        
    elif state == "CALIBRAR":
        # Erros em CALIBRAR indicam premissa errada
        return "TATEANTE"  # Rollback
        
    elif state == "ESTÁVEL":
        # Erros em ESTÁVEL são críticos
        raise CriticalError("Artifact validation failed")
```

### On Debate Timeout

```python
def handle_debate_timeout(state, debate_context):
    # Se debate não resolve em tempo razoável
    # Registrar como incerteza e continuar com assunção explícita
    log_uncertainty(debate_context)
    return state  # Mantém estado atual
```

---

## Metrics to Track

```yaml
eda_metrics:
  - name: time_in_tateante
    description: Tempo total em estado exploratório
    threshold: 80%  # Maioria do tempo deve ser aqui
    
  - name: rollback_count
    description: Número de rollbacks CALIBRAR → TATEANTE
    threshold: 3  # Se > 3, revisar premissas fundamentais
    
  - name: debate_invocations
    description: Número de vezes que @debate foi invocado
    expected: 2-5 per EDA  # Menos = assumindo demais, mais = paralysis
    
  - name: promotion_rate
    description: % de queries do scratchpad que foram promovidas
    expected: 10-30%  # Maioria do scratchpad é transitório
```

---

## References

- DatawiseAgent: FST-Based Framework (EMNLP 2025)
- OpenAI: A Practical Guide to Building Agents
- Cursor: Structured Agentic Workflow
