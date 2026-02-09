-- Initialize Ontology Storage in vox_popular (PostgreSQL)
-- This table stores a synchronized version of the markdown/YAML documentation
-- for consumption by external applications and AI agents.

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.ontology_entities (
    qualified_name      TEXT PRIMARY KEY,
    domains             TEXT[] NOT NULL,
    tier                INTEGER CHECK (tier IN (1, 2, 3)),
    semantic_markdown   TEXT,
    agentic_markdown    TEXT,
    axioms_json         JSONB DEFAULT '[]'::jsonb,
    status              TEXT DEFAULT 'DRAFT',
    metadata            JSONB DEFAULT '{}'::jsonb,
    sync_hash           TEXT,
    created_at          TIMESTAMP WITH TIME ZONE,
    updated_at          TIMESTAMP WITH TIME ZONE,
    synced_at           TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for domain search
CREATE INDEX IF NOT EXISTS idx_ontology_entities_domains ON public.ontology_entities USING GIN (domains);

-- Comment for clarity
COMMENT ON TABLE public.ontology_entities IS 'Central storage for ecosystem entities documentation and rules.';

-- --- Compatibility migrations (older schema versions) ---
-- Some early versions stored JSON as TEXT. Normalize to JSONB safely.

ALTER TABLE public.ontology_entities
  ALTER COLUMN metadata TYPE JSONB
  USING (
    CASE
      WHEN metadata IS NULL OR metadata::text = '' THEN '{}'::jsonb
      ELSE metadata::jsonb
    END
  );

ALTER TABLE public.ontology_entities
  ALTER COLUMN axioms_json TYPE JSONB
  USING (
    CASE
      WHEN axioms_json IS NULL OR axioms_json::text = '' THEN '[]'::jsonb
      ELSE axioms_json::jsonb
    END
  );
