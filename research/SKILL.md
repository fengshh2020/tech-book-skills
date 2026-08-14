---
name: research
description: "Investigate a question against high-trust primary sources and capture the findings as a structured Finding Block. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. Also used by other skills (tech-proposal, generate-book, review-tech-book) via inline invocation for directed research requests. Triggers: 调研, 查文档, 验证论断, research, investigate, look up docs, find out. Do NOT trigger for: designing solutions (use tech-proposal), generating content (use generate-book / translate-book), recording notes (use take-note)."
allowed-tools: Read Glob Grep
---

# 调研

调研问题并返回带引用的结构化发现块。可被用户直接触发，也可被其他 skill 内联调用（指令式，非运行时 API）；内联调用时可后台并行跑，调用方继续主线，回传 Finding Block。

铁律（见 `../shared/writing-core.md`）：不伪造、推断必须标明、来源必须具体。**宁可诚实说"没查到"，不硬凑答案。**

## 核心回路

**拆问题 → 查 → 实读 → 带引用作答**

1. **拆**：把问题拆成可独立回答的子查询，每个定"要回答什么 + 优先查什么源 + 怎么验证"。查询分解 / 来源质量 / 迭代策略见 `references/search-craft.md`。（被其他 skill 调用时：直接用调用方的结构化请求，不重新分解——模板见 search-craft.md。）
2. **查**：按来源优先级搜——官方文档 / spec > 源码 > 一方 API 文档 > 权威博客 > 社区（社区仅作线索，不作证据）。**不接受**：AI 生成的博客、未署名转载、无原始引用的二手总结。
3. **实读**：打开命中的源完整读，记具体段落 / 代码行 / API 签名 + 出处。
4. **答**：产出 Finding Block（下）。

**答不全就再来一轮**（换关键词 / 换源类型 / 追已有来源里的线索），**最多 3 轮**。仍答不全 → 交付部分答案 + 诚实 Gaps，不硬凑轮次、不伪造。

## Finding Block（产出契约）

```markdown
## Answer
{1-3 句直接回答。有明确答案就给，没有就说"未找到确定性答案"。}

## Evidence
- {论断} — [{实测 | 源码 | 文档 | 推断}] — {来源：URL / file:line / 文档章节}

## Gaps
- {未解问题} — {为什么没找到：源不存在 / 访问受限 / 需实机验证}

## Meta
- 来源数：{N}
- 置信度：{high（≥3 独立来源交叉验证）/ medium（1-2 个来源）/ low（单源或来源可信度低）}
- 需升级：{no / yes — 3 轮耗尽仍有 Gaps，调用方应考虑换更重的调研手段或标待定}
```

规则：每条论断单独一行、来源必须具体到可复查；严重论断须 ≥2 个独立来源或 1 个一手源（官方文档 / 源码 / 实测），不接受推断；推断标「推断」并写明依据。Gaps 非空 ≠ 调研失败——部分答案照常交付。

**落点**：被其他 skill 调用 → 直接返回块，不写文件；用户直接触发 → 写成单篇 MD（落点按 take-note 约定）。

## 参考文件（按需读，不全读）

| 文件 | 内容 | 适用 |
|---|---|---|
| `../shared/writing-core.md` | 铁律 / 反 AI 腔 | 全部 |
| `references/search-craft.md` | 查询分解 / 来源质量 / 迭代策略 / 工具兜底 | 拆与查 |
