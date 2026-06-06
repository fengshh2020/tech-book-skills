---
name: integrate-books
description: "Use when merging/synthesizing content from multiple technical books into one main book. Trigger on: 整合多本书, 补充源书到主书, merge books, enrich chapters, combine sources. Do NOT trigger for: translating a single book (use translate-book), quality review (use review-tech-book), single-file edits, or content not from another book."
---

# Integrate Books

将多本同领域技术书籍的核心知识整合到一本主书中，产出内容更完整、深度更均衡、风格一致的新版本。

## 核心约束

**整合后必须像一本书，而不是多本书的摘录拼接**。读者不应能分辨出哪些段落来自哪本书——如果读者能看出来，说明风格适配和去重没做好。这是整合失败的标志。

**每条新增知识都有三个属性**：来源（哪本书哪个章节）、位置（放在主书哪里）、读者收益（读者看了之后能做什么之前做不到的事）。缺少任意一个属性的新增内容是冗余。

**重复内容必须合并或交叉引用**。如果同一个概念在两章都有完整讲解，读者会被迫读两遍同样的东西。合并时保留更完整或更清晰的版本，另一个改为交叉引用。

**风格必须适配主书基线**。从源书摘录的段落不能保留源书的语气、用词密度和叙述节奏——必须改写为主书的风格。具体方法见 `references/synthesis-methodology.md`。

## 引用文件

每个阶段开始前执行该阶段的读取指令。

| 阶段 | 必读文件 | 读取目标 |
|------|----------|----------|
| 启动 | `../shared/progress-protocol.md` | 运行发现和恢复协议 |
| 启动 | `../shared/runtime-pruning.md` | 运行时剪枝和停止条件 |
| 启动 | `../shared/agent-compatibility.md` | 路径变量 |
| 阶段 1 | `references/knowledge-entry-format.md` | 知识点条目格式 |
| 阶段 2 | `references/integration-discipline.md` | 去重、来源、风格适配规则 |
| 阶段 2 | `../shared/verification-levels.md` | V1-V4 验证等级 |
| 阶段 3 | `references/synthesis-methodology.md` | 叙事整合方法 |
| 阶段 3 | `references/context-passing.md` | 阶段间上下文传递 |
| 阶段 4 | 当前章的 plan.md 指令块 | 整合指令 |
| 阶段 4 | `../shared/quality-ownership.md` | 整合阶段质量责任 |
| 阶段 5 | `scripts/check_coverage.sh` | 覆盖率校验 |
| 报告 | `../shared/report-templates.md` | 报告模板 |

## 运行状态

先执行共享进度协议，使用 run slug `integrate`。运行目录形如：

```text
.book-doc/runs/{YYYYMMDD}-integrate-{label}/
```

本 skill 的关键状态：

- run 目录内：`progress.md`、`context-summary.md`、`plan.md`、`report.md`
- 跨轮次知识库：`.book-doc/knowledge_base/`
- 主书输出：默认 `output/`，除非用户指定

幂等性检查：

- 阶段 1：`.book-doc/knowledge_base/` 下源书知识点文件与 `progress.md` 源书列表一致。
- 阶段 2：`.book-doc/knowledge_base/INDEX/dsp_mapping.md` 和 `gaps.md` 存在。
- 阶段 3：当前 run 的 `plan.md` 存在，且每章指令自包含。
- 阶段 4：目标 HTML `<head>` 含 `<!-- integrated: ... -->` 标记，且标记覆盖计划中的知识点 ID。
- 阶段 5：当前 run 的 `report.md` 存在且记录校验结果。

## 模式

### 全量整合

用于多本源书整合到主书。执行完整五阶段流程，建立全书知识库、冲突映射、逐章计划和最终校验。

### 快速模式

用户明确指定源书和目标章节，或使用"补充""添加"且范围限定时启用快速模式。

快速模式缩小的是修改范围，不是阅读范围。为了发现新增内容与主书已有内容的冲突，快速模式仍需通读主书和源书的相关内容：

- 阶段 1：通读源书全部内容提取知识点，但只为目标章节建立详细条目。
- 阶段 2：通读主书全部内容，检测目标章节知识点与主书已有内容的术语冲突、概念重叠和视角差异。不建立全书映射表，但冲突检测结果不能省略。
- 阶段 3：只制定目标章节指令。
- 阶段 4：只修改目标章节。
- 阶段 5：校验目标章节 + 主书相邻章节的术语和风格一致性。

仍需在 `progress.md` 记录跳过条件、源书范围、目标章节和通读范围。

## 流程

```text
Extract Knowledge → Map Conflicts → Plan Integration → Apply Chapter Changes → Validate → Report
```

每阶段结束写 `context-summary.md`（≤120 行）并更新 `progress.md`。下阶段只读 `progress.md`、`context-summary.md` 和当前阶段必要参考文件。

## 阶段 1：提取知识

**读取 `references/knowledge-entry-format.md`**。

目标：从源书提取可追踪知识点。

