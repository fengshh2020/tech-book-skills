---
name: generate-book
description: "Use when generating a technical book or project learning doc from source books or a codebase — any tech stack (Python / Rust / Go / 嵌入式 C/C++ / shell …). Triggers: generate book, 整合书籍, 生成书籍, 生成项目书籍, merge books, combine sources, translate book, 翻译书籍, codebase walkthrough, codebase book, 代码库书籍, 掌握项目, 架构学习指南, 项目学习文档, 学习指南, 生成 book.md, 项目文档, project guide, learning doc, walkthrough this project, 给这个项目生成文档. Use take-note instead to capture the current session into the Obsidian vault. Do NOT trigger for: quality review only (use review-tech-book), code review, README, or API reference."
---

# 生成技术书 / 学习文档

从源书或代码库生成一本技术书或一份项目学习文档——读起来像一本书，不是拼贴画。任意技术栈通用。

**先读 `shared/writing-core.md`**——铁律、写作原则、证据等级 V1-V4、失败模式、剪枝、校验工具都在那，本文件与各 reference 不再重述。任一阶段开始前按需读对应 reference，不顺手全读。

## 能力轴：输入 × 形态

两个正交维度，启动时一起定。

**输入轴**（读什么）——自动检测：1 个源书 → **单源**（翻译）；2+ 个源书 → **多源**（深度整合）；代码库路径 → **代码库**（发现+分析）。

**形态轴**（产什么、走多重的流水线）：

| 形态 | 适用 | 输出 |
|---|---|---|
| **book**（默认） | 正式书 / 多章系统学习 / 要发布 | `{RUN}/src/*.md` + `book.yml` → builder → `output/` HTML + `output-md/` MD |
| **doc** | 项目学习文档 / 快速上手 / 就地单文件（如 `proj/book.md`） | 就地 MD，**无 builder**，轻量 gate |

任一输入可配任一形态（代码库 × doc = 项目学习文档）。

## 启动前（生成耗时长，判错 = 整轮返工）

1. **检测输入 + 选形态**：用户说"一本书/正式/发布/多章"→ book；说"学习文档/快速上手/单个 md/就地生成"或给了单个输出路径 → doc。
2. **🛑 向用户确认再开跑**：输入类型与意图一致 ｜ 形态（book/doc）与意图一致（doc 尤其确认输出路径：就地 `book.md` 还是 `{RUN}/`）｜ 源/代码库路径、输出位置、目标语言无误。拿不准让用户显式指定，别替它猜。
3. **预检**：`{RUN}` 可写、源文件/代码库可读、book 形态下 `build_html.py` 存在。失败 = 停下告知用户，不凑合。

## 流程（共享主干，3 模式只在中段不同）

**读 → 理解 → 写 → 验证 → 报告**。每段结束按 writing-core 失败模式自检（假读 / 缩水 / 伪造校验 / 缝补整合 / 推断当结论）。**长程即上下文工程**（writing-core 总律）：`progress.md` = 窗口外结构化记忆、multi-source `context-summary.md` = 压缩（从全文、先 recall 后 precision）、≤3 并行子 Agent = 隔离——任一阶段只加载该阶段高信号 token，不为"全面"预加载。

**① 读**（所有模式）：逐章/逐文件**实读**，记证据（精确段落数、代码块首行、≥3 具体术语、file:line）。不凭标题猜——这是铁律。

**② 理解**（按输入走对应深度参考）：

| 输入 | 中段做什么 | 深度参考 |
|---|---|---|
| 单源 | 逐段翻译，1:1 段落映射；代码注释中文化、逻辑不变；术语全书一致、无翻译腔 | `references/translation.md` |
| 多源 | 每源建深度知识索引 → 设计整合架构 → 章节整合达 **L3/L4**（读者无法辨识来源）、反向覆盖 100% | `references/multi-source.md` |
| 代码库 | 发现执行路径 → 按优先级分析核心模块（每论断 file:line）→ 沿执行路径**叙事**讲解，不罗列函数 | `references/writing-and-content.md` |

