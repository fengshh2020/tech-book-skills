# Skill Compliance Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three-layer compliance enforcement (Iron Law + inline MUST/Evidence + What Failure Looks Like) to all three book skill SKILL.md files.

**Architecture:** Each SKILL.md gets identical Layer 1 (Iron Law) and Layer 3 (Failure modes), plus skill-specific Layer 2 (inline enforcement at phase boundaries). No new files created — all enforcement is inline text edits.

**Tech Stack:** Markdown editing only.

---

## File Structure

```
Files to modify:
├── generate-book/SKILL.md        (480 → ~620 lines) — largest, dual-mode
├── review-tech-book/SKILL.md     (154 → ~240 lines) — 4 phases + fix mode
└── codebase-book/SKILL.md        (160 → ~260 lines) — 5 phases, has existing failure section
```

---

### Task 1: Add Layer 1 (Iron Law) to generate-book/SKILL.md

**Files:**
- Modify: `generate-book/SKILL.md`

- [ ] **Step 1: Insert Iron Law block after frontmatter**

Find the line `# Generate Book` (line 6) and insert the following block **after** it, **before** the `Generate a unified technical book` paragraph:

```markdown

## ⛊ IRON LAW

**NO OUTPUT WITHOUT FRESH READ EVIDENCE. NO GATE SKIP. NO TITLE-ONLY INFERENCE. NO CONTENT SHRINKAGE.**

Violating the letter of this rule IS violating the spirit of this rule.

### Anti-Rationalization Table

| If you think... | The truth is... |
|-----------------|-----------------|
| "I remember this rule" | You don't. Re-read the file. |
| "The title tells me enough" | It doesn't. Open and read. |
| "Gate probably passes" | Run it. No probably. |
| "This is ~80% coverage" | Shrinkage = data loss. Expand. |
| "I'll fix it in Phase 3" | Fix now or rewrite later. |
| "Just this once" | "Just this once" is how it starts. |
| "The user wants speed" | The user wants quality. |
| "I already verified" | Re-verify. Fresh evidence only. |

```

- [ ] **Step 2: Verify Iron Law appears between `# Generate Book` and `## Mode Selection`**

Run: `grep -n "IRON LAW\|Mode Selection\|# Generate Book" generate-book/SKILL.md`
Expected: `# Generate Book` → `IRON LAW` → `Mode Selection` in sequential line order.

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/SKILL.md
git commit -m "feat: add Iron Law + anti-rationalization table to generate-book SKILL.md"
```

---

### Task 2: Add Layer 1 (Iron Law) to review-tech-book/SKILL.md

**Files:**
- Modify: `review-tech-book/SKILL.md`

- [ ] **Step 1: Insert Iron Law block after frontmatter**

Find the line `# Review Tech Book` (line 7) and insert the following block **after** it, **before** the `Structured quality review` paragraph:

```markdown

## ⛊ IRON LAW

**NO FINDING WITHOUT DIRECT QUOTE. NO GATE SKIP. NO SKIM-ONLY REVIEW. NO SHALLOW SCORING.**

Violating the letter of this rule IS violating the spirit of this rule.

### Anti-Rationalization Table

| If you think... | The truth is... |
|-----------------|-----------------|
| "I remember this rule" | You don't. Re-read the file. |
| "The title tells me enough" | It doesn't. Open and read the chapter. |
| "Gate probably passes" | Run it. No probably. |
| "I'll score from memory" | Score from evidence. Memory is not evidence. |
| "I'll fix it in the report" | Fix findings now. Report summarizes, doesn't create. |
| "Just this once" | "Just this once" is how it starts. |
| "The user wants speed" | The user wants thoroughness. |
| "I already verified" | Re-verify. Fresh evidence only. |

```

- [ ] **Step 2: Verify placement**

Run: `grep -n "IRON LAW\|## Workflow\|# Review Tech Book" review-tech-book/SKILL.md`
Expected: `# Review Tech Book` → `IRON LAW` → `## Workflow` in sequential order.

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add review-tech-book/SKILL.md
git commit -m "feat: add Iron Law + anti-rationalization table to review-tech-book SKILL.md"
```

---

### Task 3: Add Layer 1 (Iron Law) to codebase-book/SKILL.md

**Files:**
- Modify: `codebase-book/SKILL.md`

- [ ] **Step 1: Insert Iron Law block after frontmatter**

Find the line `# Codebase Book` (line 7) and insert the following block **after** it, **before** the `Generate a deep learning guide` paragraph:

