---
name: review-tech-book
description: "Use when reviewing, auditing, or assessing the quality of a technical book or learning doc (original or translated, book/doc 形态) — any tech stack, even without the word 'review'. Default: report only; fix mode only on explicit request. Triggers: review book, 审阅这本书, 审阅书籍, 书籍审阅, quality review, 质量审阅, 检查这本书, review tech book, optimize issues, 修复这些问题. Do NOT trigger for: generating books (use generate-book), translating (use translate-book), code review, API review, or atomic notes（原子笔记过轻——note 质量由 take-note 写作时自检兜住，不走多维审阅）."
---

# 审阅技术书籍 / 文档

结构化质量审阅。默认**仅出报告**；修复模式仅在用户明确请求时启用。任意技术栈、原创或译作通用。

**先读 `../shared/writing-core.md`**——讲解质量三标准与反冗余红线就是审阅的尺子。审阅铁律：**没有原文逐字引用 + 行号就没有发现；技术错误级指控必须自己复核**（跑代码 / 查源码 / 查官方文档），复核不了的标「疑似」，不写死。

## 核心回路

**通读全书（不跳章）→ 找真问题（原文 + 行号 + 类别 + 严重度）→ 出报告**

🛑 **开跑对齐走 `../shared/kickoff.md`**，决策：审阅对象、范围（深度 / 标准 / 快速）——对象搞错 = 白跑。模式无须问：默认仅报告；修复须用户显式开启且已有完整 `report.md`。发现统一记进**一个** `findings.md`（窗口外 scratchpad）。

### 通读

起步先读 `{RUN}/progress.md` 的结构决策与生产者自检记录（book-project 状态契约）——生产者标注过的薄弱点是先验地图，但不替代审阅者自己的通读与判断。第一轮略读**所有**章节（不跳过）标 🔴（需深读）；第二轮深读 🔴 章 + 首末章 + 代码密集章 + 核心概念章。跑校验（book 形态，要求 HTML；doc 形态跳过、模型自检）：

```bash
../shared/scripts/validate_code.sh output/    # 代码格式与编号 / 术语 / 断链 / 翻译腔AI腔；套件全表见 writing-core
```

**两种镜头分开跑，防互相遮蔽**：质量通读（讲解 / 冗余 / 叙事 / 腔调——文学式细读）与技术复核（P0——对抗式验证）是两种姿态，沉浸在文笔里会漏技术错误，专注复核 API 会漏叙事断裂。长书可按章分片并行审——子任务无共享上下文，每片喂全六类信号清单 + 发现格式；回传后合并去重再出报告。

### 找真问题（六类；每类识别信号与正反例见 references/review-criteria.md）

| 类别 | 严重度 |
|---|---|
| 技术错误（过时 API、不可运行代码、错误论断——须复核实锤） | P0 |
| 讲解不足（跳步、定义先行无动机、代码贴了不讲、边界缺失） | P1 |
| 冗余与装饰结构（同一知识点 / 代码多处讲；章前目标 / 章末小结 / 练习题） | P1 |
| 叙事断裂（节间无衔接、知识点堆叠、列表替代讲解） | P2 |
| 一致性（术语多译名、风格 / 深度 / 编号跳变、交叉引用断） | P2 |
| 翻译腔 / AI 腔（对照词表；结构 tell 直接判） | P2 |

**发现格式**（没有原文逐字引用 = 无效发现，不写）：

```
### [N]. [章节] [标题] [P0/P1/P2]
- 位置：`ChX line NNN-NNN`
- 原文：[逐字引用，不可改写]
- 问题：[具体分析，非泛泛]
- 证据：[怎么复核的：跑了什么 / 查了什么；查不了标「疑似」]
- 修复：[可操作步骤，非"改进一下"]
```

### 抽查讲透度（审阅最重要的一步）

每章抽 1-2 个核心知识点，按 writing-core 检验法判：读者读完能复述"是什么、为什么、什么时候用"吗？代码能说清每一段在干嘛吗？答不上 = P1，写明缺了链条的哪一环（动机 / 机制 / 示例 / 边界 / 走读）。

### 出报告

写 `report.md`：

1. **总评**：一段话——适合谁、最大优势、最大问题、可用性结论（可用 / 修复后可用 / 需重写）。
2. **系统性问题**：跨章模式（如"全书代码普遍无走读""每章末尾都有小结复述"）。
3. **问题列表**：按 P0 → P1 → P2 排序，用上述发现格式。
4. **修复批次建议**：P0 技术错误 / P1 讲解与结构 / P2 风格一致性。

系统性、跨书可复用的教训 flag 给用户（可经 take-note 进 wiki）——review **只 flag、不写库**。

## 修复（用户明确请求时）

🛑 **进入修复前再确认**——改源 MD 并重建是破坏性操作。修复是**工作区操作而非审阅者的模式**：分批顺序（P0→P1→P2）、MD 源纪律（改 `src/*.md` 不手改 HTML）、重建重校——全在 `../shared/book-project.md`「修复操作」节。

## 参考文件（按需读，不全读）

| 文件 | 适用 |
|---|---|
| `../shared/writing-core.md` | 全部（先读） |
| `references/review-criteria.md` | 找问题：六类信号 + 正反例（分片子任务必喂） |
| `../shared/translationese-patterns.md` | 腔调类 |
| `../shared/book-project.md` | 通读起步 · 修复 |
| `../shared/kickoff.md` | 开跑前 |
