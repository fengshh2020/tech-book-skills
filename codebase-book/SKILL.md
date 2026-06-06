---
name: codebase-book
description: "Use when generating a project-driven learning book from a codebase — architecture walkthrough, code-reading course, or how-this-project-works guide. Trigger on: repo with learning guide/book request, 生成项目书籍, 把代码库变成书, 架构学习指南. Do NOT trigger for: code review, README updates, API reference without book structure, single-file docs."
---

# Codebase Book

从代码库生成项目驱动的技术书籍。产出应教会读者项目如何运作、主要设计选择为什么存在、以及读者需要什么背景知识才能理解、修改和扩展代码。

## 核心约束

**书籍教会读者项目，而不是列出目录树**。每章的目标是"读完这章后读者能做什么之前做不到的事"。如果一章只是在描述文件里有什么，那不是书——那是文件索引。

**每个行为和设计断言都有源码证据**。说"这个函数处理错误"时必须标注文件路径和行号，并标注 V1-V4 验证等级。不确定的设计决策标注为 `[待确认]`，不能编造理由。为什么？代码库书籍的读者会去读源码验证——如果书里的描述和源码不一致，整本书的可信度都会受损。

**代码摘录从源文件复制**，不从记忆中重写。每个代码块必须标注源文件路径和行范围。为什么？凭记忆重写的代码经常和实际源码有细微差异，这些差异会误导读者。

**读者学习顺序优先于文件系统顺序**。章节组织应该遵循读者从零理解项目的认知路径，不是按 `src/` 目录结构排列。

## 引用文件

每个阶段开始前执行该阶段的读取指令。

| 阶段 | 必读文件 | 读取目标 |
|------|----------|----------|
| 启动 | `../shared/progress-protocol.md` | 运行发现和恢复协议 |
| 启动 | `../shared/agent-compatibility.md` | 路径变量 |
| 阶段 1 | `../shared/runtime-pruning.md` | 范围分层和停止条件 |
| 阶段 2 | `references/analysis-guide.md` | 源码分析方法 |
| 阶段 2 | `../shared/verification-levels.md` | V1-V4 验证等级 |
| 阶段 3 | `references/knowledge-expansion.md` | 章节规划和知识扩展 |
| 阶段 4 | `references/writing-guide.md` | HTML 写作和组件规范 |
| 阶段 4 | `../shared/quality-ownership.md` | 源码可追溯性责任 |
| 阶段 5 | `scripts/validate_output.sh` | 输出校验 |
| 阶段 5 | `../shared/report-templates.md` | 报告模板 |

## 运行状态

先执行共享进度协议，使用 run slug `codebase`。运行目录形如：

```text
.book-doc/runs/{YYYYMMDD}-codebase-{label}/
```

本 skill 的运行结构：

```text
{RUN}/
├── progress.md
├── codebase-map.md
├── analysis/
│   └── {module}.md
├── chapter-plan.md
└── report.md
```

生成的 HTML 写入 `output/`，除非用户指定其他目录。

幂等性检查：

- `codebase-map.md` 存在且列出了源文件/配置/测试文件及排除项。
- `analysis/{module}.md` 对每个核心路径模块和摘要支撑模块存在。
- `chapter-plan.md` 存在且包含源文件到章节的覆盖表。
- 已完成 HTML 页首行为 `<!-- generated: complete -->`；中断页面为 `<!-- generated: partial -->`，恢复时必须重做。
- `report.md` 记录验证结果和已知限制。

## 范围分层

**读取 `../shared/runtime-pruning.md`**。

发现阶段必须先为每个文件分配范围层级，再进行深度分析：

| 层级 | 含义 | 处理方式 |
|------|------|----------|
| 核心路径 | 入口、领域逻辑、编排、行为定义测试 | 深度分析，保留 file:line 证据 |
| 支撑路径 | 工具函数、适配器、配置等解释核心路径的文件 | 通读 + 关键行为摘要 |
| 参考路径 | 文档、示例、资源、生成或类 vendor 文件 | 通读确认分类正确，登记或链接 |

**所有文件都必须被读过，分层控制的是分析深度而非是否读取。** 参考路径文件仍需通读以确认分类正确——一个被误判为 vendor 的文件可能包含关键自定义逻辑。通读参考路径文件时只需确认"此文件确实不包含需要讲解的行为"即可，但不能跳过不读。

核心路径优先：先分析解释项目运作所需的最小文件集，再扩展到支撑材料。当新增文件不再改变架构图、章节计划、读者解释或源码覆盖表时停止**深度分析**——但停止深度分析不等于停止读取，所有未深度分析的文件仍需通读确认。

## 流程

```text
发现 → 分析 → 规划学习路径 → 生成 HTML → 校验
```

每个可恢复单元完成后更新 `progress.md`。

## 阶段 1：发现

目标：在写作前建立代码库全景。

1. 识别源文件、测试、配置、资源、文档、生成文件、构建/部署文件和类 vendor 文件。
2. 确定语言、框架、依赖管理、构建/测试命令、入口点和运行时假设。
3. 将每个相关文件分类为入口、核心模块、基础设施、工具、测试/规范、配置、资源、生成/vendor 或排除。
4. 分配范围层级：核心路径、支撑路径或参考路径。
5. 写入 `{RUN}/codebase-map.md`，包含目录树、文件分类、技术栈、入口点、依赖概览、范围层级和排除项。

