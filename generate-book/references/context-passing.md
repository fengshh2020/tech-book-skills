# 上下文传递协议（Context Passing Protocol）

LLM 在长工作流的跨阶段中会丢失上下文。本协议通过结构化的阶段摘要和进度文件解决此问题。

所有文件位于当前运行目录 `.book-doc/runs/{id}/` 下。

## 两个文件，两个职责

| 文件 | 职责 | 谁写入 | 谁读取 |
|------|------|--------|--------|
| `progress.md` | 进度跟踪：哪些阶段/章节已完成，从哪里恢复 | 每个步骤完成后更新 | 恢复时读取以确定从哪里继续 |
| `context-summary.md` | 知识传递：跨阶段的关键发现和决策 | 每个（子）阶段完成后追加 | 下一阶段开始时读取以获取上下文 |

**`progress.md` 回答"我们到了哪里"**，**`context-summary.md` 回答"我们知道了什么"**。两者互补，不可互相替代。

## 核心原则

在每个子阶段结束时，向 `context-summary.md` 追加一个章节（每个章节 <=150 行）。当下一个子阶段开始时，**只需读取此摘要 + 当前子阶段的参考文件**；无需重新读取先前子阶段的完整输出。

## 子阶段上下文跟踪

每个子阶段完成时向 `context-summary.md` 追加一个结构化章节。这确保了即使在同一阶段内也能保持细粒度的知识连续性。

### 阶段 0 子阶段

| 子阶段 | 说明 | 贡献的上下文 |
|--------|------|------------|
| 0.1 | 书籍盘点（Inventory） | 源书路径、章节数、文件格式、总体范围 |
| 0.2 | 逐书阅读 | 每章阅读证据：段落数、代码块数、特定术语 |
| 0.3 | 索引生成 | 每本书的知识索引（教学理念、深度校准、整合就绪度） |
| 0.4 | 覆盖度对比 | 跨书的主题重叠、缺口、独特贡献、深度差异 |
| 0.5 | 门控 0 | 验证：所有索引 >=1000 行、阅读证据完整、覆盖度对比已完成 |

### 阶段 1 子阶段

| 子阶段 | 说明 | 贡献的上下文 |
|--------|------|------------|
| 1.1 | 加载所有索引 | 每本书的阅读确认、关键发现、方法论差异（>=3 点） |
| 1.2 | 跨书分析 | 方法论差异、深度对齐、边界互补性、风格解决 |
| 1.3 | 目标目录设计 | 每章认知负荷、前置条件、能力产出、方法论选择 |
| 1.4 | 逐章计划 | 自包含的整合计划：源映射、合成策略、概念桥接 |
| 1.5 | 反向覆盖 | 100% 源书章节处置：正文 / 侧边栏 / 附录 / 排除 |
| 1.6 | 门控 1 | 验证：所有计划完成、无待定项、反向覆盖 100% |
| 1.4 | 方法论决策 | 关键方法论决策，每个选择的证据 |
| 1.5 | 排除与范围 | 排除范围，降级理由 |
| 1.6 | 计划统计与定稿 | 整合计划统计，预估增量 |

### 阶段 2 逐章子阶段

| 子阶段 | 说明 | 贡献的上下文 |
|--------|------|------------|
| 2.1 | 章节计划审阅 | 章节特定的源映射、方法论选择 |
| 2.2 | 内容合成 | 草稿长度、整合标记放置、代码块数量 |
| 2.3 | 自审与门控检查 | 门控结果（G1-G6）、发现的问题及解决方案 |
| 2.4 | 章节完成记录 | 最终长度、所有门控通过、备注 |

每个逐章子阶段追加章节特定的上下文，使后续章节能够引用前面章节做出的决策，而无需重新读取完整输出。

## 各阶段摘要格式

### 阶段 0 子阶段完成 -> 追加到 `context-summary.md`

每个子阶段（0.1-0.5）追加各自的章节。阶段 0 的完整贡献如下：

```markdown
# Deep Reading Summary

## Source Book Overview
- [Source Book 1]: [N] chapters, index [M] rows, role [mainline/reinforcement/specialty/reference]
- [Source Book 2]: [N] chapters, index [M] rows, role [...]
- [Source Book 3]: [N] chapters, index [M] rows, role [...]

## Per-Book Core Methodology
- [Source Book 1]: [one-sentence summary of teaching approach]
- [Source Book 2]: [one-sentence summary of teaching approach]
- [Source Book 3]: [one-sentence summary of teaching approach]

## Key Findings
- [Important insights discovered during reading, e.g.: Book A and Book B have fundamentally different methodologies on topic X]
- [...]

## Style Baseline Points
- [Summary of each book's style characteristics, for later style harmonization]

## Potential Integration Challenges
- [Expected difficulties during integration]
```

各子阶段贡献：

- **子阶段 0.1** 追加：源书概览（Source Book Overview）
- **子阶段 0.2** 追加：逐书核心方法论（Per-Book Core Methodology）
- **子阶段 0.3** 追加：关键发现（Key Findings）
- **子阶段 0.4** 追加：风格基线要点（Style Baseline Points）
- **子阶段 0.5** 追加：潜在整合挑战（Potential Integration Challenges）

