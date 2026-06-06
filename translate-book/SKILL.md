---
name: translate-book
description: "Use when translating an entire technical book (EPUB) into a Chinese HTML site, resuming an interrupted run, or filling missing chapters. Trigger on: EPUB with Chinese output, 翻译这本书, translate this EPUB, 续译, 补齐缺章. Do NOT trigger for: single-term/typo fixes, quality review (use review-tech-book), merging books (use integrate-books)."
---

# Translate Book

将 EPUB 技术书或长篇技术文档翻译为中文 HTML 站点。目标是一次生成可阅读、可导航、术语一致、可恢复、可校验的书籍产物。

## 核心约束

以下规则从实际翻译错误中反复提炼。违反任意一条即视为本章翻译失败，不需要等审阅阶段发现：

**段落一一对应**：原文 3 段译文就是 3 段，不合并不跳过。段落合并是最常见且最难被自动化检测到的错误——审阅者发现时往往已经合并了大量段落，修复成本极高。

**代码注释译中文**：`# This is a comment` → `# 这是注释`。但变量名、函数名、输出字符串、异常文本保留英文。区分"面向读者的注释"和"程序标识符"是关键——如果删掉这行注释读者会困惑，就翻译它。

**术语首现括注英文**：首次出现"装饰器"时写"装饰器（decorator）"，后续统一用中文。全书同一术语只能有一个中文译法。

**HTML 结构保留**：锚点 `id="item-42"` 不能改，链接 `href="ch03.html"` 不能改，`<strong>/<em>` 标记不能丢。只翻译标签之间的文字内容。

**不写翻译腔**：禁止"这就是为什么""你会发现""正如你""让我们""接下来我们将""值得注意的是"等直译句式。完整禁止列表见 `../shared/translationese-patterns.md`——翻译每章前至少重新扫一遍这个列表。

## 引用文件

每个阶段开始前执行该阶段的读取指令。不要提前加载全部文件，也不要跳过当前阶段的读取——"我记得上次读过"不是跳过理由，规则的具体措辞会影响翻译质量。

| 阶段 | 必读文件 | 读取目标 |
|------|----------|----------|
| 启动 | `../shared/progress-protocol.md` | 运行发现和恢复协议 |
| 启动 | `../shared/runtime-pruning.md` | 运行时剪枝和停止条件 |
| 启动 | `../shared/agent-compatibility.md` | `SKILL_DIR`/`SKILL_PACK_DIR`/`PROJECT_ROOT` 路径 |
| 阶段 2 | `references/spec.md` | 通用翻译规范、术语表、排版规则 |
| 阶段 3 | `references/html-templates.md` | HTML 页面结构模板 |
| 阶段 4（每章） | `references/red-lines.md` | 翻译硬规则（每章前重新读取） |
| 阶段 4（每章） | `references/common-pitfalls.md` | 常见陷阱正反例 |
| 阶段 4（每章） | `../shared/translationese-patterns.md` | 翻译腔模式列表 |
| 阶段 4（每章） | `../shared/quality-ownership.md` | 翻译阶段的质量责任边界 |
| 阶段 5 | `scripts/validate_format.sh` | 格式验证脚本 |
| 阶段 6 | `../shared/report-templates.md` | 报告模板 |

## 运行状态

先执行共享进度协议，使用 run slug `translate`。运行目录形如：

```text
.book-doc/runs/{YYYYMMDD}-translate-{label}/
```

本 skill 的关键状态：

- run 目录内：`progress.md`、`epub_extract/`、`epub-metadata.json`、`report.md`
- 跨轮次项目状态：`.book-doc/spec.md`
- 输出目录：默认 `output/`，除非用户指定

幂等性检查：

