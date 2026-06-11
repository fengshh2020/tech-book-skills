# Sub-Agent Orchestration Protocol

> For use across all phases of integrate-books. Defines sub-agent concurrency control, dependency ordering, error recovery, and progress tracking.
> Core problem: LLM agents have limited parallelism (typically 3-5), web-based source books have link/reference ordering dependencies, and unconstrained execution leads to resource contention and context loss.

## Global Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | **5** | Balance speed and resources |
| Single agent timeout | 10 minutes | Prevent hung agents |
| Failure retry count | **1** | Failing twice the same way = the approach is wrong |
| Single agent context limit | ~50k tokens | Avoid quality degradation from excessive context |

## Per-Phase Orchestration Strategy

### Phase 0: Deep Reading

**Goal**: Generate a knowledge index of >=1000 lines for each book.

**Orchestration model**: One agent per book, chapters executed sequentially within each book.

#### Sub-Phase Orchestration

| Sub-Phase | Agent Model | Description |
|-----------|-------------|-------------|
| 0.1 | Single agent | Inventory -- scan all source books, record metadata (title, chapter count, format), determine processing order. Output: inventory list to `.book-doc/inventory.md`. |
| 0.2 | One agent per book, max 3 parallel | Deep reading -- each agent reads one book chapter-by-chapter in strict sequence, writing interim progress after each chapter. Sequential chapters within a book; up to 3 books processed in parallel across agents. Output: per-chapter reading evidence and draft index entries. |
| 0.3 | One agent per book, max 3 parallel | Index generation -- consolidate per-chapter draft entries into the final `index.md` for each book. Can run in parallel with sub-phase 0.2 for different books (i.e., once Book A's reading agent finishes, its index-generation agent can start while Books B and C are still being read). Output: `.book-doc/knowledge_base/{book_name}/index.md`. |
| 0.4 | Single agent | Coverage comparison -- load all completed indexes, compare topic coverage across books, identify gaps and overlaps. Output: coverage comparison report. |
| 0.5 | Single agent | Gate check -- verify every index meets the >=1000 line threshold, every chapter has reading evidence, and the coverage comparison is complete. Pass/fail decision for Phase 0. |

```
Sub-Phase Flow:
+---------------------------------------------------------------+
| 0.1 Inventory (single agent)                                   |
|   -> Output: inventory.md                                      |
|                                                                |
| 0.2 Deep Reading (one agent per book, max 3 parallel)          |
|   Batch 1: Book A agent + Book B agent + Book C agent          |
|     Book A agent:                                              |
|       Ch1 -> Ch2 -> ... -> ChN (strict sequence)               |
|       Write interim progress after each chapter                |
|     Book B agent: (same structure)                             |
|     Book C agent: (same structure)                             |
|   Batch 1 complete -> Batch 2: Book D + Book E (if more books) |
|                                                                |
| 0.3 Index Generation (one agent per book, max 3 parallel)      |
|   Can overlap with 0.2 for different books:                   |
|   e.g., Book A index agent starts as soon as Book A read done, |
|   while Books B and C are still being read                     |
|                                                                |
| 0.4 Coverage Comparison (single agent)                         |
|   -> Requires all indexes complete                             |
|                                                                |
| 0.5 Gate Check (single agent)                                  |
|   -> Requires coverage comparison complete                     |
+---------------------------------------------------------------+
```

**Why chapters within a book cannot be parallelized**:
- Chapters have cognitive progression; later chapters reference concepts from earlier ones
- The knowledge index must record cross-chapter topic mappings; parallelism causes information fragmentation
- Style baseline analysis requires consistent end-to-end analysis

**Special handling for web-based source books**:
- Some chapters contain hyperlinks/references pointing to other pages
- Strategy: resolve all references within the current chapter before moving to the next
- If a reference points to an external site (not part of this book), record the URL but do not follow it
- If a reference points to another chapter within the same book, mark it as a cross-reference and continue the current chapter

```markdown
### Agent Task Template (Phase 0, Sub-Phase 0.2)

You are a book reading agent. Task: generate a deep knowledge index for [book name].

**Constraints**:
1. Read chapters in order; do not skip chapters
2. Every chapter must be actually read; do not infer content from titles alone
3. When encountering links/references within a chapter, resolve them within that chapter
4. Record reading evidence immediately after each chapter (paragraph count, code block count, key terms)
5. Output using the format defined in knowledge-index-format.md
6. Total output >= 1000 lines
7. Timeout limit: 10 minutes

**Input**:
- Book path/URL: [...]
- Reference file: knowledge-index-format.md

**Output**:
- Write to: .book-doc/knowledge_base/{book_name}/index.md
```

### Phase 1: Architecture Design

**Orchestration model**: Predominantly single agent, sequential execution, with limited parallelism for chapter plan drafting.

#### Sub-Phase Orchestration

| Sub-Phase | Agent Model | Description |
|-----------|-------------|-------------|
| 1.1 | Single agent | Load indexes -- read all knowledge indexes from Phase 0, including the coverage comparison report. Build an in-memory representation of all source material. |
| 1.2 | Single agent | Cross-book analysis -- perform holistic comparison across all books: identify unique contributions, overlapping coverage, complementary perspectives, and conflicting explanations. Requires a unified view of all indexes; cannot be split across agents. |
| 1.3 | Single agent | TOC design -- design the target table of contents based on the cross-book analysis. Must maintain overall coherence; parallel agents would produce inconsistent structures. |
| 1.4 | Parallel agents, max 3 | Chapter plan drafting -- draft integration plans for different chapters in parallel. Each agent receives the TOC and cross-book analysis, then writes the plan for its assigned chapter(s). Agents must not modify the TOC or analysis; they only produce chapter-level plans. |
| 1.5 | Single agent | Reverse coverage -- verify that every source book topic from the indexes is mapped to at least one chapter/section in the plan. Identify any orphaned topics. |
| 1.6 | Single agent | Gate check -- verify the architecture is complete: TOC is coherent, all chapter plans exist, reverse coverage has no unexplained gaps, and source-architecture.md + plan.md are both valid. Pass/fail decision for Phase 1. |

```
Sub-Phase Flow:
+---------------------------------------------------------------+
| 1.1 Load Indexes (single agent)                                |
|   -> Read all index.md files + coverage comparison             |
|                                                                |
| 1.2 Cross-Book Analysis (single agent)                         |
|   -> Requires holistic view; cannot shard                      |
|   -> Output: cross-book analysis section of source-arch.md     |
|                                                                |
| 1.3 TOC Design (single agent)                                  |
|   -> Requires cross-book analysis complete                     |
|   -> Output: target TOC in source-architecture.md              |
|                                                                |
| 1.4 Chapter Plan Drafting (parallel, max 3 agents)             |
|   -> Each agent drafts plans for assigned chapters             |
|   -> Agents receive TOC + analysis as read-only input          |
|   -> Output: per-chapter integration plans in plan.md          |
|                                                                |
| 1.5 Reverse Coverage (single agent)                            |
|   -> Requires all chapter plans complete                       |
|   -> Output: reverse coverage map, orphaned topic list         |
|                                                                |
| 1.6 Gate Check (single agent)                                  |
|   -> Requires reverse coverage complete                        |
+---------------------------------------------------------------+
```

**Why most of Phase 1 cannot use parallelism**:
- Architecture design requires a global perspective; cross-book analysis cannot be sharded
- TOC design requires overall coherence; parallel agents cannot coordinate their structures
- Chapter integration plans need awareness of preceding and following chapters to design transitions

**If knowledge indexes are too long** (single agent cannot hold them all):
- Allow batched reading: first read the "integration readiness summary" and "overall teaching philosophy" sections from all indexes
- Then read per-topic chapter analyses from each book in batches
- But the final output must be a unified, consistent pair of files (source-architecture.md + plan.md)

```markdown
### Agent Task Template (Phase 1, Sub-Phase 1.4)

You are a chapter plan drafting agent. Task: draft integration plans for chapters [list].

**Input** (self-contained):
- Target TOC: [the designed table of contents]
- Cross-book analysis: [relevant analysis sections]
- Knowledge index excerpts: [sections relevant to your assigned chapters]

**Constraints**:
1. Do not modify the TOC or cross-book analysis
2. Each chapter plan must include: source mapping, methodology selection, content synthesis approach
3. Ensure transitions between your chapters and adjacent chapters (by others) are noted
4. Timeout limit: 10 minutes

**Output**:
- Return: chapter integration plans for assigned chapters
```

### Phase 2: Chapter Generation

**Orchestration model**: One chapter at a time in strict sequence; sections within a chapter may be parallelized under certain conditions.

#### Sub-Phase Orchestration

| Sub-Phase | Agent Model | Description |
|-----------|-------------|-------------|
| 2.1 | Single agent per chapter | Load plan -- read the integration plan for the current chapter, load relevant knowledge index excerpts, and prepare the section-level task specifications. |
| 2.2 | Max 3 section agents parallel | Section generation -- generate sections within the current chapter. Up to 3 section agents run in parallel when sections are independent (no sequential dependency). Sections with progression dependencies must be generated sequentially. |
| 2.3 | Single agent | Quality gate -- merge sections into a complete chapter, run quality checks (integration level, source markers, style consistency, code verification tags). Pass -> proceed; Fail -> rewrite. |
| 2.4 | Single agent | Progress record -- update progress.md with chapter completion status, call workflow.py to record the milestone. This agent runs after the quality gate passes. |
| 2.5 | Single agent | Batch check -- every 5 chapters, run a consistency check across all completed chapters (terminology consistency, style drift, cross-reference integrity). |

```
Sub-Phase Flow (per chapter):
+---------------------------------------------------------------+
| Ch1 (sequential across chapters)                               |
|   2.1 Load Plan (single agent)                                 |
|     -> Read Ch1 integration plan + knowledge index excerpts    |
|                                                                |
|   2.2 Section Generation (max 3 parallel agents)               |
|     +-- Section 1.1 agent (if independent)                     |
|     +-- Section 1.2 agent (if independent)                     |
|     +-- Section 1.3 agent (if independent)                     |
|     OR sequential if sections have dependencies                |
|                                                                |
|   2.3 Quality Gate (single agent)                              |
|     -> Merge sections -> ch01.html                             |
|     -> Run quality checks                                      |
|     -> Pass -> continue / Fail -> rewrite                      |
|                                                                |
|   2.4 Progress Record (single agent)                           |
|     -> Update progress.md, call workflow.py                    |
|                                                                |
| Ch2 (starts only after Ch1 quality gate passes)                |
|   -> ...same sub-phase structure...                            |
|                                                                |
| Every 5 chapters:                                              |
|   2.5 Batch Check (single agent)                               |
|     -> Cross-chapter consistency verification                  |
+---------------------------------------------------------------+
```

**Why chapters cannot be parallelized**:
- Chapters have narrative continuity; later chapters need to reference earlier output
- Quality issues propagate -- if Ch1 has problems, references in Ch2-Ch5 will all be wrong
- Per-chapter quality gates ensure each chapter meets standards, avoiding accumulated rework

**Conditions where sections within a chapter CAN be parallelized**:
- Sections have no sequential dependency (e.g., 1.1 and 1.2 are independent topics)
- Each section agent receives complete integration instructions + style baseline
- On merge, check inter-section transitions and add transitional paragraphs if needed

**Conditions where sections within a chapter CANNOT be parallelized**:
- Sections have clear progression (concepts in 1.1 are prerequisites for 1.2)
- A unified narrative arc must be maintained

```markdown
### Agent Task Template (Phase 2, Sub-Phase 2.2)

You are a section generation agent. Task: generate Chapter [N], Section [M].

**Input** (self-contained, no need to read other files):
- Integration instructions: [the section's integration plan, including source mapping, methodology selection, content synthesis approach]
- Knowledge index excerpt: [source book chapter analysis relevant to this section]
- Style baseline: [1-2 paragraphs of primary book original text]
- Terminology conventions: [glossary terms relevant to this section]
- Preceding content summary: [2-3 sentence summary of the previous section, for continuity]

**Constraints**:
1. Integration level must be L3 or L4 (direct insertion is not allowed)
2. All content must have `<!-- integrated: [source]Ch[N]-[id] -->` markers
3. New code must have V1-V3 verification tags
4. Match the narrative style of the style baseline
5. Output in HTML format
6. Timeout limit: 10 minutes

**Output**:
- Return: section HTML content + marker list
```

### Phase 3: Validation

**Orchestration model**: Parallelizable, but bounded.

#### Sub-Phase Orchestration

| Sub-Phase | Agent Model | Description |
|-----------|-------------|-------------|
| 3.1 | Single agent | Coverage validation -- check that all plan.md IDs have corresponding markers in the output, and verify reverse coverage from source books. |
| 3.2 | Single agent | Technical validation -- run code blocks, verify API references, check version compatibility. |
| 3.3 | Single agent | Consistency validation -- check terminology consistency, style consistency, and cross-reference integrity across all chapters. |
| 3.4 | Single agent | Aggregation -- collect results from all validation agents, produce a unified validation report, and make a pass/fail decision. |

```
Validation Flow:
+---------------------------------------------------------------+
| Parallel validation (max 3 agents):                            |
|                                                                |
| Agent 1 (3.1): Coverage validation                             |
|   - Check all plan.md IDs have markers                         |
|   - Check source book reverse coverage                         |
|                                                                |
| Agent 2 (3.2): Technical validation                            |
|   - Code block execution checks                                |
|   - API verification                                           |
|   - Version compatibility                                      |
|                                                                |
| Agent 3 (3.3): Consistency validation                          |
|   - Terminology consistency                                    |
|   - Style consistency                                          |
|   - Cross-reference integrity                                  |
|                                                                |
| All complete -> 3.4 Aggregation (single agent)                 |
|   -> Unified validation report + pass/fail decision            |
+---------------------------------------------------------------+
```

## Error Recovery Strategy

| Error Type | Detection Method | Recovery Strategy |
|------------|-----------------|-------------------|
| Agent timeout | No response after 10 minutes | Terminate agent, reduce parallelism for that task, then retry |
| Agent quality failure | Gate check fails | Retry once with a different prompt. If still fails, pause and request user decision |
| Agent context overflow | Output truncated or incomplete | Split the task into smaller sub-tasks |
| Dependency conflict | Preceding agent output does not match expectations | Inspect preceding output; roll back to the dependency phase if necessary |
| Web page read failure | 404 / timeout / anti-scraping | Retry once. If still fails, mark as "source unavailable" and record in progress.md |

**Not allowed**:
- Silently skipping a failed agent
- Replacing failed content with placeholders
- Lowering quality standards to accommodate agent limitations

## Progress Tracking

Every agent's launch, completion, and failure must be recorded in progress.md:

```markdown
### Agent Tracking

| Agent ID | Phase | Sub-Phase | Task | Status | Start Time | End Time | Output |
|----------|-------|-----------|------|--------|------------|----------|--------|
| P0-0.1 | Phase 0 | 0.1 | Inventory | done | 10:00 | 10:02 | inventory.md |
| P0-0.2-A | Phase 0 | 0.2 | Book A reading | done | 10:02 | 10:10 | draft entries |
| P0-0.2-B | Phase 0 | 0.2 | Book B reading | done | 10:02 | 10:14 | draft entries |
| P0-0.2-C | Phase 0 | 0.2 | Book C reading | fail->done | 10:02 | 10:17 | draft entries |
| P0-0.3-A | Phase 0 | 0.3 | Book A index gen | done | 10:10 | 10:13 | index.md |
| P0-0.4 | Phase 0 | 0.4 | Coverage comparison | done | 10:18 | 10:20 | coverage report |
| P0-0.5 | Phase 0 | 0.5 | Gate check | done | 10:20 | 10:21 | pass |
```

## Concurrency Tuning Suggestions

| Scenario | Suggested Concurrency | Rationale |
|----------|----------------------|-----------|
| 3 or fewer source books | 3 | One agent per book; Phase 0 completes in one batch |
| 4-6 source books | 3-4 | Phase 0 in two batches; avoid resource contention |
| 7+ source books | 3 | Strict batching, 3 books per batch, ensure single-agent quality |
| Chapter generation (short chapters) | 1 (inter-chapter) + 3 (intra-chapter) | Short chapters allow 3-way section parallelism |
| Chapter generation (long chapters) | 1 (inter-chapter) + 1 (intra-chapter) | Long chapters have more content; single agent ensures coherence |
| Validation | 3 | Validation tasks are independent; full parallelism is safe |
