# Progress Protocol

> Shared by all book skills. Run discovery, state files, save timing, idempotency, recovery.

## Run Directory

```
.book-doc/
├── spec.md                          # cross-run config
├── knowledge_base/                  # cross-run KB (generate-book multi mode)
└── runs/
    └── {YYYYMMDD}-{slug}-{label}/
        ├── progress.md              # single source of truth
        ├── context-summary.md       # cross-phase summary (generate-book)
        ├── plan.md                  # generation plan
        ├── findings/                # review findings
        └── report.md                # completion report
```

## Run Slugs

| Skill | Slug |
|-------|------|
| generate-book | generate |
| review-tech-book | review |
| codebase-book | codebase |

## Phase Completion Protocol

**Every phase end** (mandatory, no skipping):

1. **Write outputs**: Confirm all files written to disk.
2. **Update progress.md**: Mark phase ✅, write output paths.
3. **Read back**: Verify progress.md actually says ✅.
4. **Next phase**: Only after 1-3 pass.

## Reading Evidence Protocol

> Prevent "claimed read but didn't".

**Every claimed read** must include ≥2 of:
- **Structure**: paragraph count, code block count, total lines
- **Content summary**: specific arguments (not title rewrite)
- **Terms**: ≥3 actual technical terms from the file

**Red flags = unread**:
- "No issues" without evidence
- Content summary is title rewrite
- Consecutive chapters have identical evidence format
- "This chapter is simple" without structure data

## Recovery

1. Scan `.book-doc/runs/` for `*{slug}*`
2. Read `progress.md` of candidate runs
3. Single active/interrupted → resume directly
4. Multiple → ask user
5. None or all completed → create new run

## Cross-Skill Report Lookup

Find latest `completed` run by date prefix:
- Generation: `*-generate-*/report.md`
- Review: `*-review-*/report.md`
- Codebase: `*-codebase-*/report.md`

Missing reports: record and ask user if it affects correctness.
