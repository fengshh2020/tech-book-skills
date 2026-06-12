# 书籍架构评估协议（Book Architecture Assessment Protocol）

> 供 generate-book 阶段 1 使用。基于阶段 0 的深度知识索引，设计整合书籍的架构。
> 核心原则：架构设计必须建立在深入理解之上 —— 不理解材料就无法绘制蓝图。

## 适用场景

- 多本源书整合为一本新书，且没有明确的主干书籍。
- 主干书籍的目录需要大幅重组而非局部补充。
- 用户强调"最优章节设计"、"知识组织"或"骨架最重要"。
- 早期输出仅由大纲、简短讲义或样章组成，存在被误判为已完成书稿的风险。

## 前置条件

**阶段 0 的所有知识索引必须已通过门控检查。** 未通过阶段 0 门控不得进入阶段 1。

阶段 1 开始前，必须：
1. 完整阅读所有知识索引（不可只浏览摘要）
2. 在 `progress.md` 中记录阅读确认
3. 列出各书之间核心方法论差异（至少 3 点）

## 核心原则

**架构设计是基于知识索引的分析工作，而非目录拼接。** 每一章的存在、顺序和深度都必须有知识索引中的证据支撑。

**章节骨架是教学设计（Instructional Design），而非大纲重排。** 章节顺序必须服务于读者的认知依赖：先建立概念基础，再引入工具，再组织项目，最后推进到专题。

**源书覆盖度必须双向检查。** 仅证明"目标章节引用了某个知识点"不够；还必须反向检查每本源书的章节和主题：分配到目标章节、降级为侧边栏/附录、或明确排除 —— 三者必居其一。

**不要默认以最大或最权威的书为骨架。** 是否采用某本书作为骨架，必须由目标受众、学习路径、现代性、工程导向和章节依赖共同决定。

**每章仅承担一个主要认知负荷（Cognitive Load）。** 如果一章包含多个核心模型（例如资源模型、错误模型、并发模型、性能模型），应拆分。

## 阶段 1 的三项核心工作

### 工作项 1：跨书深度对比 [子阶段 1.2]

基于知识索引，完成以下对比分析（输出到 `cross-book-analysis.md`）：

#### 方法论差异分析 [子阶段 1.2.1]

对每个主要主题，分析各书的教学方法论差异：

```markdown
### Topic: [Topic Name]

| Dimension | [Source A] | [Source B] | [Source C] | Integration Choice | Rationale |
|-----------|------------|------------|------------|-------------------|-----------|
| Introduction style | [Problem-driven] | [Definition-first] | [Example-led] | [Which one] | [Why] |
| Teaching order | [A->B->C] | [B->A->C] | [C->A->B] | [Which one] | [Why] |
| Depth target | [Introductory] | [Intermediate] | [Advanced] | [Target depth] | [Why] |
| Unique value | [X] | [Y] | [Z] | [How to use] | [Why] |
| Teaching quality | [High/Med/Low] | [High/Med/Low] | [High/Med/Low] | — | — |
```

#### 深度对齐分析 [子阶段 1.2.2]

识别同一主题在不同书籍中的深度差异：

```markdown
### Depth Alignment Table

| Topic | [Source A] Depth | [Source B] Depth | Target Depth | Alignment Strategy |
|-------|-----------------|-----------------|--------------|-------------------|
| [Topic 1] | Introductory | Advanced | Intermediate | A for foundation + B for depth |
| [Topic 2] | Intermediate | Introductory | Intermediate | Primarily A; B supplements introductory perspective |
```

对齐策略选项：
- **基础 + 深化（Foundation + Deepening）**：较浅的书提供基本框架；较深的书提供进阶内容。
- **优势互补（Strength Complement）**：一本书的优势弥补另一本书的不足。
- **独立视角（Independent Perspective）**：保留不同书籍的独特视角作为侧边栏。
- **重新设计（Redesign）**：两者均不满意；从头设计该主题的教学路径。

#### 边界互补分析 [子阶段 1.2.3]

识别各书知识边界的互补关系：

