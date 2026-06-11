# Context Passing Protocol

LLMs lose context across phases in long workflows. This protocol solves the problem through structured phase summaries and a progress file.

All files reside under the current run directory `.book-doc/runs/{id}/`.

## Two Files, Two Responsibilities

| File | Responsibility | Who Writes | Who Reads |
|------|---------------|------------|-----------|
| `progress.md` | Progress tracking: which phases/chapters are done, where to resume | Updated after each step completes | Read on resume to determine where to continue |
| `context-summary.md` | Knowledge transfer: cross-phase key findings and decisions | Appended after each (sub-)phase completes | Read at the start of the next phase to acquire context |

**progress.md answers "where are we"**, **context-summary.md answers "what do we know"**. They complement each other and cannot substitute for one another.

## Core Principle

At the end of each sub-phase, append a section to `context-summary.md` (each section ≤150 lines). When the next sub-phase starts, **read only this summary + the reference files for the current sub-phase**; there is no need to re-read the full output of prior sub-phases.

## Sub-Phase Context Tracking

Each sub-phase completion appends a structured section to `context-summary.md`. This ensures fine-grained knowledge continuity even within a single phase.

### Phase 0 Sub-Phases

| Sub-Phase | Description | Context Contributed |
|-----------|-------------|---------------------|
| 0.1 | Book Inventory | Source book paths, chapter counts, file formats, total scope |
| 0.2 | Per-Book Reading | Per-chapter reading evidence: paragraph counts, code block counts, specific terms |
| 0.3 | Index Generation | Per-book knowledge indexes (Teaching Philosophy, Depth Calibration, Integration Readiness) |
| 0.4 | Coverage Comparison | Topic overlaps, gaps, unique contributions, depth differences across books |
| 0.5 | Gate 0 | Verification: all indexes >=1000 lines, reading evidence complete, coverage comparison done |

### Phase 1 Sub-Phases

| Sub-Phase | Description | Context Contributed |
|-----------|-------------|---------------------|
| 1.1 | Load All Indexes | Read confirmation per book, key findings, methodology differences (>=3 points) |
| 1.2 | Cross-Book Analysis | Methodology differences, depth alignment, boundary complementarity, style resolution |
| 1.3 | Target TOC Design | Per-chapter cognitive load, prerequisites, capability output, methodology choices |
| 1.4 | Per-Chapter Plans | Self-contained integration plans: source mapping, synthesis strategy, concept bridging |
| 1.5 | Reverse Coverage | 100% source chapter disposition: main content / sidebar / appendix / exclusion |
| 1.6 | Gate 1 | Verification: all plans complete, no TBD, reverse coverage 100% |
| 1.4 | Methodology decisions | Key Methodology Decisions, evidence for each choice |
| 1.5 | Exclusion & scope | Exclusion Scope, downgrade rationale |
| 1.6 | Plan statistics & finalization | Integration Plan Statistics, estimated increment |

### Phase 2 Per-Chapter Sub-Phases

| Sub-Phase | Description | Context Contributed |
|-----------|-------------|---------------------|
| 2.1 | Chapter plan review | Chapter-specific source mapping, methodology selection |
| 2.2 | Content synthesis | Draft length, integration markers placed, code block count |
| 2.3 | Self-review & gate check | Gate results (G1-G6), issues found and resolutions |
| 2.4 | Chapter completion record | Final length, all gate passes, notes |

Each per-chapter sub-phase appends chapter-specific context so that subsequent chapters can reference decisions made in earlier chapters without re-reading the full output.

## Per-Phase Summary Format

### Phase 0 Sub-Phase Completion → append to `context-summary.md`

Each sub-phase (0.1-0.5) appends its own section. The complete Phase 0 contribution looks like:

```markdown
# Deep Reading Summary

## Source Book Overview
- [Source Book 1]: [N] chapters, index [M] rows, role [mainline/reinforcement/specialty/reference]
- [Source Book 2]: [N] chapters, index [M] rows, role [...]
- [Source Book 3]: [N] chapters, index [M] rows, role [...]

## Per-Book Core Methodology
- [Source Book 1]: [one-sentence summary of teaching approach]
- [Source Book 2]: [one-sentence summary of teaching approach]
- [Source Book 3]: [one-sentence summary of teaching approach]

## Key Findings
- [Important insights discovered during reading, e.g.: Book A and Book B have fundamentally different methodologies on topic X]
- [...]

## Style Baseline Points
- [Summary of each book's style characteristics, for later style harmonization]

## Potential Integration Challenges
- [Expected difficulties during integration]
```

Individual sub-phase contributions:

- **Sub-phase 0.1** appends: Source Book Overview
- **Sub-phase 0.2** appends: Per-Book Core Methodology
- **Sub-phase 0.3** appends: Key Findings
- **Sub-phase 0.4** appends: Style Baseline Points
- **Sub-phase 0.5** appends: Potential Integration Challenges

