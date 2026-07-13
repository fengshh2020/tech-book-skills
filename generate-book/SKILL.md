---
name: generate-book
description: "Generate a unified technical book, or a lightweight project learning doc, from one or more sources or a codebase. Product shape is chosen per run: 'book' = full multi-chapter HTML+MD book via builder; 'doc' = portable in-place MD (e.g. proj/book.md), no builder, trimmed gates. Single source: translate. Multiple sources: deep-read + integrate. Codebase: discover + analyze + generate. Trigger: generate book, 整合书籍, 生成书籍, merge books, combine sources, translate book, 翻译书籍, 生成项目书籍, codebase walkthrough, 掌握项目, 架构学习指南, codebase book, 代码库书籍, 项目学习文档, 学习指南, 生成 book.md, 项目文档, project guide, learning doc, walkthrough this project, 给这个项目生成文档. Do NOT trigger for: quality review only (use review-tech-book), code review, README, API reference."
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

命中即视为产出不合格。下面只列各模式特有的高危信号；铁律级通用红线（没读就写 / 跳过缩减 / 伪造 Gate / 占位符充数）已在上方「核心规则」与 `shared/discipline-framework.md`「防懈怠机制/防跳步检查」、`references/shared-rules.md`「失败模式识别」中列出，不在此重复。

- **拼贴 ≠ 整合**（多源）：把多本书的章节拼接在一起不叫整合；多源模式的读者必须无法辨识内容来源。
- **破坏段落映射**（单源）：源段落数 ≠ 目标段落数，合并 / 拆分段落，破坏 1:1 映射。
- **翻译腔**（单源）：照搬英文句式、被动堆叠、「进行了……的实现」（见 `shared/translationese-patterns.md`）。
- **doc 形态套 book 重型 gate**（任一模式 × doc）：对就地学习文档硬套 20KB 下限 / Coverage Guardian / builder 流水线——doc 形态用轻量 gate（见 `references/product-shapes.md`），但 file:line 证据 / 无翻译腔 / 整合 L3-L4 / 无占位符仍不可妥协。反过来：doc 形态下偷工（凭标题、缩内容、占位符）同样不合格。

## 模式选择

**源类型**（读什么）：自动检测——1 个源 -> 单源模式，2+ 个源 -> 多源模式，代码库路径 -> 代码库模式。

| 模式 | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | 详细流程 |
|------|---------|---------|---------|---------|---------|----------|
| 单源 | 提取与阅读 | 翻译 | 组装 | 验证 | 报告 | `references/mode-single.md` |
| 多源 | 深度阅读 | 架构设计 | 章节生成 | 验证 | 报告 | `references/mode-multi.md` |
| 代码库 | 发现 | 分析 | 规划 | 生成 | 验证 | `references/mode-codebase.md` |

**产品形态**（产什么，与源类型正交，详见 `references/product-shapes.md`）：

| 形态 | 适用 | 输出 |
|---|---|---|
| **book**（默认） | 正式书 / 多章系统学习 / 要发布 | `{RUN}/src` → builder → `output/` HTML + `output-md/` MD |
| **doc** | 项目学习文档 / 快速上手 / 单文件就地（如 `proj/book.md`） | 就地 MD，**无 builder**，轻量 gate |

判断：用户说"一本书 / 正式 / 发布 / 多章"→ **book**；说"学习文档 / 快速上手 / 单个 md / 就地生成"，或给了单个输出路径（如 `proj/book.md`）→ **doc**；拿不准问用户。任一源类型都可配任一形态（如代码库 × doc = 项目学习文档）。

**进入任何阶段前**，阅读对应模式的详细流程文件，按其中的子阶段和关卡执行。

> 🔴 **CHECKPOINT · 启动前确认（STOP）**：自动检测出源类型与产品形态后、进入任何 Phase 之前**必须暂停向用户确认**，不要直接开跑——生成耗时很长，判断错 = 整轮返工。逐项确认：🛑 源类型（单源 / 多源 / 代码库）与用户意图一致 ｜ 🛑 产品形态（book / doc）与用户意图一致——doc 形态尤其要确认输出路径（就地 `book.md` 还是 `{RUN}/` 工作区） ｜ 🛑 源或代码库路径、输出位置、目标语言无误 ｜ 🛑 预检已运行，结果全通过（或在此说明失败原因，见 `references/shared-rules.md`「预检清单」）。用户确认 OK 再继续；**用户拒绝 → 按反馈修改后重新确认，不要硬跑**；拿不准让用户显式指定，别替它猜。

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

### book 形态（默认）

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

运行：`python scripts/build_html.py {RUN}/src {RUN}/output`。作者约定（含 MD→HTML 组件映射）见 `references/md-authoring.md`。

### doc 形态

就地写 MD，**不走 builder、不生成 `book.yml`**。默认单文件（用户指定路径，如 `proj/book.md`）；内容明显需要多章时写 `NN_*.md` + 一个 `README.md` 目录。用 `#`/`##` 分节，顶部可选手写目录，mermaid 保留 ```` ```mermaid ```` 文本（GitHub/VS Code 原生渲染）。完整约定见 `references/product-shapes.md`。

## 参考文件

| 文件 | 用途 | 适用模式 |
|------|------|----------|
| `references/product-shapes.md` | **产品形态（book 全书 / doc 轻文档）选择 + doc 轻量 gate** | 全部 |
| `references/shared-rules.md` | 铁律、预检、关卡自检、Gate 降级、输出验证、失败模式、质量标准、Agent 编排要点 | 全部 |
| `references/mode-single.md` | 单源模式详细流程 | 单源 |
| `references/mode-multi.md` | 多源模式详细流程（含 context-passing 两文件协议） | 多源 |
| `references/mode-codebase.md` | 代码库模式详细流程 | 代码库 |
| `references/multi-read-architect.md` | 多源 Phase 0-1：深度知识索引格式 + 架构评估（跨书分析/目录/章计划模板） | 多源 |
| `references/multi-synthesis.md` | 多源 Phase 2-3：合成方法论 + 整合级别 L1-L4 + 门控 G1-G13 + Coverage Guardian | 多源 |
| `references/agent-orchestration.md` | 子 Agent 编排策略与 spawning 规格 | 单源/多源/代码库 |
| `references/translation-rules.md` | 翻译规则和指南 | 单源 |
| `references/md-authoring.md` | **MD 作者约定（务实子集）+ 组件映射** | 全部 |
| `references/analysis-guide.md` | 模块分析方法指南 | 代码库 |
| `references/writing-and-content.md` | 代码库写作与内容深度指南（叙事驱动/认知负荷/代码展示/sidebar） | 代码库 |
| `shared/discipline-framework.md` | 防懈怠/防跳步、Gate 降级、错误恢复、进度追踪、反合理化（原 anti-slacking 已并入） | 全部 |
| `shared/verification-levels.md` | 证据等级 V1-V4 定义与强制规则 | 全部 |
| `shared/translationese-patterns.md` | 翻译腔检测模式（正则源） | 单源 |
| `shared/report-templates.md` | 报告格式模板 | 全部 |
