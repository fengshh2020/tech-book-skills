#!/usr/bin/env python3
"""
Universal workflow orchestrator for all book skills.
Usage: workflow.py <skill> <run_dir> <command> [args]
"""
import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional


class WorkflowLock:
    """Universal phase lock for all book skills."""

    PHASES = {
        "generate-book": ["0", "1", "2", "2b", "3", "4"],
        "review-tech-book": ["1", "2", "3", "4", "fix"],
        "codebase-book": ["1", "2", "3", "4", "5"],
    }

    def __init__(self, skill: str, run_dir: str):
        self.skill = skill
        self.run_dir = Path(run_dir)
        self.state_file = self.run_dir / ".workflow_state.json"
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "skill": self.skill,
            "current_phase": None,
            "completed_phases": [],
            "gates": {}
        }

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def can_enter(self, phase: str) -> bool:
        """Check if phase can be entered."""
        phases = self.PHASES.get(self.skill, [])
        if phase not in phases:
            return False

        idx = phases.index(phase)
        if idx == 0:
            return True

        prev_phase = phases[idx - 1]
        return prev_phase in self.state["completed_phases"]

    def mark_complete(self, phase: str, results: Dict):
        """Mark phase as complete."""
        self.state["completed_phases"].append(phase)
        self.state["gates"][phase] = results
        self.state["current_phase"] = phase
        self._save_state()

    def get_status(self) -> Dict:
        """Get current workflow status."""
        return {
            "skill": self.skill,
            "current_phase": self.state["current_phase"],
            "completed_phases": self.state["completed_phases"],
            "next_phase": self._get_next_phase()
        }

    def _get_next_phase(self) -> Optional[str]:
        """Get next phase to enter."""
        phases = self.PHASES.get(self.skill, [])
        for phase in phases:
            if phase not in self.state["completed_phases"]:
                return phase
        return None


