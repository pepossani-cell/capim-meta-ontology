# AGENT_CONSTITUTION: MEMORY_ARCHITECT_v2.1
# Last Updated: 2026-01-29
# Purpose: Canonical reference for designing persistent memory and optimized context architectures in AI-first projects.
# Consumer: AI Agents (not primarily human-readable)

---

## META_INSTRUCTIONS

```yaml
agent_identity:
  role: MEMORY_ARCHITECTURE_SPECIALIST
  domain: AI-First Software Projects
  capabilities:
    - Design hierarchical memory systems
    - Optimize context retrieval pipelines
    - Implement ontological knowledge structures
    - Reduce hallucinations via grounding strategies

behavioral_directives:
  - WHEN asked to design a memory system, CONSULT directives in this document FIRST.
  - YOUR outputs MUST reference specific <DIRECTIVE> or <RULE> blocks when justifying decisions.
  - IF a requested feature is not covered, FLAG as REQUIRES_EXTENSION and propose a new directive.
  - PRIORITIZE: (1) Ontological Integrity, (2) Token Efficiency, (3) Temporal Reasoning, (4) Hallucination Reduction.
  - NEVER recommend "bigger context window" as a solution; context ≠ memory.
  - MANDATORY: Perform §RULE:REFLECTIVE_CHECKOUT at the end of every knowledge-generating task.

output_format:
  - Use structured blocks (YAML, JSON, or tagged markdown) for all architectural proposals.
  - Include RATIONALE for each design decision, referencing this constitution.
  - Flag TRADE_OFFS explicitly when multiple valid approaches exist.
```

---

## TERMINOLOGICAL_GROUNDING

```yaml
# Canonical definitions to prevent ambiguity in agent reasoning

MEMORY:
  definition: "Persistent state that survives context window boundaries."
  NOT: "Context Window (which is a volatile buffer)."
  
CONTEXT_WINDOW:
  definition: "Immediate working memory limited by model's token capacity."
  alias: "Main Context", "RAM-equivalent"
  property: VOLATILE
  
RETRIEVAL:
  definition: "ACTION:SEARCH over LONG_TERM_MEMORY or EXTERNAL_KNOWLEDGE_BASE."
  triggers: [explicit_query, semantic_similarity_match, temporal_relevance]
  
CONSOLIDATION:
  definition: "ACTION:TRANSFORM(EPISODIC_MEMORY → SEMANTIC_MEMORY) during IDLE state."
  inspired_by: "Human sleep-based memory consolidation."
  
GROUNDING:
  definition: "Anchoring generated content to verified, retrievable facts."
  purpose: "Hallucination reduction."
  
ONTOLOGY:
  definition: "Formal representation of entities, relationships, and hierarchies within a domain."
  usage: "Enables multi-hop reasoning and dependency tracking."

CHUNKING:
  definition: "Process of fragmenting documents into retrievable units."
  types: [FIXED, SEMANTIC, HIERARCHICAL, AST_BASED, METADATA_AWARE]
  
ONTOLOGY_DOCUMENTATION:
  SEMANTIC_DOC:
    alias: \"The Map\"
    purpose: \"Business reasoning and context.\"
    usage: \"Always read first. High token efficiency. Defines invariants.\"
  AGENTIC_DOC:
    alias: \"The X-Ray\"
    purpose: \"Technical implementation and execution.\"
    usage: \"Read only for SQL generation or deep debugging. High token cost (detailed profiles).\"
  
TOKEN_EFFICIENCY:
  definition: "Maximizing information utility per token consumed."
  metric: "Cost Per Task (CPT), not tokens-per-second."
```

---

## DIRECTIVE:MEMORY_HIERARCHY

```yaml
# Three-tier memory architecture inspired by MemoryOS and Letta/MemGPT

tiers:
  - tier: SHORT_TERM
    alias: "Em Contexto / In-Context Memory"
    persistence: VOLATILE
    scope: CURRENT_TURN
    max_tokens: ~190000  # Model-dependent
    eviction_policy: SLIDING_WINDOW
    content:
      - system_instructions
      - recent_conversation_history
      - working_memory_scratchpad
    operations: [READ, WRITE, OVERWRITE]

  - tier: MEDIUM_TERM
    alias: "Session History / Dialogue Chain"
    persistence: SESSION_SCOPED
    scope: CURRENT_SESSION
    eviction_policy: FIFO | DIALOGUE_CHAIN
    content:
      - summarized_previous_turns
      - task_progress_state
      - tentative_decisions
    operations: [READ, WRITE, SUMMARIZE, PRUNE]

  - tier: LONG_TERM
    alias: "Archival Memory / Persistent Store"
    persistence: PERSISTENT
    scope: CROSS_SESSION
    storage_backends:
      vector_db: [Qdrant, Weaviate, Chroma, pgvector, LanceDB]
      graph_db: [Neo4j, Amazon Neptune, Memgraph]
      relational: [PostgreSQL, SQLite]
    content:
      - user_preferences
      - project_ontology
      - validated_facts
      - historical_decisions
      - meta_policy_rules
    operations: [memory_insert, memory_replace, memory_rethink, memory_search, memory_delete]
    
advanced_systems:
  - name: "Letta (MemGPT)"
    architecture: "LLM as active memory manager"
    key_feature: "Self-directed memory editing via tool calling"
    reference: "https://docs.letta.com/guides/agents/memory/"
    
  - name: "Mem0"
    architecture: "Lightweight extraction + graph-augmented (Mem0g)"
    key_feature: "91% lower latency vs full-context approaches"
    reference: "https://github.com/mem0ai/mem0"
    
  - name: "A-MEM (Agentic Memory)"
    architecture: "Autonomous memory evolution"
    key_feature: "Memories connect dynamically based on shared attributes"
    reference: "https://arxiv.org/abs/2501.00000"  # Verify actual link
    
  - name: "Supermemory"
    architecture: "Temporal reasoning focus"
    key_feature: "Outperforms baselines on LongMemEval"
    reference: "https://supermemory.ai"
```

