#!/usr/bin/env bash
# 多源整合覆盖率校验
# 用法: ./check_coverage.sh [knowledge_base_dir] [output_dir]
# 数据契约：
#   - {KB}/{书名}/*.md  文件数 = 每源深读笔记基数（每源必须非空）
#   - {OUT}/*.html  中 <!-- integrated: ... --> 标记 = 整合证据（总数 + 章节分布）
# 判定留给模型的（脚本测不了）：单源占比 ≤80%、融合到无法辨识来源。

set -euo pipefail

KB="${1:-.book-doc/knowledge_base/}"
OUT="${2:-output/}"
if [[ "$KB" != */ ]]; then
  KB="${KB}/"
fi
if [[ "$OUT" != */ ]]; then
  OUT="${OUT}/"
fi
ERRORS=0

echo "=== 整合覆盖率校验 ==="

# 1. 每源深读笔记基数
echo ""
echo "--- 源书笔记统计 ---"
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
    echo "  $NAME: $COUNT 篇笔记"
    if [ "$COUNT" -eq 0 ]; then
      echo "❌ 源书 $NAME 笔记为空——没读透就别往下走"
      ERRORS=$((ERRORS + 1))
    fi
    TOTAL=$((TOTAL + COUNT))
  done
else
  echo "❌ 知识库目录不存在: $KB"
  ERRORS=$((ERRORS + 1))
fi
echo "  总计: $SOURCE_DIRS 个源 / $TOTAL 篇笔记"
if [ "$SOURCE_DIRS" -eq 0 ]; then
  echo "❌ 未找到源书笔记目录（{KB}/{书名}/*.md）"
  ERRORS=$((ERRORS + 1))
fi

# 2. 输出整合证据
echo ""
echo "--- 输出整合证据 ---"
if [ -d "$OUT" ]; then
  HTML_COUNT=$(find "$OUT" -maxdepth 1 -type f -name "*.html" | wc -l | tr -d '[:space:]')
  if [ "$HTML_COUNT" -eq 0 ]; then
    echo "❌ 输出目录中没有 HTML 文件: $OUT"
    ERRORS=$((ERRORS + 1))
  else
    echo "  HTML 页面: $HTML_COUNT"
    INTEGRATED=$( (grep -rl '<!-- integrated:' "$OUT"*.html 2>/dev/null || true) | wc -l | tr -d '[:space:]')
    if [ "$INTEGRATED" -eq 0 ]; then
      echo "❌ 未发现任何 <!-- integrated --> 整合标记（多源书必须逐章标注来源）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  含整合标记的章节: $INTEGRATED / $HTML_COUNT"
      echo "  各章标记数:"
      for f in "$OUT"*.html; do
        N=$( (grep -o '<!-- integrated:' "$f" 2>/dev/null || true) | wc -l | tr -d '[:space:]')
        echo "    $(basename "$f"): $N"
      done
    fi
  fi
else
  echo "❌ 输出目录不存在: $OUT"
  ERRORS=$((ERRORS + 1))
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
  echo "❌ $ERRORS 项硬性检查未通过"
  exit 1
fi
echo "✅ 硬性检查通过（单源占比 / 融合度由模型按底线自检）"
