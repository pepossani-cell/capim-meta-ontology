import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def _get_vox_popular_pg_config():
    host = os.getenv("VOX_POPULAR_HOST")
    port_raw = os.getenv("VOX_POPULAR_PORT", "5432")
    database = os.getenv("VOX_POPULAR_DB")
    user = os.getenv("VOX_POPULAR_USER")
    password = os.getenv("VOX_POPULAR_PASSWORD")

    missing = [k for k, v in {
        "VOX_POPULAR_HOST": host,
        "VOX_POPULAR_DB": database,
        "VOX_POPULAR_USER": user,
        "VOX_POPULAR_PASSWORD": password,
    }.items() if not v]

    try:
        port = int(port_raw)
    except ValueError:
        raise ValueError(f"VOX_POPULAR_PORT inválida: {port_raw!r}")

    if missing:
        raise RuntimeError("Variáveis ausentes: " + ", ".join(missing))

    return {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
    }

def apply_sql(sql_file):
    config = _get_vox_popular_pg_config()
    print(f"[SQL] Applying {sql_file} to {config['database']}...")
    try:
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read()
            cursor.execute(sql)
            
        print("[OK] SQL applied successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Error applying SQL: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        apply_sql(sys.argv[1])
    else:
        apply_sql("scripts/init_ontology_db.sql")
