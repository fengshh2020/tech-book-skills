---
name: take-note
description: Use when the user asks to "记笔记", "记录一下", "存到知识库", "把这个记下来", "记一笔", "写进笔记", or otherwise explicitly requests writing the current session's content into the Obsidian knowledge base at /mnt/d/知识库. Also use it proactively when the conversation has distilled reusable long-form content worth saving (a debug finding, a config trick, a design decision, a code walkthrough) even without an explicit trigger phrase. Produces a structured note following the library's project-based conventions and writes it to the right project folder. Trigger this skill BEFORE composing the note so it lands in the correct place with the correct format.
allowed-tools: Read, Write
---

Turn the current session's content into a structured note that matches the conventions already used across the /mnt/d/知识库 Obsidian library, then write it to the right place. The knowledge base root is `/mnt/d/知识库`. Write in the same language the user is using (Chinese by default).

Before writing, ask the user anything you need to decide that the session does not already answer: which project, the exact filename, or scope. Do not invent these silently — the library has strong placement/naming conventions and guessing wrong has caused rework before.

## How this library is organized（先建立心智模型）

The library is organized **by project, not by note type**. The top level looks like:

```
/mnt/d/知识库/
├── 00_首页.md                 ← 全库仪表盘/入口
├── 文档库/                    ← 书籍/长文档（多页系统学习，每本一个文件夹 + 00_MOC）
│   └── DDPM模型转换实战/      ← 例：00_MOC + 8 章 + 4 附录 + assets/
├── 项目-DDPM模型转换/         ← 每个项目自包含：MOC + 调试/方案
│   ├── DDPM模型转换.md        ← 项目总览 MOC（{项目名}.md 或 00_MOC.md）
│   └── 调试/  方案/           ← 项目内按性质再细分
├── 项目-机器狗语音控制/
├── 项目-Jetson部署/
└── 系统配置/                  ← 跨项目复用的工具链/环境配置
```

每个项目文件夹有一篇 MOC（`{项目名}.md` 或 `00_MOC.md`）串联其下笔记；`文档库/` 里每本书也有自己的 `00_MOC` 总目录。任何笔记/章节都不孤立：链回所属项目 MOC 或书 MOC，再链到 `00_首页`。

## 两类内容，先判断类型再下笔

知识库装两种内容，写之前先判断这次要写的是哪类——它们走不同规则：

| | 笔记（note） | 书籍/文档（book） |
|---|---|---|
| 形态 | 原子、单点结论（一个坑/一条配置/一个结论） | 多页、结构化系统学习（一本教程/一份精读） |
| 归位 | `项目-XXX/{调试|方案|设计}/` 或 `系统配置/` | `文档库/{书名}/` |
| type | `debug`/`plan`/`config`/`read`/`design` | `moc`（书总目录）+ `book`（章节） |
| 规则 | 下面的 7 条核心原则（结论前置/原子性/去水分） | **不套笔记的"精简"标准**——书就该厚，用多页 + MOC + 教学callout + 三级证据 |
| 导航 | 面包屑页脚链回项目 MOC | `prev`/`next` 串章节 + 面包屑链回书 MOC |

**判断口径**：一个可复用的独立结论 → 笔记；要系统讲清一个主题、需多页展开 → 书/文档。拿不准问用户。下文 Step 1-6 默认讲**笔记**的写法；写书见末尾「写书/文档的单独规则」。

## 🔴 必停检查点（命中任一，先问用户再下笔，不要默写）

这些是会造成**返工**的自主决策点。Step 1-6 里遇到标 🔴 的地方对应到这里：

1. **一个 session 有 ≥2 个独立主题** → 别堆进一篇。先说「这是两篇笔记」，给各自拟标题 + 归属，等用户确认拆分方式（原则 1）。
2. **项目归属不清 / 跨项目** → 别猜目录。列候选项目问用户归哪个，或是否新建 `项目-{名}/`（Step 1）。
3. **文件名拿不准** → 别硬造。给 2-3 个带论点的候选标题让用户选（Step 2）。
4. **写书 / 长文档** → 动笔前敲定书名、目录、目标读者——书是大工程（写书规则）。

