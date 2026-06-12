# Translation Rules

Language and formatting rules for translating technical books. Complements the project SPEC.md: this file provides universal rules; the project SPEC.md provides book-specific rules.

## Translation Principles

1. **Faithfulness and clarity first**: Do not pursue word-for-word correspondence; pursue the reader understanding the original meaning.
2. **Retain English for technical terms**: Python keywords, standard library names, protocol names, etc. must remain in English.
3. **Never translate code**: Code block content is copied verbatim, but **code comments must be translated to Chinese** (program output strings, exception text, and identifiers remain in English).
4. **Structural one-to-one correspondence**: Translate as many paragraphs as the original has; do not merge or split; preserve all markup.

## Terminology Rules

### Must Retain English

- Python keywords and built-in names: `class`, `def`, `return`, `True`, `None`, `import`, `__init__`, `self`
- Standard library modules: `os`, `sys`, `asyncio`, `dataclasses`
- Protocol names: `HTTP`, `TCP`, `WebSocket`
- Type annotations: `str`, `int`, `list[str]`, `Optional[int]`
- Command-line commands and options: `python -m`, `pip install`
- OS concepts: `PATH`, `stdin`, `stdout`

### First-Occurrence English Annotation

Use the common Chinese translation, with the English original in parentheses on first occurrence:

| English | Chinese |
|---------|---------|
| decorator | 装饰器 |
| generator | 生成器 |
| iterator | 迭代器 |
| comprehension | 推导式 |
| context manager | 上下文管理器 |
| metaclass | 元类 |
| descriptor | 描述符 |
| coroutine | 协程 |
| event loop | 事件循环 |
| type hint | 类型提示 |
| dunder method | 双下方法 |
| monkey patching | 猴子补丁 |
| duck typing | 鸭子类型 |
| dataclass | 数据类 |
| namespace | 命名空间 |
| scope | 作用域 |
| closure | 闭包 |
| iterable | 可迭代对象 |
| callable | 可调用对象 |

### Never Translate

- Variable names, function names, output strings, and exception text inside code blocks (comments must be translated to Chinese)
- English inside inline code `` `word` ``
- File names and paths
- Command-line commands
- Personal names, company names, product names
- Book titles (annotate with Chinese translation on first occurrence)
- URLs and email addresses

## Code Block Handling

1. Copy code from the source file verbatim (variable names, function names, output strings remain in English).
2. **Translate code comments to Chinese** (`# This is a comment` becomes `# 这是注释`), but program output and exception text remain in English.
3. Replace `<em>` and `<b>` inside `<pre>` with `<strong>`.
4. No nested `<code>` (write text directly inside `<pre>`).
5. Code indentation: 4 spaces.
6. Do not add decorative elements inside `<pre><code>`; if code language labels or copy buttons are needed, use separate elements placed outside the code block, and keep them consistent across the book.
7. Code listing captions use `<p class="CodeListingCaption">` below the code block.
8. **Code listing numbers must be sequential** — if the original book has gaps or insertions, renumber them consecutively.

## Formatting Standards

### Punctuation

1. No Chinese quotation marks `""`; use English quotation marks or book-title marks instead.
2. Colons in code listing captions must use the Chinese full-width colon `：`.
3. Colons in table titles and figure titles must also use the full-width colon.
4. Use compact formatting when referencing code listings; do not add extra spaces.

### Spacing

1. Add a space between English and Chinese (`Python 是` not `Python是`).
2. Add a space between numbers and Chinese (`3 个` not `3个`).
3. No extra spaces inside English parentheses with all-English content (`(Python)`); add spaces when content is mixed Chinese-English.
4. Add spaces around N in `第 N 章` (`第 3 章` not `第3章`).

### Headings

1. Use `——` (Chinese double em dash) for dashes.
2. The table-of-contents title, page `<title>`, and `<h1>` must all have identical content.
3. Sidebar titles use the `.sidebar-title` paragraph class and do not participate in the page heading outline.

### Terminology Formatting

1. `I/O` must use the uppercase-with-slash form; do not use `IO` in running text (type annotations like `IO[str]` are exceptions).
2. Technical terms must have English annotation on first occurrence; use the consistent Chinese translation thereafter.

## Common Pitfalls

### Structural Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Paragraph merging | Combining 2-3 original paragraphs into 1 | Strict one-to-one correspondence |
| Anchor loss | Original `id="item-N"` missing after translation | Verify each anchor |
| List collapse | Ordered list becomes plain text paragraph | Preserve `<ol>`/`<ul>` structure |
| Nesting error | `<p>` inside `<li>` promoted outside the list | Maintain original nesting |
| Code block markup loss | `<pre><code>` becomes plain text | Mark all code blocks |

**Example — Paragraph merging**:

❌ Merged:
```html
<p>生成器是一种特殊的迭代器。它通过 yield 语句暂停执行，
在需要时恢复。这使得我们可以处理无限序列。</p>
```

✅ Preserve original structure:
```html
<p>生成器是一种特殊的迭代器。</p>
<p>它通过 yield 语句暂停执行，在需要时恢复。</p>
<p>这使得我们可以处理无限序列。</p>
```

### Terminology Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Inconsistent translation | Same term translated differently in different places | Unify across the entire text |
| Annotation omission | First occurrence lacks English annotation | Always annotate on first occurrence |
| Over-translation | stack translated as "知识栈" instead of "堆栈" | Use standard technical translations |
| Invented terms | Self-created Chinese terminology | Use community-established translations |

