# Quality Ownership

> Shared by all book skills. Who fixes what, when.

## Principles

1. **First-time right**: Generation phase fixes what it can verify. Don't pass typos, format, links to review.
2. **Systemic only**: Review reports cross-chapter patterns, not point-by-point issues.
3. **Integration owns style**: generate-book adapts style and removes duplicates. Review only checks reader-visible seams.
4. **Source traceable**: codebase-book provides file:line evidence. Review verifies coverage and learning path.

## Responsibility

| Issue | Owner | Reviewer |
|-------|-------|----------|
| Typos, encoding, punctuation | generate-book | Report systemic patterns only |
| Terminology, glossary | generate-book | Cross-chapter inconsistencies |
| Code blocks, images, nav links | generate-book / codebase-book | Reference validation summary |
| Content source, style, dedup | generate-book | Reader-visible seams |
| Source coverage, excerpts | codebase-book | Coverage table, evidence chain |
| Technical correctness, versions | review-tech-book | V1-V3 evidence |
| Learning path, reader fit | review-tech-book | Core output |

## Report Deduplication

- Same issue type >3 times → merge into systemic finding
- Automation already listed → report summary only
- Score table ≠ issue list: scores are judgments, details in findings
