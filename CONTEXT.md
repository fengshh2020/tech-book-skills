# Tech Book Skills — 领域语言

本上下文界定这些技能的领域语言。任意技术栈通用。裁剪历史见 [ADR-0005](docs/adr/0005-trim-scaffolding-for-capable-models.md) / [ADR-0006](docs/adr/0006-generalize-and-consolidate.md)。

**KB_ROOT（知识库根）**：take-note 写入的知识库根目录——**动态解析、不硬编码**：从 cwd 向上找 `.kb-root` 或 `00_首页.md` 标记；找不到则问用户（指定已有 / 初始化新 / 就地生成）；`KB_ROOT` 环境变量可覆盖。项目名运行时扫 `$KB_ROOT/项目-*` 发现。见 [ADR-0011](docs/adr/0011-kb-root-resolution-and-portability.md)。_Avoid_：把 `/mnt/d/知识库` 这类具体路径写进 skill（那是实例，不是逻辑）。

**Book Artifact（书籍产物）**：生成出来的那本技术书/文档。同一份内容两种渲染。_Avoid_：文档、输出（太泛）。

**HTML Edition（HTML 版）**：书籍产物的交互式渲染，建立在"静奢"设计系统上（`style.css` + `script.js`，**light-only**（ADR-0003）/玻璃拟态/自适应层级/约 30 种组件）。由 [Builder](#) 从 MD 源渲染（ADR-0001）。_Avoid_：网页版、site。

**Markdown Edition（MD 版）**：可移植渲染，**通用/GitHub 方言**（无 frontmatter、无双链、无 callout），靠结构而非样式传达。MD 是**信息主源**，HTML 由 builder 从它渲染。_Avoid_：Obsidian 版（明确不选）。

**Builder**：`scripts/build_html.py`。读 MD 章节 + `book.yml` → 渲染 HTML 输出目录（含精简 style.css/script.js），承担 ADR-0002 的"务实子集"组件映射。封面/目录/导航等 chrome 由它注入，不由 agent 写。_Avoid_：渲染器、generator。

**Source（源）/ Input（输入）**：输入材料及其决定的内容智能。单源 = 一本书（翻译）；多源 = 多本书（深度整合）；代码库 = 源码路径（发现+分析）；session = 当前对话内容（→ take-note）。

**Product Shape（产品形态）**：与源类型**正交**的产出维度。`book` = 全书，走 builder 双格式（HTML+MD）+ 封面/目录 + 重型 gate；`doc` = 轻文档，就地便携 MD（如 `proj/book.md`），无 builder、轻量 gate。任一源类型可配任一形态。`note`（原子结论）由 take-note 产。_Avoid_：把"源类型"和"产品形态"焊死。

**Diagram（图表）**：agent 在 MD 中写 ` ```mermaid ` 文本，构建期 mermaid-cli 渲染为**仅 PNG**（ADR-0004）。MD 版与 HTML 版均嵌 PNG。证据（file:line）写在图注里。_Avoid_：drawio spec、`.drawio`（已废弃）。

**Gate（关卡）**：阶段锁——进入下一阶段前必须通过的自检，要么过要么失败。ADR-0005 后退化为正文自检清单（强模型能诚实自检），机械校验脚本仍兜底。_Avoid_：checkpoint。

**Verification Level（证据等级 V1–V4）**：论断背后的证据强度：V1 实机 / V2 源码 / V3 文档 / V4 推断。🔴🟠 问题须 ≥V2。定义见 [Writing Core](#writing-core写作内核)。

**Writing Core（写作内核）**：`shared/writing-core.md`——三个 skill 共用的**唯一**写作纪律源：铁律、写作原则、证据等级 V1-V4、来源可追溯、失败模式、剪枝。任一 skill 只引用、不重述。_Avoid_：在各 skill 里重复"铁律/失败模式"。

**AI 腔 / Slop**：AI 生成内容回归均值的通用腔——模板化措辞、空洞大词、无具体观点的"安全"句（delve / 值得注意的是 / 赋能 / 综上所述…）。本质是回归最可能的下一个 token、不敢给具体立场。第六类失败模式（见 Writing Core）。检测在 `shared/translationese-patterns.md` 的 AI 腔节（脚本 blunt 计数 + 模型自检）；治法是写人话——具体名词、确切动词、删套话、敢给观点。**词汇命中=警告（密度才判），结构命中=直接判**（三联排比 / 万能开头 / 复述式结尾 / 假平衡）。_Avoid_：把单次词汇命中当定罪；用 blunt 计数器做需语境判断的检测。

**Capability Axis（能力轴）**：系统级泛化的两个正交维度——**输入轴**（session / source / codebase）× **形态轴**（note / doc / book）。任一组合成立（session × note = take-note；codebase × doc = 项目学习文档）。三个 skill 合起来覆盖"任意技术 / 笔记文档"的生成。

**上下文工程（Context Engineering）**：这套 skill 的统领范式——策展长程生成时模型该看到什么，总律「最小高信号 token 集」。三战术映射既有机制：Compaction ↔ `context-summary.md`（从全文压缩）、Structured Notes ↔ `progress.md`（窗口外记忆）、Sub-agent Isolation ↔ ≤3 并行子 Agent。见 [ADR-0008](docs/adr/0008-context-engineering-spine-and-landmine-reframe.md)。_Avoid_：把长程生成当"一次性提示"而非分阶段策展上下文。

**Wiki（知识库）**：[KB_ROOT](#kb_root知识库根) 顶层的 `wiki/`——LLM 维护的可复利知识库：`raw/`（不可变源，人策展）→ 编译 concept/entity 页（LLM 写、人读）+ `index.md` + append-only `log.md`，与 `项目-{名}/` · `文档库/` 并行、交叉引用。五操作 INGEST/COMPILE/INDEX/QUERY/LINT，由 take-note 维护。见 [ADR-0009](docs/adr/0009-llm-wiki-paradigm-via-take-note.md)。_Avoid_：手写 wiki 页（那是 LLM 的活）；把 wiki 与项目笔记混为一谈。

**信息增量（AI irreducibility）**：反 slop 的密度框架——密度 = 抵抗被摘要压缩的信息量；治 slop = 写「摘要砍不掉」的内容。是 writing-core 第六类失败模式的治法判据。见 [ADR-0010](docs/adr/0010-anti-slop-precision-info-gain-and-structural-tells.md)。
