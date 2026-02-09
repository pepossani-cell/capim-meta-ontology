# 📁 Decision Archive: Architecture & Structure (2026-02)

> **Archived**: 2026-02-01
> **Session**: Project restructuring, folder naming, and credential setup

---

## 1. Project Structure & Naming

### 1.1 Cenário C (Híbrido)
- **Status**: ✅ Decided + Executed
- **Decision**: Local ontology in each project (`_domain/`), global shared ontology in `capim-meta-ontology`
- **Rationale**: Best balance between proximity to code and federation
- **Executed On**: 2026-02-01
- **Related Files**:
  - `ontologia-cf/_domain/`
  - `bnpl-funil/_domain/`
  - `capim-meta-ontology/federation/`

### 1.2 Rename `project_refactor` → `_domain`
- **Status**: ✅ Decided + Executed
- **Decision**: Yes, applied to SAAS and FINTECH. CLIENT_VOICE kept flat (no project_refactor existed)
- **Rationale**: Underscore prefix indicates meta/system directory; removes temporal connotation
- **Executed On**: 2026-02-01
- **Related Files**:
  - `ontologia-cf/_domain/` (renamed from `project_refactor/`)
  - `bnpl-funil/_domain/` (renamed from `project_refactor/`)
  - Updated: `DOMAIN_REGISTRY.yaml`, `CAPABILITY_MATRIX.yaml`, `START_HERE_ECOSYSTEM.md`

### 1.3 Replace `_REFACTOR` suffix
- **Status**: ✅ Decided + Executed
- **Decision**: `*_REFACTOR.md` → `*_SEMANTIC.md` (or `*.md` for main entry points)
- **Rationale**: Removes temporal versioning from filenames; semantic suffix indicates agent-optimized docs
- **Executed On**: 2026-02-01
- **Stats**: 48 files renamed total
- **Related Files**:
  - `START_HERE_REFACTOR.md` → `START_HERE.md`
  - `ENTITY_INDEX_REFACTOR.yaml` → `ENTITY_INDEX.yaml`
  - `BUDGETS_REFACTOR.md` → `BUDGETS_SEMANTIC.md` (and 35 others)

### 1.4 Folder naming convention
- **Status**: ✅ Decided + Executed
- **Decision**: `_domain/`, `_docs/`, `_governance/` for meta; `src/`, `data/`, `config/` for code
- **Rationale**: Underscore prefix = system/meta folders; clear separation of concerns
- **Executed On**: 2026-02-01
- **Related Files**: All project root directories

---

## 2. Data Layer Architecture

### 2.4 Add client_voice PG credentials
- **Status**: ✅ Decided + Executed
- **Decision**: `vox_popular` database on AWS RDS
- **Rationale**: Dedicated database for client-voice data (hot layer)
- **Executed On**: 2026-02-01
- **Related Files**:
  - `capim-meta-ontology/.env` (credentials added)
  - `capim-meta-ontology/scripts/test_pg_connection.py` (test script)

---

## 3. Tooling & Agents

### 3.1 Replace n8n with Cursor Subagents
- **Status**: ❌ Rejected
- **Decision**: Keep n8n for batch classification
- **Rationale**: n8n is better for scheduled, autonomous processing; Cursor subagents are for on-demand tasks
- **Rejected On**: 2026-01-31

---

## 4. Client-Voice Improvements

### 4.2 Integrate with meta-ontology
- **Status**: ✅ Decided + Executed
- **Decision**: Created `START_HERE.md` and `ENTITY_INDEX.yaml`
- **Rationale**: All 3 domains now integrated into federation layer
- **Executed On**: 2026-02-01
- **Related Files**:
  - `client-voice/START_HERE.md`
  - `client-voice/_docs/ENTITY_INDEX.yaml`
  - `DOMAIN_REGISTRY.yaml`, `CAPABILITY_MATRIX.yaml`

---

## Session Accomplishments (2026-02-01)

### Structural Changes
- Renamed `project_refactor/` → `_domain/` in SAAS and FINTECH
- Renamed 48 files to remove `_REFACTOR` suffix
- Consolidated `docs/` into `_docs/` in CLIENT_VOICE
- Cleaned up empty folders (`@temp/`, `scripts/`)
- Deleted `vibe coding/` folder

### Documentation Updates
- Rewrote `docs/START_HERE.md` (SAAS + FINTECH) for agent optimization
- Added cross-links between operational and semantic guides
- Updated all federation files with new paths
- Fixed `.env` syntax issues

### Infrastructure
- Tested PostgreSQL connection to `vox_popular`
- Updated `session-start.md` workflow with correct paths

---

## Patterns Learned

1. **Underscore prefix = meta/system**: `_domain/`, `_docs/`, `_memory/`
2. **No temporal suffixes**: Use Git for versioning, not `_V2`, `_REFACTOR`
3. **Two-layer documentation**: `docs/START_HERE.md` (operational) + `_domain/START_HERE.md` (semantic)
4. **Decision-centric sessions**: Save immediately, archive at session end
