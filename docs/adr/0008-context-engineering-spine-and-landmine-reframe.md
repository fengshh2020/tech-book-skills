# 0008 — 上下文工程脊柱 + ETH「地雷」重定位

承接 [0005](0005-trim-scaffolding-for-capable-models.md)（裁剪脚手架）/ [0007](0007-2026-research-driven-description-routing-and-anti-slop.md)（路由化 + 反 slop）。本 ADR 把这套 skill **显式重定位为上下文工程产物**，并据 ETH Zurich 对上下文文件的研究把纪律源进一步收成「地雷文件」。

## 背景（调研依据，2026-07）

- **上下文工程成统领范式**：Tobi Lutke（2025-06-18）与 Andrej Karpathy（2025-06-25）提出术语——"the delicate art and science of filling the context window with just the right information for the next step"；**Anthropic《Effective Context Engineering for AI Agents》（2025-09-29）** 形式化为 "curating and maintaining the optimal set of tokens during LLM inference"，总律 **"find the smallest set of high-signal tokens that maximize the desired outcome"**。三招长程术：**Compaction**（先 recall 后 precision，保留架构决策与未解 bug，可逆）、**Structured Notes**（笔记持久化在窗口外、回拉）、**Sub-agent Isolation**（子任务开新窗口只回传结果）。Martin Fowler（2026-02-05）指出 Claude Code 领先，并区分"谁决定加载上下文"：LLM（Skills）/ 人（slash 命令）/ agent 软件（hooks）。**认知**：这三个 skill 本质就在策展长程生成时模型该看到什么——它们就是上下文工程。
- **ETH Zurich《Evaluating AGENTS.md》（2026-02-12，arXiv:2602.11988，138 实例 × 12 仓库 × 4 frontier agent）**：LLM 生成的上下文文件**比没有文件还差 3%、且贵 20%**；人写的也只 +4%。根因是**冗余**（罗列 agent 能自发现的结构）与**过度顺从**（agent 照无用指令照做）。结论：**上下文文件只该放 agent 自己发现不了的信息——团队决策、"地雷"、非显然工具用法**。"对 AI 最好的文档不是 markdown，是不需要它的代码。" 这把 [0005]（裁剪脚手架）再推一步：纪律源要更像"地雷清单"，而**真正值钱的是确定性脚本**（`build_html.py` / `validate_*`）。

## 决策

1. **总律入 writing-core**：顶部立「**最小高信号 token 集**」为贯穿原则——任一阶段只加载该阶段需要的高信号 token，不为"全面"预加载。`剪枝`节重写成上下文工程的 Select（按需读参考）/ Compress（摘要从全文压缩、不二次压缩）。
2. **writing-core「地雷」重定位**：保留**真地雷**（铁律、V1-V4、6 失败模式、不可妥协库约定、校验脚本入口、路径运行时），**删 agent 能自发现的论证散文**（每条原则"为什么重要"的废话——agent 已知为何，留着只稀释注意力，ETH 实证 -3%）。净效果：更短更密，规则全留、说教全删。新增一行「**不要在上下文里复述 agent 能自发现的结构**」（目录罗列、通用编程概念）。
3. **既有机制显式命名为上下文工程战术**：`generate-book` 的 `progress.md` = Structured Notes、multi-source 的 `context-summary.md`（≤150 行、每子阶段追加、下阶段只读摘要+本参考）= Compaction、`≤3 并行子 Agent` = Sub-agent Isolation。三个 SKILL.md 把这些**点名**为上下文工程战术（非新机制，是给既有做法正名），并补 compaction 的 recall-先-precision-后 心法。
4. **脚本即客观价值**：writing-core 校验工具节强化——`build_html.py` / `validate_*.{sh,py}` / `check_coverage.sh` 是 ETH 说的"不需要文档的代码"，与"是否信任模型自检"无关，是机械兜底。

## 关键约束（沿用 0005 / 0006 / 0007）

- 铁律 / V1-V4 / 失败模式（含第六类 slop）/ 库约定一律保留，只删论证散文。
- description 路由化（0007）、builder 契约（0001/0002）、light-only（0003）、mermaid→PNG（0004）、触发短语（0005）全不动。
- 不新增文件、不新增依赖；上下文工程是**框定**，不引入新机制。

## 收益

- writing-core 更短更密，净减论证散文，更贴合 ETH「只放不可发现」。
- 既有长程机制（progress/context-summary/并行）获统一术语，可读性与一致性上升。
- 总律「最小高信号 token 集」给"读哪些参考、何时停"一个统一判据。

## 回退路径

- 若删某段论证后发现模型不再遵守该规则：把规则**一句话**加回（不恢复说教散文）——这正是 ETH 的平衡点：留规则、删废话。
- 若上下文工程框定造成困惑：撤回 SKILL.md 的术语正名（纯措辞），writing-core 总律保留。
