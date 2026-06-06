---
name: review-tech-book
description: "Use when reviewing/evaluating quality of a technical book — translated, integrated, codebase-generated, or any educational content. Produce structured quality report with findings, scores, and repair plans. Trigger on: 审阅这本书, review the book quality, check quality, evaluate this book. Do NOT trigger for: code review, translating (use translate-book), merging (use integrate-books), generating from code (use codebase-book)."
---

# Review Tech Book

对技术书籍进行结构化质量审阅，覆盖技术准确性、阅读体验、教学设计、读者转化和修复批次。默认只报告，不直接修改产出。

## 核心约束

**每条发现必须有原文摘引**。没有原文摘引的发现 = 无效，不得写入报告。原文摘引必须是从源文件实际读取并复制的文本，不是改写或凭记忆描述。为什么？实际审阅中出现了多次"声称学习目标包含 X/Y/Z，但源文件根本没有"的情况——没有摘引就无法验证。

**严重问题必须有证据等级**。🔴 标记至少 V2（读取了源文件对应行），🟠 标记至少 V2。API 移除时间线断言必须 V1 或 V3。V4 推断不得标记为严重。为什么？实际项目中审阅者声称 `link_to()` 在 Python 3.10 被移除（V4 推断，且推断错误），如果标注了等级，读者会知道这条未经实机验证。

**默认只报告不修复**。翻译/整合/代码库书籍问题回溯原 skill。只有用户明确要求才修改文件。为什么？审阅者直接修复翻译措辞时，不了解原始翻译上下文，容易引入新问题。

## 引用文件

每个阶段开始前执行该阶段的读取指令。

| 阶段 | 必读文件 | 读取目标 |
|------|----------|----------|
| 启动 | `../shared/progress-protocol.md` | 运行发现和恢复协议 |
| 启动 | `../shared/agent-compatibility.md` | 路径变量 |
| 启动 | `references/execution-guardrails.md` | 模式锁定、证据预算、发现上限 |
| 阶段 1 | `references/spec.md` | 审阅范围和评分标准 |
| 阶段 1 | `../shared/quality-ownership.md` | 质量归属和报告去重 |
| 阶段 1 | `../shared/runtime-pruning.md` | 审阅模式的剪枝和停止条件 |
| 阶段 2 | `references/reviewer-discipline.md` | 发现格式、反模式防护、自审清单 |
| 阶段 2 | `references/quality-reference.md` | 工程实践框架和标杆资源 |
| 阶段 3 | `references/excellence-dimensions.md` | 五转化维度 |
| 阶段 3 | `references/teaching-reference.md` | 反模式清单和教学理论 |
| 阶段 4 | `../shared/report-templates.md` | 报告模板 |

## 运行状态

先执行共享进度协议，使用 run slug `review`。运行目录形如：

```text
.book-doc/runs/{YYYYMMDD}-review-{label}/
```

本 skill 的关键状态：

- `progress.md`：模式、目标读者假设、已扫描范围、已精读章节。
- `findings/phase1.md`：全书扫描发现。
- `findings/phase2.md`：精读和技术验证发现。
- `findings/phase3.md`：维度评分和反模式发现。
- `report.md`：最终审阅报告。

幂等性检查：

- 阶段 1：`findings/phase1.md` 存在，且 `progress.md` 记录扫描范围。
- 阶段 2：`progress.md` 记录已精读章节，`findings/phase2.md` 有对应发现或无问题记录。
- 阶段 3：`findings/phase3.md` 存在，并记录评分范围。
- 阶段 4：`report.md` 存在，且包含验证摘要和自审结果。

## 模式

开始前**读取 `references/execution-guardrails.md`**，执行模式锁定并写入 `progress.md`。除非用户明确改变范围，不自动升级模式。

