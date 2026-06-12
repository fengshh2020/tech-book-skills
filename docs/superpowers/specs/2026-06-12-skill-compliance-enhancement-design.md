# Skill Compliance Enhancement Design

Date: 2026-06-12

## Problem

All three book generation skills (generate-book, review-tech-book, codebase-book) suffer from four model compliance failures:

1. **Re-read skip**: Model claims "I remember" instead of re-reading reference files
2. **Gate bypass/fabrication**: Model claims gates pass without running scripts, or fabricates evidence
3. **Title-only inference**: Model infers chapter content from titles instead of reading
4. **Content shrinkage**: Model produces output < 80% of source, losing content

Research across 33 SKILL.md files identified the most effective compliance patterns from TDD, verification-before-completion, systematic-debugging, and codebase-book skills.

## Design: Three-Layer Compliance Enhancement

Apply to all three skills: generate-book, review-tech-book, codebase-book.

### Layer 1: Iron Law + Anti-Rationalization Table

**Position**: Immediately after frontmatter, before any other content.

**Content** (identical structure across all three skills, with skill-specific wording):

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
| "I'll fix it in [later phase]" | Fix now or rewrite later. |
| "Just this once" | "Just this once" is how it starts. |
| "The user wants speed" | The user wants quality. |
| "I already verified" | Re-verify. Fresh evidence only. |
```

**Rationale**: TDD skill's Iron Law + Spirit/Letter Preemption is the single most effective compliance pattern observed. It sets absolute standards before exceptions can be argued.

### Layer 2: Inline MUST/Evidence at Key Points

Embed three types of compliance enforcement directly into each phase's steps:

#### 2a: Phase-Start Must-Read Box

**Position**: At the start of every phase, replacing the current `**Auto-load**` line.

**Content**:
```markdown
**⚠️ MANDATORY BEFORE STARTING THIS PHASE:**
- [ ] Read `[reference_file]` completely (no skimming)
- [ ] Record read confirmation in progress.md with structure evidence
- [ ] Previous gate passed with evidence in progress.md
- [ ] If ANY unchecked: STOP. Do not proceed.
```

**Changes from current**: Current SKILL.md has `**Auto-load**: references/xxx.md` which is passive. The new box is active — it creates a checklist that MUST be checked off.

#### 2b: Evidence Output Template

**Position**: After every step that produces output (reading, writing, generating).

**Content**:
```markdown
**Evidence required** (write to progress.md):
```
### [Phase.Sub] [Description] Evidence
- Files read: [list with line counts]
- Structure: [paragraphs: N, code blocks: N, images: N]
- Key terms: [≥3 specific terms from content, NOT from title]
- Read timestamp: [YYYY-MM-DD HH:MM]
```
```

**Changes from current**: Current SKILL.md mentions evidence but buries it in prose. New format is a copy-paste template that makes compliance mechanically easy.

#### 2c: Pre-Gate Red Flags Self-Check

**Position**: Immediately before every gate command.

**Content**:
```markdown
**STOP — Before running gate, verify NONE of these are true:**
- [ ] Any reference file was not re-read this phase
- [ ] Any "I read" claim lacks structure evidence
- [ ] Any chapter has identical evidence format as previous
- [ ] Output size < 80% of source for any chapter
- [ ] Gate check was not actually run (just claimed)
- [ ] Evidence was fabricated (e.g., paragraph count from title, not actual reading)

**If ANY checked: Fix before running gate. Gate will fail.**
```

**Changes from current**: Current gates only have the command and pass criteria. New self-check forces the model to audit its own work before the gate can be run.

### Layer 3: What Failure Looks Like

**Position**: New section at the end of each SKILL.md, before Reference Files table.

**Content** (four failure modes, adapted per skill):

```markdown
## What Failure Looks Like

### Failure 1: Re-read skip
- **Model says**: "I already loaded [file] earlier"
- **Reality**: Context was summarized, content is now fuzzy
- **Detection**: Read confirmation missing from progress.md for this phase
- **Fix**: Re-read file, record confirmation with evidence

### Failure 2: Title-only inference
- **Model says**: "Chapter [N] covers [topic], so it includes [list from title]"
- **Reality**: The chapter covers different aspects than title suggests
- **Detection**: Evidence uses generic terms applicable to any chapter on that topic
- **Fix**: Open file, read content, re-record evidence with specific terms

### Failure 3: Gate bypass
- **Model says**: "Gate passes — all checks look good"
- **Reality**: Gate script was never actually run
- **Detection**: No script output in progress.md
- **Fix**: Run gate command, paste output, verify pass

### Failure 4: Content shrinkage
- **Model says**: "Chapter generated successfully"
- **Reality**: Source had [X] content units, output has [Y] where Y < 80% of X
- **Detection**: Output size check fails; paragraph count mismatch
- **Fix**: Expand output to match source depth, add missing content
```

**Rationale**: codebase-book's "What Failure Looks Like" section is highly effective because it makes failure modes concrete and detectable before they happen.

## Per-Skill Adaptation

### generate-book (480 lines → ~580 lines)

**Layer 1**: Iron Law tailored to "no integration without reading all sources"
**Layer 2**: Applied to all 5 phases × 2 modes (single + multi), prioritizing Phase 0 (reading) and Phase 2 (generation) where failures are most common
**Layer 3**: Four failures as described above

Key additions:
- Phase 0 gets extra emphasis: "THIS PHASE IS THE FOUNDATION" already exists, but now has must-read box before it
- Phase 2 gets evidence template after every chapter generation
- Coverage Guardian section gets inline red-flags before each guardian check

### review-tech-book

**Layer 1**: Iron Law tailored to "no review finding without direct quote"
**Layer 2**: Applied to reading phase (skim + deep), finding documentation, and report writing
**Layer 3**: Four failures adapted: re-read → re-read chapter, title inference → skim-only review, gate bypass → scoring without evidence, shrinkage → shallow review

### codebase-book

**Layer 1**: Iron Law tailored to "no coverage claim without file:line evidence"
**Layer 2**: Applied to codebase exploration, chapter writing, and output validation
**Layer 3**: Already has partial "What Failure Looks Like" — extend with the four standardized failures

## Files to Modify

1. `generate-book/SKILL.md` — Add all three layers
2. `review-tech-book/SKILL.md` — Add all three layers
3. `codebase-book/SKILL.md` — Add all three layers (extend existing failure section)

## What NOT to Change

- `shared/anti-slacking.md` — already covers the philosophy; SKILL.md layers provide the execution mechanism
- Phase structure, gate commands, sub-phase numbering — all unchanged
- Reference files — unchanged (they're the targets of re-read requirements, not the enforcement mechanism)

## Expected Impact

| Pain Point | Layer Addressing | Mechanism |
|-----------|------------------|-----------|
| Re-read skip | Layer 1 (Iron Law) + Layer 2a (Must-Read Box) | Psychological + structural |
| Gate bypass | Layer 2c (Pre-Gate Self-Check) + Layer 3 (Failure Case) | Structural + behavioral |
| Title inference | Layer 2b (Evidence Template) + Layer 3 (Failure Case) | Structural + behavioral |
| Content shrinkage | Layer 2c (Red Flags) + Coverage Guardian | Structural + quantitative |

## Success Criteria

- All three SKILL.md files updated with three-layer compliance enhancement
- No increase in reference file count (all enforcement is inline)
- Iron Law + Anti-Rationalization Table at the top of each file
- Must-Read Boxes at every phase start
- Evidence Templates after every output step
- Pre-Gate Self-Checks before every gate
- What Failure Looks Like section at the end of each file