> 上述是「下笔前停一下」，不是「写完再问」。文件已存在怎么处理（覆盖/追加/改名）见 Rules 的 Read-before-Write。

## Core principles — 一篇优秀的笔记必须满足

These are non-negotiable; every step below exists to serve them.

1. **原子性（One note = one idea）** — 一篇笔记只回答一个问题、记一个坑、或保存一个可复用结论。一个 session 涉及多个独立主题时，拆成多篇并用 `[[链接]]` 互连，不要堆进一篇大杂烩。
2. **结论前置（Answer first）** — 正文第一句就给出最重要的答案/结论，背景和探索过程放后面。未来的读者（含半年后的你）3 秒内要能拿到答案。
3. **标题即论点（Title carries the takeaway）** — 标题不是话题标签，要尽量带上核心结论或关键变量。
4. **面向未来检索（Search-first）** — 标题、首句、tags 必须含"半年后你会用什么词搜"的关键词（技术名/报错关键字/设备型号）。
5. **上下文自足（Self-contained）** — 脱离产生它的对话也能读懂：写全环境基线、复现步骤、关键变量值，不要写"刚才那个/上面的"。
6. **抽象成可迁移原则（Generalize）** — 把单次踩坑抽象成可复用原则，不只记特殊案例。
7. **事实与推断分离（Separate fact from inference）** — 已验证的结论正常陈述；任何推断/未实测一律 `[!caution]` 标为 推断/待验证（见 Step 5）。

## Step 1 — Decide placement (project first, then subfolder)

> 本节讲**笔记**归位。若内容是书/文档（多页系统学习），不走这里——放 `文档库/{书名}/`，见末尾「写书/文档的单独规则」。

先定项目，再定项目内的子目录。当前已有项目：`DDPM模型转换`、`机器狗语音控制`、`Jetson部署`。

**第 1 问：是不是跨项目复用的工具链/环境配置？**
（Claude Code、shell 技巧、uv、功率模式、LD_LIBRARY_PATH 这类——换个项目也用得上）→ 直接放 `系统配置/`（扁平，`type: config`）。**特例**：若它同时是某项目的 debug 故事（如 Jetson 上跑转换撞见 `LD_LIBRARY_PATH` 报错），别挪进 `系统配置/`——以项目 debug 笔记为主，在 `系统配置/` 那篇里加一行链回即可（见「失败模式」跨项目行）。

**第 2 问：属于哪个项目？** → 放 `项目-{项目名}/{子目录}/`，子目录对齐该项目已有的目录（打开该项目夹看一眼即可）。常见对应：

| 笔记性质 | 子目录 | type |
|---|---|---|
| 设计 / 架构 / 读代码精读 / 学习总结 / 教学 | `设计/` | `design` |
| 踩坑 / 调试 / 部署问题 / bug 排查 | `调试/` | `debug` |
| 方案 / 选型 / 架构规划 | `方案/` | `plan` |

有的项目还有专门子目录（如 `Jetson部署/调试技术/` 放可复用调试方法）——按该项目实际目录来。

**第 3 问：项目还没有文件夹？** → 问用户：新建 `项目-{名}/`（并建一篇 `{项目名}.md` 作 MOC），还是归到某个现有项目。

**🔴 归属不清？** → 问用户，别猜。这是最容易返工的一步（见「必停检查点」#2）。

## Step 2 — Name the file

- Chinese topic words + necessary English terms, space-separated（`LD_LIBRARY_PATH 与 bash 参数展开语法`、`从需求约束倒推实现`）。
- **No date prefix** — the date lives in frontmatter, not the filename.
- **标题带论点，不只是话题**（原则 3）：能在标题里塞进核心结论/关键变量就塞。
- **标题含可搜索关键词**（原则 4）：把未来你会搜的术语/设备/报错关键字放进标题与 tags。
- 🔴 If unsure, propose 2-3 names and ask the user to pick（见「必停检查点」#3）。