### 阶段 1 子阶段完成 -> 追加到 `context-summary.md`

每个子阶段（1.1-1.6）追加各自的章节。阶段 1 的完整贡献如下：

```markdown
## Architecture Design Summary

### Target Reader
- Assumptions: ...
- Use cases: ...

### Per-Book Role
- [Source Book 1]: [mainline/reinforcement/specialty/excluded], rationale...
- [Source Book 2]: [mainline/reinforcement/specialty/excluded], rationale...

### Final Skeleton
- Volumes: [list]
- Core path: [chapter range]
- Support path: [chapter range]
- Advanced path: [chapter range]

### Key Methodology Decisions
- [Topic A]: chose [Source Book X]'s methodology, because [rationale]
- [Topic B]: redesigned, because [rationale]

### Exclusion Scope
- [Topic]: exclusion/downgrade rationale

### Integration Plan Statistics
- Total chapters: [N]
- New chapters: [list]
- Estimated increment: [N] lines
```

各子阶段贡献：

- **子阶段 1.1** 追加：目标读者（Target Reader）
- **子阶段 1.2** 追加：逐书角色（Per-Book Role）
- **子阶段 1.3** 追加：最终骨架（Final Skeleton）
- **子阶段 1.4** 追加：关键方法论决策（Key Methodology Decisions）
- **子阶段 1.5** 追加：排除范围（Exclusion Scope）
- **子阶段 1.6** 追加：整合计划统计（Integration Plan Statistics）

### 阶段 2 逐章完成 -> 追加到 `progress.md`

```markdown
## Ch[N] Completion Record
- Completed at: YYYY-MM-DD HH:MM
- Gate results: G1-G6 [pass/pass/pass/pass/pass/pass]
- Integration markers: [N]
- Code blocks: [N]
- Chapter length: [N] lines
- Notes: [if issues arose, record how they were handled]
```

阶段 2 逐章子阶段上下文追加到 `context-summary.md`：

```markdown
## Ch[N] Context
- Source mapping: [which source books contributed, roles]
- Methodology applied: [which teaching approach, with evidence]
- Key decisions: [chapter-specific methodology or content choices]
- Cross-references: [terms/concepts bridging to other chapters]
```

每章的各子阶段贡献：

- **子阶段 2.1** 追加：源映射和方法论选择
- **子阶段 2.2** 追加：草稿统计（长度、标记、代码块数）
- **子阶段 2.3** 追加：门控结果和问题解决方案
- **子阶段 2.4** 追加：最终完成记录

### 阶段 3 完成 -> 追加到 `context-summary.md`

```markdown
## Validation Results Summary
- Coverage: [N]%
- Terminology consistency: [pass / issue count]
- Code runnability: [N/M passed]
- Style consistency: [pass / issue count]
- Known limitations: [list]
```

## 读取规则

所有路径相对于当前运行目录 `.book-doc/runs/{current-run-id}/`。

| 阶段 | 必读 | 按需读取 |
|------|------|---------|
| 启动 / 恢复 | `progress.md` | -- |
| 0.1 | `progress.md` | `references/knowledge-index-format.md` |
| 0.2-0.5 | `progress.md` + `context-summary.md`（先前子阶段） | `references/agent-orchestration.md` |
| 1.1 | `progress.md` + `context-summary.md`（阶段 0 章节） | 所有知识索引 |
| 1.2-1.6 | `progress.md` + `context-summary.md`（阶段 0-1，先前子阶段） | 所有知识索引，`references/book-architecture.md` |
| 2.1 | `progress.md` + `context-summary.md`（阶段 0-1 章节）+ 当前章节的 `plan.md` 章节 | 相关知识索引章节 |
| 2.2-2.4 | `progress.md` + `context-summary.md`（阶段 0-1 + 先前章节章节）+ 当前章节的 `plan.md` 章节 | `references/full-integration.md` |
| 3 | `progress.md` + `context-summary.md`（完整） | `references/quality-gate.md` |
| 4 | `progress.md` + `context-summary.md`（完整） | `../shared/report-templates.md` |

关键规则：启动任何子阶段时，读取所有先前子阶段（同一阶段和更早阶段）产出的 `context-summary.md` 章节，以保持连续性。不要重新读取先前子阶段的原始输出。

## 阶段 2 的自包含指令块

阶段 2 的每章执行都是自包含的：整合指令包含章节所需的全部信息，无需重新读取其他文件。`plan.md` 中每章的指令块应包含：

1. 当前章节状态（现有内容和结构）
2. 源映射（哪些源书贡献什么内容，各自角色）
3. 方法论选择（选择哪本书的教学方法，附证据）
4. 深度对齐策略（目标深度，各源内容如何对齐）
5. 内容合成计划（逐小节指令）
6. 风格基线样例（主干书籍原文 1-2 段）
7. 相关术语约定（本章涉及的术语）
8. 概念桥接（与前章的衔接、内部桥接、为后章的铺垫）

**知识索引按需读取**：`plan.md` 中的源映射指示需要读取哪些知识索引的哪些章节。阶段 2 执行时按需读取，而非预先全部加载。
