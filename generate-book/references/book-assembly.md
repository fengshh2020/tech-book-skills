# 书籍组装（Book Assembly）

本文档定义页面语义结构、HTML 模板、组件契约和交互挂载点。`style.css` 提供自适应设计系统 —— 标题层级、组件分布和视觉权重会根据书籍的内容结构自动调整。生成页面时，请根据书籍的实际标题深度选择合适的模式。

## HTML 脚手架结构

所有内容页面共享的通用页面骨架：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Book Title</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="top-nav">
  <span class="book-title">Book Title (Chinese Edition)</span>
  <div class="nav-links">
    <a href="01_toc.html">Table of Contents</a>
    <button class="toc-toggle">This Section</button>
    <div class="toc-dropdown"></div>
  </div>
</nav>
<div class="prog"></div>
<main class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter N</span>
    <h1>Chapter Title</h1>
  </div>
  <div class="chapter-content">
    <!-- Body content -->
  </div>
  <div class="page-nav">
    <a href="prev.html" class="prev">&larr; Previous</a>
    <a href="next.html" class="next">Next &rarr;</a>
  </div>
</main>
<button class="btt" aria-label="Back to top">↑</button>
<script src="script.js"></script>
</body>
</html>
```

**可调整项**：导航视觉风格、头部区域布局、正文宽度、色彩体系、封面构图、组件装饰和动画。

**不可破坏项**：`style.css` 引用、目录条目、正文容器、跨章翻页导航、脚本挂载点、锚点和语义层级。

## 文件编号约定

| 编号 | 文件 |
|------|------|
| 00 | `00_cover.html` |
| 01 | `01_toc.html` |
| 02 | `02_front.html` |
| 03 | `03_intro.html` |
| 04+ | `{NN}_chapter{M}.html` |
| N+ | `{NN}_appendix_{x}.html` |

章节编号必须与 EPUB spine 顺序一致。编号确保正确的排序和页面间导航链接。

## 页面类型

### 封面页（Cover Page）

```html
<div class="cover">
  <!-- Decorative layer, background image, or visual composition can be replaced per book theme -->
  <div class="cover-content">
    <h1 class="cover-title">Book Title</h1>
    <p class="cover-subtitle">English Subtitle</p>
    <p class="cover-subtitle-cn">Chinese Subtitle</p>
    <p class="cover-author">Author</p>
    <p class="cover-edition">Chinese Translation Edition</p>
    <a href="01_toc.html" class="cover-cta">Start Reading</a>
  </div>
</div>
```

封面应立即传达书名、作者和阅读入口。是否使用背景图片、插图、几何装饰、双栏构图或极简排版，取决于书籍的定位。封面通常没有导航栏、没有翻页按钮、没有 JS。

### 目录页（Table of Contents）

```html
<main class="chapter">
  <h1>Table of Contents</h1>
  <p class="toc-part">Part Name</p>
  <ul class="toc-list">
    <li><a href="04_chapter1.html">Chapter 1: Title</a></li>
  </ul>
</main>
```

目录页应允许快速扫描章节层级。可使用列表、分组、章节摘要或进度指示器。通常没有 `chapter-header`、没有 `chapter-content` 包裹、没有翻页按钮、没有下拉目录 JS。

### 前言页（Preface Page）

推荐结构：一个 `chapter-header`（不带 `chapter-number` span）+ `chapter-content` 内的多个 `h2` 小节。有导航栏、翻页和 JS。如果前言非常简短，可以使用更轻量的头部区域，只要目录、标题和导航保持一致即可。

### 章节页（Chapter Page）

推荐结构：`nav`（带 `toc-toggle` + `toc-dropdown`）-> `chapter-header` -> `chapter-content` -> `page-nav` -> `<script>` 注入。可调整头部区域视觉和内容组件样式，但不要移除正文容器、目录挂载点或翻页导航。

### 附录页（Appendix Page）

与章节页结构相同，但在 `chapter-header` 中使用"附录 X"代替"第 N 章"：

```html
<div class="chapter-header">
  <span class="chapter-number">Appendix A</span>
  <h1>Appendix Title</h1>
