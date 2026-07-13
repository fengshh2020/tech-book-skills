# 多源模式 (Multi-Source Mode)

当提供两个或更多源书籍时使用。工作流：深度阅读（Phase 0）→ 架构设计（Phase 1）→ 章节生成（Phase 2）→ 验证（Phase 3）→ 报告（Phase 4）。

**启动前**：运行预检（见 `shared-rules.md`「预检清单」），确认每个源文件可读取且数量 >= 2。初始化 progress.md（见 `shared/discipline-framework.md`「进度追踪」）。

## 两个状态文件（context-passing 核心）

LLM 在长工作流跨阶段会丢上下文。用两个文件互补：

| 文件 | 职责 | 回答 |
|---|---|---|
| `progress.md` | 进度跟踪：哪些阶段/章节已完成、从哪里恢复 | "我们到了哪里" |
| `context-summary.md` | 知识传递：跨阶段的关键发现和决策 | "我们知道了什么" |

**规则**：每个子阶段结束时向 `context-summary.md` 追加一个 <=150 行的章节；下一子阶段开始时**只读摘要 + 本子阶段的参考文件**，不重新读先前子阶段的原始输出。所有文件在运行目录 `.book-doc/runs/{id}/` 下。

**context-summary 摘要骨架**（各阶段追加自己的章节）：
- Phase 0：源书概览（章数/索引行数/角色）、逐书核心方法论、关键发现、风格基线要点、潜在整合挑战
- Phase 1：目标读者、逐书角色、最终骨架（核心/支撑/进阶路径）、关键方法论决策（附证据）、排除范围、整合计划统计
- Phase 2（逐章）：Ch[N] 完成记录（门控结果 G1-G8、整合标记数、代码块数、长度）+ Ch[N] Context（源映射、方法论、关键决策、跨章回引）
- Phase 3：覆盖率%、术语一致性、代码可运行性、风格一致性、已知限制

## Phase 0：深度阅读（5 个子阶段）

**⚠️ 启动前**：阅读 `references/multi-read-architect.md`（知识索引格式）和 `references/agent-orchestration.md`，progress.md 记录确认。

- **0.1 书籍清点**：列出所有源书（书名、章节数、页数、路径）
- **0.2 逐书阅读**：顺序读每章（不跳过、不凭标题推断）；每本书一个 Agent，最多 3 本并行；网页源先读当前章所有链接再进下一页
- **0.3 索引生成**：按 `multi-read-architect.md` 为每本书生成知识索引（>= 1000 行）
- **0.4 覆盖率对比**：跨书对比索引——重叠、空白、独特贡献、深度差异
- **0.5 关卡（Gate 0）**：见 `multi-synthesis.md`「Phase 0 关卡」

本阶段是整个流程的基础，索引未验证前不得继续。

## Phase 1：架构设计（6 个子阶段）

**⚠️ 启动前**：阅读 `references/multi-read-architect.md`（架构评估），重新读 Phase 0 所有知识索引。Gate 0 已通过。

- **1.1 加载索引**：完整读所有知识索引（不可略读）
- **1.2 跨书分析**：方法论对比、深度对齐、边界互补、风格调和（输出 `cross-book-analysis.md`，模板见 multi-read-architect.md）
- **1.3 目标目录**：设计目录，每章有明确目的和源材料映射（模板见 multi-read-architect.md）
- **1.4 逐章计划**：为每章写自包含整合计划（源材料贡献图、方法论选择+理由、深度目标、合成策略、概念桥接、术语约定、风格基线样例）。**Phase 2 执行时不应需要重读其他文件**
- **1.5 反向覆盖**：构建反向覆盖矩阵——每个源章节 → 目标章节/侧边栏/附录/明确排除
- **1.6 关卡（Gate 1）**：见 `multi-synthesis.md`「Phase 1 关卡」

输出：`source-architecture.md` + `plan.md`。

## Phase 2：章节生成（每章 6 个子阶段）

**⚠️ 启动前**：阅读 `references/multi-synthesis.md`（合成方法论 + 整合级别 + 门控）和 `references/agent-orchestration.md`，重读 plan.md 中该章的整合计划。Gate 1 已通过。

- **2.1 加载计划与源材料**：加载该章整合计划、相关知识索引、风格基线
- **2.2 解构与重写（5 步）**：解构所有源材料 → 设计新结构（不照搬任何源结构）→ 分配主/次源 → 统一风格重写 → 加标记 `<!-- integrated: [source]Ch[N]-[id] -->`。整合必须达 L3（重组）或 L4（完全融合），见 multi-synthesis.md
- **2.3 质量门控（G1-G8）**：见 `multi-synthesis.md`「Phase 2 关卡」。未通过 = 重写本章，不累积修复
- **2.4 进度记录**：门控结果写 progress.md，通过后才进下一章
- **2.5 批量检查（每 5 章）**：跨章术语一致、源不可辨识测试、叙事弧连贯
- **2.6 组装**：在 `{RUN}/src/` 写 `book.yml` + 编号章节 MD（约定见 `md-authoring.md`）；运行 `python scripts/build_html.py {RUN}/src {RUN}/output`（封面/目录/导航/CSS/JS/组件升级/mermaid→PNG 均由 builder 完成）

> **doc 形态**（见 `references/product-shapes.md`）：不走 builder、不写 `book.yml`，整合完直接写就地 MD；轻量 gate（无 Coverage Guardian、无大小下限），但整合仍须达 L3/L4（不可辨识来源）、无翻译腔。

**输出验证（2.2 后）**：章节文件存在且非空、含 `<!-- integrated -->` 标记、无 `[待确认]`、大小 >= 最大源章节的 80%。

**子 Agent 策略**：一次一章，单章内最多 3 个小节 Agent 并行。

## Phase 3：验证

覆盖率验证（所有章节）→ 术语一致性（全书检索）→ 代码可运行性 → 风格一致性（连续 3 章）→ 交叉引用完整性 → 反向覆盖 100%。

```bash
scripts/validate_output.sh output/
python scripts/workflow.py generate-book <run_dir> coverage_report
python scripts/workflow.py generate-book <run_dir> coverage_guard
python ../shared/validate_tech.py output/
python ../shared/validate_terms.py output/
```

**关卡（Gate 3）**：见 `multi-synthesis.md`「Phase 3 关卡」。Coverage Guardian 无底线违规。

**Gate 降级**（workflow.py 不可用）：逐章 `grep -c 'integrated:' output/*.html` 查标记数，`wc -c` 查大小。

## Phase 4：报告

**⚠️ 启动前**：阅读 `shared/report-templates.md`。Gate 3 已通过。

编写 `report.md`：摘要、每章评分、问题列表、覆盖矩阵、已知限制、Coverage Guardian 结果。
