# ADR-0013: tech-proposal skill

**状态**：Accepted  
**日期**：2026-07-15  
**决策者**：用户 + Sisyphus（grill-with-docs session）

## 上下文

当前 skill 栈覆盖"生成书/文档"（generate-book）、"记录笔记"（take-note）、"审阅质量"（review-tech-book）、"调研问题"（research），但缺少一个关键能力：**从技术目标推演到可执行方案**。

典型场景：
- "宇树 GO2 加语音控制运动和跟踪"——需要调研 SDK、拆模块、定接口、写代码骨架
- "Thor 上部署 TRT 模型"——需要评估硬件约束、选转换路径、设计部署架构

当前 take-note 的 `type: plan` 只记录已有方案，不推演；generate-book 写长程叙事书，不产出方案+骨架；research 只调研不设计。

## 决策

### 1. 新建 `tech-proposal` skill

**不是修补现有 skill**——方案推演的流程、产出、纪律与现有 skill 都不同。

### 2. 产出形态

**方案文档 + 内嵌代码块**（不独立成 `src/` 目录）。代码块是文档的一部分，给人读不给编译器跑。

理由：避免 skill 膨胀；方案是设计沟通工具，不是可执行代码。

### 3. 流程主干

```
① 目标澄清（自适应：具体一轮确认，模糊多轮追问）
  → ② 调研（调 research + 读已有代码库）
  → ③ 约束提炼（含已有架构约束）
  → ④ 架构设计（增量或从零）
  → ⑤ 代码骨架（内嵌代码块）
  → ⑥ 自检（文档内自洽性）
```

模块间可并行 ≤3 agent。

### 4. 方案文档结构

整合 2026 最佳实践（Google Design Doc / Rust RFC / MADR / Living Proposal）：

```
问题定义 → 约束 → Goals & Non-Goals → 调研摘要 →
架构设计（C4 Mermaid）→ 技术选型与权衡（Drawbacks-first）→
代码骨架（接口定义 + 伪代码，TODO(#N)）→
迁移/实施路径（含验证门）→ 风险与待定 → Change Log
```

关键设计选择：
- **Goals / Non-Goals 分离**——Non-Goals 是"合理但排除的"，不是否定目标（Google Design Doc 实践）
- **C4 Mermaid 语法**——Context/Container/Component 三层，比纯 flowchart 更精确
- **Drawbacks-first**——先写每个选项的缺点再写选择理由（Rust RFC 实践）
- **代码块分两层**——接口定义（完整类型，无 any/unknown）+ 关键路径伪代码（TODO stub）
- **TODO(#N) 格式**——编号+描述，禁止 `// TODO: fix later`（Microsoft testfx / Ethereum Optimism 实践）
- **Living Proposal 生命周期**——Draft → Implementing → Done → Superseded，Change Log 追踪实现偏差

### 5. 依赖规则

| 依赖 | 安全？ | 原因 |
|------|--------|------|
| 自己的 skill 互调（research） | ✅ | 一定同时装 |
| `../shared/*` | ✅ | install.sh 一起链接 |
| 别人的 skill（codebase-design 等） | ❌ | 可能没装 |
| 插件/MCP | ❌ | agent 可能没配 |

架构设计原则**内嵌到 `references/architecture-design.md`**，不依赖 codebase-design skill。

### 6. 覆盖场景

- 从零设计新系统
- 已有系统+新需求（增量设计）
- 需求变更（调整设计）

### 7. 产出落点

默认项目目录（如 `proj/PROPOSAL.md`），用户说"存库"时交 take-note（新增 `type: proposal`）。目的地正交，跟 generate-book 一致。

### 8. review-tech-book 不扩展

方案文档由 tech-proposal 阶段⑥自检兜底，不扩展 review-tech-book 的审阅维度。

### 9. research 补完

research 从 12 行空壳扩展为完整 skill，新增 `references/output-contract.md`（Finding Block 规范）和 `references/search-craft.md`（查询分解策略）。tech-proposal 通过定向调研请求消费 Finding Block。

### 10. take-note 新增 `type: proposal`

与 `type: plan` 区分：`plan` 是已有方案的记录（笔记体），`proposal` 是 tech-proposal 产出的方案文档（方案体，保留完整结构）。归位 `项目-{名}/方案/`。

## 调研来源

- agentskills.io 开放标准（12+ 平台采纳，2026）
- Google Design Doc / Rust RFC / MADR 模板对比
- Vercel adr-skill（ADR as executable specification）
- Living Proposal 模式（DesignDoc / ai-sdlc / Tekk.coach）
- C4 Mermaid 语法（mermaid.js.org/syntax/c4.html）
- 嵌入式/机器人方案结构（Robotics Architecture Authority / Brain4Machinery）
- ML 部署方案结构（IoT Digital Twin PLM / NVIDIA TensorRT-Edge-LLM）
- Interface-First / Wave 0 模式（Neural Nexus / Luiz Parente）
- TODO(#N) 约定（Microsoft testfx / Ethereum Optimism / TODOsaurus）
- baft / archspec 图-代码一致性验证

## 后果

- 新增 1 个 skill（tech-proposal）+ 2 个 reference 文件
- research 补完（SKILL.md 扩展 + 2 个 reference）
- take-note 小改（新增 type: proposal）
- CONTEXT.md 新增术语
- install.sh 新增链接
