# Book Assembly

This document defines page semantic structure, HTML templates, component contracts, and interaction mount points. `style.css` provides an adaptive design system — heading levels, component distribution, and visual weights adjust automatically based on the book's content structure. When generating pages, select the appropriate mode based on the book's actual heading depth.

## HTML Scaffold Structure

The generic page skeleton shared by all content pages:

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

**Adjustable**: Navigation visual style, header area layout, body width, color system, cover composition, component decoration and animations.

**Must not break**: `style.css` reference, TOC entry, body container, cross-chapter page navigation, script mount points, anchors, and semantic hierarchy.

## File Numbering Convention

| Number | File |
|--------|------|
| 00 | `00_cover.html` |
| 01 | `01_toc.html` |
| 02 | `02_front.html` |
| 03 | `03_intro.html` |
| 04+ | `{NN}_chapter{M}.html` |
| N+ | `{NN}_appendix_{x}.html` |

Chapter numbers must map to the EPUB spine order. The numbering ensures correct sort order and navigation links between pages.

## Page Types

### Cover Page

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

The cover should immediately convey the book name, author, and entry point to reading. Whether to use background images, illustrations, geometric decorations, two-column composition, or minimalist typography depends on the book's character. The cover typically has no navigation bar, no page-turn buttons, and no JS.

### Table of Contents

```html
<main class="chapter">
  <h1>Table of Contents</h1>
  <p class="toc-part">Part Name</p>
  <ul class="toc-list">
    <li><a href="04_chapter1.html">Chapter 1: Title</a></li>
  </ul>
</main>
```

The TOC page should allow quick scanning of chapter hierarchy. Lists, groupings, chapter summaries, or progress indicators can be used. Typically no `chapter-header`, no `chapter-content` wrapper, no page-turn buttons, and no dropdown TOC JS.

### Preface Page

Recommended structure: one `chapter-header` (without `chapter-number` span) + multiple `h2` subsections inside `chapter-content`. Has navigation bar, page-turn, and JS. If the preface is very short, a lighter header area is acceptable as long as TOC, headings, and navigation remain consistent.

### Chapter Page

Recommended structure: `nav` (with `toc-toggle` + `toc-dropdown`) → `chapter-header` → `chapter-content` → `page-nav` → `<script>` injection. You can adjust the header area visual and content component styles, but do not remove the body container, TOC mount point, or page-turn navigation.

### Appendix Page

Same structure as chapter pages, but use "Appendix X" instead of "Chapter N" in the chapter-header:

```html
<div class="chapter-header">
  <span class="chapter-number">Appendix A</span>
  <h1>Appendix Title</h1>
</div>
```

Appendix pages have navigation bar, page-turn, and JS. Content is typically reference material or cheat sheets.

### Glossary Page

Full glossary page using the glossary-term component:

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

Has navigation bar, page-turn, and JS. No `chapter-number` span. Terms are sorted by pinyin or alphabetical order.

## Content Components

### Code Blocks

```html
<pre data-lang="Python"><code>def hello():
    print("Hello")
</code></pre>
```

- Use the `data-lang` attribute to label the language type, displayed in the code block's top toolbar
- Code copy button is automatically injected by `script.js`, no manual addition needed
- No nested `<code>` allowed
- Code indented with 4 spaces
- `<em>` and `<b>` inside code blocks are uniformly replaced with `<strong>`

### Code Titles

```html
<p class="CodeListingCaption">Listing 7-1: Initializing a class</p>
```

Can be placed above or below the code block, but must be consistent throughout the book. Visual weight should be lighter than body headings to avoid competing with the code block for attention.

### Sidebars/Tip Boxes

```html
<div class="sidebar">
  <p class="sidebar-title">PEDANTIC NOTE</p>
  <p>Sidebar content</p>
</div>
```

GOTCHA ALERT uses `class="sidebar warning"`. Headings h2/h3/h4 inside sidebars are excluded from the dropdown TOC scan.

Available sidebar variants (distinguished by additional class for visual style):

| class | Purpose | Accent Color |
|-------|---------|-------------|
| `.sidebar` | General sidebar | Default |
| `.sidebar.warning` | Warning/gotcha | Red |
| `.learn` | Learning objectives | Blue |
| `.check` | Checklist | Blue |
| `.quick-start` | Quick start | Blue |
| `.things-to-remember` | Key takeaways | Green |
| `.author-advice` | Author advice | Green |
| `.theory-note` | Theory note | Amber |
| `.pedantic-note` | Pedantic note | Amber |
| `.performance-tip` | Performance tip | Blue |
| `.gotcha-alert` | Gotcha alert | Red |
| `.error-cheatsheet` | Error cheat sheet | Red |

