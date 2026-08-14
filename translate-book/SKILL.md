---
name: translate-book
description: "Use when translating a single source book (EPUB / HTML / PDF / Markdown) into another language — faithful, fluent, structure 1:1, terminology consistent, code untouched. Triggers: 翻译书籍, 翻译这本书, 把这本书翻译成中文, 翻译英文书, translate this book, translate book, book translation, 中文化这本书, 汉化这本书. Do NOT trigger for: merging multiple books into a new original book or writing docs from a codebase (use generate-book), quality review of a translation (use review-tech-book), translating a short passage or file (just do it inline, no pipeline needed)."
---

# 翻译技术书

把一本源书完整译成目标语言。**结构、段落、代码与源 1:1 对应**——源书的结构就是结构，不重新设计、不增删栏目（源书有"本章小结"就照译，没有就不加）。功夫全部花在两件事上：**译文准确**、**中文地道**。

**先读 `../shared/writing-core.md`**（铁律 / 反 AI 腔——对译文同样生效：译得像人写的；讲解质量的重构权不适用，不能替作者重新组织内容）；翻译纪律（解析源 / 四原则 / 术语 / 红线清单）在 `references/translation.md`；项目怎么跑见 `../shared/book-project.md`。

## 核心回路

**解析源 → 逐章实读 → 翻译 → 滚动构建校验**

- **解析源**：EPUB 解压走 spine 定序、PDF 提文本层、HTML 按标题导航定章界。🛑 扫描件 / 无文本层 PDF / DRM 加密 → 停下问用户，不绕过、不静默降级（详见 translation.md）。
- **实读**：逐章打开真读、不跳章，章进度与阅读证据记进 `progress.md`（铁律，也是断点续译依据）。
- **翻译**：四原则 + 术语表 + 格式红线全在 `references/translation.md`。术语表从第一章开始建、全书统一。
- **滚动构建校验**：**首章即曳光弹**——首章 + 术语表初版译完立即构建交用户过目（术语译法、腔调基线、格式一次对齐——全书写完才发现术语不一致是翻译最贵的返工）；认可后量产，每 3-5 章重跑校验；终检对照红线清单。

## 形态与路由

book（正式出版物，`{RUN}` 工作区双格式）/ doc（就地单文件译文，无 builder）。多本整合 / 代码库书 → generate-book。

🛑 **开跑对齐走 `../shared/kickoff.md`**，决策：源路径与格式、目标语言、形态。

## 底线

对照 `references/translation.md` 红线清单终检：段落 1:1、代码逐字（注释中文）、术语全书一致、翻译腔 / AI 腔 0 命中（`../shared/translationese-patterns.md`）、输出 ≥ 源 80%（防缩减）。doc 形态模型自检。

## 参考文件（按需读，不全读）

| 文件 | 适用 |
|---|---|
| `references/translation.md` | 翻译纪律全表（先读） |
| `../shared/writing-core.md` | 全部 |
| `../shared/book-project.md` | book 形态 |
| `../shared/md-authoring.md` | book 形态：章节格式与组件 |
| `../shared/translationese-patterns.md` | 自检 |
| `../shared/kickoff.md` | 开跑前 |
