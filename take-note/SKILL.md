---
name: take-note
description: "Use when the user asks to 记笔记 / 记录一下 / 存到知识库 / 把这个记下来 / 写进笔记 / 整理知识库 / 维护 wiki, when ingesting an external source (URL / paper / pasted text / book) into the Obsidian-style knowledge base (root auto-detected), when adapting a finished generate-book/translate-book artifact into the vault (book-ingest), or proactively when the session distilled reusable content (debug finding, config trick, design decision) worth saving — even without an explicit trigger phrase. Do NOT trigger for: full multi-chapter books generated from sources/codebase (use generate-book / translate-book), quality review (use review-tech-book), or original long-form content not derived from this session."
allowed-tools: Read Write Glob
---

把当前 session 的内容写成一篇符合库约定的结构化笔记，落到正确的位置。库根 `$KB_ROOT` **动态解析**（见下），用用户当前语言写（默认中文）。铁律与反 AI 腔见 `../shared/writing-core.md`；**归位 / frontmatter / 正文骨架 / callout / 双链约定在 `references/vault-conventions.md`——下笔前读一次**。

## 核心回路

**判落点（项目 / 系统配置 / 文档库 · 笔记 vs 书）→ 写原子笔记（结论前置 + 环境基线 + 证据）→ 挂双链与面包屑**

## 笔记质量（非协商）

1. **结论前置**——首屏给最重要的答案 / 命令 / 论断，不读全文也能拿走。
2. **原子自足**——一篇只答一个问题 / 记一个坑；脱离产生它的对话也能读懂（写全环境基线、复现步骤、关键变量值）。
3. **标题即论点**——带核心结论或关键变量，不是话题标签；含"半年后你会用什么词搜"的关键词（技术名 / 报错关键字 / 设备型号）。
4. **事实与推断分离**——推断 / 未实测一律 `[!caution]` 标「推断 / 待验证」，不当结论写。
5. **只留可复用的**——删探索过程（"我先试…然后猜…"），留命令、根因、配置值、行号引用、决策。短而实胜过灌水长文。

## 定位知识库根（`$KB_ROOT`，portable）

从 cwd 向上找 KB 标记——`.kb-root` 文件（显式）**或** `00_首页.md`（约定）；命中 → 该目录即 `$KB_ROOT`；**找不到 → 问用户**：① 指定已有 KB 路径；② 在 cwd 初始化新 KB（建 `00_首页.md` + `文档库/` + `系统配置/` + `wiki/`）；③ 就地单篇。环境变量 `KB_ROOT` 设了即用。项目运行时发现——Glob 列 `$KB_ROOT/项目-*/` 现有项目（不硬编码）；每个项目夹的 `{项目名}.md` 或 `00_MOC.md` 是其 MOC。

## 归位速判（归位表与三问见 references/vault-conventions.md）

一个可复用独立结论 → 笔记；要系统讲清、多页展开 → 书/文档（长程从源/代码库生成用 generate-book / translate-book）；技术方案 → `type: proposal`（保留完整方案体，不套精简标准）；跨项目可迁移概念 → `wiki/`（opt-in）。

## 🔴 下笔前问用户（会造成返工的自主决策点；问法走 `../shared/kickoff.md`）

1. **一个 session 有 ≥2 个独立主题** → 各拟标题+归属，等确认拆分，别堆一篇。
2. **项目归属不清/跨项目** → 列候选问归哪个或是否新建 `项目-{名}/`。**特例**：既是项目 debug 故事又是可复用 config → 以项目 debug 笔记为主，在 `系统配置/` 那篇加一行链回。
3. **写书/长文档** → 动笔前敲定书名、目录、目标读者。

**Read-before-Write**：目标文件已存在时先 Read，同主题→追加并链回，撞名→问「覆盖/追加/改名」。

## 写书/文档（`文档库/`，opt-in）

- **session-book**（session 成型短篇书，无流水线）：直接写。`00_MOC.md`（`type: moc` + `book: "{书名}"`）+ `数字_标题.md` 章节（`type: book` + `prev`/`next`）；附录用 `A0_`/`A1_` 前缀，图放书根 `assets/`。
- **book-ingest**（适配已完成的 generate-book / translate-book 产物 → Vault Book）：读 `{RUN}/src/*.md`（**非 `output-md/`**；工作区布局见 `../shared/book-project.md`），每章套库 frontmatter（`type: book` + `book:` + `prev`/`next`）、建 `00_MOC`、加面包屑、挂链 `00_首页`。Obsidian 原生渲染 callout/mermaid，不走 builder、HTML 版交接时丢弃。

书不套笔记的精简标准——多页 + 教学 callout 是教学需要，长度不是水分。

## 维护可复利知识库（`wiki/`，opt-in）

跨项目/跨书、值得反复回查的可迁移 concept/entity → `$KB_ROOT/wiki/`。**你不手写 wiki，LLM 写——你只策展源、问好问题**；单 session 的项目结论仍走笔记，不进 wiki。结构 + 五操作（INGEST/COMPILE/INDEX/QUERY/LINT）见 `references/llm-wiki.md`（按需读）。

## 规则

**不碰**：`.base`、`.remember/`、`.obsidian/workspace.json`。**只写 `.md`**（不生成 `.html` 兄弟文件）。**不 commit**（用户自己同步）。

## 完成时

只打印一行：`$KB_ROOT/项目-{项目名}/{子目录}/{filename}.md — {一句话内容摘要}`

## 参考文件（按需读，不全读）

| 文件 | 适用 |
|---|---|
| `references/vault-conventions.md` | 每次下笔前（归位表 / frontmatter / 骨架 / callout / 双链） |
| `references/llm-wiki.md` | 维护 wiki |
| `../shared/writing-core.md` | 铁律 / 反 AI 腔 |
| `../shared/kickoff.md` | 下笔前问用户时 |
