# 多源模式 (Multi-Source Mode)

当提供两个或更多源书籍时使用。工作流：深度阅读、架构设计、章节生成、验证、报告。

**启动前**：运行预检（见 `shared-rules.md`「预检清单」），确认每个源文件可读取且数量 >= 2。初始化 progress.md（见「进度追踪鲁棒性」）。

## Phase 0：深度阅读（5 个子阶段）

**⚠️ 启动前**：阅读 `references/knowledge-index-format.md` 和 `references/agent-orchestration.md`，在 progress.md 中记录确认。

### 0.1 书籍清点
- 列出所有源书籍及其章节结构
- 记录：书名、章节数、总页数、文件路径

### 0.2 逐书阅读
- 按顺序阅读每个章节（不跳过，不只凭标题推断）
- 每本书分配一个 Agent，最多 3 本书并行
- 网页源：先阅读当前章节内所有链接再进入下一页

### 0.3 索引生成
- 按照 `references/knowledge-index-format.md` 为每本书生成知识索引
- 每个索引 >= 1000 行，覆盖：每章内容分析、方法论、深度校准、边界映射、独特见解、代码示例清点、交叉引用图、风格特征、整合就绪度

### 0.4 覆盖率对比
- 跨书籍对比索引：重叠部分、空白区域、独特贡献、深度差异

### 0.5 关卡（Gate 0）
- 每个源书籍在 `.book-doc/knowledge_base/` 中都有索引文件（>= 1000 行）
- 每个章节都有阅读证据（段落数、代码块数、核心概念、独特贡献）

**本阶段是整个流程的基础。在每个索引都被验证之前，不得继续。**

## Phase 1：架构设计（6 个子阶段）

**⚠️ 启动前**：阅读 `references/book-architecture.md`，重新阅读 Phase 0 的所有知识索引。Gate 0 已通过。

### 1.1 加载索引
- 完整阅读所有知识索引（不可略读）

### 1.2 跨书籍分析
- 方法论对比、深度对齐、边界互补性、风格调和

### 1.3 目标目录
- 设计目标目录结构，每个章节有明确目的和源材料映射

### 1.4 逐章计划
为每个章节编写整合计划：源材料贡献图（主要/次要/参考）、方法论选择及理由、深度目标、合成策略、空白填补需求、依赖链、预期产出

### 1.5 反向覆盖
- 构建反向覆盖矩阵：每个源章节 -> 目标章节 / 侧边栏 / 附录 / 明确排除

### 1.6 关卡（Gate 1）
- `source-architecture.md` 和 `plan.md` 存在且完整
- 反向覆盖矩阵覆盖 100% 源章节，无"TBD"占位符

## Phase 2：章节生成（每章 6 个子阶段）

**⚠️ 启动前**：阅读 `references/full-integration.md` 和 `references/agent-orchestration.md`，重新阅读 plan.md 中该章节的整合计划。Gate 1 已通过。

### 2.1 加载计划与源材料
- 加载 plan.md 中该章节的整合计划、相关知识索引、风格基线

### 2.2 解构与重写（5 步）
1. 解构所有源材料的相关内容
2. 设计新章节结构（不照搬任何源材料的原始结构）
3. 为每个小节分配主要/次要源材料
4. 以统一风格重写
5. 添加标记：`<!-- integrated: [source]Ch[N]-[id] -->`

**输出验证**：章节文件存在且非空；包含 `<!-- integrated: ... -->` 标记；无 `[待确认]` 占位符；大小 >= 最大源章节的 80%。

### 2.3 质量关卡（G1-G8）

| 检查项 | 通过标准 | 失败处理 |
|--------|----------|----------|
| G1：覆盖率 | 所有 plan.md 中的 ID 都有标记 | 重写章节 |
| G2：代码质量 | 新代码有 V1-V3 标签 | 添加标签 + 验证 |
| G3：风格匹配 | 无翻译腔，匹配基线 | 重写相关小节 |
| G4：无重复 | 无重复解释 | 合并/交叉引用 |
| G5：叙事流畅 | 过渡自然，叙事弧完整 | 重写 |
| G6：深度匹配 | 符合计划的深度目标 | 扩展或裁剪 |
| G7：源材料比例 | 每个映射的源材料在本章有 >=3 个标记 | 扩展源材料贡献 |
| G8：输出大小 | >= 最大源章节大小的 80% | 扩展内容 |

### 2.4 进度记录
- Gate 结果写入 progress.md，仅当 Gate 通过后才可进入下一章

### 2.5 批量检查（每 5 章）
- 跨章节术语一致、源不可辨识测试、叙事弧连贯

**子 Agent 策略**：一次一个章节，单章内最多 3 个小节 Agent 并行。Gate 失败 = 重写章节，不累积修复。

### 2.6 组装（MD 主源 + builder，ADR-0001）
- 在 `{RUN}/src/` 写 `book.yml` + 整合后的编号章节 MD（约定见 `references/md-authoring.md`）
- 运行 `python scripts/build_html.py {RUN}/src {RUN}/output`：封面/目录/导航/CSS/JS/组件升级/mermaid→PNG 均由 builder 完成

## Phase 3：验证

1. 覆盖率验证（所有章节）
2. 术语一致性检查（全书检索）
3. 代码可运行性检查
4. 风格一致性（连续 3 章）
5. 交叉引用完整性
6. 反向覆盖：100% 源材料已处理

```bash
scripts/validate_output.sh output/
python scripts/workflow.py generate-book <run_dir> coverage_report
python scripts/workflow.py generate-book <run_dir> coverage_guard
python ../shared/validate_tech.py output/
python ../shared/validate_terms.py output/
```

**关卡**：覆盖率 >= 95%，术语一致，代码可运行，交叉引用有效，无风格跳跃。Coverage Guardian：无章节低于底线（总标记数的 10%），无章节低于单章最低要求（3 个标记）。

**Gate 降级检查**（当 workflow.py 不可用时）：
```bash
# 逐章检查大小和标记
for f in output/*.html; do
  size=$(wc -c < "$f")
  markers=$(grep -c 'integrated:' "$f")
  echo "$f: size=${size}B, integration_markers=${markers}"
done
```

## Phase 4：报告

**⚠️ 启动前**：阅读 `shared/report-templates.md`。Gate 3 已通过。

编写 `report.md`：摘要、每章评分、问题列表、覆盖矩阵、已知限制、Coverage Guardian 结果。
