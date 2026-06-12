# Reviewer Discipline

> Rules for review quality.

## Top 3 Rules

1. **Every finding needs original quote**: No quote = invalid.
2. **Severity needs evidence**: 🔴/🟠 = at least V2. API claims = V1 or V3.
3. **Report, don't fix**: Route to original skill. Fix only on explicit request.

## Finding Format

```
### [N]. [Chapter] [Title] [🔴/🟠/🟡]

- **Location**: `ChX line NNN-NNN`
- **Quote**: [original text]
- **Issue**: [specific analysis]
- **Evidence**: [V1/V2/V3/V4]
- **Impact**: [reader effect]
- **Fix**: [specific method]
```

## Anti-Patterns

| Pattern | Prevention |
|---------|-----------|
| Content filling | Must have original quote |
| False correction | Version claims need V1/V3 |
| Source confusion | Label [original]/[translator]/[reviewer] |
| Scope inflation | Only describe what evidence supports |
| Skip verification | Run ≥2 chapter code examples |
| Micro-fix loop | Batch by category, not one-by-one |
| Overreach fix | Report only, fix on explicit request |

## Phase Gates

### Phase 2 Gate

```
□ All chapters skimmed?
□ Deep-dive findings have quotes?
□ 🔴/🟠 = at least V2?
□ API claims = V1 or V3?
□ ≥2 chapters code-verified?
□ Deep-dives cover flagged + mandatory chapters?
```

### Self-Audit (report appendix)

```
□ Factual assertions: quotes + evidence level?
□ No micro-fix patterns?
□ 🔴 severity calibrated?
□ Scope matches mode?
□ Categorization correct?
```
