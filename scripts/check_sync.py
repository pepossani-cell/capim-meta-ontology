import psycopg2
from dotenv import load_dotenv
import os

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

def check():
    conn = psycopg2.connect(**_get_vox_popular_pg_config())
    cursor = conn.cursor()
    cursor.execute("SELECT qualified_name, domains, tier, status FROM public.ontology_entities;")
    rows = cursor.fetchall()
    print(f"[CHECK] Rows in ontology_entities: {len(rows)}")
    for row in rows:
        print(f"   - {row[0]} | Domains: {row[1]} | Tier: {row[2]} | Status: {row[3]}")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    check()