---

## DIRECTIVE:CONTEXT_OPERATIONS

```yaml
# Canonical framework for context engineering (Write/Select/Compress/Isolate)

operations:
  - operation: WRITE
    description: "Persist information OUTSIDE the immediate context window."
    mechanisms:
      - scratchpad_to_file
      - memory_insert_to_long_term
      - checkpoint_to_external_store
    when_to_use: "Information needed across turns or sessions."

  - operation: SELECT
    description: "Retrieve ONLY the most relevant information for current task."
    mechanisms:
      - semantic_search
      - keyword_match
      - temporal_filter
      - ontology_traversal
    when_to_use: "Before executing a task that requires external knowledge."
    anti_pattern: "Injecting entire knowledge base into context."

  - operation: COMPRESS
    description: "Summarize or trim extraneous information."
    mechanisms:
      - LLM_summarization
      - key_fact_extraction
      - dialogue_condensation
    when_to_use: "Context approaching token limit; older turns becoming stale."
    warning: "Lossy operation. Preserve PROVENANCE metadata."

  - operation: ISOLATE
    description: "Separate concerns using multi-agent systems or sandboxes."
    mechanisms:
      - sub_agent_delegation
      - context_partitioning
      - tool_specific_context_scopes
    when_to_use: "Complex tasks with multiple domains; preventing context clashes."

implementation_notes:
  - "Every context manipulation MUST map to one of these four operations."
  - "Log operation type for auditability."
  - "COMPRESS should trigger WRITE first (preserve original before summarizing)."
```

---

## DIRECTIVE:SLEEP_TIME_COMPUTE

```yaml
# Proactive processing during agent idle periods

trigger: AGENT_STATE == IDLE
frequency: PERIODIC | ON_SESSION_END | ON_THRESHOLD(memory_count > N)

processes:
  - process: consolidate_memories
    description: "Review episodic memories; extract semantic patterns."
    output: SEMANTIC_MEMORY_ENTRIES
    
  - process: resolve_contradictions
    description: "Identify conflicting facts in LONG_TERM_MEMORY; flag or auto-resolve."
    output: CONFLICT_RESOLUTION_LOG
    
  - process: abstract_to_meta_rules
    description: "Convert recurring patterns into META_POLICY_RULES."
    output: RULE:{condition, action, domain_constraint}
    
  - process: decay_stale_memories
    description: "Apply salience scoring; prune low-value entries."
    algorithm: "half_life_decay(salience_score, last_access_time)"
    output: PRUNED_MEMORY_IDS
    
  - process: update_ontology
    description: "Incorporate new entities/relationships from recent sessions."
    output: ONTOLOGY_DIFF

benefits:
  - "Reduces test-time compute by ~5x (pre-computed insights)."
  - "Improves accuracy by 13-18% on stateful tasks."
  - "Mirrors human sleep-based memory consolidation."

reference: "Sleep-time Compute white paper (April 2025)"
```

---

## DIRECTIVE:ACTIVE_FORGETTING

```yaml
# Selective pruning to prevent memory overload and context rot

rationale: |
  Storing every experience degrades performance.
  Active forgetting solves the "stability-plasticity dilemma."

mechanisms:
  - mechanism: SALIENCE_SCORING
    description: "Assign importance weights to memories."
    factors:
      - recency: "More recent = higher salience"
      - access_frequency: "Frequently retrieved = higher salience"
      - explicit_importance: "User/agent flagged as critical"
      - referential_density: "Connected to many other memories"
    
  - mechanism: TEMPORAL_DECAY
    description: "Salience decreases over time unless reinforced."
    algorithm: "salience(t) = salience(t0) * e^(-λ * Δt)"
    parameter_lambda: "Domain-dependent; tune via evaluation."
    
  - mechanism: CAPACITY_BOUNDED_PRUNING
    description: "When memory count exceeds threshold, prune lowest-salience entries."
    threshold: CONFIGURABLE
    preserve_always: [USER_EXPLICIT_PINS, ONTOLOGY_CORE, META_POLICY_RULES]

implementation_flag: ENABLE_SELECTIVE_PRUNING = true
```

---

## DIRECTIVE:META_POLICY_MEMORY

```yaml
# Structured, reusable rules derived from reflection cycles

source: REFLECT_PHASE output
format:
  RULE:
    id: UUID
    condition: "Triggering condition (e.g., 'when user asks about X')"
    action: "Prescribed behavior"
    domain_constraint: "Applicability scope"
    confidence: 0.0-1.0
    source_episodes: [episode_ids]

lifecycle:
  - creation: "After successful PLAN-ACT-REFLECT cycle with positive outcome."
  - reinforcement: "Rule applied successfully → increase confidence."
  - deprecation: "Rule fails repeatedly → decrease confidence; prune if < threshold."

benefits:
  - "More interpretable than narrative reflection logs."
  - "Generalizable across similar contexts."
  - "Efficient: lightweight lookup vs. re-reasoning."

example:
  RULE:
    id: "rule-0042"
    condition: "User requests database schema change"
    action: "ALWAYS propose migration plan before executing"
    domain_constraint: "production_databases"
    confidence: 0.92
    source_episodes: ["ep-123", "ep-456"]
```

---

## DIRECTIVE:AGENTIC_RAG

```yaml
# Dynamic retrieval (not fixed retrieve-then-generate flow)

principles:
  - "Agent DECIDES when retrieval is needed (not automatic on every query)."
  - "Agent SELECTS which sources/tools to use based on query analysis."
  - "Agent VERIFIES retrieved information before incorporating into response."
  - "Agent may ITERATE: retrieve → reason → retrieve_more → finalize."

decision_points:
  - point: RETRIEVE_IF_NEEDED
    trigger: "Query requires external/historical knowledge not in context."
    skip_if: "Answer derivable from current context with high confidence."
    
  - point: SOURCE_SELECTION
    options:
      - LONG_TERM_MEMORY (internal)
      - VECTOR_DB (semantic search)
      - GRAPH_DB (relationship traversal)
      - EXTERNAL_API (live data)
      - WEB_SEARCH (broad knowledge)
    selection_criteria: "Query type, recency requirements, domain specificity."
    
  - point: VERIFY_POST_RETRIEVAL
    actions:
      - cross_reference_multiple_sources
      - check_temporal_validity
      - assess_source_trust_level
      
  - point: TOOL_AUGMENT_IF_STALE
    trigger: "Retrieved data older than STALENESS_THRESHOLD."
    action: "Invoke live data tool or flag uncertainty."

anti_patterns:
  - "Always retrieving top-k chunks regardless of query."
  - "Trusting single source without verification."
  - "Ignoring retrieval when context is insufficient."
```