</div>
```

附录页有导航栏、翻页和 JS。内容通常是参考资料或速查表。

### 术语表页（Glossary Page）

使用术语组件的完整术语表页面：

```html
<main class="chapter">
  <div class="chapter-header">
    <h1>Glossary</h1>
  </div>
  <div class="chapter-content">
    <p class="glossary-term">decorator</p>
    <p>A function that takes another function as an argument and returns a new function...</p>

    <p class="glossary-term">generator</p>
    <p>A function that uses the yield keyword to return values...</p>
  </div>
</main>
```

有导航栏、翻页和 JS。没有 `chapter-number` span。术语按拼音或字母顺序排列。

## 内容组件

### 代码块（Code Blocks）

```html
<pre data-lang="Python"><code>def hello():
    print("Hello")
</code></pre>
```

- 使用 `data-lang` 属性标注语言类型，显示在代码块顶部工具栏
- 代码复制按钮由 `script.js` 自动注入，无需手动添加
- 不允许嵌套 `<code>`
- 代码缩进使用 4 个空格
- 代码块内的 `<em>` 和 `<b>` 统一替换为 `<strong>`

### 代码标题（Code Titles）

```html
<p class="CodeListingCaption">Listing 7-1: Initializing a class</p>
```

可放在代码块上方或下方，但全书必须保持一致。视觉权重应轻于正文标题，避免与代码块争夺注意力。

### 侧边栏/提示框（Sidebars/Tip Boxes）

```html
<div class="sidebar">
  <p class="sidebar-title">PEDANTIC NOTE</p>
  <p>Sidebar content</p>
</div>
```

GOTCHA ALERT 使用 `class="sidebar warning"`。侧边栏内的 h2/h3/h4 标题不参与下拉目录扫描。

可用的侧边栏变体（通过额外 class 区分视觉风格）：

| class | 用途 | 强调色 |
|-------|------|--------|
| `.sidebar` | 通用侧边栏 | 默认 |
| `.sidebar.warning` | 警告/注意事项 | 红色 |
| `.learn` | 学习目标 | 蓝色 |
| `.check` | 检查清单 | 蓝色 |
| `.quick-start` | 快速入门 | 蓝色 |
| `.things-to-remember` | 要点回顾 | 绿色 |
| `.author-advice` | 作者建议 | 绿色 |
| `.theory-note` | 理论说明 | 琥珀色 |
| `.pedantic-note` | 学究式注释 | 琥珀色 |
| `.performance-tip` | 性能提示 | 蓝色 |
| `.gotcha-alert` | 陷阱警告 | 红色 |
| `.error-cheatsheet` | 错误速查 | 红色 |

### 表格（Tables）

```html
<div class="table-wrapper">
  <table>
    <thead><tr><th>Column 1</th><th>Column 2</th></tr></thead>
    <tbody><tr><td>Value 1</td><td>Value 2</td></tr></tbody>
  </table>
</div>
```

### 术语条目（Glossary Terms）

```html
<p class="glossary-term">Term Name (English Original)</p>
<p>Definition content</p>
```

### 自适应内容层级（Adaptive Content Levels）

设计系统根据书籍的内容结构自动调整视觉权重。生成页面时，请根据书籍的实际标题深度选择合适的模式：

**2 级结构**（h2 -> h4）—— 简洁型，适用于内容扁平的书籍：

```html
<div class="chapter-content">
  <section>
    <h2>Section Title</h2>
    <h4 id="item-1">Topic Keyword</h4>
    <p>Content paragraph...</p>
  </section>
</div>
```

- h2 使用渐变文字加底部分隔线，作为大块标题
- h4 自动显示为药丸标签（Pill Tag，蓝色圆角小标签）
- 当没有 h3 时，h2 自动获得更大字号（由 CSS `:not(:has(h4))` 选择器驱动）

**3 级结构**（h2 -> h3 -> h4）—— 标准型，适用于大多数技术书籍：

```html
<div class="chapter-content">
  <section>
    <h2>Major Section Title</h2>
    <h3>Topic Group</h3>
    <h4 id="item-1">Specific Topic</h4>
    <p>Content paragraph...</p>
  </section>
