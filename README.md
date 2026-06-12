# Tech Book Skills

AI agent skills for processing technical books — generate, review, and create project-driven learning guides.

## Skills

| Skill | Purpose |
|-------|---------|
| **generate-book** | Generate a unified book from one or more sources (single: translate+assemble, multi: integrate+assemble) |
| **review-tech-book** | Structured quality review with evidence-based findings |
| **codebase-book** | Generate project ownership mastery guides from codebases |

## Architecture

```
tech_book_skills/
├── generate-book/        # Book generation (single or multi source)
│   ├── SKILL.md          # Dual-mode entry point
│   ├── references/       # Translation rules, book assembly, integration methodology
│   ├── scripts/          # workflow.py, check_coverage.sh
│   ├── assets/           # style.css, script.js
│   └── agents/           # openai.yaml
├── review-tech-book/     # Quality review
│   ├── SKILL.md
│   ├── references/       # Scoring dimensions, reviewer discipline
│   └── scripts/          # Code validation (validate_code.sh)
├── codebase-book/        # Codebase → project ownership mastery guide
│   ├── SKILL.md
│   ├── references/       # Analysis guide, developer workflow, writing guide
│   └── scripts/          # Output validation (validate_output.sh)
├── shared/               # Cross-skill protocols
│   ├── progress-protocol.md      # Run management & recovery
│   ├── quality-ownership.md      # Quality responsibility boundaries
│   ├── skill-boundaries.md       # When to use which skill
│   ├── runtime-pruning.md        # Scope control for long runs
│   ├── verification-levels.md    # V1-V4 evidence classification
│   ├── translationese-patterns.md # Anti-pattern list
│   ├── report-templates.md       # Report templates
│   └── agent-compatibility.md    # Cross-agent path conventions
└── evals/                # Validation
    ├── evals.json        # Test cases
    └── validate_skill_pack.py  # Structure & contract validation
```

## Quick Start

1. Install as a skill pack in your agent's skills directory
2. The agent discovers skills via `SKILL.md` frontmatter `description` field
3. Skills reference each other through `.book-doc/runs/` reports

## Skill Workflow

```
generate-book (single or multi) → review-tech-book
codebase-book  → review-tech-book
```

## Validation

```bash
python3 evals/validate_skill_pack.py
```

Checks skill metadata, resource links, script syntax, forbidden phrases, and cross-skill contracts.

## License

MIT
