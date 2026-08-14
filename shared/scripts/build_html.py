#!/usr/bin/env python3
"""build_html.py — MD 源 → HTML 书籍渲染器。

把通用/GitHub 方言的 MD 章节渲染成"静奢"HTML 设计系统。MD 是信息主源，
HTML 是渲染目标。组件映射为"务实子集"（约定见 shared/md-authoring.md）。

用法:
    python scripts/build_html.py <md_dir> <out_dir>

<md_dir>/
    book.yml        元数据: title / subtitle / subtitle_cn / author / edition / lang
    README.md       (可选) MD 版目录; 缺失则从章节自动生成
    NN_*.md         章节, NN >= 02 (00/01 留给封面/目录)
    ```mermaid 块   构建期渲染为 diagrams/*.svg (需 npx mmdc; 缺失则降级为运行时渲染)
    src/diagrams/*.svg  手写 SVG 图表原样复制进两版产物 (可视化优先)

<out_dir>/          HTML 版
    00_cover.html 01_toc.html NN_*.html  style.css script.js  diagrams/*.{svg,png}
<out_dir>-md/       可移植 MD 版 (mermaid → svg 嵌入) + diagrams/*.{svg,png}

作者约定 (务实子集, 见 shared/md-authoring.md):
    > **[性能提示]** …            → <div class="sidebar performance-tip">…
    ```python caption="L7-1"      → <pre data-lang="Python">… + .CodeListingCaption
    ![alt](p "图：标题")          → .svg-diagram + .fig-caption[data-num]
    ![alt](p)                     → 普通 <img>
    ```mermaid …                  → diagrams/*.svg (或运行时 <pre class="mermaid">)
    <table>                       → .table-wrapper 包裹
"""
from __future__ import annotations

import hashlib
import html as _html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from markdown_it import MarkdownIt

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# callout 标签 → 现有 CSS 侧边栏变体 (book-assembly.md 词表)
TAG_VARIANTS = {
    "性能提示": "performance-tip", "performance": "performance-tip", "性能": "performance-tip",
    "警告": "gotcha-alert", "注意": "gotcha-alert", "gotcha": "gotcha-alert", "warning": "gotcha-alert",
    "学习目标": "learn", "learn": "learn",
    "检查清单": "check", "检查": "check", "checklist": "check", "check": "check",
    "要点回顾": "things-to-remember", "要点": "things-to-remember", "记住": "things-to-remember", "remember": "things-to-remember",
    "作者建议": "author-advice", "建议": "author-advice", "advice": "author-advice",
    "理论说明": "theory-note", "理论": "theory-note", "theory": "theory-note",
    "学究式注释": "pedantic-note", "注": "pedantic-note", "note": "pedantic-note", "pedantic": "pedantic-note",
    "快速入门": "quick-start", "quick": "quick-start",
    "错误速查": "error-cheatsheet", "速查": "error-cheatsheet", "cheatsheet": "error-cheatsheet",
}


def e(value: str) -> str:
    return _html.escape(str(value), quote=True)


def fail(message: str) -> "None":
    raise SystemExit(f"build_html: {message}")


# ---------------------------------------------------------------- meta

def load_meta(path: Path) -> dict:
    """解析扁平 key: value 的 book.yml（无第三方 YAML 依赖）。"""
    meta: dict[str, str] = {}
    if not path.exists():
        return meta
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta


# ---------------------------------------------------------------- markdown

def make_md() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True, "linkify": True}).enable("table")
    md.renderer.rules["fence"] = _rule_fence
    md.renderer.rules["image"] = _rule_image
    return md


def _rule_fence(tokens, idx, options, env):
    token = tokens[idx]
    info = (token.info or "").strip()
    head, _, rest = info.partition(" ")
    lang = head.strip()
    caption = ""
    match = re.search(r'caption\s*=\s*"([^"]*)"', rest) or re.search(r"caption\s*=\s*'([^']*)'", rest)
    if match:
        caption = match.group(1)
    if lang.lower() == "mermaid":
        return _render_mermaid(token.content, caption, env or {})
    lang_disp = lang.title() if lang else "Text"
    code = e(token.content.rstrip("\n"))
    cap = f'\n<p class="CodeListingCaption">{e(caption)}</p>' if caption else ""
    return f'<pre data-lang="{e(lang_disp)}"><code>{code}</code></pre>{cap}'


