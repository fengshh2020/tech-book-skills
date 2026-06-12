# 进度协议（Progress Protocol）

> 所有书籍 skill 共享。管理运行发现（discovery）、状态文件、计时保存、幂等性（idempotency）与恢复。

## 运行目录结构

```
.book-doc/
├── spec.md                          # 跨次运行的配置
├── knowledge_base/                  # 跨次运行的知识库（generate-book 多源模式）
└── runs/
    └── {YYYYMMDD}-{slug}-{label}/
        ├── progress.md              # 唯一真实来源（single source of truth）
        ├── context-summary.md       # 跨阶段摘要（generate-book）
        ├── plan.md                  # 生成计划
        ├── findings/                # 审查发现
        └── report.md                # 完成报告
```

## 运行标识符（Slug）

| Skill | 标识符 |
|-------|--------|
| generate-book | generate |
| review-tech-book | review |
| codebase-book | codebase |

## 阶段完成协议

**每个阶段结束时**（强制执行，不可跳过）：

1. **写入输出**：确认所有文件已写入磁盘。
2. **更新 progress.md**：标记阶段 ✅，写入输出路径。
3. **回读验证**：确认 progress.md 确实显示 ✅。
4. **进入下一阶段**：仅在步骤 1-3 全部通过后执行。

## 阅读证据协议

> 防止"声称已读但实际未读"的情况。

**每次声称的阅读**必须包含以下至少 2 项：
- **结构信息**：段落数、代码块数、总行数
- **内容摘要**：具体论点（而非仅复述标题）
- **术语提取**：文件中至少 3 个实际技术术语

**以下红旗 = 视为未读**：
- 无证据的"没有问题"
- 内容摘要仅是标题改写
- 连续章节的证据格式完全相同
- 没有结构数据的"本章很简单"

## 恢复机制

1. 扫描 `.book-doc/runs/` 查找 `*{slug}*`
2. 读取候选运行的 `progress.md`
3. 只有一个活跃/中断的运行 → 直接恢复
4. 有多个 → 询问用户
5. 没有或全部已完成 → 创建新运行

## 跨 Skill 报告查找

按日期前缀查找最新的 `completed`（已完成）运行：
- 生成类：`*-generate-*/report.md`
- 审查类：`*-review-*/report.md`
- 代码库类：`*-codebase-*/report.md`

报告缺失时：记录并询问用户是否影响正确性。
