#!/usr/bin/env bash
# 把 tech_book_skills 装进三工具（Claude Code / OpenCode / Codex）的用户级 skill 扫描目录。
# 方式：符号链接——仓库是单一源、可逆（--uninstall）。
# 三工具扫描路径不同（见 README「安装」），故默认同时链接进 ~/.agents/skills/ 与 ~/.claude/skills/。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS=(take-note generate-book review-tech-book shared)   # shared/ 是三 skill 的兄弟资源（无 SKILL.md，不被当 skill 加载）

AGENTS_DIR="${HOME}/.agents/skills"   # Codex CLI + OpenCode
CLAUDE_DIR="${HOME}/.claude/skills"   # Claude Code（OpenCode 也扫这里）

TARGETS=()
UNINSTALL=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agents)    TARGETS+=("$AGENTS_DIR"); shift;;
    --claude)    TARGETS+=("$CLAUDE_DIR"); shift;;
    --all)       TARGETS+=("$AGENTS_DIR" "$CLAUDE_DIR"); shift;;
    --uninstall) UNINSTALL=1; shift;;
    -h|--help)   sed -n '2,5p' "$0"; exit 0;;
    *) echo "未知参数: $1（见 --help）" >&2; exit 1;;
  esac
done
[[ ${#TARGETS[@]} -eq 0 ]] && TARGETS=("$AGENTS_DIR" "$CLAUDE_DIR")

for dir in "${TARGETS[@]}"; do
  for s in "${SKILLS[@]}"; do
    link="$dir/$s"; target="$SCRIPT_DIR/$s"
    if [[ $UNINSTALL -eq 1 ]]; then
      [[ -L "$link" ]] && { rm "$link"; echo "✗ 移除 $link"; }
      continue
    fi
    mkdir -p "$dir"
    if [[ -e "$link" || -L "$link" ]]; then
      if [[ -L "$link" && "$(readlink -f "$link" 2>/dev/null)" == "$(readlink -f "$target" 2>/dev/null)" ]]; then
        echo "✓ 已存在 $link"
      else
        echo "! 跳过 $link（已存在且非本仓库链接，需手动处理）" >&2
      fi
      continue
    fi
    ln -s "$target" "$link"
    echo "✚ 链接 $link → $target"
  done
done
