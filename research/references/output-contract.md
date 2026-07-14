# Output Contract

Structured finding block specification, confidence calibration, and composability protocol for the research skill.

## Finding Block Specification

Every research call produces exactly one finding block. The block is valid Markdown, usable as a standalone file or embedded inline.

### Required fields

```markdown
## Findings: {question}

### Answer
{1–3 sentence direct answer. Present tense. If no definitive answer exists, state that.}

### Evidence
- {claim}: {source URL or file:line} [V{1–4}]
- {claim}: {source} [V{level}]

### Gaps
- {what could not be answered, and why}

### Meta
- sources-checked: {N}
- confidence: {high | medium | low}
- escalated: {no | yes — reason}
```

### Field rules

**Answer**: Lead with the conclusion. No preamble ("After researching…"). If the answer is "we don't know", say that directly and explain what's missing.

**Evidence**: Each entry is one claim with one source and one evidence level. Format: `- claim text: source [Vlevel]`. Evidence levels follow `../shared/writing-core.md` — V1 (实机) / V2 (源文件) / V3 (文档) / V4 (推断). V4 claims must be labeled `[V4 推断]` and never presented as confirmed.

**Gaps**: What the research could not resolve. Be specific: "Could not verify whether X supports Y in version Z — changelog does not mention it and no test was found" is useful. "More research needed" is not.

**Meta**:
- `sources-checked`: total number of distinct sources examined (including ones that didn't make it into Evidence).
- `confidence`: see calibration below.
- `escalated`: `no` if the finding block is the final output. `yes — reason` if critical gaps remain after exhausting iterations — the reason should state what's unresolved (e.g., "3 orthogonal axes only partially covered"). An escalated block is still a valid deliverable — it carries honest partial answers with cited evidence.

### Optional fields (add when relevant)

```markdown
### Contradictions
- Source A says X; Source B says Y. Resolution: {explanation or "unresolved"}.

### Recommendations
- {actionable next step derived from findings}

### Related Questions
- {question that surfaced during research but was out of scope}
```

## Confidence Calibration

| Level | Criteria | Implication |
|---|---|---|
| **high** | 2+ independent Tier 1–2 sources agree; no contradiction; at least one V1–V3 source | Safe to act on. Can be cited as fact in downstream work. |
| **medium** | 1 strong source, OR sources partially agree, OR only Tier 2 sources | Usable with caveats. Flag in downstream work as "medium confidence — verify if critical". |
| **low** | Only indirect evidence; unresolved contradictions; V4-heavy; only Tier 3 sources | Do not act on without verification. Flag for manual verification or further investigation. |

**Adjustment rules**:
- Single source, no matter how authoritative, caps at `medium` unless corroborated by a second independent source.
- A contradiction between two Tier 1 sources caps at `medium` until resolved.
- All V4 evidence → `low` by definition.
- If a parent skill requires `high` confidence and the block is `medium` or `low`, the parent skill should treat this as a gap and seek additional verification.

## Composability Protocol

### How other skills use research findings

The research skill is invoked **by instruction**, not by runtime API. When a parent skill needs research:

1. **Parent skill references the research protocol.** Two patterns:
   - **Inline**: The parent skill's SKILL.md contains a `## Research` section that paraphrases the flow (Plan → Search → Read → Synthesize) and specifies the output format as the finding block.
   - **Pointer**: The parent skill's `references/` directory contains a file that says "For research, follow the protocol at `../research/SKILL.md` and produce the finding block defined in `../research/references/output-contract.md`."

2. **Agent executes the research flow** using its currently available tools. No skill switch or context swap is needed — the agent just follows the instructions.

3. **Finding block is produced inline** in the parent skill's working context. The parent skill continues its flow with the findings integrated.

4. **If the agent determines the question has unresolved gaps after exhausting iterations**, it produces the finding block with `escalated: yes — reason` and the parent skill decides whether to proceed with partial information or seek further verification.

### Embedding rules

- **Standalone use**: Write the finding block to a file (e.g., `{RUN}/research-{topic}.md`). Include the full block plus a one-line header with the date.
- **Inline use in parent skill**: Produce the block directly in the conversation context. The parent skill reads it and continues.
- **In generate-book**: Research findings become source material. The finding block's Evidence section provides `file:line` or URL citations that the book can reference. The Meta section tells the book author whether to treat the finding as confirmed or tentative.
- **In take-note**: Research findings become note content. The finding block maps directly to a note: Answer → `[!important]` callout, Evidence → body with V-level tags, Gaps → `[!caution]` callout.

### Idempotency

Re-running research on the same question should produce a finding block with the same scope and confidence level. The exact sources may differ (web content changes), but the answer should be stable if the underlying facts haven't changed. If facts have changed (e.g., a new version was released), the new finding block should note this in Gaps.
