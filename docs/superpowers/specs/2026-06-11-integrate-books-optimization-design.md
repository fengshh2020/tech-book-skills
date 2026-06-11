# Integrate-Books Skill Optimization Design

Date: 2026-06-11

## Problem Statement

The integrate-books skill has critical failures observed in real C++ 6-book integration:

1. **Coarse granularity**: 5 phases with no sub-steps; problems balloon undetected until late phases
2. **Progress tracking failure**: progress.md showed Phase 1-4 as "pending" while 25 chapters were already generated
3. **Coverage insufficiency**: Integrated output sometimes has less content than a single source book
4. **Patch-style integration**: Some source books become supplements rather than being truly merged
   - Evidence: Will=427 markers (60%), Mindset=37 markers (5%), StepByStep=45 markers (6%)
   - Mindset and StepByStep are effectively patches, not integrated sources
5. **Language inconsistency**: All skill files should be in English

## Design Decisions

### Decision 1: Sub-Phase Decomposition

Split the existing 5 phases into 16+ sub-phases with per-sub-phase gates.

Rationale: The current Phase 0-4 structure is too coarse. Phase 0 (Deep Reading) covers inventory, reading, indexing, and comparison in one step. Phase 2 (Chapter Generation) combines loading, writing, gating, and recording. Problems in early sub-steps propagate undetected to later phases.

### Decision 2: Coverage Guardian System

Add per-source coverage ratios, patch-style detection, and output size guards enforced by workflow.py.

Rationale: Current coverage checks only verify ">=95%" at Phase 3, which is too late and too coarse. The Will-dominant / Mindset-starved marker distribution proves that aggregate coverage masks per-source imbalance.

### Decision 3: workflow.py Auto-Progress

Make workflow.py the single source of truth for progress tracking. Models must call `record_progress` after each sub-phase, and workflow.py blocks subsequent gates if progress is not recorded.

Rationale: Manual progress.md updates by the model are unreliable (proven by the "Phase 1-4 pending" failure while 25 chapters existed).

### Decision 4: Full English Conversion

All skill files, references, and scripts converted to English.

Rationale: User requirement. Also improves cross-agent compatibility and reduces ambiguity from mixed-language templates.

## Sub-Phase Architecture

### Phase 0: Deep Reading (5 sub-phases)

#### 0.1: Book Inventory & Metadata

**Input**: Source book paths/URLs
**Output**: `.book-doc/knowledge_base/INVENTORY.md`

Contents:
- Per-book: name, author, target audience, chapter count, estimated code examples, language/framework version
- Total: book count, total chapter count, estimated scope

**Gate 0.1**:
- INVENTORY.md exists
- Every source book listed with complete metadata
- Chapter count per book matches actual content

#### 0.2: Per-Book Chapter-by-Chapter Reading

**Input**: INVENTORY.md, source books
**Output**: Per-chapter reading notes (inline in index generation)

Process: One agent per book, sequential chapters within each book, max 3 books in parallel.

For each chapter:
1. Read the actual chapter content (no title-only inference)
2. Record reading evidence: paragraph count, code block count, >=3 specific technical terms
3. Proceed to next chapter only after evidence is recorded

**Gate 0.2** (per book):
- Reading evidence exists for every chapter
- No two consecutive chapters have identical evidence format
- Every evidence entry has >=3 specific technical terms (not title rewrites)

#### 0.3: Index Generation

**Input**: Reading notes from 0.2
**Output**: `.book-doc/knowledge_base/{book_name}/index.md` (>=1000 lines per book)

Format: See `references/knowledge-index-format.md` (all field names in English)

**Gate 0.3** (per book):
- index.md exists and >=1000 lines
- Contains all required sections: Teaching Philosophy, Cognitive Progression, Narrative Style Baseline, Per-Chapter Deep Analysis, Cross-Chapter Theme Mapping, Knowledge Point Cross-Reference Matrix, Integration Readiness Summary
- Each chapter analysis has: Content Coverage, Methodology Analysis, Depth Calibration, Unique Insights, Code Example Inventory, Cross-References, Integration Readiness

#### 0.4: Coverage Comparison

**Input**: All index.md files
**Output**: `.book-doc/knowledge_base/INDEX/source_coverage.md`

Contents:
- Per-topic: which books cover it, at what depth, with what methodology
- Per-book: unique topics, shared topics, gap topics
- Cross-book: overlap matrix, complementarity map

**Gate 0.4**:
- source_coverage.md exists
- Covers all topics found in any source book
- Every source book's unique topics are identified

#### 0.5: Gate 0 (Final Phase 0 Gate)

Combines all sub-phase gates. Must pass before entering Phase 1.

