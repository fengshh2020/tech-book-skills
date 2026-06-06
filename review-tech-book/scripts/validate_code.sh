#!/usr/bin/env bash
# 技术书籍审阅自动化验证脚本
# 用法: ./validate_code.sh [--run-code] [output_dir] [python_version]
# 默认: output/ 3.13
# --run-code: 提取并尝试运行代码块（阶段 2 用）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_CODE=false
if [[ "${1:-}" == "--run-code" ]]; then
  RUN_CODE=true
  shift
fi

DIR="${1:-output/}"
if [[ "$DIR" != */ ]]; then
  DIR="${DIR}/"
fi
PYVER="${2:-3.13}"
PASS=0
FAIL=0
SKIP=0
HARD_ERRORS=0

echo "=== 代码验证脚本 ==="
echo "扫描目录: $DIR"
echo "Python 版本基线: $PYVER"
if $RUN_CODE; then
  echo "代码运行验证: 已启用"
fi
echo ""

if [ ! -d "$DIR" ]; then
  echo "❌ 输出目录不存在: $DIR"
  exit 1
fi

if ! compgen -G "${DIR}*.html" >/dev/null; then
  echo "❌ 输出目录中没有 HTML 文件: $DIR"
  exit 1
fi

# 安全 grep 计数：避免 pipefail 下 grep 无匹配导致脚本退出
safe_count() {
  grep -rn "$1" "${2:-$DIR}"*.html 2>/dev/null | wc -l | tr -d '[:space:]' || echo 0
}

# 提取代码块并输出（供 --run-code 使用）
extract_blocks() {
  local file="$1"

  python3 -c "
import re
with open('$file', 'r') as f:
    content = f.read()
blocks = re.findall(r'<pre><code[^>]*>(.*?)</code></pre>', content, re.DOTALL)
for i, b in enumerate(blocks):
    b = re.sub(r'<[^>]+>', '', b)
    b = b.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '\"')
    b = b.strip()
    if not b:
        continue
    if not any(kw in b for kw in ['def ', 'class ', 'import ', 'from ', 'print(', 'return ', '=', 'for ', 'while ']):
        continue
    print(f'--- Block {i+1} ---')
    print(b)
    print('--- END ---')
" 2>/dev/null || true
}

# 提取并运行代码块
run_code_blocks() {
  local file="$1"
  local basename=$(basename "$file")
  local block_num=0
  local code=""

  while IFS= read -r line; do
    if [[ "$line" == "--- Block "* ]]; then
      block_num=$((block_num + 1))
      code=""
    elif [[ "$line" == "--- END ---" ]]; then
      if [[ -n "$code" ]]; then
        echo -n "  Block $block_num: "
        if echo "$code" | python3 - 2>/dev/null; then
          echo "✅ PASS"
          PASS=$((PASS + 1))
        else
          echo "❌ FAIL"
          FAIL=$((FAIL + 1))
        fi
      else
        SKIP=$((SKIP + 1))
      fi
    else
      code="${code}${line}"$'\n'
    fi
  done < <(extract_blocks "$file")
}

# 检查术语一致性
check_terminology() {
  echo "--- 术语一致性检查 ---"
  local TERM_PAIRS=(
    "装饰器|修饰器"
    "生成器|产生器"
    "上下文管理器|情境管理器"
    "推导式|解析式"
  )

  for PAIR in "${TERM_PAIRS[@]}"; do
    local CORRECT="${PAIR%%|*}"
    local WRONG="${PAIR##*|}"
    local COUNT
    COUNT=$(safe_count "$WRONG") || COUNT=0
    if [ "$COUNT" -gt 0 ] 2>/dev/null; then
      echo "⚠ '$WRONG' 出现 ${COUNT} 次（应为 '$CORRECT'）:"
      grep -rn "$WRONG" "$DIR"*.html 2>/dev/null | head -5 || true
    fi
  done

  echo "✅ 术语一致性检查完成"
}

