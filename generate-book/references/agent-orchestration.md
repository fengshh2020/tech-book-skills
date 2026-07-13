# 子 Agent 编排协议（Sub-Agent Orchestration Protocol）

> 适用于 generate-book 的所有阶段。定义子 Agent 的并发控制、依赖排序、错误恢复和进度跟踪。
> 核心问题：LLM Agent 的并行能力有限（通常 3-5 个），基于 Web 的源书存在链接/引用顺序依赖，无约束的执行会导致资源争用和上下文丢失。

## 全局约束

| 约束 | 值 | 理由 |
|------|-----|------|
| 最大并发 Agent 数 | **5** | 平衡速度与资源 |
| 单 Agent 超时 | 10 分钟 | 防止 Agent 挂起 |
| 失败重试次数 | **1** | 同样的方式失败两次 = 方法有误 |
| 单 Agent 上下文限制 | ~50k tokens | 避免过多上下文导致质量下降 |

## 各阶段编排策略

### 阶段 0：深度阅读（Deep Reading）

**目标**：为每本书生成 >=1000 行的知识索引（Knowledge Index）。

**编排模式**：每本书一个 Agent，书内章节按顺序执行。

#### 子阶段编排

| 子阶段 | Agent 模式 | 说明 |
|--------|-----------|------|
| 0.1 | 单 Agent | 清单盘点（Inventory）—— 扫描所有源书，记录元数据（标题、章节数、格式），确定处理顺序。输出：清单文件 `.book-doc/inventory.md`。 |
| 0.2 | 每本书一个 Agent，最多 3 个并行 | 深度阅读 —— 每个 Agent 按严格顺序逐章阅读一本书，每章写完中间进度。书内章节串行；跨 Agent 最多 3 本书并行处理。输出：每章阅读证据和草稿索引条目。 |
| 0.3 | 每本书一个 Agent，最多 3 个并行 | 索引生成 —— 将每章草稿条目整合为每本书的最终 `index.md`。可与子阶段 0.2 对不同书籍并行（即 A 书阅读 Agent 完成后，A 书索引生成 Agent 即可启动，而 B、C 书仍在阅读中）。输出：`.book-doc/knowledge_base/{book_name}/index.md`。 |
| 0.4 | 单 Agent | 覆盖度对比（Coverage Comparison）—— 加载所有已完成的索引，对比各书的主题覆盖情况，识别缺口和重叠。输出：覆盖度对比报告。 |
| 0.5 | 单 Agent | 门控检查（Gate Check）—— 验证每个索引是否达到 >=1000 行阈值，每章是否有阅读证据，覆盖度对比是否完成。阶段 0 通过/失败判定。 |

```
Sub-Phase Flow:
+---------------------------------------------------------------+
| 0.1 Inventory (single agent)                                   |
|   -> Output: inventory.md                                      |
|                                                                |
| 0.2 Deep Reading (one agent per book, max 3 parallel)          |
|   Batch 1: Book A agent + Book B agent + Book C agent          |
|     Book A agent:                                              |
|       Ch1 -> Ch2 -> ... -> ChN (strict sequence)               |
|       Write interim progress after each chapter                |
|     Book B agent: (same structure)                             |
|     Book C agent: (same structure)                             |
|   Batch 1 complete -> Batch 2: Book D + Book E (if more books) |
|                                                                |
| 0.3 Index Generation (one agent per book, max 3 parallel)      |
|   Can overlap with 0.2 for different books:                   |
|   e.g., Book A index agent starts as soon as Book A read done, |
|   while Books B and C are still being read                     |
|                                                                |
| 0.4 Coverage Comparison (single agent)                         |
|   -> Requires all indexes complete                             |
|                                                                |
| 0.5 Gate Check (single agent)                                  |
|   -> Requires coverage comparison complete                     |
+---------------------------------------------------------------+
```

**为什么同一本书内的章节不能并行**：
- 章节之间存在认知递进关系（Cognitive Progression）；后续章节引用前面章节的概念
- 知识索引必须记录跨章节主题映射；并行会导致信息碎片化
- 风格基线（Style Baseline）分析需要端到端的一致性分析

**基于 Web 的源书的特殊处理**：
- 部分章节包含指向其他页面的超链接/引用
- 策略：在进入下一章之前，解析当前章节内的所有引用
- 如果引用指向外部站点（不属于本书），记录 URL 但不跟踪
- 如果引用指向同一本书的另一章节，标记为交叉引用（Cross-Reference）并继续当前章节

