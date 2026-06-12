---
name: generate-book
description: "Generate a unified technical book from one or more sources. Single source: translate and produce Chinese HTML book. Multiple sources: deep-read, integrate, and produce one coherent book. Trigger: generate book, 整合书籍, 生成书籍, merge books, combine sources, translate book, 翻译书籍. Do NOT trigger for: quality review only (use review-tech-book), codebase analysis (use codebase-book)."
---

# 生成书籍

## ⛊ 铁律 (IRON LAW)

**NO OUTPUT WITHOUT FRESH READ EVIDENCE. NO GATE SKIP. NO TITLE-ONLY INFERENCE. NO CONTENT SHRINKAGE.**
（没有新鲜阅读证据就不产出。不跳过 Gate。不只凭标题推断。不缩减内容。）

违反这条规则的字面意思，就是违反这条规则的精神。

### 反合理化表 (Anti-Rationalization Table)

| 如果你这么想…… | 真相是…… |
|-----------------|----------|
| "我记得这条规则" | 你不记得。重新读取文件。 |
| "标题已经告诉我足够多了" | 并不够。打开文件完整阅读。 |
| "Gate 大概能通过" | 去运行它。没有"大概"。 |
| "这大概有 80% 的覆盖率" | 缩减 = 数据丢失。扩展内容。 |
| "我到 Phase 3 再修" | 现在就修，否则以后重写。 |
| "就这一次" | "就这一次"就是这样开始的。 |
| "用户想要速度" | 用户想要质量。 |
| "我已经验证过了" | 重新验证。只接受新鲜证据。 |

从一个或多个源材料生成统一的技术书籍。单一源 -> 翻译 + 组装。多个源 -> 整合 + 组装。输出必须读起来像一本书，而不是拼贴画。

### 标准关卡自检清单 (Standard Gate Self-Check)

> 以下自检清单适用于本文件中所有关卡。在每个关卡前必须确认：
>
> **⛔ 运行关卡前，确认以下均不为真：**
> - [ ] 任何参考文件在本阶段未被重新阅读
> - [ ] 任何"我已阅读"的声明缺少结构证据
> - [ ] 任何章节的输出大小 < 源文件的 80%
> - [ ] Gate 检查未实际运行（仅口头声称）
>
> **如有任何一项被勾选：先修复再运行关卡。**

## 模式选择

自动检测：1 个源 -> 单源模式，2+ 个源 -> 多源模式。

| 模式 | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|---------|
| 单源 (Single) | 提取与阅读 | 翻译 | 组装 | 验证 | 报告 |
| 多源 (Multi) | 深度阅读（5 个子阶段） | 架构设计（6 个子阶段） | 生成（每章 6 个子阶段） | 验证 | 报告 |

**阶段锁定 (Phase Lock)**：进入任何阶段/子阶段前，运行 `python scripts/workflow.py generate-book <run_dir> check_gate <phase> [<sub_phase>] [chapter]`。如果 Gate 失败，修复后重试。不得继续推进。

**子 Agent 约束**：参见 `references/agent-orchestration.md`。最大并发 Agent 数：5。遵循依赖顺序。

---

## 单源模式 (Single-Source Mode)

当恰好提供一个源书籍时使用。工作流：提取、翻译、组装、验证、报告。

### Phase 0：提取与阅读（3 个子阶段）

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `references/agent-orchestration.md`（不可略读）
- [ ] 在 progress.md 中记录阅读确认及结构证据
- [ ] 如未勾选：停止。不得继续。

#### 0.1 源文件清点 (Source Inventory)
- 解析源文件（EPUB 或 HTML）
- EPUB：解压，解析 container.xml、content.opf、spine、toc.ncx
- HTML：解析结构、标题、导航
- 记录：书名、章节数、总页数、文件路径、源文件指纹
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.1 --status completed`

#### 0.2 逐章阅读 (Chapter-by-Chapter Reading)
- 按顺序阅读每个章节（不跳过，不只凭标题推断）
- 对每个章节，记录阅读证据：
  ```markdown
  ### 第[N]章 阅读证据
  - 段落数：[数量]
  - 代码块数：[数量]
  - 核心概念：[列出 >=3 个具体术语]
  - 图片/图表数：[数量]
  ```
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.2 --status completed`