def _rule_image(tokens, idx, options, env):
    token = tokens[idx]
    src = token.attrs.get("src", "")
    title = token.attrs.get("title", "")
    alt = (token.content or "").strip()
    if title:
        return (
            f'<div class="svg-diagram"><img src="{e(src)}" alt="{e(alt)}"></div>'
            f'\n<p class="fig-caption" data-num>{e(title)}</p>'
        )
    return f'<img src="{e(src)}" alt="{e(alt)}">'


def _render_mermaid(code: str, caption: str, env: dict) -> str:
    diag_dir: Path | None = env.get("_diag_dir")
    rel = env.get("_diag_rel", "diagrams")
    runtime = f'<pre class="mermaid">{e(code)}</pre>'
    if diag_dir is None:
        return runtime
    digest = hashlib.md5(code.encode("utf-8")).hexdigest()[:10]
    svg = diag_dir / f"mmd-{digest}.svg"
    rendered = svg.exists()
    if not rendered and not env.get("_mmdc_dead"):
        rendered = _try_mmdc(code, svg)
        if not rendered:
            env["_mmdc_dead"] = True  # 渲染器不可用：后续图直接降级，不重复试
    if not rendered:
        env["_mmdc_failed_count"] = env.get("_mmdc_failed_count", 0) + 1
        return runtime  # 运行时降级: script.js 渲染
    cap = f'\n<p class="fig-caption" data-num>{e(caption)}</p>' if caption else ""
    return f'<div class="svg-diagram"><img src="{rel}/{svg.name}" alt="{e(caption or "diagram")}"></div>{cap}'


