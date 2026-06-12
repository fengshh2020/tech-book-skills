# Content Synthesis Methodology

> For use by the generate-book skill. Defines how to synthesize knowledge points from different sources into coherent, excellent teaching content in Phase 4 — rather than simple knowledge stacking.
> SKILL.md Phase 4 references this file.

---

## 1. Core Problem: Knowledge Stacking vs Teaching Narrative

The most common mistake in multi-book integration: arranging knowledge points in order, adding transition sentences, and calling it done. The result is a book that is "factually correct but reads like an encyclopedia" — every knowledge point is covered, but the reader cannot form a coherent mental model.

**Bad structure** (Knowledge Stacking):

```
Ch10 Generators and Coroutines
├── 10.1 Generator Basics
├── 10.2 yield Semantics
├── 10.3 Generator Expressions
├── 10.4 itertools Module
├── 10.5 Coroutine Intro          ← Sudden jump to a new topic, no motivation
├── 10.6 yield from
├── 10.7 async/await              ← Another sudden jump
```

**Good structure** (Teaching Narrative):

```
Ch10 Generators and Coroutines
├── 10.1 Problem Introduction: Why "Lazy Evaluation" Is Needed
│     (Scenario: a 10GB log file → loading it all at once will crash)
├── 10.2 Generator Basics: From Function to Producer
│     (yield turns a function into a data producer)
├── 10.3 yield Semantics: Pause and Resume
│     (A generator doesn't return a value — it pauses execution. This distinction is the key insight)
├── 10.4 Generator Expressions: Lazy List Comprehensions
│     (Return to the 10.1 problem — process the log line by line with a generator expression)
├── 10.5 Bridge: From "Data Pipeline" to "Cooperative Scheduling"
│     (yield can both produce data and receive data — this dual purpose is the transition key)
├── 10.6 Coroutines: The Other Side of yield
│     (Use yield to implement a simple producer-consumer collaboration)
├── 10.7 yield from: Delegating to Sub-Generators
│     (The pain point of nested cooperation → yield from as the solution)
├── 10.8 async/await: Modern Syntax for Coroutines
│     (The evolution from yield coroutines to async/await — why was new syntax invented?)
```

**The essence of the difference**: Knowledge Stacking is organized by "topic classification"; Teaching Narrative is organized by "problem-driven cognitive progression." Each section exists not because "this topic belongs here," but because "after understanding the previous section, the reader naturally has a question, and this section answers that question."

---

## 2. Chapter Narrative Arc Construction

### 2.1 Three-Layer Narrative Structure

Every chapter (not every section) should have a complete three-layer narrative structure:

**Layer 1: Chapter-Level Arc**

Start from the "reader's pain point," go through "concept construction," and arrive at "capability delivery."

```
Pain Point → Concept A → Concept B → Concept C → Capability Delivery
  ↑                                              ↓
  └──── Why return to the pain point? ──────────┘
         (Re-solve the opening pain point with the new capability, forming a closed loop)
```

Example (Ch10):
- Pain point: Memory overflow when processing large files
- Concept construction: Generators → yield → Coroutines → async/await
- Capability delivery: Able to write a concurrent file processor using async/await
- Closed loop: Return to the large file scenario from the beginning, but this time handle it with async I/O

**Layer 2: Inter-Section Bridging**

The end of each section should create a "cognitive need" for the next section — after reading, the reader naturally asks "but...?", and the next section answers that "but."

| Section Ending | "But" Created | Next Section Answers |
|----------------|---------------|---------------------|
| "Generators pause execution via yield" | "But can yield only produce data?" | Coroutines: the receiving side of yield |
| "yield from delegates to a sub-generator" | "But nested yield from is too complex" | The cleaner syntax of async/await |
| "Generator expressions handle large files" | "But disk I/O still blocks" | The async I/O solution |

If there is no natural "but" bridge between two adjacent sections, it means:
- The order is wrong (should be rearranged)
- Bridge content is missing (a transition paragraph should be added)
- The topic doesn't belong in the same chapter (should be moved out)

**Layer 3: In-Paragraph Logic**

Each paragraph follows a "claim → evidence → significance" structure:
- Claim: Start with a declarative sentence ("A generator doesn't return a value — it pauses execution")
- Evidence: Prove it with a code example or reasoning
- Significance: Explain what this means for the reader ("This means you can use generators to process arbitrarily large data streams")

Do not start paragraphs with "Next, let's look at X" — that is a hallmark of Knowledge Stacking. Start with a declarative sentence or a question.

### 2.2 Source-Mixed Narrative Synthesis

When a section's content comes from multiple source books, organize the narrative by the following priority:

1. **Take the framework from the primary book**: How the primary book introduces the concept, what analogy it uses, what order it follows
2. **Take practical advice from EP**: Effective Python's item-style recommendations are converted into "common pitfalls" and "best practices" paragraphs within the narrative
3. **Take simplified explanations from PP**: Python Programming's introductory-level explanations serve as "analogy supplements" or "beginner perspective" sidebars
4. **Take precision from official documentation**: API signatures, parameter descriptions, version differences

**Specific procedure**: Do not write the primary book content first and then paste EP recommendations. Instead:
1. First write the primary book's narrative framework (introduction → concept → example)
2. Find the natural position in the narrative for "common misconceptions" or "this concept is easy to misuse"
3. Insert EP's advice at that position — not as "EP recommends doing this," but as "You might think you should write it this way, but actually..."
4. This way the advice is woven into the narrative, rather than appended as a footnote