</div>
```

- h2 = 渐变大节标题
- h3 = 卡片式分组标题（左侧蓝色边框 + 淡发光背景）
- h4 = 行内子主题标记

**4 级结构**（h2 -> h3 -> h4 -> h5）—— 深度型，适用于复杂架构书籍：

```html
<div class="chapter-content">
  <section>
    <h2>System Overview</h2>
    <h3>Module Group</h3>
    <h4>Specific Module</h4>
    <h5>Configuration Item</h5>
    <p>Content paragraph...</p>
  </section>
</div>
```

- h5 自动显示为大写微标签（小字号、柔和色、大写字母）
- 下拉目录自动为 h3/h4 添加缩进（由 `data-depth` 属性驱动）
- 侧边栏导航链接也会根据深度自动缩进

锚点使用 `<h4 id="item-{N}">` 或 `<h3 id="item-{N}">`，全局顺序编号。跨文件引用：`<a href="chapter_file.html#item-N">`。

### 组件分布指南

根据内容密度控制组件间距：

| 内容密度 | 侧边栏频率 | 代码块间距 | 最大连续组件数 |
|---------|-----------|-----------|--------------|
| 低（以概念/介绍为主） | 每 6-8 段 | 每 3-4 段 | 1 个侧边栏 + 1 个代码块 |
| 中（概念 + 代码混合） | 每 4-6 段 | 每 2-3 段 | 2 个连续组件 |
| 高（代码密集） | 每 6-8 段 | 每 1-2 段 | 不超过 3 个连续代码块 |

---

## 高级组件（v2.0）

以下组件由 `style.css` v2.0 和 `script.js` v2.0 提供。所有交互由 JS 自动挂载；HTML 只需正确的 class 名称。

### 可折叠区域（Collapsible Areas）

用于可选内容、深入讨论或进阶主题 —— 减少页面压力：

```html
<div class="collapsible">
  <button class="collapsible__trigger">Expand: Advanced Configuration Options</button>
  <div class="collapsible__body">
    <p>Collapsed content...</p>
  </div>
</div>
```

- 点击触发器切换展开/折叠
- JS 自动处理 `aria-expanded` 和动画
- 默认折叠；添加 `.open` class 可默认展开

### 代码标签页（Code Tabs）

多语言代码对比（Python/Rust/Go 等）：

```html
<div class="code-tabs">
  <div class="code-tabs__bar">
    <button class="code-tabs__tab active" data-index="0">Python</button>
    <button class="code-tabs__tab" data-index="1">Rust</button>
    <button class="code-tabs__tab" data-index="2">Go</button>
  </div>
  <div class="code-tabs__panel active" data-index="0">
    <pre data-lang="Python"><code>print("Hello")</code></pre>
  </div>
  <div class="code-tabs__panel" data-index="1">
    <pre data-lang="Rust"><code>println!("Hello");</code></pre>
  </div>
  <div class="code-tabs__panel" data-index="2">
    <pre data-lang="Go"><code>fmt.Println("Hello")</code></pre>
  </div>
</div>
```

- JS 自动处理点击切换和键盘导航
- `data-index` 匹配标签页到面板

### 全文搜索（Full-Text Search）

搜索模态框由 JS 自动创建，无需 HTML。触发方式：
- `Ctrl+K` 或 `Cmd+K` 键盘快捷键
- JS 自动索引页面上所有 h2-h5 和代码块

### 页面大纲导航（Page Outline Navigation）

大纲由 JS 自动生成，固定在页面右侧（视口宽度 >1200px 时显示），无需 HTML。自动跟踪当前阅读位置。

### 面包屑导航（Breadcrumbs）

```html
<nav class="breadcrumbs">
  <a class="breadcrumbs__item" href="toc.html">Part One</a>
  <span class="breadcrumbs__sep">›</span>
  <a class="breadcrumbs__item" href="ch03.html">Chapter 3</a>
  <span class="breadcrumbs__sep">›</span>
  <span class="breadcrumbs__item">Architecture Design</span>