```markdown

## ⛊ IRON LAW

**NO COVERAGE CLAIM WITHOUT FILE:LINE EVIDENCE. NO GATE SKIP. NO LISTING WITHOUT EXPLAINING. NO CONTENT SHRINKAGE.**

Violating the letter of this rule IS violating the spirit of this rule.

### Anti-Rationalization Table

| If you think... | The truth is... |
|-----------------|-----------------|
| "I remember this module" | You don't. Re-read the source. |
| "The function name tells me enough" | It doesn't. Read the body. |
| "Gate probably passes" | Run it. No probably. |
| "This is ~20KB per chapter" | Shrinkage = lost understanding. Expand. |
| "I'll add depth later" | Add depth now. Later never comes. |
| "Just this once" | "Just this once" is how it starts. |
| "The user wants speed" | The user wants mastery-level depth. |
| "I already analyzed this" | Re-analyze. Fresh evidence only. |

```

- [ ] **Step 2: Verify placement**

Run: `grep -n "IRON LAW\|## What Success\|# Codebase Book" codebase-book/SKILL.md`
Expected: `# Codebase Book` → `IRON LAW` → `## What Success` in sequential order.

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add codebase-book/SKILL.md
git commit -m "feat: add Iron Law + anti-rationalization table to codebase-book SKILL.md"
```

---

### Task 4: Add Layer 2 (inline enforcement) to generate-book/SKILL.md

**Files:**
- Modify: `generate-book/SKILL.md`

This is the largest task. The generate-book SKILL.md has 10 phases (5 single + 5 multi) plus Coverage Guardian, Anti-Slacking, Sub-Agent, and Quality Standards sections.

- [ ] **Step 1: Replace `**Auto-load**` lines with Must-Read Boxes (Single-Source Mode)**

For each phase in the Single-Source Mode section, replace the `**Auto-load**: \`references/xxx.md\`` line with:

Phase 0 — find `**Auto-load**: \`references/agent-orchestration.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/agent-orchestration.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] If unchecked: STOP. Do not proceed.
```

Phase 1 — find `**Auto-load**: \`references/translation-rules.md\`, \`shared/translationese-patterns.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/translation-rules.md` completely (no skimming)
- [ ] Read `shared/translationese-patterns.md` completely (no skimming)
- [ ] Read any existing `.book-doc/spec.md` for terminology
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 2 — find `**Auto-load**: \`references/book-assembly.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/book-assembly.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] Gate 1 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 4 — find `**Auto-load**: \`shared/report-templates.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `shared/report-templates.md` completely (no skimming)
- [ ] Gate 3 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

- [ ] **Step 2: Replace `**Auto-load**` lines with Must-Read Boxes (Multi-Source Mode)**

Phase 0 — find `**Auto-load**: \`references/knowledge-index-format.md\`, \`references/agent-orchestration.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/knowledge-index-format.md` completely (no skimming)
- [ ] Read `references/agent-orchestration.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 1 — find `**Auto-load**: \`references/book-architecture.md\`, all knowledge indexes from Phase 0` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/book-architecture.md` completely (no skimming)
- [ ] Re-read ALL knowledge indexes from Phase 0 (no "I remember")
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] Gate 0 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 2 — find `**Auto-load**: \`references/full-integration.md\`, \`references/agent-orchestration.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/full-integration.md` completely (no skimming)
- [ ] Read `references/agent-orchestration.md` completely (no skimming)
- [ ] Re-read chapter's integration plan from plan.md
- [ ] Gate 1 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 4 — find the second `**Auto-load**: \`shared/report-templates.md\`` (in multi-mode) and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Re-read `shared/report-templates.md` completely (no skimming)
- [ ] Gate 3 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

- [ ] **Step 3: Add Pre-Gate Red Flags self-checks before all gate commands**

Before every `python scripts/workflow.py generate-book <run_dir> check_gate` block, insert:

```markdown
**STOP — Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**
```

This applies to: Gate 0.3, Gate 1.5, Gate 2.4, Gate 3, Gate 4 (single mode) and Gate 0.5, Gate 1.6, Gate 2.3, Gate 2.5, Gate 3, Gate 4 (multi mode).

- [ ] **Step 4: Verify all Auto-load lines are replaced**

Run: `grep -n "Auto-load" generate-book/SKILL.md`
Expected: Zero matches.

