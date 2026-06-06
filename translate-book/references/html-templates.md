# HTML 结构契约

以下是页面语义结构和关键交互挂载点，不是固定视觉模板。生成页面时保留可读性、导航、锚点、代码块、表格和响应式基础体验；具体布局、封面表现、视觉主题、装饰层次和动效可根据书籍气质重新设计。

## 通用页面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题 - 书名</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="top-nav">
  <span class="book-title">书名（中文版）</span>
  <div class="nav-links">
    <a href="01_toc.html">目录</a>
    <button class="toc-toggle">本节</button>
    <div class="toc-dropdown"></div>
  </div>
</nav>
<main class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">第 N 章</span>
    <h1>章节标题</h1>
  </div>
  <div class="chapter-content">
    <!-- 正文内容 -->
  </div>
  <div class="page-nav">
    <a href="prev.html" class="prev">&larr; 上一页</a>
    <a href="next.html" class="next">下一页 &rarr;</a>
  </div>
</main>
<script>
// 顶部下拉章节目录 + 键盘翻页（从 script.js 注入）
</script>
</body>
</html>
```

可调整项：导航视觉形式、标题区布局、正文宽度、色彩系统、封面构图、组件装饰和动效。  
不应破坏项：`style.css` 引用、目录入口、正文容器、跨章翻页、脚本挂载点、锚点和语义层级。

## 封面页面

```html
<div class="cover">
  <!-- 可按书籍主题替换装饰层、背景图或视觉构图 -->
  <div class="cover-content">
    <h1 class="cover-title">书名</h1>
    <p class="cover-subtitle">英文副标题</p>
    <p class="cover-subtitle-cn">中文副标题</p>
    <p class="cover-author">作者</p>
    <p class="cover-edition">中文翻译版</p>
    <a href="01_toc.html" class="cover-cta">开始阅读</a>
  </div>
</div>
```

封面应第一眼传达书籍名称、作者和进入阅读的入口。是否使用背景图、插画、几何装饰、双栏构图或极简排版，由书籍气质决定。封面通常无导航栏、无翻页按钮、无 JS。

## 目录页面

```html
<main class="chapter">
  <h1>目录</h1>
  <p class="toc-part">部分名称</p>
  <ul class="toc-list">
    <li><a href="04_chapter1.html">第 1 章：标题</a></li>
  </ul>
</main>
```

目录页应便于快速扫描章节层级。可以使用列表、分组、章节摘要或进度样式；通常无 chapter-header、无 chapter-content 包裹、无翻页按钮、无下拉目录 JS。

## 前言页面

建议使用一个 `chapter-header`（无 chapter-number span）+ `chapter-content` 内多个 `h2` 子部分。有导航栏、翻页、JS。若前言内容很短，也可采用更轻的标题区，只要目录、标题和导航一致。

## 章节页

推荐结构：`nav`（含 toc-toggle + toc-dropdown）→ `chapter-header` → `chapter-content` → `page-nav` → `<script>` 注入。可以调整标题区视觉和内容组件样式，但不要移除正文容器、目录挂载点和翻页导航。

## 附录页面

与章节页结构相同，但 chapter-header 中使用"附录 X"而非"第 N 章"：

```html
<div class="chapter-header">
  <span class="chapter-number">附录 A</span>
  <h1>附录标题</h1>
</div>
```

附录页有导航栏、翻页、JS。内容通常是参考手册或速查表。

## 术语表页面

完整术语表页面，使用 glossary-term 组件：

```html
<main class="chapter">
  <div class="chapter-header">
    <h1>术语表</h1>
  </div>
  <div class="chapter-content">
    <p class="glossary-term">装饰器（decorator）</p>
    <p>一种以另一个函数为参数并返回新函数的函数...</p>

    <p class="glossary-term">生成器（generator）</p>
    <p>使用 yield 关键字返回值的函数...</p>
  </div>
</main>
```

有导航栏、翻页、JS。无 chapter-number span。术语按拼音或字母顺序排列。

## 内容组件模板

### 代码块

```html
<pre><code>def hello():
    print("Hello")
</code></pre>
```

- 装饰元素、语言标签、复制按钮等必须放在 `<pre><code>` 外，不影响代码复制和朗读；是否使用由页面设计决定
- 禁止 `<code>` 嵌套
- 代码缩进 4 空格
- 代码块内 `<em>` 和 `<b>` 统一替换为 `<strong>`

### 代码标题

```html
<p class="CodeListingCaption">Listing 7-1: 初始化一个类</p>
```

位于代码块下方或上方均可，但全书需统一。视觉应弱于正文标题，避免抢占代码块注意力。

### 旁注/提示框

```html
<div class="sidebar">
  <p class="sidebar-title">PEDANTIC NOTE</p>
  <p>旁注内容</p>
</div>
```

GOTCHA ALERT 使用 `class="sidebar warning"`。sidebar 内的 h2/h3/h4 不参与下拉目录扫描。

### 表格

```html
<div class="table-wrapper">
  <table>
    <thead><tr><th>列1</th><th>列2</th></tr></thead>
    <tbody><tr><td>值1</td><td>值2</td></tr></tbody>
  </table>
</div>
```

### 术语表

```html
<p class="glossary-term">术语名（英文原文）</p>
<p>定义内容</p>
```

### 两层内容结构（章→节）

层级：`<main> → <section>`。section 无容器样式，内部直接写连续段落。

```html
<div class="chapter-content">
  <p>本章导语...</p>
  <section>
    <h2>节标题</h2>
    <h4 id="item-1">话题关键词</h4>
    <p>内容段落...</p>
  </section>
</div>
```

锚点用 `<h4 id="item-{N}">话题关键词</h4>`，全局连续编号。跨文件引用：`<a href="chapter_file.html#item-N">`。
