---
name: tech-proposal
description: "Use when the user wants to design a technical solution — from a new system, a new feature, or a requirement change — producing a structured proposal document with embedded code scaffolds. Triggers: 设计方案, 技术方案, 怎么做, 怎么实现, 选型, 架构设计, design proposal, tech proposal, how to implement, architecture design, 需求变更方案, 新增功能设计, 加个功能, 改造方案. Do NOT trigger for: generating books/docs (use generate-book), recording existing conclusions (use take-note), reviewing quality (use review-tech-book), pure research without design (use research)."
allowed-tools: Read Write Edit Glob Grep
---

# 技术方案推演

从技术目标推演到结构化方案文档 + 内嵌代码骨架——读起来像方案，不是拼贴画。覆盖从零设计新系统、已有系统新需求、需求变更三种场景。任意技术栈通用。

**先读 `../shared/writing-core.md`**——铁律、写作原则、证据等级 V1-V4、失败模式、剪枝都在那，本文件与各 reference 不再重述。任一阶段开始前按需读对应 reference，不顺手全读。

## 能力轴：场景 × 产出

| 场景 | 侧重点 | 产出 |
|------|--------|------|
| 从零设计新系统 | 全局模块拆分、技术选型、部署架构 | 方案文档 + 代码骨架 |
| 已有系统 + 新需求 | 在已有架构上找接入点、解耦新模块 | 方案文档 + 代码骨架（标注已有/新增） |
| 需求变更 | 评估变更影响、调整接口、迁移路径 | 方案文档 + 变更影响矩阵 |

## 启动前（推演耗时长，判错 = 整轮返工）

1. **判场景**：从零 / 增量 / 变更——影响后续调研深度和架构设计策略。
2. **🛑 向用户确认再开跑**：目标与意图一致 ｜ 场景判对 ｜ 产出落点（项目目录 or 存库）无误。拿不准让用户显式指定。
3. **预检**：项目目录可写、已有代码库可读（增量/变更场景）。失败 = 停下告知用户。

## 流程

**目标澄清 → 调研 → 约束提炼 → 架构设计 → 代码骨架 → 自检**。每段结束按 writing-core 失败模式自检（假读 / 缩水 / 伪造校验 / 推断当结论）。**上下文工程**（writing-core 总律）：按需读 reference，不为"全面"预加载。

### ① 目标澄清（自适应深度）

**具体目标**（如"GO2 加语音控制"）：一轮确认——目标、已有系统、预期产出范围。

**模糊目标**（如"做一个嵌入式 AI 系统"）：多轮追问——
- 要解决什么问题？给谁用？
- 目标硬件/平台？已有代码库？
- 成功标准？时间约束？
- 哪些事**不做**？（Non-Goals 提前锁定）

产出：目标陈述（1 段话 + Goals + Non-Goals）。

### ② 调研

**外部调研**：调 research，发出定向调研请求——

```
调研请求：
- 目标：{一句话要回答的问题}
- 需要确认的领域：[{SDK 接口}, {硬件约束}, {框架选型}, {已知坑}]
- 证据等级要求：≥V2（硬约束须源码/文档确认，不接受 V4 推断）
- 产出格式：Finding Block（Answer + Evidence + Gaps + Meta）
```

research 返回 Finding Block 后检查：
- **Gaps 非空** → 标为"待定"进方案风险区，或追加一轮调研
- **证据等级不够** → 降级为软约束或标 `[!caution] 推断`
- **发现推翻假设** → 回到③重新提炼约束

**已有代码调研**（增量/变更场景）：读现有代码→找 seam→评估影响范围→记录已有架构约束。每论断带 `file:line`。

### ③ 约束提炼

从调研结果提炼：

| 类型 | 来源 | 示例 |
|------|------|------|
| 硬约束（不可妥协） | 硬件限制 / SDK 限制 / 兼容性 / 实时性 / 法规 | "Jetson Orin 16GB VRAM"、"UART 3Mbaud" |
| 软约束（偏好/可权衡） | 团队偏好 / 时间 / 成本 / 风险容忍度 | "优先 C++，Python 仅脚本层" |
| 已有架构约束 | 现有代码结构 / 已有接口 / 部署方式 | "运动控制走 ROS 2 node，不可改" |

