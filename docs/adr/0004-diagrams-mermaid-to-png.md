# 0004 — 图表：Mermaid 为源，mmdc 渲染仅 PNG

图表源从 "JSON spec → `render_drawio_diagrams.py` → `.drawio`" 改为：**agent 在 MD 中写 ` ```mermaid ` 文本**，构建期用 mermaid-cli (mmdc) 渲染**仅 PNG**。MD 版 `![x](diagrams/x.png)`，HTML 版同嵌 PNG。

## 理由
- LLM 易写 mermaid 文本；GitHub 原生渲染（MD 版零构建即可读）。
- light-only（[ADR-0003](./0003-light-only-no-dark-mode.md)）下无需 SVG 做主题感知，单 PNG 足够且最可移植。
- 取代既重又 CI 不友好的 drawio CLI，且 `.drawio` 无法直嵌通用 MD。

## 代价
放弃 drawio 可视化编辑；JSON spec 的边级 evidence（file:line）改为写在图注里。

## 连带清理
`render_drawio_diagrams.py`、`fixtures/diagram-specs/*.json` 废弃；`book-assembly.md` L576-590、`writing-and-content.md` L101-131 的 "SVG 嵌入 / DrawIO" 陈述、`mode-codebase.md` 的 `*.drawio` 路径需删除或改写为 Mermaid 单轨。
