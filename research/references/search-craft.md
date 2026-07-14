# Search Craft

Query decomposition, source quality heuristics, and iteration strategy for the research skill.

## Query Decomposition

Break the question into 1–3 concrete search queries before executing any. Each query should target a different source territory or angle.

**Decomposition patterns:**

| Question shape | Decompose into |
|---|---|
| "Does X support Y?" | ① official docs for X's Y feature · ② real-world examples of X+Y · ③ known limitations of X+Y |
| "What's the difference between X and Y?" | ① X official docs on the relevant dimension · ② Y official docs on the same · ③ comparison articles or migration guides |
| "How does X work internally?" | ① X source code (codegraph/grep) · ② X architecture docs · ③ X author's talks/blog posts |
| "Is X available in version V?" | ① X changelog/release notes for V · ② X API docs pinned to V · ③ GitHub issues/commits around V |
| "What's the best practice for X?" | ① official X docs/guides · ② high-signal community sources (StackOverflow top answer, core contributor blog) · ③ counter-examples (what NOT to do) |

**Rule**: Never run the same query twice. If the first query returns nothing, reformulate — change keywords, add operators, or switch source territory.

## Source Quality Heuristics

Not all sources are equal. Apply authority-aware ranking:

**Tier 1 — Primary sources** (always prefer):
- Official documentation (docs.python.org, docs.rs, kubernetes.io/docs)
- Source code (file:line references)
- Specification / RFC / PEP / W3C standard
- First-party changelog / release notes
- Vendor knowledge base (AWS docs, Azure docs)

**Tier 2 — High-signal secondary** (useful, verify against Tier 1):
- Core contributor blog posts / talks
- StackOverflow answers with 50+ upvotes
- GitHub issues/PRs with maintainer response
- Academic papers (arXiv, peer-reviewed)
- Established tech publications (InfoQ, The New Stack)

**Tier 3 — Low-signal secondary** (use only when Tier 1–2 absent):
- Random blog posts / tutorials
- Reddit/HN comments (may contain expert insight, but unvetted)
- AI-generated content (treat as V4 — unverified inference)

**Rule**: A `high` confidence answer requires at least one Tier 1 source. A `medium` answer with only Tier 2–3 sources should flag this in Gaps.

## Search Tool Selection

| Source territory | Primary tool | Fallback |
|---|---|---|
| Official docs | Context7 (`context7_resolve-library-id` → `context7_query-docs`) | Direct fetch of docs site |
| Source code (local) | codegraph_explore / codegraph_node | grep / LSP |
| Source code (remote) | librarian agent (background) | grep.app / `gh search code` |
| Web (general) | websearch | webfetch on top result |
| Web (specific page) | webfetch | librarian agent |
| Library examples | grep.app (search code patterns) | librarian agent |
| Academic | websearch with `site:arxiv.org` or `filetype:pdf` | — |

**Parallelism**: When 2+ queries target different territories, fire them in parallel. When they target the same territory, run sequentially (results from query 1 may refine query 2).

## Iteration Strategy

The research loop is **Plan → Search → Read → Synthesize**, with iteration when the first pass is insufficient.

**When to iterate** (one more pass):
- First pass returned 0 relevant results → reformulate query
- Sources contradict each other → find a tiebreaker source
- Answer is partial → narrow the gap with a targeted query
- Only Tier 3 sources found → try to reach Tier 1–2

**When to stop** (do not iterate further):
- Budget met (planned number of sources checked)
- 2+ independent Tier 1–2 sources agree
- Further searching is unlikely to change the conclusion
- The gap is structural (the information simply doesn't exist publicly) — flag it and stop

**Hard limit**: 3 iterations. After 3 passes with unresolved gaps, produce the finding block with `escalated: yes` and honest Gaps. A partial answer with cited evidence beats no answer or a fabricated one.

**Deepening tactics** (when a second or third pass is needed):
- **Switch source territory**: if web search was unproductive, try source code or official docs (or vice versa)
- **Reformulate with operators**: add `site:`, `filetype:`, `"exact"`, or `after:` to narrow
- **Chase references**: if a source cites another source, follow that citation
- **Decompose the gap**: if "does X support Y?" is unresolved, try "X Y integration" and "X Y limitation" as separate queries
- **Seek contradiction**: if all sources agree but confidence is still low, actively search for counter-evidence (`X problem OR issue OR limitation`)

## Search Operators (web)

Vary operators on every query — same query twice wastes a pass:

| Operator | Example | Use |
|---|---|---|
| `site:` | `site:docs.python.org asyncio` | Restrict to a domain |
| `filetype:` | `filetype:pdf kubernetes scheduling` | Papers, specs |
| `intitle:` | `intitle:benchmark LLM inference` | Targeted pages |
| `"exact"` | `"context window" management` | Precision match |
| `-term` | `python asyncio -tutorial` | Exclude noise |
| `OR` | `fastapi OR starlette middleware` | Coverage |
| `after:` | `rust async after:2025-01-01` | Recency control |

**High-yield combos**: official docs (`site:<docs-domain>`), GitHub (`site:github.com`), recent discussion (`site:reddit.com OR site:news.ycombinator.com after:<date>`), changelog hunting (`changelog OR "release notes" <version>`).
