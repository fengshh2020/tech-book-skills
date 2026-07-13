# 代码库模式 (Codebase Mode)

当输入为代码库路径时使用。工作流：发现、分析、规划、生成、验证。聚焦设计决策、代码理解、算法、知识点。

**启动前**：运行预检（见 `shared-rules.md`「预检清单」），确认代码库路径存在且包含源文件，有基本的构建/运行命令。初始化 progress.md（见「进度追踪鲁棒性」）。

## 成功标准

读者读完本书后，能够将每个关键行为追溯到其源码位置，理解设计选择背后的原因，并掌握所有必需的背景知识。

## Phase 0：发现

**要做什么**：
1. 识别源文件、测试、配置、资源
2. 确定语言、框架、依赖、构建命令、入口点
3. 分类每个文件：核心路径（深度）/ 支撑路径（概要）/ 参考（确认）
4. 识别自然执行路径：输入 -> 模块 -> 输出

**输出**：`{RUN}/codebase-map.md`

**输出验证**：codebase-map.md 存在且非空；每个相关文件已分类或附理由排除；分类覆盖所有源文件（无遗漏）。

**关卡（Gate 0）**：每个相关文件已分类，或附理由排除。

## Phase 1：分析

**⚠️ 启动前**：阅读 `references/analysis-guide.md`，在 progress.md 中记录确认。Gate 0 已通过。

**要做什么**（针对每个核心模块）：
- **接口与行为**：公共 API、参数语义、核心逻辑、数据/控制流
- **设计决策**：为什么选择这个数据结构/算法/模式？替代方案？权衡取舍？
- **核心算法**：核心思想、复杂度、参数影响
- **错误处理**：异常路径、降级策略、边界条件
- **隐含知识**：读者需要了解什么（语言特性、框架机制、算法理论）
- **在执行路径中的位置**：该模块在全局链路中的位置

**每个模块需要的证据**（写入 analysis/{module}.md）：
```
### [模块] 分析证据
- 已读源文件：[列出，附带行数]
- 已分析函数：[数量，附带 file:line 引用]
- 设计决策：[数量，每条都有"为什么"的记录]
- 关键术语：[>=3 个具体实现细节，不是泛泛描述]
```

**输出**：`{RUN}/analysis/{module}.md`

**输出验证**：每个核心模块的分析文件存在且非空；每个文件包含 file:line 引用；每个文件包含至少 3 个具体术语；无 `[待确认]` 占位符。

**关卡（Gate 1）**：核心模块已覆盖接口、设计、算法、隐含知识。

## Phase 2：规划

**⚠️ 启动前**：阅读 `references/writing-and-content.md`。Gate 1 已通过。

**要做什么**：
1. 定义目标读者和前置知识要求
2. 章节列表按内容逻辑排序（不是按目录树结构）
3. 每章：核心内容、覆盖的源文件、知识扩展点、延后范围

**规划原则**：结构服务于内容逻辑；每个模式只详细解释一次，其余交叉引用；每章有明确焦点；不强行安排组件。

**输出**：`{RUN}/chapter-plan.md`

**输出验证**：chapter-plan.md 存在且非空；每个章节有明确焦点和源文件映射；无 TBD 占位符；核心执行路径无缺口。

**关卡（Gate 2）**：核心执行路径没有缺口；重复机制已有首次详述 + 后续引用。

## Phase 3：生成

**⚠️ 启动前**：重新阅读 `references/writing-and-content.md`。Gate 2 已通过。

> **doc 形态**（见 `references/product-shapes.md`，如 `pi3_trt/book.md` 这种项目学习文档）：不走 builder、不写 `book.yml`、不强制多章。流程压缩为——分析完核心模块后，直接写就地 `book.md`：顶部一句话说明项目用途 + 可选目录 → 沿主执行路径叙事讲解核心模块（每论断 file:line）→ 收尾给"修改影响/常见失败"。用同一套"叙事驱动/设计决策/代码摘录"规则，只是输出单文件、用轻量 gate（无 20KB 下限、无 builder 验证；**但 file:line 证据、无占位符、叙事连贯仍不可妥协**）。book 形态才走下面的多章 + builder 流程。

**MD 主源 + builder（ADR-0001，book 形态）**：在 `{RUN}/src/` 写 MD 章节 + `book.yml`，CSS/JS/封面/目录由 builder 注入（无需手动复制）。

**每章**：
1. 文件：`{RUN}/src/NN_*.md`，首行 `# 标题`
2. 代码摘录：从源码复制，标注文件路径 + 行范围
3. **叙事驱动**：沿执行路径或设计线索展开
4. **图表优先**：复杂流程写 ` ```mermaid `（见 `references/md-authoring.md`、ADR-0004），证据 file:line 写图注
5. 核心函数：展示代码 + 解释逻辑 + 分析设计
6. 设计决策：是什么、为什么、替代方案、权衡取舍
7. 核心算法：核心思想、数据结构、参数影响
8. 知识扩展：侧边栏用 `> **[标签]**`（不在代码走读中穿插）
9. MD 中不得有 `[待确认]`

全部章节写完后运行：`python scripts/build_html.py {RUN}/src {RUN}/output`（产出 HTML 版 + 可移植 MD 版 + diagrams/*.png）。

**内容深度**：核心章节 >= 20KB，概览 >= 10KB，代码:解释比例 >= 1:1，核心路径每个函数/参数都有说明，错误路径已覆盖。

**并行写作**（章节数 > 5 时）：每批 2-3 章并行写 MD；最后由主代理统一运行 builder。

**关卡（Gate 3）**：所有章节有 `<!-- generated: complete -->` 标记，核心章节 >= 20KB，概览 >= 10KB，代码:解释 >= 1:1。

**Gate 3 降级检查**（当 workflow.py 不可用时）：
```bash
# 逐章检查
for f in output/*.html; do
  size=$(wc -c < "$f")
  has_marker=$(grep -c 'generated: complete' "$f")
  has_placeholder=$(grep -c '\[待确认\]\|TBD\|TODO' "$f")
  echo "$f: size=${size}B, marker=${has_marker}, placeholders=${has_placeholder}"
done
```

## Phase 4：验证

**⚠️ 启动前**：阅读 `shared/report-templates.md`。Gate 3 已通过。所有章节已生成。

```bash
scripts/validate_output.sh output/
python ../shared/validate_tech.py output/
python ../shared/validate_terms.py output/
```

编写 `{RUN}/report.md`。将 `progress.md` 标记为已完成。

**关卡（Gate 4）**：所有章节通过技术准确性和术语一致性验证，report.md 已生成。

## 章节红线检查

标记任何章节完成前，确认：源文件已读代码体（非仅名称）、有 file:line 引用、大小达标（核心 >= 20KB，概览 >= 10KB）、代码:解释 >= 1:1、覆盖错误路径、设计决策有替代方案/权衡取舍。
