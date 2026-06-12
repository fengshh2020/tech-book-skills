# Skill 职责与边界

> 所有书籍 skill 共享。谁做什么，何时交接，谁负责修复。

## 任务路由

| 任务 | 使用 | 不要使用 |
|------|------|----------|
| 从单一来源生成书籍 | generate-book（单源模式） | review-tech-book |
| 从多个来源生成书籍 | generate-book（多源模式） | review-tech-book |
| 从代码库生成书籍 | generate-book（代码库模式） | review-tech-book |
| 补充缺失章节 | generate-book（单源模式） | review-tech-book |
| 审查已生成的书籍 | review-tech-book | generate-book |
| 生成 + 审查 | generate-book → review-tech-book | 跳过审查 |
| 代码库 + 审查 | generate-book（代码库模式） → review-tech-book | 跳过审查 |
| 常规代码审查 | 无 | review-tech-book |
| 单个术语修正 | 直接编辑 | generate-book |

## 交接规则

- generate-book → review-tech-book：传递 `report.md`、统一术语、覆盖度、已知限制
- generate-book（代码库模式） → review-tech-book：传递 `report.md`、来源覆盖度、file:line 证据
- review-tech-book → 原始 skill：按归属路由修复项，按优先级批量处理

## 质量归属原则

1. **一次做对**：生成阶段修复其能验证的问题。不要将拼写错误、格式、链接问题留给审查阶段。
2. **仅报告系统性问题**：审查报告关注跨章节的模式，而非逐条列出问题。
3. **集成阶段负责风格**：generate-book 负责调整风格和去除重复内容。审查仅检查读者可见的衔接处（seams）。
4. **来源可追溯**：generate-book（代码库模式）提供 file:line（文件:行号）证据。审查负责验证覆盖度和学习路径。

## 职责划分

| 问题类型 | 负责方 | 审查方 |
|----------|--------|--------|
| 拼写错误、编码、标点 | generate-book | 仅报告系统性模式 |
| 术语、词汇表 | generate-book | 跨章节不一致性 |
| 代码块、图片、导航链接 | generate-book | 引用验证摘要 |
| 内容来源、风格、去重 | generate-book | 读者可见的衔接处 |
| 来源覆盖度、摘录 | generate-book（代码库模式） | 覆盖度表格、证据链 |
| 技术正确性、版本 | review-tech-book | V1-V3 证据 |
| 学习路径、读者适配 | review-tech-book | 核心输出 |

## 报告去重

- 同类问题出现 >3 次 → 合并为系统性发现
- 自动化工具已列出的 → 报告中仅保留摘要
- 评分表 ≠ 问题列表：评分是判断结论，详情见发现部分

## 核心原则

不要将低级别的质量检查（QA）传递给其他 skill。在生成阶段即修复问题。
