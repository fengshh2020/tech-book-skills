# Skill Architecture Refactor: generate-book + translate-book Absorption

Date: 2026-06-12

## Problem Statement

Current architecture has a misaligned responsibility boundary:

1. `integrate-books` only handles multi-book integration, but single-book "generation" (translate + assemble) is a natural subset (100% weight on one source)
2. `translate-book` is too heavy — it does both translation AND book assembly (scaffold, CSS, JS, navigation, page design)
3. `translate-book` is never used standalone — it's always called as part of a book generation pipeline
4. The name "integrate-books" doesn't cover the single-source case

## Design Decisions

### Decision 1: Rename integrate-books → generate-book

The skill handles both single-source (translate + assemble) and multi-source (integrate + assemble) book generation. The name should reflect this broader scope.

### Decision 2: Absorb translate-book into generate-book

translate-book is never used standalone. Its translation rules become a reference file within generate-book. Its assets (CSS/JS) move to generate-book/assets/. The translate-book directory is deleted.

### Decision 3: Dual-Mode Architecture

generate-book supports two modes:
- **Single-source mode**: 1 book → extract → translate → assemble → validate → report
- **Multi-source mode**: 2+ books → deep-read → architecture → generate → validate → report

Mode is auto-detected by source count. Both modes share the assemble, validate, and report phases.

### Decision 4: Separate Translation Rules from Book Assembly Rules

Current translate-book/references/spec.md mixes translation rules with page design rules. These split into:
- `generate-book/references/translation-rules.md` — pure translation concerns
- `generate-book/references/book-assembly.md` — HTML scaffold, CSS, navigation, design system

## Dual-Mode Architecture

### Single-Source Mode

```
Phase 0: Extract & Read
  0.1 Source Inventory (EPUB/HTML parsing)
  0.2 Chapter-by-Chapter Reading
  0.3 Gate 0 (all chapters read with evidence)

Phase 1: Translate
  1.1 Load Translation Rules (translation-rules.md, shared/translationese-patterns.md)
  1.2 Per-Chapter Translation (1:1 paragraph mapping)
  1.3 Terminology Consistency Check
  1.4 Translationese Scan
  1.5 Gate 1 (all chapters translated, terms consistent)

Phase 2: Assemble
  2.1 HTML Scaffold (book-assembly.md)
  2.2 CSS/JS Integration
  2.3 Navigation & Cross-References
  2.4 Gate 2 (all files assembled, links valid)

Phase 3: Validate
  3.1 Coverage validation (100% of source translated)
  3.2 Term consistency (full book grep)
  3.3 Code runnability check
  3.4 Style consistency
  3.5 Gate 3

Phase 4: Report
  4.1 Write report.md
  4.2 Gate 4
```

### Multi-Source Mode

Same as current integrate-books sub-phase architecture (16+ sub-phases across 5 phases), with the addition of Phase 2 including the Assemble sub-steps (scaffold, CSS/JS, navigation) that are currently missing.

```
Phase 0: Deep Reading (5 sub-phases — unchanged)
Phase 1: Architecture Design (6 sub-phases — unchanged)
Phase 2: Chapter Generation (5 sub-phases per chapter — unchanged)
  + 2.6 Assemble (scaffold, CSS/JS, navigation) — NEW
Phase 3: Validation (enhanced — unchanged)
Phase 4: Report (enhanced — unchanged)
```

### Mode Selection

Auto-detect: source count = 1 → single mode, source count >= 2 → multi mode.
Explicit override: `--mode single` or `--mode multi`.

## File Structure After Refactor

```
tech_book_skills/
├── generate-book/                    # NEW (renamed from integrate-books)
│   ├── SKILL.md                      # Dual-mode entry point
│   ├── references/
│   │   ├── agent-orchestration.md    # From integrate-books
│   │   ├── book-architecture.md      # From integrate-books
│   │   ├── book-assembly.md          # NEW (from translate-book spec.md page design + html-templates.md)
│   │   ├── context-passing.md        # From integrate-books
│   │   ├── full-integration.md       # From integrate-books
│   │   ├── integration-discipline.md # From integrate-books
│   │   ├── knowledge-index-format.md # From integrate-books
│   │   ├── quality-gate.md           # From integrate-books
│   │   ├── synthesis-methodology.md  # From integrate-books
│   │   └── translation-rules.md      # NEW (from translate-book spec.md + red-lines.md + common-pitfalls.md)
│   ├── scripts/
│   │   ├── check_coverage.sh         # From integrate-books
│   │   └── workflow.py               # From integrate-books (enhanced for dual-mode)
│   ├── assets/
│   │   ├── style.css                 # From translate-book
│   │   └── script.js                 # From translate-book
│   └── agents/
│       └── openai.yaml               # From integrate-books
├── review-tech-book/                 # Unchanged
├── codebase-book/                    # Unchanged
├── shared/                           # Unchanged (skill-boundaries.md updated)
├── evals/                            # Unchanged
└── README.md                         # Updated
```

## Translation Rules Migration

### Source Files → Target

| Source | Content | Target Section |
|--------|---------|----------------|
| `translate-book/references/spec.md` lines 1-56 | Translation principles, terminology rules, code block handling | Translation Principles, Terminology Rules, Code Block Handling |
| `translate-book/references/spec.md` lines 57-136 | Formatting standards, validation checklist | Formatting Standards, Red-Line Checklist |
| `translate-book/references/spec.md` lines 137-174 | Page design direction, CSS class names | → `book-assembly.md` (not translation-rules.md) |
| `translate-book/references/red-lines.md` | Hard-line checks | Red-Line Checklist |
| `translate-book/references/common-pitfalls.md` | Common translation mistakes | Common Pitfalls |
| `shared/translationese-patterns.md` | Translationese anti-patterns | Reference (stays in shared/) |

