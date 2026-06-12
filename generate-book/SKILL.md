---
name: generate-book
description: "Generate a unified technical book from one or more sources. Single source: translate and produce Chinese HTML book. Multiple sources: deep-read, integrate, and produce one coherent book. Trigger: generate book, 整合书籍, 生成书籍, merge books, combine sources, translate book, 翻译书籍. Do NOT trigger for: quality review only (use review-tech-book), codebase analysis (use codebase-book)."
---

# Generate Book

## ⛊ IRON LAW

**NO OUTPUT WITHOUT FRESH READ EVIDENCE. NO GATE SKIP. NO TITLE-ONLY INFERENCE. NO CONTENT SHRINKAGE.**

Violating the letter of this rule IS violating the spirit of this rule.

### Anti-Rationalization Table

| If you think... | The truth is... |
|-----------------|-----------------|
| "I remember this rule" | You don't. Re-read the file. |
| "The title tells me enough" | It doesn't. Open and read. |
| "Gate probably passes" | Run it. No probably. |
| "This is ~80% coverage" | Shrinkage = data loss. Expand. |
| "I'll fix it in Phase 3" | Fix now or rewrite later. |
| "Just this once" | "Just this once" is how it starts. |
| "The user wants speed" | The user wants quality. |
| "I already verified" | Re-verify. Fresh evidence only. |

Generate a unified technical book from one or more sources. Single source -> translate + assemble. Multiple sources -> integrate + assemble. Output must read like a single book, not a collage.

## Mode Selection

Auto-detect: 1 source -> single mode, 2+ sources -> multi mode.

| Mode | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|---------|
| Single | Extract & Read | Translate | Assemble | Validate | Report |
| Multi | Deep Reading (5 sub-phases) | Architecture (6 sub-phases) | Generate (6 sub-phases/ch) | Validate | Report |

**Phase lock**: Run `python scripts/workflow.py generate-book <run_dir> check_gate <phase> [<sub_phase>] [chapter]` before entering any phase/sub-phase. If gate fails, fix and retry. Do not proceed.

**Sub-agent constraints**: See `references/agent-orchestration.md`. Max concurrent agents: 5. Respect dependency ordering.

---

## Single-Source Mode

Use when exactly one source book is provided. The workflow is: extract, translate, assemble, validate, report.

### Phase 0: Extract & Read (3 Sub-phases)

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/agent-orchestration.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] If unchecked: STOP. Do not proceed.

#### 0.1 Source Inventory
- Parse source file (EPUB or HTML)
- For EPUB: unzip, parse container.xml, content.opf, spine, toc.ncx
- For HTML: parse structure, headings, navigation
- Record: book name, chapter count, total pages, file paths, source fingerprint
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.1 --status completed`

#### 0.2 Chapter-by-Chapter Reading
- Read EVERY chapter in order (no skipping, no title-only inference)
- For each chapter, record reading evidence:
  ```markdown
  ### Ch[N] Read Evidence
  - Paragraphs: [count]
  - Code blocks: [count]
  - Core concepts: [list >=3 specific terms]
  - Images/figures: [count]
  ```
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.2 --status completed`

#### 0.3 Gate 0

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 0
```
- Every chapter has reading evidence recorded
- Source inventory complete with all metadata
- No chapter skipped or inferred from title only

### Phase 1: Translate (5 Sub-phases)

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/translation-rules.md` completely (no skimming)
- [ ] Read `shared/translationese-patterns.md` completely (no skimming)
- [ ] Read any existing `.book-doc/spec.md` for terminology
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] If ANY unchecked: STOP. Do not proceed.

#### 1.1 Load Translation Rules
- Read `references/translation-rules.md` completely
- Read `shared/translationese-patterns.md` completely
- Read any existing `.book-doc/spec.md` for terminology
- Record read confirmation with structure evidence
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.1 --status completed`

#### 1.2 Per-Chapter Translation
- Translate paragraph by paragraph with 1:1 mapping
- Source paragraph count MUST equal target paragraph count
- Code comments translated to Chinese; code logic unchanged
- First occurrence of technical terms annotated
- Read rules files before EVERY chapter (no "I remember")
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.2 --chapter <chapter> --status completed`

