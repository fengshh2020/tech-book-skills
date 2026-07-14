# 维护可复利知识库（LLM-wiki 范式）

take-note 除"把当前 session 写成笔记"外，还维护一个**可复利的知识库**——`$KB_ROOT` 顶层 `wiki/` 与 `项目-{名}/` · `文档库/` · `系统配置/` 并列、交叉引用；**你不手写 wiki，LLM 写——你只策展源、问好问题**（wiki 是代码库、LLM 是程序员）。

先判要不要进 wiki：单 session 的项目结论 → 仍走笔记；跨项目/跨书、值得反复回查的可迁移概念 → `wiki/`。

## `wiki/` 结构

```
$KB_ROOT/wiki/
├── index.md      ← 全局目录（LLM 维护：主题树 + 所有 concept/entity 页 + 最近更新）
├── log.md        ← append-only 操作日志（每次 ingest/query/lint 追加一行）
├── raw/          ← 不可变源：URL/论文/粘贴文本 → markdown，按主题分目、文件名带日期
└── {topic}/      ← 编译页：一个 concept/entity 的合成理解，frontmatter(type: read) + 双链 + 来源引用(链回 raw/)
```

## 五操作

1. **INGEST**：给 URL/文件/粘贴文本 → 存 `raw/{topic}/YYYY-MM-DD-slug.md`（不可变）→ 读源、抽 entity/concept → 更新或新建对应 `wiki/{topic}/*.md`（一源通常触 5-15 页）→ 更新 `index.md` → 追加 `log.md`。下笔前问"要强调什么"。
2. **COMPILE**：每页是**跨多源的合成理解**（非单源摘要）——每条 claim 链回 `raw/` 出处、链相关页、标矛盾与开放问题。
3. **INDEX**：`index.md` 自动维护主题树与页清单。
4. **QUERY**：问"我对 X 了解什么"→ 跨编译页研究答 → **答案存为新页**（复利：每次查询都让库更厚）。
5. **LINT**（定期，**Read 驱动自检——take-note 无 Bash**）：断双链（`[[x]]` 目标存在）/ 孤儿页（无入链）/ frontmatter 缺字段 / 来源 `[[raw/...]]` 失效 / `index.md` 与实际页一致 / `log.md` 与操作吻合。发现即修、记 `log.md`。

## 与项目结构并行（不吞并）

- `项目-{名}/` 记**项目内**调试/方案/设计（不变）；`wiki/` 记**跨项目、跨书**的可迁移 concept/entity。
- 交叉引用：项目笔记在 `## 关联笔记` 引相关 wiki concept 页（`[[wiki/topic/concept]]`）；wiki 页引相关项目调试（"实证见 [[项目-X/调试/...]]"）。新 wiki 页也回头更新 `index.md`，让网络闭环。
- wiki 页 frontmatter：`type: read`、`project: 知识库`，沿用库的 callout / 双链 / 面包屑约定（面包屑写 `📍 知识库入口 [[00_首页]]`）。
- **多源同源**：`generate-book` 多源的 `knowledge_base/{book}/index.md`（ingest→compile）与 `context-summary.md`（compaction）同源于此范式；区别——书是交付物（不复利），wiki 是活库（复利）。
- **review 发现作 raw/ 源**：review-tech-book 报告里 flag 的"系统性/可复利候选"（跨书可复用反模式）是 wiki 的 raw/ 来源——INGEST 时**摘那条发现**进 `raw/{topic}/YYYY-MM-DD-slug.md`（不搬整份 report.md，raw/ 是不可变原子源），再 compile 成 concept 页。review 只 flag、不写库（生产者/适配者切分，[ADR-0012](../../docs/adr/0012-book-to-vault-handoff-via-take-note.md)）。
