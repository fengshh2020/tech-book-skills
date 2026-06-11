# Full Integration Guide

> How to fully integrate vs patchwork.

## Integration Levels

| Level | Name | Action | Acceptable? |
|-------|------|--------|-------------|
| L1 | Direct insert | Paste source content as-is | ❌ |
| L2 | Style adapt | Rewrite wording, keep structure | ❌ |
| L3 | Reorganize | Redesign structure, rewrite content | ✅ |
| L4 | Full fusion | Redesign from all sources, unrecognizable origin | ✅ |

**Requirement**: Phase 4 output must be L3 or L4.

## 5-Step Rewrite

1. **Deconstruct all sources**: Open every source's relevant chapter. Extract concepts, sequence, examples, analogies.
2. **Design new structure**: Don't use any source's original TOC. Organize by reader cognition.
3. **Assign primary/secondary**: Each section has one primary source for narrative, others for depth.
4. **Rewrite in main style**: Match baseline (person, sentence length, terminology, tone).
5. **Verify unidentifiable**: Random 3 paragraphs test — can reader tell source?

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| "I rewrote wording" | Structure unchanged, reader notices | Reorganize structure |
| "I added after main" | Clear seam between main and source | Interleave content |
| "I grouped all sources" | Style switches within each topic | One primary per section |

## Quality Test

After each chapter:

```
□ Random 3 paragraphs: can tell source? (no = pass)
□ Terminology consistent?
□ Narrative flow natural?
□ Depth consistent?
□ Example follows same storyline?
```

Record in progress.md:
```
### ChN Source Test
- Sample paragraphs: 3
- Identifiable: X/3 (target: ≤1/3)
- Terms: pass/fail
- Flow: pass/fail
- Depth: pass/fail
- Result: pass/rewrite
```
