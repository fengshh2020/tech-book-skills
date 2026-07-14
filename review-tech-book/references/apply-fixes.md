# 审阅后修复模式

仅在用户明确要求"修复 / 优化 / 应用改进"时使用。审阅默认仍只报告。

## 触发与边界

- 触发词：`优化所有问题`、`修复这些问题`、`apply fixes`、`按报告修复`。
- 输入：最新 `report.md` → `findings/phase2.md` → 源。
- 不重开完整审阅，只实现报告中的修复批次。发现新风险记到 `fix-report.md`，不扩张范围。
- 翻译/整合/代码库问题按**类别批量处理**，不逐点微修补。

## MD 是源

**修复改的是源 MD（`{RUN}/src/*.md`），不是 `output/*.html`**——HTML 由 builder 渲染，手改 HTML 会在下次构建被覆盖。

```
改 {RUN}/src/*.md  →  python ../generate-book/scripts/build_html.py {RUN}/src {RUN}/output  →  重跑校验
```

若被审阅的书**只有 HTML、无 `src/`**（遗留产物），停下告知用户：无法干净修复 HTML-only 输出，建议从源重建。

doc 形态产物（就地 MD，无 builder）：直接改那份 MD，无需重建。

## 执行顺序（每批后跑校验，失败先修再进下一批）

1. **P0 技术错误**：版本标注、API 说明、不可运行代码、断链、编号错误。
2. **P1 学习路径与结构**：章节拆分/合并、标题去重、交叉引用、导航更新（改 MD 后 builder 重生成目录/导航，验证 0 断链）。
3. **P2 风格与系统性残留**：翻译腔、术语残留、格式一致。
4. **P3 参考体验**：练习、自测、速查表、索引、实践项目。

```bash
generate-book/scripts/validate_output.sh output/
review-tech-book/scripts/validate_code.sh output/
python ../shared/validate_tech.py output/; python ../shared/validate_terms.py output/
```

## 修复报告

写入当前 review run 的 `fix-report.md`：

```markdown
# 修复报告
## 修复批次
| 批次 | 已修复 | 改的源文件 | 验证 |
## 验证结果
- validate_code.sh / validate_tech / validate_terms：
- 代码实机验证（至少 1 个新增/改动示例 V1）：
- 残余风险：
```

## 完成关卡

- [ ] 每个报告问题有对应修复或明确保留理由
- [ ] 改的是源 MD 并已重新构建（非手改 HTML）；0 断链
- [ ] 翻译腔和术语扫描通过；代码清单编号连续
- [ ] 至少一个新增/改动代码示例做 V1 实机验证
