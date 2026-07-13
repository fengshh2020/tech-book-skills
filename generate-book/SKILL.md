---
name: generate-book
description: "Generate a unified technical book from one or more sources, or from a codebase. Single source: translate and produce Chinese HTML book. Multiple sources: deep-read, integrate, and produce one coherent book. Codebase: generate project mastery guide from source code. Trigger: generate book, 整合书籍, 生成书籍, merge books, combine sources, translate book, 翻译书籍, 生成项目书籍, codebase walkthrough, 掌握项目, 架构学习指南, codebase book, 代码库书籍. Do NOT trigger for: quality review only (use review-tech-book), code review, README, API reference."
---

# 生成书籍

从源书籍或代码库生成统一的技术书籍。输出必须读起来像一本书，而不是拼贴画。

## 核心规则

**先阅读以下两个文件**：
- `references/shared-rules.md` — 铁律、预检清单、标准关卡自检、反合理化表、反偷工减料规则、Gate 降级方案、错误恢复协议、进度追踪鲁棒性、失败模式识别、Coverage Guardian、质量标准、子 Agent 编排
- `shared/discipline-framework.md` — Gate 降级方案、错误恢复协议、进度追踪、反合理化表

关键原则：
- 没有新鲜阅读证据就不产出。不跳过 Gate。不只凭标题推断。不缩减内容。
- 每个阶段开始时重新阅读参考文件，在 progress.md 中记录确认
- Gate 要么通过要么失败，没有"大概"
- **启动前必须通过预检**（见 shared-rules.md「预检清单」）
- **每个子阶段的输出必须通过文件级验证**（存在、非空、大小合理、无占位符）
- **崩溃后从 progress.md 恢复**，不从头开始（见 shared-rules.md「错误恢复协议」）

## 🔴 反模式（等于失败，不要做）

命中即视为产出不合格。下面只列各模式特有的高危信号；铁律级通用红线（没读就写 / 跳过缩减 / 伪造 Gate / 占位符充数）已在上方「核心规则」与 `shared/anti-slacking.md`「防跳步检查」、`references/shared-rules.md`「失败模式识别」中列出，不在此重复。

- **拼贴 ≠ 整合**（多源）：把多本书的章节拼接在一起不叫整合；多源模式的读者必须无法辨识内容来源。
- **破坏段落映射**（单源）：源段落数 ≠ 目标段落数，合并 / 拆分段落，破坏 1:1 映射。
- **翻译腔**（单源）：照搬英文句式、被动堆叠、「进行了……的实现」（见 `shared/translationese-patterns.md`）。

## 模式选择

自动检测：1 个源 -> 单源模式，2+ 个源 -> 多源模式，代码库路径 -> 代码库模式。

| 模式 | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | 详细流程 |
|------|---------|---------|---------|---------|---------|----------|
| 单源 | 提取与阅读 | 翻译 | 组装 | 验证 | 报告 | `references/mode-single.md` |
| 多源 | 深度阅读 | 架构设计 | 章节生成 | 验证 | 报告 | `references/mode-multi.md` |
| 代码库 | 发现 | 分析 | 规划 | 生成 | 验证 | `references/mode-codebase.md` |

**进入任何阶段前**，阅读对应模式的详细流程文件，按其中的子阶段和关卡执行。

> 🔴 **CHECKPOINT · 启动前确认（STOP）**：自动检测出模式后、进入任何 Phase 之前**必须暂停向用户确认**，不要直接开跑——生成一本书耗时很长，模式或源判断错 = 整轮返工。逐项确认：🛑 检测到的模式（单源 / 多源 / 代码库）与用户意图一致 ｜ 🛑 源或代码库路径、输出目录 `{RUN}/`、目标语言无误 ｜ 🛑 预检已运行，结果全通过（或在此说明失败原因，见 `references/shared-rules.md`「预检清单」）。用户确认 OK 再继续；**用户拒绝 → 按反馈修改模式 / 源 / 语言后重新确认，不要硬跑**；模式拿不准让用户显式指定，别替它猜。

**阶段锁定**：进入任何阶段/子阶段前，运行 Gate 检查：
```bash
python scripts/workflow.py generate-book <run_dir> check_gate <phase> [<sub_phase>] [chapter]
```
Gate 失败则修复后重试。如果 workflow.py 不可用，使用手动 Gate 检查（见 shared-rules.md「Gate 检查降级方案」）。

**进度记录**：每个子阶段完成后运行：
```bash
python scripts/workflow.py generate-book <run_dir> record_progress --phase <N> --sub-phase <N.M> [--chapter <chapter>] --status completed
```
如果 workflow.py 不可用，直接在 progress.md 中手动追加记录（见 shared-rules.md「进度追踪鲁棒性」）。

