# 产品形态（Product Shape）：book 全书 vs doc 轻文档

> generate-book 的产出形态。与**源类型**（单源 / 多源 / 代码库）正交——任一源类型都可产出任一形态。
> 在 SKILL.md「模式选择」与源类型一起确定，启动前 CHECKPOINT 一并确认。
> **源类型决定"读什么、用什么内容智能"**（翻译规则 / 整合方法论 / 代码分析指南）；**产品形态决定"产什么、走多重的流水线"**。

## 为什么要区分

把源类型与产品形态焊死（如"代码库只能产 HTML 全书"）会让轻量需求（项目学习文档、单文件 MD）被迫跑重型流水线——builder、封面/目录 chrome、20KB 下限、Coverage Guardian，对一个就地 `book.md` 是纯开销。例：`pi3_trt/book.md`（给某个项目 subdir 生成一份学习文档）= **代码库 × doc**。

## book vs doc 对比

| 维度 | book 全书（默认） | doc 轻文档 |
|---|---|---|
| 适用 | 正式技术书、多章系统学习、要发布/分享 | 项目学习文档、快速上手指南、单文件或少量 MD |
| 典型用例 | 单源翻译书 / 多源整合书 / 代码库精通指南 | `proj/book.md`、模块走读、上手指南 |
| 输出路径 | `{RUN}/src/*.md` + `book.yml` → builder → `{RUN}/output/*.html` + `output-md/*.md` | **就地** MD（用户指定，如 `proj/book.md`）或少量 MD 文件夹 |
| builder | 运行 `build_html.py`（封面/目录/导航/CSS/JS/组件升级/mermaid→PNG） | **不运行**——纯 MD，无 HTML chrome |
| 封面/目录/翻页 chrome | builder 注入 | 无（用 MD 的 `#`/`##`，顶部可选手写目录） |
| 大小下限 | 核心章 >= 20KB、概览 >= 10KB（代码库）；多源 >= max(源章)×0.8 | **无硬性下限**——深度匹配内容需要即可 |
| Gate 强度 | 全套（预检 / 各 Phase Gate / Coverage Guardian / 输出验证） | 轻量（见下） |
| 双格式 | HTML + MD | 仅 MD |
| mermaid | builder 构建期 mmdc 渲染 PNG | 保留 ` ```mermaid `（GitHub / VS Code 原生渲染），不强制 mmdc |

## doc 形态的轻量 gate

保留不可妥协的核心（防偷工），去掉 book 特有的重量检查。

**保留（不可妥协）**：
- 新鲜阅读证据（不凭标题 / 记忆）——见 `shared/discipline-framework.md`「防懈怠机制」
- 代码库：每个论断 file:line 证据
- 单源：自然中文、无翻译腔（1:1 段落映射在 doc 形态可放宽为"语义对应"，但仍禁缩减）
- 多源：整合达 L3/L4（不可辨识来源）——见 `multi-synthesis.md`
- 无 `[待确认]` / TBD / 占位符；文件非空、UTF-8 无乱码

**去掉（book 专属，doc 不做）**：
- 20KB / 10KB 大小下限
- Coverage Guardian（多源底线规则、每源 >= 10% 标记）
- builder 产物验证（无 HTML 可验）
- 双格式一致性、封面/目录/翻页检查

**doc 形态简化流程**：复用各模式的"读 → 理解 → 写"，但合成与验证合并为单次自检——读完 →（多源：整合 / 代码库：分析核心模块 / 单源：翻译）→ 写就地 MD → 自检（上述保留项）→ 完成。不强制多 Phase、不写 progress.md（除非跨 session 大文档）。

## 如何选

- 用户说"一本书" / "正式" / "发布" / "多章" → **book**
- 用户说"学习文档" / "快速上手" / "单个 md" / "就地生成"，或给了单个输出路径（如 `proj/book.md`）→ **doc**
- 拿不准 → 启动前 CHECKPOINT 问用户

## doc 形态输出约定

- **默认就地**：输出到用户指定路径（如 `~/wd/projects/vlnmodelserver/.../pi3_trt/book.md`）。
- **单文件优先**：除非内容明显需要多章，否则一个 `book.md`（用 `#`/`##` 分节，顶部可选手写目录）。
- 多文件时：`NN_*.md` + 一个 `README.md` 目录（沿用 `md-authoring.md` 的 MD 约定，但**不走 builder**、不生成 `book.yml`）。
- 不生成 HTML；用户后续若要 book 形态，再按 book 流程把 MD 喂给 builder。
