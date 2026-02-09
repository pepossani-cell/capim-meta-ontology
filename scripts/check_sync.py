import psycopg2
from dotenv import load_dotenv
import os
import sys

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

    cursor.execute(
        """
        SELECT qualified_name, domains, tier, status
        FROM public.ontology_entities
        ORDER BY qualified_name;
        """
    )
    rows = cursor.fetchall()
    print(f"[CHECK] Rows in ontology_entities: {len(rows)}")
    for row in rows:
        print(f"   - {row[0]} | Domains: {row[1]} | Tier: {row[2]} | Status: {row[3]}")

    cursor.execute(
        """
        SELECT
          qualified_name,
          domains,
          tier,
          status,
          COALESCE(metadata->>'source_domain', 'unknown') AS source_domain,
          COALESCE(metadata->'original_paths'->>'semantic', '') AS semantic_path,
          COALESCE(metadata->'original_paths'->>'agentic', '') AS agentic_path,
          (semantic_markdown IS NULL OR LENGTH(TRIM(semantic_markdown)) = 0) AS missing_semantic,
          (agentic_markdown IS NULL OR LENGTH(TRIM(agentic_markdown)) = 0) AS missing_agentic
        FROM public.ontology_entities
        WHERE
          (semantic_markdown IS NULL OR LENGTH(TRIM(semantic_markdown)) = 0)
          OR (agentic_markdown IS NULL OR LENGTH(TRIM(agentic_markdown)) = 0)
        ORDER BY qualified_name;
        """
    )
    missing = cursor.fetchall()

    if not missing:
        print("[CHECK] OK: todas as entidades possuem semantic_markdown e agentic_markdown não vazios.")
    else:
        missing_semantic_only = []
        missing_agentic_only = []
        missing_both = []

        for qualified_name, domains, tier, status, source_domain, sem_path, age_path, ms, ma in missing:
            item = (qualified_name, domains, tier, status, source_domain, sem_path, age_path)
            if ms and ma:
                missing_both.append(item)
            elif ms:
                missing_semantic_only.append(item)
            elif ma:
                missing_agentic_only.append(item)

        print(f"[CHECK] ATENÇÃO: entidades com docs faltando: {len(missing)}")
        if missing_both:
            print(f"[CHECK] - Sem SEMANTIC e AGENTIC: {len(missing_both)}")
            for qualified_name, domains, tier, status, source_domain, sem_path, age_path in missing_both:
                print(f"   - {qualified_name} | DomainSrc: {source_domain} | Domains: {domains} | Tier: {tier} | Status: {status}")
                print(f"     semantic_path: {sem_path or '<empty>'}")
                print(f"     agentic_path:  {age_path or '<empty>'}")
        if missing_semantic_only:
            print(f"[CHECK] - Sem SEMANTIC: {len(missing_semantic_only)}")
            for qualified_name, domains, tier, status, source_domain, sem_path, age_path in missing_semantic_only:
                print(f"   - {qualified_name} | DomainSrc: {source_domain} | Domains: {domains} | Tier: {tier} | Status: {status}")
                print(f"     semantic_path: {sem_path or '<empty>'}")
                print(f"     agentic_path:  {age_path or '<empty>'}")
        if missing_agentic_only:
            print(f"[CHECK] - Sem AGENTIC: {len(missing_agentic_only)}")
            for qualified_name, domains, tier, status, source_domain, sem_path, age_path in missing_agentic_only:
                print(f"   - {qualified_name} | DomainSrc: {source_domain} | Domains: {domains} | Tier: {tier} | Status: {status}")
                print(f"     semantic_path: {sem_path or '<empty>'}")
                print(f"     agentic_path:  {age_path or '<empty>'}")

    # --- Governance checks (strict) ---
    # Ensure ECOSYSTEM.CLINICS is SAAS-owned (canonical minimum contract).
    cursor.execute(
        """
        SELECT
          qualified_name,
          COALESCE(metadata->>'source_domain', '') AS source_domain,
          COALESCE(metadata->'original_paths'->>'semantic', '') AS semantic_path,
          COALESCE(metadata->'original_paths'->>'agentic', '') AS agentic_path
        FROM public.ontology_entities
        WHERE qualified_name = 'ECOSYSTEM.CLINICS';
        """
    )
    row = cursor.fetchone()
    governance_violations = []

    if row is None:
        governance_violations.append("ECOSYSTEM.CLINICS não encontrado em public.ontology_entities.")
    else:
        qualified_name, source_domain, sem_path, age_path = row
        if source_domain != "SAAS":
            governance_violations.append(
                "Governança violada: ECOSYSTEM.CLINICS deve ser SAAS-owned, "
                f"mas metadata.source_domain={source_domain!r}. "
                f"(semantic_path={sem_path!r}, agentic_path={age_path!r})"
            )

    if governance_violations:
        print("[CHECK] ERRO: violações de governança detectadas:")
        for msg in governance_violations:
            print(f"   - {msg}")
        cursor.close()
        conn.close()
        sys.exit(1)
    else:
        print("[CHECK] OK: governança ECOSYSTEM.CLINICS (SAAS-owned) verificada.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    check()
