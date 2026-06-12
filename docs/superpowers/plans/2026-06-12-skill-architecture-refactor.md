# Skill Architecture Refactor: generate-book Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename integrate-books → generate-book with dual-mode (single/multi source), absorb translate-book's translation rules and assets, delete old directories.

**Architecture:** Copy integrate-books/ to generate-book/, add single-source mode phases, create translation-rules.md and book-assembly.md from translate-book's files, copy assets, enhance workflow.py with mode detection, update shared/skill-boundaries.md and README.md, then delete integrate-books/ and translate-book/.

**Tech Stack:** Python 3 (workflow.py), Markdown (SKILL.md + references), Bash (check_coverage.sh)

---

## File Structure (After Refactor)

```
generate-book/
├── SKILL.md                          # Dual-mode entry point (NEW)
├── references/
│   ├── agent-orchestration.md        # Copy from integrate-books
│   ├── book-architecture.md          # Copy from integrate-books
│   ├── book-assembly.md              # NEW (from translate-book html-templates.md + spec.md page design)
│   ├── context-passing.md            # Copy from integrate-books
│   ├── full-integration.md           # Copy from integrate-books
│   ├── integration-discipline.md     # Copy from integrate-books
│   ├── knowledge-index-format.md     # Copy from integrate-books
│   ├── quality-gate.md               # Copy from integrate-books
│   ├── synthesis-methodology.md      # Copy from integrate-books
│   └── translation-rules.md          # NEW (from translate-book spec.md + red-lines.md + common-pitfalls.md)
├── scripts/
│   ├── check_coverage.sh             # Copy from integrate-books
│   └── workflow.py                   # Enhanced (from integrate-books + mode detection)
├── assets/
│   ├── style.css                     # Copy from translate-book
│   └── script.js                     # Copy from translate-book
└── agents/
    └── openai.yaml                   # Copy from integrate-books
```

---

### Task 1: Create generate-book directory and copy integrate-books files

**Files:**
- Create: `generate-book/` directory tree
- Copy: all files from `integrate-books/` to `generate-book/`

- [ ] **Step 1: Create directory structure and copy files**

```bash
cd /home/hsf/projects/others/tech_book_skills
mkdir -p generate-book/references generate-book/scripts generate-book/assets generate-book/agents
cp integrate-books/references/*.md generate-book/references/
cp integrate-books/scripts/*.sh generate-book/scripts/ 2>/dev/null; true
cp integrate-books/scripts/workflow.py generate-book/scripts/
cp integrate-books/agents/openai.yaml generate-book/agents/
```

- [ ] **Step 2: Verify copy**

```bash
ls -la generate-book/references/ && ls -la generate-book/scripts/ && ls -la generate-book/agents/
```

Expected: 8 reference files, check_coverage.sh, workflow.py, openai.yaml

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/
git commit -m "feat: create generate-book directory with integrate-books content"
```

---

### Task 2: Copy translate-book assets to generate-book

**Files:**
- Copy: `translate-book/assets/style.css` → `generate-book/assets/style.css`
- Copy: `translate-book/assets/script.js` → `generate-book/assets/script.js`

- [ ] **Step 1: Copy assets**

```bash
cd /home/hsf/projects/others/tech_book_skills
cp translate-book/assets/style.css generate-book/assets/style.css
cp translate-book/assets/script.js generate-book/assets/script.js
```

- [ ] **Step 2: Verify**

```bash
ls -la generate-book/assets/
```

Expected: style.css and script.js

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/assets/
git commit -m "feat: copy translate-book assets to generate-book"
```

---

### Task 3: Create translation-rules.md from translate-book sources

**Files:**
- Create: `generate-book/references/translation-rules.md`

This file merges content from 3 translate-book reference files (spec.md, red-lines.md, common-pitfalls.md), extracts ONLY translation concerns (not page design/assembly), and writes everything in English.

- [ ] **Step 1: Write translation-rules.md**

The agent should read these 3 source files and create the merged translation-rules.md:
- `/home/hsf/projects/others/tech_book_skills/translate-book/references/spec.md` (translation principles, terminology rules, code block handling, formatting standards, validation checklist — NOT the page design section at lines 137-174)
- `/home/hsf/projects/others/tech_book_skills/translate-book/references/red-lines.md` (hard-line checks)
- `/home/hsf/projects/others/tech_book_skills/translate-book/references/common-pitfalls.md` (common translation mistakes with examples)