1. 查找最新 completed 的 `*-translate-*` 报告；若源书仍是 EPUB，先要求 translate-book 或经用户确认后从英文提取并在阶段 4 翻译表达。
2. 为每本源书在 `.book-doc/knowledge_base/` 下创建子目录。
3. 按知识点条目格式每章提取 5-15 个知识点。判断标准：读者未来会独立查找、引用或迁移这个知识点吗？如果不会，它可能不是独立知识点。
4. 运行：

```bash
"${SKILL_DIR}/scripts/check_coverage.sh" .book-doc/knowledge_base/ output/ stage1
```

关卡：所有目标源书章节已提取或明确排除，覆盖统计已写入，`context-summary.md` 已更新。

**阅读证据**（遵循 `../shared/progress-protocol.md`）：提取知识点时必须逐章打开源文件阅读，不允许凭目录或标题推断内容。每章提取记录中必须包含结构证据（该章节的段落数或核心概念数），作为已实际阅读的证明。

## 阶段 2：映射冲突

**读取 `references/integration-discipline.md` 和 `../shared/verification-levels.md`**。

目标：识别术语冲突、内容重叠、覆盖缺口和风格基线。

1. 交叉比对知识点，标记术语冲突、重复概念、视角差异。
2. 写 `.book-doc/knowledge_base/INDEX/dsp_mapping.md`，将主书章节映射到知识点 ID。
3. 写 `.book-doc/knowledge_base/INDEX/gaps.md`，记录主书有源书无、源书有主书无和处置决策。
4. 通读主书全部章节，基于通读结果从不同位置（前/中/后）各提取 2-3 段作为风格基线样本。风格基线需要记录：平均句长、术语密度、叙述节奏（先概念后示例 vs 先示例后概念）、技术深度预期、风格是否跨章节变化。

关卡：术语冲突有统一方案，覆盖缺口有处置决策，知识库条目映射率是否 ≥95% 的风险已记录。

## 阶段 3：规划整合

**读取 `references/synthesis-methodology.md` 和 `references/context-passing.md`**。

目标：生成逐章可执行整合指令。

对主书每章制定指令：新增、替换、改写、新增边栏或不处理。

每章指令必须包含：

- 知识点 ID 列表（来自阶段 1-2 的映射）
- 目标位置（在主书哪一段之后插入，或替换哪一段）
- 整合方式（新增/替换/改写/边栏）
- 来源证据（源书原文摘录）
- 术语约定（使用统一术语表中的哪个译法）
- 风格适配要求（参照风格基线的哪些特征）
- 去重说明（与主书已有内容的重叠部分如何处理）

写当前 run 的 `plan.md`。

关卡：每章指令自包含（不需要回头查阶段 1-2 的文件就能执行），净增量估算完成，非处理章节有跳过理由。执行阶段完成协议。

## 阶段 4：执行章节修改

对每章：

1. 读取 `plan.md` 当前章指令块、目标 HTML、必要知识点条目。
2. 执行新增/替换/改写/边栏。改写时参照阶段 2 的风格基线调整语气和节奏。
3. 写入整合标记：

```html
<!-- integrated: [源书]Ch3-[知识点ID], [源书]Ch5-[知识点ID] -->
```

4. 更新学习目标、代码清单编号、跨章链接。

每章修改完成后立即执行去重验证（不能跳到下一章）。去重验证**必须在 progress.md 留下证据**：

- **重复检测**：读取修改后的 HTML，搜索同一概念的完整讲解是否出现两次。记录：`ChN 去重: "生成器" Ch7行120 + Ch9行340 → 合并为交叉引用` 或 `ChN 去重: 0重复`。
- **风格一致性**：检查新增段落与前后文的语气、深度和术语是否一致。记录：`ChN 风格: 新增段落句长均值28字 vs 基线25字, 可接受`。
- **代码标注**：检查新增代码块的验证等级标注（V1-V3），无标注则补上。记录：`ChN 代码: 新增3块, V2标注完成`。

关卡（读取修改后 HTML 逐项确认并留证据）：
① 整合标记覆盖 plan.md 中所有知识点 ID
② 无重复完整讲解（去重证据已记录）
③ 新增代码标注 V1-V3
④ 术语与统一术语表一致
⑤ progress.md 已更新（含具体证据）

## 阶段 5：校验

运行：

```bash
"${SKILL_DIR}/scripts/check_coverage.sh" .book-doc/knowledge_base/ output/ stage5
```

再执行：

- 术语一致性全量校验。
- 代码块可运行性验证覆盖所有修改过的章节（不能只抽查部分章节）。
- 连续阅读 3 章检查风格一致性、重复度和拼贴感。
- 对照 `plan.md` 确认每个目标知识点有处置。

覆盖率低于 95% 必须修复后重跑，不能只写警告。

所有失败项必须修复或写入已知限制。

## 阶段 6：报告

**读取 `../shared/report-templates.md`** 的 integrate-books 段。

在当前 run 写 `report.md`。

完成后将 `progress.md` 状态改为 `completed`。

## 质量标准

- 整合后的书像一本书，而不是多本书摘录拼接。
- 每条新增知识都有来源、位置和读者收益。
- 重复内容被合并或交叉引用，不让读者反复读同一解释。
- 输出可被 review-tech-book 通过 `.book-doc/runs/*-integrate-*/report.md` 接续审阅。