### Tables

```html
<div class="table-wrapper">
  <table>
    <thead><tr><th>Column 1</th><th>Column 2</th></tr></thead>
    <tbody><tr><td>Value 1</td><td>Value 2</td></tr></tbody>
  </table>
</div>
```

### Glossary Terms

```html
<p class="glossary-term">Term Name (English Original)</p>
<p>Definition content</p>
```

### Adaptive Content Levels

The design system automatically adjusts visual weights based on the book's content structure. When generating pages, select the appropriate mode based on the book's actual heading depth:

**2-Level Structure** (h2 → h4) — Concise type, suitable for books with flat content:

```html
<div class="chapter-content">
  <section>
    <h2>Section Title</h2>
    <h4 id="item-1">Topic Keyword</h4>
    <p>Content paragraph...</p>
  </section>
</div>
```

- h2 uses gradient text with bottom separator line, serving as large block headings
- h4 automatically displays as a pill tag (blue rounded small label)
- When no h3 is present, h2 automatically gets a larger font size (driven by CSS `:not(:has(h4))` selector)

**3-Level Structure** (h2 → h3 → h4) — Standard type, most technical books:

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

- h2 = gradient large section heading
- h3 = card-style group heading (left blue border + subtle glow background)
- h4 = inline sub-topic marker

**4-Level Structure** (h2 → h3 → h4 → h5) — Deep type, suitable for complex architecture books:

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

- h5 automatically displays as an uppercase micro-label (small, muted color, uppercase)
- TOC dropdown automatically adds indentation for h3/h4 (driven by `data-depth` attribute)
- Sidebar navigation links also auto-indent based on depth

Anchors use `<h4 id="item-{N}">` or `<h3 id="item-{N}">`, with globally sequential numbering. Cross-file references: `<a href="chapter_file.html#item-N">`.

### Component Distribution Guide

Control component spacing based on content density:

| Content Density | Sidebar Frequency | Code Block Spacing | Max Consecutive Components |
|----------------|-------------------|-------------------|---------------------------|
| Low (concept/intro-heavy) | Every 6-8 paragraphs | Every 3-4 paragraphs | 1 sidebar + 1 code block |
| Medium (concept + code mix) | Every 4-6 paragraphs | Every 2-3 paragraphs | 2 consecutive components |
| High (code-dense) | Every 6-8 paragraphs | Every 1-2 paragraphs | No more than 3 consecutive code blocks |

---

## Advanced Components (v2.0)

The following components are provided by `style.css` v2.0 and `script.js` v2.0. All interactions are automatically mounted by JS; HTML only needs correct class names.

### Collapsible Areas

For optional content, deep discussions, or advanced topics — reduces page pressure:

```html
<div class="collapsible">
  <button class="collapsible__trigger">Expand: Advanced Configuration Options</button>
  <div class="collapsible__body">
    <p>Collapsed content...</p>
  </div>
</div>
```

- Click trigger toggles expand/collapse
- JS automatically handles `aria-expanded` and animation
- Default collapsed; add `.open` class to default expanded

### Code Tabs

Multi-language code comparison (Python/Rust/Go etc.):

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

- JS automatically handles click switching and keyboard navigation
- `data-index` matches tab to panel

### Full-Text Search

Search modal is automatically created by JS, no HTML needed. Trigger methods:
- `Ctrl+K` or `Cmd+K` keyboard shortcut
- JS automatically indexes all h2-h5 and code blocks on the page

### Page Outline Navigation

Outline is automatically generated by JS and pinned to the right side of the page (>1200px viewport), no HTML needed. Automatically tracks current reading position.

### Breadcrumbs

```html
<nav class="breadcrumbs">
  <a class="breadcrumbs__item" href="toc.html">Part One</a>
  <span class="breadcrumbs__sep">›</span>
  <a class="breadcrumbs__item" href="ch03.html">Chapter 3</a>
  <span class="breadcrumbs__sep">›</span>
  <span class="breadcrumbs__item">Architecture Design</span>
</nav>
```

- Insert above `.chapter-header`
- Last item is the current page, not clickable

### Diff View

Before/after code comparison:

```html
<div class="diff-block">
  <div class="diff-chunk-header">src/main.py</div>
  <pre><code><span class="diff-del">- print("Hello World")</span>
<span class="diff-add">+ print("Hello, Zenoh!")</span></code></pre>
</div>
```

