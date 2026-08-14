---
name: tech-proposal
description: "Use when the user wants to design a technical solution — from a new system, a new feature, or a requirement change — producing a structured proposal document with embedded code scaffolds. Triggers: 设计方案, 技术方案, 怎么做, 怎么实现, 选型, 架构设计, design proposal, tech proposal, how to implement, architecture design, 需求变更方案, 新增功能设计, 加个功能, 改造方案. Do NOT trigger for: generating books/docs (use generate-book / translate-book), recording existing conclusions (use take-note), reviewing quality (use review-tech-book), pure research without design (use research)."
allowed-tools: Read Write Edit Glob Grep
---

# 技术方案推演

从技术目标推演到结构化方案文档 + 内嵌代码骨架——读起来像方案，不是拼贴画。覆盖从零设计新系统、已有系统新需求、需求变更三种场景。任意技术栈通用。

**先读 `../shared/writing-core.md`**（铁律——硬约束相关论断须官方文档 / 源码 / 实测确认，不接受推断）。

## 核心回路

**厘清目标 + Non-Goals → 提约束 → 架构（C4）+ Drawbacks-first 选型 → 接口骨架 + TODO(#N) → 自检图与代码一致**

🛑 **开跑对齐走 `../shared/kickoff.md`**，决策：目标与意图、场景（从零 / 增量 / 变更——影响调研深度与架构策略）、产出落点（项目目录 or 存库）。**模糊目标**（如"做一个嵌入式 AI 系统"）按 kickoff 分轮规则追问到未决清零：要解决什么问题？给谁用？目标硬件/平台？成功标准？时间约束？哪些事**不做**（Non-Goals 提前锁定）。

## 调研（调 research）

需要外部事实（库能力、硬件规格、兼容性）时发定向调研请求（格式见 `../research/references/search-craft.md`）。返回后检查：**Gaps 非空** → 标"待定"进风险区或追加一轮；**证据不够** → 降级软约束或标推断；**推翻假设** → 回到约束重新提炼。增量/变更场景另读现有代码找 seam、评估影响范围，每论断 `file:line`。

## 约束提炼

| 类型 | 来源 | 示例 |
|---|---|---|
| 硬约束（不可妥协） | 硬件 / SDK / 兼容性 / 实时性 / 法规 | "Jetson Orin 16GB VRAM"、"UART 3Mbaud" |
| 软约束（可权衡） | 团队偏好 / 时间 / 成本 / 风险容忍度 | "优先 C++，Python 仅脚本层" |
| 已有架构约束 | 现有代码结构 / 已有接口 / 部署方式 | "运动控制走 ROS 2 node，不可改" |

## 架构设计

读 `references/architecture-design.md`（模块拆分 + C4 图约定 + 嵌入式/ML 专节 + 权衡框架）。产出：① C4 架构图（Mermaid：Context → Container → Component）；② 模块职责表（模块 / 职责 / 关键接口 / 依赖）；③ 关键路径数据流（sequence）；④ 技术选型与权衡（**Drawbacks-first**：先写每个候选的缺点，再写选择理由）。

## 代码骨架

读 `references/code-scaffold.md`（接口优先 + 两层代码块 + TODO(#N)）。代码块**内嵌在方案文档中**，不独立成文件：第一层接口定义（完整类型标注，无 `any`/stub），第二层关键路径伪代码（逻辑骨架 + `TODO(#N): 描述`）。

## 自检（文档内自洽，不跑外部工具）

- [ ] 架构图模块 ↔ 代码块接口/类名一致；同一接口在不同代码块不矛盾
- [ ] 所有 `TODO(#N)` 有描述、编号无遗漏；类型引用有定义
- [ ] Goals 都有方案覆盖；Non-Goals 没被悄悄纳入
- [ ] 硬约束都满足或有明确缓解；代码块调用关系与数据流图一致

## 方案文档结构

```markdown
# {项目名}：{一句话目标}

---
status: Draft           # Draft → Implementing → Done → Superseded
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## 问题定义
- 现状 / 目标 / 成功标准（可观测）

## 约束
### 硬约束 / 软约束

## Goals & Non-Goals

## 调研摘要
> 来源：research Finding Block
| 领域 | 关键发现 | 来源 |

## 架构设计
### 模块划分（C4 Container/Component） / 模块职责表 / 数据流（sequence）

## 技术选型与权衡（Drawbacks-first）
| 决策点 | 候选 A | 候选 B | 选择 | 理由 |

## 代码骨架
### 接口定义 / 关键路径伪代码（TODO(#N)）

## 迁移 / 实施路径（每阶段带验证门）
## 风险与待定
## Change Log
```

## 产出落点

**默认**：项目目录（如 `proj/PROPOSAL.md`）。**存库**：用户说"存库"时交 take-note，新增 `type: proposal`，归位 `项目-{名}/方案/`（方案体保留完整结构，不套笔记精简标准）。跨 session 续作：读方案文档末尾 Change Log + 已完成部分继续。

## 参考文件（按需读，不全读）

| 文件 | 适用 |
|---|---|
| `../shared/writing-core.md` | 全部（先读） |
| `references/architecture-design.md` | 架构：模块拆分 / C4 / 嵌入式·ML 专节 / Drawbacks-first |
| `references/code-scaffold.md` | 代码骨架：接口优先 / 两层代码块 / TODO(#N) |
| `../shared/kickoff.md` | 开跑前 |
