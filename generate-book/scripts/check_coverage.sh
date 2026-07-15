#!/usr/bin/env bash
# 知识整合覆盖率校验脚本
# 用法: ./check_coverage.sh [knowledge_base_dir] [output_dir] [summary|stage1|stage5]
# 默认: .book-doc/knowledge_base/ output/

set -euo pipefail

KB="${1:-.book-doc/knowledge_base/}"
OUT="${2:-output/}"
STAGE="${3:-summary}"
if [[ "$KB" != */ ]]; then
  KB="${KB}/"
fi
if [[ "$OUT" != */ ]]; then
  OUT="${OUT}/"
fi
ERRORS=0

case "$STAGE" in
  summary|stage1|stage5) ;;
  *)
    echo "❌ 未知阶段模式: $STAGE"
    exit 1
    ;;
esac

echo "=== 整合覆盖率校验 ==="
echo "阶段模式: $STAGE"

# 1. 统计各源书知识点数
echo ""
echo "--- 知识点统计 ---"
TOTAL=0
SOURCE_DIRS=0
if [ -d "$KB" ]; then
  for DIR in "$KB"*/; do
    [ -d "$DIR" ] || continue
    NAME=$(basename "$DIR")
    if [ "$NAME" = "INDEX" ]; then
      continue
    fi
    SOURCE_DIRS=$((SOURCE_DIRS + 1))
    COUNT=$(find "$DIR" -name "*.md" | wc -l)
    echo "  $NAME: $COUNT 个知识点"
    TOTAL=$((TOTAL + COUNT))
  done
else
  echo "❌ 知识库目录不存在: $KB"
  ERRORS=$((ERRORS + 1))
fi
echo "  总计: $TOTAL 个知识点"
if [ "$SOURCE_DIRS" -eq 0 ] || [ "$TOTAL" -eq 0 ]; then
  if [ "$STAGE" = "stage5" ]; then
    echo "❌ 未找到源书知识点"
    ERRORS=$((ERRORS + 1))
  else
    echo "⚠ 未找到源书知识点（summary 仅报告；KB 应为 {book}/*.md 子目录结构）"
  fi
fi

ID_REPORT=$(python3 - "$KB" "${KB}INDEX/dsp_mapping.md" <<'PY'
import os
import re
import sys

kb, mapping = sys.argv[1], sys.argv[2]
ids = []
missing_id_files = []

for root, dirs, files in os.walk(kb):
    dirs[:] = [d for d in dirs if d != "INDEX"]
    if os.path.basename(root) == "INDEX":
        continue
    for name in files:
        if not name.endswith(".md"):
            continue
        path = os.path.join(root, name)
        with open(path, encoding="utf-8") as fh:
            head = fh.read(4096)
        match = re.search(r"^id:\s*([A-Za-z0-9_-]+)\s*$", head, re.MULTILINE)
        if match:
            ids.append(match.group(1))
        else:
            missing_id_files.append(os.path.relpath(path, kb))

unique_ids = sorted(set(ids))
mapping_text = ""
if os.path.exists(mapping):
    with open(mapping, encoding="utf-8") as fh:
        mapping_text = fh.read()

mapped_ids = []
for item_id in unique_ids:
    pattern = r"(?<![A-Za-z0-9_-])" + re.escape(item_id) + r"(?![A-Za-z0-9_-])"
    if re.search(pattern, mapping_text):
        mapped_ids.append(item_id)

unmapped = [item_id for item_id in unique_ids if item_id not in set(mapped_ids)]
print(f"IDS_TOTAL={len(unique_ids)}")
print(f"IDS_MAPPED={len(set(mapped_ids))}")
print(f"IDS_MISSING={len(missing_id_files)}")
print("IDS_MISSING_LIST=" + ",".join(missing_id_files[:10]))
print("IDS_UNMAPPED_LIST=" + ",".join(unmapped[:10]))
PY
)

IDS_TOTAL=0
IDS_MAPPED=0
IDS_MISSING=0
IDS_MISSING_LIST=""
IDS_UNMAPPED_LIST=""
while IFS='=' read -r KEY VALUE; do
  case "$KEY" in
    IDS_TOTAL) IDS_TOTAL="$VALUE" ;;
    IDS_MAPPED) IDS_MAPPED="$VALUE" ;;
    IDS_MISSING) IDS_MISSING="$VALUE" ;;
    IDS_MISSING_LIST) IDS_MISSING_LIST="$VALUE" ;;
    IDS_UNMAPPED_LIST) IDS_UNMAPPED_LIST="$VALUE" ;;
  esac
done <<< "$ID_REPORT"

echo "  有 ID 的知识点: $IDS_TOTAL"
if [ "$IDS_MISSING" -gt 0 ]; then
  if [ "$STAGE" = "stage5" ]; then
    echo "❌ $IDS_MISSING 个知识点文件缺少 frontmatter id"
    echo "  示例: $IDS_MISSING_LIST"
    ERRORS=$((ERRORS + 1))
  else
    echo "⚠ $IDS_MISSING 个知识点文件缺少 frontmatter id（summary 仅报告；stage5 才强制）"
  fi