```markdown
### Boundary Complementarity Table

| Topic | [Source A] Boundary | [Source B] Boundary | Complementarity |
|-------|--------------------|--------------------|----------------|
| [Topic 1] | Stops at X | Starts from X, goes to Y | A->B natural continuation |
| [Topic 2] | No practical coverage | Practice-oriented | A for concepts + B for practice |
```

#### 风格冲突解决 [子阶段 1.2.4]

识别风格差异并制定解决策略：

```markdown
### Style Resolution Table

| Style Dimension | [Source A] | [Source B] | Unified Style | Resolution Method |
|----------------|------------|------------|--------------|-------------------|
| Person | "We" | "You" | [Choice] | [How to unify] |
| Terminology | English + Local | Local only | [Choice] | [How to unify] |
| Code comments | Local language | English | [Choice] | [How to unify] |
| Code block length | 5-10 lines | 15-30 lines | [Choice] | [How to unify] |
```

### 工作项 2：目标目录设计 [子阶段 1.3]

基于跨书对比分析，设计整合目录结构。

**设计步骤**：
1. 确定目标受众和使用场景
2. 确定主干来源（不一定是某本源书的原始目录）
3. 按认知依赖排序章节
4. 每章分配一个主要认知负荷
5. 检查覆盖完整性

**输出**：

```markdown
## Target TOC

### Part X: [Part Name]

#### Chapter N: [Chapter Title]
- **Capability objective**: What the reader can do after completing this chapter
- **Prerequisite concepts**: What must be understood first
- **Primary cognitive load**: The core learning point of this chapter (only one)
- **Source coverage**:
  - [Source A] Ch[X]: [What content it contributes]
  - [Source B] Ch[Y]: [What content it contributes]
- **Methodology choice**: [Which book's teaching method is chosen and why]
- **Depth target**: [Introductory / Intermediate / Advanced]
```

### 工作项 3：逐章整合计划 [子阶段 1.4]

为目标章节的每一章编写详细整合计划，输出到 `plan.md`。这是阶段 2 的执行指南。

**每章的整合计划必须自包含（Self-Contained）** —— 阶段 2 执行时不应需要重新读取其他文件（除非按需查阅知识索引中的特定章节）。

```markdown
## Chapter N Integration Plan

### Basic Information
- Chapter title:
- Capability objective:
- Prerequisite concepts (referencing preceding chapters):
- Estimated output length:
- Estimated code examples:

### Source Mapping
| Source | Chapter | Role | Contributed Content | Usage Method |
|--------|---------|------|---------------------|--------------|
| [Source A] | Ch[X] | Main narrative | [Core narrative framework] | Take its teaching path and analogies |
| [Source B] | Ch[Y] | Reinforcement | [In-depth content] | Supplement principles and boundary conditions |
| [Source C] | Ch[Z] | Reference | [Practical advice] | Convert into "common pitfalls" paragraphs |

### Methodology Choice
- Introduction style: [Choice] — Rationale: [Based on what evidence in the knowledge indexes]
- Teaching strategy: [Choice] — Rationale: [...]
- Cognitive progression path: [X -> Y -> Z] — Rationale: [...]

### Depth Alignment Strategy
- Target depth: [Level]
- [Source A] content needs: [Maintain / Deepen / Simplify]
- [Source B] content needs: [Maintain / Deepen / Simplify]
- Gap content: [What needs to be newly written]

### Content Synthesis Plan
Section by section:

#### [N.1 Section Title]
- Narrative source: [Primarily from which part of which book]
- Supplementary content: [What to supplement from other books]
- New content: [What needs to be written from scratch]
- Code examples: [Which example to use, from where, whether modification is needed]
- Integration level: [L3 Reorganization / L4 Full Fusion]

#### [N.2 Section Title]
...

### Concept Bridging
- Transition from the previous chapter: [How to bridge from the preceding chapter]
- Internal bridging concepts: [Whether bridging content is needed between sections]
- Setup for the next chapter: [How this chapter's ending creates a cognitive need for the next chapter]

### Terminology Conventions
| English | Unified Translation | First Appears In |
|---------|-------------------|-----------------|
| ... | ... | Chapter N / Chapter M |

### Style Baseline Example
[Quote 1-2 paragraphs from the primary book as a style reference]

### Quality Expectations
- Knowledge points covered: [N]
- Code examples: [N]
- Estimated word count: [N]
- Integration markers: [Estimated N `<!-- integrated -->` markers]
```

