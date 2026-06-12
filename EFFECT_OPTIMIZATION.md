# 书籍 Skill 效果优化总结

## 优化日期
2026-06-09

## 核心问题

用户反馈："我只要最终的效果最佳，生成的书籍质量最佳。"

经过分析，发现质量问题的根本原因不是"规则不够多"，而是：

1. **规则是"建议"而非"强制"**：模型可以跳过 gate 检查
2. **缺乏"常见错误"预警**：模型不知道自己容易犯什么错
3. **阶段依赖不明确**：模型不知道"如果 Phase 0 没完成，不能进入 Phase 1"
4. **证据要求模糊**："差不多"就够了，没有具体的检查标准
5. **事后检查而非事前预防**：质量门控在生成阶段执行不到位

## 优化策略

### 1. 增加"常见错误"预警（解决"模型不知道自己错在哪"）

每个 skill 增加了 **5 个常见错误** 的预警：

```markdown
## What Failure Looks Like (Common Model Mistakes)

**Mistake 1: Patchwork insertion**
- Model behavior: "I'll add source content after main book content"
- Result: Reader sees clear seams between main and source
- Fix: Interleave content, rewrite everything in main book style
```

**效果**：模型在执行前就知道"这样做会失败"，从而避免错误。

### 2. 明确"如果不这样做会怎样"（解决"规则是建议而非强制"）

每个 gate 检查都增加了明确的后果：

```markdown
**Gate (must pass)**:
- [ ] Coverage ≥80% per source
- [ ] Every chapter has ≥1 item
- [ ] All core topics extracted

**If gate fails**: Re-extract missing chapters. Do not enter Phase 2.
```

**效果**：模型知道"如果不通过 gate，就不能继续"，而不是"差不多就行了"。

### 3. 阶段依赖关系明确化（解决"模型跳过步骤"）

增加了强制性的阶段依赖：

```markdown
**Critical rule**: You cannot enter Phase N until Phase N-1 is complete with evidence. No exceptions.
```

**效果**：模型知道"必须先完成 Phase 0，才能进入 Phase 1"，不能跳过。

### 4. 证据要求具体化（解决"差不多就行了"）

每个 gate 检查都有具体的证据要求：

```markdown
| # | Check | Evidence Required |
|---|-------|-------------------|
| G1 | All plan.md IDs have markers | List every ID, show marker location |
| G2 | New code has V1-V3 tags | List every code block, show tag |
| G3 | Style matches baseline | Compare 3 paragraphs: sentence length, terminology, tone |
```

**效果**：模型知道"需要什么样的证据"，而不是"看起来没问题"。

### 5. 质量门控前置（解决"审阅几十轮还有问题"）

将质量门控从"事后检查"变为"事中检查"：

```
旧流程：Phase 4 (生成) → Phase 5 (校验) → review-tech-book (审阅)
新流程：Phase 4 (生成) → Phase 4.5 (强制门控) → 通过 → 下一章
                              ↓ 不通过
                            立即返工
```

**效果**：问题在生成阶段就被发现和修复，不会积累到审阅阶段。

## 文件变更

### 修改文件
- `integrate-books/SKILL.md` — 增加常见错误预警，明确 gate 后果，具体化证据要求
- `review-tech-book/SKILL.md` — 同上
- `translate-book/SKILL.md` — 同上
- `codebase-book/SKILL.md` — 同上

### 关键设计变化

**旧版本**：
```markdown
## Core Rules
1. Reader cannot tell which paragraph came from which source
2. Full rewrite, not patchwork
...

## Phase 4: Rewrite
1. Read plan.md
2. Rewrite content
3. Add markers
```

**新版本**：
```markdown
## What Failure Looks Like (Common Model Mistakes)
**Mistake 1: Patchwork insertion**
- Model behavior: "I'll add source content after main book content"
- Result: Reader sees clear seams
- Fix: Interleave content, rewrite everything

## Phase 4: Rewrite
**Critical**: Do not paste source content. Do not keep source structure. Rewrite everything.

### Phase 4.5: Quality Gate (Mandatory)
After every chapter. No exceptions.

| # | Check | Evidence Required |
|---|-------|-------------------|
| G1 | All plan.md IDs have markers | List every ID, show marker location |
...

**All 5 must pass. Any fail = rewrite chapter.**
```

## 预期效果

1. **模型更清楚自己在做什么**：常见错误预警让模型知道"这样做会失败"
2. **模型更清楚后果**："If gate fails"让模型知道"不通过就不能继续"
3. **证据更具体**："Evidence Required"让模型知道"需要什么样的证据"
4. **质量在生成阶段就保证**：Phase 4.5 的强制门控防止问题积累
5. **审阅更高效**：问题在生成阶段就被发现和修复，审阅阶段问题更少

## 与精简版本的区别

**精简版本**：追求最小字节数，删除了"为什么"的解释
**效果版本**：追求最佳质量，保留了"常见错误"预警和"如果不这样做会怎样"的后果

**关键洞察**：
- 精简版本假设"模型会自觉遵从"
- 效果版本假设"模型需要知道什么会失败"
- 效果版本增加了"常见错误"预警，让模型在执行前就知道"这样做会失败"
- 效果版本增加了"如果不这样做会怎样"的后果，让模型知道"不通过就不能继续"
