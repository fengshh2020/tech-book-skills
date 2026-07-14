# 0011 — KB 根解析与 portable：去硬编码 `/mnt/d/知识库`

承接 [0009](0009-llm-wiki-paradigm-via-take-note.md)（take-note 维护 wiki）。本 ADR 把 take-note 从「焊死在 `/mnt/d/知识库` 这一个 Obsidian 库」改成「在任何地方调用都能正确定位库根、生成结构」——把 **portable 结构逻辑** 与 **实例数据** 彻底分开。

## 背景

用户要求："在任何一个地方使用 skill，都能正确生成结构；当前只是借用了 Obsidian 的知识库目录。" 审查发现 take-note 三处不可移植：
- 库根硬编码 `/mnt/d/知识库`（description / 正文 / 输出示例 / 0009 / CONTEXT）。
- **实例项目名硬编码**：`SKILL.md` 把 `[[DDPM模型转换]]` / `[[机器狗语音控制]]` / `[[Jetson部署]]` 写死成"已知 hub"——换库即失效。
- 结构约定（`00_首页` / `文档库` / `项目-{名}` / `系统配置` / `wiki`）本是 portable 逻辑，却被和具体路径焊在一起。

对照：`generate-book`（写 `{RUN}/`）、`review-tech-book`（审给定路径）、`shared/writing-core.md`（资源相对 `SKILL_DIR`/`SKILL_PACK_DIR`）**本就 portable**。只有 take-note 被钉死。

## 决策

1. **`$KB_ROOT` 动态解析（git 式）**：从 cwd 向上逐级找标记——`.kb-root` 文件（显式）**或** `00_首页.md`（约定，零配置覆盖现有 Obsidian 库）。命中即根。
2. **找不到 → 问用户三选一**（不猜）：① 指定一个已有 KB 绝对路径；② 在 cwd **初始化新 KB**（建 `00_首页.md` + `文档库/` + `系统配置/` + `wiki/` 骨架）；③ 就地生成单篇（不建 KB）。
3. **覆盖**：环境变量 `KB_ROOT` 设了即用（CI / 固定库场景）。
4. **实例数据运行时发现**：项目名 / MOC 全部扫 `$KB_ROOT/项目-*/` 得，**不再硬编码**；`文档库/` 下每本书的 `00_MOC` 是书总目录、与项目 MOC 区分。
5. 所有 `/mnt/d/知识库` → `$KB_ROOT`（含 [0009] 的 `$KB_ROOT/wiki/`、CONTEXT 术语、take-note description / 正文 / 输出示例）。

## 关键约束

- **结构逻辑 portable、实例数据 discover**：约定（frontmatter / callout / 双链 / MOC / wiki 五操作）在任何 `$KB_ROOT` 下一致生成；具体项目名永远运行时扫，不进 skill 正文。
- **vault `CLAUDE.md` 仍是实例配置**（列真实项目、库规）——它在库内运行时提供额外上下文；skill 的扫描在任何地方都能工作。两者并存。
- 触发短语、writing-core、builder 契约等（0001–0010）全不动。
- `generate-book` / `review-tech-book` 已 portable，不改。

## 收益

- take-note 可装进任何 agent / 任何项目 / 任何机器，自动定位或初始化 KB，正确生成结构。
- 现有 Obsidian 库**零配置**识别（靠 `00_首页.md`）。
- 实例项目名不再腐烂在 skill 正文里。

## 回退路径

- 若标记发现误判（随机 `00_首页.md`）：优先认 `.kb-root` 显式标记，或在可疑目录问用户确认。
- 若发现机制不稳：`KB_ROOT` 环境变量硬指定（本 ADR 既定的覆盖路径）。