#### 0.3 关卡（Gate 0）

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 0
```
- 每个章节都有阅读证据记录
- 源文件清点完成，包含所有元数据
- 没有章节被跳过或仅凭标题推断

### Phase 1：翻译（5 个子阶段）

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `references/translation-rules.md`（不可略读）
- [ ] 完整阅读 `shared/translationese-patterns.md`（不可略读）
- [ ] 阅读任何已有的 `.book-doc/spec.md` 以获取术语表
- [ ] 在 progress.md 中记录阅读确认及结构证据
- [ ] 如有任何一项未勾选：停止。不得继续。

#### 1.1 加载翻译规则 (Load Translation Rules)
- 完整阅读 `references/translation-rules.md`
- 完整阅读 `shared/translationese-patterns.md`
- 阅读任何已有的 `.book-doc/spec.md` 以获取术语表
- 记录阅读确认及结构证据
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.1 --status completed`

#### 1.2 逐章翻译 (Per-Chapter Translation)
- 逐段翻译，保持 1:1 映射
- 源文件段落数必须等于目标段落数
- 代码注释翻译为中文；代码逻辑保持不变
- 技术术语首次出现时加注中文注释
- 每翻译一章之前重新阅读规则文件（不要说"我记得"）
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.2 --chapter <chapter> --status completed`

#### 1.3 术语一致性检查 (Terminology Consistency Check)
- 所有章节翻译完成后，运行全书术语检索
- 验证每个术语在所有章节中翻译一致
- 标记并修复任何不一致之处
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.3 --status completed`

#### 1.4 翻译腔扫描 (Translationese Scan)
- 对照 `shared/translationese-patterns.md` 扫描所有已翻译章节
- 目标：对任何列出的模式命中数为 0
- 修复所有检测到的翻译腔
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.4 --status completed`

#### 1.5 关卡（Gate 1）

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 1
```
- 所有章节都有 `<!-- translated: complete -->` 标记
- 每个章节的段落数匹配（源 = 目标）
- 所有术语已检查并一致
- 翻译腔扫描：0 次命中
- progress.md 已为每个章节更新证据

### Phase 2：组装（4 个子阶段）

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `references/book-assembly.md`（不可略读）
- [ ] 在 progress.md 中记录阅读确认及结构证据
- [ ] 关卡（Gate 1）已通过，progress.md 中有证据
- [ ] 如有任何一项未勾选：停止。不得继续。

#### 2.1 HTML 脚手架 (HTML Scaffold)
- 按照 `references/book-assembly.md` 创建输出目录结构
- 文件编号：
  | 编号 | 文件 |
  |------|------|
  | 00 | `00_cover.html` |
  | 01 | `01_toc.html` |
  | 02 | `02_front.html` |
  | 03 | `03_intro.html` |
  | 04+ | `{NN}_chapter{M}.html` |
  | N+ | `{NN}_appendix_{x}.html` |
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.1 --status completed`

#### 2.2 CSS/JS 集成 (CSS/JS Integration)
- 复制 `assets/style.css` 和 `assets/script.js` 到输出目录
- 验证 CSS/JS 在 HTML 文件中正确加载
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.2 --status completed`

#### 2.3 导航与交叉引用 (Navigation & Cross-References)
- 构建目录，链接到所有章节
- 在章节之间添加上一章/下一章导航
- 验证所有内部链接正确解析
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.3 --status completed`

#### 2.4 关卡（Gate 2）

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 2
```
- 输出目录中存在所有 HTML 文件
- CSS/JS 文件存在且已链接
- 目录完整，链接可用
- 所有交叉引用有效
- 所有图片在输出中存在

### Phase 3：验证 (Validate)

**执行操作**：
1. 运行覆盖率验证：输出大小 >= 源文件的 80%
2. 术语一致性检查（全书检索）
3. 代码可运行性检查（所有代码块）
4. 翻译腔二次扫描（0 次命中）
5. 交叉引用完整性（所有章节链接有效）
6. 段落数验证（每个章节的源 = 目标）

