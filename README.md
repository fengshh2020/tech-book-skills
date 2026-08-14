# Tech Book Skills

六个 skill 把**任意技术栈**的源材料 / 代码库 / 当前 session 变成结构化文档（note / doc / book / 译文），审阅它，并推演技术方案；**research** 为其他 skill 提供带引用的调研能力。为强模型设计——每个 skill 只承载核心回路与路由，纪律与协议收敛到少数共享原语，引用不重述。

**三工具通用**——Claude Code / OpenCode / Codex 均遵循开放 [Agent Skills](https://agentskills.io) 标准（`<name>/SKILL.md` + frontmatter `name`/`description`）；`./install.sh` 一键符号链接安装（见下「安装」）。

## Skills

| Skill | 职责 | 触发场景 |
|-------|------|----------|
| **translate-book** | 翻译一本书：结构 1:1、信达、术语统一 | 翻译英文书、中文化、汉化 |
| **generate-book** | 写原创书/学习文档：多源整合或代码库走读，**讲得透** | 整合多书、代码库走读、项目学习文档 |
| **review-tech-book** | 结构化质量审阅（默认仅报告）：六类问题 + 证据 | 审阅已生成的书/文档、按报告修复 |
| **take-note** | 把当前 session 写成 Obsidian 笔记/短文档 | 记笔记、存知识库、书进库（book-ingest） |
| **research** | 调研问题 → 带引用的 Finding Block | 查文档、验证论断、对比选型 |
| **tech-proposal** | 从技术目标推演到方案文档 + 内嵌代码骨架 | 新系统设计、增量需求、选型架构 |

**路由判据 = 长程流水线要不要**：session 短篇沉淀 → take-note；要分阶段流水线的独立交付物 → translate-book（单源翻译）/ generate-book（多源、代码库）。翻译与写作是两种任务、两套纪律，各是一个 skill。

## 共享原语（shared/，各 skill 引用不重述）

| 文件 | 内容 |
|------|------|
| `shared/writing-core.md` | ★ 唯一纪律源：讲解质量三标准 / 反冗余红线 / 铁律 / 反 AI 腔 / 校验套件表（唯一命令源） |
| `shared/book-project.md` | ★ 书籍项目契约：工作区 / 生命周期 / progress.md 状态 / 曳光弹首章 / 滚动构建 / 修复操作 |
| `shared/kickoff.md` | ★ 开跑对齐原语：事实自查 / 决策带推荐 / 一轮问完 |
| `shared/md-authoring.md` | book 形态 MD 作者约定（builder 契约） |
| `shared/translationese-patterns.md` | 翻译腔 + AI 腔词表（validate_code.sh 动态读取） |
| `shared/scripts/` + `shared/assets/` | `build_html.py` · `validate_output.sh` · `validate_code.sh` · style.css · script.js |

每个 skill 渐进披露：`SKILL.md`（核心回路 + 路由）→ `references/`（按输入/阶段）→ `../shared/`（共用纪律与协议）。

## 一本书的生命周期

```
对齐（kickoff）→ 读透 → 首章曳光弹（构建+校验+用户过目）→ 逐章量产 · 滚动构建
  → review-tech-book 审阅（起步读 progress.md；默认仅报告）
  → 修复 = 工作区操作（改源 MD → 重建 → 重校验）
  → 沉淀：书进库 take-note book-ingest；系统性发现 flag → take-note 进 wiki
research ←── 各 skill 内联调用（可后台并行）
```

## 设计原则

- **一 skill 一职责**：翻译 ≠ 写书 ≠ 审阅 ≠ 记笔记 ≠ 调研 ≠ 方案；description 即路由规则（`Use when…` + 触发短语 + 负路由）。
- **纪律收敛一处**：写作纪律只在 writing-core（含校验命令表）；开跑对齐只在 kickoff；书籍管线只在 book-project——各 skill 引用不重述。
- **流程适配注意力**：每个 skill 一条 3-4 步核心回路；流程仪式（阶段编号、评分矩阵、多级 guardian）会切碎注意力、诱导平庸——砍。
- **保留真实客观校验**：四个脚本每个都被文档正确引用、实跑有效；跑不通的兜底宁可删。
- **portable**：take-note 的 `$KB_ROOT` 动态发现；结构逻辑 portable、实例数据 discover。
- **可视化优先（原创内容）**：结构/流程/状态/架构/数据流能画就画，图表格式标准 SVG。

> **`allowed-tools` 约定（刻意区分，非遗漏）**：read-only / 库写类 skill 声明紧 `allowed-tools`（research=`Read Glob Grep`、take-note=`Read Write Glob`、tech-proposal=`Read Write Edit Glob Grep`）；全流水线 skill（translate-book、generate-book、review-tech-book）不声明 = 不受限。

## 双格式输出

**MD 是信息主源**：agent 在 `{RUN}/src/` 写 MD 章节 + `book.yml`，`python shared/scripts/build_html.py {RUN}/src {RUN}/output` 渲染出 `output/`（HTML 版，"静奢"设计系统）+ `output-md/`（可移植 MD 版）。作者约定见 `shared/md-authoring.md`。

## 安装（Claude Code / OpenCode / Codex）

三工具扫描路径不同——**没有单目录被三者全扫**（Codex 只扫 `~/.agents/skills/`；OpenCode 三处全扫；Claude Code 只扫 `~/.claude/skills/`）。仓库根 `install.sh` 一键符号链接（仓库为单一源、可逆）：

```bash
./install.sh                # 默认：链接进 ~/.agents/skills/ + ~/.claude/skills/
./install.sh --agents       # 只装 Codex+OpenCode
./install.sh --claude       # 只装 Claude
./install.sh --uninstall    # 移除链接
```

链接 `take-note` / `generate-book` / `translate-book` / `review-tech-book` / `research` / `tech-proposal` / `shared` 七项（`shared/` 是兄弟资源，无 SKILL.md、不会被当 skill 加载）。Windows 原生（非 WSL）时路径改 `%USERPROFILE%\.agents\skills` 等，符号链接需开发者模式或 `mklink /D`。

## License

MIT
