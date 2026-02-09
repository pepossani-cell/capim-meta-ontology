# 📁 Decision Archive: Workspace Standards & Documentation (2026-02-03)

## Archived: 2026-02-03

---

### 8.1 Workspace Structure Standardization

**Status**: ✅➡️ Executed

**Decision**: Hierarchical cursorrules (global + project-specific)

**Rationale**: 
- Eliminate duplication of visualization standards and Snowflake protocols across projects
- Create single source of truth in capim-meta-ontology
- Projects extend global rules with domain-specific additions

**Executed On**: 2026-02-03

**Implementation**:
- Global cursorrules in capim-meta-ontology/.cursorrules
- Projects extend with domain-specific rules (bnpl-funil, ontologia-saas, client-voice-data, client-voice)
- Eliminated duplication of visualization standards (moved to shared doc)
- Standardized Snowflake protocols across projects

**Related Files**:
- `capim-meta-ontology/.cursorrules` (global)
- `docs/WORKSPACE_STRUCTURE.md` (complete documentation)
- `.cursor/INTEGRATION_TEST.md` (validation tests)
- `.cursor/CURSORRULES_AUDIT.md` (analysis of common sections)
- All project `.cursorrules` files

---

### 8.2 Client-Voice Classification

**Status**: ✅➡️ Executed

**Decision**: Application Layer (not ontological project)

**Rationale**:
- Separate concerns: data ontology vs UI/application
- client-voice-data/ = ontology project (data structures, ETL)
- client-voice/ = Streamlit app (UI, visualization)
- Aligns with MEMORY_ARCHITECTURE_CONSTITUTION separation of concerns

**Executed On**: 2026-02-03

**Implementation**:
- Confirmed separation: client-voice-data/ (ontology) + client-voice/ (app)
- Created .cursorrules for client-voice-app (to be renamed)
- Updated DOMAIN_REGISTRY.yaml with CLIENT_VOICE path

**Related Files**:
- `client-voice-data/` (ontology project)
- `client-voice/` (Streamlit app)
- `federation/DOMAIN_REGISTRY.yaml`

**Note**: Rename to client-voice-app/ pending (ID 8.5)

---

### 8.3 Visualization Standards Centralization

**Status**: ✅➡️ Executed

**Decision**: Extract to shared doc

**Rationale**:
- 30+ lines of visualization standards were duplicated across project cursorrules
- Single source of truth easier to maintain
- All projects reference shared doc instead of duplicating

**Executed On**: 2026-02-03

**Implementation**:
- Created `capim-meta-ontology/docs/VISUALIZATION_STANDARDS.md`
- All project cursorrules now reference this doc
- Eliminated 30+ line duplication per project

**Related Files**:
- `docs/VISUALIZATION_STANDARDS.md` (shared standards)
- All project `.cursorrules` files (reference instead of duplicate)

**Content**:
- Theme: Seaborn whitegrid, talk, pastel
- Layout: Dual panels for volume+share charts
- Legend: Outside plot area (right side)
- Labels: Always annotate latest month datapoints
- Export: DPI 220, bbox_inches='tight'
- Traceability: Include period, source, caveats

---

### 8.4 Rules Language Standardization

**Status**: ✅➡️ Executed

**Decision**: English for .cursor/rules/, Portuguese for .cursorrules

**Rationale**:
- Rules (technical protocols) in English for consistency with Cursor conventions
- Cursorrules (business context) in Portuguese for local team
- Global cursorrules bilingual (serves as bridge)

**Executed On**: 2026-02-03

**Implementation**:
- All `.cursor/rules/*.mdc` files in English
- All project `.cursorrules` files in Portuguese
- Global `.cursorrules` bilingual with clear separation

**Related Files**:
- `.cursor/rules/` folder (all English)
- Project `.cursorrules` files (all Portuguese)

---

### 9.1 Rename ontologia-cf to ontologia-saas

**Status**: ✅➡️ Executed

**Decision**: ontologia-cf → ontologia-saas

**Rationale**:
- "saas" is more descriptive than "cf" (clinic flow)
- Consistent with DOMAIN_ID naming
- Better reflects the domain scope

**Executed On**: 2026-02-03

**Implementation**:
- Folder renamed: ontologia-cf/ → ontologia-saas/
- Updated 40+ references across meta-ontology, bnpl-funil, client-voice-data
- Updated DOMAIN_REGISTRY.yaml paths
- Fixed 4 Python scripts with hardcoded paths in bnpl-funil
- Updated 30+ documentation files (WORKSPACE_STRUCTURE, START_HERE, skills)
- Git history preserved (simple folder rename)