**自动检查脚本**：

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/validate_tech.py output/
python scripts/validate_terms.py output/
python scripts/workflow.py generate-book <run_dir> check_gate 3
```

**关卡（Gate 3）**：
- 所有术语一致
- 所有代码可运行
- 所有交叉引用有效
- 翻译腔：0 次命中
- 输出大小 >= 源文件的 80%
- 所有段落已核对

### Phase 4：报告 (Report)

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `shared/report-templates.md`（不可略读）
- [ ] 关卡（Gate 3）已通过，progress.md 中有证据
- [ ] 如有任何一项未勾选：停止。不得继续。

**执行操作**：编写 `report.md`，包含摘要、每章评分、问题列表、术语表、已知限制。

**关卡（Gate 4）**：

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 4
```
- report.md 存在
- 包含：摘要、评分、问题列表、术语表、已知限制

---

## 多源模式 (Multi-Source Mode)

当提供两个或更多源书籍时使用。工作流：深度阅读、架构设计、章节生成、验证、报告。

### Phase 0：深度阅读（5 个子阶段）

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `references/knowledge-index-format.md`（不可略读）
- [ ] 完整阅读 `references/agent-orchestration.md`（不可略读）
- [ ] 在 progress.md 中记录阅读确认及结构证据
- [ ] 如有任何一项未勾选：停止。不得继续。

#### 0.1 书籍清点 (Book Inventory)
- 列出所有源书籍及其章节结构
- 记录：书名、章节数、总页数、文件路径
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.1 --status completed`

#### 0.2 逐书阅读 (Per-Book Reading)
- 对每本书：按顺序阅读每个章节（不跳过，不只凭标题推断）
- 每本书分配一个 Agent，最多 3 本书并行
- 对于网页源：在进入下一页之前，先阅读当前章节内的所有链接
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.2 --status completed`

#### 0.3 索引生成 (Index Generation)
- 按照 `references/knowledge-index-format.md` 为每本书生成知识索引
- 每个索引 >= 1000 行，覆盖：
  - 每章内容分析（主题、顺序、重点）
  - 方法论和教学方式
  - 讲解深度校准
  - 边界映射（范围限制、前置要求）
  - 独特见解和视角
  - 代码示例清点（数量、质量、模式）
  - 交叉引用图
  - 风格和语调特征
  - 整合就绪度评估
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.3 --status completed`

#### 0.4 覆盖率对比 (Coverage Comparison)
- 跨书籍对比索引
- 识别：重叠部分、空白区域、独特贡献、深度差异
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 0 --sub-phase 0.4 --status completed`

#### 0.5 关卡（Gate 0）

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 0
```
- 每个源书籍在 `.book-doc/knowledge_base/` 中都有索引文件
- 每个索引 >= 1000 行
- 每个索引包含所有必需章节
- 每个章节都有阅读证据

**阅读证据**（在 progress.md 中为每个章节记录）：
```markdown
### [书名] 第[N]章 阅读证据
- 段落数：[数量]
- 代码块数：[数量]
- 核心概念：[列出 >=3 个具体术语]
- 本书独特贡献：[本章的独特贡献是什么]
```

**本阶段是整个流程的基础。在每个索引都被验证之前，不得继续。**

### Phase 1：架构设计（6 个子阶段）

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `references/book-architecture.md`（不可略读）
- [ ] 重新阅读 Phase 0 的所有知识索引（不要说"我记得"）
- [ ] 在 progress.md 中记录阅读确认及结构证据
- [ ] 关卡（Gate 0）已通过，progress.md 中有证据
- [ ] 如有任何一项未勾选：停止。不得继续。

#### 1.1 加载索引 (Load Indexes)
- 完整阅读所有知识索引（不可略读）
- 记录阅读确认及结构证据
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.1 --status completed`

#### 1.2 跨书籍分析 (Cross-Book Analysis)
- 方法论对比：每本书如何处理相同主题
- 深度对齐：书籍在不同深度上的重叠区域
- 边界互补性：一本书的局限在哪里是另一本书的优势
- 风格调和：识别并解决风格冲突
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.2 --status completed`

#### 1.3 目标目录 (Target TOC)
- 设计目标目录结构
- 每个章节必须有明确的目的和源材料映射
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.3 --status completed`

