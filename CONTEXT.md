# Tech Book Skills — 领域语言

术语边界索引：每条一句话界定，详情指向单一源文件（引用不重述）。任意技术栈通用。

**KB_ROOT（知识库根）**：take-note 写入的知识库根——动态解析、不硬编码（`.kb-root` 或 `00_首页.md` 向上找；`KB_ROOT` 环境变量覆盖；找不到问用户）。_Avoid_：把具体路径写进 skill（那是实例，不是逻辑）。

**Book Artifact（书籍产物）**：generate-book / translate-book 产出的独立技术书——HTML + MD 双格式，builder 驱动，不依赖库。_Avoid_：与 Vault Book 混为一谈。

**Vault Book（库内书）**：库内 Obsidian 原生书（`文档库/{书名}/` + `00_MOC` + 编号章节），由 take-note **book-ingest** 从 Book Artifact 的 `src/*.md` 适配；Obsidian 原生渲染、不走 builder、HTML 版交接时丢弃。_Avoid_：手改 HTML 进库。

**HTML Edition / MD Edition**：同一 MD 源的双格式渲染。MD 是**信息主源**（通用/GitHub 方言，无 frontmatter/双链/callout）；HTML 由 builder 渲染（"静奢"设计系统，light-only）。_Avoid_：网页版、site、Obsidian 版。

**Builder**：`shared/scripts/build_html.py`——MD 章节 + `book.yml` → HTML 输出目录；封面/目录/导航 chrome 由它注入，agent 不手写。_Avoid_：渲染器、generator。

**Source（源）/ Input（输入）**：输入材料决定 skill 路由——单源书 = 翻译（translate-book）；多源书 / 代码库 = 原创整合书（generate-book）；session = 笔记（take-note）。_Avoid_：让一个 skill 装两种源的心智模型。

**Product Shape（产品形态）**：与源类型**正交**的产出维度——`book`（全书，builder 双格式）/ `doc`（就地单文件，无 builder）/ `note`（原子结论，take-note 产）。_Avoid_：把"源类型"和"产品形态"焊死。

**Diagram（图表）**：原创内容的可视化优先媒介，格式标准 **SVG**（手写 `src/diagrams/*.svg` 首选，mermaid 为兼容路径）；证据 `file:line` 写图注。Vault Book 与 tech-proposal 的 C4 走 Obsidian/GitHub 原生 mermaid，不经 builder。_Avoid_：PNG、drawio；把图当文字的复述。

**讲解质量三标准 / 反冗余红线 / 铁律 / 反 AI 腔 / 校验套件**：见 `shared/writing-core.md`（唯一纪律源）——各 skill 只引用、不重述。

**Book Project（曳光弹 / 滚动构建 / progress.md / 修复操作）**：见 `shared/book-project.md`（工作区与生命周期契约）。

**Kickoff（开跑对齐）**：见 `shared/kickoff.md`——事实自己查绝不问用户；决策才问、每问带推荐；一轮问完。

**Finding Block（发现块）**：research 的标准输出契约——`Answer`（1-3 句）+ `Evidence`（论断 + 类型[实测/源码/文档/推断] + 具体来源）+ `Gaps` + `Meta`（来源数/置信度/需升级）。规范在 `research/SKILL.md`。_Avoid_：自由格式散文输出（不可组合）。

**Escalation（升级边界）**：research 最多 3 轮迭代耗尽仍有 Gaps → 交付部分答案 + `需升级: yes`，不伪造不扣留。_Avoid_：硬凑轮次；把"没查到"当失败而掩饰。

**Wiki（可复利知识库）**：`$KB_ROOT/wiki/`——`raw/`（不可变源，人策展）→ 编译 concept/entity 页（LLM 写）+ `index.md` + `log.md`；五操作 INGEST/COMPILE/INDEX/QUERY/LINT，take-note 维护（opt-in）。见 `take-note/references/llm-wiki.md`。_Avoid_：手写 wiki 页；与项目笔记混为一谈。

**Tech Proposal（技术方案推演）**：从目标推演到方案文档 + 内嵌代码骨架（不独立成文件）；默认落项目目录，"存库"时交 take-note `type: proposal`（方案体不套笔记精简标准）。_Avoid_：当 generate-book 的子集；把方案文档当笔记。
