"""
Test PostgreSQL connection for Client Voice (vox_popular)
"""
import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
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

config = _get_vox_popular_pg_config()

print("[PG] Testing PostgreSQL connection...")
print(f"   Host: {config['host']}")
print(f"   Database: {config['database']}")
print(f"   User: {config['user']}")

try:
    conn = psycopg2.connect(
        host=config["host"],
        port=config["port"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
        connect_timeout=10
    )
    
    print("[OK] Connection successful!")
    
    # Test query - list tables
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    print(f"\n[PG] Tables in vox_popular ({len(tables)} found):")
    for table in tables:
        print(f"   - {table[0]}")
    
    cursor.close()
    conn.close()
    print("\n[OK] Test completed successfully!")
    
except psycopg2.OperationalError as e:
    print(f"[ERROR] Connection failed: {e}")
except Exception as e:
    print(f"[ERROR] Error: {e}")