#### 1.4 逐章计划 (Per-Chapter Plans)
为每个章节编写详细的整合计划：
- 源材料贡献图（主要/次要/参考）
- 方法论选择及理由
- 深度目标和实现策略
- 内容合成策略
- 空白填补需求
- 依赖链
- 预期产出（长度、代码数量、核心概念）
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.4 --status completed`

#### 1.5 反向覆盖 (Reverse Coverage)
- 构建反向覆盖矩阵
- 每个源章节必须映射到：目标章节 / 侧边栏 / 附录 / 明确排除
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 1 --sub-phase 1.5 --status completed`

#### 1.6 关卡（Gate 1）

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 1
```
- `source-architecture.md` 存在且包含所有必需章节
- `plan.md` 存在，包含每个目标章节的整合计划
- 每个计划包含：源映射、方法论选择、深度目标、合成策略、空白列表、依赖链
- 反向覆盖矩阵覆盖 100% 的源章节
- 没有"TBD"或占位符文本

### Phase 2：章节生成（每章 6 个子阶段）

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `references/full-integration.md`（不可略读）
- [ ] 完整阅读 `references/agent-orchestration.md`（不可略读）
- [ ] 重新阅读 plan.md 中该章节的整合计划
- [ ] 关卡（Gate 1）已通过，progress.md 中有证据
- [ ] 如有任何一项未勾选：停止。不得继续。

#### 2.1 加载计划与源材料 (Load Plan + Sources)
- 加载 plan.md 中该章节的整合计划
- 加载相关知识索引章节
- 加载 source-architecture.md 中的风格基线
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.1 --chapter <chapter> --status completed`

#### 2.2 解构与重写 (Deconstruct & Rewrite)
执行 5 步重写：
1. 解构所有源材料的相关内容
2. 设计新的章节结构（不照搬任何源材料的原始结构）
3. 为每个小节分配主要/次要源材料
4. 以统一风格重写
5. 添加标记：`<!-- integrated: [source]Ch[N]-[id] -->`
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.2 --chapter <chapter> --status completed`

#### 2.3 质量关卡 (Quality Gate, G1-G8)

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 2 <chapter>
```

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

- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.3 --chapter <chapter> --status completed`

#### 2.4 进度记录 (Progress Record)
- 在 progress.md 中记录 Gate 结果
- 仅当 Gate 通过后才可进入下一章
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.4 --chapter <chapter> --status completed`

#### 2.5 批量检查（每 5 章）(Batch Check)

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 2b
```
- 跨章节术语一致
- 源不可辨识测试（从不同章节随机抽取 3 段）
- 叙事弧在章节间连贯
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.5 --status completed`

**子 Agent 策略**：
- 一次处理一个章节（顺序执行）
- 单个章节内：最多 3 个小节 Agent 并行
- Gate 失败 = 重写章节（不累积修复）

**失败 = 重写章节。不得继续。不得将问题累积到 Phase 3。**

#### 2.6 组装 (Assemble)
所有章节生成后，组装最终书籍：
- 创建 HTML 脚手架（`references/book-assembly.md`）
- 集成 CSS/JS
- 构建导航和交叉引用
- 命令：`python scripts/workflow.py generate-book <run_dir> record_progress --phase 2 --sub-phase 2.6 --status completed`

**输出**：`output/{chapter}.html` 文件，每章一个，加上带导航的组装书籍

### Phase 3：验证 (Validation)

**执行操作**：
1. 对所有章节运行覆盖率验证
2. 术语一致性检查（全书检索）
3. 代码可运行性检查（所有代码块）
4. 风格一致性（阅读来自不同部分的 3 个连续章节）
5. 交叉引用完整性（所有章节链接有效）
6. 反向覆盖：验证 100% 源材料已处理

**Coverage Guardian（覆盖守护者）检查**：
```bash
python scripts/workflow.py generate-book <run_dir> coverage_report
python scripts/workflow.py generate-book <run_dir> coverage_guard
```