### 2.3 Inserted Content Depth Calibration

Content inserted from non-primary books tends to be "shallow insertions" — only a definition and an example, without motivation, principles, or common pitfalls. Calibrate using the following checklist:

```
□ Motivation paragraph: Why should the reader learn this? (Not "because Chapter X needs it" but "because you will encounter scenario Y")
□ Definition paragraph: What is this concept? (Use an analogy from concepts the reader already knows)
□ Principle paragraph: Why does it work this way? (Not a black box — explain the underlying mechanism)
□ Example paragraph: How to use it? (At least one practical scenario, not a toy example)
□ Common pitfall paragraph: What mistake do beginners most often make? (EP's advice is usually most valuable here)
□ Best practice paragraph: How should production code be written?
```

If the inserted content only has a definition and an example, lacking motivation/principles/pitfalls/best practices, it must be supplemented. "Shallow insertions" are not allowed — either complete the teaching chain or do not insert.

---

## 3. Example Evolution Design

### 3.1 Continuous vs Standalone Examples

There are two code example strategies in technical books:

**Continuous Examples**: Gradually stack new features on the same scenario/project. The reader follows one example from start to finish, seeing how concepts combine in a real project.

**Standalone Examples**: Each concept is illustrated with its own small example. Clear but lacking a sense of integration.

**Best strategy for integrated books**: Keep the primary book's original examples standalone (do not replace verified good examples); for newly added content, prefer continuous examples — stack new knowledge points on the same scenario as the primary book's examples.

For example: If the primary book Ch5 uses a "bookstore inventory" example to teach variables and types, when Ch9 adds "dictionary comprehension" content, do not use a brand-new "student grades" example. Instead, use a dictionary comprehension version of "bookstore inventory." The reader is already familiar with the scenario, so the cognitive load is lower.

### 3.2 Example Quality Standards

Every code example must satisfy:

1. **Runnable**: Actually executed on the target version baseline
2. **Self-contained**: No external files or undefined variables needed
3. **Has output**: Include comments showing the execution result
4. **Real-world scenario**: Not a `foo = "bar"` type toy example
5. **Appropriate scale**: 3–15 lines (within the primary book's style baseline)
6. **Minimal comments**: The code itself should be clear enough; only comment when "why" is not obvious

Code examples over 20 lines require special scrutiny — can they be split into two smaller examples? If not, add intermediate "step-by-step build" stages.

---

## 4. Concept Bridging Design

### 4.1 Bridge Concept Identification

The most easily overlooked element in the integration process is "bridge concepts" — intermediate steps between two major concepts. If a bridge is missing, the reader encounters a cognitive gap.

**Identification method**: For every "insert X then insert Y" sequence in the integration instructions, ask yourself:

> "The reader just understood X. Can they directly understand Y? If not, what is missing in between?"

Common scenarios with missing bridges:

| Concept A | Concept B | Missing Bridge |
|-----------|-----------|----------------|
| Closures | Decorators | Higher-order functions / functions as parameters |
| Generators | Coroutines | The dual purpose of yield (produce + receive) |
| Class basics | Metaclasses | Descriptors / attribute access mechanism |
| Functions | Closures | LEGB scope + free variables |
| Synchronous code | async/await | Event loop + cooperative scheduling |

If a missing bridge is found, add bridge content in the integration instructions (approximately 500–1500 words + 1–2 examples). The bridge does not need to be deep; it just needs to ensure the reader does not "skip a step."

### 4.2 Cross-Chapter Back-Reference

When a chapter's content depends on concepts from earlier chapters, a back-reference must be provided. Format:

> "In Chapter 6, we saw how closures capture outer variables. Now you'll see that decorators exploit exactly this mechanism —"

Do not just write "as discussed in Chapter 6" — **remind the reader of the key point of that concept in one sentence**, so they can follow along without having to flip back.

---

## 5. Quality Perception Checklist

In Phase 4, after each chapter is completed, in addition to the technical correctness/completeness/style gates, it must also pass the following **teaching perception checks**:

### Chapter-Level Perception Check

```
□ Does the chapter opening have a clear "reader pain point" or "capability promise"?
□ Does the chapter ending have a closed loop (returning to the opening pain point, solved with the new capability)?
□ Is there a natural "but" bridge between sections? (Not "next, let's look at")
□ Are there any cognitive gaps missing a bridge? (Two adjacent sections cannot transition naturally)
□ Does every newly added section cover the complete teaching chain? (Motivation → Definition → Principle → Example → Pitfall → Best Practice)
```

### Paragraph-Level Perception Check

```
□ Do paragraphs start with a declarative sentence or a question? (Not "next" or "now")
□ Are there 3 or more consecutive paragraphs that merely state facts without explaining "why"?
□ Do examples have real-world scenarios? (Not foo/bar toy examples)
□ Is EP advice woven into the narrative? (Not appended as "EP recommends X" footnotes)
```

### Reader Experience Self-Test

Mentally simulate a target reader reading this chapter in order. At the end of each section, ask:

1. "What can I do now that I couldn't do before?"
2. "What is the next question I naturally want to ask?"
3. "Does the next section answer that question?"

If the answer to question 3 is "no," the narrative arc has a problem — the order needs to be adjusted or a bridge needs to be added.
