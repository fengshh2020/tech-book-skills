#!/usr/bin/env python3
"""Validate the local book skill pack structure and guardrails."""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ["translate-book", "integrate-books", "review-tech-book", "codebase-book"]
FORBIDDEN = [
    "含注释不翻",
    "本轮修复",
    "每轮修复后",
    "/tmp/epub_extract",
    "rm -rf .cache",
    "任何英文技术文档",
    "代码块与源文件逐字一致",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    global FAILED
    FAILED = True


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        fail(f"{path} missing YAML frontmatter")
        return {}
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        fail(f"{path} has unterminated YAML frontmatter")
        return {}
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def validate_skill_metadata() -> None:
    for skill in SKILLS:
        path = ROOT / skill / "SKILL.md"
        if not path.exists():
            fail(f"{path} missing")
            continue
        meta = parse_frontmatter(path)
        if meta.get("name") != skill:
            fail(f"{path} name must be {skill!r}")
        desc = meta.get("description", "")
        if not desc:
            fail(f"{path} missing description")
        if not desc.startswith("Use when"):
            fail(f"{path} description should start with 'Use when'")
        if len(desc) > 500:
            fail(f"{path} description too long: {len(desc)} chars")


def validate_skill_resource_links() -> None:
    resource_re = re.compile(r"\|\s*`([^`]+)`\s*\|")
    for skill in SKILLS:
        skill_dir = ROOT / skill
        skill_md = skill_dir / "SKILL.md"
        for match in resource_re.finditer(skill_md.read_text(encoding="utf-8")):
            rel = match.group(1)
            if not re.search(r"\.(md|sh|css|js)$", rel):
                continue
            target = (skill_dir / rel).resolve()
            if not target.exists():
                fail(f"{skill_md} references missing resource {rel}")


def validate_scripts() -> None:
    for script in sorted(ROOT.glob("*/scripts/*.sh")):
        result = subprocess.run(["bash", "-n", str(script)], text=True, capture_output=True)
        if result.returncode != 0:
            fail(f"{script} fails bash -n: {result.stderr.strip()}")


def validate_evals_json() -> None:
    path = ROOT / "evals" / "evals.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation script should show any parse issue
        fail(f"{path} invalid JSON: {exc}")
        return
    ids = [item.get("id") for item in data.get("evals", [])]
    if len(ids) != len(set(ids)):
        fail(f"{path} contains duplicate eval ids")
    for item in data.get("evals", []):
        if item.get("skill") not in SKILLS:
            fail(f"{path} eval {item.get('id')} has unknown skill {item.get('skill')}")


def validate_forbidden_phrases() -> None:
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir() or path.suffix not in {".md", ".json", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN:
            if phrase in text:
                if path.name == "evals.json" and phrase in {"rm -rf .cache"}:
                    continue
                fail(f"{path} contains forbidden phrase: {phrase}")


def validate_book_skill_contracts() -> None:
    shared = ROOT / "shared"
    compatibility_path = shared / "agent-compatibility.md"
    if not compatibility_path.exists():
        fail("shared/agent-compatibility.md must define agent-neutral path conventions")
    else:
        compatibility = compatibility_path.read_text(encoding="utf-8")
        for phrase in ("SKILL_DIR", "SKILL_PACK_DIR", "PROJECT_ROOT", "agents/openai.yaml"):
            if phrase not in compatibility:
                fail(f"agent-compatibility.md missing compatibility concept: {phrase}")

    quality_ownership_path = shared / "quality-ownership.md"
    if not quality_ownership_path.exists():
        fail("shared/quality-ownership.md must define non-overlapping book quality ownership")
        quality_ownership = ""
    else:
        quality_ownership = quality_ownership_path.read_text(encoding="utf-8")
        for phrase in ("一次做对", "系统性残留", "拼贴感", "模式化评分"):
            if phrase not in quality_ownership:
                fail(f"quality-ownership.md missing ownership concept: {phrase}")

    runtime_pruning_path = shared / "runtime-pruning.md"
    if not runtime_pruning_path.exists():
        fail("shared/runtime-pruning.md must define runtime pruning rules for long book skills")
        runtime_pruning = ""
    else:
        runtime_pruning = runtime_pruning_path.read_text(encoding="utf-8")
        for phrase in ("跳过条件", "停止条件", "范围分层", "按需读取"):
            if phrase not in runtime_pruning:
                fail(f"runtime-pruning.md missing pruning concept: {phrase}")

    progress = (shared / "progress-protocol.md").read_text(encoding="utf-8")
    for slug in ("translate", "integrate", "review", "codebase"):
        if f"{slug}:" not in progress:
            fail(f"progress-protocol.md missing run slug definition for {slug!r}")

    review_skill = (ROOT / "review-tech-book" / "SKILL.md").read_text(encoding="utf-8")
    translate_skill = (ROOT / "translate-book" / "SKILL.md").read_text(encoding="utf-8")
    integrate_skill = (ROOT / "integrate-books" / "SKILL.md").read_text(encoding="utf-8")
    for skill_name, skill_text in {
        "translate-book": translate_skill,
        "integrate-books": integrate_skill,
        "review-tech-book": review_skill,
        "codebase-book": (ROOT / "codebase-book" / "SKILL.md").read_text(encoding="utf-8"),
    }.items():
        if "../shared/agent-compatibility.md" not in skill_text:
            fail(f"{skill_name} must reference shared agent compatibility")
        if "SKILL_DIR" not in skill_text:
            fail(f"{skill_name} must use SKILL_DIR for local resource commands")
        if ".claude/skills/" in skill_text or "/home/" in skill_text:
            fail(f"{skill_name} must not hard-code platform-specific skill paths")
        if "../shared/quality-ownership.md" not in skill_text:
            fail(f"{skill_name} must reference shared quality ownership")
        if "../shared/runtime-pruning.md" not in skill_text:
            fail(f"{skill_name} must reference shared runtime pruning")
    if "*-codebase-*" not in review_skill:
        fail("review-tech-book must describe codebase-book report lookup")

    if "无标记也视为已完成" in translate_skill:
        fail("translate-book must not treat unmarked HTML as completed")
    if "unknown" not in translate_skill:
        fail("translate-book should define an unknown state for unmarked HTML")

    review_spec = (ROOT / "review-tech-book" / "references" / "spec.md").read_text(encoding="utf-8")
    for duplicate in ("| D1 | 读者旅程", "| D2 | 首次成功", "| D3 | 错误恢复", "| D4 | 参考可用性", "| D5 | 动机维持"):
        if duplicate in review_spec:
            fail("review-tech-book spec duplicates five transformation dimensions inside the sixteen dimensions")

    integration_discipline = (ROOT / "integrate-books" / "references" / "integration-discipline.md").read_text(encoding="utf-8")
    coverage_script = (ROOT / "integrate-books" / "scripts" / "check_coverage.sh").read_text(encoding="utf-8")
    evals = (ROOT / "evals" / "evals.json").read_text(encoding="utf-8")
    if "知识库条目映射率是否 ≥95%" not in integration_discipline:
        fail("integrate-books discipline must keep the 95% mapping gate")
    if "低于 95%" not in coverage_script:
        fail("check_coverage.sh must hard-fail stage5 mapping coverage below 95%")
    if "低于 95%" not in evals:
        fail("evals must expect the 95% stage5 mapping coverage gate")

    shared_patterns = (shared / "translationese-patterns.md").read_text(encoding="utf-8")
    review_validator = (ROOT / "review-tech-book" / "scripts" / "validate_code.sh").read_text(encoding="utf-8")
    patterns = []
    for line in shared_patterns.splitlines():
        match = re.match(r"^\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)", line)
        if match:
            patterns.append(match.group(2).strip())
    if not patterns:
        fail("shared translationese pattern table parsed no patterns")
    if "([^|]+?)" not in review_validator or "m.group(2).strip()" not in review_validator:
        fail("review-tech-book validate_code.sh must parse the shared translationese table format")

    reviewer_discipline = (ROOT / "review-tech-book" / "references" / "reviewer-discipline.md").read_text(encoding="utf-8")
    if "第三节的 5 个反模式" in reviewer_discipline:
        fail("reviewer-discipline must reference all 7 reviewer anti-patterns")

    if "目标读者假设" not in review_skill:
        fail("review-tech-book must capture target reader assumptions before scoring")
    if "学习路径图" not in review_skill:
        fail("review-tech-book must require a book-level learning path map")
    if "系统性残留" not in review_skill:
        fail("review-tech-book must distinguish systemic residual translation issues from translation QA")
    if "修复批次" not in review_skill:
        fail("review-tech-book report must include repair batches")
    if "拼贴感" not in review_skill:
        fail("review-tech-book must review integration style as reader-visible patchwork")
    if "模式化评分" not in review_skill:
        fail("review-tech-book must use mode-specific scoring to avoid redundant reports")
    if "深度模式" not in review_spec or "标准模式" not in review_spec or "快速模式" not in review_spec:
        fail("review-tech-book spec must define mode-specific report scope")
    if "补缺模式" not in translate_skill:
        fail("translate-book must define missing-chapter mode to skip unnecessary full-book setup")
    if "缩小的是修改范围，不是阅读范围" not in integrate_skill:
        fail("integrate-books quick mode must read all content to detect conflicts, only narrowing modification scope")
    codebase_skill = (ROOT / "codebase-book" / "SKILL.md").read_text(encoding="utf-8")
    if "范围分层" not in codebase_skill or "核心路径优先" not in codebase_skill:
        fail("codebase-book must avoid full-depth analysis for every file by using scope tiers")

    review_guardrails_path = ROOT / "review-tech-book" / "references" / "execution-guardrails.md"
    if not review_guardrails_path.exists():
        fail("review-tech-book must define execution guardrails for efficiency and LLM compliance")
        review_guardrails = ""
    else:
        review_guardrails = review_guardrails_path.read_text(encoding="utf-8")
        for phrase in ("模式锁定", "证据预算", "发现上限", "停止哨兵", "遵从清单"):
            if phrase not in review_guardrails:
                fail(f"execution-guardrails.md missing review guardrail: {phrase}")
    if "execution-guardrails.md" not in review_skill:
        fail("review-tech-book must reference execution guardrails")
    for phrase in ("模式锁定", "证据预算", "发现上限", "停止哨兵"):
        if phrase not in review_skill:
            fail(f"review-tech-book workflow must enforce {phrase}")
    if "真实检索任务" not in review_spec:
        fail("review-tech-book spec must define reference usability search tasks")
    if "练习" in review_spec:
        fail("review-tech-book spec must not add exercise-review requirements")
    if "反馈闭环" not in review_spec:
        fail("review-tech-book spec should use feedback-loop wording instead of exercise requirements")


def validate_openai_yaml() -> None:
    for skill in SKILLS:
        path = ROOT / skill / "agents" / "openai.yaml"
        if not path.exists():
            fail(f"{path} missing")
            continue
        text = path.read_text(encoding="utf-8")
        for field in ("display_name", "short_description", "default_prompt"):
            if field not in text:
                fail(f"{path} missing required field: {field}")


def validate_executable_bits() -> None:
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts:
            continue
        if path.is_dir():
            continue
        executable = bool(path.stat().st_mode & stat.S_IXUSR)
        should_execute = path.parent.name == "scripts" or path.name == "validate_skill_pack.py"
        if executable and not should_execute:
            fail(f"{path} should not be executable")
        if path.suffix == ".sh" and not executable:
            fail(f"{path} should be executable")


FAILED = False


def main() -> int:
    os.chdir(ROOT.parent.parent)
    validate_skill_metadata()
    validate_skill_resource_links()
    validate_scripts()
    validate_evals_json()
    validate_forbidden_phrases()
    validate_book_skill_contracts()
    validate_openai_yaml()
    validate_executable_bits()
    if FAILED:
        return 1
    print("OK: skill pack validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