- `epub_extract/` 和 `epub-metadata.json` 存在，且源 EPUB 路径、大小或时间戳未变化，可跳过提取。
- `.book-doc/spec.md` 存在且包含本书特有规则，可更新而不是重建。
- `output/style.css`、`output/script.js` 存在且通过基础校验，可保留。
- 每个 HTML 文件首行 `<!-- translated: complete -->` 表示可信完成；`<!-- translated: partial -->` 必须重做；缺少标记是 `unknown`，必须结合 `progress.md`、源 spine 清单和验证结果判断，不能自动跳过。

## 模式

### 全量翻译

用于新书或源文件已变化的全量翻译。执行完整六阶段流程。

### 恢复

用于 active/interrupted 运行。恢复时读取 `progress.md` 和 HTML 首行标记，从第一个未可信完成的章节继续。

### 补缺模式

用户要求"补齐缺章""只翻译缺失章节"，或恢复时只剩少量章节未完成时启用补缺模式：

- 源 EPUB 未变化且已有 `epub-metadata.json` 时，跳过 EPUB 重新提取和 spine 全量分析。
- `.book-doc/spec.md`、`output/style.css`、`output/script.js` 已存在且校验通过时，跳过项目 SPEC 和输出初始化。
- 只读取目标章节源 XHTML、相邻章节标题、必要术语规则和红线规则。
- 只对目标章节运行逐章自检；最终校验可先限定目标文件，完整校验留到全书完成时。
- 在 `progress.md` 记录目标章节、跳过依据和残余风险。

## 流程

```text
Extract → Project Spec → Output Scaffold → Translate Chapters → Validate → Report
```

每个可恢复单元完成后更新 `progress.md`。

## 阶段 1：提取 EPUB

目标：建立稳定的源文件清单和阅读顺序。

1. 在当前 run 目录创建 `epub_extract/`。
2. 解压 EPUB；失败则记录 `interrupted` 并停止。
3. 通过 `container.xml`、`content.opf`、manifest、spine、toc.ncx 或 nav 文档确定阅读顺序。
4. 扫描章节 XHTML、图片资源、代码块、旁注、脚注和封面信息。
5. 写入 `{RUN}/epub-metadata.json`，包含源文件指纹、spine、标题层级、图片清单和特殊结构。

关卡：spine 中每个可翻译文档都有源路径、目标编号和标题。

## 阶段 2：项目规范

**读取 `references/spec.md`**——包含术语表、排版规则和代码块处理规范。

目标：记录本书特有规则。

1. 完整读取 `references/spec.md`。
2. 新建或更新 `.book-doc/spec.md`，包含固定标题译法、术语表、文件编号、特殊组件、已知问题。
3. 若已有 SPEC，保留用户或前序运行的明确规则，只更新与当前源文件变化相关的部分。

关卡：`.book-doc/spec.md` 足以让后续章节不重新推断术语和结构。

## 阶段 3：输出脚手架

**读取 `references/html-templates.md`**——包含 HTML 页面结构。

目标：建立可导航 HTML 站点基础。

1. 创建 `output/images/`。
2. 从 `assets/` 复制 `style.css` 和 `script.js` 到输出目录。已有文件更完整且关键类名可用时不覆盖。
3. 收集图片到 `output/images/`，保持相对路径可解析。
4. 建立文件编号映射：

| 编号 | 文件 |
|------|------|
| 00 | `00_cover.html` |
| 01 | `01_toc.html` |
| 02 | `02_front.html` |
| 03 | `03_intro.html` |
| 04+ | `{NN}_chapter{M}.html` |
| N+ | `{NN}_appendix_{x}.html` |
| N+ | `{NN}_glossary.html` |

关卡：CSS/JS 存在，章节编号与 spine 一一对应，图片目标目录存在。

## 阶段 4：翻译章节

每批最多 2 章并行处理；若上下文、术语或跨章引用高度耦合，则串行处理。

