# 0009 — LLM-wiki 范式：演进 take-note 维护顶层 `wiki/`

承接 [0006](0006-generalize-and-consolidate.md)（输入×形态正交）/ [0008](0008-context-engineering-spine-and-landmine-reframe.md)。把 Karpathy 的「LLM 维护的可复利知识库」范式落进本库，**演进 take-note**（不新增 skill），并在 vault 顶层开一个与项目结构**并行**的 `wiki/`。

## 背景（调研依据，2026-07）

- **Karpathy LLM Wiki（2026-04-02，X + Gist，19.6M 阅读）**："Obsidian 是 IDE，LLM 是程序员，wiki 是代码库。" 五层：**INGEST**（`raw/` 不可变源，人策展）→ **COMPILE**（`wiki/` LLM 写、人读：entity/concept 页 + 摘要 + 反向链接）→ **INDEX**（自动目录/分类树/导航）→ **QUERY**（跨编译知识研究答）→ **ENHANCE**（查询结果回写，复利）。三操作：Ingest（1 源触 10–15 页）、Query（答案存为新页）、**Lint**（周度健康检查：矛盾 / 孤儿页 / 断链）。`raw/` 不可变 vs `wiki/` LLM 维护；append-only `log.md`。"你不写 wiki，LLM 写；你只策展源、问好问题。" 社区实现（Astro-Han/karpathy-llm-wiki，94 篇 / 99 源 / 日维护）验证可落地。
- 与本库的契合：take-note **本就是** Obsidian 适配层（归位 / 双链 / MOC），vault 现有笔记**已经是手工维护的 wiki**；`generate-book` 多源的 `knowledge_base/` 索引 + `progress.md`（=Structured Notes，见 [0008]）已是 ingest/compile 的雏形。差的是**复利性**（查询回写）与**健康检查**（lint）的显式化。

## 决策

1. **演进 take-note**（不新增 skill）：take-note 除"把当前 session 写成笔记"外，新增**维护一个可复利知识库**的职责——ingest 外部源（URL / 论文 / 粘贴文本 / 文件）→ compile 进 `wiki/` → 维护 index → 答查询并把结果回写 → 定期 lint。与 [0006] 的能力轴一致：session × note/doc 仍是 take-note，wiki 是其知识库形态的延伸。
2. **顶层 `wiki/` 并行结构**（用户决策，非叠加进项目夹）：`$KB_ROOT` 顶层开 `wiki/`（路径动态解析见 [ADR-0011](0011-kb-root-resolution-and-portability.md)），与 `项目-{名}/` · `文档库/` · `系统配置/` 并列。结构：
   ```
   $KB_ROOT/wiki/
   ├── index.md          ← 全局目录（LLM 维护）
   ├── log.md            ← append-only 操作日志（ingest/query/lint）
   ├── raw/              ← 不可变源（按主题分目，文件名带日期）
   └── {topic}/          ← 编译页：entity/concept 页，带双链 + 来源引用
   ```
   项目笔记 ↔ wiki 页**交叉引用**（项目笔记引相关 concept 页，wiki 页引相关项目调试）。**不重构 `项目-{名}/`**（CLAUDE.md 硬约定不动）。
3. **lint 用 Read 驱动的模型自检**（不用脚本）：take-note 是 `allowed-tools: Read, Write`，无 Bash——lint 做成**读文件自检清单**：断双链（`[[x]]` 目标存在）/ 孤儿笔记（无入链）/ frontmatter 缺字段 / `file:line` 引用失效 / `log.md` 与实际文件一致。与 [0005]「Gate 退化为正文自检」一致，不为 take-note 跑不了的东西加 Bash 依赖。
4. **multi-source 借同一套结构**（非重复实现）：`generate-book` 多源 Phase 0 的 `knowledge_base/{book}/index.md` 沿用 ingest→compile 心法（raw 索引 → 编译索引），`context-summary.md` 即 Compaction（[0008]）。不把 wiki 复利机制塞进一次性书生成（书是交付物、非复利库）。

## 关键约束（沿用 0006 / 0008）

- `项目-{名}/{调试|方案|设计}/` 结构与归位规则**不动**（CLAUDE.md 硬约定）；wiki 与之并行、交叉引用，不吞并。
- take-note 不加 Bash / 不加脚本；lint 是 Read 自检。
- wiki 的 frontmatter / callout / 双链约定**沿用 take-note 既有库约定**（不另立一套）。
- description 路由化（0007）：take-note description 增"维护知识库 / ingest 源"触发短语，不破坏既有触发。

## 收益

- take-note 从"记单笔"升级为"维护可复利知识库"，吃透 Karpathy 范式而不增 skill。
- vault 多一个与项目并行的 wiki 层，复利沉淀跨项目 / 跨书的可迁移知识。
- lint 让库"健康可见"（断链 / 孤儿 / 失效引用），补上手工 wiki 最缺的维护闭环。

## 回退路径

- 若 wiki/ 与项目结构并行造成归属混乱：把 wiki 降级为 `文档库/_wiki/`（并入既有书区），take-note 逻辑不变。
- 若 Read 自检 lint 力度不够：可后续加 `shared/lint_knowledge.py` + 给 take-note 开 Bash（独立决策，本 ADR 不做）。
- 若 ingest 外部源不被使用：wiki 章节可整体撤回，take-note 回到"仅记 session"，不影响其余 skill。