**Example — Inconsistent translation**:

❌ Same term, two translations:
> 第 3 章介绍了**装饰器**（decorator）的用法……第 7 章深入探讨了**修饰器**的高级技巧。

✅ Consistent throughout:
> 第 3 章介绍了**装饰器**（decorator）的用法……第 7 章深入探讨了**装饰器**的高级技巧。

**Example — Annotation omission**:

❌ First occurrence without annotation:
> 上下文管理器可以自动管理资源的获取和释放。

✅ First occurrence with annotation:
> 上下文管理器（context manager）可以自动管理资源的获取和释放。

### Style Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Translationese | "它是一个...的东西" | Rewrite in natural Chinese |
| Passive voice overuse | "被用来做" | Use active voice: "用于做" |
| Stacked modifiers | "一个用于处理数据的可以被重用的对象" | Split into shorter sentences or front-load the definition |
| English sentence structure | Preserving English relative clause structure | Adjust to Chinese word order |

**Example — Translationese**:

❌ Translationese:
> 它是一个被用来将函数作为参数传递给另一个函数的机制。

✅ Natural Chinese:
> 高阶函数可以接收函数作为参数，也可以返回函数。

**Example — Passive voice overuse**:

❌ Passive overuse:
> 这个方法被用来创建对象。参数被传递给构造函数。返回值被存储在变量中。

✅ Active voice:
> 这个方法用于创建对象。构造函数接收参数，返回值存入变量。

**Example — Stacked modifiers**:

❌ Stacked modifiers:
> 这是一个用于在多个协程之间进行协作式调度的基于事件循环的异步执行机制。

✅ Split:
> 异步执行机制基于事件循环，在多个协程之间进行协作式调度。

### Formatting Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Inline code loss | Original `` `word` `` loses backticks after translation | Preserve inline code markup |
| Bold loss | Original `<strong>` becomes plain text after translation | Preserve all emphasis markup |
| Link text not translated | English text inside `<a>` tags left untranslated | Keep href unchanged, translate the text |
| Image alt not translated | `alt="Description"` left in English | Translate to Chinese |

**Example — Inline code loss**:

❌ Backticks lost:
> 使用 class 关键字定义类。

✅ Markup preserved:
> 使用 `class` 关键字定义类。

**Example — Link text**:

❌ Link text not translated:
```html
<a href="ch03.html#item-42">Understanding Closures</a>
```

✅ URL unchanged, text translated:
```html
<a href="ch03.html#item-42">理解闭包</a>
```

### Translationese Pitfalls (High-Frequency Review Feedback)

For the full prohibition list, see `../shared/translationese-patterns.md`. Below are the most frequent pitfalls with examples:

**Example — Literal translation of connectors**:

❌ Literal:
> 这就是为什么 Python 的生成器如此强大——它允许你在不需要将所有数据加载到内存的情况下处理无限序列。

✅ Rewritten:
> Python 生成器的强大之处在于：它能按需产出数据，处理无限序列时不会耗尽内存。

**Example — Redundant filler phrases**:

❌ Redundant:
> 你会发现，当我们调用 `len()` 时，Python 实际上调用的是 `__len__` 方法。

✅ Direct:
> 调用 `len()` 时，Python 实际调用 `__len__` 方法。

## Red-Line Checklist

Violating any of these hard constraints constitutes a translation failure.

### Text Processing Red Lines

- [ ] Every paragraph is translated with no omissions (red line: paragraph-by-paragraph translation)
- [ ] No paragraph merging: original has N paragraphs, translation has N paragraphs
- [ ] No paragraph splitting: one original paragraph is not split into multiple (unless the original structure implies it, e.g. list items)
- [ ] Code blocks are preserved verbatim: variable names, function names, output strings, and exception text are copied character-for-character. **Code comments are translated to Chinese** (`# This is a comment` becomes `# 这是注释`), but program output and Python error text remain in English
- [ ] Emphasis structure from the original is preserved: bold, italic, and inline code markup must correspond in the translation

### Terminology Red Lines

- [ ] First occurrence of a technical term includes English annotation in parentheses (e.g. "装饰器（decorator）"); subsequent uses can be Chinese only
- [ ] Consistent terminology: the same English term must use the same Chinese translation throughout; no "迭代器" in one place and "迭代对象" in another
- [ ] No invented terms: use established community translations (e.g. class is "类", not "类别")

### Format Red Lines

- [ ] All HTML tags and attributes from the original are preserved
- [ ] Anchor IDs are not modified or deleted (`id="..."`)
- [ ] Link addresses are not modified (`href` values unchanged), but link text is translated
- [ ] Image alt attributes are translated to Chinese

### Quality Checks (Per-Chapter Self-Check)

- [ ] Spaces between Chinese and English text
- [ ] `第 N 章` format is consistent
- [ ] Code listing captions use full-width colon
- [ ] Table-of-contents title / `<title>` / `<h1>` are identical
- [ ] Sidebar titles do not participate in page outline
- [ ] Code listing numbers are sequential with no gaps
- [ ] Cross-reference chapter numbers are correct
- [ ] No translationese (see `../shared/translationese-patterns.md`)
- [ ] Code comments have been translated to Chinese
- [ ] I/O written consistently

## Translationese Reference

For the complete list of prohibited translationese patterns and their corrections, see `../shared/translationese-patterns.md`.
