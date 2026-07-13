# 0006 — 泛化到任意技术栈 + 合并 reference 文件 + 修正 MD 源修复模式

承接 [ADR-0005](0005-trim-scaffolding-for-capable-models.md)（为强模型裁剪防御性脚手架）。本 ADR 记录三处进一步的结构性精简。

## 背景

0005 把纪律收敛到 `writing-core.md`、删了两份 `workflow.py`。但留下了三个问题：

1. **泛化不足**：`translation-rules.md` 的术语表、`quality-reference.md` 的标杆资源全是 Python，隐含"这些 skill 生成/审阅 Python 书"的假设。实际目标场景更广（用户库含 DDPM/TensorRT、机器狗语音、Jetson 部署，语言跨 Python/C++/shell）。
2. **reference 仍碎**：generate-book 有 9 个 reference，其中 `mode-single/multi/codebase` 三文件共享同一主干（读→写→验证→报告 + doc/book 分支 + 并行 + 报告）三份重述，各自独有的内容已在其深度参考里；review 有 5 个 reference，`excellence/teaching/quality` 三份重叠。
3. **MD 源修复模式未对齐**：`apply-fixes.md` 仍是 ADR-0001 之前的"手改 HTML"守则（检查 `<main>`/`<article>` 数量、移动章节重新编号清单），与"MD 是源、HTML 由 builder 渲染"矛盾——手改的 HTML 下次构建即被覆盖。
4. **过度工程的评分**：`spec.md` 五维度用加权公式 `C1×0.4+B4×0.3+D1×0.3` + 封顶规则；强模型能整体推理读者效果，精确权重是噪声。多源 G1-G13 门控表同理（0005 已说降级为自检，但表还在）。

## 决策

- **去 Python 中心化**：术语表标注"以 Python 为例，其它语言同理"；标杆资源改为"以目标语言官方文档为权威，换栈时替换"；十六维度/反模式/五转化维度本就语言无关。描述与触发短语补"any tech stack / 任意技术栈"。
- **合并 generate-book reference（9 → 4）**：共享主干（含 doc/book 形态、并行、报告、长流程恢复）上移到 `SKILL.md` 一次定义；删 `product-shapes.md`（形态表进 hub）、`mode-single/multi/codebase.md`（主干已在 hub，独有内容在各自深度参考）；`multi-read-architect.md` + `multi-synthesis.md` 合为 `multi-source.md`；`translation-rules.md` 压成 `translation.md`（删 HTML 结构陷阱——builder 负责、agent 只写 MD）。保留：`md-authoring.md`（builder 契约）、`writing-and-content.md`（叙事写作方法论）。
- **合并 review reference（5 → 3）**：`excellence-dimensions.md` + `teaching-reference.md` + `quality-reference.md` 合为 `review-criteria.md`；`spec.md` 删加权公式、保留十六维度 + 整合映射 + 质性封顶规则 + 报告模板。
- **修正修复模式**：`apply-fixes.md` 改为"改源 MD `{RUN}/src/*.md` → 重跑 `build_html.py` → 跑校验"；明确只有 HTML 无 src/ 的遗留产物无法干净修复，停下告知用户。
- **门控 → 自检**：多源 G1-G13 门控表与 multi-read-architect 失败模式表压成每阶段一处自检清单（落实 0005 的"Gate 退化为正文自检"）。

## 关键约束

- **builder 契约不动**：`md-authoring.md` 的组件映射（`book.yml` 键、`NN_*.md`、`> **[标签]**`、`caption=`、` ```mermaid `、图注）与 `build_html.py` 一致，是硬约束，本次只精简周边散文。
- **校验脚本耦合不动**：`validate_code.sh` 从 `shared/translationese-patterns.md` 读取正则列（含硬编码后备），该文件与表格式保持不变。
- **take-note 只轻剪**：归位/frontmatter/callout/双链是 Obsidian 库的硬约定（库 CLAUDE.md 指明"细节以 skill 为准"），只去重复述（"问用户"3 处合 1、Read-before-Write 2 处合 1），不动规则。
- **回退路径**：若某模式自检清单不够用，可在该深度参考里为高风险阶段重新加回显式 checklist，不必恢复整套门控。

## 收益

reference 文件数 −6（generate-book 9→4，review 5→3），正文总量约 −45%，且每个 skill 现在面向任意技术栈。强模型读 hub 即得完整流程主干，按输入轴加载一个深度参考即可开工。