## 输出：source-architecture.md [子阶段 1.6]

必须包含以下章节：

1. **目标受众和使用场景**：现有基础、阅读目的、工作应用方式，以及明确声明的超出范围的内容。
2. **逐书画像（Per-Book Portraits）**：基于知识索引的每本源书画像（角色、优势、局限、推荐整合策略）。
3. **跨书对比分析摘要**：核心方法论差异、深度对齐方案、边界互补性、风格解决方案。
4. **统一知识图谱（Knowledge Graph）**：主题节点、前置依赖、下游能力、难度级别、实践产出。
5. **目标目录设计**：部分、章节、每章能力目标、前置概念、源书覆盖。
6. **反向覆盖矩阵（Reverse Coverage Matrix）** [子阶段 1.5]：源书章节/主题到目标章节/侧边栏/附录/排除理由的映射。
7. **排除和降级范围**：不进入正文的内容、原因，以及是否放入附录或未来路线图。
8. **骨架自检**：覆盖度、依赖关系、粒度、项目主线（Project Thread）、进阶主线（Advanced Thread）、风格统一风险。

## 源书画像维度（基于知识索引）

| 维度 | 检查来源 |
|------|---------|
| 学习路径 | 知识索引 -> 整体教学理念 -> 认知递进策略 |
| 概念深度 | 知识索引 -> 逐章深度校准 -> 深度级别 |
| 现代性 | 知识索引 -> 元信息 -> 语言/框架版本 |
| 工程导向 | 知识索引 -> 逐章内容覆盖 -> 工程实践覆盖 |
| 代码密度 | 知识索引 -> 逐章代码示例盘点 |
| 独特价值 | 知识索引 -> 逐章独到见解 |
| 排除风险 | 知识索引 -> 逐章深度校准 -> 边界 |
| 整合适配度 | 知识索引 -> 整合就绪摘要 |

## 目标目录自检 [子阶段 1.3]

```
[ ] Does each chapter have only one primary cognitive load?
[ ] Does each chapter have clearly defined prerequisite concepts and output capabilities?
[ ] Has every core topic from the source books been accounted for: main narrative / sidebar / appendix / excluded?
[ ] Are advanced topics avoided before foundational models are established?
[ ] Is there a running project thread to help readers combine knowledge?
[ ] Is engineering practice placed where it is usable, rather than relegated to a final appendix?
[ ] Is there a record of why a particular source book's original TOC was not adopted?
[ ] Are outline drafts, short lecture notes, or sample chapters never marked as completed manuscripts?
[ ] Is every chapter integration plan self-contained?
[ ] Does every chapter integration plan have evidence-supported methodology choices?
[ ] Have all cross-book methodology differences been analyzed with integration choices made?
```

## 常见失败模式

| 失败模式 | 症状 | 修复方式 |
|---------|------|---------|
| 最大书偏差（Largest-Book Bias） | 默认以最大/最权威的源书为骨架 | 先做跨书对比分析；由目标受众匹配度决定 |
| 覆盖度幻觉（Coverage Illusion） | 只检查目标知识点是否被映射；未检查源书章节是否遗漏 | 增加反向覆盖矩阵 |
| 粒度过粗 | 一章塞入多个核心模型 | 按认知负荷拆分章节 |
| 缺少项目主线 | 每章都是纯概念；读者不知道如何综合运用 | 设计阶段项目和综合项目（Capstone Project） |
| 过早完成 | 大纲或简短讲义被报告为已完成的书 | 明确标记为架构草稿；禁止标记为"已完成" |
| 专题污染 | 性能、并发或框架细节过早打断基础路径 | 拆分为核心路径、支撑路径和进阶路径 |
| 空洞整合计划 | 计划只说"将 X 整合到 Y"而无方法论 | 每个整合决策必须有知识索引证据支撑 |
| 缺少风格解决 | 源书之间的风格差异被忽略 | 必须完成风格冲突解决分析 |