</nav>
```

- 插入到 `.chapter-header` 上方
- 最后一项是当前页面，不可点击

### 差异视图（Diff View）

代码前后对比：

```html
<div class="diff-block">
  <div class="diff-chunk-header">src/main.py</div>
  <pre><code><span class="diff-del">- print("Hello World")</span>
<span class="diff-add">+ print("Hello, Zenoh!")</span></code></pre>
</div>
```

- `.diff-del` = 删除行（红色），`.diff-add` = 新增行（绿色）
- 宽屏自动切换为并排对比

### 测验（Quizzes）

```html
<div class="quiz">
  <p class="quiz__question">What is Zenoh's default communication mode?</p>
  <div class="quiz__answers">
    <button class="quiz__answer" data-correct="false">A. Client-Server</button>
    <button class="quiz__answer" data-correct="true">B. Pub/Sub</button>
    <button class="quiz__answer" data-correct="false">C. Request/Response</button>
    <button class="quiz__answer" data-correct="false">D. Point-to-Point</button>
  </div>
  <div class="quiz__explain">
    Zenoh's core communication mode is Pub/Sub, while also supporting Query/Reply.
  </div>
</div>
```

- `data-correct="true"` 标记正确答案
- JS 自动验证、显示反馈并揭示解析
- 回答后自动禁用

### 文件树（File Trees）

```html
<div class="file-tree">
  <div class="file-tree__dir">
    <span class="file-tree__name">src/</span>
    <div class="file-tree__file"><span class="file-tree__name">main.rs</span></div>
    <div class="file-tree__file active"><span class="file-tree__name">lib.rs</span></div>
    <div class="file-tree__dir">
      <span class="file-tree__name">network/</span>
      <div class="file-tree__file"><span class="file-tree__name">tcp.rs</span></div>
      <div class="file-tree__file"><span class="file-tree__name">udp.rs</span></div>
    </div>
  </div>
  <div class="file-tree__file"><span class="file-tree__name">Cargo.toml</span></div>
</div>
```

- 目录可点击展开/折叠
- `.active` 高亮当前文件

### 图编号（Figure Numbering）

```html
<div class="svg-diagram">
  <!-- SVG content -->
</div>
<p class="fig-caption" data-num>Architecture Layer Diagram</p>
```

- `data-num` 属性触发 CSS 计数器自动编号：显示为"图 3-2：架构层图"
- 不加 `data-num` 则不编号

### 交叉引用（Cross-References）

```html
<p>As shown in <a class="xref xref--fig" href="#fig-arch">Figure 3-2</a>,
see <a class="xref xref--listing" href="#lst-hello">Listing 4-1</a>,
for details see <a class="xref xref--chapter" href="ch05.html">Chapter 5</a>.</p>
```

### 定义列表（Definition Lists）

```html
<div class="def-list">
  <p class="def-list__term">Session</p>
  <p class="def-list__def">Zenoh's core component, managing all network connections.</p>
  <p class="def-list__term">KeyExpr</p>
  <p class="def-list__def">Key expression, Zenoh's address space, supports wildcards.</p>
</div>
```

### API 参考（API References）

```html
<div class="api-ref">
  <div class="api-ref__signature">
    <code>session.put(key_expr: str, payload: Any, **kwargs) -> None</code>
  </div>
  <div class="api-ref__params">
    <div class="api-ref__param">
      <span class="api-ref__param-name">key_expr</span>
      <span class="api-ref__param-type">str | KeyExpr</span>
      <span class="api-ref__param-desc">Target key expression</span>
    </div>
    <div class="api-ref__param">
      <span class="api-ref__param-name">payload</span>
      <span class="api-ref__param-type">Any</span>
      <span class="api-ref__param-desc">Data to publish</span>
    </div>
  </div>
  <div class="api-ref__returns">No return value</div>
</div>
```

### 代码标注（Code Annotations）

```html
<pre data-lang="Python"><code>with zenoh.open(zenoh.Config()) as session:  <span class="code-annotation__marker" data-note="1"></span>
    session.put("demo/key", "Hello")         <span class="code-annotation__marker" data-note="2"></span>
</code></pre>
<ol class="code-annotation__list">
  <li class="code-annotation__item">Using `with` ensures the session is properly closed</li>
  <li class="code-annotation__item">`put()` is a shortcut for one-time publishing</li>
