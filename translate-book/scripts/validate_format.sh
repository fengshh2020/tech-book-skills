#!/usr/bin/env bash
# 翻译产出格式验证脚本
# 用法: ./validate_format.sh [output_dir]
# 默认 output_dir=output/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIR="${1:-output/}"
if [[ "$DIR" != */ ]]; then
  DIR="${DIR}/"
fi
ERRORS=0

echo "=== 翻译格式验证 ==="
echo "扫描目录: $DIR"
echo ""

if [ ! -d "$DIR" ]; then
  echo "❌ 输出目录不存在: $DIR"
  exit 1
fi

if ! compgen -G "${DIR}*.html" >/dev/null; then
  echo "❌ 输出目录中没有 HTML 文件: $DIR"
  exit 1
fi

# 1. <pre> 中不应有 <em> 或 <b>
echo "--- 检查: <pre> 中的 <em>/<b> 标签 ---"
FOUND=$(python3 -c "
import re, glob, sys
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    for m in re.finditer(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL):
        block = m.group(1)
        if '<em>' in block or '<b>' in block:
            line = content[:m.start()].count('\n') + 1
            print(f'{f}:{line}: <pre> 中含 <em>/<b>')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "❌ 发现 <pre> 中的 <em>/<b> 标签:"
  echo "$FOUND"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ 通过"
fi

# 2. 禁止中文引号（U+201C U+201D U+2018 U+2019）
echo ""
echo "--- 检查: 中文引号 ---"
FOUND=$(python3 -c "
import glob
for f in sorted(glob.glob('${DIR}*.html')):
    for i, line in enumerate(open(f), 1):
        if any(c in line for c in ['\u201c', '\u201d', '\u2018', '\u2019']):
            print(f'{f}:{i}')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  COUNT=$(echo "$FOUND" | wc -l)
  echo "⚠ 发现中文引号 ($COUNT 处，请人工确认是否为正文引用):"
  echo "$FOUND" | head -10
else
  echo "✅ 通过"
fi

# 3. 禁止嵌套 <code>
echo ""
echo "--- 检查: 嵌套 <code> 标签 ---"
FOUND=$(python3 -c "
import re, glob
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    # 只检查 code 块内部是否出现真正的 <code 开始标签；
    # 不把 Python 表达式里的 <、<=、泛型文本等误判为 HTML 标签。
    for m in re.finditer(r'<code[^>]*>(.*?)</code>', content, re.DOTALL):
        inner = m.group(1)
        if '<code' in inner:
            line = content[:m.start()].count('\n') + 1
            print(f'{f}:{line}: {m.group(0)[:60]}')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "❌ 发现嵌套 <code>:"
  echo "$FOUND"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ 通过"
fi

# 4. code-header/code-dot 装饰元素提示
echo ""
echo "--- 检查: code-header/code-dot 装饰元素 ---"
FOUND=$(grep -rn 'class="code-header"\|class="code-dot"' "$DIR"*.html 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "⚠ 发现 code-header/code-dot 装饰元素，请确认其位于 <pre><code> 外且不影响代码复制:"
  echo "$FOUND"
else
  echo "✅ 通过"
fi

# 5. 中英文间应有空格（检查所有文件）
echo ""
echo "--- 检查: 中英文间距 ---"
if compgen -G "${DIR}*.html" >/dev/null; then
  # 检测中文紧跟英文（无空格）的常见模式
  FOUND=$(grep -rn '[一-龥][A-Za-z]\|[A-Za-z][一-龥]' "$DIR"*.html 2>/dev/null | head -20 || true)
  COUNT=$(echo "$FOUND" | grep -c '.' || true)
  if [ "$COUNT" -gt 10 ]; then
    echo "⚠ 可能存在中英文间距问题（>10 处），请人工复查:"
    echo "$FOUND" | head -10
  else
    echo "✅ 通过（少量间距问题可忽略）"
  fi
fi

# 6. 导航链接完整性
echo ""
echo "--- 检查: prev/next 导航链接 ---"
BROKEN=0
for f in "$DIR"*.html; do
  [ -f "$f" ] || continue
  PREV=$(grep -o 'class="prev"[^>]*href="[^"]*"' "$f" 2>/dev/null | grep -o 'href="[^"]*"' | sed 's/href="//;s/"//' || true)
  NEXT=$(grep -o 'class="next"[^>]*href="[^"]*"' "$f" 2>/dev/null | grep -o 'href="[^"]*"' | sed 's/href="//;s/"//' || true)
  for LINK in $PREV $NEXT; do
    TARGET="$DIR$LINK"
    if [ -n "$LINK" ] && [ ! -f "$TARGET" ]; then
      echo "❌ $(basename "$f"): 链接 $LINK 指向不存在的文件"
      ((BROKEN++))
    fi
  done
done
if [ "$BROKEN" -eq 0 ]; then
  echo "✅ 通过"
else
  ERRORS=$((ERRORS + 1))
fi

# 7. 锚点 ID 保留检查
echo ""
echo "--- 检查: item-N 锚点存在性 ---"
ITEM_COUNT=$(grep -roh 'id="item-[0-9]*"' "$DIR"*.html 2>/dev/null | sort -u | wc -l || true)
REF_COUNT=$(grep -roh '#item-[0-9]*' "$DIR"*.html 2>/dev/null | sed 's/#//' | sort -u | wc -l || true)
echo "  定义锚点: $ITEM_COUNT 个 | 引用锚点: $REF_COUNT 个"
if [ "$ITEM_COUNT" -eq 0 ]; then
  echo "⚠ 无 item-N 锚点（可能不适用本书结构）"
else
  echo "✅ 锚点存在"
fi

# 8. 图片路径有效性检查
echo ""
echo "--- 检查: 图片路径有效性 ---"
BROKEN_IMGS=0
FOUND=$(python3 -c "
import re, glob, os
dir_path = '${DIR}'
for f in sorted(glob.glob(dir_path + '*.html')):
    content = open(f).read()
    for m in re.finditer(r'<img[^>]+src=[\"\\x27]([^\"\\x27]+)[\"\\x27]', content):
        src = m.group(1)
        if not os.path.exists(os.path.join(dir_path, src)):
            print(f'{os.path.basename(f)}: {src}')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  COUNT=$(echo "$FOUND" | wc -l)
  echo "❌ 发现 $COUNT 个无效图片路径:"
  echo "$FOUND"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ 通过"
fi

# 9. 标题一致性检查（<title> vs <h1>）
echo ""
echo "--- 检查: title 与 h1 一致性 ---"
FOUND=$(python3 -c "
import re, glob
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    title_m = re.search(r'<title>(.*?)</title>', content)
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    if title_m and h1_m:
        title_text = re.sub(r'<[^>]+>', '', title_m.group(1)).strip()
        h1_text = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip()
        # 允许 title 比 h1 多前缀如\"第N章 \"
        if title_text not in h1_text and h1_text not in title_text:
            print(f'{f}: title=\"{title_text}\" vs h1=\"{h1_text}\"')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "⚠ title 与 h1 不一致（请人工确认）:"
  echo "$FOUND"
else
  echo "✅ 通过"
fi

# 10. 跨章引用章节编号检查
echo ""
echo "--- 检查: 跨章引用锚点有效性 ---"
FOUND=$(python3 -c "
import re, glob, os
dir_path = '${DIR}'
# 收集所有锚点
all_anchors = set()
for f in glob.glob(dir_path + '*.html'):
    content = open(f).read()
    for m in re.finditer(r'id=\"([^\"]+)\"', content):
        all_anchors.add((os.path.basename(f), m.group(1)))

# 检查所有内部链接
for f in sorted(glob.glob(dir_path + '*.html')):
    content = open(f).read()
    for m in re.finditer(r'href=\"([^\"#]+)#([^\"]+)\"', content):
        target_file = m.group(1)
        target_anchor = m.group(2)
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target_file) or target_file.startswith('//'):
            continue
        target_path = os.path.join(dir_path, target_file)
        if not os.path.exists(target_path):
            print(f'{os.path.basename(f)}: 链接 {m.group(0)[:60]} 目标文件不存在')
            continue
        target_content = open(target_path).read()
        if f'id=\"{target_anchor}\"' not in target_content:
            print(f'{os.path.basename(f)}: 锚点 #{target_anchor} 在 {target_file} 中不存在')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  COUNT=$(echo "$FOUND" | wc -l)
  echo "❌ 发现 $COUNT 个无效跨章引用:"
  echo "$FOUND" | head -10
  ERRORS=$((ERRORS + 1))
else
  echo "✅ 通过"
fi

# 11. 正文中非代码区独立 IO 用法检查（应为 I/O）
echo ""
echo "--- 检查: 正文中 IO/I/O 术语一致性 ---"
FOUND=$(python3 -c "
import re, glob
results = []
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    text = re.sub(r'<pre[^>]*>.*?</pre>', '', content, flags=re.DOTALL)
    text = re.sub(r'<code[^>]*>.*?</code>', '', text, flags=re.DOTALL)
    for m in re.finditer(r'(?<![.\w/])IO(?!\[|S|T|R|U|E|L|N)(?!\w)', text):
        line = text[:m.start()].count('\n') + 1
        results.append(f'{f}:{line}: 正文独立 IO')
if results:
    print('\n'.join(results[:10]))
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "⚠ 正文中有独立 IO（建议检查是否应为 I/O）:"
  echo "$FOUND" | head -5
else
  echo "✅ 通过"
fi

# 12. 翻译腔高频模式检查（从 shared/translationese-patterns.md 读取，与 validate_code.sh 同源）
echo ""
echo "--- 检查: 翻译腔高频模式 ---"
FOUND=$(python3 -c "
import re, glob, os
# 从共享文件读取模式；若文件不存在则使用硬编码后备列表
shared_path = os.path.join('${SCRIPT_DIR}', '..', '..', 'shared', 'translationese-patterns.md')
patterns = []
if os.path.exists(shared_path):
    for line in open(shared_path):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\x60([^\x60]+)\x60\s*\|\s*([^|]+)', line)
        if m:
            patterns.append((m.group(2).strip(), m.group(3).strip()))
if not patterns:
    patterns = [
        (r'这就是为什么', '直译连接词'),
        (r'这也是为什么', '直译连接词'),
        (r'你会发现', '冗余提示语'),
        (r'可以看到', '冗余提示语'),
        (r'正如你', '读者称谓直译'),
        (r'如你所见', '读者称谓直译'),
        (r'值得注意的是', '冗余提示语'),
        (r'让我们', '直译祈使句'),
        (r'接下来我们将', '冗余过渡语'),
        (r'简单来说', '冗余填充语'),
        (r'在这个例子中', '直译过渡语'),
        (r'需要注意的是', '冗余提示语'),
        (r'事实上', '直译副词'),
        (r'换句话说', '直译过渡语'),
    ]
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    # 跳过 <pre> 区域
    text = re.sub(r'<pre[^>]*>.*?</pre>', '', content, flags=re.DOTALL)
    for pattern, label in patterns:
        for m in re.finditer(pattern, text):
            line = text[:m.start()].count('\n') + 1
            print(f'{f}:{line}: [{label}] {pattern}')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  COUNT=$(echo "$FOUND" | wc -l)
  echo "⚠ 发现 $COUNT 处可能的翻译腔（请人工确认是否需要修改）:"
  echo "$FOUND" | head -10
else
  echo "✅ 通过"
fi

# 13. 检查 epub-metadata.json 中 spine 章节是否都有对应输出
echo ""
echo "--- 检查: spine 章节覆盖完整性 ---"
SCRIPT_DIR2="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
META=""
# 查找最近的 translate run 目录中的 epub-metadata.json
for RUN_DIR in .book-doc/runs/*-translate-*/; do
  CANDIDATE="${RUN_DIR}epub-metadata.json"
  if [ -f "$CANDIDATE" ]; then
    META="$CANDIDATE"
  fi
done
if [ -z "$META" ] || [ ! -f "$META" ]; then
  echo "⚠ 未找到 epub-metadata.json，跳过 spine 覆盖检查"
else
  FOUND=$(python3 -c "
import json, glob, os, sys
meta = json.load(open('${META}'))
spine = meta.get('spine', [])
if not spine:
    print('SKIP: spine 为空')
    sys.exit(0)
missing = []
for item in spine:
    target = item.get('target', '')
    if not target:
        continue
    path = os.path.join('${DIR}', target)
    if not os.path.exists(path):
        missing.append(target)
if missing:
    print('MISSING:' + ','.join(missing))
else:
    print(f'OK: {len(spine)} spine items all have output files')
" 2>/dev/null || echo "WARN: spine 覆盖检查执行失败")
  if echo "$FOUND" | grep -q "^MISSING:"; then
    MISSING_LIST=$(echo "$FOUND" | sed 's/^MISSING://')
    echo "❌ spine 中有章节缺少对应输出: $MISSING_LIST"
    ERRORS=$((ERRORS + 1))
  else
    echo "$FOUND"
  fi
fi

# 总结
echo ""
echo "=== 验证完成 ==="
if [ "$ERRORS" -eq 0 ]; then
  echo "✅ 所有硬性检查通过"
else
  echo "❌ $ERRORS 项硬性检查未通过"
  exit 1
fi