**③ 写**：
- **book 形态**（MD 是信息主源）：在 `{RUN}/src/` 写 `book.yml`（`title/subtitle/subtitle_cn/author/edition/lang`）+ 编号章节 `NN_*.md`（NN ≥ 02，首行 `# 标题`）。作者约定（callout `> **[标签]**`、` ```mermaid `、代码 `caption=`、图片图注）见 `references/md-authoring.md`。然后：
  ```bash
  python scripts/build_html.py {RUN}/src {RUN}/output
  ```
  builder 注入封面/目录/翻页/CSS/JS/mermaid→PNG。自检：`output/*.html` 与 `output-md/*.md` 均生成、非空、目录完整、内链有效。
- **doc 形态**：就地写 MD（单文件优先：顶部一句话用途 + 可选目录，`#`/`##` 分节）。mermaid 保留 ` ```mermaid ` 文本（GitHub/VS Code 原生渲染）。多文件时 `NN_*.md` + `README.md` 目录，沿用 md-authoring 约定但**不走 builder**、不写 `book.yml`。

**④ 验证**：
```bash
scripts/validate_output.sh output/                       # book 形态
python ../shared/validate_tech.py output/                 # 技术准确性
python ../shared/validate_terms.py output/                # 术语一致
scripts/check_coverage.sh {RUN}/knowledge_base/ output/ summary   # 仅多源
```
任一失败先修后进。模式专属自检：单源 = 段落数 源=目标、翻译腔 0、输出 ≥ 源 80%；多源 = 覆盖率 ≥95%、来源不可辨识；代码库 = 每论断 file:line、核心章 ≥20KB / 概览 ≥10KB / 代码:解释 ≥1:1。

**⑤ 报告**：写 `{RUN}/report.md`（摘要 + 每章评分 + 问题列表 + 覆盖矩阵/设计决策表[代码库] + 校验结果 + 已知限制）。

### doc 形态的轻量 gate

保留不可妥协的核心（真读证据、file:line[代码库]、1:1 不缩减[单源]、L3/L4[多源]、无占位符、文件非空无乱码），去掉 book 专属重量：20KB/10KB 下限、Coverage Guardian、builder 产物验证、双格式一致性。流程压成"读 → 理解 → 写就地 MD → 单次自检"，不写 `progress.md`（除非跨 session 大文档）。

### 并行（可选优化）

认知递进 + 风格需端到端一致 → **章节串行**（单 Agent 逐章）。任务独立的阶段（多源 Phase 0 每书一 Agent、代码库 Phase 1 每核心模块一 Agent、验证）可 ≤3 并行。全局上限 5 Agent；单 Agent 失败重试 1 次。

## 输出结构

**book 形态**：
```
{RUN}/
├── src/                    ← agent 写这里（MD 主源）：book.yml + NN_*.md + (可选)README.md
├── output/                 ← builder 产出（HTML 版）
└── output-md/              ← builder 产出（可移植 MD 版）
```
**doc 形态**：就地 MD（用户指定路径，如 `proj/book.md`），无 `src/`、无 builder 产物。

**长流程恢复**（跨 session）：读 `{RUN}/progress.md` 定位最后完成阶段 → 验证其输出（存在/非空/无占位符）→ 从下一阶段继续，不从头开始。

## 参考文件（按需读，不全读）

| 文件 | 内容 | 适用 |
|---|---|---|
| `shared/writing-core.md` | 铁律 / 原则 / V1-V4 / 失败模式 / 剪枝 / 校验工具 | 全部 |
| `references/translation.md` | 翻译规则：术语 / 代码块 / 标点 / 红线 + 术语表 | 单源 |
| `references/multi-source.md` | 多源：知识索引 + 架构设计 + 整合 L1-L4 + Coverage Guardian + 自检 | 多源 |
| `references/writing-and-content.md` | 代码库写作：叙事驱动 / 认知负荷 / 代码展示 / sidebar | 代码库 |
| `references/md-authoring.md` | MD 作者约定 + 组件映射（务实子集） | book 形态 |