**Impact**:
- ✅ DOMAIN_REGISTRY.yaml — Paths updated
- ✅ Python scripts in bnpl-funil — 4 scripts fixed
- ✅ Documentation — 30+ files updated
- ✅ Folder renamed successfully
- ⚠️ Git history preserved

**Related Files**:
- `ontologia-saas/` (renamed folder)
- `federation/DOMAIN_REGISTRY.yaml`
- Multiple Python scripts in bnpl-funil
- Documentation files across projects

---

### 10.1 Dual Documentation Pattern (Semantic + Agentic)

**Status**: ✅➡️ Executed

**Decision**: Create `.cursor/rules/entity_documentation.mdc` + enhance `@investigate-entity` skill

**Rationale**:
- Formalizes "Map (Semantic) vs X-Ray (Agentic)" principle from 2026-02-02
- Clear separation of "Why" (business context) vs "How" (technical details)
- Auto-enforced via glob patterns
- Prevents mixing of concerns in entity documentation

**Executed On**: 2026-02-03

**Implementation**:
1. Created `.cursor/rules/entity_documentation.mdc` (303 lines):
   - Naming convention: `<ENTITY>_SEMANTIC.md` + `<ENTITY>.md`
   - Mandatory sections for each type
   - Validation checklist (structure + content + tone)
   - Location rules (domain-specific vs ECOSYSTEM)
   - Cross-reference requirements

2. Updated `@investigate-entity/SKILL.md` (351 lines):
   - Step 2 expanded with 15+ specific debate questions
   - Example: "Profiling vs Debate Output" (concrete difference)
   - Content validation checklist (10 items)
   - Post-profiling guidance section
   - Common pitfalls explicitly listed

**Related Files**:
- `.cursor/rules/entity_documentation.mdc` (new)
- `.cursor/skills/investigate-entity/SKILL.md` (updated)
- `client-voice-data/_domain/_docs/reference/` (examples)

**Key Concepts**:
- **SEMANTIC** (Map/Why): Business definition, use cases, limitations, caveats
- **AGENTIC** (X-Ray/How): Schema, column profile, query optimization, validation

**Example**: ZENDESK_TICKETS dual docs created as reference implementation

---

### 10.2 ZENDESK docs relocation

**Status**: ✅➡️ Executed

**Decision**: Move from capim-meta-ontology/ECOSYSTEM to client-voice-data/reference

**Rationale**:
- ZENDESK is CLIENT_VOICE domain, not cross-domain
- Even though other domains JOIN to ZENDESK, they don't define its semantics
- Violates "no single domain owns" criterion for ECOSYSTEM
- Aligns with Dual Documentation Pattern

**Executed On**: 2026-02-03

**Implementation**:
1. Created dual docs in `client-voice-data/_domain/_docs/reference/`:
   - `ZENDESK_TICKETS_SEMANTIC.md` (1,800 lines) — Bifurcated Model, Routing Logic, Tag Taxonomy
   - `ZENDESK_TICKETS.md` (600 lines) — Schema, Column Profile, Query Optimization
   - `ZENDESK_USERS_SEMANTIC.md` (400 lines) — Identity Resolution Patterns, Role Semantics
   - `ZENDESK_USERS.md` (500 lines) — Schema, Relationships, Validation Queries

2. Validated existing dual docs (already correct):
   - `SOURCE_ZENDESK_COMMENTS_SEMANTIC.md`
   - `SOURCE_ZENDESK_COMMENTS.md`
   - `ZENDESK_TICKETS_ENHANCED_SEMANTIC.md`
   - `ZENDESK_TICKETS_ENHANCED.md`

3. Deleted old files from `capim-meta-ontology/_domain/_docs/ECOSYSTEM/`:
   - `ZENDESK_TICKETS.md` (mixed semantic+technical)
   - `ZENDESK_USERS.md` (mixed semantic+technical)
   - `ZENDESK_COMMENTS.md`

4. Updated `client-voice-data/_domain/_docs/ENTITY_INDEX.yaml`:
   - Added 4 entities with documentation references
   - Each entity has `documentation.semantic` and `documentation.agentic` fields

5. Created `capim-meta-ontology/_domain/_docs/ECOSYSTEM/README.md`:
   - Documents promotion criteria (3 requirements)
   - Explains what was moved and why
   - Guides future ECOSYSTEM promotions (CLINICS, PATIENTS candidates)

