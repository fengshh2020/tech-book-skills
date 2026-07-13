# Tech Book Skills

三个 AI 技能把**任意技术栈**的源材料 / 代码库 / 当前 session 变成结构化文档（note / doc / book），并审阅它。为强模型设计——纪律收敛到一处，不堆防御性脚手架（见 [ADR-0005](docs/adr/0005-trim-scaffolding-for-capable-models.md)、[ADR-0006](docs/adr/0006-generalize-and-consolidate.md)）。

## 能力轴：输入 × 形态（系统级泛化）

三个 skill 合起来覆盖"任意技术 / 笔记文档"的生成——**输入轴**决定读什么（session / 源书 / 代码库），**形态轴**决定产什么（note 原子 / doc 就地 MD / book 全书+builder）。任一组合成立。

```
                 形态 →    note(原子)     doc(就地MD)      book(全书+builder)
输入 ↓
session 内容  ─────────  take-note       take-note        take-note(短篇)
源书(1/多)    ─────────      —          generate-book    generate-book
代码库        ─────────      —          generate-book    generate-book
```

- **take-note**：session → note/doc（Obsidian 库适配层）。
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
│   └── test-prompts.json
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

## 工作流

```
generate-book → review-tech-book → generate-book (按报告修复：改源 MD 重建)
```

1. **generate-book** 生成（单源/多源/代码库 × book/doc）
2. **review-tech-book** 审阅（默认仅报告）
3. 有问题 → 用户请求 review 修复模式（改 `{RUN}/src/*.md` → 重跑 builder），或把报告喂回 generate-book

## 设计原则

- **纪律收敛一处**：铁律、原则、证据等级、失败模式只在 `shared/writing-core.md` 定义一次，各 skill 引用不重述（ADR-0005）。
- **输入 × 形态正交 + 任意技术栈**：任一输入配任一形态；note/doc/book 覆盖从原子结论到全书的谱系；不假设特定语言（ADR-0006）。
- **MD 为源（ADR-0001）**：agent 写可移植 MD；`build_html.py` 渲染 HTML + MD；light-only、Mermaid→PNG。修复改源 MD 再重建，不手改 HTML（ADR-0006）。
- **保留客观校验**：`build_html.py` + `validate_*.{sh,py}` + `check_coverage.sh` 是真 builder / 真校验，提供机械兜底——与"是否信任模型自检"无关。
- **渐进披露 + 共享主干**：SKILL.md 是 hub（流程主干一次定义），细节按输入轴加载单个深度参考（ADR-0006）。

## 安装

作为 skill pack 放进 agent 的 skills 目录；agent 经 `SKILL.md` frontmatter `description` 发现 skill；每个 skill 渐进披露：SKILL.md（hub）→ reference（按输入/阶段）→ `shared/writing-core.md`（共用纪律）。

## License

MIT