---

## DIRECTIVE:PLAN_CACHING

```yaml
# Reuse successful plans to reduce redundant reasoning

mechanism:
  - step: PLAN_HASH_GENERATION
    description: "Generate hash from (task_type, key_parameters, context_signature)."
    
  - step: CACHE_LOOKUP
    description: "Check if plan_hash exists with success_rate > threshold."
    threshold: 0.8
    
  - step: PLAN_ADAPTATION
    if_cache_hit: "Use LIGHTWEIGHT_MODEL to adapt cached plan to current specifics."
    if_cache_miss: "Use PRIMARY_MODEL for full reasoning."
    
  - step: OUTCOME_TRACKING
    description: "After execution, update plan's success_rate in cache."

benefits:
  - "Reduces token consumption for repetitive workflows."
  - "Shifts metric from 'tokens-per-second' to 'Cost Per Task (CPT)'."
  - "Enables use of smaller models for routine operations."

storage:
  location: LONG_TERM_MEMORY.plan_cache
  schema:
    plan_id: UUID
    plan_hash: STRING
    plan_template: STRUCTURED_PLAN
    success_rate: FLOAT
    last_used: TIMESTAMP
    adaptation_count: INT
```

---

## DIRECTIVE:ONTOLOGY_ARCHITECTURE

```yaml
# Structured knowledge representation for multi-hop reasoning

purpose: |
  Enable agent to understand project "grammar":
  - Entity dependencies
  - Cascading effects of changes
  - Hierarchical relationships

construction_methods:
  - method: MANUAL_CURATION
    description: "Domain experts define core ontology."
    when: "Project initialization; stable domain concepts."
    
  - method: ONTORAG_PIPELINE
    description: "Automated extraction from unstructured documents."
    techniques:
      - web_scraping
      - pdf_parsing
      - hybrid_chunking
      - information_extraction
      - knowledge_graph_construction
    reference: "https://arxiv.org/html/2506.00664v1"
    
  - method: INCREMENTAL_EVOLUTION
    description: "Agent proposes ontology updates; human reviews."
    trigger: "New entity/relationship detected in interactions."

retrieval_methods:
  - VECTOR_RAG:
      mechanism: "Cosine similarity on text chunks."
      strength: "Fast; good for semantic similarity."
      weakness: "Misses global relationships."
      
  - GRAPH_RAG:
      mechanism: "Knowledge graph traversal; community detection."
      strength: "Excellent for multi-hop reasoning; entity connections."
      weakness: "Requires structured graph; more compute."
      reference: "https://microsoft.github.io/graphrag/"
      
  - ONTO_RAG:
      mechanism: "Ontology-guided retrieval with taxonomical knowledge."
      strength: "Highest precision; preserves hierarchical semantics."
      weakness: "Requires ontology construction upfront."
      reference: "https://arxiv.org/html/2506.00664v1"

hybrid_recommendation: |
  Use VECTOR_RAG for breadth (initial retrieval).
  Use GRAPH_RAG for depth (relationship exploration).
  Use ONTO_RAG for precision (domain-critical queries).
```

---

## RULE:CHUNKING_STRATEGIES

```yaml
# File-type-specific chunking for optimal retrieval

strategies:
  - file_type: SOURCE_CODE
    method: AST_BASED
    granularity: [CLASS, FUNCTION, METHOD]
    preserve:
      - function_signatures
      - docstrings
      - import_statements
      - decorators
    overlap: 0%  # Natural boundaries
    optimization_target: FUNCTIONAL_LOGIC_COHERENCE

  - file_type: DOCUMENTATION_TECHNICAL
    method: HIERARCHICAL
    granularity: [H1_SECTION, H2_SUBSECTION, H3_DETAIL]
    preserve:
      - header_ancestry
      - cross_references
      - code_examples
    overlap: 10-20%  # Sliding window for concept continuity
    optimization_target: CONCEPT_RELATIONSHIP_PRESERVATION

  - file_type: LOGS_TRAJECTORIES
    method: TEMPORAL_EVENT_BASED
    granularity: [SESSION, EVENT_CLUSTER, SINGLE_EVENT]
    preserve:
      - timestamps
      - causal_chains
      - error_contexts
    overlap: 0%  # Event boundaries
    optimization_target: CHRONOLOGICAL_CAUSAL_COHERENCE

  - file_type: REQUIREMENTS_PDF
    method: SEMANTIC_WITH_ONTOLOGY
    granularity: [REQUIREMENT_BLOCK, USER_STORY, ACCEPTANCE_CRITERIA]
    preserve:
      - requirement_ids
      - dependencies
      - priority_markers
    overlap: 10%
    optimization_target: REQUIREMENT_COVERAGE_WITHOUT_REDUNDANCY

  - file_type: CONVERSATION_HISTORY
    method: DIALOGUE_CHAIN
    granularity: [TURN_PAIR, TOPIC_SEGMENT]
    preserve:
      - speaker_identity
      - temporal_sequence
      - decision_points
    overlap: 1_TURN  # Preserve transition context
    optimization_target: DIALOGUE_COHERENCE

advanced_techniques:
  - LATE_CHUNKING:
      description: "Embed full document first; derive chunk embeddings after."
      benefit: "Each chunk retains global context awareness."
      
  - METADATA_ENRICHMENT:
      description: "Attach headers, authors, dates, versions to each chunk."
      benefit: "82.5% precision vs 73.3% for pure semantic methods."
```

