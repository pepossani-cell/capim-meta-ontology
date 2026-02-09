import os
import json
import yaml
import hashlib
import psycopg2
import psycopg2.extras
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def _get_vox_popular_pg_config():
    """
    Read vox_popular Postgres credentials from environment variables.

    Expected variables (see .env):
      - VOX_POPULAR_HOST
      - VOX_POPULAR_PORT
      - VOX_POPULAR_DB
      - VOX_POPULAR_USER
      - VOX_POPULAR_PASSWORD
    """
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
        raise RuntimeError(
            "Variáveis de ambiente ausentes para conexão com vox_popular: "
            + ", ".join(missing)
        )

    return {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
    }

REGISTRY_PATH = "federation/DOMAIN_REGISTRY.yaml"

import re

def extract_axioms(content):
    """
    Extracts axioms from markdown content.
    Looks for:
    - > [!TYPE] Message
    - ### 3.X. Rule Name
    - ## Armadilhas / Guardrails
    """
    axioms = []
    if not content:
        return axioms

    # Regex for GitHub callouts: > [!DANGER] Message
    callouts = re.findall(r'> \[!(.*?)\]\s*(.*?)(?=\n>|\n\n|\n#|$)', content, re.DOTALL)
    for type_str, msg in callouts:
        axioms.append({
            "type": type_str.strip(),
            "description": msg.strip().replace('\n> ', ' '),
            "source": "callout"
        })

    # Regex for Business Rules: ### 3.X. Rule Name
    rules = re.findall(r'### \d+\.\d+\. (.*?)\n(.*?)(?=\n###|\n##|\n#|$)', content, re.DOTALL)
    for title, desc in rules:
        axioms.append({
            "type": "BUSINESS_RULE",
            "title": title.strip(),
            "description": desc.strip(),
            "source": "section"
        })

    return axioms

