# Skill 边界

> 所有书籍 skill 共享。谁做什么，何时交接。

## 矩阵

| 任务 | 使用 | 不要使用 |
|------|------|----------|
| 从单一来源生成书籍 | generate-book（单源模式） | review-tech-book |
| 从多个来源生成书籍 | generate-book（多源模式） | review-tech-book |
| 补充缺失章节 | generate-book（单源模式） | review-tech-book |
| 审查已生成的书籍 | review-tech-book | generate-book |
| 从代码库生成书籍 | codebase-book | generate-book |
| 生成 + 审查 | generate-book → review-tech-book | 跳过审查 |
| 代码库 + 审查 | codebase-book → review-tech-book | 跳过审查 |
| 常规代码审查 | 无 | review-tech-book |
| 单个术语修正 | 直接编辑 | generate-book |

## 交接规则

- generate-book → review-tech-book：传递 `report.md`、统一术语、覆盖度、已知限制
- codebase-book → review-tech-book：传递 `report.md`、来源覆盖度、file:line 证据
- review-tech-book → 原始 skill：按归属路由修复项，按优先级批量处理

## 核心原则

不要将低级别的质量检查（QA）传递给其他 skill。在生成阶段即修复问题。
