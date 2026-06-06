# Skill 边界定义

> 供 translate-book、review-tech-book、integrate-books、codebase-book 共享。定义各 skill 的职责边界、移交条件和报告查找方式。

---

## 职责矩阵

| 场景 | 使用 | 不使用 |
|------|------|--------|
| 翻译 EPUB/长篇技术文档为中文 HTML | translate-book | review-tech-book |
| 补齐翻译缺章或续译中断运行 | translate-book（补缺/恢复） | integrate-books |
| 从代码库生成项目学习书籍 | codebase-book | translate-book |
| 审阅翻译、整合或代码库书籍产出 | review-tech-book | 原生成 skill 直接评分 |
| 合并多本同领域技术书 | integrate-books | translate-book |
| 将源书特定章节补充到主书 | integrate-books（快速模式） | 全量整合流程 |
| 翻译 + 整合 | translate-book → integrate-books | 直接从英文 EPUB 整合，除非用户确认 |
| 整合 + 审阅 | integrate-books → review-tech-book | 用 review-tech-book 执行整合 |
| 代码库书籍 + 审阅 | codebase-book → review-tech-book | 用 review-tech-book 生成书 |
| 代码库书籍 + 整合参考书 | codebase-book → integrate-books | 用 integrate-books 从代码库生成内容 |
| 翻译 + 整合 + 审阅 | translate-book → integrate-books → review-tech-book | 跳过中间阶段 |
| 普通代码审阅 | 不使用任何 book skill | review-tech-book |
| 单点术语/错字修复 | 直接编辑目标文件 | translate-book 长流程 |

## 协作机制

- **translate-book → integrate-books**：源书是 EPUB 格式时，先翻译为 HTML 再整合。integrate-books 扫描 `.book-doc/runs/` 下最新 completed 的 `*-translate-*` 运行目录，读取 `report.md` 的术语表、已知问题和输出目录。
- **translate-book → review-tech-book**：翻译完成后，review-tech-book 自动查找翻译报告，重点审阅系统性残留、术语一致性、代码块完整性和读者体验。
- **integrate-books → review-tech-book**：整合完成后，review-tech-book 自动查找整合报告，重点审阅拼贴感、重复度、风格一致性和学习路径影响。
- **codebase-book → review-tech-book**：代码库书籍生成后，review-tech-book 自动查找 `*-codebase-*` 运行目录读取 `report.md`，审阅源码覆盖、file:line 证据、摘录一致性和架构学习路径。
- **codebase-book → integrate-books**：代码库书籍生成后需要整合参考书内容时，integrate-books 查找 `*-codebase-*` 报告获取源码覆盖表和架构证据，将代码库书籍视为主书进行整合。
- **review-tech-book → translate-book/integrate-books/codebase-book**：审阅默认只报告不修复；需要修复时，把问题按归属和修复批次回溯给原 skill。

## 移交规则

- 移交前置 skill 产出时，只传递 `report.md`、必要术语表、覆盖表、已知限制和验证摘要。
- 找不到前置报告时，记录缺失；若缺失会影响正确性或术语一致性，先询问用户是否继续降级执行。
- 不把一个 skill 的低层 QA 留给另一个 skill。生成阶段能修的问题应在生成阶段完成。