**每章翻译前必须重新读取**（不能"记住上次读的"）：
1. `references/red-lines.md` —— 翻译硬规则
2. `references/common-pitfalls.md` —— 高频错误正反例
3. `../shared/translationese-patterns.md` —— 翻译腔禁止列表
4. `.book-doc/spec.md` 中本章相关的术语约定
5. 相邻 2 章的已完成标题和风格基线

为什么每章都要重新读取？因为这些文件中的具体措辞和正反例会直接影响翻译质量。凭记忆翻译会丢失细节约束——实际翻译中出现的大量段落合并和翻译腔问题，都发生在"我以为我记住了规则"的时候。

### 4a. 逐段翻译

对源 XHTML 的每个可翻译内容块（段落、标题、列表项、表格单元格、alt 属性）：

- 翻译正文为自然中文，保留所有 HTML 标签和属性不变
- 代码块逐字复制源文件，只翻译面向读者的代码注释（`# 注释`）
- 链接地址不翻译，链接文字翻译
- 图片路径保持原样，alt 属性翻译为中文

### 4b. 章节自检

翻译完成后，对本章执行以下检查。每项检查必须**在 progress.md 中留下具体证据**，不能只写"通过"。遵循 `../shared/progress-protocol.md` 阅读证据协议：

- **段落计数**：读取源文件统计段落数，读取译文统计段落数，对比。记录格式：`ChN 段落: 源 M = 译 M`。不一致时必须找出合并/遗漏的段落并修复。
- **术语全量检查**：遍历 `.book-doc/spec.md` 术语表中**所有**本章出现的术语，验证首次出现有括注且后续一致。记录：`术语: decorator✓ 首现ChN行NN, generator✓ 首现ChN行NN, closure✓ 首现ChN行NN`，列出全部已检查术语，不允许用"等"省略。
- **翻译腔扫描**：用 `../shared/translationese-patterns.md` 的正则逐个搜索本章 HTML。记录：`翻译腔: 0命中` 或 `翻译腔: "正如你" 行234 已修复`。
- **代码完整性**：代码注释已翻译、代码清单编号连续、图片路径存在。记录具体验证的代码清单编号范围。
- **内容校验**：从译文中抽取一段核心段落的首行和末行，记录原文和译文对照。这证明你实际打开并对比了源文件和译文，不是凭记忆填写。

### 4c. 修复与写入

自检发现的问题必须在写入前修复。修复后重新执行 4b 中失败的项目。

全部通过后：
- 首行写入 `<!-- translated: complete -->`（中断文件写 `partial`）
- 注入 `script.js`（封面和目录除外）
- 更新 `progress.md` 的已完成章节列表

关卡（逐项在 progress.md 留下证据，5 项全过才继续下一章）：
① 首行 `<!-- translated: complete -->` 标记
② 段落计数一致（源 = 译）
③ 术语全量检查通过（列出所有已检查术语）
④ 翻译腔 0 命中
⑤ progress.md 已更新（含具体证据）

## 阶段 5：校验

运行：

```bash
"${SKILL_DIR}/scripts/validate_format.sh" output/
```

再做全量检查：

- 逐章对比代码块，确认翻译没有改变代码行为。对比方式：提取源文件和译文的所有代码块，逐块对比非注释部分是否一致。
- 打开封面、目录和所有正文页，测试导航和代码渲染。
- 全量术语一致性检查：遍历术语表所有术语，确认全文统一。

所有失败项必须修复或写入 `report.md` 的已知限制。

## 阶段 6：报告

**读取 `../shared/report-templates.md`** 的 translate-book 段。

在当前 run 目录写 `report.md`。

完成后将 `progress.md` 状态改为 `completed`。

## 质量标准

- 中文表达自然，不把翻译腔和机械直译留给审阅阶段。
- 术语、编号、导航、图片和代码注释在生成阶段一次做对。
- 恢复和补缺只处理必要范围，但必须记录跳过依据。
- 输出可被 integrate-books 和 review-tech-book 通过 `.book-doc/runs/*-translate-*/report.md` 接续使用。
