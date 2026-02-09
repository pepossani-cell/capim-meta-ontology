import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment or hardcoded test_pg_connection settings
config = {
    "host": "n8n-data.cktq8qw4cdda.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "database": "vox_popular",
    "user": "vox_popular_user",
    "password": "W9y@tN4%mG2s#Q8k!FbZ1rLp"
}

def apply_sql(sql_file):
    print(f"🚀 Applying {sql_file} to {config['database']}...")
    try:
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read()
            cursor.execute(sql)
            
        print("✅ SQL applied successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error applying SQL: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        apply_sql(sys.argv[1])
    else:
        apply_sql("scripts/init_ontology_db.sql")
