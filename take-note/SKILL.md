---
name: take-note
description: Use when the user asks to "记笔记", "记录一下", "存到知识库", "把这个记下来", "记一笔", "写进笔记", or otherwise explicitly requests writing the current session's content into the Obsidian knowledge base at /mnt/d/知识库. Also use it proactively when the conversation has distilled reusable long-form content worth saving (a debug finding, a config trick, a design decision, a code walkthrough) even without an explicit trigger phrase. Produces a structured note following the library's project-based conventions and writes it to the right project folder. Trigger this skill BEFORE composing the note so it lands in the correct place with the correct format. Do NOT trigger for: writing a full multi-page book or long document from scratch (use generate-book), code/API review (use review-tech-book), or generating brand-new technical content rather than capturing this session's content.
allowed-tools: Read, Write
---

把当前 session 的内容写成一篇符合库约定的结构化笔记，落到正确的位置。库根 `/mnt/d/知识库`，用用户当前语言写（默认中文）。

**写作原则（结论前置 / 原子性 / 标题即论点 / 面向检索 / 上下文自足 / 抽象成原则 / 事实与推断分离）见 `shared/writing-core.md`**——本文件只讲 Obsidian 库特有的：归位、frontmatter、callout 语义、面包屑与双链。库有强归位/命名约定，**下笔前缺信息（哪个项目、文件名、范围、是否拆篇）一律问用户，别默写——猜错会返工**。

## 库结构（按项目组织）

```
/mnt/d/知识库/
├── 00_首页.md                 ← 全库入口/仪表盘
├── 文档库/                    ← 书籍/长文档（多页系统学习，每本一文件夹 + 00_MOC）
├── 项目-{名}/                 ← 每项目自包含：{项目名}.md 作 MOC + 调试/方案/设计 子目录
│   （现有：DDPM模型转换、机器狗语音控制、Jetson部署）
└── 系统配置/                  ← 跨项目复用的工具链/环境配置（扁平，type: config）
```

每个项目夹有一篇 MOC（`{项目名}.md` 或 `00_MOC.md`）串联其下笔记；`文档库/` 每本书有自己的 `00_MOC`。任何笔记都链回所属 MOC + `00_首页`，不孤立。

## 先判类型：笔记 vs 书

| | 笔记（note） | 书籍/文档（book） |
|---|---|---|
| 形态 | 原子、单点结论（一个坑/一条配置/一个结论） | 多页、系统讲清一个主题 |
| 归位 | `项目-{名}/{调试|方案|设计}/` 或 `系统配置/` | `文档库/{书名}/` |
| type | `debug`/`plan`/`config`/`read`/`design` | `moc`（书总目录）+ `book`（章节） |
| 规则 | writing-core 六原则（结论前置/原子/去水分） | **不套笔记的"精简"标准**——书就该厚，多页+MOC+教学 callout+三级证据 |
| 导航 | 面包屑链回项目 MOC | `prev`/`next` 串章 + 面包屑链回书 MOC |

一个可复用独立结论 → 笔记；要系统讲清、需多页展开 → 书/文档（且从零生成时用 generate-book）。拿不准问用户。下文默认讲**笔记**写法。

## 🔴 下笔前停下问用户（会造成返工的自主决策点）

1. **一个 session 有 ≥2 个独立主题** → 别堆一篇，各拟标题+归属，等确认拆分。
2. **项目归属不清/跨项目** → 别猜目录，列候选问归哪个或是否新建 `项目-{名}/`。**特例**：既是项目 debug 故事又是可复用 config（如 Jetson 跑 DDPM 撞见 `LD_LIBRARY_PATH`）→ 以**项目 debug 笔记**为主，在 `系统配置/` 那篇加一行链回，别把 debug 故事挪进 `系统配置/`。
3. **文件名拿不准** → 给 2-3 个带论点的候选让用户选。
4. **写书/长文档** → 动笔前敲定书名、目录、目标读者（大工程）。

边角情况（文件已存在/项目无夹/MOC 不存在）一律「先试合理默认 → 失败就问用户」，绝不静默猜或静默覆盖。**Read-before-Write**：目标文件已存在时先 Read ≥1 行，同主题→追加章节并链回，撞名→问用户「覆盖/追加/改名」。

## Step 1 — 归位（先项目，再子目录）

**第 1 问：跨项目复用的工具链/环境配置？**（换项目也用得上的 Claude Code/shell 技巧/uv/功率模式/LD_LIBRARY_PATH 等）→ `系统配置/`（`type: config`）。
**第 2 问：哪个项目？** → `项目-{名}/{子目录}/`，子目录对齐该项目已有目录（打开该项目夹看一眼）：

| 笔记性质 | 子目录 | type |
|---|---|---|
| 设计/架构/读代码精读/学习总结/教学 | `设计/` | `design` |
| 踩坑/调试/部署问题/bug 排查 | `调试/` | `debug` |
| 方案/选型/架构规划 | `方案/` | `plan` |

**第 3 问：项目还没有文件夹？** → 问用户：新建 `项目-{名}/`（并建 `{项目名}.md` 作 MOC）还是归现有项目。

## Step 2 — 文件名

中文主题词 + 必要英文术语，空格分隔（`LD_LIBRARY_PATH 与 bash 参数展开语法`）。**无日期前缀**（日期在 frontmatter）。标题带论点（原则 3）、含可搜索关键词（原则 4）。多页连续主题用 `数字_标题.md` + `prev`/`next` 串起来。

