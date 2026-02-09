# Debate Triggers — Quando Invocar @debate em EDA

> **Purpose**: Lista de ambiguidades que devem triggerar @debate durante EDA  
> **Principle**: Parar e debater é melhor que assumir e corrigir depois

---

## Regra Geral

**Se surgir ambiguidade que pode mudar QUALQUER um destes itens, PARE e invoque @debate**:

1. População/universo (quem entra/sai)
2. Âncora temporal (mês/janela; "mês parcial")
3. Definição de "no mês", "ever", "ativo"
4. Classes/buckets/eixos (inclui/exclui subgrupos)
5. Semântica de status/timestamps (evento vs cadastro/snapshot)

---

## Triggers por Categoria

### 1. População/Universo

| Sintoma | Exemplo | Template de Debate |
|---------|---------|-------------------|
| Incerteza sobre inclusão | "Incluo clínicas canceladas?" | Ver abaixo |
| Critério ambíguo | "Ativo = login ou orçamento?" | Ver abaixo |
| Subpopulação não clara | "Independentes inclui franquias de 1 unidade?" | Ver abaixo |

**Template**:
```markdown
@debate

**Ambiguidade**: Definição de população para [estudo]
**Contexto**: Analisando [objetivo], preciso definir quem entra no universo
**Opções**:
- A: Incluir [grupo X] (N estimado: ~Y)
- B: Excluir [grupo X] (N estimado: ~Z)
- C: [outra opção]
**Impacto se errado**: [descrever o que muda]
```

---

### 2. Âncora Temporal

| Sintoma | Exemplo | Quando Debater |
|---------|---------|----------------|
| Mês parcial | "Análise em 15/jan inclui janeiro inteiro?" | Sempre |
| Múltiplos timestamps | "`created_at` ou `event_date`?" | Quando divergem |
| Timezone | "Dados em UTC, análise em BRT?" | Sempre normalizar |

**Template**:
```markdown
@debate

**Ambiguidade**: Âncora temporal para [métrica]
**Contexto**: Preciso definir quando um evento é considerado "no mês X"
**Opções**:
- A: Usar [timestamp_1] — eventos às 23h de 31/jan contam em janeiro
- B: Usar [timestamp_2] — eventos às 23h de 31/jan contam em fevereiro (se UTC)
**Dados**: [query mostrando distribuição de timestamps]
**Impacto se errado**: [descrever divergência de contagens]
```

---

### 3. Definições de "Ativo", "No Mês", "Ever"

| Sintoma | Exemplo | Quando Debater |
|---------|---------|----------------|
| "Ativo" ambíguo | "Clínica ativa = login recente ou subscription ativa?" | Sempre |
| "No mês" vs "ever" | "Teve orçamento no mês ou alguma vez?" | Sempre |
| Threshold não claro | "Clínica grande = >50 orçamentos ou >R$10k?" | Sempre |

**Template**:
```markdown
@debate

**Ambiguidade**: Definição de "[termo]"
**Contexto**: O termo "[termo]" aparece em [N] lugares mas tem definições diferentes
**Definições encontradas**:
- Def 1: [descrição] — usado em [fonte 1]
- Def 2: [descrição] — usado em [fonte 2]
**Proposta**: Adotar [definição] como canônica
**Impacto**: [quais análises mudam]
```

---

### 4. Classes/Buckets/Eixos

| Sintoma | Exemplo | Quando Debater |
|---------|---------|----------------|
| Cutoffs arbitrários | "Por que small <10, não <5?" | Se impacta >10% da análise |
| Sobreposição | "Clínica é SP E grande — qual eixo priorizar?" | Sempre |
| Categoria residual grande | "'Outros' tem 40% do volume" | Se >20% em 'outros' |

**Template**:
```markdown
@debate

**Ambiguidade**: Definição de classes para eixo [nome]
**Contexto**: Criando buckets para [análise], mas cutoffs são arbitrários
**Opções**:
- A: Quartis (P25/P50/P75) — [vantagens/desvantagens]
- B: Thresholds de negócio ([X], [Y], [Z]) — [vantagens/desvantagens]
- C: Clustering automático — [vantagens/desvantagens]
**Dados**: [distribuição mostrando impacto de cada opção]
```