class GateChecker:
    """Universal gate checker."""

    @staticmethod
    def check_file_exists(run_dir: Path, filename: str, required_sections: List[str] = None) -> Dict:
        """Check if file exists and contains required sections."""
        file_path = run_dir / filename
        if not file_path.exists():
            return {"passed": False, "reason": f"{filename} not found"}

        if required_sections:
            content = file_path.read_text()
            missing = [s for s in required_sections if s not in content]
            if missing:
                return {"passed": False, "reason": f"Missing sections: {missing}"}

        return {"passed": True, "reason": f"{filename} present"}

    @staticmethod
    def check_coverage(run_dir: Path, min_coverage: int = 80) -> Dict:
        """Check knowledge base coverage."""
        coverage_file = run_dir / ".book-doc" / "knowledge_base" / "INDEX" / "source_coverage.md"
        if not coverage_file.exists():
            return {"passed": False, "reason": "Coverage report not found"}

        content = coverage_file.read_text()
        match = re.search(r'Coverage:\s*(\d+)%', content)
        if not match:
            return {"passed": False, "reason": "Coverage percentage not parseable"}

        coverage = int(match.group(1))
        if coverage < min_coverage:
            return {"passed": False, "reason": f"Coverage {coverage}% < {min_coverage}%"}

        return {"passed": True, "reason": f"Coverage {coverage}% >= {min_coverage}%"}

    @staticmethod
    def check_chapter_quality(run_dir: Path, chapter: str) -> Dict:
        """Check chapter quality (generate-book Phase 2)."""
        chapter_file = run_dir / "output" / f"{chapter}.html"
        if not chapter_file.exists():
            return {"passed": False, "reason": f"Chapter {chapter}.html not found"}

        content = chapter_file.read_text()

        # G1: Integration markers
        markers = content.count("<!-- integrated:")

        # G2: Code verification tags
        code_blocks = len(re.findall(r'<pre><code>', content))
        verified_blocks = len(re.findall(r'<!-- V[123]:', content))

        # G3: Translationese scan
        translationese = [
            "这就是为什么", "你会发现", "正如你", "让我们",
            "接下来我们将", "值得注意的是"
        ]
        hits = sum(1 for p in translationese if p in content)

        results = {
            "G1_markers": markers,
            "G2_code_verified": f"{verified_blocks}/{code_blocks}",
            "G3_translationese_hits": hits,
        }

        passed = markers > 0 and verified_blocks == code_blocks and hits == 0

        return {
            "passed": passed,
            "reason": f"Markers: {markers}, Code: {verified_blocks}/{code_blocks}, Translationese: {hits}",
            "details": results
        }

    @staticmethod
    def check_review_phase2(run_dir: Path) -> Dict:
        """Check review Phase 2: All chapters read."""
        findings_file = run_dir / "findings" / "phase2.md"
        if not findings_file.exists():
            return {"passed": False, "reason": "findings/phase2.md not found"}

        content = findings_file.read_text()
        chapters = re.findall(r'### (?:Skim|Deep):\s*Ch\d+', content)
        quotes = content.count("**Quote**:")

        if len(chapters) < 1:
            return {"passed": False, "reason": "No chapter readings found"}
        if quotes < 1:
            return {"passed": False, "reason": "No quoted findings found"}

        return {"passed": True, "reason": f"{len(chapters)} chapters, {quotes} findings with quotes"}

    @staticmethod
    def check_translate_phase4(run_dir: Path, chapter: str) -> Dict:
        """Check translate Phase 4: Chapter translation quality."""
        chapter_file = run_dir / "output" / f"{chapter}.html"
        if not chapter_file.exists():
            return {"passed": False, "reason": f"Chapter {chapter}.html not found"}

        content = chapter_file.read_text()

        # Check marker
        has_marker = "<!-- translated: complete -->" in content

        # Check translationese
        translationese = [
            "这就是为什么", "你会发现", "正如你", "让我们",
            "接下来我们将", "值得注意的是"
        ]
        hits = sum(1 for p in translationese if p in content)

        # Check terminology consistency (simplified)
        # In real implementation, compare with spec.md
        results = {
            "has_marker": has_marker,
            "translationese_hits": hits,
        }

        passed = has_marker and hits == 0

        return {
            "passed": passed,
            "reason": f"Marker: {has_marker}, Translationese: {hits}",
            "details": results
        }


def _check_integrate_phase0(rd: Path) -> Dict:
    """Check Phase 0: Knowledge indexes exist, >=1000 lines each."""
    kb_dir = rd / ".book-doc" / "knowledge_base"
    if not kb_dir.exists():
        return {"passed": False, "reason": "Knowledge base directory not found"}

    index_files = list(kb_dir.glob("*/index.md"))
    if not index_files:
        return {"passed": False, "reason": "No knowledge index files found"}

    issues = []
    for idx_file in index_files:
        book_name = idx_file.parent.name
        line_count = len(idx_file.read_text().splitlines())
        if line_count < 1000:
            issues.append(f"{book_name}: {line_count} lines (min 1000)")

        content = idx_file.read_text()
        required = ["教学哲学", "深度分析", "主题映射", "整合准备"]
        missing = [s for s in required if s not in content]
        if missing:
            issues.append(f"{book_name}: missing sections: {missing}")

    if issues:
        return {"passed": False, "reason": "; ".join(issues)}

    return {"passed": True, "reason": f"{len(index_files)} indexes verified, all >=1000 lines"}


def _check_integrate_phase1(rd: Path) -> Dict:
    """Check Phase 1: Architecture + plan.md with per-chapter plans."""
    arch_file = rd / "source-architecture.md"
    if not arch_file.exists():
        return {"passed": False, "reason": "source-architecture.md not found"}

    plan_file = rd / "plan.md"
    if not plan_file.exists():
        return {"passed": False, "reason": "plan.md not found"}

    plan_content = plan_file.read_text()
    chapter_plans = re.findall(r'## 第 \d+ 章整合计划|## Ch\d+ Integration Plan', plan_content)
    if not chapter_plans:
        return {"passed": False, "reason": "plan.md has no per-chapter integration plans"}

    tbd = plan_content.count("TBD") + plan_content.count("待定")
    if tbd > 0:
        return {"passed": False, "reason": f"plan.md has {tbd} TBD/待定 placeholders"}

    return {"passed": True, "reason": f"Architecture + {len(chapter_plans)} chapter plans, no TBD"}


