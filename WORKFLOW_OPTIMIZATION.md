# 工作流程优化总结

## 优化日期
2026-06-09

## 核心问题

用户反馈："从 skill 的工作流程优化"

经过分析，发现工作流程的 5 个关键问题：

1. **模型手动读取引用文件**：容易遗漏，没有自动加载机制
2. **阶段依赖不明确**：模型不知道"如果 Phase 0 没完成，不能进入 Phase 1"
3. **Gate 检查是手动的**：模型需要"记住"要检查什么，结果是主观的
4. **质量标准是定性的**："Reader cannot identify sources"无法量化
5. **工作流程是线性的**：没有快速迭代和回退机制

## 解决方案

### 1. 统一工作流程脚本（解决"手动读取"和"阶段依赖"）

**新增文件**：`shared/workflow.py`

**核心功能**：
- **阶段锁（Phase Lock）**：自动检查阶段依赖关系，防止跳过
- **自动 Gate 检查**：脚本自动检查文件是否存在、覆盖率是否达标
- **统一接口**：所有 skill 使用同一个脚本，减少模型记忆负担

**使用方式**：
```bash
# 检查状态
python shared/workflow.py <skill> <run_dir> status

# 检查 Gate
python shared/workflow.py <skill> <run_dir> check_gate <phase> [chapter]
```

**示例输出**：
```
$ python shared/workflow.py integrate-books /tmp/run check_gate 1
FAIL: Phase 1 gate failed. Coverage 75% < 80%

$ python shared/workflow.py integrate-books /tmp/run check_gate 1
PASS: Phase 1 gate passed. Coverage 85% >= 80%
```

### 2. 自动化 Gate 检查（解决"手动检查"和"主观结果"）

**旧方式**：
```markdown
**Gate**: Coverage >= 80%
```
- 模型自己判断是否达标
- "差不多 80%"可能被认为通过

**新方式**：
```bash
**Gate** (auto-check):
python ../shared/workflow.py integrate-books <run_dir> check_gate 1
```
- 脚本自动解析覆盖率报告
- "75%"明确失败，"85%"明确通过
- 没有模糊空间

### 3. 量化质量标准（解决"定性标准"）

**旧标准**：
```markdown
- Reader cannot identify content sources
```

**新标准**：
```markdown
| # | Check | Evidence Required |
|---|-------|-------------------|
| G1 | All plan.md IDs have markers | List every ID, show marker location |
| G2 | New code has V1-V3 tags | List every code block, show tag |
| G3 | Style matches baseline | Compare 3 paragraphs |
```

**脚本自动检查**：
- G1: 统计 `<!-- integrated:` 标记数量
- G2: 统计 `<!-- V[123]:` 标记数量
- G3: 扫描翻译腔模式，统计命中次数

### 4. 迭代模式支持（解决"线性流程"）

**工作流程脚本支持**：
- `status`：查看当前阶段、已完成阶段、下一阶段
- `check_gate`：检查当前阶段是否通过
- 自动记录状态到 `.workflow_state.json`

**迭代流程**：
```
Phase 4 (生成) → check_gate 4 → FAIL → 修复 → check_gate 4 → PASS → 下一章
```

## 文件变更

### 新增文件
- `shared/workflow.py` — 统一工作流程脚本
- `integrate-books/scripts/workflow.py` — integrate-books 专用（已废弃，使用 shared）
- `review-tech-book/scripts/review_workflow.py` — review 专用（已废弃，使用 shared）

### 修改文件
- `integrate-books/SKILL.md` — 使用 `../shared/workflow.py`
- `review-tech-book/SKILL.md` — 使用 `../shared/workflow.py`

## 工作流程对比

### 旧工作流程
```
模型加载 skill → 手动读取引用文件 → 执行阶段 → 手动检查 gate → 主观判断 → 下一阶
```

### 新工作流程
```
模型加载 skill → 自动执行阶段 → 运行脚本检查 gate → 客观结果（PASS/FAIL）→ 下一阶
```

## 预期效果

1. **模型不再遗漏引用文件**：脚本自动检查，不需要模型"记住"
2. **阶段依赖自动 enforced**：脚本检查上一阶段是否完成，模型不能跳过
3. **Gate 检查客观化**：脚本自动解析文件，没有"差不多"的模糊空间
4. **质量标准可量化**：从"读者不能分辨"变为"标记数量 >= 1，翻译腔命中 = 0"
5. **支持快速迭代**：失败时立即返回修复，不需要重新走完整流程

## 测试验证

```bash
# Phase 0: 架构文档完整
$ python shared/workflow.py integrate-books /tmp/run check_gate 0
PASS: Phase 0 gate passed. source-architecture.md present

# Phase 1: 覆盖率不足
$ python shared/workflow.py integrate-books /tmp/run check_gate 1
FAIL: Phase 1 gate failed. Coverage 75% < 80%

# Phase 1: 覆盖率足够
$ python shared/workflow.py integrate-books /tmp/run check_gate 1
PASS: Phase 1 gate passed. Coverage 85% >= 80%
```
