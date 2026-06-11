# Quality Gate

> Chapter-level quality gates. Each chapter must pass before the next one starts.
> Core principle of Phase 2: resolve quality issues on the spot; do not accumulate them to the end.

## Purpose

Prevent "reviewed 30 rounds, still problems". Catch issues during generation, not after. Every chapter passes its gate BEFORE the next chapter starts.

## Phase 0 Gate: Knowledge Indexing

```
□ Every source book has an index.md file?
□ Every index.md >= 1000 lines?
□ Every index.md contains all required sections? (Teaching Philosophy, Per-Chapter Deep Analysis, Cross-Chapter Theme Mapping, Integration Readiness Summary)
□ Every chapter has reading evidence? (paragraph count, code block count, specific terminology)
□ No two consecutive chapters have identical reading evidence format?
□ No content inferred from titles alone? (every topic has specific supporting evidence)
```

**Fail = re-read and supplement the index. Do not enter Phase 1.**

## Phase 1 Gate: Architecture Design

```
□ source-architecture.md contains all required sections?
□ Cross-book comparison analysis complete? (methodology differences, depth alignment, boundary complementarity, style harmonization)
□ Each chapter in target TOC has only one primary cognitive load?
□ Source book reverse coverage matrix is 100%?
□ Each chapter in plan.md has a self-contained integration plan?
□ Each integration plan has: source mapping, methodology selection (with evidence), depth alignment, content synthesis approach?
□ No TBD / placeholders?
□ Target TOC self-check all passed?
```

**Fail = redesign. Do not enter Phase 2.**

## Phase 2 Gate: Chapter Generation (per chapter)

### Per Chapter (2a) — after each chapter

| ID | Check | Pass Criteria | Fail Action |
|----|-------|--------------|-------------|
| G1 | Coverage | All plan.md IDs have markers | Rewrite chapter |
| G2 | Code quality | New code has V1-V3 tags | Add tags + verify |
| G3 | Style match | No translationese, matches baseline | Rewrite sections |
| G4 | No duplicates | No repeated explanations | Merge/cross-ref |
| G5 | Narrative flow | Transitions natural, arc complete | Rewrite |
| G6 | Depth match | Matches plan's depth target, sufficient length | Expand or trim |
| G7 | Source ratio | Each mapped source has >=3 markers in this chapter | Expand source contribution |
| G8 | Output size | Chapter size >= max(source_chapter_sizes) * 0.8 | Expand content |

### Per Batch (2b) — every 5 chapters

| ID | Check | Pass Criteria | Fail Action |
|----|-------|--------------|-------------|
| G9 | Cross-chapter consistency | Terms consistent, style uniform | Fix batch |
| G10 | Source unidentifiable | 3 random paragraphs, can't tell source | Rewrite |

### Full Book (2c) — after all chapters

| ID | Check | Pass Criteria | Fail Action |
|----|-------|--------------|-------------|
| G11 | Global consistency | Full book term/style/flow check | Fix |
| G12 | Coverage complete | 100% source material accounted for | Add missing |
| G13 | Resample check | Re-check 3 chapters against G1-G8 | Rewrite if fail |

## Record Format

```markdown
### Ch[N] Gate
- Time: YYYY-MM-DD HH:MM
- G1: pass/fail — [markers count]
- G2: pass/fail — [verified/total code blocks]
- G3: pass/fail — [translationese hits]
- G4: pass/fail — [duplicate count]
- G5: pass/fail — [notes]
- G6: pass/fail — [line count, depth assessment]
- G7: pass/fail — [markers per source, lowest count]
- G8: pass/fail — [chapter size vs max(source_chapter_sizes)]
- Issues: [list]
- Action: proceed/rewrite
```

## Phase 3 Gate: Validation

```
□ Coverage >= 95%?
□ All terms consistent across full book?
□ All code blocks runnable?
□ All cross-references valid?
□ No style jumps between chapters?
□ Reverse coverage 100%?
```

## Core Rule

**Fail = rewrite. Do not proceed to next chapter. Do not accumulate.**

If 2 consecutive chapters fail the same gate item, stop and check whether plan.md has a problem.
