---
name: codebase-book
description: "Generate project mastery guide from codebase. Trigger: 生成项目书籍, codebase walkthrough, 掌握项目, 架构学习指南. Do NOT trigger for: code review, README, API reference."
---

# Codebase Book

Generate a deep learning guide from a codebase. Focus: design decisions, code understanding, algorithms, knowledge points.

## What Success Looks Like

A reader finishing the book can trace every key behavior to its source location, understand why the design choice was made, and master all background knowledge needed.

## What Failure Looks Like (Common Model Mistakes)

**Mistake 1: Listing functions**
- Model behavior: "Function A does X, Function B does Y"
- Result: Reader sees isolated facts, no understanding
- Fix: Follow execution paths, tell a coherent story

**Mistake 2: Shallow coverage**
- Model behavior: "15 chapters covering everything"
- Result: Each topic gets 1 paragraph, reader learns nothing
- Fix: Depth over breadth. 5 thorough chapters > 15 shallow ones.

**Mistake 3: No source evidence**
- Model behavior: "This function handles errors"
- Result: Reader cannot verify, cannot trace
- Fix: Every claim needs file path + line number

**Mistake 4: Skipping error paths**
- Model behavior: "The happy path works like this"
- Result: Reader crashes on first exception
- Fix: Cover error handling, boundary conditions

**Mistake 5: Repetition**
- Model behavior: "This pattern appears in 5 places, I'll explain it 5 times"
- Result: Reader reads the same thing 5 times
- Fix: Explain once, cross-reference afterwards

## Phase Flow (Mandatory Sequence)

```
Phase 1: Discover → Phase 2: Analyze → Phase 3: Plan → Phase 4: Generate → Phase 5: Validate
```

**Critical rule**: You cannot enter Phase N until Phase N-1 is complete with evidence.

## Phase 1: Discover

**What to do**:
1. Identify source files, tests, configs, resources
2. Determine languages, frameworks, dependencies, build commands, entry points
3. Classify each file: core path (deep) / support path (summary) / reference (confirm)
4. Identify natural execution paths: input → modules → output

**Output**: `{RUN}/codebase-map.md`

**Gate (must pass)**:
- [ ] Every relevant file classified or excluded with reason

**If gate fails**: Re-classify. Do not enter Phase 2.

## Phase 2: Analyze

**Read**: `references/analysis-guide.md`

**What to do** (per core module):
- **Interface & behavior**: public API, parameter semantics, core logic, data/control flow
- **Design decisions**: why this data structure/algorithm/pattern? alternatives? trade-offs?
- **Key algorithms**: core idea, complexity, parameter effects
- **Error handling**: exception paths, degradation, boundary conditions
- **Implicit knowledge**: what reader needs to know (language features, framework mechanisms, algorithm theory)
- **Position in execution path**: where this module sits in global chain

**Output**: `{RUN}/analysis/{module}.md`

**Gate (must pass)**:
- [ ] Core modules covered for interface, design, algorithm, implicit knowledge

**If gate fails**: Add missing analysis. Do not enter Phase 3.

## Phase 3: Plan

**Read**: `references/writing-and-content.md`, `references/writing-guide.md`

**What to do**:
1. Define target audience and prerequisites
2. Chapter list ordered by content logic (not directory tree)
3. Per chapter: core content, covered source files, knowledge expansion points, deferred scope

**Planning principles**:
- Structure serves content logic
- Each pattern explained once, rest cross-referenced
- Each chapter has clear focus
- No forced components unless natural

**Output**: `{RUN}/chapter-plan.md`

**Gate (must pass)**:
- [ ] Core execution paths have no gaps
- [ ] Repeated mechanisms have first detailed + subsequent referenced

**If gate fails**: Revise plan. Do not enter Phase 4.

## Phase 4: Generate

**Read**: `references/writing-and-content.md`, `references/writing-guide.md`

Copy `assets/style.css` and `assets/script.js` to `output/`.

**Per chapter**:
1. First line: `<!-- generated: complete -->`
2. Code excerpts: copy from source, annotate file path + line range
3. **Narrative-driven**: follow execution path or design thread
4. **Diagrams first**: complex flows → `{RUN}/diagram-specs/*.json` → `output/diagrams/*.drawio`
5. Core functions: show code + explain logic + analyze design
6. Design decisions: what, why, alternatives, trade-offs
7. Key algorithms: core idea, data structures, parameter effects
8. Knowledge expansion: sidebar (not in code walkthrough)
9. No `[待确认]` in final HTML

**Content depth**:
- Core chapters ≥ 20KB, overview ≥ 10KB
- Core path: every function has code + explanation
- Core path: every parameter explained
- Error paths covered
- Code:explanation ratio ≥ 1:1

**Parallel writing** (chapters > 5):
- Batch by 2-3 chapters
- Each writer prompt: full source + chapter plan + HTML template + cross-reference info
- Cover, TOC, CSS/JS by main agent before parallel

## Phase 5: Validate

Run: `scripts/validate_output.sh output/`

**Auto-check scripts**:
```bash
# Technical accuracy validation
python ../shared/validate_tech.py output/

# Terminology consistency validation
python ../shared/validate_terms.py output/
```

**Read**: `../shared/report-templates.md`

Write `{RUN}/report.md`. Mark `progress.md` as completed.

## Quality Standards

- Reader understands design decisions and trade-offs
- Reader can trace every key behavior to source location
- Reader masters all background knowledge (language, framework, algorithm)
- Depth: not "this function does X" but "why this way, alternatives, parameter effects"
- No repetition: one detailed explanation, rest cross-referenced
- Structure follows content logic, not template filling
