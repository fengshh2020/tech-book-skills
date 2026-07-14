# Tech Book Skills

三个 AI 技能把**任意技术栈**的源材料 / 代码库 / 当前 session 变成结构化文档（note / doc / book），并审阅它。为强模型设计——纪律收敛到一处，不堆防御性脚手架（见 [ADR-0005](docs/adr/0005-trim-scaffolding-for-capable-models.md)、[ADR-0006](docs/adr/0006-generalize-and-consolidate.md)、[ADR-0007](docs/adr/0007-2026-research-driven-description-routing-and-anti-slop.md)）。2026-07 进一步以**上下文工程**为脊柱、演进 take-note 维护可复利 **wiki/**、反 slop 精确化（[ADR-0008](docs/adr/0008-context-engineering-spine-and-landmine-reframe.md) / [0009](docs/adr/0009-llm-wiki-paradigm-via-take-note.md) / [0010](docs/adr/0010-anti-slop-precision-info-gain-and-structural-tells.md)）。

**三工具通用**——Claude Code / OpenCode / Codex 均遵循开放 [Agent Skills](https://agentskills.io) 标准（`<name>/SKILL.md` + frontmatter `name`/`description`）；`./install.sh` 一键符号链接安装（见下「安装」）。

## 能力轴：输入 × 形态（系统级泛化）

三个 skill 合起来覆盖"任意技术 / 笔记文档"的生成——**输入轴**决定读什么（session / 源书 / 代码库），**形态轴**决定产什么（note 原子 / doc 就地 MD / book 全书+builder）。任一组合成立。

```
                 形态 →    note(原子)     doc(就地MD)      book(全书+builder)
输入 ↓
session 内容  ─────────  take-note       take-note     take-note(短篇)/generate-book(长程)
源书(1/多)    ─────────      —          generate-book    generate-book
代码库        ─────────      —          generate-book    generate-book
```

**路由判据 = 长程流水线要不要**（非页数）：session 短篇书（无流水线）→ take-note；session 长程独立交付物（要分阶段流水线）→ generate-book。目的地正交——产物要进库再经 take-note book-ingest（[ADR-0012](docs/adr/0012-book-to-vault-handoff-via-take-note.md)）。

- **take-note**：session → note/doc/短篇书（Obsidian 库适配层）+ 维护顶层 `wiki/` 可复利知识库（ingest/query/lint，[ADR-0009](docs/adr/0009-llm-wiki-paradigm-via-take-note.md)）+ 把 generate-book 产物 book-ingest 进 `文档库/`（[ADR-0012](docs/adr/0012-book-to-vault-handoff-via-take-note.md)）。
- **generate-book**：源书 / 代码库 → doc/book。任意技术栈（Python / Rust / Go / 嵌入式 C/C++ / shell …）。
- 三个 skill 共用 [`shared/writing-core.md`](shared/writing-core.md)（铁律、写作原则、证据 V1-V4、失败模式），各保留自己的目标约定（take-note = Obsidian 库；generate-book = 工作区）。

## Skills

| Skill | 职责 | 触发场景 |
|-------|------|----------|
| **generate-book** | 从源书 / 代码库生成技术书或学习文档 | 翻译书、整合多书、代码库走读、项目学习文档 |
| **review-tech-book** | 结构化质量审阅（默认仅报告） | 审阅已生成的书/文档、质量评估、按报告修复 |
| **take-note** | 把当前 session 写成 Obsidian 笔记/短文档 | 记笔记、存知识库、记录踩坑/配置/决策 |

## 结构

```
tech_book_skills/
├── generate-book/                    # 生成（单源/多源/代码库 × book/doc）
│   ├── SKILL.md                      # Hub：能力轴 + 共享流程主干 + 参考索引
│   ├── references/
│   │   ├── translation.md            # 单源：翻译规则 + 术语表（任意语言，Python 示例）
│   │   ├── multi-source.md           # 多源：知识索引 + 架构 + 整合 L1-L4 + Coverage Guardian
│   │   ├── writing-and-content.md    # 代码库：叙事驱动 / 先图后文 / sidebar 纪律
│   │   └── md-authoring.md           # MD 作者约定 + 组件映射（builder 契约，ADR-0002）
│   ├── scripts/  build_html.py · check_coverage.sh · validate_output.sh
│   └── assets/   style.css · script.js
├── review-tech-book/                 # 审阅（任意技术栈）
│   ├── SKILL.md                      # Hub：4 阶段 + 修复模式
│   ├── references/
│   │   ├── spec.md                   # 十六维度 + 五转化整合 + 报告模板 + 校验清单
│   │   ├── review-criteria.md        # 反模式 + 五转化维度 + 教学理论 + 工程实践标杆
│   │   └── apply-fixes.md            # 修复模式：P0-P3（改源 MD 重建，非手改 HTML）
│   └── scripts/  validate_code.sh
├── take-note/                        # Obsidian 笔记/短文档适配层
│   ├── SKILL.md                      # 归位/frontmatter/callout/双链（引用 writing-core）
│   ├── references/
│   │   └── llm-wiki.md               # 可复利 wiki/ 范式：结构 + 五操作 + 交叉引用（按需读）
│   └── test-prompts.json
├── install.sh                    # 三工具（Claude/OpenCode/Codex）用户级符号链接安装
└── shared/                           # 跨 skill 复用
    ├── writing-core.md               # ★ 唯一纪律源：铁律/原则/V1-V4/失败模式/剪枝/校验工具
    ├── translationese-patterns.md    # 翻译腔模式（validate_code.sh 动态读取）
    ├── validate_tech.py              # 技术准确性校验
    └── validate_terms.py             # 术语一致性校验
```

## 双格式输出（ADR-0001）

**MD 是信息主源**：agent 在 `{RUN}/src/` 写 MD 章节 + `book.yml`，运行 `scripts/build_html.py {RUN}/src {RUN}/output` 渲染：
- `output/` —— HTML 版（"静奢"设计系统，light-only，封面/目录/翻页/mermaid→PNG）
- `output-md/` —— 可移植 MD 版（mermaid→PNG 嵌入，GitHub/VS Code 直读）

作者约定见 `generate-book/references/md-authoring.md`；架构决策见 `docs/adr/`：
- **ADR-0001** MD 为源·builder 渲染 ｜ **ADR-0002** 富组件务实子集映射
- **ADR-0003** light-only ｜ **ADR-0004** Mermaid→PNG
- **ADR-0005** 为强模型裁剪脚手架 ｜ **ADR-0006** 泛化任意技术栈 + 合并 reference + 修正 MD 源修复
- **ADR-0007** 2026 研究驱动重构：description 路由化 + 反 AI 腔（slop）
- **ADR-0008** 上下文工程脊柱 + ETH「地雷」重定位（writing-core 收成地雷文件）
- **ADR-0009** LLM-wiki 范式：演进 take-note 维护顶层 `wiki/` 可复利知识库
- **ADR-0010** 反 slop 精确化：信息增量框架 + 结构 tell 细化
- **ADR-0011** KB 根解析与 portable：`$KB_ROOT` 动态发现（标记/问/init）+ 实例数据运行时发现，去硬编码
- **ADR-0012** 生产者/适配者切分：Book Artifact 经 take-note book-ingest 进库（目的地正交；review flag wiki 候选、generate-book flag 沉淀副产物，都不自动写库）

## 工作流

```
generate-book → review-tech-book → generate-book (按报告修复：改源 MD 重建)
   │                │
   │                └─ 系统性发现 → flag wiki 候选 → take-note INGEST
   └─ 书 → take-note book-ingest → 文档库/  ；副产物(配置/洞察) → flag → take-note
```

1. **generate-book** 生成（单源/多源/代码库/session × book/doc）
2. **review-tech-book** 审阅（默认仅报告）
3. 有问题 → 用户请求 review 修复模式（改 `{RUN}/src/*.md` → 重跑 builder），或把报告喂回 generate-book
4. **沉淀出口**（端到端）：书进库 → take-note book-ingest（`文档库/`）；review 系统性发现 → take-note INGEST wiki；generate-book 副产物（配置/环境技巧、可迁移洞察）→ take-note。三处都 flag、都由 take-note 写、都不自动写库（生产者/审阅者 portable，库+wiki 唯一主人=take-note）。

## 设计原则

- **纪律收敛一处**：铁律、原则、证据等级、失败模式只在 `shared/writing-core.md` 定义一次，各 skill 引用不重述（ADR-0005）。
- **正文纯粹、出处归档**：skill 正文只留规则、不夹出处（论文 / 人名 / arXiv / 书名标杆）——借来的方法直接用；同一概念（slop 清单、密度公式）只在 writing-core 定义一次、他处指回；决策出处归 `docs/adr/`，不进 skill 正文做徽章。
- **输入 × 形态正交 + 任意技术栈**：任一输入配任一形态；note/doc/book 覆盖从原子结论到全书的谱系；不假设特定语言（ADR-0006）。
- **MD 为源（ADR-0001）**：agent 写可移植 MD；`build_html.py` 渲染 HTML + MD；light-only、Mermaid→PNG。修复改源 MD 再重建，不手改 HTML（ADR-0006）。
- **保留客观校验**：`build_html.py` + `validate_*.{sh,py}` + `check_coverage.sh` 是真 builder / 真校验，提供机械兜底——与"是否信任模型自检"无关。
- **渐进披露 + 共享主干**：SKILL.md 是 hub（流程主干一次定义），细节按输入轴加载单个深度参考（ADR-0006）。
- **上下文工程脊柱（ADR-0008）**：长程生成 = 分阶段策展上下文，总律「最小高信号 token 集」；既有 `progress.md` / `context-summary.md` / 并行子 Agent 即 Compaction / Structured Notes / Sub-agent Isolation。writing-core 收成「地雷文件」（只放 agent 自发现不了的）。
- **可复利 wiki（ADR-0009）**：take-note 维护顶层 `wiki/`（raw/ 不可变源 → 编译 concept/entity 页 + index + log + lint），与项目结构并行、交叉引用。
- **portable（ADR-0011）**：take-note 不焊死库路径——`$KB_ROOT` 从 cwd 向上发现（`.kb-root` / `00_首页.md`），找不到问 / init；项目名运行时扫 `项目-*`、不硬编码。结构逻辑 portable、实例数据 discover。
- **description 即路由规则**：每个 SKILL.md 的 description 是"何时触发"的路由（`Use when…` + 触发短语 + 负路由），不述"做什么"（那是正文）——对齐 2026 Anthropic Agent Skills 规范（ADR-0007）。
- **反 AI 腔（slop）**：生成内容不得回归通用腔——第六类失败模式 + `translationese-patterns` 的 AI 腔节 + review 反模式三处守住；**密度 = 抵抗被摘要的信息增量**，词汇警告 + 结构 tell 直接判，模型自检为主、脚本计数为辅（ADR-0007）。

## 安装（Claude Code / OpenCode / Codex）

三工具都采用开放 [Agent Skills](https://agentskills.io) 标准（`<name>/SKILL.md` + frontmatter `name`/`description`），本套已合规（目录名 == frontmatter `name`）。差别在扫描路径——**没有单目录被三者全扫**：

- **Codex CLI**：`~/.agents/skills/`（不扫 `.claude/`）
- **OpenCode**：`~/.agents/skills/`、`~/.opencode/skills/`、`~/.claude/skills/`（全扫）
- **Claude Code**：`~/.claude/skills/`（不扫 `.agents/`）

故用户级安装需同时链接进 `~/.agents/skills/`（Codex+OpenCode）和 `~/.claude/skills/`（Claude+OpenCode）。仓库根的 `install.sh` 一键做（符号链接，仓库为单一源、可逆）：

```bash
./install.sh                # 默认：链接进 ~/.agents/skills/ + ~/.claude/skills/
./install.sh --agents       # 只装 Codex+OpenCode
./install.sh --claude       # 只装 Claude
./install.sh --uninstall    # 移除链接
```

链接 `take-note` / `generate-book` / `review-tech-book` / `shared/` 四项。`shared/` 是三 skill 的兄弟资源（供 `../shared/writing-core.md` 解析；无 `SKILL.md`、不会被当 skill 加载）。

> Windows 原生（非 WSL）运行某工具时，路径改 `%USERPROFILE%\.agents\skills` / `%USERPROFILE%\.claude\skills`，符号链接需开发者模式或 `mklink /D`。

每个 skill 渐进披露：`SKILL.md`（hub）→ reference（按输入/阶段）→ `../shared/writing-core.md`（共用纪律）。

## License

MIT