| 模式 | 场景 | 范围 |
|------|------|------|
| 深度模式 | 全面评估新书或交付前审阅 | 全阶段，完整十六维度 + 五转化维度 |
| 标准模式 | 日常质量审阅 | 全阶段；只评分有证据的风险维度 + 五转化维度 |
| 快速模式 | 已知问题复查或限定章节 | 阶段 1-2 + 4；不做完整维度表 |

运行护栏（来自 `references/execution-guardrails.md`）：

- **模式锁定**：模式写入 `progress.md` 后不得因发现变多而自行扩展。
- **证据预算**：按模式限制精读章节、代码/API 验证和代表性样本数。
- **发现上限**：同类问题合并为系统性发现；标准模式每个归属类别最多列 5 个问题。
- **停止哨兵**：新增发现不改变评分、严重程度、学习路径图或修复批次时停止扫描。
- **模式化评分**：审阅报告按模式收缩评分范围。深度模式完整评分；标准模式只评分有证据的风险维度和五转化维度；快速模式只给层面级结论。

## 流程

```text
Book Scan → Close Reading → Dimension Review → Report
```

发现增量写入 files，不依赖对话记忆回溯。

## 阶段 1：全书扫描

**读取 `references/spec.md`、`references/execution-guardrails.md`、`../shared/quality-ownership.md`**。

目标：建立全书概览、目标读者假设和高风险区域。

1. 查找前置报告：
   - 翻译产出：最新 completed `*-translate-*`。
   - 整合产出：最新 completed `*-integrate-*`。
   - 代码库书籍产出：最新 completed `*-codebase-*`。
2. 批量扫描章节结构、逻辑顺序、代码密度、排版一致性、术语模式、翻译腔、代码清单编号。
3. 写出目标读者假设：水平、阅读目的、使用方式、评价基准。
4. 绘制学习路径图：每章输入概念、输出能力、依赖关系和可能断点。
5. 运行自动化基线：

```bash
"${SKILL_DIR}/scripts/validate_code.sh" output/
```

6. 将问题归类为翻译质量、整合质量、代码库书籍质量或书籍本体问题。

关卡（逐项写入 `findings/phase1.md`）：
① 目标读者假设已写入
② 学习路径图已写入
③ 高风险章节已列出
④ `validate_code.sh` 摘要已记录
⑤ 问题类别清单已分类
完成所有 5 项后执行阶段完成协议。

## 阶段 2：精读

**读取 `references/reviewer-discipline.md` 和 `references/quality-reference.md`**。

目标：用 V1-V3 证据发现技术错误、代码问题和关键教学断点。

1. 选章并记录：在 `progress.md` 列出选中的章节编号。必须包含首章 + 末章 + 代码密集章 + 核心概念章，确保前/中/后分散分布。深度模式选 6-10 章；标准模式按证据预算选 4-6 章；快速模式只选目标问题相关章节。

2. 对每章：读取源文件 → 标注发现 → 写入 `findings/phase2.md`。每条发现必须使用以下结构化格式：

```
### [编号]. [章节] [简要标题] [严重程度标记]

- **位置**：`ChX 行NNN-NNN`
- **原文摘引**：从源文件实际读取并复制的原文片段（≥1 行，含行号）
- **问题/评价**：基于原文的具体分析
- **验证等级**：[V1]/[V2]/[V3]/[V4]
- **影响范围**：对读者的影响
- **建议修复**：具体修复方法（严重错误必须提供）
```

为什么强制此格式？"原文摘引"字段要求实际打开并读取源文件。如果无法提供原文摘引，说明没有真正读过源文件。

3. 对 API 存在性、版本兼容、代码行为等断言执行 V1-V3 验证。
4. 至少 2 章的代码示例必须实际运行或逐行审查（不能只声称已验证）。

**自检反模式**（来自 `references/reviewer-discipline.md` 的 7 个高频失败模式）：