---

### 5. Semântica de Timestamps/Status

| Sintoma | Exemplo | Quando Debater |
|---------|---------|----------------|
| created_at ambíguo | "created_at é quando criou o registro ou quando ocorreu o evento?" | Se divergem |
| Status inconsistente | "status='active' mas cancelled_at não é null" | Sempre |
| Drift temporal | "Antes de 2024, o campo X não existia" | Sempre documentar |

**Template**:
```markdown
@debate

**Ambiguidade**: Semântica de [campo]
**Contexto**: O campo [campo] tem interpretação ambígua
**Evidência**:
```sql
-- Query mostrando a ambiguidade
SELECT [campo], COUNT(*) FROM [tabela] GROUP BY 1;
```
**Hipóteses**:
- H1: [campo] significa [interpretação 1]
- H2: [campo] significa [interpretação 2]
**Próximo passo**: [como validar]
```

---

## Anti-Patterns (Quando NÃO Debater)

❌ **Não invoque @debate para**:
- Decisões puramente técnicas (qual JOIN usar)
- Formatação de output
- Ordem de execução de queries
- Escolha de visualização

✅ **Essas decisões podem ser tomadas diretamente** pelo agente.

---

## Fluxo Pós-Debate

```
@debate invocado
    │
    ▼
[Usuário confirma decisão]
    │
    ├── Se decisão é local ao estudo:
    │   └── Registrar em eda/<estudo>/README.md
    │
    ├── Se decisão é estrutural/reutilizável:
    │   └── Criar ADR em docs/adr/
    │
    └── Se decisão muda semântica de entidade:
        └── Atualizar docs/reference/<ENTIDADE>.md
```

---

## Métricas de Debate Saudável

| Métrica | Valor Esperado | Se Fora do Range |
|---------|----------------|------------------|
| Debates por EDA | 2-5 | <2 = assumindo demais; >5 = analysis paralysis |
| Tempo médio de debate | 5-15 min | <5 = não explorando; >15 = escopo muito amplo |
| % debates que geraram ADR | 10-30% | <10% = decisões locais demais; >30% = over-engineering |

---

## Exemplos Reais

### Exemplo 1: População de Churn

```markdown
@debate

**Ambiguidade**: Quem entra no universo de análise de churn?

**Contexto**: Analisando churn de clínicas nos últimos 6 meses. Preciso definir o universo.

**Opções**:
- A: Todas as clínicas com subscription em algum momento do período
  - N estimado: ~5,000
  - Inclui: clinics que já cancelaram, clinics em trial
- B: Apenas clínicas com subscription ATIVA no início do período
  - N estimado: ~3,200
  - Exclui: clinics que entraram durante o período
- C: Clínicas com pelo menos 1 orçamento no período
  - N estimado: ~4,100
  - Proxy operacional, não de subscription

**Impacto se errado**: Taxa de churn muda de 12% (opção B) para 18% (opção A)

**Recomendação**: Opção B, pois foca em "clínicas que tinham algo a perder"
```

### Exemplo 2: Semântica de Timestamp

```markdown
@debate

**Ambiguidade**: `settlement_date` em TRANSACTIONS

**Contexto**: Usando settlement_date para calcular receita por mês

**Evidência**:
```sql
SELECT 
  COUNT(*) as total,
  COUNT(settlement_date) as with_settlement,
  COUNT(CASE WHEN status = 'settled' AND settlement_date IS NULL THEN 1 END) as settled_no_date
FROM TRANSACTIONS;
-- Resultado: 15% das transações settled não têm settlement_date
```

**Hipóteses**:
- H1: settlement_date só é preenchido após reconciliação bancária
- H2: Bug no sistema que não preenche em certos casos

**Próximo passo**: Investigar padrão temporal (quando começou o gap?)
```

---

## References

- `@debate` skill (capim-meta-ontology/.cursor/skills/debate/SKILL.md)
- Memory Governance Rule (.cursor/rules/memory_governance.mdc)
- ADR Template (docs/adr/)
