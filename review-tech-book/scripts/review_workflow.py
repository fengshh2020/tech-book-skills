#!/usr/bin/env python3
"""
Workflow orchestrator for review-tech-book skill.
Ensures phases execute in order, gates pass before proceeding.
"""
import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional


class ReviewPhaseLock:
    """Ensures review phases execute in order."""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.state_file = self.run_dir / ".review_state.json"
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "current_phase": None,
            "completed_phases": [],
            "findings": {},
            "scores": {}
        }

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def can_enter(self, phase: str) -> bool:
        """Check if phase can be entered."""
        phase_order = ["1", "2", "3", "4", "fix"]
        if phase not in phase_order:
            return False

        idx = phase_order.index(phase)
        if idx == 0:
            return True

        prev_phase = phase_order[idx - 1]
        return prev_phase in self.state["completed_phases"]

    def mark_complete(self, phase: str, results: Dict):
        """Mark phase as complete."""
        self.state["completed_phases"].append(phase)
        self.state["current_phase"] = phase
        if "findings" in results:
            self.state["findings"][phase] = results["findings"]
        if "scores" in results:
            self.state["scores"][phase] = results["scores"]
        self._save_state()


def check_phase1_gate(run_dir: str) -> Dict:
    """Check Phase 1 gate: Scan complete."""
    findings_file = Path(run_dir) / "findings" / "phase1.md"
    if not findings_file.exists():
        return {"passed": False, "reason": "findings/phase1.md not found"}

    content = findings_file.read_text()

    # Check required sections
    required = ["Target reader", "Learning path", "Anomalies", "Validation"]
    missing = [r for r in required if r not in content]
    if missing:
        return {"passed": False, "reason": f"Missing sections: {missing}"}

    return {"passed": True, "reason": "All required sections present"}


def check_phase2_gate(run_dir: str) -> Dict:
    """Check Phase 2 gate: All chapters read."""
    findings_file = Path(run_dir) / "findings" / "phase2.md"
    if not findings_file.exists():
        return {"passed": False, "reason": "findings/phase2.md not found"}

    content = findings_file.read_text()

    # Count chapters with evidence
    chapters = re.findall(r'### (?:Skim|Deep):\s*Ch\d+', content)
    if len(chapters) < 1:
        return {"passed": False, "reason": "No chapter readings found"}

    # Check for quotes
    quotes = content.count("**Quote**:")
    if quotes < 1:
        return {"passed": False, "reason": "No quoted findings found"}

    return {"passed": True, "reason": f"{len(chapters)} chapters read, {quotes} findings with quotes"}


def check_phase4_gate(run_dir: str) -> Dict:
    """Check Phase 4 gate: Report complete."""
    report_file = Path(run_dir) / "report.md"
    if not report_file.exists():
        return {"passed": False, "reason": "report.md not found"}

    content = report_file.read_text()

    # Check required sections
    required = ["Executive summary", "Score overview", "Top 3", "Learning path"]
    missing = [r for r in required if r not in content]
    if missing:
        return {"passed": False, "reason": f"Missing sections: {missing}"}

    return {"passed": True, "reason": "All required sections present"}


def check_fix_gate(run_dir: str) -> Dict:
    """Check Fix mode gate: All batches applied."""
    fix_report = Path(run_dir) / "fix-report.md"
    if not fix_report.exists():
        return {"passed": False, "reason": "fix-report.md not found"}

    content = fix_report.read_text()

    # Check for batch completion
    batches = ["P0", "P1", "P2", "P3"]
    completed = [b for b in batches if f"{b} complete" in content]

    if len(completed) < 4:
        return {"passed": False, "reason": f"Only {len(completed)}/4 batches completed"}

    return {"passed": True, "reason": "All 4 batches completed"}


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: review_workflow.py <run_dir> <command> [args]")
        print("Commands: status, check_gate <phase>")
        sys.exit(1)

    run_dir = sys.argv[1]
    command = sys.argv[2]

    lock = ReviewPhaseLock(run_dir)

    if command == "status":
        print(f"Current phase: {lock.state['current_phase']}")
        print(f"Completed phases: {lock.state['completed_phases']}")

    elif command == "check_gate":
        phase = sys.argv[3]
        if not lock.can_enter(phase):
            print(f"ERROR: Cannot enter Phase {phase}. Previous phase not complete.")
            sys.exit(1)

        if phase == "1":
            result = check_phase1_gate(run_dir)
        elif phase == "2":
            result = check_phase2_gate(run_dir)
        elif phase == "4":
            result = check_phase4_gate(run_dir)
        elif phase == "fix":
            result = check_fix_gate(run_dir)
        else:
            result = {"passed": True, "reason": "Gate not implemented"}

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