Write to: `/home/hsf/projects/others/tech_book_skills/generate-book/references/translation-rules.md`

The file must be fully in English and structured as:
1. Translation Principles (from spec.md "翻译原则")
2. Terminology Rules (from spec.md "术语规则")
3. Code Block Handling (from spec.md "代码块处理")
4. Formatting Standards (from spec.md "排版规范")
5. Common Pitfalls (from common-pitfalls.md — translate the tables and examples to English)
6. Red-Line Checklist (from red-lines.md + spec.md "校验清单" — translate to English)
7. Translationese Reference (pointer to `../shared/translationese-patterns.md`)

- [ ] **Step 2: Verify file exists and has no Chinese structural headers**

```bash
grep -cP '[\x{4e00}-\x{9fff}]' /home/hsf/projects/others/tech_book_skills/generate-book/references/translation-rules.md
```

Expected: Chinese content in examples/terminology table is OK. Chinese in section headers is NOT OK.

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/references/translation-rules.md
git commit -m "feat: create translation-rules.md from translate-book sources"
```

---

### Task 4: Create book-assembly.md from translate-book sources

**Files:**
- Create: `generate-book/references/book-assembly.md`

This file merges content from translate-book's page design and HTML template files, extracting ONLY the assembly/structure concerns.

- [ ] **Step 1: Write book-assembly.md**

The agent should read these source files and create book-assembly.md:
- `/home/hsf/projects/others/tech_book_skills/translate-book/references/spec.md` (only the "页面设计方向" section at lines 137-174)
- `/home/hsf/projects/others/tech_book_skills/translate-book/references/html-templates.md` (HTML scaffold, component templates, file numbering)

Write to: `/home/hsf/projects/others/tech_book_skills/generate-book/references/book-assembly.md`

The file must be fully in English and structured as:
1. HTML Scaffold Structure (page skeleton, file numbering from html-templates.md)
2. Page Types (cover, TOC, preface, chapter, appendix, glossary — from html-templates.md)
3. Content Components (code blocks, sidebars, tables, glossary terms — from html-templates.md)
4. CSS/JS Integration (design system features from spec.md "页面设计方向" + html-templates.md interaction system)
5. Navigation Structure (top nav, TOC dropdown, prev/next, keyboard — from html-templates.md)
6. CSS Class Naming Conventions (from spec.md "建议保留的结构类名" + html-templates.md components)
7. Advanced Components (v2.0 components from html-templates.md — collapsibles, code-tabs, quizzes, etc.)

- [ ] **Step 2: Verify**

```bash
wc -l /home/hsf/projects/others/tech_book_skills/generate-book/references/book-assembly.md
```

Expected: 300+ lines (this is a large reference file)

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/references/book-assembly.md
git commit -m "feat: create book-assembly.md from translate-book html-templates and page design"
```

---

### Task 5: Write dual-mode SKILL.md for generate-book

**Files:**
- Rewrite: `generate-book/SKILL.md`

- [ ] **Step 1: Write the new SKILL.md**

This must be a complete rewrite of the generate-book/SKILL.md (currently a copy of integrate-books/SKILL.md) to support dual-mode architecture. Read the current file at `/home/hsf/projects/others/tech_book_skills/generate-book/SKILL.md` first.

Key changes from integrate-books SKILL.md:
1. Frontmatter: `name: generate-book`, updated description to include both single and multi-source triggers
2. Add "Mode Selection" section: auto-detect by source count, or explicit `--mode`
3. Add "Single-Source Mode" section with its own phase flow (0: Extract, 1: Translate, 2: Assemble, 3: Validate, 4: Report)
4. Rename "Integrate Books" heading to "Generate Book"
5. Keep multi-source mode as "Multi-Source Mode" section (same as current Phase 0-4)
6. Add references to `translation-rules.md` and `book-assembly.md`
7. In multi-source Phase 2, add sub-phase 2.6 "Assemble" (scaffold, CSS/JS, navigation)
8. Update Coverage Guardian to note that in single-source mode, the "source ratio" checks are trivially satisfied (one source = 100%)