### ④ 架构设计

读 `references/architecture-design.md`（模块拆分原则 + C4 图约定 + 嵌入式/ML 专节 + 权衡分析框架）。

产出：
1. **C4 架构图**（Mermaid）：Context → Container → Component 三层
2. **模块职责表**：模块 / 职责 / 关键接口 / 依赖
3. **数据流图**（sequence diagram）：关键路径的端到端流
4. **技术选型与权衡**（Drawbacks-first）：先写每个选项的缺点，再写选择理由

### ⑤ 代码骨架

读 `references/code-scaffold.md`（接口优先 / 两层代码块 / TODO(#N) / 自检标准）。

代码块**内嵌在方案文档中**，不独立成文件。两层：

| 层 | 内容 | 要求 |
|----|------|------|
| 接口定义 | 类型、接口、函数签名 | 完整类型标注，无 `any`/`unknown`，无 stub |
| 关键路径伪代码 | 核心逻辑骨架 + `TODO(#N): 描述` | 逻辑流在，实现细节留 TODO |

### ⑥ 自检

文档内自洽性检查（不跑外部工具）：

- [ ] 架构图中的模块 ↔ 代码块中的接口/类名一致
- [ ] 同一接口在不同代码块中定义不矛盾
- [ ] 所有 `TODO(#N)` 有描述、编号无遗漏
- [ ] 类型引用有定义（至少在某个代码块中出现过）
- [ ] Goals 都有对应方案覆盖
- [ ] Non-Goals 没有被悄悄纳入
- [ ] 硬约束都满足或有明确缓解
- [ ] 代码块之间的调用关系与数据流图一致

## 方案文档结构

```markdown
# {项目名}：{一句话目标}

---
status: Draft           # Draft → Implementing → Done → Superseded
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## 问题定义
- 现状：{当前是什么}
- 目标：{要达到什么}
- 成功标准：{怎么算做成了，可观测}

## 约束
### 硬约束（不可妥协）
### 软约束（偏好 / 可权衡）

## Goals & Non-Goals
### Goals
- {可衡量的目标}
### Non-Goals
- {合理但排除的事项}

## 调研摘要
> 来源：research 发现块，附 V 等级

| 领域 | 关键发现 | 证据等级 | 来源 |
|------|----------|----------|------|

## 架构设计
### 模块划分
{C4 Container/Component 图}

### 模块职责
| 模块 | 职责 | 关键接口 | 依赖 |
|------|------|----------|------|

### 数据流
{sequence 图}

## 技术选型与权衡
| 决策点 | 候选 A | 候选 B | 选择 | 理由 |
|--------|--------|--------|------|------|
{Drawbacks-first：先写每个候选的缺点}

## 代码骨架
### 接口定义
{完整类型、接口、函数签名}

### 关键路径伪代码
{核心逻辑骨架 + TODO(#N)}

## 迁移 / 实施路径
1. {阶段 1：最小可运行} → 验证门
2. {阶段 2：核心功能} → 验证门
3. {阶段 3：完善}

## 风险与待定
- {已知风险 + 缓解}
- {未决问题 → 后续 research}

## Change Log
| 日期 | 变更 | 原因 |
|------|------|------|
```

## 产出落点

**默认**：项目目录（如 `proj/PROPOSAL.md`）。

**存库**：用户说"存库"时交 take-note，新增 `type: proposal`，归位 `项目-{名}/方案/`。方案体保留完整结构，不套笔记精简标准。

## 并行（可选优化）

架构设计阶段拆出独立模块可 ≤3 并行 agent。全局上限 5 agent；单 agent 失败重试 1 次。

## 长流程恢复

跨 session 时：读方案文档末尾 Change Log + 已完成阶段 → 从下一阶段继续。

## 参考文件（按需读，不全读）

| 文件 | 内容 | 适用 |
|------|------|------|
| `../shared/writing-core.md` | 铁律 / 原则 / V1-V4 / 失败模式 / 剪枝 / 校验工具 | 全部 |
| `references/architecture-design.md` | 模块拆分 / C4 图约定 / 嵌入式专节 / ML 部署专节 / 权衡分析 | ④ |
| `references/code-scaffold.md` | 接口优先 / 两层代码块 / TODO(#N) / 自检标准 | ⑤ |
