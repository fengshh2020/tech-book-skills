# Skill Boundaries

> Shared by all book skills. Who does what, when to hand off.

## Matrix

| Task | Use | Don't Use |
|------|-----|-----------|
| Generate book from single source | generate-book (single mode) | review-tech-book |
| Generate book from multiple sources | generate-book (multi mode) | review-tech-book |
| Fill missing chapters | generate-book (single mode) | review-tech-book |
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