The file should be ~350 lines (larger than integrate-books SKILL.md due to dual-mode content).

- [ ] **Step 2: Verify structure**

```bash
grep -n "^## \|^### " /home/hsf/projects/others/tech_book_skills/generate-book/SKILL.md | head -50
```

Expected: Sections for both Single-Source Mode and Multi-Source Mode, Mode Selection, Coverage Guardian, Assemble sub-phase

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/SKILL.md
git commit -m "feat: write dual-mode SKILL.md for generate-book"
```

---

### Task 6: Enhance workflow.py for dual-mode support

**Files:**
- Modify: `generate-book/scripts/workflow.py`

- [ ] **Step 1: Enhance workflow.py**

Read the current file at `/home/hsf/projects/others/tech_book_skills/generate-book/scripts/workflow.py` first.

Add the following features:

1. **Mode detection function**: `detect_mode(run_dir)` — reads INVENTORY.md, counts source books, returns "single" or "multi"

2. **Single-mode sub-phases**:
```python
SINGLE_MODE_SUB_PHASES = {
    "0": ["0.1", "0.2", "0.3"],
    "1": ["1.1", "1.2", "1.3", "1.4", "1.5"],
    "2": ["2.1", "2.2", "2.3", "2.4"],
    "3": ["3.1", "3.2", "3.3", "3.4", "3.5"],
    "4": ["4.1", "4.2"],
}
```

3. **Multi-mode sub-phases** (same as current, but rename variable from `SUB_PHASES` to `MULTI_MODE_SUB_PHASES`)

4. **Mode-aware SubPhaseWorkflowLock**: accepts mode parameter, uses the correct sub-phase set based on mode

5. **Status command shows mode**: `workflow.py generate-book <run_dir> status` prints "Mode: single" or "Mode: multi"

6. **Skill name change**: all references to "integrate-books" → "generate-book"

7. **Add assemble sub-phase 2.6 for multi-mode**: `MULTI_MODE_SUB_PHASES["2"]` becomes `["2.1", "2.2", "2.3", "2.4", "2.5", "2.6"]`

Keep the CoverageGuardian and GateChecker classes unchanged (they work the same for both modes).

- [ ] **Step 2: Test workflow.py**

```bash
cd /home/hsf/projects/others/tech_book_skills
python3 generate-book/scripts/workflow.py generate-book /tmp/test-gen-run status
```

Expected: Shows mode: unknown, sub-phases for multi-mode (default)

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/scripts/workflow.py
git commit -m "feat: enhance workflow.py with dual-mode support for generate-book"
```

---

### Task 7: Update shared/skill-boundaries.md

**Files:**
- Modify: `shared/skill-boundaries.md`

- [ ] **Step 1: Read current file and rewrite**

Read `/home/hsf/projects/others/tech_book_skills/shared/skill-boundaries.md` first.

Replace all content with the new boundaries matrix (remove all translate-book references, add generate-book with single/multi modes):

