# 写作规范

> 供 codebase-book 阶段 4 使用。定义 HTML 结构、代码讲解模式和视觉规范。
> 内容深度标准和知识扩展方法见 `references/writing-and-content.md`。

## HTML 模板

### 通用页面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>章节标题 - 项目名</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="top-nav">
  <span class="book-title">项目名</span>
  <div class="nav-links">
    <a href="01_toc.html">目录</a>
    <button class="toc-toggle">本节</button>
    <div class="toc-dropdown"></div>
  </div>
</nav>
<div class="prog"></div>
<main class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">第 N 章</span>
    <h1>章节标题</h1>
  </div>
  <div class="chapter-content">
    <!-- 正文 -->
  </div>
  <div class="page-nav">
    <a href="prev.html" class="prev">&larr; 上一页</a>
    <a href="next.html" class="next">下一页 &rarr;</a>
  </div>
</main>
<button class="btt" aria-label="回到顶部">↑</button>
<script src="script.js"></script>
</body>
</html>
```

### 封面

```html
<div class="cover">
  <div class="cover-content">
    <p class="cover-tag">项目深度学习指南</p>
    <h1 class="cover-title">项目名</h1>
    <p class="cover-subtitle">技术栈描述</p>
    <p class="cover-author">基于 [版本/commit] 生成</p>
    <a href="01_toc.html" class="cover-cta">开始阅读</a>
  </div>
</div>
```

### 特殊页面

- **快速上手**（02）：环境搭建 → 构建运行 → 成功信号 → 常见失败
- **架构总览**（03）：整体数据流 + 模块关系 + 设计决策总览
- **速查表**（末尾，可选）：参数速查、命令速查、设计决策索引

## 代码讲解模式

代码讲解是叙事驱动的——先讲思路，再贴代码，代码后紧跟分析。详见 `writing-and-content.md` 的"叙事驱动的代码讲解"。

### 展示方式

| 代码长度 | 展示方式 |
|----------|----------|
| < 30 行 | 完整展示 |
| 30-80 行 | 分段展示，标注在源文件中的位置 |
| > 80 行 | 只贴关键 20-30 行，其余用叙事说明 |

```html
<p class="CodeListingCaption">文件：<code>src/module/core.py</code> 第 23-67 行</p>
<pre data-lang="Python"><code># 源文件代码，原样保留</code></pre>
```

### 避免的写法

- **函数签名罗列**：每个函数单独成节，只有签名+参数+代码块，无叙事串联
- **代码块序列**：连续多个代码块之间只有简短说明，无连贯的分析段落
- **叙事被 sidebar 打断**：在代码走查中间插入 sidebar，读者思路断裂
- **逐行复述**：对 import、常量、简单 getter 逐个解释

### 推荐的写法

- 用一条执行路径串联多个函数，代码在叙事需要时自然出现
- 每段代码后分析它的关键设计、参数影响、边界情况
- 重复模式只讲一次，后续交叉引用
- 背景知识融入叙事段落，不在代码走查中间开 sidebar

## 可选组件

以下 CSS 组件在内容自然需要时使用，不强制每章都包含：

| class | 用途 | 适用场景 |
|-------|------|---------|
| `.sidebar` | 知识扩展框 | 需要 3-8 段讲解的背景知识 |
| `.sidebar.warning` | 工程实践/警告 | 常见陷阱、最佳实践 |
| `.dev-task` | 能力目标卡片 | 章节开头列出读者将学会什么 |
| `.debug-map` | 调试地图 | 模块有多个常见失败模式时 |
| `.change-impact` | 修改影响 | 模块接口复杂、修改易出错时 |
| `.safe-zone` / `.risk-zone` / `.cascade` | 修改区域分类 | change-impact 内部子组件 |
| `.practice` | 实战练习 | 章末提供具体动手任务 |
| `.cheatsheet` | 速查表 | 最终章节的参数/命令索引 |
| `.chapter-summary` | 章节总结 | 章末回顾要点 |
| `.chapter-intro` | 章节导读 | 章首概述本章内容和覆盖范围 |
| `.flow-position` | 运行位置 | 标注本章代码在全局链路中的位置 |
| `.chapter-scope` | 覆盖范围 | 列出本章涉及的源文件 |

## 视觉方向

使用统一的高端自适应设计系统（`assets/style.css`）。设计语言：安静奢华——通过克制而非装饰传达品质。

### 标题层级

| 层级 | 视觉表现 | 典型用途 |
|------|----------|----------|
| `h2` | 渐变文字 + 底部分隔线 | 主节标题 |
| `h3` | 左侧蓝色边框 + 微光背景 | 话题组 |
| `h4` | 常规加粗 | 具体话题 |
| `h5` | 大写微标签 | 细节配置 |

设计系统根据页面实际使用的标题深度自动调整权重。

### 组件密度

- 连续正文中最多每 4-6 段出现一个 sidebar
- 一段话能说清的直接写正文，不创建框
- 代码块使用 `data-lang` 标注语言，复制按钮由 JS 自动注入
