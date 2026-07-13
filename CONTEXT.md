# Tech Book Skills

三个 AI 技能（generate-book / review-tech-book / shared）把技术源材料变成一本可读的技术书，并审阅它。本上下文界定这些技能的领域语言。

## Language

**Book Artifact（书籍产物）**:
生成出来的那本技术书。它有同一份内容、两种渲染形态。
_Avoid_: 文档、输出（太泛）。

**HTML Edition（HTML 版）**:
书籍产物的交互式渲染，建立在"静奢"设计系统上（`style.css` + `script.js`，**light-only**（已去暗色，ADR-0003）/玻璃拟态/自适应层级/约 30 种组件）。由 [Builder](#) 从 MD 源渲染生成（ADR-0001）。
_Avoid_: 网页版、site。

**Markdown Edition（MD 版）**:
书籍产物的可移植渲染，**通用/GitHub 方言**（无 frontmatter、无双链、无 callout）。靠结构而非视觉样式传达。2026-07-13 决议：与 HTML 版并存（"同时支持"），不是替代。MD 是**信息主源**，HTML 由 builder 从它渲染（ADR-0001）。
_Avoid_: Obsidian 版（明确不选）。

**Builder**:
新增的构建器（`scripts/build_html.py`）。读 MD 章节 + `book.yml` 元数据 → 渲染 HTML 输出目录（含精简版 style.css/script.js）。承担 ADR-0002 的"务实子集"组件映射（标签化引用块→sidebar、图+图注→figure 等）。封面/目录/导航等 chrome 由它注入，不由 agent 写。
_Avoid_: 渲染器、generator。

**Source（源）/ Mode（模式）**:
输入材料及其决定的工作流。单源 = 一本书（翻译+组装）；多源 = 多本书（深度整合）；代码库 = 源码路径（发现+分析+生成）。
_Avoid_: input（太泛）。

**Diagram（图表）**:
agent 在 MD 中写 ` ```mermaid ` 文本，构建期 mermaid-cli (mmdc) 渲染为**仅 PNG**（ADR-0004）。MD 版 `![x](diagrams/x.png)`，HTML 版同嵌 PNG。证据（file:line）写在图注里。
_Avoid_: drawio spec、`.drawio`（已废弃）。

**Gate（关卡）**:
阶段锁——进入下一阶段前必须通过的自检，要么过要么失败，没有"大概"。
_Avoid_: checkpoint。

**Verification Level（证据等级 V1–V4）**:
论断背后的证据强度：V1 实机 / V2 源码 / V3 文档 / V4 推断。🔴🟠 问题须 ≥V2。