### Resulting translation-rules.md Structure

```markdown
# Translation Rules

> For generate-book single-source mode and multi-source mode translation steps.

## Translation Principles
1. Faithfulness first, clarity as foundation
2. Technical terms retain English
3. Code blocks never translated (comments translated to Chinese)
4. Structure 1:1 mapping

## Terminology Rules
### Must Retain English
(Python keywords, stdlib modules, protocols, type annotations, CLI commands, OS concepts)

### First-Occurrence English Annotation
(Translation table: English → Chinese)

### Never Translate
(Code variables, inline code, file paths, CLI commands, names, URLs)

## Code Block Handling
1. Copy code verbatim from source
2. Translate code comments to Chinese
3. Preserve code structure, indentation, numbering

## Formatting Standards
### Punctuation
### Spacing
### Headings
### Terminology formatting

## Common Pitfalls
(From translate-book/references/common-pitfalls.md)

## Red-Line Checklist
(From translate-book/references/red-lines.md + spec.md validation section)

## Translationese Reference
See `../shared/translationese-patterns.md` for the full anti-pattern list.
```

## Book Assembly Rules Migration

### Source → Target

| Source | Content |
|--------|---------|
| `translate-book/references/spec.md` "页面设计方向" section | Page design system, CSS class conventions |
| `translate-book/references/html-templates.md` | HTML scaffold structure, file numbering |

### Resulting book-assembly.md Structure

```markdown
# Book Assembly

> For generate-book Phase 2 (Assemble sub-phase). Handles HTML scaffold, CSS/JS, navigation.

## HTML Scaffold Structure
(File numbering, cover, TOC, chapters, appendices)

## CSS/JS Integration
(style.css and script.js features, theme system, responsive design)

## Navigation Structure
(Top nav, TOC dropdown, prev/next, keyboard navigation)

## Page Design System
(Quiet luxury design language, adaptive heading levels, glass-morphism, code blocks)

## CSS Class Naming Conventions
(.chapter, .sidebar, .CodeListingCaption, .page-nav, etc.)
```

## workflow.py Enhancement

### New: Mode Detection

```python
# In workflow.py
def detect_mode(run_dir: Path) -> str:
    """Auto-detect single vs multi source mode."""
    inventory = run_dir / ".book-doc" / "knowledge_base" / "INVENTORY.md"
    if not inventory.exists():
        return "unknown"
    content = inventory.read_text()
    book_count = len(re.findall(r'^\|\s*\w+', content, re.MULTILINE)) - 1  # minus header
    if book_count <= 1:
        return "single"
    return "multi"
```

### New: Single-Mode Sub-Phases

```python
SINGLE_MODE_SUB_PHASES = {
    "0": ["0.1", "0.2", "0.3"],      # Extract & Read
    "1": ["1.1", "1.2", "1.3", "1.4", "1.5"],  # Translate
    "2": ["2.1", "2.2", "2.3", "2.4"],  # Assemble
    "3": ["3.1", "3.2", "3.3", "3.4", "3.5"],  # Validate
    "4": ["4.1", "4.2"],              # Report
}
```

### New: Mode-Aware Status

```bash
workflow.py generate-book <run_dir> status
# Shows: Mode: single (or multi), current phase, sub-phase progress
```

## shared/skill-boundaries.md Update

```markdown
| Task | Use | Don't Use |
|------|-----|-----------|
| Generate book from single source | generate-book (single mode) | translate-book |
| Generate book from multiple sources | generate-book (multi mode) | translate-book |
| Review generated book | review-tech-book | generate-book |
| Generate from codebase | codebase-book | generate-book |
| Generate + Review | generate-book → review-tech-book | skip review |
| Codebase + Review | codebase-book → review-tech-book | skip review |
| Regular code review | none | review-tech-book |
| Single term fix | edit directly | generate-book |
```

## Files to Create/Modify/Delete

### Create
1. `generate-book/SKILL.md` — Dual-mode entry point (from integrate-books/SKILL.md + single-mode additions)
2. `generate-book/references/translation-rules.md` — Merged translation rules
3. `generate-book/references/book-assembly.md` — Book assembly rules
4. `generate-book/references/agent-orchestration.md` — From integrate-books
5. `generate-book/references/book-architecture.md` — From integrate-books
6. `generate-book/references/context-passing.md` — From integrate-books
7. `generate-book/references/full-integration.md` — From integrate-books
8. `generate-book/references/integration-discipline.md` — From integrate-books
9. `generate-book/references/knowledge-index-format.md` — From integrate-books
10. `generate-book/references/quality-gate.md` — From integrate-books
11. `generate-book/references/synthesis-methodology.md` — From integrate-books
12. `generate-book/scripts/workflow.py` — Enhanced for dual-mode
13. `generate-book/scripts/check_coverage.sh` — From integrate-books
14. `generate-book/assets/style.css` — From translate-book
15. `generate-book/assets/script.js` — From translate-book
16. `generate-book/agents/openai.yaml` — From integrate-books

### Modify
17. `shared/skill-boundaries.md` — Remove translate-book references, add generate-book
18. `README.md` — Update skill table and architecture diagram

### Delete
19. `integrate-books/` — Entire directory (replaced by generate-book)
20. `translate-book/` — Entire directory (absorbed into generate-book)

## Files NOT Modified

- `shared/` files (except skill-boundaries.md) — unchanged
- `review-tech-book/` — unchanged
- `codebase-book/` — unchanged
- `evals/` — unchanged
