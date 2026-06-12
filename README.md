# Tech Book Skills

AI agent skills for processing technical books — generate, review, and create project-driven learning guides.

## Skills

| Skill | Purpose |
|-------|---------|
| **generate-book** | Generate a unified book from sources or codebase (single-source: translate+assemble, multi-source: integrate+assemble, codebase: discover+analyze+generate) |
| **review-tech-book** | Structured quality review with evidence-based findings and fix mode |

## Architecture

```
tech_book_skills/
├── generate-book/                    # Book generation (3 modes)
│   ├── SKILL.md                      # Hub: mode selection, core rules, reference index
│   ├── references/
│   │   ├── shared-rules.md           # Iron law, pre-flight, failure modes, coverage guardian, agent orchestration
│   │   ├── mode-single.md            # Single-source mode: extract → translate → assemble
│   │   ├── mode-multi.md             # Multi-source mode: deep-read → architect → integrate
│   │   ├── mode-codebase.md          # Codebase mode: discover → analyze → plan → generate
│   │   ├── agent-orchestration.md    # Sub-agent rules and constraints
│   │   ├── book-assembly.md          # HTML scaffold and assembly
│   │   ├── translation-rules.md      # Translation guidelines (single-source)
│   │   ├── book-architecture.md      # Architecture design (multi-source)
│   │   ├── full-integration.md       # Integration levels (multi-source)
│   │   ├── analysis-guide.md         # Module analysis (codebase)
│   │   ├── writing-and-content.md    # Content depth (codebase)
│   │   ├── writing-guide.md          # Writing style (codebase)
│   │   └── ...                       # Other reference files
│   ├── scripts/
│   │   ├── workflow.py               # Gate checks and progress recording
│   │   ├── validate_output.sh        # HTML output validation
│   │   ├── render_drawio_diagrams.py # Diagram rendering
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
    ├── discipline-framework.md       # Shared discipline: gate degradation, error recovery, progress tracking
    ├── anti-slacking.md              # Anti-slacking rules
    ├── report-templates.md           # Report templates
    ├── translationese-patterns.md    # Anti-pattern list
    ├── validate_tech.py              # Technical accuracy validation
    ├── validate_terms.py             # Terminology consistency validation
    └── workflow.py                   # Shared workflow engine
```

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

- **Progressive disclosure**: SKILL.md under 150 lines, details in reference files
- **Shared discipline**: Common gate/error/progress patterns in `shared/discipline-framework.md`
- **Robustness**: Pre-flight checks, gate degradation, error recovery, output validation
- **Evidence-based**: Every finding needs a direct quote (review), every claim needs file:line (codebase)

## License

MIT
