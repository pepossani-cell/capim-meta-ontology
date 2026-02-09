---
name: Clinic Health Check
description: Execute comprehensive health diagnostic for a specific clinic
---

# Clinic Health Check Skill

This skill executes RULE-CROSS-001 (Clinic Health Diagnostic) to assess the overall health of a clinic across all domains.

## When to Use

- User asks about problems with a specific clinic
- User asks "what's wrong with clinic X?"
- User asks about a clinic's health status
- Proactive health monitoring (scheduled)

## Prerequisites

1. `clinic_id` must be known or resolvable
2. Snowflake access configured
3. PostgreSQL access configured (for CLIENT_VOICE data)

## Reference

This skill implements: `ontology/INFERENCE_RULES.yaml` → RULE-CROSS-001

## Execution Steps

### 1. Resolve Clinic ID
If user provides clinic name, resolve to ID:
```sql
SELECT clinic_id FROM CLINICS WHERE name ILIKE '%{clinic_name}%'
```

### 2. Query CLIENT_VOICE (Support Health)
```sql
SELECT 
    COUNT(ticket_id) as ticket_count_90d,
    AVG(sentimento_score) as avg_sentiment,
    LISTAGG(DISTINCT categoria, ', ') as top_issues
FROM CAPIM_DATA_DEV.POSSANI_SANDBOX.TICKET_ANALYSIS_V3
WHERE clinic_id = {clinic_id}
  AND event_date >= CURRENT_DATE() - 90
```

### 3. Query SAAS (Schedule Volume)
```sql
SELECT 
    COUNT(*) as appointment_count,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) as cancellation_rate
FROM SCHEDULES
WHERE clinic_id = {clinic_id}
  AND created_at >= CURRENT_DATE() - 90
```

### 4. Query FINTECH (Rejection Rate)
```sql
SELECT 
    COUNT(*) as total_simulations,
    SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) / COUNT(*) as rejection_rate
FROM CREDIT_SIMULATIONS
WHERE clinic_id = {clinic_id}
  AND created_at >= CURRENT_DATE() - 90
```

### 5. Synthesize Findings
Apply synthesis logic from RULE-CROSS-001:
- If ticket_count_90d > 5 AND avg_sentiment < 2.5: SUPPORT_CRISIS
- If churn_probability > 0.7: HIGH_CHURN_RISK
- If rejection_rate increased > 10pp: CREDIT_ISSUE

## Output Format

```markdown
## 🏥 Clinic Health Report: {clinic_name} (ID: {clinic_id})

### Overall Status: [CRITICAL / WARNING / HEALTHY]

### Support Health (CLIENT_VOICE)
- Tickets (90d): {count}
- Avg Sentiment: {score}/5
- Top Issues: {issues}

### Operational Health (SAAS)
- Appointments (90d): {count}
- Cancellation Rate: {rate}%
- Activity Trend: {trend}

### Credit Health (FINTECH)
- Simulations (90d): {count}
- Rejection Rate: {rate}%
- Top Rejection Reasons: {reasons}

### Recommendations
1. {recommendation_1}
2. {recommendation_2}
```

## Files

- `scripts/check.py` - Main execution script
- `../../ontology/INFERENCE_RULES.yaml` - Rule definition
- `../../federation/CAPABILITY_MATRIX.yaml` - Capability references
