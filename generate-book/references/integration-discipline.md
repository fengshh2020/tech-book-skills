# Integration Discipline

> Rules for correctness, completeness, style consistency.

## Correctness

### Verification Levels

| Level | Meaning | Method | Tag |
|-------|---------|--------|-----|
| V1 | Runtime verified | Ran code, called `hasattr()` | `[V1]` |
| V2 | Source confirmed | Read source file lines | `[V2]` |
| V3 | Docs checked | Read PEP/What's New | `[V3]` |
| V4 | Inferred | General knowledge, unverified | `[V4]` |

**Rules**:
- Critical/High severity = at least V2
- API existence/removal = V1 or V3
- V4 = severity auto-downgraded, mark "unverified"
- New code blocks in integration = V2 or V1, never V4

### Code Verification (3 steps)

1. **Block review**: Check imports, API names, parameter signatures
2. **Runtime**: Run code blocks with version-specific APIs
3. **Version**: Confirm version-specific APIs match baseline

### Common Traps

| Trap | Prevention |
|------|------------|
| API hallucination | V1 runtime check |
| Version timeline error | V3 check What's New |
| Import path error | V1 runtime check |
| Parameter drift | V1 or V3 verify |

## Completeness

### Coverage Check (Phase 1)

| Chapter | Keywords | Extracted | Status |
|---------|----------|-----------|--------|
| Ch1 | ... | N | Pass/Warning/Fail |

**Standard**: >=80% per source, all core topics covered, proportional to length.

### Mapping Check (Phase 2)

- **Forward**: Every KB ID mapped to a chapter?
- **Reverse**: Every chapter checked against all sources?
- **Gaps**: Every gap has decision (add/exclude/deferred)?

### Output Check (Phase 4)

- Every "insert" action executed?
- Every sidebar added?
- Every mapped KB item appears in output?
- Conflicts resolved?
- Gaps addressed?

## Style Consistency

### Baseline Extraction

| Dimension | What to Extract |
|-----------|----------------|
| Person | "we" / "you" / none |
| Sentence length | Average characters |
| Code comment language | EN / mixed |
| Term introduction | EN only / EN+CN |
| Code block size | Average lines |
| Sidebar density | Per 1000 lines |
| Explanation depth | Concept -> principle -> example -> pitfall -> best practice |
| Tone | Formal / casual / conversational |

### Source Adaptation

| Source Type | Typical Bias | Adaptation |
|-------------|-------------|------------|
| Deep textbook | Long, detailed | Keep depth, trim wording |
| Advice book | Itemized, no context | Add motivation, merge related |
| Beginner book | Shallow, simple | Deepen, upgrade examples |
| Reference docs | Dry, authoritative | Add analogy, practice guidance |

**Rule**: New content adapts to main book style. Main book doesn't adapt to new content.

### Per-Paragraph Self-Check

After writing each paragraph from non-main source:
- [ ] Person matches baseline?
- [ ] Sentence length within +/-30%?
- [ ] Term introduction follows convention?
- [ ] Code block size matches baseline?
- [ ] Context transition added?
- [ ] Tone matches baseline?

Fix before writing next paragraph. Don't fix after.

## Phase Gates

### Phase 1 Gate

```
[ ] Coverage >=80% per source?
[ ] Every chapter has >=1 item?
[ ] All core topics covered?
[ ] Item format uniform?
[ ] Dependencies annotated?
```

### Phase 2 Gate

```
[ ] Forward mapping >=95%?
[ ] Reverse mapping complete?
[ ] Unmapped items reviewed?
[ ] All gaps have decision?
[ ] Conflicts identified?
```

### Phase 3 Gate

```
[ ] Global constraints complete?
[ ] Per-chapter instruction: state/source/content/terms/estimate?
[ ] Estimate reasonable (15-35% increment)?
[ ] No vague instructions?
```

### Phase 4 Gate (per chapter)

```
[ ] Code blocks reviewed, >=2 run?
[ ] Version APIs match baseline?
[ ] Every plan action executed?
[ ] All KB items in output?
[ ] Markers present?
[ ] Style adapted?
[ ] Terms consistent?
[ ] No duplicate explanations?
```

### Full Book Gate

```
[ ] Terms consistent (grep full book)?
[ ] Cross-references valid?
[ ] Code listings renumbered?
[ ] No duplicate concepts?
[ ] Learning objectives updated?
[ ] All chapter gates passed?
```

## Coverage Guardian

### Per-Source Coverage Ratio

Per-chapter rule: If a source book is mapped as "primary" or "secondary" for a chapter, it MUST contribute >=3 integration markers in that chapter.

Per-book rule: Each source book's total markers >= (total_source_chapters * 0.5).
- Example: Will has 30 chapters -> minimum 15 markers
- Example: Mindset has 15 chapters -> minimum 8 markers

Floor rule: No source book may have fewer than 10% of total markers across the integrated book.
- If total markers = 700, minimum per source = 70.

### Patch-Style Detection

A source is "patch-style" if ANY of these is true:
1. All its markers appear in <=2 chapters (concentrated, not integrated)
2. Its markers never appear as the first marker in any section (always supplemental)
3. Its content always appears after the primary source content within every section

Detection timing:
- After each chapter gate (sub-phase 2.3)
- After batch check (sub-phase 2.5)
- During Phase 3 validation

Escalation:
- First detection: WARNING logged to progress.md
- Second detection for same source: REQUIRE REWRITE of affected chapters

### Output Size Guard

Per-chapter rule: Output chapter size MUST be >= max(source_chapter_sizes_for_this_topic) * 0.8

This prevents the "integrated book has less content than a single source book" problem.
- Example: If Will Ch8 = 50KB and Stroustrup Ch7 = 40KB cover the same topic, the integrated chapter must be >= 40KB (50KB * 0.8).