- [ ] **Step 5: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/SKILL.md
git commit -m "feat: add inline MUST boxes, pre-gate self-checks to generate-book SKILL.md"
```

---

### Task 5: Add Layer 2 (inline enforcement) to review-tech-book/SKILL.md

**Files:**
- Modify: `review-tech-book/SKILL.md`

- [ ] **Step 1: Replace `**Auto-load**` lines with Must-Read Boxes**

Phase 1 — find `**Auto-load**: \`references/spec.md\`, \`references/execution-guardrails.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/spec.md` completely (no skimming)
- [ ] Read `references/execution-guardrails.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 2 — find `**Auto-load**: \`references/reviewer-discipline.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/reviewer-discipline.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] Gate 1 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 3 — find `**Auto-load**: \`references/excellence-dimensions.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/excellence-dimensions.md` completely (no skimming)
- [ ] Gate 2 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 4 — find `**Auto-load**: \`../shared/report-templates.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `shared/report-templates.md` completely (no skimming)
- [ ] Gate 3 complete with scored dimensions
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Fix Mode — find `**Auto-load**: \`references/apply-fixes.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING FIX MODE:**
- [ ] Read `references/apply-fixes.md` completely (no skimming)
- [ ] Gate 4 passed (report completed)
- [ ] User explicitly requested fix mode
- [ ] If ANY unchecked: STOP. Do not proceed.
```

- [ ] **Step 2: Add Pre-Gate Red Flags before all gate commands**

Before each `python ../shared/workflow.py review-tech-book <run_dir> check_gate` block, insert:

```markdown
**STOP — Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Any finding lacks a direct quote from the source
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**
```

This applies to: Gate 1, Gate 2, Gate 4, Gate fix.

- [ ] **Step 3: Add evidence template after Phase 2 reading step**

After the `**Pass 1: Skim all chapters**` block, add:

```markdown

**Evidence required per chapter** (write to findings/phase2.md):
```
### [ChN] Skim Evidence
- Paragraphs: [count]
- Code blocks: [count]
- Key terms: [≥3 specific terms from actual content, NOT from title]
- Flags: [🔴 issues found or "clean"]
```
```

- [ ] **Step 4: Verify no Auto-load lines remain**

Run: `grep -n "Auto-load" review-tech-book/SKILL.md`
Expected: Zero matches.

- [ ] **Step 5: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add review-tech-book/SKILL.md
git commit -m "feat: add inline MUST boxes, pre-gate self-checks, evidence templates to review-tech-book SKILL.md"
```

---

### Task 6: Add Layer 2 (inline enforcement) to codebase-book/SKILL.md

**Files:**
- Modify: `codebase-book/SKILL.md`

- [ ] **Step 1: Replace `**Read**:` lines with Must-Read Boxes**

Phase 2 — find `**Read**: \`references/analysis-guide.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/analysis-guide.md` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] Gate 1 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 3 — find `**Read**: \`references/writing-and-content.md\`, \`references/writing-guide.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `references/writing-and-content.md` completely (no skimming)
- [ ] Read `references/writing-guide.md` completely (no skimming)
- [ ] Gate 2 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 4 — find the first `**Read**: \`references/writing-and-content.md\`, \`references/writing-guide.md\`` (in Phase 4) and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Re-read `references/writing-and-content.md` completely (no "I remember")
- [ ] Re-read `references/writing-guide.md` completely (no "I remember")
- [ ] Gate 3 passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

Phase 5 — find `**Read**: \`../shared/report-templates.md\`` and replace with:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `shared/report-templates.md` completely (no skimming)
- [ ] All chapters generated with `<!-- generated: complete -->` marker
- [ ] If ANY unchecked: STOP. Do not proceed.
```

- [ ] **Step 2: Add Pre-Gate Red Flags before all gate checks**

Before each `**Gate (must pass)**:` block, insert:

```markdown
**STOP — Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I analyzed" claim lacks file:line evidence
- [ ] Any module analyzed by name only (no source code read)
- [ ] Gate check was not actually run (just claimed)

**If ANY checked: Fix before running gate.**
```

This applies to: Phase 1 gate, Phase 2 gate, Phase 3 gate.

- [ ] **Step 3: Add evidence template after Phase 2 analysis**

After the `**What to do** (per core module):` block's bullet list, add:

```markdown

**Evidence required per module** (write to analysis/{module}.md):
```
### [Module] Analysis Evidence
- Source files read: [list with line counts]
- Functions analyzed: [count, with file:line references]
- Design decisions: [count, each with "why" documented]
- Key terms: [≥3 specific implementation details, NOT generic descriptions]
```
```

- [ ] **Step 4: Verify no plain `**Read**:` lines remain (except in Phase 4 `**Read**:`) **

Run: `grep -n "^\*\*Read\*\*:" codebase-book/SKILL.md`
Expected: Zero matches (all replaced with Must-Read Boxes).

- [ ] **Step 5: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add codebase-book/SKILL.md
git commit -m "feat: add inline MUST boxes, pre-gate self-checks, evidence templates to codebase-book SKILL.md"
```

