---
name: review-tech-book
description: "Use when reviewing, auditing, or assessing the quality of a technical book or learning doc (book/doc 形态) — any tech stack, even without the word 'review'. Default: report only; fix mode only on explicit request. Triggers: review book, 审阅这本书, 审阅书籍, 书籍审阅, quality review, 质量审阅, 检查这本书, review tech book, optimize issues, 修复这些问题. Do NOT trigger for: generating books (use generate-book), code review, API review, or **atomic notes**（原子笔记过轻——note 质量由 take-note 写作时按 writing-core 自检兜住，不走 16 维审阅）."
---

# 审阅技术书籍 / 文档

结构化质量审阅。默认**仅出报告**；修复模式仅在用户明确请求时启用。任意技术栈通用。

**先读 `../shared/writing-core.md`**——铁律、证据等级 V1-V4、失败模式、校验工具都在那，本文件与各 reference 不再重述。审阅的铁律就是 writing-core 铁律在审阅侧的体现：**没有原文逐字引用 + 行号就没有发现；🔴/🟠 问题须 ≥V2 证据；不浅层均匀打分**。

## 启动前

向用户确认审阅对象（哪本书 / `output/` 目录路径）与范围（深度/标准/快速模式）——审阅耗时，对象搞错 = 白跑。模式无须问：默认仅报告；修复须用户显式开启且已有完整 `report.md`。确认 OK 再进入阶段 1。

## 工作流

```
P1 扫描 → P2 精读 → P3 打分 → P4 报告 → [修复模式，用户明确请求时]
```

每阶段进入前读对应 reference（按需读 = 上下文工程 Select），按其维度执行；阶段状态写 `findings/phaseN.md`（窗口外结构化记忆）；阶段结束按 writing-core 失败模式自检（假读 / 伪造校验 / 浅层均匀打分 / 推断当结论）。

### 阶段 1：扫描
读 `references/spec.md`（评分框架 + 输出模板）。批量扫结构/逻辑/代码密度/术语/翻译痕迹；定义目标读者；绘学习路径图；跑 `scripts/validate_code.sh output/`。输出 `findings/phase1.md`。

### 阶段 2：精读
读 `references/review-criteria.md`（反模式清单，对照识别问题）。**第一轮略读所有章节（不跳过）**，标 🔴（需深读）/轻微；每章证据：段落数+核心内容+≥3 术语。**第二轮深读**首轮 🔴 + 首章/末章/代码密集章/核心概念章。发现格式：

```
### [N]. [章节] [标题] [🔴/🟠/🟡]
- 位置：`ChX line NNN-NNN`
- 原文：[逐字引用，不可改写]
- 问题：[具体分析，非泛泛]
- 证据：[V1/V2/V3/V4 + 验证方法]   ← 🔴/🟠 须 ≥V2
- 影响：[对读者的具体影响]
- 修复：[可操作步骤，非"改进一下"]
```

没有直接引用 = 无效发现，不写。每 5 章批量检查（跨章术语一致、严重度/证据分布合理、去重）。输出 `findings/phase2.md`。

### 阶段 3：打分
读 `references/review-criteria.md`（五转化维度 + 工程实践标杆）。按 `references/spec.md` 十六维度（仅评有证据的）+ 五转化维度打分；标跨章节反模式。禁均匀打分（全 7/10）、禁无引用评分。输出 `findings/phase3.md`。

### 阶段 4：报告
读 `../shared/writing-core.md`（报告铁律）+ spec.md 报告模板。写 `report.md`：执行摘要、评分总览、Top3 优势/问题、学习路径+断点、问题分类、系统性问题、**可复利候选（→ wiki）**、修复批次（P0 技术错误 / P1 结构 / P2 风格翻译 / P3 参考体验）。**可复利候选**：系统性 + 跨书可复用的反模式/教训 → flag 为 wiki 候选；review **只 flag、不写库**，由 take-note INGEST（摘条进 `raw/`，非整份报告）。判据 + 模板见 `references/spec.md`，原理见 [ADR-0012](../docs/adr/0012-book-to-vault-handoff-via-take-note.md) / [ADR-0009](../docs/adr/0009-llm-wiki-paradigm-via-take-note.md)。跑自动校验并附结果：
```bash
scripts/validate_code.sh output/
python ../shared/validate_tech.py output/
python ../shared/validate_terms.py output/
```

## 修复模式（仅用户明确请求）

读 `references/apply-fixes.md`。加载最新 `report.md` → 提取 P0→P3 → 逐批执行。**MD 是源**：改 `{RUN}/src/*.md`（非手改 HTML）→ 重新跑 `generate-book/scripts/build_html.py` → 跑校验。翻译/整合/代码库问题按类别批量处理；发现新风险记 `fix-report.md`，不扩张范围。输出 `fix-report.md`。

## 参考文件

| 文件 | 内容 | 阶段 |
|---|---|---|
| `../shared/writing-core.md` | 铁律 / V1-V4 / 失败模式 / 校验工具 | 全部 |
| `references/spec.md` | 十六维度 + 五转化整合 + 报告模板 + 校验清单 | P1/P3/P4 |
| `references/review-criteria.md` | 4 类反模式 + 五转化维度 + 教学理论 + 工程实践标杆 | P2/P3 |
| `references/apply-fixes.md` | 修复模式：P0-P3 批次 + MD 源重建（非手改 HTML） | 修复 |
| `../shared/translationese-patterns.md` | 翻译腔模式（`validate_code.sh` 读取） | P2 |
| `../shared/validate_tech.py` / `../shared/validate_terms.py` | 技术准确性 / 术语一致性校验 | P4 |