## 单源模式概览

适用于恰好一个源书籍（EPUB 或 HTML）。翻译 + 组装为中文 HTML 书籍。

**流程**：提取源文件 -> 逐章阅读 -> 逐章翻译（1:1 段落映射）-> 术语一致性检查 -> 翻译腔扫描 -> HTML 组装 -> 验证 -> 报告

**关键要求**：自然的中文，无翻译腔；源段落数 = 目标段落数；代码注释翻译，逻辑不变。

详细步骤见 `references/mode-single.md`。

## 多源模式概览

适用于两个或更多源书籍。深度整合为一本连贯的书籍。

**流程**：逐书阅读 -> 知识索引生成（每本 >= 1000 行）-> 跨书籍分析 -> 架构设计 -> 逐章整合 -> Coverage Guardian 验证 -> 报告

**关键要求**：读者无法辨识内容来源；整合等级仅限 L3（重组）或 L4（完全融合）；反向覆盖矩阵 100%；Coverage Guardian 无底线违规。

详细步骤见 `references/mode-multi.md`。

## 代码库模式概览

适用于源代码库路径。生成项目精通指南。

**流程**：发现（分类文件）-> 分析（核心模块的接口/设计/算法/错误处理）-> 规划（按内容逻辑排序）-> 生成（叙事驱动 + 代码摘录）-> 验证

**关键要求**：每个论断需要 file:line 证据；核心章节 >= 20KB，概览 >= 10KB；代码:解释 >= 1:1；覆盖错误路径；设计决策有替代方案/权衡取舍；沿执行路径讲述连贯故事，不孤立罗列函数。

详细步骤见 `references/mode-codebase.md`。

## 输出结构

**MD 是信息主源**（[ADR-0001](../../docs/adr/0001-markdown-as-source-html-built.md)）。agent 在 `{RUN}/src/` 写 MD 章节 + `book.yml`，再运行 builder 渲染双格式：

```
{RUN}/
├── src/                         # ← agent 写这里（MD 主源）
│   ├── book.yml                 # 元数据（title/author/lang…）
│   ├── README.md                # （可选）MD 版目录
│   └── NN_*.md                  # 章节，NN >= 02（00/01 留给封面/目录）
├── output/                      # ← builder 产出（HTML 版）
│   ├── 00_cover.html  01_toc.html  NN_*.html
│   ├── style.css  script.js
│   └── diagrams/*.png           # mermaid → PNG
└── output-md/                   # ← builder 产出（可移植 MD 版，mermaid → png 嵌入）
```

运行：`python scripts/build_html.py {RUN}/src {RUN}/output`
作者约定见 `references/md-authoring.md`；HTML 组件契约见 `references/book-assembly.md`。

## 参考文件

| 文件 | 用途 | 适用模式 |
|------|------|----------|
| `references/shared-rules.md` | 铁律、预检、关卡自检、Gate 降级、错误恢复、进度追踪、输出验证、失败模式、Coverage Guardian、质量标准、Agent 编排 | 全部 |
| `references/mode-single.md` | 单源模式详细流程 | 单源 |
| `references/mode-multi.md` | 多源模式详细流程 | 多源 |
| `references/mode-codebase.md` | 代码库模式详细流程 | 代码库 |
| `references/agent-orchestration.md` | 子 Agent 规则和约束 | 单源/多源/代码库 |
| `references/knowledge-index-format.md` | 知识索引结构 | 多源 |
| `references/book-architecture.md` | 架构设计指南 | 多源 |
| `references/full-integration.md` | 整合等级和重写方法 | 多源 |
| `references/integration-discipline.md` | 整合纪律规则 | 多源 |
| `references/synthesis-methodology.md` | 内容合成方法 | 多源 |
| `references/quality-gate.md` | 质量关卡规范 | 多源 |
| `references/context-passing.md` | Agent 之间的上下文传递 | 单源/多源 |
| `references/translation-rules.md` | 翻译规则和指南 | 单源 |
| `references/md-authoring.md` | **MD 作者约定（务实子集）+ 组件映射** | 全部 |
| `references/book-assembly.md` | builder 产出的 HTML 组件契约（渲染目标，非手写） | 单源/多源/代码库 |
| `references/analysis-guide.md` | 模块分析方法指南 | 代码库 |
| `references/writing-and-content.md` | 写作与内容深度指南 | 代码库 |
| `references/writing-guide.md` | 写作风格指南 | 代码库 |
| `shared/translationese-patterns.md` | 翻译腔检测模式 | 单源 |
| `shared/anti-slacking.md` | 反偷工减料规则 | 全部 |
| `shared/report-templates.md` | 报告格式模板 | 全部 |