**Gate 0**:
- All sub-phase gates 0.1-0.4 passed
- INVENTORY.md + all index.md files + source_coverage.md exist
- Per-book marker: every source chapter has reading evidence
- Coverage comparison identifies all unique and shared topics

### Phase 1: Architecture Design (6 sub-phases)

#### 1.1: Load All Indexes

**Input**: All index.md files from Phase 0
**Output**: Read confirmation in progress.md

Process:
1. Read every index.md completely (no skimming)
2. Record read confirmation with evidence: which sections read, key findings per book
3. List core methodology differences across books (>=3 points)

**Gate 1.1**:
- Read confirmation exists for every source book
- At least 3 methodology differences identified across books
- Evidence is specific (not "Book A is different from Book B")

#### 1.2: Cross-Book Analysis

**Input**: Indexes + source_coverage.md
**Output**: `.book-doc/runs/{run_id}/cross-book-analysis.md`

Required sections:
- Methodology Difference Analysis (per topic)
- Depth Alignment Analysis (per topic)
- Boundary Complementarity Analysis (per topic)
- Style Conflict Resolution (per dimension)

Each analysis must cite specific index evidence (e.g., "Will Ch8 uses problem-driven introduction, Stroustrup Ch7 uses definition-first approach").

**Gate 1.2**:
- cross-book-analysis.md exists with all 4 required sections
- Every analysis cites specific index evidence
- No "TBD" or "to be determined"

#### 1.3: Target TOC Design

**Input**: cross-book-analysis.md
**Output**: Target TOC in `source-architecture.md`

Rules:
- Each chapter has exactly ONE primary cognitive load
- Each chapter has explicit prerequisites and capability output
- Source coverage: which books contribute to which chapter
- Methodology choice: which book's teaching approach to follow, with evidence

**Gate 1.3**:
- Every chapter has: title, capability goal, prerequisites, primary cognitive load
- No chapter has more than one primary cognitive load
- Methodology choices cite cross-book-analysis.md evidence

#### 1.4: Per-Chapter Integration Plans

**Input**: Target TOC + knowledge indexes
**Output**: `plan.md` with self-contained per-chapter plans

Each plan must include:
- Source mapping (which source, which chapter, what role, what contribution)
- Methodology choice with evidence
- Depth alignment strategy (target depth, per-source adjustment)
- Content synthesis plan (per-section: primary source, supplements, new content, integration level)
- Concept bridging (previous chapter transition, internal bridges, next chapter setup)
- Terminology conventions (English term, unified translation, first appearance)
- Style baseline example (1-2 paragraphs from primary source)
- Expected output: estimated length, code example count, marker count

**Gate 1.4**:
- plan.md has an integration plan for EVERY target chapter
- Each plan is self-contained (Phase 2 agents need not read other files)
- No "TBD" or "待定"
- Every methodology choice has evidence citation

#### 1.5: Reverse Coverage Matrix

**Input**: plan.md + all index.md files
**Output**: Reverse coverage matrix in `source-architecture.md`

Format:
```
| Source Book | Source Chapter | Target Disposition | Target Location | Rationale |
|-------------|---------------|-------------------|-----------------|-----------|
| Will | Ch1 | Main content | Target Ch1 | Primary source for build topics |
| Mindset | Ch5 | Supplement | Target Ch8 Sidebar | Complementary ownership perspective |
| LowLatency | Ch20 | Excluded | - | Too specialized for target audience |
```

**CRITICAL**: Every source chapter must map to one of: main content, sidebar, appendix, or explicit exclusion with rationale. **Coverage target: 100%** (not 95%).

**Gate 1.5**:
- Reverse coverage matrix accounts for 100% of source chapters
- Every excluded chapter has documented rationale
- Every sidebar/appendix entry has specified content

#### 1.6: Gate 1 (Final Phase 1 Gate)

**Gate 1**:
- All sub-phase gates 1.1-1.5 passed
- source-architecture.md exists with: target audience, per-book portraits, cross-book analysis, knowledge graph, TOC, reverse coverage matrix, exclusions, self-check
- plan.md exists with self-contained plans for all chapters
- No TBD/placeholders anywhere
- Reverse coverage = 100%

### Phase 2: Chapter Generation (5 sub-phases per chapter)

#### 2.1: Load Plan + Sources