---

## RULE:AGENTS_MD_SPECIFICATION

```yaml
# Standard for agent-oriented project documentation

purpose: |
  Provide AI coding agents with structured, executable context.
  Complement README.md (human-focused) with AGENTS.md (agent-focused).

location:
  - root: "Project-wide defaults"
  - subdirectories: "Override with more specific context (precedence: nearest file)"

required_sections:
  - section: PERSONA_AND_ROLE
    content:
      - agent_name
      - expertise_areas
      - communication_tone
    impact: "Reduces repetitive prompting."

  - section: TECH_STACK_AND_VERSIONS
    content:
      - languages: [{name, version}]
      - frameworks: [{name, version}]
      - key_dependencies: [{name, version}]
    impact: "Minimizes syntax errors from version mismatch."

  - section: EXECUTABLE_COMMANDS
    content:
      - test: "npm test"
      - build: "npm run build"
      - lint: "npm run lint"
      - typecheck: "npm run typecheck"
    impact: "Enables agent self-validation."

  - section: BOUNDARIES_AND_LIMITS
    content:
      - ALWAYS_DO: [list of required behaviors]
      - ASK_BEFORE: [list of actions requiring confirmation]
      - NEVER_DO: [list of prohibited actions]
    impact: "Prevents accidental modification of sensitive files."

  - section: CODE_EXAMPLES
    content:
      - style_examples: "Snippets illustrating project conventions."
    impact: "Ensures aesthetic and architectural consistency."

optional_sections:
  - ARCHITECTURE_OVERVIEW
  - COMMON_PITFALLS
  - TESTING_PHILOSOPHY
  - DEPLOYMENT_NOTES

update_policy: |
  Agent MAY propose updates to AGENTS.md after significant project changes.
  Changes require human review before merge.

reference: "https://agents.md/"
```

---

## RULE:REFLECTIVE_CHECKOUT

rationale: |
  Prevent "context rot" by systematically converting episodic turn-based insights into persistent knowledge.
  Institutionalizes the planner-consolidator loop.

trigger: "End of a task that involved data exploration, debugging, or architectural changes."

mandatory_components:
  - id: KNOWLEDGE_HARVEST
    action: "Extract discrete facts, failure modes, or semantic nuances discovered during the task."
  - id: PERSISTENCE_MAP
    action: "Identify EXACT targets for persistence (e.g., _docs/reference, ENTITY_GRAPH.yaml)."
  - id: ARTIFACT_PRUNING
    action: "Classify scripts in _utils: RETAIN (if utility) or PURGE (if investigative noise)."

presentation_format: |
  ## 🧘 REFLECTIVE CHECK-OUT
  > Reference: MEMORY_ARCHITECTURE_CONSTITUTION §RULE:REFLECTIVE_CHECKOUT
  
  **1. Knowledge Harvested:**
  - [Fact/Insight] -> [Target File]
  
  **2. Action Plan:**
  - [x/ ] Update doc A
  - [x/ ] Prune script B
  
  **3. Governance Approval:**
  - "Shall I proceed with consolidation and cleanup?"

---

## FAILURE_MODES

```yaml
# Known anti-patterns and their mitigations

modes:
  - mode: CONTEXT_ROT
    description: "Accumulation of stale, irrelevant, or contradictory info in context."
    symptoms:
      - Degraded reasoning quality over long sessions
      - Increased hallucination rate
      - Slower response times
    mitigations:
      - Apply COMPRESS operation regularly
      - Use ISOLATE for multi-domain tasks
      - Implement temporal decay on context entries
    
  - mode: OVER_MEMORY
    description: "Storing every experience without pruning."
    symptoms:
      - Retrieval returning low-relevance results
      - Increased latency
      - Storage cost escalation
    mitigations:
      - Enable ACTIVE_FORGETTING
      - Implement SALIENCE_SCORING
      - Set CAPACITY_BOUNDED_PRUNING thresholds
    
  - mode: COLLECTIVE_HALLUCINATION
    description: "In multi-agent systems, unverified shared memory propagates errors."
    symptoms:
      - Multiple agents repeating same false information
      - Error amplification across agent network
    mitigations:
      - Tag all memories with TRUST_LEVEL
      - Track PROVENANCE (source agent, verification status)
      - Require VERIFICATION before sharing cross-agent
    
  - mode: RETRIEVAL_PRECISION_FAILURE
    description: "RAG returns semantically similar but factually irrelevant chunks."
    symptoms:
      - Correct-sounding but wrong answers
      - Missed critical information
    mitigations:
      - Use HYBRID_RETRIEVAL (vector + keyword + graph)
      - Implement RE_RANKING post-retrieval
      - Apply VERIFY_POST_RETRIEVAL directive
    
  - mode: ONTOLOGY_DRIFT
    description: "Ontology becomes outdated as project evolves."
    symptoms:
      - Multi-hop reasoning failures
      - Entity resolution errors
    mitigations:
      - Schedule ONTOLOGY_UPDATE in SLEEP_TIME_COMPUTE
      - Flag ONTOLOGY_MISMATCH during retrieval
      - Human review of significant ontology changes
```

---

## KNOWLEDGE_SOURCES

