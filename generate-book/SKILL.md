---
name: generate-book
description: "Use when writing an original technical book or project learning doc from multiple source books or a codebase — unified structure, deep explanation, any tech stack (Python / Rust / Go / 嵌入式 C/C++ / shell …). Triggers: 整合书籍, merge books, 多本书整合, 整合成一本书, 生成书籍, 项目学习文档, 代码库走读, codebase book, 掌握项目, 架构学习指南, 学习指南, 给这个项目生成文档, walkthrough this project, project guide, learning doc. Do NOT trigger for: translating a single book (use translate-book), session notes or short docs (use take-note), quality review (use review-tech-book)."
---

# 写技术书 / 学习文档（原创）

从多本源书或一个代码库写一本**讲得透**的原创技术书——结构服务讲解，不是讲解填充结构。

**先读 `../shared/writing-core.md`**（讲解质量三标准 / 反冗余红线 / 铁律）；**项目怎么跑见 `../shared/book-project.md`**（工作区 / 曳光弹首章 / 滚动构建 / 恢复）。

## 核心回路

**读透源 → 设计结构 → 逐章讲透 → 滚动构建校验**

- **读透**：多源逐书逐章实读，读到能答出"两本书在此主题上的方法论差异"；代码库沿执行路径读，每论断带 `file:line`。凭标题 / 目录猜 = 违反铁律。
- **设计结构**：先写读者模型（记 `progress.md`），按认知递进组织；结构到"依赖顺畅、目的清晰"即停，预算留给正文。
- **逐章讲透**：每个知识点走完整讲解链（动机 → 机制 → 示例 → 边界）；结构 / 流程 / 状态 / 数据流能画就画（SVG）；一个知识点只讲一次；多源融合成同一个作者的声音。
- **滚动构建校验**：按 book-project 写作回路——首章曳光弹（构建 + 校验 + 用户过目）→ 每 3-5 章重跑 → 终检全套。

## 路由与形态

单本书翻译 → translate-book；短 session 沉淀 → take-note。**book**（正式书，`{RUN}` 工作区双格式）/ **doc**（就地单文件，无 builder，轻量自检）。

🛑 **开跑对齐走 `../shared/kickoff.md`**，决策：源 / 代码库、形态与输出位置、目标语言、目标读者。

## 底线自检（generate 特有项；writing-core 红线同时生效）

- 多源：每源章节都处置了、融合到读者无法辨识来源、无单源占 80%（`scripts/check_coverage.sh`）。
- 代码库：每论断 `file:line`，贴出的代码都有走读（代码与讲解比 ≥1:1）。
- doc 形态：真读证据 + 上述对应项 + 无占位符、文件非空。

## 参考文件（按需读，不全读）

| 文件 | 适用 |
|---|---|
| `../shared/writing-core.md` | 全部（先读） |
| `references/multi-source.md` | 多源：读透判据 / 统一结构 / 融合写作 / 覆盖率 |
| `references/writing-and-content.md` | 代码库：发现分析 / 叙事驱动走读 / 先图后文 |
| `references/craft.md` | 写作全程：读者模型 / 误解驱动 / 示例三件套 / 能力弧 |
| `../shared/book-project.md` | book 形态 |
| `../shared/md-authoring.md` | book 形态：章节格式与组件（builder 契约） |
| `../shared/kickoff.md` | 开跑前 |
