---
name: review-tech-book
description: "Structured quality review of technical books. Default: report only, fix mode only when user explicitly requests. Trigger: review book, 审阅这本书, 审阅书籍, quality review, 质量审阅, optimize issues, 修复这些问题, review tech book, 检查这本书, 书籍审阅. Use this skill whenever the user wants to review, audit, or assess the quality of a technical book — even if they don't say 'review'. Do NOT trigger for: generating books (use generate-book), code review, API review."
---

# 审阅技术书籍

技术书籍的结构化质量审阅。默认模式：仅出报告。修复模式：仅在用户明确请求时启用。

## 核心规则

**先阅读以下两个文件**：
- `references/review-shared-rules.md` — 铁律、预检、关卡自检、反合理化、证据等级体系、发现质量控制、失败模式、质量标准
- `shared/discipline-framework.md` — Gate 降级方案、错误恢复协议、进度追踪

关键原则：
- 没有直接引用就没有发现。不跳过关卡。不只扫不读。不浅层打分。
- 每个阶段开始时重新阅读参考文件，在 progress.md 中记录确认
- **启动前必须通过预检**（见 review-shared-rules.md「预检清单」）
- **崩溃后从 progress.md 恢复**，不从头开始

## 🔴 反模式（等于失败，不要做）

命中即视为产出不合格。下面只列各阶段特有的高危信号；更多偷工模式见 `references/review-shared-rules.md`「发现质量控制」「失败模式识别」与 `shared/anti-slacking.md`。

- **无引用发现 / 证据不配级**（全阶段）：没有原文逐字引用 + 行号就写发现；或 🔴/🟠 问题却只有 V1 证据、V4 推断不降级且不标「未经验证」。
- **只扫不读**（P1–P2）：扫描结构后声称「已审阅」，发现项用泛泛描述而非具体段落 / 代码行。
- **跳过章节**（P2）：略读阶段跳过任何章节（所有章节必须至少略读）。
- **浅层 / 均匀打分**（P3）：所有维度都打 7/10，或评分无直接引用支撑。
- **伪造 Gate**（全阶段）：没跑 `validate_code.sh` / 关卡检查就标「通过」。

## 工作流

```
阶段 1: 扫描 → 阶段 2: 精读 → 阶段 3: 打分 → 阶段 4: 报告 → [修复模式]
```

> 🔴 **CHECKPOINT · 启动前确认（STOP）**：进入阶段 1 之前**必须暂停向用户确认**审阅目标（哪本书 / `output/` 目录路径）——审阅耗时，对象搞错 = 白跑。模式无须在此问：默认仅出报告；修复模式须用户显式开启且已有完整 `report.md`。确认 OK 再进入阶段 1。

**阶段锁**：进入任何阶段前，运行 Gate 检查：
```bash
python ../shared/workflow.py review-tech-book <run_dir> check_gate <phase>
```
Gate 失败则修复后重试。如果 workflow.py 不可用，使用手动 Gate 检查（见 review-shared-rules.md「Gate 降级方案」）。

## 阶段 1：扫描 (Scan)

**⚠️ 启动前**：阅读 `references/spec.md` 和 `references/execution-guardrails.md`，在 progress.md 中记录确认。

**执行事项**：
1. 批量扫描：结构、逻辑、代码密度、术语、翻译痕迹
2. 定义目标读者
3. 绘制学习路径图
4. 运行：`scripts/validate_code.sh output/`

**输出**：`findings/phase1.md`

**Gate 1**：目标读者已定义，学习路径已绘制，异常项已列出并标注类型，问题已分类。

## 阶段 2：精读 (Read)

**⚠️ 启动前**：阅读 `references/reviewer-discipline.md`，在 progress.md 中记录确认。Gate 1 已通过。

**第一轮：略读所有章节**（不允许跳过）
- 检查：事实性声明、术语、教学流程、格式
- 标记：🔴（需要深读）或轻微问题
- 每章证据：段落数 + 核心内容 + 3 个以上术语

