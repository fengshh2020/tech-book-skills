# Deep Knowledge Index Format

> For generate-book multi-mode Phase 0. Each source book generates a knowledge index of >=1000 lines.
> Goal: Enable the LLM in subsequent phases to understand "how to integrate" — not just "what was covered," but "how it was taught," "why it was taught this way," and "where the boundaries lie."

## Why This Depth Is Needed

The current "5-15 items/chapter, 200-word summary" extraction approach has three fatal flaws:

1. **Information Loss**: Summaries compress away methodological differences. Both Book A and Book B cover "decorators," but A introduces them via the "function wrapping" metaphor while B uses the "middleware pattern." The summary only records "covers decorators," leaving the model unable to decide which introduction approach to use.
2. **Context Break**: Summaries do not record inter-chapter cognitive progression relationships. The model sees isolated knowledge points and cannot reconstruct the original book's teaching path.
3. **Depth Blind Spot**: Summaries do not calibrate depth boundaries. The model does not know how deeply a given book covers a particular topic before stopping, nor what the book assumes the reader already knows.

**Solution**: Generate a deep knowledge index for each book, covering 9 dimensions. The granularity of the index must be sufficient for the model to answer questions like "what are the methodological differences between these two books on the same topic?"

## Index File Structure

```
.book-doc/knowledge_base/
├── {source-book-name}/
│   └── index.md          # Deep knowledge index for this source book (>=1000 lines)
├── cross-book-analysis.md # Phase 1 output: cross-book comparative analysis
└── INDEX/
    └── source_coverage.md # Coverage statistics for each source book
```

## Index File Format