# 检查代码块格式
check_code_format() {
  echo ""
  echo "--- 代码块格式检查 ---"

  FOUND=$(grep -rn '<em>\|<b>' "$DIR"*.html 2>/dev/null | grep -B1 '<pre>' || true)
  if [ -n "$FOUND" ]; then
    echo "❌ <pre> 中发现 <em>/<b> 标签"
    HARD_ERRORS=$((HARD_ERRORS + 1))
  else
    echo "✅ <pre> 中无 <em>/<b> 标签"
  fi

  FOUND=$(python3 -c "
import re, glob
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    # Remove <pre>...</pre> blocks to avoid false positives from code examples
    stripped = re.sub(r'<pre>.*?</pre>', '', content, flags=re.DOTALL)
    for m in re.finditer(r'<code[^>]*>([^<]*(?:<(?!/code>)[^>]*>[^<]*)*)</code>', stripped):
        if '<code' in m.group(1):
            line = stripped[:m.start()].count('\n') + 1
            print(f'{f}:{line}: {m.group(0)[:60]}')
" 2>/dev/null || true)
  if [ -n "$FOUND" ]; then
    echo "❌ 发现嵌套 <code> 标签"
    HARD_ERRORS=$((HARD_ERRORS + 1))
  else
    echo "✅ 无嵌套 <code> 标签"
  fi

  FOUND=$(python3 -c "
import glob
for f in sorted(glob.glob('${DIR}*.html')):
    for i, line in enumerate(open(f), 1):
        if any(c in line for c in ['“', '”', '‘', '’']):
            print(f'{f}:{i}')
" 2>/dev/null || true)
  if [ -n "$FOUND" ]; then
    echo "⚠ 发现中文引号（请确认是否为内容引用）"
  else
    echo "✅ 无中文引号"
  fi
}

# 检查内部链接
check_links() {
  echo ""
  echo "--- 内部链接检查 ---"
  local BROKEN=0
  local TOTAL=0
  for f in "$DIR"*.html; do
    [ -f "$f" ] || continue
    local LINKS
    LINKS=$(grep -oP 'href="([^"#]+)(#[^"]*)?"' "$f" 2>/dev/null | grep -vP 'http:|https:|mailto:' || true)
    for LINK in $LINKS; do
      local FILE_PART
      FILE_PART=$(echo "$LINK" | grep -oP 'href="\K[^"#]+' || true)
      TOTAL=$((TOTAL + 1))
      if [ -n "$FILE_PART" ] && [ ! -f "$DIR$FILE_PART" ]; then
        echo "❌ $(basename "$f") → $FILE_PART (文件不存在)"
        BROKEN=$((BROKEN + 1))
      fi
    done
  done
  echo "  检查链接: $TOTAL | 断链: $BROKEN"
  if [ "$BROKEN" -gt 0 ]; then
    HARD_ERRORS=$((HARD_ERRORS + 1))
  fi
}

# 执行格式检查（始终运行）
check_code_format
echo ""
check_terminology
echo ""
check_links

# 翻译质量扫描（始终运行）
echo ""
echo "--- 翻译质量扫描 ---"

# 翻译腔高频模式（从 shared/translationese-patterns.md 读取，与 translate-book/validate_format.sh 同源）
TRANSLATIONESE=$(python3 -c "
import re, glob, os
count = 0
# 从共享文件读取模式；若文件不存在则使用硬编码后备列表
shared_path = os.path.join('${SCRIPT_DIR}', '..', '..', 'shared', 'translationese-patterns.md')
patterns = []
if os.path.exists(shared_path):
    for line in open(shared_path):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\x60([^\x60]+)\x60\s*\|\s*([^|]+)', line)
        if m:
            patterns.append(m.group(2).strip())
if not patterns:
    patterns = ['这就是为什么', '这也是为什么', '你会发现', '可以看到', '正如你', '如你所见', '值得注意的是', '让我们', '接下来我们将', '简单来说', '在这个例子中', '需要注意的是', '事实上', '换句话说']
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    text = re.sub(r'<pre[^>]*>.*?</pre>', '', content, flags=re.DOTALL)
    for p in patterns:
        count += len(re.findall(p, text))
print(count)
" 2>/dev/null || echo 0)
if [ "$TRANSLATIONESE" -gt 0 ]; then
  echo "⚠ 发现 $TRANSLATIONESE 处可能的翻译腔"
else
  echo "✅ 翻译腔扫描通过"
fi

# 代码清单编号连续性
NUMBERING=$(python3 -c "
import re, glob
issues = []
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    captions = re.findall(r'CodeListingCaption[^>]*>.*?(\d+)-(\d+)', content)
    if captions:
        chapter = captions[0][0]
        nums = [int(c[1]) for c in captions]
        for i in range(len(nums)-1):
            if nums[i+1] != nums[i]+1 and nums[i+1] != nums[i]:
                issues.append(f'{f}: {chapter}-{nums[i]} -> {chapter}-{nums[i+1]}')
if issues:
    for iss in issues[:5]:
        print(f'⚠ {iss}')
else:
    print('OK')
" 2>/dev/null || echo "OK")
if [ "$NUMBERING" != "OK" ]; then
  echo "$NUMBERING"
  echo "⚠ 代码清单编号可能不连续"
else
  echo "✅ 代码清单编号连续性检查通过"
fi

# I/O 术语一致性
IO_ISSUES=$(python3 -c "
import re, glob
count = 0
for f in sorted(glob.glob('${DIR}*.html')):
    content = open(f).read()
    text = re.sub(r'<pre[^>]*>.*?</pre>', '', content, flags=re.DOTALL)
    text = re.sub(r'<code[^>]*>.*?</code>', '', text, flags=re.DOTALL)
    # 独立 IO（非 IO[str] 类型注解）
    for m in re.finditer(r'(?<![.\w/])IO(?![\[A-Z])', text):
        count += 1
print(count)
" 2>/dev/null || echo 0)
if [ "$IO_ISSUES" -gt 0 ]; then
  echo "⚠ 正文中发现 $IO_ISSUES 处独立 'IO'（可能应为 'I/O'）"
else
  echo "✅ I/O 术语一致性检查通过"
fi

# 代码运行验证（--run-code 时执行）
if $RUN_CODE; then
  echo ""
  echo "--- 代码运行验证 ---"
  for f in "$DIR"*.html; do
    [ -f "$f" ] || continue
    echo "📄 $(basename "$f")"
    run_code_blocks "$f"
  done
  echo ""
  echo "  通过: $PASS | 失败: $FAIL | 跳过: $SKIP"
fi

echo ""
echo "=== 验证完成 ==="
if [ "$HARD_ERRORS" -gt 0 ] || [ "$FAIL" -gt 0 ]; then
  echo "❌ 硬错误: $HARD_ERRORS | 代码运行失败: $FAIL"
  exit 1
fi

echo "✅ 硬性检查通过"