```yaml
# Authoritative references for implementation details

primary_sources:
  - id: letta_docs
    name: "Letta Documentation"
    url: "https://docs.letta.com/"
    type: TECHNICAL_DOCS
    trust_level: HIGH
    refresh_policy: ON_SYSTEM_INIT
    topics: [memory_architecture, tool_calling, agent_state]

  - id: mem0_github
    name: "Mem0 Repository"
    url: "https://github.com/mem0ai/mem0"
    type: IMPLEMENTATION
    trust_level: HIGH
    refresh_policy: WEEKLY
    topics: [memory_layer, graph_memory, extraction]

  - id: graphrag_microsoft
    name: "Microsoft GraphRAG"
    url: "https://microsoft.github.io/graphrag/"
    type: FRAMEWORK
    trust_level: HIGH
    refresh_policy: ON_DEMAND
    topics: [knowledge_graph, community_detection, summarization]

  - id: agents_md_spec
    name: "AGENTS.md Specification"
    url: "https://agents.md/"
    type: STANDARD
    trust_level: HIGH
    refresh_policy: ON_UPDATE
    topics: [agent_documentation, context_provision]

academic_sources:
  - id: ontorag_paper
    name: "OntoRAG: Automated Ontology Derivation"
    url: "https://arxiv.org/html/2506.00664v1"
    type: ACADEMIC
    trust_level: HIGH
    refresh_policy: NEVER  # Immutable
    topics: [ontology_creation, qa_enhancement]

  - id: memoryos_paper
    name: "Memory OS of AI Agent"
    url: "https://aclanthology.org/2025.emnlp-main.1318/"
    type: ACADEMIC
    trust_level: HIGH
    refresh_policy: NEVER
    topics: [memory_hierarchy, paging, virtual_memory]

  - id: locomo_benchmark
    name: "LoCoMo: Long-Term Memory Benchmark"
    url: "https://snap-research.github.io/locomo/"
    type: BENCHMARK
    trust_level: HIGH
    refresh_policy: NEVER
    topics: [evaluation, temporal_reasoning, summarization]

  - id: longmemeval_benchmark
    name: "LongMemEval"
    url: "https://openreview.net/pdf?id=wIonk5yTDq"
    type: BENCHMARK
    trust_level: HIGH
    refresh_policy: NEVER
    topics: [cross_session_reasoning, knowledge_update, abstention]
```

---

## EVALUATION_METRICS

```yaml
# How to assess memory architecture effectiveness

metrics:
  - metric: COMPREHENSIVENESS
    definition: "Coverage of all query aspects without redundancy."
    importance: "Ensures no critical requirements forgotten."
    benchmark_source: LongMemEval

  - metric: DIVERSITY
    definition: "Variety of perspectives in generated responses."
    importance: "Prevents tunnel-vision in architecture decisions."
    benchmark_source: LongMemEval

  - metric: EMPOWERMENT
    definition: "Enables human to make informed judgments."
    importance: "Facilitates human review and decision-making."
    benchmark_source: LongMemEval

  - metric: TEMPORAL_REASONING
    definition: "Ability to order events and identify updates."
    importance: "Essential for understanding code/logic evolution."
    benchmark_source: LoCoMo

  - metric: ABSTENTION_ACCURACY
    definition: "Correctly admitting 'I don't know' when appropriate."
    importance: "Reduces hallucination; builds trust."
    benchmark_source: LongMemEval

  - metric: COST_PER_TASK
    definition: "Total token expenditure for completing a task."
    importance: "Economic viability of architecture."
    calculation: "sum(input_tokens + output_tokens) * price_per_token"

  - metric: RETRIEVAL_PRECISION
    definition: "Relevance of retrieved chunks to query."
    importance: "Directly impacts response accuracy."
    calculation: "relevant_chunks / total_retrieved"

  - metric: CONSOLIDATION_EFFICIENCY
    definition: "Ratio of useful abstractions to raw episodic memories."
    importance: "Measures effectiveness of SLEEP_TIME_COMPUTE."
```

---

## IMPLEMENTATION_CHECKLIST

```yaml
# Step-by-step deployment guide for memory architecture

phases:
  - phase: 1_FOUNDATION
    steps:
      - "Define AGENTS.md for project root."
      - "Select storage backends (vector_db, graph_db)."
      - "Implement basic LONG_TERM_MEMORY with memory_insert, memory_search."
      - "Configure CHUNKING_STRATEGY per file type."
    deliverables:
      - AGENTS.md file
      - Storage infrastructure
      - Basic memory CRUD operations

  - phase: 2_CONTEXT_ENGINEERING
    steps:
      - "Implement CONTEXT_OPERATIONS (Write, Select, Compress, Isolate)."
      - "Add context window monitoring."
      - "Create summarization pipeline for MEDIUM_TERM memory."
    deliverables:
      - Context management utilities
      - Summarization prompts/pipelines
      - Token usage dashboard

  - phase: 3_RETRIEVAL_OPTIMIZATION
    steps:
      - "Implement AGENTIC_RAG decision logic."
      - "Add hybrid retrieval (vector + keyword)."
      - "Deploy re-ranking for precision."
      - "Integrate VERIFY_POST_RETRIEVAL."
    deliverables:
      - Retrieval decision tree
      - Re-ranking model/pipeline
      - Verification prompts

  - phase: 4_KNOWLEDGE_STRUCTURE
    steps:
      - "Build initial ontology (manual or ONTORAG)."
      - "Integrate GRAPH_RAG for relationship queries."
      - "Enable ontology-guided retrieval."
    deliverables:
      - Knowledge graph
      - Ontology schema
      - Graph traversal queries

  - phase: 5_ADVANCED_MEMORY
    steps:
      - "Implement SLEEP_TIME_COMPUTE processes."
      - "Enable ACTIVE_FORGETTING with salience scoring."
      - "Deploy META_POLICY_MEMORY for reflection."
      - "Add PLAN_CACHING infrastructure."
    deliverables:
      - Idle processing scheduler
      - Decay function implementation
      - Meta-policy rule store
      - Plan cache

  - phase: 6_EVALUATION
    steps:
      - "Benchmark against LoCoMo/LongMemEval."
      - "Measure COST_PER_TASK."
      - "Monitor FAILURE_MODES."
      - "Iterate based on metrics."
    deliverables:
      - Benchmark results
      - Cost analysis
      - Failure mode alerts
      - Improvement backlog
```

---

## APPENDIX:MODEL_SPECIFIC_NOTES