**第二轮：深读**
- 标记对象：第一轮中标记为 🔴 的章节
- 必须深读：首章、末章、代码密集章节、核心概念章节

**发现格式**：
```
### [N]. [章节] [标题] [🔴/🟠/🟡]
- **位置**：`ChX line NNN-NNN`
- **原文**：[原文引用]
- **问题**：[具体分析]
- **证据**：[V1/V2/V3/V4]
- **影响**：[对读者的影响]
- **修复**：[具体修复方法]
```

**没有直接引用 = 无效发现。不要写。**

**输出**：`findings/phase2.md`

**Gate 2**：所有章节已略读，深读章节包含直接引用，🔴/🟠 问题至少达到 V2 证据等级，至少 2 个章节已进行代码验证。

## 阶段 3：打分 (Score)

**⚠️ 启动前**：阅读 `references/excellence-dimensions.md`，在 progress.md 中记录确认。Gate 2 已通过。

**执行事项**：
1. 对风险维度进行打分（仅基于证据）
2. 对五大转化维度进行打分
3. 标记跨章节反模式

**输出**：`findings/phase3.md`

**Gate 3**：所有维度已评分（每个评分有具体证据），跨章节反模式已标记，无"全部 7 分"式均匀评分。

## 阶段 4：报告 (Report)

**⚠️ 启动前**：阅读 `shared/report-templates.md`，在 progress.md 中记录确认。Gate 3 已通过。

**执行事项**：撰写 `report.md`，包含：
- 执行摘要
- 评分总览
- 前 3 优势、前 3 问题
- 学习路径 + 断点
- 问题分类
- 系统性问题
- 修复批次：P0（错误）、P1（结构）、P2（风格）、P3（参考）

**自动检查**：
```bash
scripts/validate_code.sh output/
python ../shared/validate_tech.py output/
python ../shared/validate_terms.py output/
```

**自我审计**：事实性声明有引用+证据等级；无微小修复模式；🔴 严重程度已校准；范围与模式匹配；分类正确。

**Gate 4**：所有必需章节已呈现，发现项包含直接引用，评分有证据支撑。

## 修复模式 (Fix Mode)

**仅在用户明确请求时启用。**

**⚠️ 启动前**：阅读 `references/apply-fixes.md`。Gate 4 已通过（报告已完成）。用户已明确请求修复。

**执行事项**：
1. 加载最新的 `report.md`
2. 提取 P0→P3 各批次
3. 执行 P0 → 验证 → P1 → 验证 → P2 → 验证 → P3 → 验证
4. 每批次后：运行 `validate_code.sh`，检查 HTML、导航、编号

**输出**：`fix-report.md`

**Gate Fix**：全部 4 个批次已完成，每个批次已通过验证。

## 参考文件

| 文件 | 用途 | 使用阶段 |
|------|------|----------|
| `references/review-shared-rules.md` | 铁律、预检、关卡自检、Gate 降级、错误恢复、进度追踪、失败模式、质量标准 | 全部 |
| `references/spec.md` | 审阅规范定义 | 阶段 1 |
| `references/execution-guardrails.md` | 执行护栏规则 | 阶段 1 |
| `references/reviewer-discipline.md` | 审阅纪律要求 | 阶段 2 |
| `references/excellence-dimensions.md` | 卓越维度评分标准 | 阶段 3 |
| `references/apply-fixes.md` | 修复执行指南 | 修复模式 |
| `references/quality-reference.md` | 质量参考基准 | 阶段 3 |
| `references/teaching-reference.md` | 教学参考基准 | 阶段 2 |
| `shared/report-templates.md` | 报告格式模板 | 阶段 4 |
| `shared/anti-slacking.md` | 反偷工减料规则 | 全部 |
| `shared/validate_tech.py` | 技术准确性验证脚本 | 阶段 4 |
| `shared/validate_terms.py` | 术语一致性验证脚本 | 阶段 4 |
