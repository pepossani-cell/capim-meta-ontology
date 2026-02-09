-- Prune obsolete qualified_name entries after index renames.
-- This is intentionally explicit (no wildcard deletes).

DELETE FROM public.ontology_entities
WHERE qualified_name IN (
  'ECOSYSTEM.CLINICS.RAW',
  'ECOSYSTEM.CLINICS.ACQUISITION'
);