def get_file_content(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def resolve_doc_path(root_path: str, doc_path):
    """
    Resolve documentation path.

    - If doc_path is absolute: use as-is
    - Else: join with root_path (from DOMAIN_REGISTRY)
    """
    if not doc_path:
        return None
    p = Path(doc_path)
    if p.is_absolute():
        return str(p)
    return os.path.join(root_path, doc_path)

def get_sync_hash(content):
    if not content:
        return ""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def extract_dates(content):
    """Simple extraction of Last Updated from markdown content."""
    # Default to now if not found
    updated_at = datetime.now()
    created_at = datetime.now() # Fallback
    
    if not content:
        return created_at, updated_at
        
    for line in content.split('\n'):
        if 'Last Updated:' in line:
            try:
                date_str = line.split('Last Updated:')[1].strip()
                updated_at = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
        if 'Created:' in line:
            try:
                date_str = line.split('Created:')[1].strip()
                created_at = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
    
    return created_at, updated_at

import argparse

def sync():
    parser = argparse.ArgumentParser(description='Sync Ontology to PostgreSQL')
    parser.add_argument('--dry-run', action='store_true', help='Simulate sync without DB connection')
    args = parser.parse_args()

    print(f"[SYNC] Starting Ontology Synchronization... {'(DRY RUN)' if args.dry_run else ''}")
    
    if not os.path.exists(REGISTRY_PATH):
        print(f"[ERROR] Registry not found: {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        registry = yaml.safe_load(f)

    conn = None
    cursor = None

    if not args.dry_run:
        try:
            config = _get_vox_popular_pg_config()
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
        except Exception as e:
            print(f"[ERROR] Database connection failed: {e}")
            return
    else:
        print("[INFO] Dry run mode: Skipping database connection.")

    for domain in registry['domains']:
        domain_id = domain['id']
        root_path = domain['root_path']
        # Prefer ontology_index if present (CLIENT_VOICE), fallback to entity_index
        index_rel_path = domain.get('ontology_index') or domain.get('entity_index')
        if not index_rel_path:
            print(f"[WARN] Skipping {domain_id}: neither ontology_index nor entity_index present in registry")
            continue
        index_path = os.path.join(root_path, index_rel_path)

        if not os.path.exists(index_path):
            print(f"[WARN] Skipping {domain_id}: Index not found at {index_path}")
            continue

        print(f"[DOMAIN] Processing domain: {domain_id}")
        with open(index_path, 'r', encoding='utf-8') as f:
            index = yaml.safe_load(f)

        for entity in index['entities']:
            qualified_name = entity['id']
            print(f"   [ENTITY] Syncing: {qualified_name}")
            
            sem_path = resolve_doc_path(root_path, entity.get('semantic_doc'))
            age_path = resolve_doc_path(root_path, entity.get('agentic_doc'))
            
            sem_content = get_file_content(sem_path)
            age_content = get_file_content(age_path)
            
            # Extract Axioms
            axioms = extract_axioms(sem_content) + extract_axioms(age_content)
            
            # Extract timestamps
            created_at, updated_at = extract_dates(sem_content if sem_content else age_content)
            
            # Calculate hash
            combined_content = (sem_content or "") + (age_content or "")
            sync_hash = get_sync_hash(combined_content)
            
            # Prepare data
            data = {
                "qualified_name": qualified_name,
                "domains": entity['domains'],
                "tier": entity['tier'],
                "semantic_markdown": sem_content,
                "agentic_markdown": age_content,
                "axioms_json": psycopg2.extras.Json(axioms),
                "status": entity.get('status', 'ACTIVE'),
                "metadata": psycopg2.extras.Json({
                    "source_domain": domain_id,
                    "tier": entity['tier'],
                    "original_paths": {
                        "semantic": entity.get('semantic_doc'),
                        "agentic": entity.get('agentic_doc')
                    }
                }),
                "sync_hash": sync_hash,
                "created_at": created_at,
                "updated_at": updated_at,
                "synced_at": datetime.now()
            }

            if args.dry_run:
                print(f"      [OK] [DRY RUN] Prepared data for {qualified_name}")
                print(f"      - Axioms: {len(axioms)}")
                print(f"      - Hash: {sync_hash}")
                continue

            # Upsert with ECOSYSTEM merge logic
            # If ECOSYSTEM entity exists, we append the content if it's different
            try:
                cursor.execute("""
                    INSERT INTO public.ontology_entities (
                        qualified_name, domains, tier, semantic_markdown, agentic_markdown, axioms_json, 
                        status, metadata, sync_hash, created_at, updated_at, synced_at
                    ) VALUES (
                        %(qualified_name)s, %(domains)s, %(tier)s, %(semantic_markdown)s, 
                        %(agentic_markdown)s, %(axioms_json)s, %(status)s, %(metadata)s, %(sync_hash)s, 
                        %(created_at)s, %(updated_at)s, %(synced_at)s
                    )
                    ON CONFLICT (qualified_name) DO UPDATE SET
                        domains = ARRAY(SELECT DISTINCT UNNEST(public.ontology_entities.domains || EXCLUDED.domains)),
                        tier = LEAST(public.ontology_entities.tier, EXCLUDED.tier),
                        semantic_markdown = CASE 
                            WHEN public.ontology_entities.qualified_name LIKE 'ECOSYSTEM.%%' 
                            AND public.ontology_entities.semantic_markdown NOT LIKE '%%' || EXCLUDED.semantic_markdown || '%%'
                            THEN public.ontology_entities.semantic_markdown
                              || '\n\n--- [Merged from '
                              || COALESCE((EXCLUDED.metadata::jsonb)->>'source_domain', 'unknown')
                              || '] ---\n\n'
                              || EXCLUDED.semantic_markdown
                            ELSE EXCLUDED.semantic_markdown 
                        END,
                        agentic_markdown = EXCLUDED.agentic_markdown,
                        axioms_json = (public.ontology_entities.axioms_json::jsonb) || (EXCLUDED.axioms_json::jsonb),
                        status = EXCLUDED.status,
                        metadata = (public.ontology_entities.metadata::jsonb) || (EXCLUDED.metadata::jsonb),
                        sync_hash = EXCLUDED.sync_hash,
                        updated_at = EXCLUDED.updated_at,
                        synced_at = EXCLUDED.synced_at
                    WHERE public.ontology_entities.sync_hash IS DISTINCT FROM EXCLUDED.sync_hash OR public.ontology_entities.qualified_name LIKE 'ECOSYSTEM.%%';
                """, data)
            except Exception as e:
                print(f"      [ERROR] Error syncing {qualified_name}: {e}")
                conn.rollback()

    if not args.dry_run and conn:
        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] Synchronization complete!")
    elif args.dry_run:
        print("[OK] Dry run complete!")

if __name__ == "__main__":
    sync()
