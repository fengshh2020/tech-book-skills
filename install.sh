#!/usr/bin/env bash
# 把 tech_book_skills 装进三工具（Claude Code / OpenCode / Codex）的用户级 skill 扫描目录。
# 方式：符号链接——仓库是单一源、可逆（--uninstall）。
# 三工具扫描路径不同（见 README「安装」），故默认同时链接进 ~/.agents/skills/ 与 ~/.claude/skills/。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS=(take-note generate-book review-tech-book research tech-proposal shared)   # shared/ 是 skill 的兄弟资源（无 SKILL.md，不被当 skill 加载）

AGENTS_DIR="${HOME}/.agents/skills"   # Codex CLI + OpenCode
CLAUDE_DIR="${HOME}/.claude/skills"   # Claude Code（OpenCode 也扫这里）

TARGETS=()
UNINSTALL=0
FORCE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agents)    TARGETS+=("$AGENTS_DIR"); shift;;
    --claude)    TARGETS+=("$CLAUDE_DIR"); shift;;
    --all)       TARGETS+=("$AGENTS_DIR" "$CLAUDE_DIR"); shift;;
    --uninstall) UNINSTALL=1; shift;;
    --force)     FORCE=1; shift;;
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
        continue
      fi
      # drift：已存在但非本仓库链接（如 ~/.agents 下的真目录副本）。
      # --force 备份旧值后重建为仓库链接；否则跳过并提示（旧版仅 stderr 提示，drift 会永久化）。
      if [[ $FORCE -eq 1 ]]; then
        mv "$link" "${link}.drift-bak.$(date +%s)" 2>/dev/null || rm -rf "$link" || { echo "! 无法移除 $link，跳过（需手动处理）" >&2; continue; }
        ln -s "$target" "$link"
        echo "↻ --force 重建 $link → $target（旧值备份为 *.drift-bak.*）"
      else
        echo "! 跳过 $link（已存在且非本仓库链接；加 --force 强制重建会备份旧值）" >&2
      fi
      continue
    fi
    ln -s "$target" "$link"
    echo "✚ 链接 $link → $target"
  done
done
