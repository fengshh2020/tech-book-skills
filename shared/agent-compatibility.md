# Agent 兼容性约定

> 供所有 book skills 共享。目标是让 skill 可被不同 agent runtime 使用，而不依赖某个产品的目录名、工具名或调用方式。

## 路径变量

执行 skill 时先确定这些路径：

| 变量 | 含义 |
|------|------|
| `SKILL_DIR` | 当前 skill 目录，即包含本 `SKILL.md` 的目录 |
| `SKILL_PACK_DIR` | book skill 包根目录，即包含 `shared/` 和各 book skill 子目录的目录 |
| `PROJECT_ROOT` | 用户项目工作区根目录 |
| `RUN` | 当前 `.book-doc/runs/{id}/` 运行目录 |

如果 agent runtime 没有直接暴露 `SKILL_DIR`，从被加载的 `SKILL.md` 文件路径推断。所有 skill 内部资源路径默认相对于 `SKILL_DIR`；共享资源路径默认相对于 `SKILL_PACK_DIR/shared/`。

## 通用执行规则

- 不假设当前目录就是 skill 目录；命令必须显式使用 `SKILL_DIR` 或 `SKILL_PACK_DIR`。
- 不要求特定 agent 工具名。需要读文件、写文件、运行命令或并行处理时，用自然语言说明能力需求，由当前 runtime 映射到自己的工具。
- 不把产品专属 UI 元数据或平台特有路径作为执行依赖。安装位置可以是任意 skills 目录，只要相对资源结构保持不变。
- 并行工作是可选优化。只有当前 runtime 明确支持独立 worker/sub-agent，且任务写入范围不冲突时才使用；否则串行执行。

## 命令模板

在命令示例中使用变量：

```bash
"${SKILL_DIR}/scripts/validate_output.sh" output/
"${SKILL_PACK_DIR}/shared/validate_terms.py" output/
```

如果 shell 不支持这种变量形式，agent 应把变量替换为实际路径后执行。