```markdown
# [Source Book Name] Deep Knowledge Index

## Metadata
- Book Title:
- Author:
- Target Audience:
- Prerequisite Knowledge Assumptions:
- Primary Programming Language/Framework Version:
- Total Chapter Count:
- Total Code Examples (estimated):

---

## Teaching Philosophy

### Core Teaching Method
[What is this book's teaching approach? Is it "problem-driven," "concept-first," "example-led," or "project-throughout"? Describe in 2-3 sentences.]

### Cognitive Progression Strategy
[How does this book organize the reader's learning path? Is it "simple to complex," "low-level to high-level," "practical to theoretical," or a mixed strategy?]

### Narrative Style Baseline
- Narrative Person:
- Sentence Length:
- Code Comment Language:
- Terminology Introduction Style (English+Chinese / Chinese only):
- Tone (formal / casual / conversational):
- Average Code Block Length (lines):
- Sidebar Density (one every N lines):

### Overall Assessment (Integration Perspective)
- What role should this book play in integration (main thread / reinforcement / specialized / reference)?
- Core Strengths:
- Core Limitations:
- Complementary Points with Other Source Books:

---

## Per-Chapter Deep Analysis

### Chapter 1: [Chapter Title]

#### Content Coverage
- Core Topics: [What core concepts are covered in this section, listed in order of appearance]
- Topic Weight: [Which are key topics, which are briefly mentioned]
- Coverage Scope: [Which aspects of the topic are covered, which are not]
- Paragraph Structure: [N paragraphs + M code blocks + K figures/sidebars]

#### Methodology Analysis
- Introduction Approach: [How does this section introduce core concepts? Via problem / scenario / definition / analogy?]
- Teaching Strategy: [Concept → Principle → Example → Exercise? Or another sequence?]
- Cognitive Progression: [How do concepts progress from simple to complex within this section?]
- Unique Methods: [Does this section use any distinctive teaching techniques? E.g., showing a wrong example first then correcting it?]

#### Depth Calibration
- Depth Level: [Introductory / Intermediate / Advanced / Expert]
- Explanation Depth: [API usage only? Or principles, implementation details, boundary conditions?]
- Assumes Reader Already Knows: [What does this section assume the reader has already mastered?]
- Not Covered in This Section: [What does this section explicitly exclude? Left for later chapters?]
- Depth Boundary: [At what point does it stop going deeper? Why?]

#### Unique Insights
- Insights Unique to This Section: [Observations unlikely to appear in other books]
- Unique Analogies/Metaphors: [Distinctive analogies used in this section]
- Unique Examples: [Example scenarios in this section not found in other books]
- Common Misconception Corrections: [Common reader misunderstandings pointed out in this section]

#### Code Example Inventory
| Example | Lines | Scenario | Runnability | Teaching Purpose |
|---------|-------|----------|-------------|------------------|
| [Example 1 description] | [N] | [Real-world / Toy] | [Yes / No / Needs Modification] | [Introduce concept / Demonstrate usage / Show pitfall] |

#### Cross-References
- Depends on Prior Chapters: [Which earlier chapters does this section reference?]
- Referenced by Later Chapters: [Which later chapters will use this section's content?]
- External References: [What external resources does this section cite (docs, PEPs, papers)?]

#### Style Characteristics
- Narrative Density: [High (dense concepts) / Medium / Low (heavy on examples and explanations)]
- Code Density: [High (code in every segment) / Medium / Low (primarily text explanations)]
- Exercises: [Present / Absent, quantity]
- Sidebars/Tip Boxes: [Present / Absent, content types]

#### Integration Readiness
- Recommended Integration Role: [Main content / Supplementary content / Sidebar content / Reference material]
- Integration Considerations: [What needs special attention during integration? Style differences? Terminology conflicts?]
- Direct Reusability: [High (can be quoted directly) / Medium (needs rewriting) / Low (needs reorganization)]

---

[Repeat the above structure for each chapter's deep analysis]

---

## Cross-Chapter Theme Mapping

### Progression Path for Theme [A]
- Chapter X: [Basic introduction]
- Chapter Y: [In-depth expansion]
- Chapter Z: [Advanced application / practical use]
- Progression Pattern: [How concepts deepen from Chapter X to Y to Z]

### Progression Path for Theme [B]
...

### Running Project
[If the book has a project that spans multiple chapters, describe its evolution path]

---

## Knowledge Point Cross-Reference Matrix

| Knowledge Point | Chapter | Depth | Prerequisites | Uniqueness Rating |
|-----------------|---------|-------|---------------|-------------------|
| [Concept 1] | Ch[1] | [Introductory / Intermediate / Advanced] | [None / Ch0] | [High / Medium / Low] |
| [Concept 2] | Ch[3] | [Intermediate] | [Concept 1] | [Medium] |
...

---

## Integration Readiness Summary

### What This Book Can Contribute to the Integration
[3-5 sentences summarizing this book's core value in the integration]

### Style Adaptation Needs
[If this book serves as the main thread, what style adaptations do other books need? If this book is in a supplementary role, what style adaptations does it need?]

### Known Risks
[Potential problems during integration: terminology conflicts, depth mismatches, methodological conflicts, etc.]

### Recommended Integration Strategy
[Suggested approach for using this book's content: which chapters to use as the main thread, which as supplements, which to skip]
```

## Line Count Estimation

Per-chapter deep analysis is approximately 60-100 lines. A 15-chapter book = 900-1500 lines of chapter analysis + 100 lines of overall analysis + 50 lines of cross-chapter mapping + 50 lines of cross-reference matrix = **1100-1700 lines**. Meets the >=1000 line requirement.

## Quality Standards

How to verify whether the index is sufficiently deep:

```
□ Can it answer "What are the methodological differences between these two books on [topic]?"
□ Can it answer "How deeply does this book cover [topic] before stopping?"
□ Can it answer "What is the unique value of this book's treatment of [topic]?"
□ Can it answer "How are [Concept A] and [Concept B] connected in this book?"
□ Can it answer "What does this book assume the reader already knows before learning [topic]?"

If any of the above questions cannot be answered from the index, the index is not deep enough.
```

## Reading Evidence Requirements

The "Content Coverage" section of each chapter must include:
- Exact paragraph count (not "approximately N paragraphs" but a precise count)
- Exact code block count
- At least 3 specific technical terms that appear in the chapter (not rewordings of the chapter title)

**Prohibited**:
- Inferring content from titles alone
- Having identical reading evidence formats for two consecutive chapters
- "This chapter mainly covers X" style title rewording