```markdown
### Agent Task Template (Phase 0, Sub-Phase 0.2)

You are a book reading agent. Task: generate a deep knowledge index for [book name].

**Constraints**:
1. Read chapters in order; do not skip chapters
2. Every chapter must be actually read; do not infer content from titles alone
3. When encountering links/references within a chapter, resolve them within that chapter
4. Record reading evidence immediately after each chapter (paragraph count, code block count, key terms)
5. Output using the format defined in knowledge-index-format.md
6. Total output >= 1000 lines
7. Timeout limit: 10 minutes

**Input**:
- Book path/URL: [...]
- Reference file: knowledge-index-format.md

**Output**:
- Write to: .book-doc/knowledge_base/{book_name}/index.md
```

### 阶段 1：架构设计（Architecture Design）

**编排模式**：以单 Agent 顺序执行为主，章节计划起草时可有限并行。

#### 子阶段编排

| 子阶段 | Agent 模式 | 说明 |
|--------|-----------|------|
| 1.1 | 单 Agent | 加载索引 —— 读取阶段 0 的所有知识索引，包括覆盖度对比报告。在内存中构建所有源材料的表示。 |
| 1.2 | 单 Agent | 跨书分析（Cross-Book Analysis）—— 对所有书籍进行整体对比：识别独特贡献、重叠覆盖、互补视角和冲突解释。需要对所有索引的统一视图；无法拆分到多个 Agent。 |
| 1.3 | 单 Agent | 目录设计（TOC Design）—— 基于跨书分析设计目标目录。必须保持整体连贯性；并行 Agent 会产生不一致的结构。 |
| 1.4 | 并行 Agent，最多 3 个 | 章节计划起草 —— 并行起草不同章节的整合计划。每个 Agent 接收目录和跨书分析，然后编写其负责章节的计划。Agent 不得修改目录或分析；只产出章节级计划。 |
| 1.5 | 单 Agent | 反向覆盖（Reverse Coverage）—— 验证索引中每本源书的每个主题都映射到计划中至少一个章节/小节。识别孤立主题（Orphaned Topics）。 |
| 1.6 | 单 Agent | 门控检查 —— 验证架构是否完整：目录连贯、所有章节计划就绪、反向覆盖无未解释的缺口、`source-architecture.md` + `plan.md` 均有效。阶段 1 通过/失败判定。 |

```
Sub-Phase Flow:
+---------------------------------------------------------------+
| 1.1 Load Indexes (single agent)                                |
|   -> Read all index.md files + coverage comparison             |
|                                                                |
| 1.2 Cross-Book Analysis (single agent)                         |
|   -> Requires holistic view; cannot shard                      |
|   -> Output: cross-book analysis section of source-arch.md     |
|                                                                |
| 1.3 TOC Design (single agent)                                  |
|   -> Requires cross-book analysis complete                     |
|   -> Output: target TOC in source-architecture.md              |
|                                                                |
| 1.4 Chapter Plan Drafting (parallel, max 3 agents)             |
|   -> Each agent drafts plans for assigned chapters             |
|   -> Agents receive TOC + analysis as read-only input          |
|   -> Output: per-chapter integration plans in plan.md          |
|                                                                |
| 1.5 Reverse Coverage (single agent)                            |
|   -> Requires all chapter plans complete                       |
|   -> Output: reverse coverage map, orphaned topic list         |
|                                                                |
| 1.6 Gate Check (single agent)                                  |
|   -> Requires reverse coverage complete                        |
+---------------------------------------------------------------+
```

**为什么阶段 1 的大部分不能使用并行**：
- 架构设计需要全局视角；跨书分析无法分片（Shard）
- 目录设计需要整体连贯性；并行 Agent 无法协调各自的结构
- 章节整合计划需要感知前后章节，以设计过渡内容

**如果知识索引过长**（单 Agent 无法全部容纳）：
- 允许分批读取：先读取所有索引的"整合就绪摘要"（Integration Readiness Summary）和"整体教学理念"部分
- 然后分批读取每本书的逐主题章节分析
- 但最终输出必须是一对统一、一致的文件（`source-architecture.md` + `plan.md`）

