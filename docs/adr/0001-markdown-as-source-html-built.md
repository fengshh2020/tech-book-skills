# 0001 — Markdown 为源，HTML 由 MD 构建

generate-book 此前直接生成 HTML 章节（每章手写 `<div class="sidebar">` 等组件 class）。现改为：**agent 写通用/GitHub 方言 Markdown，由一个新增的 builder 把 MD 包进现有"静奢" HTML 设计系统**（blockquote→sidebar、code fence→组件、图+图注→figure）。MD 成为一等公民与可移植主源，HTML 成为渲染目标。

## 考虑过的方案
- **HTML→MD 后处理导出**：最小改动，但 MD 是 HTML 的降级投影、富组件映射有损，且 MD 非一等公民。
- **并行双写**：质量最高但双倍写作量、两份易漂移、维护最重。

## 选 MD 为源的理由
单一信息源、MD 可 diff / 可移植 / 可版本控制；HTML 设计系统作为渲染层保留其全部价值。代价：`book-assembly.md` 与生成 prompt 需大改；builder 须维护"MD 约定 → HTML 组件"映射表。

## 关键约束
作者约定必须兼容通用/GitHub 方言（Q1 决议）：GitHub 不渲染围栏指令/admonition，会原样显示裸 HTML。约定须"优雅降级"——GitHub 上可读，builder 识别后升级为富组件。见 ADR-0002。
