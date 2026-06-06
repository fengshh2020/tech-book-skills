# 写作规范

> 供 codebase-book 阶段 4 使用。定义章节结构、内容组件、代码讲解模式和 HTML 模板。

---

## 写作原则

1. **代码驱动**：每个知识点都有对应的代码作为锚点，不从概念出发而从代码出发
2. **决策透明**：每个设计选择都说明为什么，读者应理解权衡而非记住结论
3. **渐进深入**：先给出整体图景，再逐层深入细节
4. **可验证**：代码引用精确到文件和行号，知识断言标注验证等级
5. **成组讲解**：按执行路径、数据流、抽象边界组织内容，不按文件逐行流水账
6. **低噪声组件**：知识框用于真正需要停顿理解的内容，不把每个小标题都做成框

---

## 章节结构模板

每章遵循以下结构：

### 1. 本章导读

```html
<div class="chapter-intro">
  <h2>本章导读</h2>
  <div class="learning-objectives">
    <p><strong>学习目标</strong></p>
    <ul>
      <li>目标 1</li>
      <li>目标 2</li>
    </ul>
  </div>
  <div class="prerequisites">
    <p><strong>前置知识</strong>：[链接到前序章节或外部资源]</p>
  </div>
  <div class="chapter-scope">
    <p><strong>本章覆盖</strong>：<code>file1.py</code>、<code>file2.py</code>、<code>file3.py</code></p>
  </div>
</div>
```

### 2. 架构/设计总览

本章涉及的模块在整个系统中的位置，与其他模块的关系。使用自然语言描述，必要时配以简化的代码示例展示模块间的调用关系。

### 3. 代码讲解

核心内容。按分析结果中的顺序，逐段讲解关键代码。

**代码讲解模式**：

- **完整代码块 + 逐段注释**：先展示完整代码块，再逐段讲解
- **关键代码段 + 上下文**：只展示关键段落，说明在完整文件中的位置
- **对比讲解**：展示替代实现，对比分析优劣

选择标准：代码 < 30 行用完整展示；30-80 行用分段展示；> 80 行只展示关键段落并标注在源文件中的位置。

```html
<p class="CodeListingCaption">文件：<code>src/module/core.py</code> 第 23-67 行</p>
<pre><code># 源文件代码，原样保留
</code></pre>
```

讲解紧跟代码块之后，每段讲解对应代码中的一段逻辑。

**避免**：

- 对每个 import、常量、简单 getter 单独解释
- 连续堆叠多个 sidebar 打断正文
- 为了“完整”展示 80 行以上代码块
- 让章节结构变成 `file.py → function_a → function_b` 的文件清单

**推荐**：

- 用一个“执行路径”小节串联多个函数
- 每个代码块后解释它改变了什么状态、建立了什么契约、触发了什么副作用
- 对重复模式只讲一次，后续用交叉引用

### 4. 设计决策分析

```html
<div class="sidebar">
  <p class="sidebar-title">设计决策：[决策名称]</p>
  <p><strong>选择</strong>：[具体选择]</p>
  <p><strong>原因</strong>：[为什么]</p>
  <p><strong>替代方案</strong>：[其他可能的选择] — [为什么没选]</p>
  <p><strong>权衡</strong>：[获得了什么，放弃了什么]</p>
</div>
```

### 5. 知识扩展框

格式见 `knowledge-expansion.md` 中的内容组件规范。标题格式统一为：

- `深入理解：[知识点]` — 语言特性、框架原理、设计模式
- `工程实践：[实践名]` — 错误处理、测试、部署等工程实践
- `背景知识：[主题]` — 算法、协议、标准等

### 6. 关键要点

```html
<div class="chapter-summary">
  <h2>关键要点</h2>
  <ul>
    <li><strong>[概念]</strong>：一句话概括</li>
    <li><strong>[概念]</strong>：一句话概括</li>
  </ul>
</div>
```

---

## HTML 模板

### 通用页面骨架

页面骨架的完整规范参见 `../translate-book/references/html-templates.md`，以该文件为准。以下仅列出 codebase-book 的关键结构和差异点：

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
<script src="script.js"></script>
</body>
</html>
```

### 封面页面

```html
<div class="cover">
  <div class="cover-content">
    <p class="cover-tag">项目驱动学习</p>
    <h1 class="cover-title">项目名</h1>
    <p class="cover-subtitle">技术栈描述</p>
    <p class="cover-author">基于 [版本/commit] 生成</p>
    <a href="01_toc.html" class="cover-cta">开始学习</a>
  </div>
</div>
```

### 特殊页面类型

- **快速上手**（02）：环境搭建 → 安装依赖 → 构建/运行 → 基本使用流程。无 chapter-number span
- **架构总览**（03）：整体架构图（用文字描述或简化代码）+ 模块关系 + 数据流。无 chapter-number span，使用 `<h1>架构总览</h1>`

## 视觉方向

默认使用统一的深色学习指南风格：

- 深色背景 + 左侧章节导航
- 渐变标题用于封面和章节主标题
- 正文卡片保持同一材质，不同类型只用轻微标题色/边框区分
- `h2` 负责大章节层级，`h3` 负责小节组，`h4` 负责局部标签
- 代码块、表格、练习块可使用卡片；普通正文不包卡片

组件密度规则：

- 连续正文中最多每 4-6 个自然段出现一个 sidebar
- 如果 3 个 sidebar 连续出现，改为一个小节 + 列表/表格
- 一段话能说清的知识点直接写在正文，不创建框
- 章节导读、关键要点、练习/检查可以用框；普通小标题不要用框

---

## 写作风格

### 代码讲解语气

- 直接陈述代码行为，不用"我们来看"等引导语
- 说"这段代码做了 X"而不是"让我们来看看这段代码做了什么"
- 设计决策用分析语气：列出选择、原因、权衡，不做价值判断

### 知识扩展语气

- 教学语气：先给出直觉，再给出精确定义
- 用简化的独立示例解释概念，不直接搬用复杂的项目代码
- 关联项目代码："在本项目的 `file.py` 中，你可以看到这个概念的实际应用"

### 术语处理

- 技术术语首次出现时括注英文原文：`装饰器（decorator）`
- 项目特有的概念/命名给出明确界定
- 统一使用中文标点，代码和命令保持原文

### 排版规范

与 translate-book `references/spec.md` 排版规范一致：
- 中英文间加空格
- `第 N 章` 格式
- 代码清单标题用全角冒号
- 代码缩进 4 空格
- sidebar 标题不参与页面大纲
- 每个可见小标题后至少跟随一个自然段或一个相关代码块，避免孤立标题
- `h3/h4` 必须表达真实层级，不用粗体段落冒充标题