```markdown
### Agent Task Template (Phase 1, Sub-Phase 1.4)

You are a chapter plan drafting agent. Task: draft integration plans for chapters [list].

**Input** (self-contained):
- Target TOC: [the designed table of contents]
- Cross-book analysis: [relevant analysis sections]
- Knowledge index excerpts: [sections relevant to your assigned chapters]

**Constraints**:
1. Do not modify the TOC or cross-book analysis
2. Each chapter plan must include: source mapping, methodology selection, content synthesis approach
3. Ensure transitions between your chapters and adjacent chapters (by others) are noted
4. Timeout limit: 10 minutes

**Output**:
- Return: chapter integration plans for assigned chapters
```

### 阶段 2：章节生成（Chapter Generation）

**编排模式**：严格按顺序每次生成一个章节；章节内在特定条件下小节可并行。

#### 子阶段编排

| 子阶段 | Agent 模式 | 说明 |
|--------|-----------|------|
| 2.1 | 每章单 Agent | 加载计划 —— 读取当前章节的整合计划，加载相关知识索引摘录，准备小节级任务规格。 |
| 2.2 | 最多 3 个小节 Agent 并行 | 小节生成 —— 在当前章节内生成各小节。当小节之间无顺序依赖时，最多 3 个小节 Agent 并行运行。有递进依赖的小节必须串行生成。 |
| 2.3 | 单 Agent | 质量门控（Quality Gate）—— 将小节合并为完整章节，运行质量检查（整合级别、源标记、风格一致性、代码验证标签）。通过 -> 继续；失败 -> 重写。 |
| 2.4 | 单 Agent | 进度记录 —— 更新 `progress.md` 中的章节完成状态，调用 `workflow.py` 记录里程碑。此 Agent 在质量门控通过后运行。 |
| 2.5 | 单 Agent | 批量检查 —— 每完成 5 章，对所有已完成章节运行一致性检查（术语一致性、风格漂移、交叉引用完整性）。 |

```
Sub-Phase Flow (per chapter):
+---------------------------------------------------------------+
| Ch1 (sequential across chapters)                               |
|   2.1 Load Plan (single agent)                                 |
|     -> Read Ch1 integration plan + knowledge index excerpts    |
|                                                                |
|   2.2 Section Generation (max 3 parallel agents)               |
|     +-- Section 1.1 agent (if independent)                     |
|     +-- Section 1.2 agent (if independent)                     |
|     +-- Section 1.3 agent (if independent)                     |
|     OR sequential if sections have dependencies                |
|                                                                |
|   2.3 Quality Gate (single agent)                              |
|     -> Merge sections -> ch01.html                             |
|     -> Run quality checks                                      |
|     -> Pass -> continue / Fail -> rewrite                      |
|                                                                |
|   2.4 Progress Record (single agent)                           |
|     -> Update progress.md, call workflow.py                    |
|                                                                |
| Ch2 (starts only after Ch1 quality gate passes)                |
|   -> ...same sub-phase structure...                            |
|                                                                |
| Every 5 chapters:                                              |
|   2.5 Batch Check (single agent)                               |
|     -> Cross-chapter consistency verification                  |
+---------------------------------------------------------------+
```

**为什么章节不能并行**：
- 章节之间有叙事连贯性（Narrative Continuity）；后续章节需要引用前面的输出
- 质量问题会传播 —— 如果第 1 章有问题，第 2-5 章中的引用都会出错
- 逐章质量门控确保每章达标，避免累积返工

**章节内小节可以并行的条件**：
- 小节之间无顺序依赖（例如 1.1 和 1.2 是独立主题）
- 每个小节 Agent 接收完整的整合指令 + 风格基线
- 合并时检查小节间过渡，必要时添加过渡段落

**章节内小节不可并行的条件**：
- 小节之间有明确的递进关系（1.1 中的概念是 1.2 的前置条件）
- 必须维护统一的叙事弧线（Narrative Arc）

```markdown
### Agent Task Template (Phase 2, Sub-Phase 2.2)

You are a section generation agent. Task: generate Chapter [N], Section [M].

**Input** (self-contained, no need to read other files):
- Integration instructions: [the section's integration plan, including source mapping, methodology selection, content synthesis approach]
- Knowledge index excerpt: [source book chapter analysis relevant to this section]
- Style baseline: [1-2 paragraphs of primary book original text]
- Terminology conventions: [glossary terms relevant to this section]
- Preceding content summary: [2-3 sentence summary of the previous section, for continuity]

**Constraints**:
1. Integration level must be L3 or L4 (direct insertion is not allowed)
2. All content must have `<!-- integrated: [source]Ch[N]-[id] -->` markers
3. New code must have V1-V3 verification tags
4. Match the narrative style of the style baseline
5. Output in MD format（作者约定见 references/md-authoring.md，ADR-0001）
6. Timeout limit: 10 minutes

**Output**:
- Return: section MD content + marker list
```

