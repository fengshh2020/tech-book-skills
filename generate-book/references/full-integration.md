# 完整整合指南（Full Integration Guide）

> 如何做到真正的完整整合，而非拼凑缝合。

## 整合级别

| 级别 | 名称 | 操作 | 可接受？ |
|------|------|------|---------|
| L1 | 直接插入（Direct Insert） | 原样粘贴源内容 | ❌ |
| L2 | 风格适配（Style Adapt） | 改写措辞，保留结构 | ❌ |
| L3 | 重组（Reorganize） | 重新设计结构，重写内容 | ✅ |
| L4 | 完全融合（Full Fusion） | 从所有来源重新设计，无法辨识出处 | ✅ |

**要求**：阶段 4 输出必须达到 L3 或 L4。

## 5 步改写法

1. **解构所有来源**：打开每个来源的相关章节。提取概念、顺序、示例、类比。
2. **设计新结构**：不使用任何来源的原始目录。按读者认知组织。
3. **分配主/次来源**：每个小节有一个主要来源用于叙事，其他用于深度补充。
4. **以主干风格改写**：匹配基线（人称、句长、术语、语调）。
5. **验证不可辨识性**：随机抽取 3 段测试 —— 读者能否看出来源？

## 反模式（Anti-Patterns）

| 模式 | 问题 | 修复方式 |
|------|------|---------|
| "我改写了措辞" | 结构未变，读者能看出 | 重组结构 |
| "我在主干之后添加了" | 主干内容与源内容之间有明显接缝 | 交错穿插内容 |
| "我把所有来源分组了" | 每个主题内风格切换 | 每小节只设一个主要来源 |

## 质量测试

每章完成后：

```
□ Random 3 paragraphs: can tell source? (no = pass)
□ Terminology consistent?
□ Narrative flow natural?
□ Depth consistent?
□ Example follows same storyline?
```

记录到 `progress.md`：
```
### ChN Source Test
- Sample paragraphs: 3
- Identifiable: X/3 (target: ≤1/3)
- Terms: pass/fail
- Flow: pass/fail
- Depth: pass/fail
- Result: pass/rewrite
```