```markdown
# Skill Boundaries

> Shared by all book skills. Who does what, when to hand off.

## Matrix

| Task | Use | Don't Use |
|------|-----|-----------|
| Generate book from single source | generate-book (single mode) | review-tech-book |
| Generate book from multiple sources | generate-book (multi mode) | review-tech-book |
| Review generated book | review-tech-book | generate-book |
| Generate from codebase | codebase-book | generate-book |
| Generate + Review | generate-book → review-tech-book | skip review |
| Codebase + Review | codebase-book → review-tech-book | skip review |
| Regular code review | none | review-tech-book |
| Single term fix | edit directly | generate-book |

## Handoff Rules

- generate-book → review-tech-book: pass `report.md`, unified terms, coverage, known limits
- codebase-book → review-tech-book: pass `report.md`, source coverage, file:line evidence
- review-tech-book → original: route fixes by ownership, batch by priority

## Principle

Don't pass low-level QA to another skill. Fix in generation phase.
```

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add shared/skill-boundaries.md
git commit -m "feat: update skill-boundaries.md for generate-book, remove translate-book"
```

---

### Task 8: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read current file and update**

Read `/home/hsf/projects/others/tech_book_skills/README.md` first.

Update the skills table and architecture diagram to reflect:
- `integrate-books` → `generate-book` with dual-mode description
- Remove `translate-book` from the skills table
- Update the skill workflow diagram
- Update the architecture tree

The new skills table:

```markdown
| Skill | Purpose |
|-------|---------|
| **generate-book** | Generate a unified book from one or more sources (single: translate+assemble, multi: integrate+assemble) |
| **review-tech-book** | Structured quality review with evidence-based findings |
| **codebase-book** | Generate project ownership mastery guides from codebases |
```

The new skill workflow:

```
generate-book (single or multi) → review-tech-book
codebase-book → review-tech-book
```

The new architecture tree (generate-book section replaces integrate-books + translate-book):

```
generate-book/
├── SKILL.md              # Dual-mode entry point
├── references/
│   ├── translation-rules.md  # Translation principles, terminology, pitfalls
│   ├── book-assembly.md      # HTML scaffold, CSS/JS, navigation, design
│   ├── book-architecture.md  # Architecture protocol (multi-mode)
│   ├── integration-discipline.md  # Correctness, completeness, style
│   ├── full-integration.md   # Integration levels, 5-step rewrite
│   ├── knowledge-index-format.md  # Index template (multi-mode)
│   ├── quality-gate.md       # Per-chapter gates G1-G8
│   ├── synthesis-methodology.md    # Narrative synthesis (multi-mode)
│   ├── agent-orchestration.md      # Sub-agent rules
│   └── context-passing.md    # Context protocol
├── scripts/
│   ├── workflow.py           # Dual-mode workflow orchestrator
│   └── check_coverage.sh     # Coverage check
├── assets/
│   ├── style.css             # Design system
│   └── script.js             # Interactive features
└── agents/
    └── openai.yaml           # Agent config
```

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add README.md
git commit -m "feat: update README.md for generate-book dual-mode, remove translate-book"
```

---

### Task 9: Delete integrate-books/ and translate-book/ directories

**Files:**
- Delete: `integrate-books/` (entire directory)
- Delete: `translate-book/` (entire directory)

- [ ] **Step 1: Verify generate-book is complete before deletion**

```bash
cd /home/hsf/projects/others/tech_book_skills
echo "=== generate-book references ===" && ls generate-book/references/
echo "=== generate-book scripts ===" && ls generate-book/scripts/
echo "=== generate-book assets ===" && ls generate-book/assets/
echo "=== SKILL.md exists ===" && test -f generate-book/SKILL.md && echo "yes" || echo "NO"
```

Expected: All files present

- [ ] **Step 2: Delete old directories**

```bash
cd /home/hsf/projects/others/tech_book_skills
git rm -r integrate-books/
git rm -r translate-book/
```

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git commit -m "feat: remove integrate-books and translate-book (replaced by generate-book)"
```

---

### Task 10: Final verification and commit

- [ ] **Step 1: Verify directory structure**

```bash
cd /home/hsf/projects/others/tech_book_skills
echo "=== Top-level dirs ===" && ls -d */ | grep -v '.git'
echo "=== generate-book references ===" && ls generate-book/references/
echo "=== No integrate-books ===" && test -d integrate-books && echo "ERROR: still exists" || echo "OK: removed"
echo "=== No translate-book ===" && test -d translate-book && echo "ERROR: still exists" || echo "OK: removed"
```

- [ ] **Step 2: Verify workflow.py works**

```bash
cd /home/hsf/projects/others/tech_book_skills
python3 generate-book/scripts/workflow.py generate-book /tmp/test-final status
```

- [ ] **Step 3: Verify no broken references to integrate-books or translate-book**

```bash
cd /home/hsf/projects/others/tech_book_skills
grep -r "integrate-books" --include="*.md" --include="*.py" --include="*.sh" generate-book/ shared/skill-boundaries.md README.md 2>/dev/null | grep -v "generate-book/references/" || echo "OK: no stale references"
grep -r "translate-book" --include="*.md" --include="*.py" --include="*.sh" generate-book/ shared/skill-boundaries.md README.md 2>/dev/null || echo "OK: no stale references"
```

Expected: No references to the old skill names in modified files (some reference files may legitimately mention integration concepts)

- [ ] **Step 4: Final commit if any fixes needed**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add -A
git diff --cached --stat
# If there are changes, commit them
git commit -m "fix: final cleanup for generate-book refactor" 2>/dev/null || echo "No changes needed"
```