关卡：每个相关源文件/配置/测试文件已被分类或明确排除并说明理由。

## 阶段 2：分析

**读取 `references/analysis-guide.md` 和 `../shared/verification-levels.md`**。

按依赖顺序和范围层级分析模块：

1. 入口点
2. 核心流程
3. 行为定义测试
4. 基础设施
5. 工具函数
6. 支撑/参考材料

每个分析模块写入 `{RUN}/analysis/{module}.md`，包含：

- 公共接口和行为契约
- 关键控制/数据流
- 源码支撑的设计决策（标注 V1-V4 验证等级）
- 依赖和被依赖关系
- 读者需要的隐含知识
- 测试作为行为规范
- 跳过或摘要的文件及理由（遵循 `../shared/progress-protocol.md` 阅读证据协议）

**参考路径和支撑路径文件的通读证据**（遵循 `../shared/progress-protocol.md`）：

每个被分类为参考/支撑路径的文件，analysis 中必须包含至少两项阅读证据：
- **结构证据**：文件行数、函数/类数量、导出接口数
- **内容摘要**：该文件的实际行为，不是文件名推断。如"此文件定义了 3 个工具函数：parse_config()、validate_env()、resolve_path()"可接受；"工具函数文件"不可接受
- **排除理由**：如果排除该文件，必须说明读过后确认了什么。如"已读 42 行，确认为自动生成的 protobuf 代码，无自定义逻辑"可接受；"vendor 文件，排除"不可接受

分析时必须执行的证据收集：

- **file:line 引用**：每个行为描述标注具体文件和行号范围。记录：`"错误处理流程: src/handler.py:45-62, V2 已读取确认"`
- **设计决策来源**：如果代码注释解释了设计选择，引用注释内容。如果没有注释，标注为推断（V4）并标记 `[待确认]`。
- **代码摘录锚点**：标记未来写作时需要引用的代码段位置。

关卡：
- 没有行为或设计断言缺少 file:line 证据或 V 标签
- 不编造理由；不确定的设计决策标注为 `[待确认]`
- 核心路径模块全部分析完毕、支撑/参考路径已摘要或明确推迟后，才进入章节规划

## 阶段 3：规划学习路径

**读取 `references/knowledge-expansion.md`**。

写入 `{RUN}/chapter-plan.md`，包含：

- 书籍受众和前置知识
- 按读者学习顺序排列的章节列表
- 每章覆盖的文件/函数/类
- 需引用的关键代码摘录（标注文件路径和行范围）
- 需解释的设计决策
- 知识扩展项目和深度
- 源文件到章节的覆盖表
- 推迟范围和理由

读者学习顺序优先于文件系统顺序：

1. 项目目的和快速上手
2. 架构和数据流
3. 核心抽象
4. 从基础到编排的模块
5. 测试、部署、扩展和常见陷阱

关卡：每个未排除的源文件出现在覆盖表或推迟范围列表中。

## 阶段 4：生成 HTML

**读取 `references/writing-guide.md` 和 `../shared/quality-ownership.md`**。

生成文件结构：

```text
output/
├── 00_cover.html
├── 01_toc.html
├── 02_quickstart.html
├── 03_architecture.html
├── NN_chapterM.html
├── style.css
└── script.js
```

每页生成时遵循：

- 已完成页首行：`<!-- generated: complete -->`
- 中断页面：`<!-- generated: partial -->`，恢复时重做
- 每段代码摘录必须从源文件复制，标注文件路径和行范围
- 按逻辑流分组解释代码，不做机械的逐行转录
- 知识框只在有助于理解当前代码时使用，不要把每个小事实放进独立框
- 不按文件系统结构组织章节，除非这恰好是最好的学习路径
- 最终 HTML 中不出现 `[待确认]`，除非用户要求保留开放问题

逐页关卡（每页完成后**在 progress.md 留下证据**）：

① 首行有 `<!-- generated: complete -->` 标记
② 代码摘录标注了源文件路径和行范围（记录具体引用：`ChN 引用: handler.py:45-62, parser.py:120-135`）
③ 导航链接指向存在的文件（记录验证：`导航: prev→Ch(N-1)✓ next→Ch(N+1)✓`）
④ 章节计划中该页对应项已覆盖
⑤ `report.md` 有推迟或不确定主题的记录（检查是否有"推迟"章节；如果没有，说明有静默省略，必须补充）

每页通过所有 5 项后更新 `progress.md`，再继续下一页。

## 阶段 5：校验

运行：

```bash
"${SKILL_DIR}/scripts/validate_output.sh" output/
```

当可行时，也运行项目特有的检查以验证示例或生成命令。

**读取 `../shared/report-templates.md`** 的 codebase-book 段，写入 `{RUN}/report.md`。

校验结果记录后才能将运行标记为 `completed`。

## 移交

完成后，review-tech-book 可通过最新 `*-codebase-*` 报告接续审阅：

- 源码覆盖表
- file:line 证据
- 代码摘录一致性
- `validate_output.sh` 结果
- 架构讲解完整性
- 学习路径合理性

## 质量标准

- 书籍教会读者项目，而不仅仅是目录树。
- 行为和设计断言基于源码、测试、文档或明确的推断标签。
- 读者能将每个主要解释追溯到代码。
- 范围剪枝可见、有理由、不隐藏核心行为。
- 最终 UI 连贯可读；组件密度支持理解而非碎片化文本。