**多页连续主题**（一本书、一个分多阶段的项目）：在该项目下用 `数字_标题.md` 命名（`01_转换流程.md`、`02_精度实验.md`），并在 `prev`/`next` frontmatter 里串起来；若体量大，建/更新该项目 MOC 列出全部页。

## Step 3 — Write frontmatter

Every note starts with a `---`-delimited YAML block. **六个核心字段必填**：`title` / `type` / `project` / `date` / `status` / `tags`。（库内个别历史笔记缺 `title`/`type`/`status`——碰到时顺手补齐 backfill，新笔记必须六字段齐全。）

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
  - {topic}        # deployment, conversion, precision, 并发（主题）
---
```

字段说明：
- `type` 决定笔记角色，通常与放置的子目录对应（见 Step 1 表）。`moc` 用于项目总览/首页；`read` 用于不归属具体项目的通用学习笔记。
- `project` 填项目名（不含"项目-"前缀）。跨项目配置填 `系统配置`。
- `status`：`active`（默认，已完成/在用）、`draft`（仍在写）、`archived`（已被取代）。方案类也可用 `implemented`/`approved`/`rejected`。
- `tags`：小写连字符或中文皆可（`tensorrt`、`多线程`），3-8 个，覆盖 platform + tech + topic。**保持扁平，不要用 `topic/subtag` 层级 tag**。行内数组 `tags: [a, b, c]` 同样可接受。

**可选字段**（仅相关时加）：
- `platform: {设备 + OS/JetPack 版本}` — 硬件相关时
- `source: {信息来源}` — 调研/综述类
- `prev: "[[{上一页}]]"` / `next: "[[{下一页}]]"` / `milestone` / `book` — **仅多页系列/书式笔记用**；普通笔记不要加

## Step 4 — Write the body

Exactly one `# H1` heading (same as the filename). Then follow this skeleton; adapt the sections to the note's type — not every section applies to every note.

```markdown
# {标题}

> {YYYY-MM-DD} · {项目或场景} · {一句话摘要，说明这篇笔记记的是什么、为什么记}

> [!important] 结论 / TL;DR
> {最重要的答案、关键命令或核心论点，1-3 句。读者不读全文也能拿走这个结论。}

## 背景 / 概述 / 环境基线 / 问题描述
{背景交代。环境基线用表格（设备/版本/配置）。}

## {主体章节}
{正文内容。用 ## 做章节，### 做子节。}

## 坑 N：{坑标题}            ← 只踩坑/调试类笔记用这个
**现象**：{报错信息或表现，原样引用}
**根因**：{为什么。复杂根因用编号 1→2→3 的 5-Why 链}
**解决**：
\`\`\`bash
{具体命令}
# 预期输出: {...}
\`\`\`

## 方法论沉淀                ← 调试/配置类笔记的结尾
> [!abstract] 红线一：{一句话原则}
> {一两句解释。把单次经验抽象成可迁移红线。}

## 关联笔记
- [[{相关笔记名}]] — {一句话说明关系}
- [[{待创建的笔记名}]]（待创建）

---
📍 所属项目：[[{项目MOC 或 00_首页}]] · 知识库入口 [[00_首页]]
```

Body conventions:

- **结论先行（原则 2）。** `[!important] 结论 / TL;DR` 紧跟摘要，放全文最重要的答案；背景和探索过程都在它之后。读者 3 秒内拿走结论。
- **面包屑页脚（必加）。** 正文末尾加一行 `📍 所属项目：[[{该项目 MOC}]] · 知识库入口 [[00_首页]]`，让任何笔记都能一键回到项目总览和全库首页。`系统配置/` 的笔记没有项目 MOC，写 `📍 知识库入口 [[00_首页]]` 即可。这条让笔记不再是孤岛——和"每篇必加 frontmatter"一样是硬约定。
- **🔴 拆，不要堆（原则 1）。** 正文自然分成 2+ 个互不相关的问题时，停下，先按「必停检查点」#1 跟用户确认拆成多篇 + 互链。
- **Commands carry expected output.** 任何 shell/dockerfile/python 块下加 `# 预期输出: ...` 或 `# 期望: ...`，让读者一眼判断是否跑通。
- **Cite code with `file:line`.** 引用"为什么"时指向源码行（`policy_agent.py:113-114`），不要含糊叙述。
- **One `#`, many `##`.** 单个 H1；其余用 `##`/`###`，不要跳级。

## Step 5 — Use callouts correctly

The library uses Obsidian callouts heavily with fixed semantics. Pick by purpose:

| Purpose | Callout |
|---|---|
| Trap / pitfall / counter-example | `> [!warning]` |
| Explanation / supplementary detail | `> [!info]` or `> [!tip]` |
| Key conclusion / the one thing to remember | `> [!important]` |
| Methodology red-line (in 方法论沉淀 section) | `> [!abstract] 红线N：{title}` |
| Unverified / pending / not-yet-concluded | `> [!caution]` |
| Verified / confirmed working | `> [!success]` |

> [!caution] 推断 ≠ 结论
> Anything inferred but not yet verified by the user's actual measurement must go under `[!caution]` and be labelled as 推断/待验证. Do not present a hypothesis as a finding. This is the single most important rule — earlier notes failed by stating guesses as conclusions.

## Step 6 — Link related notes

优秀笔记是知识网络的节点，不是孤岛。每篇笔记有两类链接，都要有：

1. **结构回链**（面包屑页脚，Step 4 已写）— 指向本项目 MOC 与 `00_首页`，保证"任何笔记都能回到总览"。
2. **主题互链**（`## 关联笔记` 区）— 用 `- [[note name]] — {relationship}` 链接 1-2 条相关笔记并注明关系（因果/对比/前置/同主题）。`[[待创建]]（待创建）` 占位符留给那些应该存在但还没有的笔记。

To find candidates, recall the session's topics and the library's known hubs: `[[DDPM模型转换]]`（DDPM 项目总览）、`[[机器狗语音控制]]`、`[[Jetson部署]]`，加本次 session 触及的任何笔记。（`[[00_MOC]]` 是 `文档库/` 里 DDPM 那本书的总目录，不是项目 MOC——别链错。）新写的笔记也要回头更新它引用到的项目 MOC（在 MOC 的笔记地图里加一行指向新笔记），让双向链接真正闭环。

## 失败模式与兜底（写之前/写之中遇到的边角情况）

边角情况一律「先试合理默认 → 失败就问用户」，绝不静默猜测或静默覆盖。**与上方 🔴 检查点的区别**：🔴 管*何时问*（下笔前必须停下的决策门）；本表管*怎么处理*（遇到状况的兜底）——别当成两份重复清单。

| 触发条件 | 一线处理 | 仍失败 → 兜底（别静默） |
|---|---|---|
| **目标文件已存在**（Write 报 "File has not been read yet"） | Read 该文件 ≥1 行，判断是同主题延续还是撞名 | 同主题→追加章节并链回；撞名→问用户「覆盖 / 追加章节 / 改名」三选一 |
| **项目还没有文件夹** | 按 Step 1 第3问处理（新建 `项目-{名}/`+MOC 或归现有） | 用户暂不在→先不写，回复说明「需要先定项目归属」 |
| **要回链的项目 MOC 不存在** | 面包屑仍写预期 MOC 名 `[[{项目名}]]`，「关联笔记」标 `（待创建）` | 写完主动建一篇占位 MOC（标题 +「待补」），让双向链不悬空 |
| **文件名撞名 / 拿不准** | 按 🔴 #3 给 2-3 个带论点候选让用户选 | 用户不选→用「核心结论 + 关键变量」作默认名，并告知可改 |
| **一个 session 有 ≥2 个独立主题** | 按 🔴 #1 拆成多篇、各自拟标题+归属，问用户确认 | 用户坚持合一篇→遵从，但开头加两节目录 + `多主题` tag |
| **归属跨项目**（既是项目 debug 故事、又是可复用 config，如 Jetson 上跑 DDPM 转换遇到 LD_LIBRARY_PATH） | 写**项目 debug 笔记**为主，在对应 `系统配置/` 笔记里加一行链回/扩展，别把 debug 故事挪进 `系统配置/` | 用户明确要独立 config 笔记→遵从，两篇互链 |