- `.diff-del` = deleted line (red), `.diff-add` = added line (green)
- Wide screens automatically switch to side-by-side comparison

### Quizzes

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

- `data-correct="true"` marks the correct answer
- JS automatically validates, shows feedback, and reveals explanation
- Automatically disabled after answering

### File Trees

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

- Directories are clickable to expand/collapse
- `.active` highlights the current file

### Figure Numbering

```html
<div class="svg-diagram">
  <!-- SVG content -->
</div>
<p class="fig-caption" data-num>Architecture Layer Diagram</p>
```

- `data-num` attribute triggers CSS counter auto-numbering: displays as "Figure 3-2: Architecture Layer Diagram"
- Without `data-num`, no numbering is applied

### Cross-References

```html
<p>As shown in <a class="xref xref--fig" href="#fig-arch">Figure 3-2</a>,
see <a class="xref xref--listing" href="#lst-hello">Listing 4-1</a>,
for details see <a class="xref xref--chapter" href="ch05.html">Chapter 5</a>.</p>
```

### Definition Lists

```html
<div class="def-list">
  <p class="def-list__term">Session</p>
  <p class="def-list__def">Zenoh's core component, managing all network connections.</p>
  <p class="def-list__term">KeyExpr</p>
  <p class="def-list__def">Key expression, Zenoh's address space, supports wildcards.</p>
</div>
```

### API References

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

### Code Annotations

```html
<pre data-lang="Python"><code>with zenoh.open(zenoh.Config()) as session:  <span class="code-annotation__marker" data-note="1"></span>
    session.put("demo/key", "Hello")         <span class="code-annotation__marker" data-note="2"></span>
</code></pre>
<ol class="code-annotation__list">
  <li class="code-annotation__item">Using `with` ensures the session is properly closed</li>
  <li class="code-annotation__item">`put()` is a shortcut for one-time publishing</li>
</ol>
```

### Learning Objectives

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

- JS automatically persists check state to localStorage

### Video Embeds

```html
<div class="video-wrap video-wrap--16x9">
  <iframe src="https://www.youtube.com/embed/xxx" allowfullscreen></iframe>
</div>
<p class="fig-caption" data-num>Zenoh Architecture Overview</p>
```

### Math Formulas

```html
<p>Time complexity is <span class="math-inline">O(n \log n)</span>.</p>
<div class="math-block">
  $$E = mc^2$$
</div>
```

- JS automatically detects and loads KaTeX rendering

### Terminal Output

```html
<div class="terminal">
  <div class="terminal__header"></div>
  <div class="terminal__body">
    <span class="terminal__prompt">$ </span><span class="terminal__cmd">pip install eclipse-zenoh</span>
    <span class="terminal__output">Successfully installed eclipse-zenoh-1.9.0</span>
  </div>
</div>
```

### Interactive Exercises

```html
<div class="exercise">
  <p class="exercise__prompt">Try it: Modify the subscriber code above to only subscribe to temperature sensor data.</p>
  <button class="exercise__solution-btn">Show Answer</button>
  <div class="exercise__solution">
    <pre data-lang="Python"><code>session.declare_subscriber("sensor/**/temperature")</code></pre>
  </div>
</div>
```

### Reading Aids

```html
<p class="reading-time"></p>  <!-- JS automatically calculates and inserts -->
<span class="difficulty difficulty--beginner">Beginner</span>
<span class="difficulty difficulty--intermediate">Intermediate</span>
<span class="difficulty difficulty--advanced">Advanced</span>
```

### Badge System

```html
<span class="badge badge--stable">Stable</span>
<span class="badge badge--beta">Beta</span>
<span class="badge badge--deprecated">Deprecated</span>
<span class="badge badge--new">New</span>
<span class="badge badge--experimental">Experimental</span>
<span class="badge badge--version">v1.8+</span>
```

### Footnotes

```html
<p>Zenoh's wire overhead is only 4-6 bytes<a class="footnote-ref" href="#fn-1">[1]</a>.</p>
<!-- At bottom of chapter -->
<div class="footnotes">
  <div class="footnotes__item" id="fn-1">
    <a href="#fn-ref-1">↑</a> Wire overhead refers to the protocol header size, excluding payload.
  </div>
</div>
```

### Accessibility Tools

```html
<!-- At the very top of the page, start of body -->
<a class="skip-link" href="#main-content">Skip to content</a>
<!-- Main content -->
<main id="main-content" class="mn">...</main>
```

- `.sr-only` for text visible only to screen readers

### DrawIO/SVG Diagrams

DrawIO files are converted to SVG at build time and embedded:

```html
<div class="svg-diagram arch-diagram">
  <svg><!-- Theme-aware SVG --></svg>
</div>
<p class="fig-caption" data-num>System Architecture Diagram</p>
```

- Use `currentColor` and CSS variables inside SVG for theme switching
- Semantic class names: `.arch-diagram`, `.flow-diagram`, `.seq-diagram`
- JS automatically syncs SVG colors on theme switch

### Theme and Font Size

```html
<!-- Theme toggle (existing) -->
<button class="sb-toggle">☀️</button>

<!-- Font size adjustment (new) -->
<!-- JS can switch via html[data-font-scale] -->
<!-- Supported: "default" (16px), "large" (18px), "xl" (20px) -->
```

### Keyboard Shortcuts

Press `?` key to display the shortcuts panel. Built-in shortcuts:

| Shortcut | Function |
|----------|----------|
| `Ctrl+K` | Full-text search |
| `←` / `→` | Previous page / Next page |
| `?` | Keyboard shortcuts help |
| `Escape` | Close modal/search |

## CSS/JS Integration

`style.css` provides a high-end adaptive design system with a "quiet luxury" design language — conveying quality through restraint rather than decoration. When generating pages, prioritize reading experience and structural consistency, while adjusting component distribution based on the book's content hierarchy and audience.

### Design System Core Features

- **Adaptive hierarchy**: Heading visual weights automatically adjust based on the page's actual h2/h3/h4/h5 depth. Flat structures (2-level) get auto-enlarged h2; deep structures (4-level) get auto-micro-labeled h5
- **Dual theme + system preference**: Supports dark/light themes, detects `prefers-color-scheme`, persists setting to `localStorage`
- **Glass-morphism interaction layer**: Navigation bar, copy buttons, and back-to-top all use `backdrop-filter` frosted glass effect
- **Code blocks**: `data-lang` language label + auto copy button (shown on hover), auto-detected from hljs class when not set
- **Reading experience**: `requestAnimationFrame` progress bar, elastic easing scroll reveal, keyboard page-turn, active section highlighting

### Required Experience Constraints

- Body width, line height, font size, and paragraph spacing must be suitable for extended reading
- Code blocks, tables, sidebars, and glossary must be clearly readable on both desktop and mobile
- Top navigation, TOC, previous/next page, and keyboard page-turn must remain functional
- Pages must not overflow horizontally on mobile; interactive controls are hidden when printing
- Colors, contrast, and accent styles must serve the technical content, not overshadow the body text

## Navigation Structure

The interaction system is automatically provided by `script.js`:

- **Smart TOC**: Automatically detects page heading depth, builds a hierarchical dropdown TOC with indentation and active section highlighting
- **Reading progress bar** (`.prog`): Gradient progress indicator, smoothly rendered with `requestAnimationFrame`
- **Code copy**: Glass-morphism style copy button shown on hover, supports Clipboard API with fallback
- **Scroll reveal**: Headings, code blocks, cards, and other elements fade in and slide up when entering the viewport, powered by IntersectionObserver
- **Back to top** (`.btt`): Glass-morphism style, appears after scrolling past 500px
- **Keyboard page-turn**: Left/right arrow keys trigger previous/next page (automatically skipped inside input fields)
- **Theme toggle** (`.sb-toggle`): Dark/light switch, supports `prefers-color-scheme` detection + `localStorage` persistence
- **Auto language detection**: Code blocks without `data-lang` set automatically detect language label from hljs class

## CSS Class Naming Conventions

The following structural class names must be preserved — they are the contract between HTML templates and the CSS design system:

- `.chapter` / `.art` — Chapter main container
- `.chapter-header` / `.chapter-number` — Chapter heading area
- `.chapter-content` — Body content container
- `.sidebar` / `.sidebar.warning` — Sidebar boxes (multiple variant classes)
- `.CodeListingCaption` — Code listing title
- `.page-nav` / `.prev` / `.next` — Page-turn navigation
- `.top-nav` / `.toc-toggle` / `.toc-dropdown` — Top navigation bar
- `.table-wrapper` — Table scroll container
- `.glossary-term` — Glossary entry
- `.cover` / `.cover-content` — Cover page
- `.prog` — Reading progress bar
- `.btt` — Back to top button
- `.sb-link[data-depth]` — Sidebar hierarchical navigation links

Visual themes, layout details, cover presentation, component decoration, and animations are all adjustable. Prefer implementing styles in `style.css`; only add minimal local class names in HTML when a single page has specific semantic or asset needs, avoiding inline style proliferation.
