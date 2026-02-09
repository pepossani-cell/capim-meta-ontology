import os
import sys
import argparse
import pandas as pd
from datetime import datetime

# Add project src to path for snowflake utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../src')))
from utils.snowflake_connection import run_query

def df_to_markdown(df):
    """Simple converter from DataFrame to Markdown table without tabulate."""
    if df is None or df.empty:
        return ""
    
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    for _, row in df.iterrows():
        # Sanitize values to avoid breaking markdown (e.g. newlines)
        row_values = []
        for val in row:
            v = str(val).replace('\n', ' ').replace('\r', '')
            row_values.append(v)
        lines.append("| " + " | ".join(row_values) + " |")
    
    return "\n".join(lines)

def profile_entity(table_name):
    """
    Executes a series of queries to profile a Snowflake table/view.
    Returns a markdown-formatted report.
    """
    print(f"Investigating {table_name}...")
    
    report = []
    report.append(f"# Investigation Report: {table_name}")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n---\n")

    # 1. Fetch Schema first to be dynamic
    print("  - Fetching schema info...")
    parts = table_name.split('.')
    if len(parts) == 3:
        database_name = parts[0]
        schema_name = parts[1]
        table_name_short = parts[2]
    elif len(parts) == 2:
        database_name = None
        schema_name = parts[0]
        table_name_short = parts[1]
    else:
        database_name = None
        schema_name = 'PUBLIC'
        table_name_short = parts[0]
    
    is_table = f"{database_name}.INFORMATION_SCHEMA.COLUMNS" if database_name else "INFORMATION_SCHEMA.COLUMNS"
    
    q_schema = f"""
    SELECT 
        column_name, 
        data_type, 
        is_nullable
    FROM {is_table}
    WHERE table_name = '{table_name_short.upper()}' 
      AND table_schema = '{schema_name.upper()}'
    ORDER BY ordinal_position
    """
    res_schema = run_query(q_schema)
    if res_schema is None or res_schema.empty:
        return f"Error: Table {table_name} not found in {is_table}."
    
    all_cols = res_schema['COLUMN_NAME'].tolist()

    # 1. Row Count 
    print("  - Fetching volume...")
    q_volume = f"SELECT COUNT(*) as total_rows FROM {table_name}"
    res_vol = run_query(q_volume)
    total_rows = res_vol['TOTAL_ROWS'].iloc[0] if res_vol is not None else 0
    
    report.append("## 1. Volume & Grain")
    report.append(f"- **Total Rows**: {total_rows:,}")
    
    # Try to find meaningful ID columns for unique counts
    id_candidates = [c for c in all_cols if any(x in c.upper() for x in ['ID', 'KEY', 'CODE'])]
    clinic_candidates = [c for c in all_cols if any(x in c.upper() for x in ['CLINIC_ID', 'RETAIL_ID'])]
    
    if id_candidates or clinic_candidates:
        select_parts = []
        if id_candidates:
            # Pick the most likely primary ID (usually first one or shortest name)
            best_id = sorted(id_candidates, key=len)[0]
            select_parts.append(f"COUNT(DISTINCT {best_id}) as distinct_{best_id.lower()}")
        if clinic_candidates:
            best_clinic = sorted(clinic_candidates, key=len)[0]
            select_parts.append(f"COUNT(DISTINCT {best_clinic}) as distinct_{best_clinic.lower()}")
            
        if select_parts:
            q_distinct = f"SELECT {', '.join(select_parts)} FROM {table_name}"
            try:
                res_dist = run_query(q_distinct)
                if res_dist is not None:
                    for col in res_dist.columns:
                        report.append(f"- **{col.replace('_', ' ').title()}**: {res_dist[col].iloc[0]:,}")
            except:
                pass

    # 2. Schema Summary
    report.append("\n## 2. Schema Summary")
    report.append(df_to_markdown(res_schema))

    # 3. Null Analysis
    print("  - Performing null analysis...")
    if all_cols:
        # Limit to first 30 columns to avoid query length issues
        cols_to_check = all_cols[:30]
        null_queries = [f"SUM(CASE WHEN {c} IS NULL THEN 1 ELSE 0 END) as {c}_nulls" for c in cols_to_check]
        q_nulls = f"SELECT {', '.join(null_queries)} FROM {table_name}"
        res_nulls = run_query(q_nulls)
        if res_nulls is not None:
            null_data = []
            for c in cols_to_check:
                n_count = res_nulls[f"{c.upper()}_NULLS"].iloc[0]
                n_pct = (n_count / total_rows * 100) if total_rows > 0 else 0
                null_data.append({"Column": c, "Null Count": n_count, "Null %": f"{n_pct:.2f}%"})
            
            report.append("\n## 3. Null Analysis")
            report.append(df_to_markdown(pd.DataFrame(null_data)))

    # 4. Temporal Drift
    print("  - Fetching temporal drift...")
    ts_candidates = [c for c in all_cols if any(x in c.upper() for x in ['AT', 'DATE', 'TIME', 'CREATED', 'INSERTED'])]
    if ts_candidates:
        # Pick the best timestamp (usually the one with "CREATED" or shortest "AT")
        best_ts = None
        for cand in ts_candidates:
            if 'CREATED_AT' in cand.upper():
                best_ts = cand
                break
        if not best_ts:
            best_ts = sorted(ts_candidates, key=len)[0]
            
        q_drift = f"""
        SELECT 
            DATE_TRUNC('month', {best_ts})::DATE as month,
            COUNT(*) as row_count
        FROM {table_name}
        WHERE {best_ts} IS NOT NULL
        GROUP BY 1 ORDER BY 1 DESC
        LIMIT 24
        """
        try:
            res_drift = run_query(q_drift)
            if res_drift is not None:
                report.append(f"\n## 4. Temporal Drift (by {best_ts})")
                report.append(df_to_markdown(res_drift))
        except:
            pass

    return "\n".join(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile a Snowflake table or view")
    parser.add_argument("--table", required=True, help="Full table name (DATABASE.SCHEMA.TABLE)")
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    report_md = profile_entity(args.table)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"\nReport saved to {args.output}")
    else:
        print("\n" + report_md)
