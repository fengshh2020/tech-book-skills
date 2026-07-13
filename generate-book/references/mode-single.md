# 单源模式 (Single-Source Mode)

当恰好提供一个源书籍时使用。工作流：提取、翻译、组装、验证、报告。

**启动前**：运行预检（见 `shared-rules.md`「预检清单」），确认源文件可读取。初始化 progress.md（见「进度追踪鲁棒性」）。

## Phase 0：提取与阅读（3 个子阶段）

**⚠️ 启动前**：阅读 `references/agent-orchestration.md`，在 progress.md 中记录确认。

### 0.1 源文件清点
- 解析源文件（EPUB 或 HTML）
- EPUB：解压，解析 container.xml、content.opf、spine、toc.ncx
- HTML：解析结构、标题、导航
- 记录：书名、章节数、总页数、文件路径、源文件指纹
- **输出验证**：清点记录存在且包含所有元数据字段（书名、章节数、路径、指纹）

### 0.2 逐章阅读
- 按顺序阅读每个章节（不跳过，不只凭标题推断）
- 对每个章节记录阅读证据：段落数、代码块数、核心概念（>=3）、图片/图表数
- **输出验证**：每个章节都有证据记录，核心概念为具体术语（非泛化描述）

### 0.3 关卡（Gate 0）
- 每个章节都有阅读证据记录
- 源文件清点完成，包含所有元数据
- 没有章节被跳过或仅凭标题推断

## Phase 1：翻译（5 个子阶段）

**⚠️ 启动前**：阅读 `references/translation-rules.md` 和 `shared/translationese-patterns.md`，在 progress.md 中记录确认。

### 1.1 加载翻译规则
- 完整阅读 `references/translation-rules.md` 和 `shared/translationese-patterns.md`
- 阅读任何已有的 `.book-doc/spec.md` 以获取术语表

### 1.2 逐章翻译
- 逐段翻译，保持 1:1 映射（源段落数 = 目标段落数）
- 代码注释翻译为中文；代码逻辑保持不变
- 技术术语首次出现时加注中文注释
- 每翻译一章之前重新阅读规则文件

### 1.3 术语一致性检查
- 全书术语检索，验证每个术语在所有章节中翻译一致
- 标记并修复不一致之处

### 1.4 翻译腔扫描
- 对照 `shared/translationese-patterns.md` 扫描所有已翻译章节
- 目标：命中数为 0

### 1.5 关卡（Gate 1）
- 所有章节有 `<!-- translated: complete -->` 标记
- 段落数匹配（源 = 目标）
- 术语一致，翻译腔 0 次命中

## Phase 2：组装（MD 主源 + builder，ADR-0001）

> **doc 形态**（见 `references/product-shapes.md`）：不走 builder，翻译完直接写就地 MD（如 `proj/book.md`），用轻量 gate（无 builder 产物验证；1:1 段落映射放宽为"语义对应但仍禁缩减"）。book 形态才走下面的 2.1-2.3。

**⚠️ 启动前**：阅读 `references/md-authoring.md`（作者约定），在 progress.md 中记录确认。Gate 1 已通过。

### 2.1 写 MD 章节
- 在 `{RUN}/src/` 下按 `references/md-authoring.md` 写 `book.yml` + 编号章节 MD（`02_*.md` 起）
- 每章 `# 标题` + 正文；callout 用 `> **[标签]**`；图表用 ` ```mermaid `
- 翻译规则（术语、代码注释中文化）见 `references/translation-rules.md`，套用到 MD 围栏/强调

### 2.2 运行 builder
```bash
python scripts/build_html.py {RUN}/src {RUN}/output
```
- builder 自动：封面/目录/翻页导航、CSS/JS 复制、组件升级、mermaid → PNG

### 2.3 关卡（Gate 2）
- `{RUN}/output/*.html` 与 `{RUN}/output-md/*.md` 均已生成、非空
- 目录完整，内部链接有效

## Phase 3：验证（Gate 3）

```bash
scripts/validate_output.sh output/
python ../shared/validate_tech.py output/
python ../shared/validate_terms.py output/
```

额外检查：
1. 覆盖率验证：输出大小 >= 源文件的 80%
2. 术语一致性检查（全书检索）
3. 翻译腔二次扫描（0 次命中）
4. 段落数验证（源 = 目标）

**Gate 降级**（workflow.py 不可用时）：手动执行上述 6 项检查，结果写入 progress.md。

**Gate 3**：所有术语一致，所有代码可运行，所有交叉引用有效，翻译腔 0 次命中，输出大小 >= 源文件的 80%，段落数匹配。

## Phase 4：报告

**⚠️ 启动前**：阅读 `shared/report-templates.md`。Gate 3 已通过。

编写 `report.md`：
- 摘要（书籍概述、翻译质量总结）
- 每章评分（完整性、术语一致性、翻译质量）
- 问题列表（按严重程度排序）
- 术语表（全书统一的术语对照）
- 已知限制
