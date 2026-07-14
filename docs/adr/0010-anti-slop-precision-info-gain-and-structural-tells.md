# 0010 — 反 slop 精确化：信息增量框架 + 结构 tell 细化

承接 [0007](0007-2026-research-driven-description-routing-and-anti-slop.md)（反 slop 三处守住）。本 ADR 不新增防线，只据 2026 新共识把既有 slop 纪律**精确化**——换更锋利的密度框架、补几个高精度词与结构 tell。

## 背景（调研依据，2026-07）

- **arXiv:2509.19163v2（2026-01-24，"Measuring AI Slop in Text"，NEU）**：WQRM 模型 + 专家逐句标注 150 篇新闻 + 100 QA，slop 六维（Repetition / Templatedness / low Coherence / low Density / wrong Tone / low Relevance）+ Factuality / Bias。**确认"问题数越多、质量越降"**——为 [0007]「密度即信号」提供量化背书。
- **Wikipedia《Signs of AI Writing》（MOS:AICLEAN，2026 权威词表）**：AI 词表（delve / tapestry / pivotal / underscore / foster / testament / enhance / crucial / intricate / landscape）+ **"tailing clauses"**（句尾现在分词堆意义）+ 堆叠原则（单标志非证、多标志堆叠才查）。
- **Olivia Cal（2026）17 tell + 黑名单**：低 **burstiness**（句长方差小 = AI）、**"perfect rectangle"段**（3 句各 15–20 词 SVO 的整齐段）、**"No X. No Y. Just Z."** 模式、虚词族（myriad / plethora / comprehensive / pivotal / unwavering / multifaceted）、花喻族（tapestry / landscape / beacon / journey / roadmap / symphony）。
- **PG / Saharia《NiemanLab》"AI irreducibility"（2025-12 → 2026）**：最锋利的密度框架——"没有摘要器能量出它砍掉的密度。杠杆不是'写更好'，是**相对摘要的信息增量**。""写得密到摘要都觉得空洞。" 即 **密度 = 抵抗被摘要的信息量**。

## 决策

1. **失败模式 6 换信息增量框架**（writing-core）：slop 治法从"写人话"升级表述为「**写不可被摘要压缩的信息**」——具体名词 / 确切动词 / 删套话 / 敢给观点 = 让每句都贡献摘要砍不掉的信息增量。密度即信号（[0007]）= 信息增量即信号。
2. **translationese-patterns 补高精度固定词**（沿用 [0007] blunt 计数器边界——只收无管道、无误报的固定词）：新增 `myriad` / `plethora` / `pivotal` / `underscore` / `foster` / `intricate` / `beacon`（技术写作里几乎只出在 AI 文）。**不收**易误报的 `landscape` / `journey` / `roadmap` / `symphony`（legit 技术语境常见）→ 交模型自检（与 [0007] 一致）。**动态读取即生效**——后备硬编码列表沿用 [0007] 约束（仅翻译腔子集，AI 腔词含新增者一律动态读取、不入后备）。
3. **结构 tell 精确化**（review-criteria / translationese-patterns 自检节）：[0007] 已收三联排比 / 万能骨架 / 复述结尾 / 假平衡 / 段长整齐无 burstiness；补三个更具体的：**完美矩形段**（3 句各 15–20 词 SVO 的整齐段）、**"No X. No Y. Just Z."** 三段式、**tailing clause**（句尾 `-ing` / 「……，从而实现……」式现在分词堆意义）。结构命中仍**直接判**（非词汇的警告级）。
4. **信息增量为 review 质量维度**：spec/review-criteria 的 B1 可读性 / B4 组织节奏补一条质性判据——「随机抽一段做摘要，若摘要几乎不丢信息 = 该段密度不足（slop 嫌疑）」。

## 关键约束（沿用 0007）

- blunt 计数器只数总数、WARNING 级、密度 / 语境判断归模型（直引 / 学术 / 法律豁免）。
- 新增词必须无 `\|` 管道、无 ML 术语撞车（故不收 `landscape` 等）。
- 表格式与脚本耦合不变（[0006]）；后备列表不变（仅翻译腔子集，[0007]）。

## 收益

- slop 纪律换上 2026 最锋利的「信息增量」框架，治法更可操作（写"摘要砍不掉的"比"写人话"更具体）。
- blunt 计数器多 7 个高精度词，结构 tell 多 3 个具体模式，误报不增（边界守住）。
- review 多一条可操作的密度判据（摘要法）。

## 回退路径

- 若某新词误报：删该行（单行编辑，[0007] 既定回退路径）。
- 若信息增量框架不如"写人话"好执行：两表述并存（"写不可被摘要压缩的信息 = 写人话的具体化"），不撤框架。
