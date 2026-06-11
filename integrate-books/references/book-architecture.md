# Book Architecture Assessment Protocol

> For use by integrate-books Phase 1. Based on the deep knowledge indexes from Phase 0, design the architecture of the integrated book.
> Core principle: architecture design must be built on deep understanding — you cannot draw blueprints without first understanding the material.

## When to Use

- Multiple source books are being integrated into a single new book, with no clear primary book.
- The primary book's table of contents requires major restructuring rather than local supplementation.
- The user emphasizes "optimal chapter design," "knowledge organization," or "skeleton matters most."
- Early outputs consist only of outlines, short lecture notes, or sample chapters, which risk being misjudged as completed manuscripts.

## Prerequisites

**All knowledge indexes from Phase 0 must have passed the gate check.** You cannot enter Phase 1 without passing the Phase 0 gate.

Before Phase 1 begins, you must:
1. Read all knowledge indexes in full (not skim summaries)
2. Record read confirmation in progress.md
3. List core methodology differences across books (at least 3 points)

## Core Principles

**Architecture design is analytical work based on knowledge indexes, not TOC stitching.** Every chapter's existence, order, and depth must be supported by evidence from the knowledge indexes.

**The chapter skeleton is instructional design, not outline rearrangement.** Chapter order must serve the reader's cognitive dependencies: establish conceptual foundations first, then introduce tools, then organize projects, and finally advance to specialized topics.

**Source book coverage must be checked bidirectionally.** Proving "the target chapter references a knowledge point" is not enough; you must also reverse-check each source book's chapters and topics: assigned to a target chapter, demoted to sidebar/appendix, or explicitly excluded — one of the three must apply.

**Do not default to the largest or most authoritative book as the backbone.** Whether to adopt a particular book as the skeleton must be determined jointly by the target audience, learning path, modernity, engineering orientation, and chapter dependencies.

**Each chapter bears only one primary cognitive load.** If a single chapter contains multiple core models (e.g., resource model, error model, concurrency model, performance model), it should be split.

## Three Core Work Items of Phase 1

### Work Item 1: Cross-Book Deep Comparison [Sub-phase 1.2]

Based on the knowledge indexes, complete the following comparative analyses (output to `cross-book-analysis.md`):

#### Methodology Difference Analysis [Sub-phase 1.2.1]

For each major topic, analyze the teaching methodology differences across books:

```markdown
### Topic: [Topic Name]

| Dimension | [Source A] | [Source B] | [Source C] | Integration Choice | Rationale |
|-----------|------------|------------|------------|-------------------|-----------|
| Introduction style | [Problem-driven] | [Definition-first] | [Example-led] | [Which one] | [Why] |
| Teaching order | [A->B->C] | [B->A->C] | [C->A->B] | [Which one] | [Why] |
| Depth target | [Introductory] | [Intermediate] | [Advanced] | [Target depth] | [Why] |
| Unique value | [X] | [Y] | [Z] | [How to use] | [Why] |
| Teaching quality | [High/Med/Low] | [High/Med/Low] | [High/Med/Low] | — | — |
```

#### Depth Alignment Analysis [Sub-phase 1.2.2]

Identify depth differences across books on the same topic:

```markdown
### Depth Alignment Table

| Topic | [Source A] Depth | [Source B] Depth | Target Depth | Alignment Strategy |
|-------|-----------------|-----------------|--------------|-------------------|
| [Topic 1] | Introductory | Advanced | Intermediate | A for foundation + B for depth |
| [Topic 2] | Intermediate | Introductory | Intermediate | Primarily A; B supplements introductory perspective |
```

Alignment strategy options:
- **Foundation + Deepening**: The shallower book provides the basic framework; the deeper book provides advanced content.
- **Strength complement**: One book's strengths compensate for another's weaknesses.
- **Independent perspective**: Preserve distinctive perspectives from different books as sidebars.
- **Redesign**: Neither is satisfactory; design the teaching path for this topic from scratch.

#### Boundary Complementarity Analysis [Sub-phase 1.2.3]

Identify how the knowledge boundaries of each book complement one another:

```markdown
### Boundary Complementarity Table

| Topic | [Source A] Boundary | [Source B] Boundary | Complementarity |
|-------|--------------------|--------------------|----------------|
| [Topic 1] | Stops at X | Starts from X, goes to Y | A->B natural continuation |
| [Topic 2] | No practical coverage | Practice-oriented | A for concepts + B for practice |
```

#### Style Conflict Resolution [Sub-phase 1.2.4]

Identify style differences and formulate resolution strategies:

```markdown
### Style Resolution Table

| Style Dimension | [Source A] | [Source B] | Unified Style | Resolution Method |
|----------------|------------|------------|--------------|-------------------|
| Person | "We" | "You" | [Choice] | [How to unify] |
| Terminology | English + Local | Local only | [Choice] | [How to unify] |
| Code comments | Local language | English | [Choice] | [How to unify] |
| Code block length | 5-10 lines | 15-30 lines | [Choice] | [How to unify] |
```

### Work Item 2: Target TOC Design [Sub-phase 1.3]

Based on the cross-book comparative analysis, design the integrated table of contents structure.

**Design steps**:
1. Determine the target audience and use cases
2. Determine the primary skeleton source (not necessarily any single source book's original TOC)
3. Order chapters by cognitive dependencies
4. Assign one primary cognitive load per chapter
5. Check coverage completeness

**Outputs**:

```markdown
## Target TOC

### Part X: [Part Name]

#### Chapter N: [Chapter Title]
- **Capability objective**: What the reader can do after completing this chapter
- **Prerequisite concepts**: What must be understood first
- **Primary cognitive load**: The core learning point of this chapter (only one)
- **Source coverage**:
  - [Source A] Ch[X]: [What content it contributes]
  - [Source B] Ch[Y]: [What content it contributes]
- **Methodology choice**: [Which book's teaching method is chosen and why]
- **Depth target**: [Introductory / Intermediate / Advanced]
```

### Work Item 3: Per-Chapter Integration Plans [Sub-phase 1.4]

Write a detailed integration plan for each target chapter, output to `plan.md`. This is the execution guide for Phase 2.

**Each chapter's integration plan must be self-contained** — Phase 2 execution should not require re-reading other files (except to look up specific chapters in the knowledge indexes as needed).

```markdown
## Chapter N Integration Plan

### Basic Information
- Chapter title:
- Capability objective:
- Prerequisite concepts (referencing preceding chapters):
- Estimated output length:
- Estimated code examples:

### Source Mapping
| Source | Chapter | Role | Contributed Content | Usage Method |
|--------|---------|------|---------------------|--------------|
| [Source A] | Ch[X] | Main narrative | [Core narrative framework] | Take its teaching path and analogies |
| [Source B] | Ch[Y] | Reinforcement | [In-depth content] | Supplement principles and boundary conditions |
| [Source C] | Ch[Z] | Reference | [Practical advice] | Convert into "common pitfalls" paragraphs |

### Methodology Choice
- Introduction style: [Choice] — Rationale: [Based on what evidence in the knowledge indexes]
- Teaching strategy: [Choice] — Rationale: [...]
- Cognitive progression path: [X -> Y -> Z] — Rationale: [...]

### Depth Alignment Strategy
- Target depth: [Level]
- [Source A] content needs: [Maintain / Deepen / Simplify]
- [Source B] content needs: [Maintain / Deepen / Simplify]
- Gap content: [What needs to be newly written]

### Content Synthesis Plan
Section by section:

#### [N.1 Section Title]
- Narrative source: [Primarily from which part of which book]
- Supplementary content: [What to supplement from other books]
- New content: [What needs to be written from scratch]
- Code examples: [Which example to use, from where, whether modification is needed]
- Integration level: [L3 Reorganization / L4 Full Fusion]

#### [N.2 Section Title]
...

### Concept Bridging
- Transition from the previous chapter: [How to bridge from the preceding chapter]
- Internal bridging concepts: [Whether bridging content is needed between sections]
- Setup for the next chapter: [How this chapter's ending creates a cognitive need for the next chapter]

### Terminology Conventions
| English | Unified Translation | First Appears In |
|---------|-------------------|-----------------|
| ... | ... | Chapter N / Chapter M |

### Style Baseline Example
[Quote 1-2 paragraphs from the primary book as a style reference]

### Quality Expectations
- Knowledge points covered: [N]
- Code examples: [N]
- Estimated word count: [N]
- Integration markers: [Estimated N `<!-- integrated -->` markers]
```

## Outputs: source-architecture.md [Sub-phase 1.6]

Must contain the following sections:

1. **Target audience and use cases**: Existing foundation, reading purpose, work application method, and explicitly stated out-of-scope areas.
2. **Per-book portraits**: A portrait of each source book based on the knowledge indexes (role, strengths, limitations, recommended integration strategy).
3. **Cross-book comparative analysis summary**: Core methodology differences, depth alignment scheme, boundary complementarity, style resolution.
4. **Unified knowledge graph**: Topic nodes, prerequisite dependencies, downstream capabilities, difficulty levels, practical outputs.
5. **Target TOC design**: Parts, chapters, capability objective per chapter, prerequisite concepts, source coverage.
6. **Reverse coverage matrix** [Sub-phase 1.5]: Source book chapters/topics mapped to target chapters/sidebars/appendix/exclusion rationale.
7. **Exclusion and demotion scope**: Content not entering the main narrative, reasons, and whether placed in appendix or future roadmap.
8. **Skeleton self-check**: Coverage, dependencies, granularity, project thread, advanced thread, style unification risks.

## Source Book Portrait Dimensions (Based on Knowledge Indexes)

| Dimension | Check Source |
|---|---|
| Learning path | Knowledge index -> Overall teaching philosophy -> Cognitive progression strategy |
| Conceptual depth | Knowledge index -> Per-chapter depth calibration -> Depth level |
| Modernity | Knowledge index -> Meta-information -> Language/framework version |
| Engineering orientation | Knowledge index -> Per-chapter content coverage -> Engineering practice coverage |
| Code density | Knowledge index -> Per-chapter code example inventory |
| Specialized value | Knowledge index -> Per-chapter unique insights |
| Exclusion risk | Knowledge index -> Per-chapter depth calibration -> Boundaries |
| Integration fitness | Knowledge index -> Integration readiness summary |

## Target TOC Self-Check [Sub-phase 1.3]

```
[ ] Does each chapter have only one primary cognitive load?
[ ] Does each chapter have clearly defined prerequisite concepts and output capabilities?
[ ] Has every core topic from the source books been accounted for: main narrative / sidebar / appendix / excluded?
[ ] Are advanced topics avoided before foundational models are established?
[ ] Is there a running project thread to help readers combine knowledge?
[ ] Is engineering practice placed where it is usable, rather than relegated to a final appendix?
[ ] Is there a record of why a particular source book's original TOC was not adopted?
[ ] Are outline drafts, short lecture notes, or sample chapters never marked as completed manuscripts?
[ ] Is every chapter integration plan self-contained?
[ ] Does every chapter integration plan have evidence-supported methodology choices?
[ ] Have all cross-book methodology differences been analyzed with integration choices made?
```

## Common Failure Modes

| Failure Mode | Symptom | Fix |
|---|---|---|
| Largest-book bias | Default to the largest/most authoritative source book as the skeleton | Conduct cross-book comparative analysis first; let the target audience match decide |
| Coverage illusion | Only check that target knowledge points are mapped; fail to check whether source book chapters are missed | Add a reverse coverage matrix |
| Coarse granularity | One chapter crams in multiple core models | Split chapters by cognitive load |
| Missing project thread | Every chapter is concepts; readers do not know how to combine them | Design stage projects and capstone projects |
| Premature completion | An outline or short lecture notes reported as a finished book | Explicitly mark as architecture draft; forbid "completed" |
| Specialized topic pollution | Performance, concurrency, or framework details interrupt the foundational path too early | Separate into core path, support path, and advanced path |
| Hollow integration plan | Plan only says "integrate X into Y" without methodology | Every integration decision must be supported by knowledge index evidence |
| Missing style resolution | Style differences between source books are ignored | Style conflict resolution analysis must be completed |
