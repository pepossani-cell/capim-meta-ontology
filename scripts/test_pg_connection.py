"""
Test PostgreSQL connection for Client Voice (vox_popular)
"""
import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

# VOX POPULAR (Client Voice) Configuration
config = {
    "host": "n8n-data.cktq8qw4cdda.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "database": "vox_popular",
    "user": "vox_popular_user",
    "password": "W9y@tN4%mG2s#Q8k!FbZ1rLp"
}

print("🔌 Testing PostgreSQL connection...")
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
    
    print("✅ Connection successful!")
    
    # Test query - list tables
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    print(f"\n📋 Tables in vox_popular ({len(tables)} found):")
    for table in tables:
        print(f"   - {table[0]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Test completed successfully!")
    
except psycopg2.OperationalError as e:
    print(f"❌ Connection failed: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