**Input**: Current chapter's integration plan from plan.md
**Output**: Loaded context (in agent's working memory)

Process:
1. Load the chapter's integration plan (self-contained)
2. Load relevant knowledge index sections (as specified in source mapping)
3. Load style baseline from plan.md
4. Record load confirmation in progress.md

**Gate 2.1**:
- Load confirmation recorded with: plan loaded, sources loaded, style baseline loaded

#### 2.2: Deconstruct & Rewrite

**Input**: Loaded plan + sources + style baseline
**Output**: Chapter HTML with integration markers

Process (5-step rewrite):
1. Deconstruct all sources' relevant content
2. Design new section structure (no source's original structure reused)
3. Assign primary/secondary sources per section
4. Rewrite in unified style
5. Add markers: `<!-- integrated: [Source]Ch[N]-[id] -->`

Integration level must be L3 (reorganize) or L4 (full fusion). L1 (direct insert) and L2 (style adapt only) are prohibited.

**Gate 2.2**:
- Chapter HTML exists with integration markers
- No section uses L1 or L2 integration

#### 2.3: Quality Gate

**Input**: Chapter HTML
**Output**: Gate results

| ID | Check | Pass Criteria | Fail Action |
|----|-------|--------------|-------------|
| G1 | Coverage | All plan.md IDs have markers | Rewrite chapter |
| G2 | Code quality | New code has V1-V3 tags | Add tags + verify |
| G3 | Style match | No translationese, matches baseline | Rewrite sections |
| G4 | No duplicates | No repeated explanations | Merge/cross-ref |
| G5 | Narrative flow | Transitions natural, arc complete | Rewrite |
| G6 | Depth match | Matches plan's depth target, sufficient length | Expand or trim |
| G7 | Source ratio | Each mapped source has >=3 markers in this chapter | Expand source contribution |
| G8 | Output size | Chapter size >= max(source_chapter_sizes) * 0.8 | Expand content |

**Gate 2.3**:
- G1-G6 pass (existing rules)
- G7: per-source minimum 3 markers if source is mapped as primary or secondary
- G8: output size guard

#### 2.4: Progress Record

**Input**: Gate results
**Output**: Updated progress.md (via workflow.py)

**MANDATORY**: Must call `workflow.py integrate-books <run_dir> record_progress` after every chapter.

**Gate 2.4**:
- workflow.py record_progress called successfully
- progress.md reflects current chapter completion
- Per-source marker counts recorded

#### 2.5: Batch Consistency Check (every 5 chapters)

**Input**: Last 5 completed chapters
**Output**: Consistency report

Checks:
- Cross-chapter terminology consistent
- Source unidentifiable test (3 random paragraphs from different chapters)
- Narrative arc connects across chapters
- Per-source coverage ratio across batch >=10% for each source

**Gate 2.5**:
- All batch checks pass
- No source has <10% of batch markers

### Phase 3: Validation (enhanced)

Same structure as before, but with stricter gates:

- Coverage >= 95% (aggregate)
- Per-source coverage >= 10% of total markers
- No patch-style sources detected
- All terms consistent
- All code runnable
- All cross-references valid
- No style jumps

### Phase 4: Report (unchanged structure)

Same as before.

## Coverage Guardian System

### Per-Source Coverage Ratio

```
Per-chapter rule:
  If a source book is mapped as "primary" or "secondary" for a chapter,
  it MUST contribute >=3 integration markers in that chapter.

Per-book rule:
  Each source book's total markers >= (total_source_chapters * 0.5)
  Example: Will has 30 chapters -> minimum 15 markers
  Example: Mindset has 15 chapters -> minimum 8 markers

Floor rule:
  No source book may have fewer than 10% of total markers.
  If total markers = 700, minimum per source = 70.
```

### Patch-Style Detection

A source is "patch-style" if ANY of these is true:

1. All its markers appear in <=2 chapters (concentrated, not integrated)
2. Its markers never appear as the first marker in any section (always supplemental)
3. Its content always appears after the primary source content within every section

Detection timing:
- After each chapter gate (sub-phase 2.3)
- After batch check (sub-phase 2.5)
- During Phase 3 validation

Escalation:
- First detection: WARNING logged to progress.md
- Second detection for same source: REQUIRE REWRITE of affected chapters

### Output Size Guard

```
Per-chapter rule:
  Output chapter size MUST be >= max(source_chapter_sizes_for_this_topic) * 0.8
  
  Example: If Will Ch8 = 50KB and Stroustrup Ch7 = 40KB cover the same topic,
  the integrated chapter must be >= 40KB (50KB * 0.8).
```

This prevents the "integrated book has less content than a single source" problem.

## workflow.py Enhancement

### New Commands

```bash
# Sub-phase level gate checking
workflow.py integrate-books <run_dir> check_gate <phase> <sub_phase> [chapter]

# Progress recording (mandatory after each sub-phase)
workflow.py integrate-books <run_dir> record_progress \
  --phase <N> \
  --sub-phase <N> \
  [--chapter <name>] \
  --status <completed|failed> \
  [--markers <count>] \
  [--gate-result <results>]

# Coverage report (per-source marker counts, ratios, patch warnings)
workflow.py integrate-books <run_dir> coverage_report

# Coverage guard for a specific chapter
workflow.py integrate-books <run_dir> coverage_guard <chapter>

# Status with sub-phase detail
workflow.py integrate-books <run_dir> status
```

### Sub-Phase State Tracking

```json
{
  "skill": "integrate-books",
  "current_phase": "2",
  "current_sub_phase": "3",
  "completed_phases": ["0", "1"],
  "completed_sub_phases": {
    "0": ["0.1", "0.2", "0.3", "0.4", "0.5"],
    "1": ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"],
    "2": ["2.1:ch01", "2.2:ch01", "2.3:ch01", "2.4:ch01",
          "2.1:ch02", "2.2:ch02", "2.3:ch02", "2.4:ch02"]
  },
  "chapter_progress": {
    "ch01": {"status": "completed", "markers": 27, "gate": "PASS"},
    "ch02": {"status": "completed", "markers": 29, "gate": "PASS"},
    "ch03": {"status": "in_progress", "markers": 0, "gate": null}
  },
  "source_coverage": {
    "Will": 57,
    "Stroustrup": 24,
    "Cookbook": 22,
    "LowLatency": 9,
    "Mindset": 5,
    "StepByStep": 7
  }
}
```

### Progress Blocking

Before allowing gate check for sub-phase N+1:
1. Verify sub-phase N is recorded as completed in .workflow_state.json
2. If not, ERROR: "Cannot enter sub-phase N+1. Sub-phase N not completed."
3. For Phase 2: verify previous chapter's sub-phase 2.4 (Progress Record) is completed before allowing next chapter's sub-phase 2.1

## English Conversion

### Files to Convert

| File | Conversion Scope |
|------|-----------------|
| SKILL.md | Full English |
| references/agent-orchestration.md | Full English |
| references/book-architecture.md | Full English |
| references/context-passing.md | Full English |
| references/full-integration.md | Full English |
| references/integration-discipline.md | Full English |
| references/knowledge-index-format.md | Full English (field names + instructions, example content can show Chinese where output would be Chinese) |
| references/quality-gate.md | Full English |
| references/synthesis-methodology.md | Full English |
| scripts/workflow.py | English messages, English gate descriptions |

### Naming Conventions (Chinese to English)

| Chinese | English |
|---------|---------|
| 整体教学哲学 | Teaching Philosophy |
| 认知递进策略 | Cognitive Progression Strategy |
| 叙事风格基线 | Narrative Style Baseline |
| 逐章深度分析 | Per-Chapter Deep Analysis |
| 整合准备摘要 | Integration Readiness Summary |
| 深度标定 | Depth Calibration |
| 独特洞察 | Unique Insights |
| 代码示例清单 | Code Example Inventory |
| 交叉引用 | Cross-References |
| 整合就绪度 | Integration Readiness |
| 方法论差异分析 | Methodology Difference Analysis |
| 深度对齐分析 | Depth Alignment Analysis |
| 边界互补分析 | Boundary Complementarity Analysis |
| 风格冲突与调和 | Style Conflict Resolution |
| 来源映射 | Source Mapping |
| 概念桥接 | Concept Bridging |
| 术语约定 | Terminology Conventions |
| 防懈怠 | Anti-Slacking |
| 阅读证据 | Reading Evidence |
| 跨书对比 | Cross-Book Analysis |
| 反向覆盖矩阵 | Reverse Coverage Matrix |
| 认知负担 | Cognitive Load |
| 内容覆盖 | Content Coverage |
| 方法论分析 | Methodology Analysis |
| 风格特征 | Style Characteristics |

## Files to Modify

1. `integrate-books/SKILL.md` — Rewrite with sub-phase architecture, English
2. `integrate-books/references/knowledge-index-format.md` — English field names + instructions
3. `integrate-books/references/book-architecture.md` — English, add sub-phase references
4. `integrate-books/references/full-integration.md` — English
5. `integrate-books/references/integration-discipline.md` — English, add coverage guardian rules
6. `integrate-books/references/quality-gate.md` — English, add G7/G8 checks
7. `integrate-books/references/agent-orchestration.md` — English, add sub-phase orchestration
8. `integrate-books/references/synthesis-methodology.md` — English
9. `integrate-books/references/context-passing.md` — English, add sub-phase context
10. `integrate-books/scripts/workflow.py` — Enhanced with sub-phase tracking, coverage guardian, auto-progress

## Files NOT Modified

- `shared/` directory (out of scope per user decision)
- Other skill directories (translate-book, review-tech-book, codebase-book)
- `integrate-books/agents/openai.yaml`
- `integrate-books/assets/` (style.css, script.js)