**Related Files**:
- `client-voice-data/_domain/_docs/reference/ZENDESK_*` (6 new dual docs)
- `client-voice-data/_domain/_docs/ENTITY_INDEX.yaml` (updated)
- `capim-meta-ontology/_domain/_docs/ECOSYSTEM/README.md` (new)
- Deleted 3 files from ECOSYSTEM

**Result**: client-voice-data now has 100% dual documentation coverage for all ZENDESK entities.

---

### 10.3 Workspace Hygiene Protocol (Scratchpad + Cleanup)

**Status**: ✅➡️ Executed

**Decision**: Create `.cursor/rules/workspace_hygiene.mdc` + .gitignore enforcement

**Rationale**:
- Formalizes scratchpad pattern from ontologia-saas (dual scratchpad: per-study + global)
- Prevents project bloat via gitignore rules
- Prepares client-voice-data for future EDA work
- Consistent pattern across all data projects

**Executed On**: 2026-02-03

**Implementation**:
1. Created `.cursor/rules/workspace_hygiene.mdc` (460 lines):
   - Scratchpad Protocol (dual level: per-study + global)
   - Named blocks (BEGIN_/END_) + `run_scratchpad_block` execution
   - Lifecycle: scratchpad → estabiliza → migrate
   - Temporary artifacts protocol (`_scratch/`, `@temp`, `outputs/`)
   - Gitignore rules for enforcement
   - Cleanup protocol (before commit, end of task, session end)
   - Anti-patterns + validation checklist
   - Project-specific notes (bnpl-funil, ontologia-saas, client-voice-data)

2. Updated `.cursor/rules/snowflake_data.mdc`:
   - Added explicit link to workspace_hygiene.mdc for scratchpad protocol

3. Created `.gitignore` in ontologia-saas (WAS MISSING!):
   - Python cache blocking
   - `_scratch/` folder (gitignored)
   - `outputs/` (transitório)
   - EDA temp artifacts patterns
   - Explicit opt-in for published plots (`!eda/**/plots/*.png`)

4. Updated `.gitignore` in client-voice-data:
   - Added `_scratch/` folder (future-proof)
   - Added `outputs/` folder (transitório)
   - Added EDA patterns (future EDA preparation)
   - Comments about explicit opt-in

5. Created `client-voice-data/queries/audit/scratchpad.sql`:
   - Header with rules of conduct
   - Named blocks (BEGIN_/END_) explained
   - Example queries commented (ticket volume, sentiment drift)
   - Empty but documented (ready for use)

**Related Files**:
- `.cursor/rules/workspace_hygiene.mdc` (new, 460 lines)
- `.cursor/rules/snowflake_data.mdc` (updated, link added)
- `ontologia-saas/.gitignore` (new, WAS MISSING!)
- `client-voice-data/.gitignore` (updated)
- `client-voice-data/queries/audit/scratchpad.sql` (new)

**Applies to**:
- ✅ bnpl-funil (queries + eda)
- ✅ ontologia-saas (queries + eda)
- ✅ client-voice-data (queries, future eda)
- ❌ client-voice (Streamlit app, different patterns)

**Key Concepts**:
- **Dual scratchpad**: Per-study (`eda/<estudo>/scratchpad.sql`) + Global (`queries/audit/scratchpad.sql`)
- **Lifecycle**: scratchpad → estabiliza → migrate to queries/audit/ or queries/studies/
- **Enforcement**: Auto-applied via glob patterns + gitignore blocking

**Gap Fixed**: ontologia-saas had NO .gitignore before (all temp files could be committed!)

---

## Summary

**Total Archived**: 8 decisions

**Themes**:
1. **Workspace Standardization** (8.1-8.4) — Global rules, project structure, language conventions
2. **Project Rename** (9.1) — ontologia-cf → ontologia-saas
3. **Documentation Standards** (10.1-10.3) — Dual docs, ZENDESK relocation, workspace hygiene

**Impact**:
- 3 new rules created (entity_documentation, workspace_hygiene)
- 2 skills updated (investigate-entity, indirectly snowflake_data)
- 10+ documentation files created/updated
- 2 .gitignore files created/updated (ontologia-saas was missing!)
- 6 dual docs created for ZENDESK entities
- Workspace now has consistent patterns across all data projects

**Files Created/Updated**: 20+ files
**Lines of Documentation**: 2,500+ lines of formalized protocols

---

## Next Session

Use `@session-start` to load context and continue with:
- Pending items (9 still active in DECISIONS_IN_PROGRESS.md)
- SaaS App Patients identification (Priority 2)
- Optimize Streamlit code when priorities defined (Priority 7)