#### 1.3 Terminology Consistency Check
- After all chapters translated, run full-book terminology grep
- Verify every term is translated consistently across all chapters
- Flag and fix any inconsistencies
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.3 --status completed`

#### 1.4 Translationese Scan
- Scan all translated chapters against `shared/translationese-patterns.md`
- Target: 0 hits for any listed pattern
- Fix any detected translationese
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.4 --status completed`

#### 1.5 Gate 1

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 1
```
- All chapters have `<!-- translated: complete -->` marker
- Paragraph count matches for every chapter (source = target)
- All terms checked and consistent
- Translationese scan: 0 hits
- progress.md updated with evidence for every chapter

### Phase 2: Assemble (4 Sub-phases)

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/book-assembly.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] Gate 1 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.

#### 2.1 HTML Scaffold
- Create output directory structure following `references/book-assembly.md`
- File numbering:
  | Number | File |
  |--------|------|
  | 00 | `00_cover.html` |
  | 01 | `01_toc.html` |
  | 02 | `02_front.html` |
  | 03 | `03_intro.html` |
  | 04+ | `{NN}_chapter{M}.html` |
  | N+ | `{NN}_appendix_{x}.html` |
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.1 --status completed`

#### 2.2 CSS/JS Integration
- Copy `assets/style.css` and `assets/script.js` to output directory
- Verify CSS/JS load correctly in HTML files
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.2 --status completed`

#### 2.3 Navigation & Cross-References
- Build table of contents with links to all chapters
- Add previous/next navigation between chapters
- Verify all internal links resolve correctly
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.3 --status completed`

#### 2.4 Gate 2

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 2
```
- All HTML files exist in output directory
- CSS/JS files present and linked
- Table of contents complete with working links
- All cross-references valid
- All images present in output

### Phase 3: Validate

**Do**:
1. Run coverage validation: output size >= 80% of source
2. Term consistency check (full book grep)
3. Code runnability check (all code blocks)
4. Translationese re-scan (0 hits)
5. Cross-reference integrity (all chapter links valid)
6. Paragraph count verification (source = target for every chapter)

**Auto-check scripts**:

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/validate_tech.py output/
python scripts/validate_terms.py output/
python scripts/workflow.py generate-book <run_dir> check_gate 3
```

**Gate**:
- All terms consistent
- All code runnable
- All cross-references valid
- Translationese: 0 hits
- Output size >= 80% of source
- All paragraphs accounted for

### Phase 4: Report

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `shared/report-templates.md` completely (no skimming)
- [ ] Gate 3 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.

**Do**: Write `report.md` with summary, per-chapter scores, issues, terminology table, known limits.

**Gate**:

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 4
```
- report.md exists
- Contains: summary, scores, issues, terminology table, known limits

---

## Multi-Source Mode

Use when two or more source books are provided. The workflow is: deep reading, architecture design, chapter generation, validation, report.

### Phase 0: Deep Reading (5 Sub-phases)

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/knowledge-index-format.md` completely (no skimming)
- [ ] Read `references/agent-orchestration.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] If ANY unchecked: STOP. Do not proceed.

#### 0.1 Book Inventory
- List all source books with chapter structure
- Record: book name, chapter count, total pages, file paths
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.1 --status completed`

#### 0.2 Per-Book Reading
- For each book: read EVERY chapter in order (no skipping, no title-only inference)
- One agent per book, max 3 books parallel
- For web sources: follow links within a chapter before moving to next
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.2 --status completed`

#### 0.3 Index Generation
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
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.3 --status completed`

#### 0.4 Coverage Comparison
- Compare indexes across books
- Identify: overlaps, gaps, unique contributions, depth differences
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.4 --status completed`

#### 0.5 Gate 0

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 0
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

### Phase 1: Architecture Design (6 Sub-phases)

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/book-architecture.md` completely (no skimming)
- [ ] Re-read ALL knowledge indexes from Phase 0 (no "I remember")
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] Gate 0 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.

#### 1.1 Load Indexes
- Read ALL knowledge indexes completely (do not skim)
- Record read confirmation with structure evidence
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.1 --status completed`

#### 1.2 Cross-Book Analysis
- Methodology comparison: how each book approaches same topic
- Depth alignment: where books overlap at different depths
- Boundary complementarity: where one book's limits are another's strengths
- Style reconciliation: identify and resolve style conflicts
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.2 --status completed`