### Phase 1 Sub-Phase Completion → append to `context-summary.md`

Each sub-phase (1.1-1.6) appends its own section. The complete Phase 1 contribution looks like:

```markdown
## Architecture Design Summary

### Target Reader
- Assumptions: ...
- Use cases: ...

### Per-Book Role
- [Source Book 1]: [mainline/reinforcement/specialty/excluded], rationale...
- [Source Book 2]: [mainline/reinforcement/specialty/excluded], rationale...

### Final Skeleton
- Volumes: [list]
- Core path: [chapter range]
- Support path: [chapter range]
- Advanced path: [chapter range]

### Key Methodology Decisions
- [Topic A]: chose [Source Book X]'s methodology, because [rationale]
- [Topic B]: redesigned, because [rationale]

### Exclusion Scope
- [Topic]: exclusion/downgrade rationale

### Integration Plan Statistics
- Total chapters: [N]
- New chapters: [list]
- Estimated increment: [N] lines
```

Individual sub-phase contributions:

- **Sub-phase 1.1** appends: Target Reader
- **Sub-phase 1.2** appends: Per-Book Role
- **Sub-phase 1.3** appends: Final Skeleton
- **Sub-phase 1.4** appends: Key Methodology Decisions
- **Sub-phase 1.5** appends: Exclusion Scope
- **Sub-phase 1.6** appends: Integration Plan Statistics

### Phase 2 Per-Chapter Completion → append to `progress.md`

```markdown
## Ch[N] Completion Record
- Completed at: YYYY-MM-DD HH:MM
- Gate results: G1-G6 [pass/pass/pass/pass/pass/pass]
- Integration markers: [N]
- Code blocks: [N]
- Chapter length: [N] lines
- Notes: [if issues arose, record how they were handled]
```

Phase 2 per-chapter sub-phase context appended to `context-summary.md`:

```markdown
## Ch[N] Context
- Source mapping: [which source books contributed, roles]
- Methodology applied: [which teaching approach, with evidence]
- Key decisions: [chapter-specific methodology or content choices]
- Cross-references: [terms/concepts bridging to other chapters]
```

Individual sub-phase contributions for each chapter:

- **Sub-phase 2.1** appends: Source mapping and methodology selection
- **Sub-phase 2.2** appends: Draft statistics (length, markers, code blocks)
- **Sub-phase 2.3** appends: Gate results and issue resolutions
- **Sub-phase 2.4** appends: Final completion record

### Phase 3 Completion → append to `context-summary.md`

```markdown
## Validation Results Summary
- Coverage: [N]%
- Terminology consistency: [pass / issue count]
- Code runnability: [N/M passed]
- Style consistency: [pass / issue count]
- Known limitations: [list]
```

## Reading Rules

All paths are relative to the current run directory `.book-doc/runs/{current-run-id}/`.

| Phase | Must Read | Read on Demand |
|-------|-----------|----------------|
| Start / Resume | progress.md | -- |
| 0.1 | progress.md | references/knowledge-index-format.md |
| 0.2-0.5 | progress.md + context-summary.md (prior sub-phases) | references/agent-orchestration.md |
| 1.1 | progress.md + context-summary.md (Phase 0 section) | all knowledge indexes |
| 1.2-1.6 | progress.md + context-summary.md (Phase 0-1, prior sub-phases) | all knowledge indexes, references/book-architecture.md |
| 2.1 | progress.md + context-summary.md (Phase 0-1 sections) + current chapter's plan.md section | relevant knowledge index chapters |
| 2.2-2.4 | progress.md + context-summary.md (Phase 0-1 + prior Ch sections) + current chapter's plan.md section | references/full-integration.md |
| 3 | progress.md + context-summary.md (full) | references/quality-gate.md |
| 4 | progress.md + context-summary.md (full) | ../shared/report-templates.md |

Key rule: when starting any sub-phase, read the `context-summary.md` sections produced by all prior sub-phases (within the same phase and earlier phases) to maintain continuity. Do not re-read raw outputs from earlier sub-phases.

## Self-Contained Instruction Block for Phase 2

Each chapter execution in Phase 2 is self-contained: the integration instructions include all information the chapter needs, with no need to re-read other files. The instruction block for each chapter in `plan.md` should contain:

1. Current chapter state (existing content and structure)
2. Source mapping (which source books contribute what content, and their roles)
3. Methodology selection (which book's teaching approach is chosen, with evidence)
4. Depth alignment strategy (target depth, how each source's content aligns)
5. Content synthesis plan (section-by-section instructions)
6. Style baseline samples (1-2 paragraphs from the primary book's original text)
7. Relevant terminology conventions (terms involved in this chapter)
8. Concept bridging (connection to previous chapter, internal bridges, setup for next chapter)

**Knowledge indexes are read on demand**: the source mapping in `plan.md` indicates which chapters of which knowledge indexes to read. During Phase 2 execution, read them on demand rather than loading everything upfront.
