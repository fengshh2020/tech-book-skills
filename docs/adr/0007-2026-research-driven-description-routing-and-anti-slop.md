# 0007 — 2026 研究驱动重构：description 路由化 + 反 AI 腔（slop）

承接 [0005](0005-trim-scaffolding-for-capable-models.md)（裁剪脚手架）/ [0006](0006-generalize-and-consolidate.md)（泛化 + 合并）。本 ADR 记录 2026-07 针对"最新 skill 设计潮流 + AI 内容生成质量共识"的调研驱动重构。

## 背景（调研依据，2026-07）

- **Anthropic Agent Skills 官方规范**（2025-10 发布；[agentskills.io](https://agentskills.io) 2025-12 开放 spec）：progressive disclosure 三级加载（metadata 恒载 ~100 token / 触发载 SKILL.md <5k / 按需载 references）；**description 是"何时触发"的路由规则**（`Use when…`，frontmatter ≤1024 字符），不应复述流程（流程在正文）。`disable-model-invocation: true` 区分模型触发 vs 用户触发。
- **AI 内容质量共识**：「slop」一词 2024 初由 Charlie Warzel（The Atlantic）等提出并流行；其本质被 Wikipedia「AI 生成文特征」概括为**"回归均值是唯一大信号"**，[arXiv:2509.19163](https://arxiv.org/html/2509.19163v1) 把 slop 操作化为 Repetition / Templatedness / low Coherence / low Density / wrong Tone / low Relevance。AI 过用词实证来自 Kobak et al. 2024（*Science Advances*，14M PubMed 摘要，delves ×25.2）与 Juzek & Ward 2025（COLING）；Paul Graham 2024-04 推文以 *delve* 为标志引爆讨论（注：流传的"AI 词表"非 PG 所列，乃上述学术研究；"delve"在西非 / 印度英语里正常，词表只作警告不作定罪）。Karpathy 的相关立场是"AI 产出是待读的草稿、非可接受交付物；人拥有判断"（nanochat 全手写、AI agent "net unhelpful"）——与本库铁律「真读 / 不伪造」同向。共识：**密度 > 出现，结构 > 词汇**——单次词汇命中弱，结构 tell（三联排比 / 万能开头 / 复述结尾 / 假平衡）直接判。
- **工艺锚点**（均有来源）：Winston *How to Speak*（near miss「几乎对但不对」的对照、贡献式结尾不复述）、Julia Evans（写给过去的自己）、Dan Luu（具体压倒抽象）。

## 决策

1. **description → 路由规则**：三个 skill 的 description 改写为「`Use when…` + 触发短语 + 负路由（Do NOT trigger for…）」，删去复述流程的散文（book/doc 形态、builder 流水线等——已在正文）。**所有触发短语保留**（0005 约束），只删散文、重组顺序。take-note 本就 `Use when` 起步，仅删两句 what-it-does。
2. **第六类失败模式：AI 腔 / slop**：writing-core 失败模式从 5 类增至 6 类。slop 是 2026 模型**自身**会犯的真实风险——与 0005 裁剪的"防御性脚手架"不同（那针对偷懒 / 伪造 / 缩水，slop 针对**腔调 / 立场缺失**）。一行定义 + 治法 + 密度原则。
3. **`translationese-patterns.md` 扩域**：从「翻译腔」扩为「翻译腔 + AI 腔」，加 13 行高精度固定词模式（综上所述 / 不难发现 / 赋能 / delve / tapestry / seamless…）。**表格式与脚本耦合不变**（0006 约束）：`validate_code.sh` 一并读取两表，后备硬编码列表保持原翻译腔子集。**只收无管道、无误报的固定词**——与 ML 术语撞车的 `重塑`(reshape) / `深度融合`(deep fusion) 不收；需密度判断的语族（navigate the complexities / plays a crucial role / 赋能家族…）不进 blunt 计数器，交模型自检（与 0005「Gate 退化为正文自检」一致）。
4. **工艺锚点入 `review-criteria.md`**：教学理论节补 near miss / 贡献式结尾 / 写给过去的自己 / 具体压倒抽象。
5. **AI 腔 分布锚点**：writing-core 定义 → translationese-patterns 检测 → review-criteria/spec 反模式 → 各 reference 一行指针。概念**单源**（writing-core），各处只引用不重述。

## 关键约束（沿用 0005 / 0006）

- builder 契约（`md-authoring.md`）不动；校验脚本耦合不动（表格式不变）；light-only、mermaid→PNG 不动；**触发短语不动**。
- slop 检测以**模型自检为主、脚本 blunt 计数为辅**——脚本只数总数（既有行为，现为 WARNING 级），密度 / 语境判断归模型（直引 / 学术 / 法律豁免）。
- description 改写不删任何触发短语，只删流程散文（避免破坏用户调用习惯）。

## 收益

- description 全部转为 2026 路由规则形态，frontmatter 更短、路由更准、与正文单一源；
- 生成内容多一道"反通用腔"纪律（失败模式 + 检测 + 审阅三处），且不增防御性脚手架；
- review 多 4 条有来源的工艺判据。

## 回退路径

- 若某 AI 腔 lint 模式误报多：删该行（单行编辑，不影响其余模式或脚本）。
- 若 slop 自检失效：可在高风险阶段（多源 Phase 2、代码库写作）加显式 checklist（0005 既定回退路径）。
- 若 description 路由化导致漏触发：把对应触发短语加回（短语本就全部保留，仅散文被删）。