#### 1.3 Target TOC
- Design target table of contents
- Each chapter must have clear purpose and source mapping
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.3 --status completed`

#### 1.4 Per-Chapter Plans
For EACH chapter, write detailed integration plan:
- Source contribution map (primary/secondary/reference)
- Methodology choice with justification
- Depth target and achievement strategy
- Content synthesis strategy
- Gap filling requirements
- Dependency chain
- Expected output (length, code count, key concepts)
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.4 --status completed`

#### 1.5 Reverse Coverage
- Build reverse coverage matrix
- Every source chapter must map to: target chapter / sidebar / appendix / explicit exclusion
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.5 --status completed`

#### 1.6 Gate 1

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 1
```
- `source-architecture.md` exists with all required sections
- `plan.md` exists with per-chapter integration plan for EVERY target chapter
- Each plan contains: source map, methodology choice, depth target, synthesis strategy, gap list, dependency chain
- Reverse coverage matrix accounts for 100% of source chapters
- No "TBD" or placeholder text

### Phase 2: Chapter Generation (6 Sub-phases per Chapter)

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/full-integration.md` completely (no skimming)
- [ ] Read `references/agent-orchestration.md` completely (no skimming)
- [ ] Re-read chapter's integration plan from plan.md
- [ ] Gate 1 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.

#### 2.1 Load Plan + Sources
- Load chapter's integration plan from plan.md
- Load relevant knowledge index sections
- Load style baseline from source-architecture.md
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.1 --chapter <chapter> --status completed`