fi

# 2. 检查映射文件
echo ""
echo "--- 映射状态 ---"
MAPPING="${KB}INDEX/dsp_mapping.md"
if [ -f "$MAPPING" ]; then
  ROWS=$(awk -F'|' 'NR>2 && NF>3 && $0 ~ /^\|/ {count++} END {print count+0}' "$MAPPING" 2>/dev/null || echo "0")
  echo "  映射表行数: $ROWS"
  echo "  已映射知识点 ID: $IDS_MAPPED"
  if [ "$IDS_TOTAL" -gt 0 ]; then
    COVERAGE=$((IDS_MAPPED * 100 / IDS_TOTAL))
    echo "  ID 映射覆盖率: ${COVERAGE}%"
    if [ "$STAGE" = "stage5" ] && [ "$COVERAGE" -lt 95 ]; then
      echo "❌ ID 映射覆盖率低于 95%"
      if [ -n "$IDS_UNMAPPED_LIST" ]; then
        echo "  未映射示例: $IDS_UNMAPPED_LIST"
      fi
      ERRORS=$((ERRORS + 1))
    fi
  fi
else
  if [ "$STAGE" = "stage5" ]; then
    echo "❌ 映射文件不存在: $MAPPING"
    ERRORS=$((ERRORS + 1))
  else
    echo "⚠ 映射文件不存在: $MAPPING"
  fi
fi

GAPS="${KB}INDEX/gaps.md"
if [ -f "$GAPS" ]; then
  GAP_COUNT=$(awk '/^-/{count++} END {print count+0}' "$GAPS" 2>/dev/null || echo "0")
  echo "  覆盖缺口: $GAP_COUNT"
else
  if [ "$STAGE" = "stage5" ]; then
    echo "❌ 缺口文件不存在: $GAPS"
    ERRORS=$((ERRORS + 1))
  else
    echo "⚠ 缺口文件不存在: $GAPS"
  fi
fi

# 3. 检查覆盖率
echo ""
echo "--- 输出覆盖率 ---"
if [ -d "$OUT" ]; then
  HTML_COUNT=$(find "$OUT" -maxdepth 1 -type f -name "*.html" | wc -l | tr -d '[:space:]')
  ITEM_ANCHORS=$( (grep -roh 'id="item-[0-9]*"' "$OUT"*.html 2>/dev/null || true) | sort -u | wc -l | tr -d '[:space:]' )
  INTEGRATED=$( (grep -rl '<!-- integrated:' "$OUT"*.html 2>/dev/null || true) | wc -l | tr -d '[:space:]' )
  echo "  HTML 页面: $HTML_COUNT"
  echo "  内容锚点: $ITEM_ANCHORS"
  echo "  已整合章节: $INTEGRATED"
  if [ "$STAGE" = "stage5" ] && [ "$HTML_COUNT" -eq 0 ]; then
    echo "❌ 输出目录中没有 HTML 文件"
    ERRORS=$((ERRORS + 1))
  fi
  if [ "$STAGE" = "stage5" ] && [ "$HTML_COUNT" -gt 0 ] && [ "$INTEGRATED" -eq 0 ]; then
    echo "❌ 未发现任何整合标记"
    ERRORS=$((ERRORS + 1))
  fi
else
  if [ "$STAGE" = "stage5" ]; then
    echo "❌ 输出目录不存在: $OUT"
    ERRORS=$((ERRORS + 1))
  else
    echo "⚠ 输出目录不存在: $OUT"
  fi
fi

# 4. 术语冲突检测
echo ""
echo "--- 术语一致性 ---"
if [ -f "$MAPPING" ]; then
  # 检查同一英文术语是否有多种中文译法
  DUPES=$(awk -F'|' 'NR>1 && NF>3 {gsub(/^ +| +$/,"",$3); print $3}' "$MAPPING" 2>/dev/null | sort | uniq -c | sort -rn | awk '$1 > 1' || true)
  if [ -n "$DUPES" ]; then
    echo "⚠ 同一术语有多种译法:"
    echo "$DUPES" | head -10
  else
    echo "✅ 术语一致"
  fi
else
  echo "⚠ 跳过（映射文件不存在）"
fi

echo ""
echo "=== 校验完成 ==="
if [ "$ERRORS" -gt 0 ]; then
  if [ "$STAGE" = "stage5" ]; then
    echo "❌ $ERRORS 项硬性检查未通过（stage5 强制 exit）"
    exit 1
  else
    echo "⚠ $ERRORS 项硬性检查未通过（summary 仅报告不 exit；交付前用 stage5 卡门）"
  fi
fi

echo "✅ 硬性检查通过"
