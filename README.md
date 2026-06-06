# Tech Book Skills

AI agent skills for processing technical books — translate, review, integrate, and generate project-driven learning guides.

## Skills

| Skill | Purpose |
|-------|---------|
| **translate-book** | Translate EPUB technical books into Chinese HTML sites |
| **review-tech-book** | Structured quality review with evidence-based findings |
| **codebase-book** | Generate project-driven learning books from codebases |
| **integrate-books** | Synthesize multiple technical books into one coherent book |

## Architecture

```
tech_book_skills/
├── translate-book/       # EPUB → Chinese HTML translation
│   ├── SKILL.md          # Skill definition (start here)
│   ├── references/       # Translation rules, templates, pitfalls
│   ├── scripts/          # Output validation (validate_format.sh)
│   └── assets/           # style.css, script.js
├── review-tech-book/     # Quality review
│   ├── SKILL.md
│   ├── references/       # Scoring dimensions, reviewer discipline
│   └── scripts/          # Code validation (validate_code.sh)
├── codebase-book/        # Codebase → learning book
│   ├── SKILL.md
│   ├── references/       # Analysis guide, writing guide
│   └── scripts/          # Output validation (validate_output.sh)
├── integrate-books/      # Multi-book synthesis
│   ├── SKILL.md
│   ├── references/       # Synthesis methodology, integration discipline
│   └── scripts/          # Coverage check (check_coverage.sh)
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
translate-book → integrate-books → review-tech-book
                 codebase-book  → review-tech-book
```

## Validation

```bash
python3 evals/validate_skill_pack.py
```

Checks skill metadata, resource links, script syntax, forbidden phrases, and cross-skill contracts.

## License

MIT