**自动检查脚本**：

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/validate_tech.py output/
python scripts/validate_terms.py output/
python scripts/workflow.py generate-book <run_dir> check_gate 3
```

**关卡（Gate）**：
- 覆盖率 >= 95%
- 所有术语一致
- 所有代码可运行
- 所有交叉引用有效
- 章节之间无风格跳跃
- Coverage Guardian：无章节低于底线（总标记数的 10%）
- Coverage Guardian：无章节低于单章最低要求（3 个标记）

### Phase 4：报告 (Report)

**⚠️ 本阶段启动前必须完成：**
- [ ] 完整阅读 `shared/report-templates.md`（不可略读）
- [ ] 关卡（Gate 3）已通过，progress.md 中有证据
- [ ] 如有任何一项未勾选：停止。不得继续。

**执行操作**：编写 `report.md`，包含摘要、每章评分、问题列表、覆盖矩阵、已知限制、Coverage Guardian 结果。

**关卡（Gate 4）**：

*（执行标准关卡自检清单，见文件顶部。）*

```bash
python scripts/workflow.py generate-book <run_dir> check_gate 4
```
- report.md 存在
- 包含：摘要、评分、问题列表、修复批次、覆盖矩阵
- Coverage Guardian 结果已包含

---

## Coverage Guardian（覆盖守护者）

**用途**：检测并防止覆盖缺口、偷工减料和表面化整合。

**规则**：

1. **底线规则 (Floor Rule)**：任何源书籍在整合书籍中的标记数不得少于总标记数的 10%。如果某个源低于底线，标记为待审查并扩展。

2. **单章最低要求 (Per-Chapter Minimum)**：如果某个源书籍被映射为某章的"主要"或"次要"来源，则在该章中必须有 >=3 个整合标记。被映射的源零标记 = 自动失败。

3. **补丁式检测 (Patch-Style Detection)**：如果某个源书籍的标记全部出现在 <=2 个章节中，或者其标记从未作为任何小节的第一个/主要标记出现，则标记为补丁式整合。

4. **输出大小守护 (Output Size Guard)**：章节输出大小必须 >= 其整合的最大源章节大小的 80%。更小 = 可能存在内容丢失。

**在单源模式下**，Coverage Guardian 检查天然满足（一个源 = 100% 权重）。跳过按源比例和补丁式检测。仅检查：输出大小 >= 源文件的 80%，所有内容已翻译。

**命令**：
```bash
python scripts/workflow.py generate-book <run_dir> coverage_report
python scripts/workflow.py generate-book <run_dir> coverage_guard
```

**Coverage Guardian 运行时机**：
- Phase 2 完成后（全量扫描）
- Phase 3 验证中
- Phase 4 报告中

## 反偷工减料规则 (Anti-Slacking Rules)

遵循 `shared/anti-slacking.md`：
- 每个阶段开始时：重新阅读参考文件，在 progress.md 中记录阅读确认
- 每次声称的阅读：附带结构证据（段落数、代码块数、具体术语）
- 没有"我记得"——始终重新阅读
- 没有只凭标题推断——打开文件阅读实际内容
- 没有"大约"——Gate 要么通过要么失败，没有部分通过
- 不跳过子阶段——每个子阶段必须完成并记录后才能进入下一个
- 在单源模式下，验证 1:1 段落映射而非整合标记

## 子 Agent 编排 (Sub-Agent Orchestration)

完整规则见 `references/agent-orchestration.md`。关键约束：

1. **最大并发数**：5 个 Agent 同时运行
2. **Phase 0（多源）**：每本书一个 Agent，最多 3 本书并行。单本书内：顺序阅读章节。
3. **Phase 0（单源）**：顺序阅读章节，一个 Agent。
4. **Phase 1（多源）**：单个 Agent（架构设计需要全局视角，不适合并行）。
5. **Phase 1（单源）**：单个 Agent 翻译，逐章顺序执行。
6. **Phase 2（多源）**：一次一个章节。单章内：最多 3 个小节 Agent 并行。
7. **Phase 2（单源）**：组装 Agent，顺序执行任务。
8. **Phase 3**：验证 Agent 可并行运行（最多 3 个）。
9. **依赖顺序**：对于网页源，在进入下一页之前，先解析当前页面的所有链接/引用。
10. **错误恢复**：失败的 Agent = 用不同方法重试一次。第二次失败 = 暂停并询问用户。

## 质量标准 (Quality Standards)

- 读者无法辨识内容来源（多源模式）
- 章节骨架通过反向覆盖检查（多源模式）
- 每项新增内容都有来源、位置、收益说明
- 重复内容已合并或交叉引用
- 输出可通过 `report.md` 进入 review-tech-book 流程
- 整合等级：仅限 L3（重组）或 L4（完全融合）——参见 `references/full-integration.md`（多源模式）
- 自然的中文，无翻译腔（单源模式）
- 保持 1:1 段落映射（单源模式）
- 术语、编号、导航、图片、代码注释在首次通过时即正确

## 失败模式识别 (What Failure Looks Like)

### 失败模式 1：跳过重新阅读
- **模型说**："我之前已经加载了翻译规则" / "我记得整合计划"
- **真相是**：上下文被压缩过，规则已经模糊，计划细节被遗忘
- **检测方法**：progress.md 中缺少本阶段的阅读确认
- **修复方法**：重新阅读文件，记录确认及结构证据（行数、关键规则）

### 失败模式 2：只凭标题推断
- **模型说**："第 5 章讲函数，所以包括参数、返回类型、重载"
- **真相是**：第 5 章讲的是函数对象和 lambda，不是基础函数
- **检测方法**：证据使用了适用于任何关于"函数"章节的泛化术语
- **修复方法**：打开文件，阅读完整内容，用文本中的具体术语重新记录证据

### 失败模式 3：绕过 Gate
- **模型说**："Gate 通过了——所有检查看起来都不错" / "覆盖率足够了"
- **真相是**：Gate 脚本从未实际运行；覆盖率是估算的，不是测量的
- **检测方法**：progress.md 中没有粘贴脚本输出；没有标记计数
- **修复方法**：运行 Gate 命令，粘贴完整输出，用证据验证通过

### 失败模式 4：内容缩减
- **模型说**："章节生成成功"
- **真相是**：源章节有 40 段，输出只有 15 段（37% 覆盖率）——内容被概括而非翻译/整合
- **检测方法**：输出文件 < 源章节大小的 80%；段落数不匹配
- **修复方法**：扩展输出以匹配源深度。补充缺失的小节。重新运行 Gate。

### 失败模式 5：补丁式整合（仅多源模式）
- **模型说**："所有源都已整合"
- **真相是**：一个源贡献了 80% 的标记，其他源只出现在 1-2 个章节中
- **检测方法**：Coverage Guardian 显示底线规则违规；单章最低要求未满足
- **修复方法**：在受影响章节中扩展代表性不足的源的贡献


## 参考文件 (Reference Files)

| 文件 | 用途 | 适用模式 |
|------|------|----------|
| `references/agent-orchestration.md` | 子 Agent 规则和约束 | 两种模式 |
| `references/knowledge-index-format.md` | 知识索引结构 | 多源 |
| `references/book-architecture.md` | 架构设计指南 | 多源 |
| `references/full-integration.md` | 整合等级和重写方法 | 多源 |
| `references/integration-discipline.md` | 整合纪律规则 | 多源 |
| `references/synthesis-methodology.md` | 内容合成方法 | 多源 |
| `references/quality-gate.md` | 质量关卡规范 | 多源 |
| `references/context-passing.md` | Agent 之间的上下文传递 | 两种模式 |
| `references/translation-rules.md` | 翻译规则和指南 | 单源 |
| `references/book-assembly.md` | HTML 组装和脚手架指南 | 两种模式 |
| `shared/translationese-patterns.md` | 翻译腔检测模式 | 单源 |
| `shared/anti-slacking.md` | 反偷工减料规则 | 两种模式 |
| `shared/report-templates.md` | 报告格式模板 | 两种模式 |