## Rules

- **Read before Write.** If the target file already exists, Read at least 1 line first — the Write tool refuses to overwrite a file that was not read this session, with "File has not been read yet." Reading 1 line satisfies the check.
- **Keep only what's reusable.** Drop narrative journey ("first I tried… then I guessed…"). Keep commands, root causes, config values, line citations, and decisions. The next reader wants the answer, not the struggle.
- **No empty process dumps.** 某步没有可复用结论就省掉。短而实的笔记胜过灌水的长笔记。
- 原则 1（拆不要堆）/ 5（上下文自足）/ 7（推断标 caution）见上方 **Core principles** 与 Step 4/5，此处不重复。
- **Don't touch**: `.base` files、`.remember/`（gitignored session memory）、`.obsidian/workspace.json`。
- **Write only the `.md`.** 不要生成 `.html` 兄弟文件（那是另一个导出插件的事）。
- **Don't commit.** 用户用 github-sync 插件（`Ctrl+Shift+S`）自己同步，只写文件即可。

## 写书/文档的单独规则

写一本书或长篇文档时，笔记的原子化原则（结论前置/去水分/一篇一结论）**不适用**——书就该厚，靠多页 + 结构展开一个主题。规则：

1. **归位**：`文档库/{书名}/`，书名即文件夹名。例：`文档库/DDPM模型转换实战/`。
2. **总目录 `00_MOC.md`**：开头写「这本书给谁看 + 目标 + 阅读路径（mermaid 流程图）+ 目录表（链各章）+ 怎么用这本书」。这是书的入口，`type: moc`，加 `book: "{书名}"` 字段。
3. **章节**：`数字_标题.md`（`01_全景.md`、`02_精度实验.md`…），frontmatter 加 `prev: "[[{上一章}]]"` / `next: "[[{下一章}]]"` 串成阅读链；`type: book`。
4. **附录/公共资产**：术语表、桥接字典、环境清单等全书复用资产用 `A0_`/`A1_`… 前缀放书根。
5. **图片**：放书根 `assets/`，章节里用 `![[assets/xxx.png]]` 相对嵌入，命名 `章号_序号_描述.png`。
6. **教学手法尽情用**：七种 callout（🤔你先想/🔍来拆/✅验证/🛠️动手/⚠️陷阱/🌉桥梁/🏁里程碑）、mermaid 全景图、三级证据制（代码实证 file:line / 实跑验证 / 官方文档）、螺旋穿插（概念跨章重述是特性，不是水分）。**不要按笔记标准精简书**——长度是教学需要。
7. **配套项目**：书若服务于某项目，在该项目的 MOC 里加一行链到书的 `00_MOC`；书 `00_MOC` 末尾也链回项目 MOC，双向闭环。
8. **面包屑页脚**：书章节末尾 `📍 关联项目：[[{项目MOC}]] · 知识库入口 [[00_首页]]`（无关联项目则只 `📍 [[00_首页]]`）。

🔴 书是**大工程**（通常跨多 session），动笔前先和用户确认书名、目录结构、目标读者（见「必停检查点」#4）。

## When done

Print one line: the absolute path of the written file, followed by a single-sentence summary of what the note covers. Nothing else.

```
/mnt/d/知识库/项目-{项目名}/{子目录}/{filename}.md — {一句话内容摘要}
```
