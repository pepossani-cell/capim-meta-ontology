# Cross-Attribute Correlation Query Templates

Reference for Step 6 of `@investigate-entity` skill.

## 1. Identify Candidate Columns

```sql
-- Find boolean and low-cardinality categorical columns
WITH column_stats AS (
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        COUNT(DISTINCT {COLUMN_NAME}) as cardinality
    FROM {TABLE}
    GROUP BY 1, 2
)
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    cardinality
FROM column_stats
WHERE DATA_TYPE = 'BOOLEAN'
   OR (DATA_TYPE IN ('TEXT', 'VARCHAR') AND cardinality < 10)
ORDER BY cardinality;
```

## 2. Cross-Coverage Analysis (Boolean A → Any B)

```sql
-- Template: How does A affect coverage of B?
SELECT 
    {A_COLUMN} as a_value,
    COUNT(*) as total,
    COUNT({B_COLUMN}) as b_filled,
    COUNT(*) - COUNT({B_COLUMN}) as b_null,
    ROUND(100.0 * COUNT({B_COLUMN}) / NULLIF(COUNT(*), 0), 2) as b_coverage_pct
FROM {TABLE}
WHERE {FILTER}
GROUP BY 1
ORDER BY 1 NULLS FIRST;
```

**Example** (discovered in C2_ENRICHED_REQUESTS):
```sql
SELECT 
    is_canceled_after_signing as a_value,
    COUNT(*) as total,
    COUNT(payments_as_of_date) as b_filled,
    ROUND(100.0 * COUNT(payments_as_of_date) / NULLIF(COUNT(*), 0), 2) as b_coverage_pct
FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.C2_ENRICHED_REQUESTS
WHERE was_signed = TRUE
GROUP BY 1;
-- Result: is_canceled=TRUE → 0% coverage, is_canceled=FALSE → 100% coverage
-- Lift = ∞ (functional dependency)
```

## 3. Lift Calculation

```sql
-- Calculate Lift: P(B_null|A=TRUE) / P(B_null|overall)
WITH base AS (
    SELECT 
        {A_COLUMN},
        CASE WHEN {B_COLUMN} IS NULL THEN 1 ELSE 0 END as b_is_null
    FROM {TABLE}
    WHERE {FILTER}
),
overall AS (
    SELECT AVG(b_is_null) as p_b_null_overall
    FROM base
),
conditional AS (
    SELECT 
        {A_COLUMN},
        AVG(b_is_null) as p_b_null_given_a,
        COUNT(*) as cnt
    FROM base
    GROUP BY 1
)
SELECT 
    c.{A_COLUMN},
    c.cnt,
    ROUND(c.p_b_null_given_a * 100, 2) as pct_b_null,
    ROUND(o.p_b_null_overall * 100, 2) as pct_b_null_overall,
    ROUND(c.p_b_null_given_a / NULLIF(o.p_b_null_overall, 0), 2) as lift
FROM conditional c
CROSS JOIN overall o
ORDER BY lift DESC NULLS LAST;
```

## 4. Perfect Correlation Detection (A ↔ B)

```sql
-- Detect if A and B are always equal (or inverse)
SELECT 
    {A_COLUMN},
    {B_COLUMN},
    COUNT(*) as cnt
FROM {TABLE}
WHERE {FILTER}
GROUP BY 1, 2
ORDER BY 1, 2;

-- If only diagonal cells have values, it's a perfect correlation
-- Example: c1_origin_type IS NULL ↔ c1_is_synthetic = TRUE
```

## 5. Coverage Delta Matrix (Multiple Pairs)

```sql
-- Compare coverage of multiple B columns across A values
SELECT 
    {A_COLUMN},
    COUNT(*) as total,
    ROUND(100.0 * COUNT({B1_COLUMN}) / NULLIF(COUNT(*), 0), 2) as b1_coverage,
    ROUND(100.0 * COUNT({B2_COLUMN}) / NULLIF(COUNT(*), 0), 2) as b2_coverage,
    ROUND(100.0 * COUNT({B3_COLUMN}) / NULLIF(COUNT(*), 0), 2) as b3_coverage
FROM {TABLE}
WHERE {FILTER}
GROUP BY 1
ORDER BY 1;
```

## 6. Automated Batch Analysis

For tables with many boolean columns, run this meta-query:

```sql
-- Generate cross-coverage queries for all boolean pairs
-- (Run in Python, not directly in Snowflake)

-- Step 1: Get boolean columns
SELECT COLUMN_NAME
FROM {DATABASE}.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = '{SCHEMA}'
  AND TABLE_NAME = '{TABLE}'
  AND DATA_TYPE = 'BOOLEAN';

-- Step 2: For each pair (A, B), generate and run Template #2
-- Step 3: Flag pairs where coverage_delta > 20%
```

**Python implementation**: See `scripts/investigate.py` function `analyze_cross_correlations()`

## 7. Interpretation Guide

| Lift Value | Interpretation | Action |
|:---|:---|:---|
| 0.8 - 1.2 | No correlation | None |
| 1.2 - 2.0 | Weak correlation | Note in doc |
| 2.0 - 5.0 | Moderate dependency | ⚠️ Document as caveat |
| > 5.0 | Strong dependency | 🔴 Document + consider derived field |
| ∞ (division by zero) | Functional dependency | 📌 A completely determines B |

| Coverage Delta | Interpretation | Action |
|:---|:---|:---|
| < 10% | Negligible | None |
| 10% - 30% | Notable | Document if relevant |
| 30% - 50% | Significant | ⚠️ Document as caveat |
| > 50% | Critical | 🔴 Must document, likely functional |

## 8. Example Output (for AGENTIC doc)

```markdown
### 8.X. Cross-Attribute Dependencies (Auto-detected 2026-02-05)

| Attribute A | Condition | Attribute B | Coverage A=TRUE | Coverage A=FALSE | Delta | Lift |
|:---|:---|:---|---:|---:|---:|---:|
| is_canceled_after_signing | TRUE | payments_as_of_date | 0% | 100% | 100% | ∞ |
| is_bnpl_contract | FALSE | payment_status | 0.68% | 98.02% | 97.34% | 143.8 |
| c1_is_synthetic | TRUE | c1_origin_id | 0% | 100% | 100% | ∞ |

**Interpretation**:
- `is_canceled_after_signing` **functionally determines** absence of payment status
- `is_bnpl_contract = FALSE` nearly guarantees no payment tracking
- `c1_is_synthetic = TRUE` means `c1_origin_id` will always be NULL (by design)
```

---

## Version History

| Date | Change |
|:---|:---|
| 2026-02-05 | Initial version created after C2_ENRICHED_REQUESTS payment gap investigation |