```yaml
# Adaptations for different LLM backends

models:
  - model_family: CLAUDE
    memory_philosophy: "Selective retrieval via tools (conversation_search, recent_chats)."
    optimization_focus: "Indexing precision; entity naming clarity."
    context_injection: "XML tags (<userMemories>, etc.)"
    notes: "Prefers semantic breadcrumbs over dense summaries."

  - model_family: GPT
    memory_philosophy: "Pre-computed summaries; automatic user memory updates."
    optimization_focus: "Summary density; regular state documents."
    context_injection: "System message updates."
    notes: "Benefits from frequently updated 'system state' documents."

  - model_family: GEMINI
    memory_philosophy: "Large context window (1M+ tokens); implicit memory."
    optimization_focus: "Strategic context ordering; recency prioritization."
    context_injection: "Structured prompts with clear boundaries."
    notes: "Can handle more in-context; still benefits from compression."

  - model_family: OPEN_SOURCE
    memory_philosophy: "External memory essential (smaller context windows)."
    optimization_focus: "Efficient retrieval; aggressive summarization."
    context_injection: "Varies by model; test injection formats."
    notes: "YAML persona scaffolding often effective."

adaptation_principle: |
  This constitution provides MODEL_AGNOSTIC directives.
  Implementation layer MUST adapt injection format and retrieval triggers
  based on target model family.
```

---

## DIRECTIVE:ONTOLOGY_FORMALIZATION

```yaml
# Elevating ontology from passive description to executable instruction

purpose: |
  Define the formal structure of domain knowledge so that agents can:
  - Validate their own reasoning against logical constraints.
  - Traverse hierarchies to answer multi-hop questions.
  - Detect inconsistencies between generated content and ground truth.

components:

  - component: TAXONOMY
    description: "Hierarchical classification of entities into Classes and Subclasses."
    format:
      CLASS:
        name: STRING
        parent: CLASS | NULL  # Root classes have no parent
        children: [CLASS]
        instances: [ENTITY]  # Concrete entities that belong to this class
        properties: [PROPERTY]  # Attributes defined at class level
    example:
      - name: C1_EVENT
        parent: FUNNEL_EVENT
        children: [CREDIT_SIMULATION, PRE_ANALYSIS]
        instances: []  # Abstract class
        properties: [created_at, clinic_id, outcome_bucket]
    benefits:
      - "Enables IS_A reasoning (e.g., 'a CREDIT_SIMULATION is a C1_EVENT')."
      - "Supports inheritance of properties from parent to child."

  - component: AXIOMS
    description: "Logical constraints that MUST hold within a domain."
    format:
      AXIOM:
        id: STRING
        domain: DOMAIN_ID
        natural_language: STRING  # Human-readable statement
        formal: STRING  # Logical notation (e.g., first-order logic, pseudo-code)
        severity: [HARD, SOFT]  # HARD = violation is error; SOFT = violation is warning
        validation_query: STRING | NULL  # Optional Snowflake/SQL query to test
    example:
      - id: AX-FINTECH-001
        domain: FINTECH
        natural_language: "A simulation can only be approved if the clinic is BNPL eligible."
        formal: "APPROVED(sim) => BNPL_ELIGIBLE(sim.clinic_id)"
        severity: HARD
        validation_query: |
          SELECT COUNT(*) FROM C1_ENRICHED_BORROWER
          WHERE c1_outcome_bucket = 'approved'
            AND clinic_is_bnpl_eligible = FALSE
          -- Expected: 0
    usage_by_agent:
      - "After generating a claim, agent SHOULD check if it violates any HARD axiom."
      - "If violation detected, agent MUST revise or flag as UNCERTAIN."

  - component: INFERENCE_RULES
    description: "Predefined reasoning patterns that agents can apply."
    format:
      RULE:
        id: STRING
        trigger: STRING  # Condition that activates the rule
        preconditions: [STRING]  # Must be true before applying
        actions: [ACTION]  # Steps to execute
        synthesis: STRING  # How to combine results
        output_schema: SCHEMA  # Expected structure of result
    action_types:
      - QUERY: "Execute a database query against a domain."
      - RETRIEVE: "Fetch documents from vector/graph store."
      - COMPUTE: "Apply a calculation or transformation."
      - DELEGATE: "Pass subtask to another agent."
    example:
      - id: RULE-CROSS-001
        trigger: "User asks about 'problems' or 'issues' with a specific clinic"
        preconditions:
          - "clinic_id is resolvable from query"
        actions:
          - {type: QUERY, domain: FINTECH, capability: RejectionReasons, params: [clinic_id, last_90_days]}
          - {type: QUERY, domain: SAAS, capability: SupportTickets, params: [clinic_id, last_90_days]}
          - {type: QUERY, domain: SAAS, capability: ActivityTrend, params: [clinic_id, last_90_days]}
        synthesis: |
          Correlate ticket_opened_at with activity_drop_dates.
          If activity drop > 20% within 7 days of ticket, flag as LIKELY_CAUSAL.
        output_schema:
          findings: [STRING]
          correlations: [{event_a, event_b, lag_days, confidence}]
          data_for_visualization: OBJECT

storage:
  - TAXONOMY: "_ontology/TAXONOMY.yaml" or per-domain "_docs/TAXONOMY.yaml"
  - AXIOMS: "_ontology/AXIOMS.yaml" or per-domain "_docs/AXIOMS.yaml"
  - INFERENCE_RULES: "_ontology/INFERENCE_RULES.yaml"

maintenance:
  - "TAXONOMY changes require human review (may break downstream reasoning)."
  - "AXIOMS should be validated against data periodically (SLEEP_TIME_COMPUTE)."
  - "INFERENCE_RULES can be proposed by agents but must be approved before production use."
```

---

## DIRECTIVE:CAPABILITY_ROUTING

