#!/usr/bin/env bash
# Validate generated codebase-book HTML output.
# Usage: validate_output.sh [output_dir]

set -euo pipefail

DIR="${1:-output/}"
if [[ "$DIR" != */ ]]; then
  DIR="${DIR}/"
fi

ERRORS=0

echo "=== codebase-book output validation ==="
echo "output: $DIR"
echo ""

if [ ! -d "$DIR" ]; then
  echo "FAIL: output directory missing: $DIR"
  exit 1
fi

if ! compgen -G "${DIR}*.html" >/dev/null; then
  echo "FAIL: no HTML files in $DIR"
  exit 1
fi

echo "--- required assets ---"
for asset in style.css script.js; do
  if [ ! -s "${DIR}${asset}" ]; then
    echo "FAIL: missing or empty ${DIR}${asset}"
    ERRORS=$((ERRORS + 1))
  else
    echo "OK: ${asset}"
  fi
done

echo ""
echo "--- completion markers ---"
FOUND=$(python3 -c "
import glob, os
for path in sorted(glob.glob('${DIR}*.html')):
    first = open(path, encoding='utf-8').readline().strip()
    base = os.path.basename(path)
    if base in {'00_cover.html', '01_toc.html'}:
        continue
    if first != '<!-- generated: complete -->':
        print(f'{base}: first line is not complete marker')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "FAIL: incomplete or unmarked pages"
  echo "$FOUND"
  ERRORS=$((ERRORS + 1))
else
  echo "OK: all content pages have complete marker"
fi

echo ""
echo "--- local links ---"
FOUND=$(python3 -c "
import glob, os, re
dir_path='${DIR}'
for path in sorted(glob.glob(dir_path + '*.html')):
    text=open(path, encoding='utf-8').read()
    for m in re.finditer(r'href=[\"\\x27]([^\"\\x27]+)[\"\\x27]', text):
        href=m.group(1)
        if href.startswith(('#','http://','https://','mailto:','tel:','//')):
            continue
        target, _, anchor = href.partition('#')
        if not target:
            continue
        target_path=os.path.join(dir_path, target)
        if not os.path.exists(target_path):
            print(f'{os.path.basename(path)}: missing target {href}')
            continue
        if anchor:
            target_text=open(target_path, encoding='utf-8').read()
            if f'id=\"{anchor}\"' not in target_text and f\"id='{anchor}'\" not in target_text:
                print(f'{os.path.basename(path)}: missing anchor {href}')
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "FAIL: broken local links"
  echo "$FOUND"
  ERRORS=$((ERRORS + 1))
else
  echo "OK: local links"
fi

echo ""
echo "--- source reference hints ---"
COUNT=$(python3 -c "
import glob, re
count=0
for path in glob.glob('${DIR}*.html'):
    text=open(path, encoding='utf-8').read()
    count += len(re.findall(r'[A-Za-z0-9_./-]+\\.[A-Za-z0-9_+-]+:\\d+', text))
print(count)
" 2>/dev/null || echo 0)
if [ "${COUNT:-0}" -eq 0 ]; then
  echo "WARN: no file:line source references found"
else
  echo "OK: found $COUNT file:line source references"
fi

echo ""
echo "--- unresolved markers ---"
FOUND=$(grep -RIn 'TODO\|TBD\|待确认\|generated: partial' "$DIR"*.html 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "FAIL: unresolved markers found"
  echo "$FOUND" | head -20
  ERRORS=$((ERRORS + 1))
else
  echo "OK: no unresolved markers"
fi

echo ""
echo "--- script syntax ---"
if command -v node >/dev/null 2>&1 && [ -s "${DIR}script.js" ]; then
  if node -c "${DIR}script.js" >/dev/null 2>&1; then
    echo "OK: script.js syntax"
  else
    echo "FAIL: script.js syntax error"
    node -c "${DIR}script.js" || true
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "WARN: node unavailable or script.js missing; skipped"
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "OK: codebase-book output validation passed"
else
  echo "FAIL: $ERRORS hard validation issue(s)"
  exit 1
fi