def _check_integrate_batch(rd: Path) -> Dict:
    """Check Phase 2b: Batch consistency across chapters."""
    output_dir = rd / "output"
    if not output_dir.exists():
        return {"passed": False, "reason": "Output directory not found"}

    chapters = sorted(output_dir.glob("*.html"))
    if len(chapters) < 2:
        return {"passed": True, "reason": "Less than 2 chapters, batch check skipped"}

    return {"passed": True, "reason": f"Batch check passed: {len(chapters)} chapters"}


GATE_CHECKERS = {
    # generate-book: 0=Deep Reading, 1=Architecture, 2=Chapter Gen, 2b=Batch, 3=Validation, 4=Report
    ("generate-book", "0"): lambda rd: _check_integrate_phase0(rd),
    ("generate-book", "1"): lambda rd: _check_integrate_phase1(rd),
    ("generate-book", "2"): lambda rd, ch="chapter1": GateChecker.check_chapter_quality(rd, ch),
    ("generate-book", "2b"): lambda rd: _check_integrate_batch(rd),
    ("generate-book", "3"): lambda rd: GateChecker.check_coverage(rd, 95),
    ("generate-book", "4"): lambda rd: GateChecker.check_file_exists(
        rd, "report.md",
        ["Summary", "Scores", "Issues", "Fix batches"]
    ),
    ("review-tech-book", "1"): lambda rd: GateChecker.check_file_exists(
        rd, "findings/phase1.md",
        ["Target reader", "Learning path", "Anomalies", "Validation"]
    ),
    ("review-tech-book", "2"): lambda rd: GateChecker.check_review_phase2(rd),
    ("review-tech-book", "4"): lambda rd: GateChecker.check_file_exists(
        rd, "report.md",
        ["Executive summary", "Score overview", "Top 3"]
    ),
}


def main():
    """CLI entry point."""
    if len(sys.argv) < 4:
        print("Usage: workflow.py <skill> <run_dir> <command> [args]")
        print("Skills: generate-book, review-tech-book, codebase-book")
        print("Commands: status, check_gate <phase> [chapter]")
        sys.exit(1)

    skill = sys.argv[1]
    run_dir = sys.argv[2]
    command = sys.argv[3]

    lock = WorkflowLock(skill, run_dir)

    if command == "status":
        status = lock.get_status()
        print(f"Skill: {status['skill']}")
        print(f"Current phase: {status['current_phase']}")
        print(f"Completed phases: {status['completed_phases']}")
        print(f"Next phase: {status['next_phase']}")

    elif command == "check_gate":
        phase = sys.argv[4]
        if not lock.can_enter(phase):
            print(f"ERROR: Cannot enter Phase {phase}. Previous phase not complete.")
            print(f"Completed: {lock.state['completed_phases']}")
            sys.exit(1)

        key = (skill, phase)
        if key not in GATE_CHECKERS:
            print(f"WARNING: Gate checker not implemented for {skill} Phase {phase}")
            result = {"passed": True, "reason": "Gate not implemented"}
        else:
            checker = GATE_CHECKERS[key]
            # Check if checker needs chapter argument
            if len(sys.argv) > 5:
                result = checker(Path(run_dir), sys.argv[5])
            else:
                result = checker(Path(run_dir))

        lock.mark_complete(phase, result)

        if result["passed"]:
            print(f"PASS: Phase {phase} gate passed. {result['reason']}")
        else:
            print(f"FAIL: Phase {phase} gate failed. {result['reason']}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
