---
name: research
description: "Investigate a question against high-trust sources and return a structured finding block with cited evidence. Use when any skill or conversation needs verified facts, API details, library behavior, comparative data, or external context — triggers: research, look up, find out, investigate, verify, check docs, what does X do, how does X work, 调研, 查一下, 查文档, 验证. Do NOT trigger for: code review, book generation, or questions answerable from files already in context."
---

# Research — Cited Finding Block

Investigate a question, return a **single structured finding block** with cited evidence. One adaptive loop; depth scales with budget, not with explicit tiers.

**Evidence levels (V1–V4) and writing discipline** — see `../shared/writing-core.md`. This skill does not redefine them.

## Depth control

This skill uses one adaptive loop — **Plan → Search → Read → Synthesize** — that deepens naturally with the question. There are no fixed tiers; depth scales by iterating the loop.

**When to deepen** (run another iteration):
- First pass returned 0 relevant results → reformulate query
- Sources contradict each other → find a tiebreaker source
- Answer is partial → narrow the gap with a targeted query
- Only Tier 3 sources found → try to reach Tier 1–2
- User explicitly asks for more thorough investigation

**When to stop**:
- 2+ independent Tier 1–2 sources agree, no contradiction
- Budget met (planned number of sources checked)
- Further searching is unlikely to change the conclusion
- The gap is structural (the information simply doesn't exist publicly) — flag it and stop

**Hard limit**: 3 iterations. After 3 passes with unresolved axes, produce the finding block with `escalated: yes` and honest Gaps — a partial answer with cited evidence is more useful than no answer or a fabricated one.

**Optional shortcut**: if `ulw-research` is available (OhMyOpenCode runtime) and the question has 3+ orthogonal axes, you may delegate to it for saturation coverage. This is a convenience, not a requirement — research handles any question independently.

## Flow

**Plan → Search → Read → Synthesize**. Iterate when the first pass is insufficient (see Depth control above).

**① Plan** — Decompose the question into 1–3 concrete search queries. Identify the best source territory (official docs / source code / web / academic). Set a budget: how many sources justify stopping? Write the plan as a one-line note to yourself.

**② Search** — Execute the planned queries. Use the right tool per territory:
- Official docs → Context7 or direct fetch
- Source code → codegraph / grep / LSP
- Web → websearch / webfetch
- Library examples → librarian agent (background) or grep.app
Search craft details → `references/search-craft.md`.

**③ Read** — Actually read the top results; snippets lie. For each relevant source, capture: exact claim, source URL/path, evidence level (V1–V4). If two sources contradict, note both and flag the conflict.

**④ Synthesize** — Write the **finding block**. If the first pass left critical gaps, iterate: reformulate queries, try a different source territory, or narrow scope. Apply the depth control rules above.

**⑤ Deliver** — Produce the finding block. If critical gaps remain after exhausting iterations, deliver it with `escalated: yes` and honest Gaps rather than fabricating or withholding.

## Finding Block (output contract)

Every research call produces exactly this block — as a file for standalone use, or inline for skill-to-skill calls.

```markdown
## Findings: {question}

### Answer
{1–3 sentence direct answer. If no definitive answer, say so.}

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

**Confidence heuristic**: `high` = 2+ independent sources agree, no contradiction · `medium` = 1 strong source or sources partially agree · `low` = only indirect evidence, unresolved contradictions, or V4-heavy.

Full output contract and composability protocol → `references/output-contract.md`.

## Composability: calling research from another skill

When a parent skill needs research mid-flow, the agent:

1. Reads this SKILL.md (or the parent skill's `references/research.md` pointer).
2. Follows the flow above using its available tools.
3. Produces the finding block **inline** — the block becomes part of the parent skill's working context.
4. Continues the parent skill's flow with the findings integrated.

No separate skill invocation is needed. The research protocol is instructions, not a runtime call.

## Rules

- **Cite every claim.** No claim without a source or a V-level tag.
- **Don't fabricate.** If a source doesn't say what you need, flag it as a gap.
- **Don't over-research.** Stop when the answer is clear. More sources ≠ better if they repeat the same claim.
- **Don't under-research.** A single secondary blog post is not sufficient for a `high` confidence answer.
- **Flag V4.** Inferred claims are `[V4 推断]` — never present them as confirmed findings.

## Reference files (load on demand)

| File | When to read |
|---|---|
| `references/search-craft.md` | Need query decomposition, source quality heuristics, or iteration strategy |
| `references/output-contract.md` | Need composability protocol, confidence calibration, or embedding rules |
| `../shared/writing-core.md` | Need evidence level definitions, iron law, or failure modes |
