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
echo "--- editable draw.io diagrams ---"
RUN_DIR="$(cd "$DIR/.." && pwd)"
SPEC_DIR="${RUN_DIR}/diagram-specs"
DIAGRAM_DIR="${DIR}diagrams"
export DIR SPEC_DIR DIAGRAM_DIR
FOUND=$(python3 - <<'PY' 2>/dev/null || true
import glob, json, os, re, sys
import xml.etree.ElementTree as ET

dir_path = os.environ["DIR"]
spec_dir = os.environ["SPEC_DIR"]
diagram_dir = os.environ["DIAGRAM_DIR"]
errors = []

editable_links = []
for html_path in glob.glob(os.path.join(dir_path, "*.html")):
    text = open(html_path, encoding="utf-8").read()
    if '<figure class="editable-diagram"' in text:
        editable_links.extend(re.findall(r'href=["\']([^"\']+\.drawio)["\']', text))
    if re.search(r'<pre\s+class=["\']mermaid["\']', text):
        errors.append(f"{os.path.basename(html_path)}: bare Mermaid block remains")

for link in editable_links:
    target = os.path.normpath(os.path.join(dir_path, link))
    if not os.path.exists(target):
        errors.append(f"missing drawio target: {link}")

for path in glob.glob(os.path.join(diagram_dir, "*.drawio")):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        errors.append(f"{os.path.basename(path)}: invalid XML: {exc}")
        continue
    if root.tag != "mxfile":
        errors.append(f"{os.path.basename(path)}: root is {root.tag}, expected mxfile")

for path in glob.glob(os.path.join(spec_dir, "*.json")):
    try:
        spec = json.load(open(path, encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{os.path.basename(path)}: invalid JSON: {exc}")
        continue
    if len(spec.get("nodes", [])) < 2:
        errors.append(f"{os.path.basename(path)}: fewer than two nodes")
    if len(spec.get("edges", [])) < 1:
        errors.append(f"{os.path.basename(path)}: fewer than one edge")
    for edge in spec.get("edges", []):
        if not edge.get("evidence") and not edge.get("inferred_reason"):
            errors.append(f"{os.path.basename(path)}: edge {edge.get('from')}->{edge.get('to')} lacks evidence")

if errors:
    print("\n".join(errors))
    sys.exit(1)
PY
)
if [ -n "$FOUND" ]; then
  echo "FAIL: editable diagram validation"
  echo "$FOUND"
  ERRORS=$((ERRORS + 1))
else
  echo "OK: editable draw.io diagrams"
fi

echo ""
echo "--- source file:line references ---"
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
echo "--- narrative coherence check ---"
FOUND=$(python3 -c "
import glob, os
dir_path='${DIR}'
skip={'00_cover.html','01_toc.html'}
optional={'12_glossary.html','glossary.html','index.html'}
bad=[]
for path in sorted(glob.glob(dir_path + '*.html')):
    base=os.path.basename(path)
    if base in skip or base in optional:
        continue
    text=open(path, encoding='utf-8').read()
    plain=re.sub(r'<[^>]+>', '', text) if 're' in dir() else text
    import re
    plain=re.sub(r'<[^>]+>', '', text)
    if '自行查阅' in plain or '自行了解' in plain:
        bad.append(f'{base}: sends reader to external self-study')
    # Check for code blocks without following explanation
    code_blocks = re.findall(r'<pre[^>]*>.*?</pre>', text, re.DOTALL)
    if len(code_blocks) > 5:
        # Check that there are substantial text paragraphs between code blocks
        paragraphs = [p.strip() for p in re.split(r'<p>', text) if len(re.sub(r'<[^>]+>', '', p).strip()) > 50]
        if len(paragraphs) < len(code_blocks) // 2:
            bad.append(f'{base}: too many code blocks relative to explanation paragraphs')
if bad:
    print('\n'.join(bad))
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "WARN: narrative coherence issues"
  echo "$FOUND" | head -20
else
  echo "OK: narrative coherence (no external self-study, code-text balance)"
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
echo "--- content depth check ---"
FOUND=$(python3 -c "
import glob, os
dir_path='${DIR}'
skip={'00_cover.html','01_toc.html','style.css','script.js'}
bad=[]
for path in sorted(glob.glob(dir_path + '*.html')):
    base=os.path.basename(path)
    if base in skip:
        continue
    size = os.path.getsize(path)
    is_overview = base.startswith('02_') or base.startswith('03_')
    is_index = 'glossary' in base or 'index' in base or 'cheatsheet' in base
    if is_index and size < 6000:
        bad.append(f'{base}: {size} bytes (index pages should be >= 6KB)')
    elif is_overview and size < 10000:
        bad.append(f'{base}: {size} bytes (overview pages should be >= 10KB)')
    elif not is_index and not is_overview and size < 20000:
        bad.append(f'{base}: {size} bytes (core pages should be >= 20KB)')
if bad:
    print('\n'.join(bad))
" 2>/dev/null || true)
if [ -n "$FOUND" ]; then
  echo "WARN: pages below minimum content depth"
  echo "$FOUND"
else
  echo "OK: all pages meet minimum content depth"
fi

echo ""
echo "--- run structure coverage ---"
CHAPTER_PLAN=""
for RUN_DIR in .book-doc/runs/*-codebase-*/; do
  CANDIDATE="${RUN_DIR}chapter-plan.md"
  if [ -f "$CANDIDATE" ]; then
    CHAPTER_PLAN="$CANDIDATE"
  fi
done
if [ -z "$CHAPTER_PLAN" ] || [ ! -f "$CHAPTER_PLAN" ]; then
  echo "WARN: no chapter-plan.md found, skipping coverage check"
else
  FOUND=$(python3 -c "
import re, glob, os, sys
plan = open('${CHAPTER_PLAN}').read()
src_files = re.findall(r'\|\s*([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)\s*\|', plan)
src_files = list(dict.fromkeys(src_files))
html_files = set(os.path.basename(f) for f in glob.glob('${DIR}*.html'))
stubs = []
for f in sorted(glob.glob('${DIR}*.html')):
    size = os.path.getsize(f)
    if size < 200:
        stubs.append(f'{os.path.basename(f)}: {size} bytes (possible stub)')
if stubs:
    print('STUB:' + ','.join(stubs))
else:
    print(f'OK: {len(html_files)} output pages, {len(src_files)} source files in coverage table')
" 2>/dev/null || echo "WARN: coverage check failed")
  if echo "$FOUND" | grep -q "^STUB:"; then
    STUB_LIST=$(echo "$FOUND" | sed 's/^STUB://')
    echo "FAIL: suspiciously small output files (possible stubs)"
    echo "$STUB_LIST"
    ERRORS=$((ERRORS + 1))
  else
    echo "$FOUND"
  fi
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