def _find_browser() -> str | None:
    """跨平台探测 Chromium 系浏览器可执行文件路径。

    优先级：环境变量 > PATH 上的 Chromium 系二进制 > 平台常见绝对路径 > None。
    返回 None 时，mmdc 回退到 puppeteer 自带的 Chromium（仍带 --no-sandbox）。
    不同机器浏览器装法各异：找不到时让用户设 PUPPETEER_EXECUTABLE_PATH。
    """
    # 1. 显式环境变量（最高优先，跨平台通用）
    for key in ("PUPPETEER_EXECUTABLE_PATH", "MMDC_CHROME_PATH"):
        env_path = os.environ.get(key)
        if env_path and Path(env_path).exists():
            return env_path
    # 2. PATH 上的 Chromium 系二进制（Chrome / Chromium / Edge / Brave，任何 OS）
    for name in (
        "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
        "chrome", "microsoft-edge", "microsoft-edge-stable", "brave-browser",
    ):
        found = shutil.which(name)
        if found:
            return found
    # 3. 平台相关的常见绝对路径
    candidates: list[str] = []
    if sys.platform == "darwin":
        candidates.append("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    elif sys.platform == "win32":
        for root in (r"C:\Program Files\Google\Chrome\Application",
                     r"C:\Program Files (x86)\Google\Chrome\Application",
                     r"C:\Program Files (x86)\Microsoft\Edge\Application"):
            candidates.append(root + r"\chrome.exe" if "Chrome" in root else root + r"\msedge.exe")
    else:  # Linux / WSL：也覆盖 WSL 里访问 Windows 侧 Chrome 的情况
        for drive in ("c", "d"):
            for prog in (f"/mnt/{drive}/Program Files/Google/Chrome/Application",
                         f"/mnt/{drive}/Program Files (x86)/Google/Chrome/Application"):
                candidates.append(f"{prog}/chrome.exe")
    for cand in candidates:
        if Path(cand).exists():
            return cand
    return None


def _try_mmdc(code: str, svg: Path) -> bool:
    """渲染一张 mermaid 为 SVG（按输出扩展名定格式）。跨平台探测浏览器 + --no-sandbox（WSL/容器/CI 必需）。"""
    has_mmdc = shutil.which("mmdc") is not None
    has_npx = shutil.which("npx") is not None
    if not has_mmdc and not has_npx:
        return False
    mmd = svg.with_suffix(".mmd")
    cfg = svg.with_suffix(".puppeteer.json")
    mmd.write_text(code, encoding="utf-8")
    chrome = _find_browser()
    puppeteer = {"args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]}
    if chrome:
        puppeteer["executablePath"] = chrome
    cfg.write_text(json.dumps(puppeteer), encoding="utf-8")
    cmd = ["mmdc"] if has_mmdc else ["npx", "-y", "@mermaid-js/mermaid-cli"]
    cmd += ["-i", str(mmd), "-o", str(svg), "-b", "transparent",
            "--puppeteerConfigFile", str(cfg)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
    except Exception:
        return False
    finally:
        for tmp in (mmd, cfg):
            if tmp.exists():
                tmp.unlink()
    return result.returncode == 0 and svg.exists()


# ---------------------------------------------------------------- transforms

def transform_callouts(body: str, md: MarkdownIt) -> str:
    """标签化引用块 > **[tag]** … → <div class="sidebar {variant}">。"""
    lines = body.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        match = re.match(r"^>\s+\*{0,2}\[(.*?)\]\*{0,2}\s*(.*)$", lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        tag, first = match.group(1), match.group(2)
        buf = [first]
        i += 1
        while i < n and re.match(r"^>\s?", lines[i]):
            buf.append(re.sub(r"^>\s?", "", lines[i]))
            i += 1
        variant = TAG_VARIANTS.get(tag.strip().lower(), "sidebar")
        inner = md.render("\n".join(b for b in buf if b is not None).strip())
        out.append(f'<div class="sidebar {variant}">{inner}</div>')
    return "\n".join(out)


def wrap_tables(rendered: str) -> str:
    rendered = re.sub(r"<table>", r'<div class="table-wrapper">\g<0>', rendered)
    return rendered.replace("</table>", "</table></div>")


def promote_fig_captions(rendered: str) -> str:
    """svg-diagram 后紧跟的『图：…』段落 → fig-caption[data-num]（触发 CSS 自动编号）。"""
    return re.sub(
        r'(<div class="svg-diagram">.*?</div>)\s*<p>(图[:：][^<]*)</p>',
        r'\1\n<p class="fig-caption" data-num>\2</p>',
        rendered, flags=re.DOTALL,
    )


# ---------------------------------------------------------------- scaffolds

SCAFFOLD = """<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - {book}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="top-nav">
  <span class="book-title">{book}</span>
  <div class="nav-links">
    <a href="01_toc.html">目录</a>
    <button class="toc-toggle">本节</button>
    <div class="toc-dropdown"></div>
  </div>
</nav>
<div class="prog"></div>
<main class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">{number}</span>
    <h1>{title}</h1>
  </div>
  <div class="chapter-content">
{content}
  </div>
  <div class="page-nav">
    {prev}
    {next}
  </div>
</main>
<button class="btt" aria-label="返回顶部">↑</button>
<script src="script.js"></script>
</body>
</html>
"""

COVER = """<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="cover">
  <div class="cover-content">
    <h1 class="cover-title">{title}</h1>
    {subtitle}
    {subtitle_cn}
    <p class="cover-author">{author}</p>
    <p class="cover-edition">{edition}</p>
    <a href="01_toc.html" class="cover-cta">开始阅读</a>
  </div>
</div>
</body>
</html>
"""

TOC = """<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>目录 - {book}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="top-nav">
  <span class="book-title">{book}</span>
  <div class="nav-links"><a href="00_cover.html">封面</a></div>
</nav>
<div class="prog"></div>
<main class="chapter">
  <div class="chapter-header"><h1>目录</h1></div>
  <div class="chapter-content">
{entries}
  </div>
</main>
<script src="script.js"></script>
</body>
</html>
"""


def render_cover(meta: dict, book: str, lang: str) -> str:
    subtitle = meta.get("subtitle", "")
    subtitle_cn = meta.get("subtitle_cn", "")
    return COVER.format(
        lang=e(lang),
        title=e(book),
        subtitle=f'<p class="cover-subtitle">{e(subtitle)}</p>' if subtitle else "",
        subtitle_cn=f'<p class="cover-subtitle-cn">{e(subtitle_cn)}</p>' if subtitle_cn else "",
        author=e(meta.get("author", "")),
        edition=e(meta.get("edition", "")),
    )


def render_toc(book: str, lang: str, chapters: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'    <li><a href="{e(stem)}.html">{e(title)}</a></li>' for stem, title in chapters
    )
    entries = f'<ul class="toc-list">\n{items}\n  </ul>'
    return TOC.format(lang=e(lang), book=e(book), entries=entries)


# ---------------------------------------------------------------- build

def build(md_dir: Path, out_dir: Path) -> dict:
    if not md_dir.is_dir():
        fail(f"源目录不存在: {md_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "diagrams").mkdir(exist_ok=True)

    meta = load_meta(md_dir / "book.yml")
    book = meta.get("title") or "未命名书籍"
    lang = meta.get("lang") or "zh-CN"

    chapters = sorted(
        p for p in md_dir.glob("*.md")
        if p.name != "README.md" and re.match(r"\d{2}", p.name)
    )
    if not chapters:
        fail(f"在 {md_dir} 未找到 NN_*.md 章节（00/01 留给封面/目录）")

    diag_dir = out_dir / "diagrams"
    # 手写 SVG 图表（可视化优先）：src/diagrams/*.svg 原样进入两版产物
    for svg in sorted((md_dir / "diagrams").glob("*.svg")):
        shutil.copy2(svg, diag_dir / svg.name)
    env = {"_diag_dir": diag_dir, "_diag_rel": "diagrams"}
    md = make_md()

    nav_chain = ["01_toc.html"] + [f"{p.stem}.html" for p in chapters]
    rendered: list[tuple[str, str]] = []

    for idx, path in enumerate(chapters):
        raw = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", raw, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        body = re.sub(r"^#\s+.+\n?", "", raw, count=1) if title_match else raw
        body = transform_callouts(body, md)
        content = promote_fig_captions(wrap_tables(md.render(body, env=env)))

        num = idx + 1
        prev_link = nav_chain[idx]
        next_link = nav_chain[idx + 2] if idx + 2 < len(nav_chain) else None
        prev_html = f'<a href="{prev_link}" class="prev">&larr; 上一页</a>'
        next_html = (
            f'<a href="{next_link}" class="next">下一页 &rarr;</a>'
            if next_link else '<span class="next"></span>'
        )

        page = SCAFFOLD.format(
            lang=e(lang), title=e(title), book=e(book),
            number=f"第 {num} 章", content=content, prev=prev_html, next=next_html,
        )
        (out_dir / f"{path.stem}.html").write_text(page, encoding="utf-8")
        rendered.append((path.stem, title))

    (out_dir / "00_cover.html").write_text(render_cover(meta, book, lang), encoding="utf-8")
    (out_dir / "01_toc.html").write_text(render_toc(book, lang, rendered), encoding="utf-8")

    for asset in ("style.css", "script.js"):
        src = ASSETS / asset
        if src.exists():
            shutil.copy2(src, out_dir / asset)
        else:
            print(f"警告: 缺少 {src}（HTML 将无样式/交互）", file=sys.stderr)

    build_md_edition(md_dir, out_dir, chapters, diag_dir, rendered, book)
    return env


def build_md_edition(md_dir: Path, out_dir: Path, chapters: list[Path],
                     diag_dir: Path, rendered: list[tuple[str, str]], book: str) -> None:
    """可移植 MD 版：mermaid 块替换为 SVG 嵌入（旧 PNG 回退）+ 复制 diagrams。"""
    md_out = Path(str(out_dir) + "-md")
    md_out.mkdir(parents=True, exist_ok=True)
    (md_out / "diagrams").mkdir(exist_ok=True)
    for pattern in ("*.svg", "*.png"):
        for f in diag_dir.glob(pattern):
            shutil.copy2(f, md_out / "diagrams")

    for path in chapters:
        text = path.read_text(encoding="utf-8")

        def repl(match: re.Match) -> str:
            digest = hashlib.md5(match.group(1).encode("utf-8")).hexdigest()[:10]
            for name in (f"mmd-{digest}.svg", f"mmd-{digest}.png"):  # svg 优先，旧 png 回退
                if (diag_dir / name).exists():
                    return f"![diagram](diagrams/{name})"
            return match.group(0)  # 未生成 → 保留 ```mermaid（GitHub 原生渲染）

        text = re.sub(r"```mermaid\n(.*?)```", repl, text, flags=re.DOTALL)
        (md_out / path.name).write_text(text, encoding="utf-8")

    readme = md_dir / "README.md"
    if readme.exists():
        shutil.copy2(readme, md_out / "README.md")
    else:
        items = "\n".join(f"- [{title}](./{stem}.md)" for stem, title in rendered)
        (md_out / "README.md").write_text(f"# {book}\n\n{items}\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print(__doc__)
        return 2
    md_dir = Path(argv[0]).resolve()
    out_dir = Path(argv[1]).resolve()
    env = build(md_dir, out_dir)
    print(f"成功: HTML → {out_dir} ; MD → {Path(str(out_dir) + '-md')}")
    n_failed = env.get("_mmdc_failed_count", 0)
    if n_failed:
        print(
            f"注意: mermaid 渲染器不可用，{n_failed} 张图降级为运行时渲染"
            f'（<pre class="mermaid">，由 script.js 渲染）。',
            file=sys.stderr,
        )
        print("      排查: 安装 Chrome/Edge，或设 PUPPETEER_EXECUTABLE_PATH 指向浏览器可执行文件，再试 npx -y @mermaid-js/mermaid-cli", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
