---
name: research
description: "Investigate a question against high-trust primary sources and capture the findings as a structured Finding Block. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. Also used by other skills (tech-proposal, generate-book, review-tech-book) via inline invocation for directed research requests. Triggers: 调研, 查文档, 验证论断, research, investigate, look up docs, find out. Do NOT trigger for: designing solutions (use tech-proposal), generating content (use generate-book), recording notes (use take-note)."
allowed-tools: Read Glob Grep
---

# 调研

调研问题并返回带引用的结构化发现块。可被用户直接触发，也可被其他 skill 内联调用（指令式，非运行时 API）。

**先读 `../shared/writing-core.md`**——铁律、证据等级 V1-V4、失败模式都在那，本文件不再重述。

## 流程

**Plan → Search → Read → Synthesize**，自适应循环，最多 3 轮。每轮加深而非拓宽。

### ① Plan（查询分解）

读 `references/search-craft.md`（查询分解 / 来源质量 / 迭代策略）。

将问题拆为可独立回答的子查询。每个子查询指定：
- 要回答什么
- 优先查什么源（官方文档 > 源码 > 一方 API > 社区文章）
- 证据等级要求

**定向调研请求**（被其他 skill 调用时）：调用方提供结构化请求——目标、需确认领域、证据等级要求、产出格式。直接用，不重新分解。

### ② Search

按子查询优先级搜索。来源优先级：

| 优先级 | 来源 | 信任度 |
|--------|------|--------|
| 1 | 官方文档 / spec / PEP / RFC | 最高 |
| 2 | 源码（GitHub / 本地） | 高 |
| 3 | 一方 API 文档 | 高 |
| 4 | 权威博客 / 技术委员会文章 | 中 |
| 5 | Stack Overflow / 社区回答 | 低（需交叉验证） |

**不接受的来源**：AI 生成的博客 / 未署名的转载 / 无原始引用的二手总结。

### ③ Read

实读找到的源，记录：
- 具体段落 / 代码行 / API 签名
- 证据等级（V1-V4）
- 与问题的关联

**不凭标题猜**——这是铁律。打开文件/页面完整读，记录段落数/代码块首行/术语位置。

### ④ Synthesize

读 `references/output-contract.md`（Finding Block 规范 / 置信度校准 / 可组合性协议）。

产出 Finding Block：

```
## Answer
{1-3 句直接回答}

## Evidence
- {论断} — [V{1-4} {类型}] — {来源：URL/文件:行号}
- {论断} — [V{1-4} {类型}] — {来源}

## Gaps
- {未解问题} — {为什么没找到答案}
- {未解问题} — {需要什么额外信息}

## Meta
- 来源数：{N}
- 置信度：{high/medium/low}
- 升级：{no/yes} — {理由}
```

### 迭代与升级边界

**迭代条件**：Gaps 非空且有可能通过追加搜索填补 → 进入下一轮（重新 Plan→Search→Read→Synthesize）。

🔴 **升级边界**（3 轮耗尽后仍有 Gaps——关键决策点：到此停下交付，不再硬凑轮次）：
- 产出 `升级: yes` 的 Finding Block
- Gaps 诚实列出，不伪造也不扣留
- 已找到的部分答案正常产出
- 调用方可选择：接受部分答案 / 标为待定 / 换用 runtime 提供的更重调研能力（若有——非功能前提，research 自身能处理任何问题）

**不建多级 tier**（quick/moderate/deep）——深度由迭代次数控制，非固定分类。

## 产出落点

- **被其他 skill 内联调用**：Finding Block 直接返回给调用方，不写文件
- **用户直接触发**：写成单篇 MD 文件，落项目目录或知识库（按 take-note 约定）

## 参考文件（按需读，不全读）

| 文件 | 内容 | 适用 |
|------|------|------|
| `../shared/writing-core.md` | 铁律 / V1-V4 / 失败模式 | 全部 |
| `references/search-craft.md` | 查询分解 / 来源质量 / 迭代策略 | ①② |
| `references/output-contract.md` | Finding Block 规范 / 置信度校准 / 可组合性 | ④ |
