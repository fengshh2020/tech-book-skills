---
name: integrate-books
description: "Merge multiple technical books into one unified book. Trigger: integrate books, merge books, combine sources, enrich chapters. Do NOT trigger for: single book translation (use translate-book), quality review (use review-tech-book)."
---

# Integrate Books

Merge multiple technical books into one unified book. Output must read like a single book, not a collage.

## Workflow

```
Phase 0: Deep Reading → Phase 1: Architecture → Phase 2: Chapter Generation → Phase 3: Validation → Phase 4: Report
```

**Phase lock**: Run `python scripts/workflow.py integrate-books <run_dir> check_gate <phase> [<sub_phase>] [chapter]` before entering any phase/sub-phase. If gate fails, fix and retry. Do not proceed.

**Sub-agent constraints**: See `references/agent-orchestration.md`. Max concurrent agents: 5. Respect dependency ordering.

## Phase 0: Deep Reading (5 Sub-phases)

**Auto-load**: `references/knowledge-index-format.md`, `references/agent-orchestration.md`

### 0.1 Book Inventory
- List all source books with chapter structure
- Record: book name, chapter count, total pages, file paths
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 0 --sub-phase 0.1 --status completed`

### 0.2 Per-Book Reading
- For each book: read EVERY chapter in order (no skipping, no title-only inference)
- One agent per book, max 3 books parallel
- For web sources: follow links within a chapter before moving to next
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 0 --sub-phase 0.2 --status completed`

### 0.3 Index Generation
- Generate knowledge index per book following `references/knowledge-index-format.md`
- Each index >= 1000 lines, covering:
  - Per-chapter content analysis (topics, sequence, emphasis)
  - Methodology and teaching approach
  - Explanation depth calibration
  - Boundary mapping (scope limits, prerequisites)
  - Unique insights and perspectives
  - Code example inventory (count, quality, patterns)
  - Cross-reference map
  - Style and tone profile
  - Integration readiness assessment
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 0 --sub-phase 0.3 --status completed`

### 0.4 Coverage Comparison
- Compare indexes across books
- Identify: overlaps, gaps, unique contributions, depth differences
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 0 --sub-phase 0.4 --status completed`

### 0.5 Gate 0
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 0
```
- Every source book has index file in `.book-doc/knowledge_base/`
- Each index >= 1000 lines
- Each index contains all required sections
- Reading evidence exists for every chapter

**Reading evidence** (record in progress.md for each chapter):
```markdown
### [BookName] Ch[N] Read Evidence
- Paragraphs: [count]
- Code blocks: [count]
- Core concepts: [list >=3 specific terms]
- Unique to this book: [what this chapter contributes uniquely]
```

**THIS PHASE IS THE FOUNDATION. Do not proceed until every index is verified.**

## Phase 1: Architecture Design (6 Sub-phases)

**Auto-load**: `references/book-architecture.md`, all knowledge indexes from Phase 0

### 1.1 Load Indexes
- Read ALL knowledge indexes completely (do not skim)
- Record read confirmation with structure evidence
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 1 --sub-phase 1.1 --status completed`

### 1.2 Cross-Book Analysis
- Methodology comparison: how each book approaches same topic
- Depth alignment: where books overlap at different depths
- Boundary complementarity: where one book's limits are another's strengths
- Style reconciliation: identify and resolve style conflicts
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 1 --sub-phase 1.2 --status completed`

### 1.3 Target TOC
- Design target table of contents
- Each chapter must have clear purpose and source mapping
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 1 --sub-phase 1.3 --status completed`

### 1.4 Per-Chapter Plans
For EACH chapter, write detailed integration plan:
- Source contribution map (primary/secondary/reference)
- Methodology choice with justification
- Depth target and achievement strategy
- Content synthesis strategy
- Gap filling requirements
- Dependency chain
- Expected output (length, code count, key concepts)
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 1 --sub-phase 1.4 --status completed`

### 1.5 Reverse Coverage
- Build reverse coverage matrix
- Every source chapter must map to: target chapter / sidebar / appendix / explicit exclusion
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 1 --sub-phase 1.5 --status completed`

### 1.6 Gate 1
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 1
```
- `source-architecture.md` exists with all required sections
- `plan.md` exists with per-chapter integration plan for EVERY target chapter
- Each plan contains: source map, methodology choice, depth target, synthesis strategy, gap list, dependency chain
- Reverse coverage matrix accounts for 100% of source chapters
- No "TBD" or placeholder text

## Phase 2: Chapter Generation (5 Sub-phases per Chapter)

**Auto-load**: `references/full-integration.md`, `references/agent-orchestration.md`

### 2.1 Load Plan + Sources
- Load chapter's integration plan from plan.md
- Load relevant knowledge index sections
- Load style baseline from source-architecture.md
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 2 --sub-phase 2.1 --chapter <chapter> --status completed`