---

### Task 7: Add Layer 3 (What Failure Looks Like) to generate-book/SKILL.md

**Files:**
- Modify: `generate-book/SKILL.md`

- [ ] **Step 1: Insert What Failure Looks Like section before `## Reference Files`**

Find the `## Reference Files` section and insert the following block **before** it:

```markdown
## What Failure Looks Like

### Failure 1: Re-read skip
- **Model says**: "I already loaded the translation rules earlier" / "I remember the integration plan"
- **Reality**: Context was summarized, rules are now fuzzy, plan details forgotten
- **Detection**: Read confirmation missing from progress.md for this phase
- **Fix**: Re-read file, record confirmation with structure evidence (line count, key rules)

### Failure 2: Title-only inference
- **Model says**: "Chapter 5 covers functions, so it includes parameters, return types, overloading"
- **Reality**: Chapter 5 is about function objects and lambdas, not basic functions
- **Detection**: Evidence uses generic terms applicable to any chapter on "functions"
- **Fix**: Open file, read full content, re-record evidence with specific terms from actual text

### Failure 3: Gate bypass
- **Model says**: "Gate passes — all checks look good" / "Coverage is sufficient"
- **Reality**: Gate script was never actually run; coverage was estimated, not measured
- **Detection**: No script output pasted in progress.md; no marker counts
- **Fix**: Run gate command, paste full output, verify pass with evidence

### Failure 4: Content shrinkage
- **Model says**: "Chapter generated successfully"
- **Reality**: Source chapter had 40 paragraphs, output has 15 (37% coverage) — content was summarized, not translated/integrated
- **Detection**: Output file < 80% of source chapter size; paragraph count mismatch
- **Fix**: Expand output to match source depth. Add missing sections. Re-run gate.

### Failure 5: Patch-style integration (multi-mode only)
- **Model says**: "All sources integrated"
- **Reality**: One source contributes 80% of markers, others only appear in 1-2 chapters
- **Detection**: Coverage Guardian shows floor rule violation; per-chapter minimum not met
- **Fix**: Expand contributions from underrepresented sources in affected chapters

```

- [ ] **Step 2: Verify section appears before Reference Files**

Run: `grep -n "What Failure Looks Like\|## Reference Files" generate-book/SKILL.md`
Expected: `What Failure Looks Like` appears before `## Reference Files`.

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add generate-book/SKILL.md
git commit -m "feat: add What Failure Looks Like section to generate-book SKILL.md"
```

---

### Task 8: Add Layer 3 (What Failure Looks Like) to review-tech-book/SKILL.md

**Files:**
- Modify: `review-tech-book/SKILL.md`

- [ ] **Step 1: Insert What Failure Looks Like section before `## Quality Standards`**

Find `## Quality Standards` and insert the following block **before** it:

```markdown
## What Failure Looks Like

### Failure 1: Re-read skip
- **Model says**: "I already loaded the spec earlier" / "I know the reviewer discipline rules"
- **Reality**: Context was summarized, specific scoring criteria forgotten
- **Detection**: Read confirmation missing from progress.md for this phase
- **Fix**: Re-read reference file, record confirmation with structure evidence

### Failure 2: Skim-only review (title inference variant)
- **Model says**: "I reviewed all chapters" but findings use generic descriptions
- **Reality**: Chapters were scanned for structure only, not read for content
- **Detection**: Findings lack direct quotes; evidence level V1 for 🔴/🟠 issues
- **Fix**: Re-read flagged chapters, add direct quotes with line references

### Failure 3: Gate bypass
- **Model says**: "Gate passes — all chapters reviewed"
- **Reality**: Chapters were listed, not actually read; findings are fabricated summaries
- **Detection**: No chapter evidence in findings/phase2.md; no quotes for deep-dives
- **Fix**: Re-read chapters, document with paragraph counts + terms + quotes

### Failure 4: Shallow scoring
- **Model says**: "All dimensions scored"
- **Reality**: Scores are rounded estimates without evidence, or all dimensions scored 7/10
- **Detection**: No quotes supporting scores; uniform scoring across all dimensions
- **Fix**: Re-score each dimension with specific evidence: quote + issue + impact

```

- [ ] **Step 2: Verify section placement**

