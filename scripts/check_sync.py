import psycopg2

config = {
    "host": "n8n-data.cktq8qw4cdda.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "database": "vox_popular",
    "user": "vox_popular_user",
    "password": "W9y@tN4%mG2s#Q8k!FbZ1rLp"
}

def check():
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT qualified_name, domains, tier, status FROM public.ontology_entities;")
    rows = cursor.fetchall()
    print(f"📊 Rows in ontology_entities: {len(rows)}")
    for row in rows:
        print(f"   - {row[0]} | Domains: {row[1]} | Tier: {row[2]} | Status: {row[3]}")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    check()