- **内容填充**：声称源文件包含实际不存在的内容 → 必须有原文摘引
- **虚假修正**：纠正时引入新错误（如把"弃用"改成"移除"但版本号错）→ 版本断言必须 V1 或 V3
- **来源混淆**：把原文翻译当译者注 → 每条问题标注 [原文]/[译者注]/[审阅者评论]
- **范围膨胀**：把小问题描述为大问题 → 只描述原文证据能支持的范围
- **跳过验证**：对可运行验证的事实不做验证 → 至少 2 章实际运行代码
- **微修补循环**：每轮只修 1-3 处 → 按类别批量修复
- **越权修复**：直接修复翻译/整合问题 → 默认只报告，问题回溯原 skill

关卡（读取 `findings/phase2.md` 逐项确认）：
① 每条发现有原文摘引
② 🔴/🟠 标记至少 V2
③ API 时效断言达到 V1 或 V3
④ 至少 2 章有运行验证记录
完成所有 4 项后执行阶段完成协议。

## 阶段 3：维度评审

**读取 `references/excellence-dimensions.md` 和 `references/teaching-reference.md`**。

目标：根据模式进行评分和转化效果判断。

1. 深度模式逐项评估十六维度；标准模式只评估有证据的风险维度；快速模式跳过完整维度表。
2. 标准/深度模式评估五转化维度：读者旅程、首次成功、错误恢复、参考可用性、动机维持。
3. 标记跨章节反模式。

关卡：评分范围符合模式；每个评分都有证据或明确说明不评分。

## 阶段 4：报告

**读取 `../shared/report-templates.md`**（review-tech-book 无固定模板，结构如下）。

报告必须包含：

- 总评：适合谁、核心优势、最大问题、推荐度。
- 评分总览：十六维度评分表和五转化维度评分表，按模式收缩。
- 核心发现：优势 Top3 和问题 Top3。
- 目标读者与学习路径：目标读者假设、学习路径图摘要、主要断点。
- 问题归属分类：书籍本体问题、翻译质量问题、整合质量问题、代码库书籍质量问题。
- 逐章详细审阅：只覆盖已精读或模式要求的章节。
- 系统性问题：跨章节模式性问题，标注严重程度。
- 改进建议：高/中/低优先级。
- 修复批次：P0 技术错误、P1 学习路径与结构、P2 风格与系统性残留、P3 参考体验。
- 自动化验证结果：`validate_code.sh` 摘要。
- 收敛状态：停止哨兵、覆盖、失败项和残余风险。

报告生成后执行自审：

1. **事实性断言审计**：严重发现有原文摘引和验证等级。
2. **反模式复核**：未陷入逐点微修补、无证据评分或越权修复。
3. **严重程度校准**：高严重度确实影响理解、正确性或学习路径。
4. **范围校准**：模式和用户要求一致。
5. **归属校准**：翻译/整合/codebase/本体问题分类正确。

自审结果作为报告附录写入。

完成后将 `progress.md` 状态改为 `completed`。

## 审阅生成产出

### 翻译产出

读取 `*-translate-*` 报告的术语表和已知问题。额外检查翻译准确性、术语一致性、代码块完整性和格式规范性；只报告系统性残留，不替代 translate-book 的逐章 QA。

### 整合产出

读取 `*-integrate-*` 报告的统一术语表、来源占比、已知限制和验证结果。额外检查整合痕迹、风格一致性、内容重复度和拼贴感。

### 代码库书籍产出

读取 `*-codebase-*` 运行目录的 `report.md`。额外检查源码覆盖表、file:line 证据、代码摘录一致性、`validate_output.sh` 结果、源码可追溯性、架构讲解完整性和学习路径合理性。

## 质量标准

- 审阅结论建立在证据、模式和目标读者假设上。
- 报告按系统性问题和修复批次组织，不制造散点问题清单。
- 默认不修复文件；只有用户明确要求应用修复时才进入修改模式。
- 低层 QA 回溯到原生成 skill，审阅聚焦读者能否真正学会和使用。
