---
name: review-tech-book
description: "Review technical books for quality. Trigger: review book, 审阅这本书, optimize issues, 修复这些问题. Default: report only, do not fix."
---

# Review Tech Book

Structured quality review of technical books. Default: report only. Fix mode: only when user explicitly requests.

## Workflow

```
Phase 1: Scan → Phase 2: Read → Phase 3: Score → Phase 4: Report → [Fix Mode]
```

**Phase lock**: Run `python ../shared/workflow.py review-tech-book <run_dir> check_gate <phase>` before entering any phase. If gate fails, fix and retry.

## Phase 1: Scan

**Auto-load**: `references/spec.md`, `references/execution-guardrails.md`

**Do**:
1. Batch scan: structure, logic, code density, terminology, translation artifacts
2. Define target reader
3. Draw learning path map
4. Run: `scripts/validate_code.sh output/`

**Output**: `findings/phase1.md`

**Gate** (auto-check):
```bash
python ../shared/workflow.py review-tech-book <run_dir> check_gate 1
```
- Target reader defined
- Learning path drawn
- Anomalies listed with types
- Validation summary recorded
- Issues categorized

## Phase 2: Read

**Auto-load**: `references/reviewer-discipline.md`

**Pass 1: Skim all chapters** (no skipping)
- Check: factual claims, terminology, teaching flow, formatting
- Mark: 🔴 (needs deep dive) or minor issues
- Evidence per chapter: paragraph count + core content + 3+ terms

**Pass 2: Deep dive**
- Flagged: 🔴 chapters from Pass 1
- Mandatory: first, last, code-heavy, core concept chapters

**Finding format** (strict):
```
### [N]. [Chapter] [Title] [🔴/🟠/🟡]
- **Location**: `ChX line NNN-NNN`
- **Quote**: [original text]
- **Issue**: [specific analysis]
- **Evidence**: [V1/V2/V3/V4]
- **Impact**: [reader effect]
- **Fix**: [specific method]
```

**No quote = invalid. Do not write.**

**Output**: `findings/phase2.md`

**Gate** (auto-check):
```bash
python ../shared/workflow.py review-tech-book <run_dir> check_gate 2
```
- All chapters skimmed
- Deep-dives have quotes
- 🔴/🟠 = at least V2
- >=2 chapters code-verified

## Phase 3: Score

**Auto-load**: `references/excellence-dimensions.md`

**Do**:
1. Score risk dimensions (evidence-based only)
2. Score five conversion dimensions
3. Mark cross-chapter anti-patterns

**Output**: `findings/phase3.md`

## Phase 4: Report

**Auto-load**: `../shared/report-templates.md`

**Do**: Write report with:
- Executive summary
- Score overview
- Top 3 strengths, top 3 issues
- Learning path + breakpoints
- Issue categorization
- Systemic issues
- Fix batches: P0 (errors), P1 (structure), P2 (style), P3 (references)

**Auto-check scripts**:
```bash
# Technical accuracy validation
python ../shared/validate_tech.py output/

# Terminology consistency validation
python ../shared/validate_terms.py output/

# Workflow gate
python ../shared/workflow.py review-tech-book <run_dir> check_gate 4
```

**Self-audit** (appendix):
- [ ] Factual assertions: quotes + evidence level
- [ ] No micro-fix patterns
- [ ] 🔴 severity calibrated
- [ ] Scope matches mode
- [ ] Categorization correct

**Output**: `report.md`

**Gate** (auto-check):
```bash
python ../shared/workflow.py review-tech-book <run_dir> check_gate 4
```
- All required sections present
- Findings have quotes
- Scores have evidence

## Fix Mode (user requests)

**Auto-load**: `references/apply-fixes.md`

**Do**:
1. Load latest `report.md`
2. Extract P0→P3 batches
3. Apply P0 → validate → P1 → validate → P2 → validate → P3 → validate
4. Per batch: run `validate_code.sh`, check HTML, navigation, numbering

**Output**: `fix-report.md`

**Gate** (auto-check):
```bash
python ../shared/workflow.py review-tech-book <run_dir> check_gate fix
```
- All 4 batches completed
- Each batch validated

## Quality Standards

- Conclusions based on evidence, not intuition
- Systemic issues, not scattershot lists
- Fix mode: validate HTML, nav, numbering, code after each batch