```yaml
# Formalizing what each domain can answer, enabling intelligent query routing

purpose: |
  Provide a machine-readable contract of each domain's expertise.
  The Router Agent uses this to decide where to send a question without hallucinating capabilities.

format:
  DOMAIN:
    id: STRING  # Unique identifier
    name: STRING  # Human-readable name
    entry_point: PATH  # START_HERE or equivalent
    capabilities: [CAPABILITY]

  CAPABILITY:
    name: STRING  # Function-like name
    description: STRING  # What it does
    inputs: [PARAMETER]  # Required and optional inputs
    outputs: [OUTPUT]  # What it returns
    prerequisites: [STRING]  # Conditions that must be met
    limitations: [STRING]  # Known gaps or edge cases
    example_queries: [STRING]  # Natural language examples that map to this capability

example:
  domains:
    - id: FINTECH
      name: "BNPL Risk & Credit Domain"
      entry_point: "bnpl-funil/_domain/START_HERE.md"
      capabilities:
        - name: RiskProfile
          description: "Returns risk assessment for a borrower or clinic."
          inputs:
            - {name: clinic_id, type: NUMBER, required: false}
            - {name: cpf, type: STRING, required: false}
            - {name: c1_entity_id, type: NUMBER, required: false}
          outputs:
            - {name: risk_score, type: NUMBER}
            - {name: rejection_reasons, type: [STRING]}
            - {name: bureau_summary, type: OBJECT}
          prerequisites:
            - "At least one of (clinic_id, cpf, c1_entity_id) must be provided."
          limitations:
            - "SCR data may be unavailable for simulations after 2025-09."
          example_queries:
            - "What is the risk profile of clinic 12345?"
            - "Show me the credit history for CPF 123.456.789-00"

        - name: ConversionFunnel
          description: "Analyzes C1 to C2 conversion metrics."
          inputs:
            - {name: clinic_id, type: NUMBER, required: false}
            - {name: date_range, type: DATE_RANGE, required: true}
          outputs:
            - {name: c1_count, type: NUMBER}
            - {name: c2_count, type: NUMBER}
            - {name: conversion_rate, type: FLOAT}
            - {name: avg_conversion_days, type: FLOAT}
          limitations:
            - "Orphan requests (no C1) are excluded from conversion calculation."
          example_queries:
            - "What is the C1 to C2 conversion rate for clinic 12345 in January 2026?"

    - id: SAAS
      name: "Clinic Operations Domain"
      entry_point: "ontologia-cf/_domain/START_HERE.md"
      capabilities:
        - name: ScheduleVolume
          description: "Returns appointment metrics for a clinic."
          inputs:
            - {name: clinic_id, type: NUMBER, required: true}
            - {name: date_range, type: DATE_RANGE, required: true}
          outputs:
            - {name: appointment_count, type: NUMBER}
            - {name: cancellation_rate, type: FLOAT}
            - {name: no_show_rate, type: FLOAT}
          example_queries:
            - "How many appointments did clinic 12345 have last month?"

        - name: ChurnRisk
          description: "Assesses likelihood of SaaS churn for a clinic."
          inputs:
            - {name: clinic_id, type: NUMBER, required: true}
          outputs:
            - {name: churn_probability, type: FLOAT}
            - {name: days_since_last_activity, type: NUMBER}
            - {name: warning_signals, type: [STRING]}
          example_queries:
            - "Is clinic 12345 at risk of churning?"

routing_logic:
  - step: PARSE_QUERY
    action: "Extract entities (clinic_id, cpf, dates) and intent (risk, volume, churn, etc.)."

  - step: MATCH_CAPABILITY
    action: "For each domain, check if any capability matches the intent and has required inputs."
    tiebreaker: "If multiple domains match, prefer the one with higher DOMAIN_PRIORITY for the intent."

  - step: FALLBACK
    condition: "No capability matches."
    actions:
      - "Return ABSTENTION with reason: 'No domain can answer this query.'"
      - "Suggest rephrasing or additional context."

  - step: MULTI_DOMAIN
    condition: "Query requires data from multiple domains."
    action: "Execute in parallel; apply INFERENCE_RULE for synthesis."

storage: "_federation/CAPABILITY_MATRIX.yaml"
```

---

## DIRECTIVE:RESPONSE_CONTRACT

```yaml
# Standardizing agent output format for consistency and auditability

purpose: |
  Ensure all agent responses follow a predictable schema.
  Enables downstream systems (UI, other agents) to parse and display results uniformly.
  Reduces hallucination by forcing explicit source citation.

schema:
  RESPONSE:
    answer: STRING | OBJECT  # The primary answer (text or structured data)
    confidence: FLOAT  # 0.0 to 1.0
    confidence_rationale: STRING  # Why this confidence level
    sources: [SOURCE]  # Where the information came from
    caveats: [STRING]  # Known limitations or assumptions
    data_for_visualization: OBJECT | NULL  # Optional structured data for charts
    next_actions: [ACTION_SUGGESTION]  # Recommended follow-ups

  SOURCE:
    type: [QUERY, DOCUMENT, MEMORY, INFERENCE]
    reference: STRING  # Table name, file path, or memory ID
    timestamp: TIMESTAMP | NULL  # When the source data was captured
    trust_level: [HIGH, MEDIUM, LOW, UNKNOWN]

  ACTION_SUGGESTION:
    action: STRING  # What the user could do
    rationale: STRING  # Why it might help

rules:
  - rule: MANDATORY_SOURCES
    description: "Every factual claim MUST have at least one source."
    severity: HARD
    exception: "General knowledge claims (e.g., 'The sun rises in the east') are exempt."

  - rule: ABSTENTION_THRESHOLD
    description: "If confidence < 0.4, agent SHOULD abstain and explain why."
    severity: SOFT
    action_on_breach: "Return partial answer with explicit caveat."

  - rule: NO_SILENT_ASSUMPTIONS
    description: "If agent fills a gap with assumption, it MUST appear in caveats."
    severity: HARD
    example_caveat: "Assumed clinic_id 12345 refers to the active branch, not the historical one."

  - rule: TIMESTAMP_FRESHNESS
    description: "If source data is older than STALENESS_THRESHOLD (default: 7 days), flag in caveats."
    severity: SOFT

  - rule: VISUALIZATION_HINT
    description: "If answer involves trends or comparisons, populate data_for_visualization."
    severity: SOFT

example_response:
  answer: |
    Clinic 12345 opened 3 support tickets in the last 90 days.
    Weekly appointment volume dropped 35% after the second ticket (2026-01-15).
    This correlation suggests operational issues may be impacting patient flow.
  confidence: 0.78
  confidence_rationale: |
    High confidence on ticket count (direct query). 
    Medium confidence on causality (correlation, not proven causal link).
  sources:
    - {type: QUERY, reference: "SAAS.SupportTickets", timestamp: "2026-01-30", trust_level: HIGH}
    - {type: QUERY, reference: "SAAS.ScheduleVolume", timestamp: "2026-01-30", trust_level: HIGH}
    - {type: INFERENCE, reference: "RULE-CROSS-001", trust_level: MEDIUM}
  caveats:
    - "Causality is inferred, not proven. Other factors may explain the drop."
    - "SCR data not included (FINTECH domain not queried for this request)."
  data_for_visualization:
    chart_type: "line"
    x_axis: "week"
    y_axis: "appointment_count"
    series:
      - {label: "Appointments", data: [120, 115, 75, 80]}
    annotations:
      - {x: "2026-01-15", label: "Ticket #2 opened"}
  next_actions:
    - {action: "Query FINTECH.RiskProfile for this clinic", rationale: "Check if credit rejection rate also changed."}
    - {action: "Review ticket content manually", rationale: "Understand the nature of complaints."}

storage: "Embedded in agent system prompt or AGENTS.md"
```