### 2.2 Deconstruct & Rewrite
Execute 5-step rewrite:
1. Deconstruct all sources' relevant content
2. Design new section structure (do not reuse any source's original structure)
3. Assign primary/secondary sources per section
4. Rewrite in unified style
5. Add markers: `<!-- integrated: [source]Ch[N]-[id] -->`
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 2 --sub-phase 2.2 --chapter <chapter> --status completed`

### 2.3 Quality Gate (G1-G8)
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 2 <chapter>
```

| Check | Pass Criteria | Fail Action |
|-------|--------------|-------------|
| G1: Coverage | All plan.md IDs have markers | Rewrite chapter |
| G2: Code quality | New code has V1-V3 tags | Add tags + verify |
| G3: Style match | No translationese, matches baseline | Rewrite sections |
| G4: No duplicates | No repeated explanations | Merge/cross-ref |
| G5: Narrative flow | Transitions natural, arc complete | Rewrite |
| G6: Depth match | Matches plan's depth target | Expand or trim |
| G7: Source ratio | Each mapped source has >=3 markers in this chapter | Expand source contribution |
| G8: Output size | >= 80% of max source chapter size | Expand content |

- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 2 --sub-phase 2.3 --chapter <chapter> --status completed`

### 2.4 Progress Record
- Record gate results in progress.md
- Only proceed to next chapter if gate PASSES
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 2 --sub-phase 2.4 --chapter <chapter> --status completed`

### 2.5 Batch Check (Every 5 Chapters)
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 2b
```
- Cross-chapter terminology consistent
- Source unidentifiable test (3 random paragraphs from different chapters)
- Narrative arc connects across chapters
- Command: `python scripts/workflow.py integrate-books <run_dir> record_progress --phase 2 --sub-phase 2.5 --status completed`

**Sub-agent strategy**:
- One chapter at a time (sequential)
- Within a chapter: max 3 section agents parallel
- Failed gate = rewrite chapter (do not accumulate fixes)

**Output**: `output/{chapter}.html` files, one per chapter

**Fail = rewrite chapter. Do not proceed. Do not accumulate issues for Phase 3.**

## Phase 3: Validation

**Do**:
1. Run coverage validation across all chapters
2. Term consistency check (full book grep)
3. Code runnability check (all code blocks)
4. Style consistency (read 3 consecutive chapters from different parts)
5. Cross-reference integrity (all chapter links valid)
6. Reverse coverage: verify 100% source material accounted for

**Coverage Guardian checks**:
```bash
python scripts/workflow.py integrate-books <run_dir> coverage_report
python scripts/workflow.py integrate-books <run_dir> coverage_guard
```

**Auto-check scripts**:
```bash
python scripts/validate_tech.py output/
python scripts/validate_terms.py output/
python scripts/workflow.py integrate-books <run_dir> check_gate 3
```

**Gate**:
- Coverage >= 95%
- All terms consistent
- All code runnable
- All cross-references valid
- No style jumps between chapters
- Coverage Guardian: no chapter below floor (10% of total markers)
- Coverage Guardian: no chapter below per-chapter minimum (3 markers)

## Phase 4: Report

**Auto-load**: `shared/report-templates.md`

**Do**: Write `report.md` with summary, per-chapter scores, issues, coverage matrix, known limits, Coverage Guardian results.

**Gate**:
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 4
```
- report.md exists
- Contains: summary, scores, issues, fix batches, coverage matrix
- Coverage Guardian results included

## Coverage Guardian

**Purpose**: Detect and prevent coverage gaps, slacking, and superficial integration.

**Rules**:

1. **Floor Rule**: No source book may have fewer than 10% of total markers across the integrated book. If a source is below floor, flag for review and expansion.

2. **Per-Chapter Minimum**: If a source book is mapped as "primary" or "secondary" for a chapter, it must contribute >=3 integration markers in that chapter. Zero markers from a mapped source = automatic fail.

3. **Patch-Style Detection**: If a source book's markers all appear in <=2 chapters, or its markers never appear as the first/primary marker in any section, flag as patch-style integration.

4. **Output Size Guard**: Chapter output size must be >= 80% of the largest source chapter it integrates. Smaller = likely content loss.

**Commands**:
```bash
python scripts/workflow.py integrate-books <run_dir> coverage_report
python scripts/workflow.py integrate-books <run_dir> coverage_guard
```

**Coverage Guardian runs**:
- After Phase 2 completion (full scan)
- In Phase 3 validation
- In Phase 4 report

## Anti-Slacking Rules

Per `shared/anti-slacking.md`:
- Every phase start: re-read reference files, record read confirmation in progress.md
- Every claimed read: attach structure evidence (paragraph count, code block count, specific terms)
- No "I remember" — always re-read
- No title-only inference — open and read actual content
- No "approximately" — gate either passes or fails, no partial credit
- No skipping sub-phases — each sub-phase must complete and record before next

## Sub-Agent Orchestration

See `references/agent-orchestration.md` for full rules. Key constraints:

1. **Max concurrency**: 5 agents simultaneously
2. **Phase 0**: One agent per book, max 3 books parallel. Within a book: sequential chapter reading.
3. **Phase 1**: Single agent (architecture requires holistic view, not parallel).
4. **Phase 2**: One chapter at a time. Within a chapter: max 3 section agents parallel.
5. **Phase 3**: Validation agents can run parallel (max 3).
6. **Dependency ordering**: For web sources, resolve all links/references within a page before moving to next page.
7. **Error recovery**: Failed agent = retry once with different approach. Second failure = pause and ask user.

## Quality Standards

- Reader cannot identify content sources
- Chapter skeleton survives reverse coverage check
- Every addition has source, location, benefit
- Duplicates merged or cross-referenced
- Output ready for review-tech-book via `report.md`
- Integration level: L3 (reorganize) or L4 (full fusion) only — see `references/full-integration.md`