### 阶段 3：验证（Validation）

**编排模式**：可并行但有上限。

#### 子阶段编排

| 子阶段 | Agent 模式 | 说明 |
|--------|-----------|------|
| 3.1 | 单 Agent | 覆盖度验证 —— 检查 `plan.md` 中所有 ID 是否在输出中有对应标记，并验证源书的反向覆盖。 |
| 3.2 | 单 Agent | 技术验证 —— 运行代码块，验证 API 引用，检查版本兼容性。 |
| 3.3 | 单 Agent | 一致性验证 —— 检查所有章节的术语一致性、风格一致性和交叉引用完整性。 |
| 3.4 | 单 Agent | 汇总 —— 收集所有验证 Agent 的结果，生成统一验证报告，做出通过/失败判定。 |

```
Validation Flow:
+---------------------------------------------------------------+
| Parallel validation (max 3 agents):                            |
|                                                                |
| Agent 1 (3.1): Coverage validation                             |
|   - Check all plan.md IDs have markers                         |
|   - Check source book reverse coverage                         |
|                                                                |
| Agent 2 (3.2): Technical validation                            |
|   - Code block execution checks                                |
|   - API verification                                           |
|   - Version compatibility                                      |
|                                                                |
| Agent 3 (3.3): Consistency validation                          |
|   - Terminology consistency                                    |
|   - Style consistency                                          |
|   - Cross-reference integrity                                  |
|                                                                |
| All complete -> 3.4 Aggregation (single agent)                 |
|   -> Unified validation report + pass/fail decision            |
+---------------------------------------------------------------+
```

## 错误恢复策略

| 错误类型 | 检测方式 | 恢复策略 |
|----------|---------|---------|
| Agent 超时 | 10 分钟无响应 | 终止 Agent，降低该任务的并行度，然后重试 |
| Agent 质量失败 | 门控检查未通过 | 用不同的提示（Prompt）重试一次。若仍失败，暂停并请求用户决策 |
| Agent 上下文溢出 | 输出截断或不完整 | 将任务拆分为更小的子任务 |
| 依赖冲突 | 前置 Agent 的输出与预期不符 | 检查前置输出；必要时回滚到依赖阶段 |
| 网页读取失败 | 404 / 超时 / 反爬虫机制 | 重试一次。若仍失败，标记为"源不可用"并记录到 `progress.md` |

**不允许**：
- 静默跳过失败的 Agent
- 用占位符替代失败的内容
- 降低质量标准以适应 Agent 的能力限制

## 进度跟踪

每个 Agent 的启动、完成和失败都必须记录在 `progress.md` 中：

```markdown
### Agent Tracking

| Agent ID | Phase | Sub-Phase | Task | Status | Start Time | End Time | Output |
|----------|-------|-----------|------|--------|------------|----------|--------|
| P0-0.1 | Phase 0 | 0.1 | Inventory | done | 10:00 | 10:02 | inventory.md |
| P0-0.2-A | Phase 0 | 0.2 | Book A reading | done | 10:02 | 10:10 | draft entries |
| P0-0.2-B | Phase 0 | 0.2 | Book B reading | done | 10:02 | 10:14 | draft entries |
| P0-0.2-C | Phase 0 | 0.2 | Book C reading | fail->done | 10:02 | 10:17 | draft entries |
| P0-0.3-A | Phase 0 | 0.3 | Book A index gen | done | 10:10 | 10:13 | index.md |
| P0-0.4 | Phase 0 | 0.4 | Coverage comparison | done | 10:18 | 10:20 | coverage report |
| P0-0.5 | Phase 0 | 0.5 | Gate check | done | 10:20 | 10:21 | pass |
```

## 并发调优建议

| 场景 | 建议并发数 | 理由 |
|------|-----------|------|
| 3 本及以下源书 | 3 | 每本书一个 Agent；阶段 0 一批完成 |
| 4-6 本源书 | 3-4 | 阶段 0 分两批；避免资源争用 |
| 7 本以上源书 | 3 | 严格分批，每批 3 本书，确保单 Agent 质量 |
| 章节生成（短章节） | 1（章节间）+ 3（章节内） | 短章节允许 3 路小节并行 |
| 章节生成（长章节） | 1（章节间）+ 1（章节内） | 长章节内容多；单 Agent 确保连贯性 |
| 验证 | 3 | 验证任务相互独立；完全并行安全 |