Run: `grep -n "What Failure Looks Like\|## Quality Standards" review-tech-book/SKILL.md`
Expected: `What Failure Looks Like` appears before `## Quality Standards`.

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add review-tech-book/SKILL.md
git commit -m "feat: add What Failure Looks Like section to review-tech-book SKILL.md"
```

---

### Task 9: Extend Layer 3 in codebase-book/SKILL.md

**Files:**
- Modify: `codebase-book/SKILL.md`

codebase-book already has a `## What Failure Looks Like` section with 5 mistakes (Listing functions, Shallow coverage, No source evidence, Skipping error paths, Repetition). We extend it with 4 compliance-specific failures.

- [ ] **Step 1: Add 4 compliance failures after existing Mistake 5**

Find the end of Mistake 5 (the line `- **Mistake 5: Repetition**` block ending with `Fix: Explain once, cross-reference afterwards`) and append:

```markdown

**Mistake 6: Re-read skip**
- **Model behavior**: "I already analyzed this module in Phase 2"
- **Result**: Stale analysis, missing code changes, wrong design decisions
- **Fix**: Re-read source files before writing. Record evidence with line counts.

**Mistake 7: Name-only analysis (title inference variant)**
- **Model behavior**: "Function `processData` processes data" (reads name, not body)
- **Result**: Misses error handling, side effects, algorithm complexity, actual logic
- **Fix**: Read function body. Document what it ACTUALLY does, not what the name says.

**Mistake 8: Gate bypass**
- **Model behavior**: "Gate passes — all modules covered"
- **Result**: Core modules analyzed by name only; no file:line evidence
- **Fix**: Run gate check. Paste output. Verify every core module has analysis file.

**Mistake 9: Content shrinkage**
- **Model behavior**: "Chapter generated" (5KB for what should be 20KB core chapter)
- **Result**: Reader sees superficial overview, cannot trace behavior to source
- **Fix**: Check output size against minimums (core ≥ 20KB). Expand shallow sections.
```

- [ ] **Step 2: Add Pre-Gate Red Flags section before `## Quality Standards`**

Find `## Quality Standards` and insert **before** it:

```markdown
## Pre-Chapter Red Flags

**Before marking any chapter complete, verify NONE of these:**
- [ ] Source files were analyzed by name only (no code body read)
- [ ] No file:line references in the chapter
- [ ] Chapter size below minimum (core < 20KB, overview < 10KB)
- [ ] Code:explanation ratio below 1:1
- [ ] Error paths not covered for core modules
- [ ] Design decisions stated without alternatives/trade-offs

**If ANY checked: Expand chapter before proceeding.**

```

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add codebase-book/SKILL.md
git commit -m "feat: extend What Failure Looks Like + add pre-chapter red flags to codebase-book SKILL.md"
```

---

### Task 10: Final verification

- [ ] **Step 1: Verify all Auto-load lines are gone from all three files**

```bash
cd /home/hsf/projects/others/tech_book_skills
grep -rn "Auto-load\|^\*\*Read\*\*:" generate-book/SKILL.md review-tech-book/SKILL.md codebase-book/SKILL.md
```

Expected: Zero matches.

- [ ] **Step 2: Verify Iron Law in all three files**

```bash
cd /home/hsf/projects/others/tech_book_skills
grep -c "IRON LAW" generate-book/SKILL.md review-tech-book/SKILL.md codebase-book/SKILL.md
```

Expected: `1` for each file.

- [ ] **Step 3: Verify What Failure Looks Like in all three files**

```bash
cd /home/hsf/projects/others/tech_book_skills
grep -c "What Failure Looks Like" generate-book/SKILL.md review-tech-book/SKILL.md codebase-book/SKILL.md
```

Expected: `1` for each file.

- [ ] **Step 4: Verify Pre-Gate self-checks exist in all three files**

```bash
cd /home/hsf/projects/others/tech_book_skills
grep -c "STOP — Before running gate" generate-book/SKILL.md review-tech-book/SKILL.md codebase-book/SKILL.md
```

Expected: ≥2 for each file (multiple gates per skill).

- [ ] **Step 5: Verify Must-Read boxes in all three files**

```bash
cd /home/hsf/projects/others/tech_book_skills
grep -c "MANDATORY BEFORE STARTING" generate-book/SKILL.md review-tech-book/SKILL.md codebase-book/SKILL.md
```

Expected: ≥3 for each file (multiple phases per skill).

- [ ] **Step 6: Final commit if any fixes needed**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add -A
git diff --cached --stat
git commit -m "fix: final compliance enforcement cleanup" 2>/dev/null || echo "No changes needed"
```