#### 2.2 Deconstruct & Rewrite
Execute 5-step rewrite:
1. Deconstruct all sources' relevant content
2. Design new section structure (do not reuse any source's original structure)
3. Assign primary/secondary sources per section
4. Rewrite in unified style
5. Add markers: `<!-- integrated: [source]Ch[N]-[id] -->`
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.2 --chapter <chapter> --status completed`

#### 2.3 Quality Gate (G1-G8)

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 2 <chapter>
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

- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.3 --chapter <chapter> --status completed`

#### 2.4 Progress Record
- Record gate results in progress.md
- Only proceed to next chapter if gate PASSES
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.4 --chapter <chapter> --status completed`

#### 2.5 Batch Check (Every 5 Chapters)

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 2b
```
- Cross-chapter terminology consistent
- Source unidentifiable test (3 random paragraphs from different chapters)
- Narrative arc connects across chapters
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.5 --status completed`

**Sub-agent strategy**:
- One chapter at a time (sequential)
- Within a chapter: max 3 section agents parallel
- Failed gate = rewrite chapter (do not accumulate fixes)

**Fail = rewrite chapter. Do not proceed. Do not accumulate issues for Phase 3.**

#### 2.6 Assemble
After all chapters generated, assemble the final book:
- Create HTML scaffold (`references/book-assembly.md`)
- Integrate CSS/JS
- Build navigation and cross-references
- Command: `python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.6 --status completed`

**Output**: `output/{chapter}.html` files, one per chapter, plus assembled book with navigation

### Phase 3: Validation

**Do**:
1. Run coverage validation across all chapters
2. Term consistency check (full book grep)
3. Code runnability check (all code blocks)
4. Style consistency (read 3 consecutive chapters from different parts)
5. Cross-reference integrity (all chapter links valid)
6. Reverse coverage: verify 100% source material accounted for

**Coverage Guardian checks**:
```bash
python scripts/workflow.py generate-book <run_dir> coverage_report
python scripts/workflow.py generate-book <run_dir> coverage_guard
```

**Auto-check scripts**:

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/validate_tech.py output/
python scripts/validate_terms.py output/
python scripts/workflow.py generate-book <run_dir> check_gate 3
```

**Gate**:
- Coverage >= 95%
- All terms consistent
- All code runnable
- All cross-references valid
- No style jumps between chapters
- Coverage Guardian: no chapter below floor (10% of total markers)
- Coverage Guardian: no chapter below per-chapter minimum (3 markers)

### Phase 4: Report

**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `shared/report-templates.md` completely (no skimming)
- [ ] Gate 3 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.

**Do**: Write `report.md` with summary, per-chapter scores, issues, coverage matrix, known limits, Coverage Guardian results.

**Gate**:

**STOP -- Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 4
```
- report.md exists
- Contains: summary, scores, issues, fix batches, coverage matrix
- Coverage Guardian results included

---

## Coverage Guardian

**Purpose**: Detect and prevent coverage gaps, slacking, and superficial integration.

**Rules**:

1. **Floor Rule**: No source book may have fewer than 10% of total markers across the integrated book. If a source is below floor, flag for review and expansion.

2. **Per-Chapter Minimum**: If a source book is mapped as "primary" or "secondary" for a chapter, it must contribute >=3 integration markers in that chapter. Zero markers from a mapped source = automatic fail.

3. **Patch-Style Detection**: If a source book's markers all appear in <=2 chapters, or its markers never appear as the first/primary marker in any section, flag as patch-style integration.

4. **Output Size Guard**: Chapter output size must be >= 80% of the largest source chapter it integrates. Smaller = likely content loss.

**In single-source mode**, Coverage Guardian checks are trivially satisfied (one source = 100% weight). Skip per-source ratio and patch-style detection. Only check: output size >= 80% of source, all content translated.

**Commands**:
```bash
python scripts/workflow.py generate-book <run_dir> coverage_report
python scripts/workflow.py generate-book <run_dir> coverage_guard
```

**Coverage Guardian runs**:
- After Phase 2 completion (full scan)
- In Phase 3 validation
- In Phase 4 report

## Anti-Slacking Rules

Per `shared/anti-slacking.md`:
- Every phase start: re-read reference files, record read confirmation in progress.md
- Every claimed read: attach structure evidence (paragraph count, code block count, specific terms)
- No "I remember" -- always re-read
- No title-only inference -- open and read actual content
- No "approximately" -- gate either passes or fails, no partial credit
- No skipping sub-phases -- each sub-phase must complete and record before next
- In single-source mode, verify 1:1 paragraph mapping instead of integration markers

## Sub-Agent Orchestration

See `references/agent-orchestration.md` for full rules. Key constraints:

1. **Max concurrency**: 5 agents simultaneously
2. **Phase 0 (multi)**: One agent per book, max 3 books parallel. Within a book: sequential chapter reading.
3. **Phase 0 (single)**: Sequential chapter reading, one agent.
4. **Phase 1 (multi)**: Single agent (architecture requires holistic view, not parallel).
5. **Phase 1 (single)**: Single agent for translation, sequential chapters.
6. **Phase 2 (multi)**: One chapter at a time. Within a chapter: max 3 section agents parallel.
7. **Phase 2 (single)**: Assembly agent, sequential tasks.
8. **Phase 3**: Validation agents can run parallel (max 3).
9. **Dependency ordering**: For web sources, resolve all links/references within a page before moving to next page.
10. **Error recovery**: Failed agent = retry once with different approach. Second failure = pause and ask user.

## Quality Standards

- Reader cannot identify content sources (multi-source mode)
- Chapter skeleton survives reverse coverage check (multi-source mode)
- Every addition has source, location, benefit
- Duplicates merged or cross-referenced
- Output ready for review-tech-book via `report.md`
- Integration level: L3 (reorganize) or L4 (full fusion) only -- see `references/full-integration.md` (multi-source mode)
- Natural Chinese, no translationese (single-source mode)
- 1:1 paragraph mapping preserved (single-source mode)
- Terms, numbering, navigation, images, code comments correct on first pass

## Reference Files

| File | Purpose | Mode |
|------|---------|------|
| `references/agent-orchestration.md` | Sub-agent rules and constraints | Both |
| `references/knowledge-index-format.md` | Knowledge index structure | Multi |
| `references/book-architecture.md` | Architecture design guide | Multi |
| `references/full-integration.md` | Integration levels and rewrite method | Multi |
| `references/integration-discipline.md` | Integration discipline rules | Multi |
| `references/synthesis-methodology.md` | Content synthesis methods | Multi |
| `references/quality-gate.md` | Quality gate specifications | Multi |
| `references/context-passing.md` | Context passing between agents | Both |
| `references/translation-rules.md` | Translation rules and guidelines | Single |
| `references/book-assembly.md` | HTML assembly and scaffold guide | Both |
| `shared/translationese-patterns.md` | Translationese detection patterns | Single |
| `shared/anti-slacking.md` | Anti-slacking rules | Both |
| `shared/report-templates.md` | Report format templates | Both |
