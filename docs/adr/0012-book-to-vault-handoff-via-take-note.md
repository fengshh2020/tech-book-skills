# 0012 — 生产者/适配者切分：Book Artifact 经 take-note book-ingest 进库

承接 [0011](0011-kb-root-resolution-and-portability.md)（portable）。解决"缝 2"：generate-book 的 Book Artifact（独立交付物）与库内 Obsidian 原生书（`文档库/{书名}/`）是两种不同形态、无路径相通——从源生成的书要进库只能手工转换。

## 背景

端到端工作流（ADR 范围 = 用户旅程，非仅生产闭环）暴露的交接缝：

- generate-book 产 **Book Artifact**：`{RUN}/src/*.md` + `book.yml`，GitHub 方言、无 frontmatter/双链/面包屑/MOC，builder 渲染 HTML + MD（ADR-0001）。portable、不感知 `$KB_ROOT`（ADR-0011）。
- take-note 的库内书：`文档库/{书名}/` + `00_MOC`（type: moc）+ 编号章节（type: book + prev/next）+ 面包屑 + 挂链 `00_首页`，Obsidian 原生渲染 callout/mermaid。
- 两者不可互转：生成的书进不了库。

三选项：① take-note 负责"书 → 库"交接（generate-book 保持 portable）；② generate-book 加 `--vault` 模式直接写库（耦合库、破坏 portable/GitHub-MD 设计）；③ 宣告两者本就分开（接受摩擦）。

## 决策

1. **选 ①——生产者/适配者切分**：generate-book 保持纯粹/portable，**不感知 `$KB_ROOT`、不加库依赖**；take-note（库适配层）新增 **book-ingest** 模式，把一份已完成 Book Artifact 的 `src/*.md` 适配进 `文档库/{书名}/`（每章套库 frontmatter、建 `00_MOC`、加面包屑、挂链 `00_首页`）。
2. **book-ingest 消费 `src/*.md`，不是 `output-md/`**：`src/` 是信息主源（ADR-0001），带完整 callout/mermaid 文本；库原生渲染这些（Obsidian），**不走 builder**；HTML Edition 在交接时丢弃。
3. **库内书（Vault Book）一旦 ingest 即 Obsidian 公民，不可 builder 重建**：独立书留 `{RUN}/`（builder 驱动，HTML+MD）；库内书分叉。两种书、两个渲染器、一份源在交接时消费一次。
4. **take-note 三模式并列**：session-book（从零写 session 成型短篇书）/ book-ingest（适配已有 Book Artifact）/ wiki-ingest（编译 concept 页，[0009](0009-llm-wiki-paradigm-via-take-note.md)）。唯 book-ingest 适配已有产物。

## 关键约束

- generate-book 不加库依赖、不感知 `$KB_ROOT`（ADR-0011 portable 不动）；库约定（frontmatter / MOC / 面包屑 / prev-next）**只在 take-note 侧**。
- Book Artifact 与 Vault Book **不互为渲染**：前者 builder 产 HTML+MD，后者 Obsidian 原生；交接单向、一次性。
- 沿用 0001/0011；builder 契约（0002）、light-only（0003）、mermaid→PNG（0004）、writing-core 全不动。
- vault `CLAUDE.md` 仍是实例配置；take-note 的 `$KB_ROOT` 扫描在任何地方工作（0011）。
- book-ingest 是**可选触发**：用户要独立交付物时 generate-book 照常产 Book Artifact，不强制进库。

## 收益

- 补上"生成的书进库"的缺失路径；库有唯一主人（take-note）；generate-book 保持 portable。
- 两种"书"各归其 renderer，不互相耦合——Book Artifact 给对外发布，Vault Book 给库内研读。

## 回退路径

- 若 book-ingest 不被使用：撤回 take-note 的 book-ingest 模式与 Vault Book 术语，generate-book 不受影响（本就是独立路径）。
- 若用户其实要 generate-book 直接写库：切到选项 ②（加 `--vault`），但需接受 portable 损失与生产者/适配者边界的溶解。