## Step 3 — frontmatter（六字段必填）

```yaml
---
title: "{标题，与文件名、H1 一致}"
type: {moc | design | debug | plan | config | read}
project: {DDPM模型转换 | 机器狗语音控制 | Jetson部署 | 系统配置 | {新项目名}}
date: YYYY-MM-DD
status: {active | draft | archived}
tags:
  - {platform}     # thor, jetson-agx-orin, jetpack-7（硬件相关时）
  - {tech}         # tensorrt, pytorch, docker, onnx（核心技术）
  - {tech-2}       # 再补 1-2 个相关技术
  - {topic}        # deployment, conversion, precision（主题）
---
```

`type` 决定角色，通常对应子目录（`moc`=项目总览，`read`=不属具体项目的通用学习）。`project` 填项目名（不含"项目-"前缀）；跨项目配置填 `系统配置`。`status`：`active`(默认)/`draft`/`archived`（方案类也可 `implemented`/`approved`/`rejected`）。`tags` 3-8 个，扁平、不要 `topic/subtag` 层级。可选：`platform`、`source`、`prev`/`next`/`book`（仅多页系列/书式笔记）。

## Step 4 — 正文骨架

单个 `# H1`（同文件名）。按 type 裁剪章节，不是每节都用：

```markdown
# {标题}

> {YYYY-MM-DD} · {项目或场景} · {一句话：记什么、为什么记}

> [!important] 结论 / TL;DR
> {最重要的答案/命令/论点，1-3 句。不读全文也能拿走。}

## 背景 / 环境基线 / 问题描述
{环境基线用表格（设备/版本/配置）。}

## {主体章节}            ## 坑 N：{坑标题}（仅踩坑/调试类）
{## 分章。}              **现象**：{报错原样引用}
                         **根因**：{为什么；复杂根因用 5-Why 链}
                         **解决**：`{命令}` → `# 预期输出: {...}`

## 方法论沉淀            ← 调试/配置类结尾
> [!abstract] 红线一：{一句话原则}
> {把单次经验抽象成可迁移红线。}

## 关联笔记
- [[{相关笔记}]] — {一句话关系}
- [[{待创建}]]（待创建）

---
📍 所属项目：[[{项目MOC 或 00_首页}]] · 知识库入口 [[00_首页]]
```

**面包屑页脚（必加，硬约定）**：末尾 `📍 所属项目：[[{项目 MOC}]] · 知识库入口 [[00_首页]]`。`系统配置/` 无项目 MOC，写 `📍 知识库入口 [[00_首页]]`。**Commands carry expected output**（shell/dockerfile/python 块下加 `# 预期输出: ...`）。**Cite code with `file:line`**。单 H1、不跳级。

## Step 5 — Callout 语义（库固定）

| 用途 | Callout |
|---|---|
| 陷阱/坑/反例 | `> [!warning]` |
| 补充说明 | `> [!info]` / `> [!tip]` |
| 最重要结论/唯一要点 | `> [!important]` |
| 方法论红线（方法论沉淀节） | `> [!abstract] 红线N：{title}` |
| 推断/未实测/待验证 | `> [!caution]`（标"推断/待验证"——**最重要的一条**，别把假设写成结论） |
| 已验证/确认可用 | `> [!success]` |

## Step 6 — 双链（笔记是网络节点）

1. **结构回链**：面包屑页脚指向项目 MOC + `00_首页`。
2. **主题互链**：`## 关联笔记` 区用 `- [[note]] — {关系}` 链 1-2 条相关笔记并注明关系（因果/对比/前置/同主题）；`[[待创建]]（待创建）` 留给应存在但还没的笔记。已知 hub：`[[DDPM模型转换]]`、`[[机器狗语音控制]]`、`[[Jetson部署]]`（`[[00_MOC]]` 是 `文档库/` 里 DDPM 那本书的总目录，不是项目 MOC——别链错）。新笔记也要回头更新它引用到的项目 MOC（笔记地图加一行），让双链闭环。

## 规则

- **只留可复用的**：删探索过程（"我先试…然后猜…"），留命令、根因、配置值、行号引用、决策。短而实胜过灌水长文。
- **不碰**：`.base`、`.remember/`、`.obsidian/workspace.json`。**只写 `.md`**（不生成 `.html` 兄弟文件，导出插件的事）。**不 commit**（用户用 github-sync 插件 `Ctrl+Shift+S` 自己同步）。

## 写书/文档

**从零生成一整本多章技术书 / 给项目或代码库生成学习文档 → 不要用 take-note，用 generate-book**（book 形态 = 全书双格式 builder；doc 形态 = 就地 MD，轻量 gate）。本节仅适用于 **session 里自然成型的短篇**书式文档（几页精读/教程/长方案）：归位 `文档库/{书名}/`，`00_MOC.md`（`type: moc` + `book: "{书名}"`，写"给谁看+目标+阅读路径+目录表+怎么用"）+ `数字_标题.md` 章节（`type: book` + `prev`/`next`）；附录用 `A0_`/`A1_` 前缀，图放书根 `assets/`。**书不套笔记的精简标准**——多页+教学 callout+三级证据都是教学需要，长度不是水分。

## 完成时

只打印一行：写入文件的绝对路径 + 一句话内容摘要。

```
/mnt/d/知识库/项目-{项目名}/{子目录}/{filename}.md — {一句话内容摘要}
```
