# 0003 — 全书 light-only，去除暗色模式

去除书籍 HTML 版的暗色主题。CSS 删除 `[data-theme=dark]` / `prefers-color-scheme` 相关整块；`script.js` 删除 `.sb-toggle` 主题切换与 localStorage 持久化；移除主题切换按钮；移除 SVG `currentColor` 主题同步逻辑。

## 理由
用户明确不需要暗色模式。去除后：简化 CSS/JS、消除主题感知图表机制（使图表只出 PNG 即可，见 [ADR-0004](./0004-diagrams-mermaid-to-png.md)）。"静奢"美学在浅色下同样成立。

## 代价
读者无法切换暗色（长时阅读偏好）。若未来需要，须重新引入双主题 CSS 与主题感知图表机制——非零成本。