</ol>
```

### 学习目标（Learning Objectives）

```html
<div class="learning-objectives">
  <p class="learning-objectives__title">Chapter Learning Objectives</p>
  <ul class="learning-objectives__list">
    <li class="learning-objectives__item">Understand Zenoh's three node modes</li>
    <li class="learning-objectives__item">Master key expression wildcard rules</li>
    <li class="learning-objectives__item">Be able to implement pub/sub in Python</li>
  </ul>
</div>
```

- JS 自动将勾选状态持久化到 localStorage

### 视频嵌入（Video Embeds）

```html
<div class="video-wrap video-wrap--16x9">
  <iframe src="https://www.youtube.com/embed/xxx" allowfullscreen></iframe>
</div>
<p class="fig-caption" data-num>Zenoh Architecture Overview</p>
```

### 数学公式（Math Formulas）

```html
<p>Time complexity is <span class="math-inline">O(n \log n)</span>.</p>
<div class="math-block">
  $$E = mc^2$$
</div>
```

- JS 自动检测并加载 KaTeX 渲染

### 终端输出（Terminal Output）

```html
<div class="terminal">
  <div class="terminal__header"></div>
  <div class="terminal__body">
    <span class="terminal__prompt">$ </span><span class="terminal__cmd">pip install eclipse-zenoh</span>
    <span class="terminal__output">Successfully installed eclipse-zenoh-1.9.0</span>
  </div>
</div>
```

### 互动练习（Interactive Exercises）

```html
<div class="exercise">
  <p class="exercise__prompt">Try it: Modify the subscriber code above to only subscribe to temperature sensor data.</p>
  <button class="exercise__solution-btn">Show Answer</button>
  <div class="exercise__solution">
    <pre data-lang="Python"><code>session.declare_subscriber("sensor/**/temperature")</code></pre>
  </div>
</div>
```

### 阅读辅助（Reading Aids）

```html
<p class="reading-time"></p>  <!-- JS automatically calculates and inserts -->
<span class="difficulty difficulty--beginner">Beginner</span>
<span class="difficulty difficulty--intermediate">Intermediate</span>
<span class="difficulty difficulty--advanced">Advanced</span>
```

### 徽章系统（Badge System）

```html
<span class="badge badge--stable">Stable</span>
<span class="badge badge--beta">Beta</span>
<span class="badge badge--deprecated">Deprecated</span>
<span class="badge badge--new">New</span>
<span class="badge badge--experimental">Experimental</span>
<span class="badge badge--version">v1.8+</span>
```

### 脚注（Footnotes）

```html
<p>Zenoh's wire overhead is only 4-6 bytes<a class="footnote-ref" href="#fn-1">[1]</a>.</p>
<!-- At bottom of chapter -->
<div class="footnotes">
  <div class="footnotes__item" id="fn-1">
    <a href="#fn-ref-1">↑</a> Wire overhead refers to the protocol header size, excluding payload.
  </div>
</div>
```

### 无障碍工具（Accessibility Tools）

```html
<!-- At the very top of the page, start of body -->
<a class="skip-link" href="#main-content">Skip to content</a>
<!-- Main content -->
<main id="main-content" class="mn">...</main>
```

- `.sr-only` 用于仅供屏幕阅读器（Screen Reader）可见的文本

### DrawIO/SVG 图表

DrawIO 文件在构建时转换为 SVG 并嵌入：

```html
<div class="svg-diagram arch-diagram">
  <svg><!-- Theme-aware SVG --></svg>
</div>
<p class="fig-caption" data-num>System Architecture Diagram</p>
```

- 在 SVG 内部使用 `currentColor` 和 CSS 变量以支持主题切换
- 语义化 class 名称：`.arch-diagram`、`.flow-diagram`、`.seq-diagram`
- JS 在主题切换时自动同步 SVG 颜色

### 主题和字号（Theme and Font Size）

```html
<!-- Theme toggle (existing) -->
<button class="sb-toggle">☀️</button>

