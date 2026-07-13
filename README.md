# Tech Book Skills

AI agent skills for processing technical books — generate, review, and create project-driven learning guides.

## Skills

| Skill | Purpose |
|-------|---------|
| **generate-book** | Generate a unified book from sources or codebase. Source type (single/multi/codebase) × product shape (book: full HTML+MD pipeline / doc: lightweight in-place MD like `proj/book.md`) |
| **review-tech-book** | Structured quality review with evidence-based findings and fix mode |

## Architecture

```
tech_book_skills/
├── generate-book/                    # Book generation (3 modes)
│   ├── SKILL.md                      # Hub: mode selection, core rules, reference index
│   ├── references/
│   │   ├── product-shapes.md         # book vs doc product shape + doc lightweight gate
│   │   ├── shared-rules.md           # Iron law, pre-flight, failure modes, agent orchestration
│   │   ├── mode-single.md            # Single-source: extract → translate → assemble
│   │   ├── mode-multi.md             # Multi-source: deep-read → architect → integrate (+ context-passing)
│   │   ├── mode-codebase.md          # Codebase: discover → analyze → plan → generate
│   │   ├── multi-read-architect.md   # Multi Phase 0-1: knowledge index format + architecture
│   │   ├── multi-synthesis.md        # Multi Phase 2-3: synthesis + L1-L4 + gates G1-G13 + coverage
│   │   ├── agent-orchestration.md    # Sub-agent orchestration strategy
│   │   ├── md-authoring.md           # MD authoring conventions + component map (pragmatic subset)
│   │   ├── translation-rules.md      # Translation guidelines (single-source)
│   │   ├── analysis-guide.md         # Module analysis (codebase)
│   │   └── writing-and-content.md    # Writing & content depth (codebase)
│   ├── scripts/
│   │   ├── workflow.py               # Gate checks and progress recording
│   │   ├── build_html.py             # MD → HTML builder (ADR-0001, dual-format)
│   │   ├── validate_output.sh        # HTML output validation
│   │   └── check_coverage.sh         # Coverage checking
│   └── assets/
│       ├── style.css                 # Book stylesheet
│       └── script.js                 # Book interactivity
├── review-tech-book/                 # Quality review
│   ├── SKILL.md                      # Hub: workflow, phases, gate checks
│   ├── references/
│   │   ├── review-shared-rules.md    # Iron law, evidence levels, finding quality control
│   │   ├── spec.md                   # Review specification
│   │   ├── execution-guardrails.md   # Execution rules
│   │   ├── reviewer-discipline.md    # Review discipline
│   │   ├── excellence-dimensions.md  # Scoring dimensions
│   │   ├── apply-fixes.md            # Fix mode guide
│   │   └── ...                       # Other reference files
│   ├── scripts/
│   │   ├── review_workflow.py        # Review state management
│   │   └── validate_code.sh          # Code validation
│   └── assets/
│       ├── style.css
│       └── script.js
└── shared/                           # Cross-skill resources
    ├── discipline-framework.md       # Anti-slacking, gate degradation, error recovery, progress (merged anti-slacking)
    ├── progress-protocol.md          # Run structure, reading-evidence protocol, recovery
    ├── report-templates.md           # Report templates
    ├── translationese-patterns.md    # Anti-pattern list (regex source)
    ├── validate_tech.py              # Technical accuracy validation
    ├── validate_terms.py             # Terminology consistency validation
    └── workflow.py                   # Shared workflow engine
```

## 输出格式（双格式，ADR-0001）

**MD 是信息主源**：agent 在 `{RUN}/src/` 写 MD 章节 + `book.yml`，运行 `scripts/build_html.py {RUN}/src {RUN}/output` 渲染：

- `output/` —— HTML 版（"静奢"设计系统，light-only，含封面/目录/翻页/mermaid→PNG）
- `output-md/` —— 可移植 MD 版（mermaid→PNG 嵌入，GitHub/VS Code 直读）

作者约定见 `generate-book/references/md-authoring.md`；架构决策见 `docs/adr/`：
- **ADR-0001** MD 为源·builder 渲染 ｜ **ADR-0002** 富组件务实子集映射
- **ADR-0003** light-only（去暗色）｜ **ADR-0004** Mermaid→PNG

## Skill Workflow

```
generate-book → review-tech-book → generate-book (fix mode)
```

1. **generate-book** creates the book (single/multi/codebase mode)
2. **review-tech-book** reviews it (report only by default)
3. If issues found, user requests **review-tech-book fix mode** or feeds report back to **generate-book**

## Quick Start

1. Install as a skill pack in your agent's skills directory
2. The agent discovers skills via `SKILL.md` frontmatter `description` field
3. Each skill uses progressive disclosure: SKILL.md (hub) → reference files (detail)

## Design Principles

- **Source type × product shape (orthogonal)**: any source (single/multi/codebase) can produce either a `book` (full HTML+MD pipeline via builder) or a `doc` (lightweight in-place MD like `proj/book.md`, no builder, trimmed gates). See `generate-book/references/product-shapes.md`
- **Progressive disclosure**: SKILL.md under 150 lines, details in reference files
- **MD as source (ADR-0001)**: agent writes portable MD; `build_html.py` renders the "Quiet Luxury" HTML edition + a portable MD edition; light-only (ADR-0003), Mermaid→PNG (ADR-0004)
- **Shared discipline**: Common anti-slacking/gate/error/progress patterns canonical in `shared/discipline-framework.md` (anti-slacking merged in), referenced (not duplicated) by each skill's shared-rules
- **Robustness**: Pre-flight checks, gate degradation, error recovery, output validation
- **Evidence-based**: Every finding needs a direct quote (review), every claim needs file:line (codebase)

## License

MIT