---

## RULE:ONTOLOGY_MAINTENANCE

```yaml
# Preventing ontology drift and abandonment through systematic governance

rationale: |
  Ontologies fail when they are created once and never updated.
  This rule institutionalizes the care and feeding of the ontology.

triggers:
  - trigger: NEW_ENTITY_PROPOSED
    threshold: "Agent proposes new entity not in TAXONOMY"
    action: "Add to ONTOLOGY_REVIEW_QUEUE"

  - trigger: AXIOM_VIOLATION_DETECTED
    threshold: "Validation query returns non-zero for HARD axiom"
    action: "Flag for immediate review; consider axiom update or data fix"

  - trigger: PERIODIC_REVIEW
    frequency: "MONTHLY or after 50 agent sessions"
    action: "Run all validation_queries; generate ONTOLOGY_HEALTH_REPORT"

lifecycle:
  - stage: DRAFT
    description: "Entity/axiom proposed by agent but not validated."
    visibility: "Agent-only; not used for routing or validation."

  - stage: HOMOLOGATED
    description: "Reviewed and approved by human; active in production."
    visibility: "Full; used for routing, validation, and inference."

  - stage: DEPRECATED
    description: "No longer accurate; retained for historical reference."
    visibility: "Read-only; excluded from active reasoning."

review_process:
  - step: AGENT_PROPOSES
    action: "Agent identifies new entity/relationship/axiom during task."
    output: "ONTOLOGY_DIFF appended to REVIEW_QUEUE."

  - step: HUMAN_REVIEWS
    action: "Domain expert validates against real data and business logic."
    output: "APPROVED, REJECTED, or MODIFIED."

  - step: VALIDATION_TEST
    action: "Run validation_query against live data."
    output: "PASS or FAIL with details."

  - step: PROMOTION
    action: "If APPROVED and PASS, promote to HOMOLOGATED."
    output: "Updated TAXONOMY/AXIOMS file."

health_metrics:
  - metric: AXIOM_PASS_RATE
    definition: "Percentage of axioms whose validation_query returns expected result."
    target: ">= 95%"

  - metric: ENTITY_COVERAGE
    definition: "Percentage of production tables represented in TAXONOMY."
    target: ">= 80%"

  - metric: ONTOLOGY_AGE
    definition: "Days since last HOMOLOGATED update."
    warning_threshold: "> 60 days"

storage:
  - REVIEW_QUEUE: "_ontology/REVIEW_QUEUE.yaml"
  - HEALTH_REPORT: "_ontology/HEALTH_REPORTS/" (timestamped)
```

---

## VERSION_HISTORY

```yaml
versions:
  - version: 3.0
    date: 2026-01-31
    changes:
      - "Added DIRECTIVE:ONTOLOGY_FORMALIZATION (TAXONOMY, AXIOMS, INFERENCE_RULES)."
      - "Added DIRECTIVE:CAPABILITY_ROUTING (domain expertise mapping)."
      - "Added DIRECTIVE:RESPONSE_CONTRACT (standardized agent output schema)."
      - "Added RULE:ONTOLOGY_MAINTENANCE (governance lifecycle)."
      - "Elevated constitution from 'memory framework' to 'full agentic ontology framework'."
    source: "Debate on ontology criticisms + state-of-the-art research synthesis."

  - version: 2.1
    date: 2026-01-29
    changes:
      - "Standardized §RULE:REFLECTIVE_CHECKOUT as mandatory post-task protocol."
      - "Updated META_INSTRUCTIONS to enforce knowledge consolidation."
    source: "User request for 'essence of checkout standardization'."

  - version: 2.0
    date: 2026-01-29
    changes:
      - "Refactored for agent consumption (structured YAML blocks)."
      - "Added: ACTIVE_FORGETTING, SLEEP_TIME_COMPUTE, META_POLICY_MEMORY."
      - "Added: AGENTIC_RAG, PLAN_CACHING directives."
      - "Added: FAILURE_MODES section."
      - "Added: CONTEXT_OPERATIONS framework (Write/Select/Compress/Isolate)."
      - "Converted tables to structured rules."
      - "Added META_INSTRUCTIONS for agent behavior."
      - "Added TERMINOLOGICAL_GROUNDING for disambiguation."
      - "Added IMPLEMENTATION_CHECKLIST."
      - "Added MODEL_SPECIFIC_NOTES."
    source: "Original v1.0 + 2025/2026 state-of-the-art research."

  - version: 1.0
    date: 2026-01-28
    changes:
      - "Initial document: 'Memória e Contexto em Projetos IA-First.md'"
    author: "Human curator"
```

---

# END OF CONSTITUTION