<!-- Font size adjustment (new) -->
<!-- JS can switch via html[data-font-scale] -->
<!-- Supported: "default" (16px), "large" (18px), "xl" (20px) -->
```

### 键盘快捷键（Keyboard Shortcuts）

按 `?` 键显示快捷键面板。内置快捷键：

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+K` | 全文搜索 |
| `←` / `→` | 上一页 / 下一页 |
| `?` | 键盘快捷键帮助 |
| `Escape` | 关闭模态框/搜索 |

## CSS/JS 集成

`style.css` 提供高端自适应设计系统，采用"静奢"（Quiet Luxury）设计语言 —— 通过克制而非装饰来传达品质。生成页面时，优先保证阅读体验和结构一致性，同时根据书籍的内容层级和受众调整组件分布。

### 设计系统核心特性

- **自适应层级（Adaptive Hierarchy）**：标题视觉权重根据页面实际的 h2/h3/h4/h5 深度自动调整。扁平结构（2 级）自动放大 h2；深层结构（4 级）自动为 h5 添加微标签
- **双主题 + 系统偏好**：支持深色/浅色主题，检测 `prefers-color-scheme`，设置持久化到 `localStorage`
- **玻璃拟态交互层（Glass-Morphism）**：导航栏、复制按钮和返回顶部均使用 `backdrop-filter` 毛玻璃效果
- **代码块**：`data-lang` 语言标签 + 自动复制按钮（悬停时显示），未设置时从 hljs class 自动检测
- **阅读体验**：`requestAnimationFrame` 进度条、弹性缓动滚动揭示（Scroll Reveal）、键盘翻页、当前节高亮

### 必要体验约束

- 正文宽度、行高、字号和段间距必须适合长时间阅读
- 代码块、表格、侧边栏和术语表在桌面端和移动端都必须清晰可读
- 顶部导航、目录、上/下页和键盘翻页必须正常运作
- 页面在移动端不得水平溢出；打印时隐藏交互控件
- 颜色、对比度和强调风格必须服务于技术内容，不得喧宾夺主

## 导航结构

交互系统由 `script.js` 自动提供：

- **智能目录（Smart TOC）**：自动检测页面标题深度，构建带缩进和当前节高亮的层级下拉目录
- **阅读进度条**（`.prog`）：渐变进度指示器，使用 `requestAnimationFrame` 平滑渲染
- **代码复制**：悬停时显示的毛玻璃风格复制按钮，支持 Clipboard API 并带降级方案
- **滚动揭示（Scroll Reveal）**：标题、代码块、卡片等元素进入视口时淡入上滑，由 IntersectionObserver 驱动
- **返回顶部**（`.btt`）：毛玻璃风格，滚动超过 500px 后出现
- **键盘翻页**：左右方向键触发上/下页（在输入框内自动跳过）
- **主题切换**（`.sb-toggle`）：深色/浅色切换，支持 `prefers-color-scheme` 检测 + `localStorage` 持久化
- **自动语言检测**：未设置 `data-lang` 的代码块从 hljs class 自动检测语言标签

## CSS Class 命名约定

以下结构性 class 名称必须保留 —— 它们是 HTML 模板与 CSS 设计系统之间的契约：

- `.chapter` / `.art` —— 章节主容器
- `.chapter-header` / `.chapter-number` —— 章节标题区域
- `.chapter-content` —— 正文内容容器
- `.sidebar` / `.sidebar.warning` —— 侧边栏框（多种变体 class）
- `.CodeListingCaption` —— 代码清单标题
- `.page-nav` / `.prev` / `.next` —— 翻页导航
- `.top-nav` / `.toc-toggle` / `.toc-dropdown` —— 顶部导航栏
- `.table-wrapper` —— 表格滚动容器
- `.glossary-term` —— 术语条目
- `.cover` / `.cover-content` —— 封面页
- `.prog` —— 阅读进度条
- `.btt` —— 返回顶部按钮
- `.sb-link[data-depth]` —— 侧边栏层级导航链接

视觉主题、布局细节、封面呈现、组件装饰和动画均可调整。优先在 `style.css` 中实现样式；仅在单页有特定语义或资产需求时才在 HTML 中添加最少的局部 class，避免内联样式泛滥。
