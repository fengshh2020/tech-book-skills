# 0002 — 富组件映射取"务实子集"

MD 为源（见 [ADR-0001](./0001-markdown-as-source-html-built.md)）下，通用/GitHub MD 无法表达 HTML 设计系统的全部 ~30 个富组件。决议：**只为高阅读价值组件定作者约定**，builder 识别后升级为对应 HTML 富组件。

## 升级组件（有约定）
- **callout/侧边栏**：标签化引用块 `> **[性能提示]** …` → `.sidebar.performance-tip` 等（沿用现有变体词汇）。
- **图 + 图注**：`![alt](path "图：标题")` → `<figure>` + `.fig-caption[data-num]` 自动编号。
- **代码块**：围栏 + 语言标签 + 可选 `caption="…"` → `<pre data-lang>` + `.CodeListingCaption`。
- **表格 / 术语条**：原生 MD 表格 / `**术语**（English）` → `.table-wrapper` / `.glossary-term`。

## 降级组件（用最近原生等价物，HTML 不做特殊交互）
多语言标签页 → 顺序代码块；测验 → "问题/答案"列表；文件树 → 缩进列表；差异视图 → 注释行；API 参考/代码标注 → 代码块 + 列表。

## 理由
覆盖约 80% 阅读价值，同时把 builder 的组件映射表限定在可控规模。完整映射令 builder 过重；极简会放弃"静奢"设计系统差异化、与"漂亮优雅"目标相悖。
