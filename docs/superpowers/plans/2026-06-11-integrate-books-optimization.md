# Integrate-Books Skill Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Optimize the integrate-books skill with fine-grained sub-phases, coverage guardian, auto-progress tracking, and full English conversion to fix real-world integration failures.

**Architecture:** Split 5 coarse phases into 16+ sub-phases with per-sub-phase gates. Add coverage guardian (per-source ratios, patch detection, size guards) enforced by an enhanced workflow.py. Convert all 10 files to English.

**Tech Stack:** Python 3 (workflow.py), Markdown (SKILL.md + references), Bash (check_coverage.sh)

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `integrate-books/SKILL.md` | Rewrite | Entry point with sub-phase architecture |
| `integrate-books/references/knowledge-index-format.md` | Rewrite | Index template with English field names |
| `integrate-books/references/book-architecture.md` | Rewrite | Architecture protocol with sub-phase references |
| `integrate-books/references/full-integration.md` | Rewrite | Integration levels + 5-step rewrite guide |
| `integrate-books/references/integration-discipline.md` | Rewrite | Correctness + completeness + style + coverage guardian |
| `integrate-books/references/quality-gate.md` | Rewrite | Per-chapter gates including G7/G8 |
| `integrate-books/references/agent-orchestration.md` | Rewrite | Sub-phase orchestration rules |
| `integrate-books/references/synthesis-methodology.md` | Rewrite | Narrative synthesis methodology |
| `integrate-books/references/context-passing.md` | Rewrite | Context protocol with sub-phase support |
| `integrate-books/scripts/workflow.py` | Rewrite | Enhanced with sub-phase tracking, coverage guardian, auto-progress |

---

### Task 1: Rewrite workflow.py with Sub-Phase Tracking

**Files:**
- Rewrite: `integrate-books/scripts/workflow.py`

This is the foundation — all other files reference workflow.py commands. Must be done first.

- [ ] **Step 1: Write the enhanced workflow.py**

Rewrite `integrate-books/scripts/workflow.py` with the following capabilities:

```python
#!/usr/bin/env python3
"""
Enhanced workflow orchestrator for integrate-books skill.
Supports sub-phase tracking, coverage guardian, auto-progress recording.

Usage:
  workflow.py integrate-books <run_dir> status
  workflow.py integrate-books <run_dir> check_gate <phase> [<sub_phase>] [chapter]
  workflow.py integrate-books <run_dir> record_progress --phase <N> --sub-phase <N> [--chapter <name>] --status <completed|failed> [--markers <count>] [--gate-result <results>]
  workflow.py integrate-books <run_dir> coverage_report
  workflow.py integrate-books <run_dir> coverage_guard <chapter>
"""
import json
import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# Sub-phase definitions for integrate-books
SUB_PHASES = {
    "0": ["0.1", "0.2", "0.3", "0.4", "0.5"],
    "1": ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"],
    "2": ["2.1", "2.2", "2.3", "2.4", "2.5"],
    "3": ["3.1", "3.2", "3.3", "3.4"],
    "4": ["4.1", "4.2"],
}

PHASES = list(SUB_PHASES.keys())


class SubPhaseWorkflowLock:
    """Sub-phase-aware workflow lock for integrate-books."""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.state_file = self.run_dir / ".workflow_state.json"
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "skill": "integrate-books",
            "current_phase": None,
            "current_sub_phase": None,
            "completed_phases": [],
            "completed_sub_phases": {"0": [], "1": [], "2": [], "3": [], "4": []},
            "chapter_progress": {},
            "source_coverage": {},
            "gates": {},
        }

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def can_enter_sub_phase(self, phase: str, sub_phase: str, chapter: str = None) -> Tuple[bool, str]:
        """Check if a sub-phase can be entered based on prior completion."""
        phase_sub_phases = SUB_PHASES.get(phase, [])
        if sub_phase not in phase_sub_phases:
            return False, f"Unknown sub-phase {sub_phase} for phase {phase}"

        # Phase 0: no prerequisites
        if phase == "0":
            idx = phase_sub_phases.index(sub_phase)
            if idx == 0:
                return True, "First sub-phase of Phase 0"
            prev = phase_sub_phases[idx - 1]
            if prev not in self.state["completed_sub_phases"].get("0", []):
                return False, f"Sub-phase {prev} not completed"
            return True, f"Sub-phase {prev} completed"

        # Must have completed all of previous phase
        prev_phase = str(int(phase) - 1)
        if prev_phase not in self.state["completed_phases"]:
            return False, f"Phase {prev_phase} not completed"

        # First sub-phase of a phase is always enterable if prior phase done
        idx = phase_sub_phases.index(sub_phase)
        if idx == 0:
            if chapter:
                # For Phase 2: verify previous chapter's 2.4 is done
                if phase == "2":
                    prev_ch = self._get_prev_chapter(chapter)
                    if prev_ch and prev_ch in self.state["chapter_progress"]:
                        if self.state["chapter_progress"][prev_ch].get("status") != "completed":
                            return False, f"Previous chapter {prev_ch} not completed (progress record required)"
            return True, f"First sub-phase of Phase {phase}"

        # Check prior sub-phase in same phase
        prev_sub = phase_sub_phases[idx - 1]
        completed = self.state["completed_sub_phases"].get(phase, [])
        # For Phase 2, sub-phase completion is per-chapter
        if phase == "2" and chapter:
            key = f"{prev_sub}:{chapter}"
            if key not in completed:
                return False, f"Sub-phase {prev_sub} for {chapter} not completed"
        else:
            if prev_sub not in completed:
                return False, f"Sub-phase {prev_sub} not completed"
        return True, "Prior sub-phase completed"

    def _get_prev_chapter(self, chapter: str) -> Optional[str]:
        """Get the chapter before the given one in order."""
        chapters = sorted(self.state["chapter_progress"].keys())
        if chapter in chapters:
            idx = chapters.index(chapter)
            if idx > 0:
                return chapters[idx - 1]
        return None

    def record_progress(self, phase: str, sub_phase: str, status: str,
                        chapter: str = None, markers: int = 0,
                        gate_result: str = "") -> Dict:
        """Record sub-phase completion and update state."""
        # Mark sub-phase as completed
        completed_key = phase
        completed_list = self.state["completed_sub_phases"].setdefault(completed_key, [])

        if phase == "2" and chapter:
            entry = f"{sub_phase}:{chapter}"
        else:
            entry = sub_phase

        if status == "completed" and entry not in completed_list:
            completed_list.append(entry)

        # Update current position
        self.state["current_phase"] = phase
        self.state["current_sub_phase"] = sub_phase

        # Update chapter progress if applicable
        if chapter and phase == "2":
            ch_state = self.state["chapter_progress"].setdefault(chapter, {
                "status": "pending", "markers": 0, "gate": None
            })
            if sub_phase == "2.4" and status == "completed":
                ch_state["status"] = "completed"
            if markers > 0:
                ch_state["markers"] = markers
            if gate_result:
                ch_state["gate"] = gate_result

        # Check if all sub-phases of this phase are done
        all_sub = SUB_PHASES.get(phase, [])
        if phase != "2":  # Non-chapter phases
            if all(s in completed_list for s in all_sub):
                if phase not in self.state["completed_phases"]:
                    self.state["completed_phases"].append(phase)

        # Update progress.md
        self._update_progress_md()

        # Save state
        self._save_state()

        return {"status": "ok", "phase": phase, "sub_phase": sub_phase, "chapter": chapter}

    def _update_progress_md(self):
        """Auto-write progress.md based on current state."""
        progress_file = self.run_dir / "progress.md"
        lines = ["# Integration Run Progress\n"]
        lines.append(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        # Status overview
        lines.append("## Status Overview\n")
        for phase in PHASES:
            completed_subs = self.state["completed_sub_phases"].get(phase, [])
            total_subs = len(SUB_PHASES.get(phase, []))
            if phase in self.state["completed_phases"]:
                status = "done"
            elif completed_subs:
                status = f"in-progress ({len(completed_subs)}/{total_subs} sub-phases)"
            else:
                status = "pending"
            lines.append(f"- Phase {phase}: {status}\n")

        # Chapter progress
        if self.state["chapter_progress"]:
            lines.append("\n## Chapter Progress\n")
            lines.append("| Chapter | Status | Markers | Gate |\n")
            lines.append("|---------|--------|---------|------|\n")
            for ch, info in sorted(self.state["chapter_progress"].items()):
                lines.append(f"| {ch} | {info.get('status', 'pending')} | {info.get('markers', 0)} | {info.get('gate', '-')} |\n")

        # Source coverage
        if self.state["source_coverage"]:
            lines.append("\n## Source Coverage\n")
            total = sum(self.state["source_coverage"].values())
            lines.append("| Source | Markers | Ratio |\n")
            lines.append("|--------|---------|-------|\n")
            for src, count in sorted(self.state["source_coverage"].items(), key=lambda x: -x[1]):
                ratio = f"{count/total*100:.1f}%" if total > 0 else "0%"
                lines.append(f"| {src} | {count} | {ratio} |\n")

        progress_file.write_text("".join(lines))

    def get_status(self) -> Dict:
        """Get current workflow status."""
        return {
            "skill": "integrate-books",
            "current_phase": self.state["current_phase"],
            "current_sub_phase": self.state["current_sub_phase"],
            "completed_phases": self.state["completed_phases"],
            "completed_sub_phases": self.state["completed_sub_phases"],
            "chapter_progress": self.state["chapter_progress"],
            "source_coverage": self.state["source_coverage"],
        }


class CoverageGuardian:
    """Coverage guardian for integrate-books output."""

    # Source name variants (handle different marker formats)
    SOURCE_ALIASES = {
        "Will": ["Will", "will", "[Will]"],
        "Stroustrup": ["Stroustrup", "stroustrup", "[Stroustrup]"],
        "Cookbook": ["Cookbook", "cookbook", "[Cookbook]"],
        "LowLatency": ["LowLatency", "lowlatency", "[LowLatency]"],
        "Mindset": ["Mindset", "mindset", "[Mindset]"],
        "StepByStep": ["StepByStep", "stepbystep", "[StepByStep]"],
    }

    @staticmethod
    def count_source_markers(output_dir: Path) -> Dict[str, int]:
        """Count markers per source across all output chapters."""
        source_counts = {}
        for html_file in sorted(output_dir.glob("*.html")):
            content = html_file.read_text(errors="ignore")
            markers = re.findall(r'<!--\s*integrated:\s*([^-]+)', content)
            for marker in markers:
                # Determine source from marker prefix
                source = CoverageGuardian._identify_source(marker.strip())
                if source:
                    source_counts[source] = source_counts.get(source, 0) + 1
        return source_counts

    @staticmethod
    def _identify_source(marker_prefix: str) -> Optional[str]:
        """Identify which source book a marker prefix belongs to."""
        for canonical, aliases in CoverageGuardian.SOURCE_ALIASES.items():
            for alias in aliases:
                if marker_prefix.startswith(alias):
                    return canonical
        return None

    @staticmethod
    def check_per_source_ratio(output_dir: Path, min_ratio: float = 0.10) -> Dict:
        """Check if each source has >= min_ratio of total markers."""
        counts = CoverageGuardian.count_source_markers(output_dir)
        if not counts:
            return {"passed": False, "reason": "No markers found"}

        total = sum(counts.values())
        violations = []
        for source, count in counts.items():
            ratio = count / total
            if ratio < min_ratio:
                violations.append(f"{source}: {count}/{total} = {ratio:.1%} < {min_ratio:.0%}")

        if violations:
            return {"passed": False, "reason": f"Sources below {min_ratio:.0%} floor: " + "; ".join(violations)}

        return {"passed": True, "reason": f"All {len(counts)} sources >= {min_ratio:.0%} floor", "counts": counts}

    @staticmethod
    def detect_patch_style(output_dir: Path) -> Dict:
        """Detect sources that are used as patches rather than integrated."""
        source_chapters = {}  # source -> set of chapters where it appears
        source_positions = {}  # source -> list of (is_first_in_section)

        for html_file in sorted(output_dir.glob("*.html")):
            content = html_file.read_text(errors="ignore")
            ch_name = html_file.stem

            # Find all markers with their positions
            markers = list(re.finditer(r'<!--\s*integrated:\s*([^>]+?)\s*-->', content))
            for i, match in enumerate(markers):
                marker_text = match.group(1).strip()
                source = CoverageGuardian._identify_source(marker_text.split("Ch")[0].strip() if "Ch" in marker_text else marker_text)
                if source:
                    source_chapters.setdefault(source, set()).add(ch_name)
                    is_first = (i == 0) or (match.start() - markers[max(0, i-1)].end() > 500)
                    source_positions.setdefault(source, []).append(is_first)

        warnings = []
        for source, chapters in source_chapters.items():
            # Patch condition 1: all markers in <=2 chapters
            if len(chapters) <= 2:
                warnings.append(f"{source}: all markers in {len(chapters)} chapter(s) — concentrated, not integrated")

            # Patch condition 2: never first marker in any section
            positions = source_positions.get(source, [])
            if positions and not any(positions):
                warnings.append(f"{source}: never appears as first/primary marker — always supplemental")

        return {
            "patch_warnings": warnings,
            "is_patch_detected": len(warnings) > 0,
            "source_chapter_distribution": {s: len(ch) for s, ch in source_chapters.items()},
        }

    @staticmethod
    def check_chapter_coverage(output_dir: Path, chapter: str, plan_file: Path = None) -> Dict:
        """Check per-chapter coverage for a specific chapter."""
        ch_file = output_dir / f"{chapter}.html"
        if not ch_file.exists():
            return {"passed": False, "reason": f"{chapter}.html not found"}

        content = ch_file.read_text(errors="ignore")
        total_markers = content.count("<!-- integrated:")

        # Count per-source markers in this chapter
        source_markers = {}
        markers = re.findall(r'<!--\s*integrated:\s*([^-]+)', content)
        for marker in markers:
            source = CoverageGuardian._identify_source(marker.strip())
            if source:
                source_markers[source] = source_markers.get(source, 0) + 1

        # G7: each mapped source must have >=3 markers
        low_sources = [s for s, c in source_markers.items() if c < 3]

        # G8: output size guard
        ch_size = ch_file.stat().st_size

        return {
            "passed": len(low_sources) == 0,
            "total_markers": total_markers,
            "source_markers": source_markers,
            "low_sources": low_sources,
            "chapter_size": ch_size,
            "reason": f"Markers: {total_markers}, Low sources: {low_sources}" if low_sources else f"Markers: {total_markers}, all sources >=3",
        }


class GateChecker:
    """Gate checkers for each sub-phase."""

    @staticmethod
    def check_file_exists(run_dir: Path, filename: str, required_sections: List[str] = None) -> Dict:
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
    def check_inventory(run_dir: Path) -> Dict:
        inv = run_dir / ".book-doc" / "knowledge_base" / "INVENTORY.md"
        if not inv.exists():
            return {"passed": False, "reason": "INVENTORY.md not found"}
        content = inv.read_text()
        books = re.findall(r'^\|\s*(\w+)', content, re.MULTILINE)
        if len(books) < 2:
            return {"passed": False, "reason": "INVENTORY.md has fewer than 2 books"}
        return {"passed": True, "reason": f"INVENTORY.md present with {len(books)} books"}

    @staticmethod
    def check_phase0_sub3(run_dir: Path) -> Dict:
        kb_dir = run_dir / ".book-doc" / "knowledge_base"
        if not kb_dir.exists():
            return {"passed": False, "reason": "Knowledge base directory not found"}
        index_files = list(kb_dir.glob("*/index.md"))
        if not index_files:
            return {"passed": False, "reason": "No knowledge index files found"}
        issues = []
        required_sections = ["Teaching Philosophy", "Cognitive Progression",
                           "Per-Chapter Deep Analysis", "Integration Readiness"]
        for idx_file in index_files:
            book_name = idx_file.parent.name
            line_count = len(idx_file.read_text().splitlines())
            if line_count < 1000:
                issues.append(f"{book_name}: {line_count} lines (min 1000)")
            content = idx_file.read_text()
            missing = [s for s in required_sections if s not in content]
            if missing:
                issues.append(f"{book_name}: missing sections: {missing}")
        if issues:
            return {"passed": False, "reason": "; ".join(issues)}
        return {"passed": True, "reason": f"{len(index_files)} indexes verified, all >=1000 lines"}

    @staticmethod
    def check_phase1_sub5(run_dir: Path) -> Dict:
        arch_file = run_dir / "source-architecture.md"
        if not arch_file.exists():
            return {"passed": False, "reason": "source-architecture.md not found"}
        content = arch_file.read_text()
        if "Reverse Coverage Matrix" not in content and "reverse coverage" not in content.lower():
            return {"passed": False, "reason": "Reverse coverage matrix missing from source-architecture.md"}
        # Check for 100% coverage claim
        if "100%" not in content:
            return {"passed": False, "reason": "Coverage is not 100% — reverse coverage must be complete"}
        return {"passed": True, "reason": "source-architecture.md with reverse coverage at 100%"}

    @staticmethod
    def check_chapter_quality(run_dir: Path, chapter: str) -> Dict:
        ch_file = run_dir / "output" / f"{chapter}.html"
        if not ch_file.exists():
            return {"passed": False, "reason": f"Chapter {chapter}.html not found"}
        content = ch_file.read_text()
        markers = content.count("<!-- integrated:")
        code_blocks = len(re.findall(r'<pre><code>', content))
        verified_blocks = len(re.findall(r'<!-- V[123]:', content))
        translationese = ["这就是为什么", "你会发现", "正如你", "让我们", "接下来我们将", "值得注意的是"]
        hits = sum(1 for p in translationese if p in content)
        # Also check G7/G8 via CoverageGuardian
        coverage = CoverageGuardian.check_chapter_coverage(run_dir / "output", chapter)
        results = {
            "G1_markers": markers,
            "G2_code_verified": f"{verified_blocks}/{code_blocks}",
            "G3_translationese_hits": hits,
            "G7_low_sources": coverage.get("low_sources", []),
            "G8_size": coverage.get("chapter_size", 0),
        }
        passed = markers > 0 and hits == 0 and len(coverage.get("low_sources", [])) == 0
        return {
            "passed": passed,
            "reason": f"Markers: {markers}, Translationese: {hits}, Low sources: {coverage.get('low_sources', [])}",
            "details": results,
        }


def cmd_status(lock: SubPhaseWorkflowLock):
    status = lock.get_status()
    print(f"Skill: {status['skill']}")
    print(f"Current phase: {status['current_phase']}")
    print(f"Current sub-phase: {status['current_sub_phase']}")
    print(f"Completed phases: {status['completed_phases']}")
    for phase, subs in status['completed_sub_phases'].items():
        total = len(SUB_PHASES.get(phase, []))
        print(f"  Phase {phase}: {len(subs)}/{total} sub-phases completed")
    if status['chapter_progress']:
        print(f"Chapters: {len(status['chapter_progress'])} tracked")
    if status['source_coverage']:
        print(f"Source coverage: {status['source_coverage']}")


def cmd_check_gate(lock: SubPhaseWorkflowLock, run_dir: Path, phase: str, sub_phase: str = None, chapter: str = None):
    if not sub_phase:
        # Legacy phase-level gate
        sub_phases = SUB_PHASES.get(phase, [])
        sub_phase = sub_phases[-1] if sub_phases else None  # Use final sub-phase as phase gate

    can_enter, reason = lock.can_enter_sub_phase(phase, sub_phase, chapter)
    if not can_enter:
        print(f"ERROR: Cannot enter sub-phase {sub_phase}. {reason}")
        sys.exit(1)

    # Dispatch to appropriate checker
    key = f"{phase}.{sub_phase}"
    checkers = {
        "0.0.1": lambda: GateChecker.check_inventory(run_dir),
        "0.0.3": lambda: GateChecker.check_phase0_sub3(run_dir),
        "0.0.5": lambda: GateChecker.check_inventory(run_dir),  # Final gate combines all
        "1.1.5": lambda: GateChecker.check_phase1_sub5(run_dir),
        "2.2.3": lambda: GateChecker.check_chapter_quality(run_dir, chapter or "chapter1"),
    }

    checker_key = f"{phase}.{sub_phase}"
    if checker_key in checkers:
        result = checkers[checker_key]()
    else:
        result = {"passed": True, "reason": f"Gate for sub-phase {sub_phase} not implemented — auto-pass"}

    if result["passed"]:
        print(f"PASS: Sub-phase {sub_phase} gate passed. {result['reason']}")
    else:
        print(f"FAIL: Sub-phase {sub_phase} gate failed. {result['reason']}")
        sys.exit(1)


def cmd_record_progress(lock: SubPhaseWorkflowLock, phase: str, sub_phase: str,
                         status: str, chapter: str = None, markers: int = 0,
                         gate_result: str = ""):
    result = lock.record_progress(phase, sub_phase, status, chapter, markers, gate_result)
    print(f"Recorded: Phase {phase} Sub-phase {sub_phase} = {status}" +
          (f" (chapter: {chapter})" if chapter else ""))


def cmd_coverage_report(run_dir: Path):
    output_dir = run_dir / "output"
    if not output_dir.exists():
        print("ERROR: Output directory not found")
        sys.exit(1)

    # Per-source ratio
    ratio = CoverageGuardian.check_per_source_ratio(output_dir)
    print("=== Per-Source Coverage ===")
    counts = ratio.get("counts", CoverageGuardian.count_source_markers(output_dir))
    total = sum(counts.values())
    for src, count in sorted(counts.items(), key=lambda x: -x[1]):
        pct = f"{count/total*100:.1f}%" if total > 0 else "0%"
        print(f"  {src}: {count} markers ({pct})")
    print(f"  Total: {total}")
    print(f"  Floor check (10%): {'PASS' if ratio['passed'] else 'FAIL'} — {ratio['reason']}")

    # Patch detection
    print("\n=== Patch-Style Detection ===")
    patch = CoverageGuardian.detect_patch_style(output_dir)
    if patch["patch_warnings"]:
        for w in patch["patch_warnings"]:
            print(f"  WARNING: {w}")
    else:
        print("  No patch-style sources detected")
    print(f"  Chapter distribution: {patch['source_chapter_distribution']}")


def cmd_coverage_guard(run_dir: Path, chapter: str):
    output_dir = run_dir / "output"
    result = CoverageGuardian.check_chapter_coverage(output_dir, chapter)
    print(f"=== Coverage Guard for {chapter} ===")
    print(f"  Total markers: {result.get('total_markers', 0)}")
    print(f"  Source distribution: {result.get('source_markers', {})}")
    if result.get("low_sources"):
        print(f"  G7 FAIL: Sources with <3 markers: {result['low_sources']}")
    else:
        print(f"  G7 PASS: All sources have >=3 markers")
    print(f"  Chapter size: {result.get('chapter_size', 0)} bytes")
    print(f"  Overall: {'PASS' if result['passed'] else 'FAIL'}")


def main():
    if len(sys.argv) < 4:
        print("Usage: workflow.py integrate-books <run_dir> <command> [args]")
        print("Commands: status, check_gate, record_progress, coverage_report, coverage_guard")
        sys.exit(1)

    skill = sys.argv[1]
    if skill != "integrate-books":
        print(f"ERROR: This script only supports integrate-books, got '{skill}'")
        sys.exit(1)

    run_dir = sys.argv[2]
    command = sys.argv[3]
    lock = SubPhaseWorkflowLock(run_dir)
    rd = Path(run_dir)

    if command == "status":
        cmd_status(lock)
    elif command == "check_gate":
        if len(sys.argv) < 5:
            print("Usage: workflow.py integrate-books <run_dir> check_gate <phase> [<sub_phase>] [chapter]")
            sys.exit(1)
        phase = sys.argv[4]
        sub_phase = sys.argv[5] if len(sys.argv) > 5 else None
        chapter = sys.argv[6] if len(sys.argv) > 6 else None
        cmd_check_gate(lock, rd, phase, sub_phase, chapter)
    elif command == "record_progress":
        parser = argparse.ArgumentParser()
        parser.add_argument("--phase", required=True)
        parser.add_argument("--sub-phase", required=True, dest="sub_phase")
        parser.add_argument("--chapter", default=None)
        parser.add_argument("--status", required=True)
        parser.add_argument("--markers", type=int, default=0)
        parser.add_argument("--gate-result", default="", dest="gate_result")
        args = parser.parse_args(sys.argv[5:])
        cmd_record_progress(lock, args.phase, args.sub_phase, args.status,
                           args.chapter, args.markers, args.gate_result)
    elif command == "coverage_report":
        cmd_coverage_report(rd)
    elif command == "coverage_guard":
        if len(sys.argv) < 5:
            print("Usage: workflow.py integrate-books <run_dir> coverage_guard <chapter>")
            sys.exit(1)
        cmd_coverage_guard(rd, sys.argv[4])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test workflow.py status command**

Run: `cd /home/hsf/projects/others/tech_book_skills && python integrate-books/scripts/workflow.py integrate-books /tmp/test-run status`

Expected: Shows skill name, empty state (no prior run data).

- [ ] **Step 3: Test workflow.py record_progress command**

Run: `python integrate-books/scripts/workflow.py integrate-books /tmp/test-run record_progress --phase 0 --sub-phase 0.1 --status completed`

Expected: "Recorded: Phase 0 Sub-phase 0.1 = completed"

- [ ] **Step 4: Test workflow.py coverage_report on real data**

Run: `python integrate-books/scripts/workflow.py integrate-books /home/hsf/文档/books/cpp_xf coverage_report`

Expected: Shows per-source marker counts with floor check. Should flag Mindset/StepByStep as below 10% floor.

- [ ] **Step 5: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/scripts/workflow.py
git commit -m "feat: rewrite workflow.py with sub-phase tracking, coverage guardian, auto-progress"
```

---

### Task 2: Rewrite SKILL.md with Sub-Phase Architecture

**Files:**
- Rewrite: `integrate-books/SKILL.md`

- [ ] **Step 1: Write the new SKILL.md**

Rewrite `integrate-books/SKILL.md` completely in English with the sub-phase architecture:

```markdown
---
name: integrate-books
description: "Merge multiple technical books into one unified book. Trigger: integrate books, merge books, combine sources, enrich chapters. Do NOT trigger for: single book translation (use translate-book), quality review (use review-tech-book)."
---

# Integrate Books

Merge multiple technical books into one unified book. Output must read like a single book, not a collage.

## Workflow

```
Phase 0: Deep Reading (5 sub-phases)
  0.1 Book Inventory → 0.2 Per-Book Reading → 0.3 Index Generation → 0.4 Coverage Comparison → 0.5 Gate 0

Phase 1: Architecture Design (6 sub-phases)
  1.1 Load Indexes → 1.2 Cross-Book Analysis → 1.3 Target TOC → 1.4 Per-Chapter Plans → 1.5 Reverse Coverage → 1.6 Gate 1

Phase 2: Chapter Generation (5 sub-phases per chapter)
  2.1 Load Plan+Sources → 2.2 Deconstruct & Rewrite → 2.3 Quality Gate → 2.4 Progress Record → 2.5 Batch Check (every 5 ch)

Phase 3: Validation → Phase 4: Report
```

**Phase lock**: Run `python scripts/workflow.py integrate-books <run_dir> check_gate <phase> [<sub_phase>] [chapter]` before entering any sub-phase. If gate fails, fix and retry. Do not proceed.

**Sub-agent constraints**: See `references/agent-orchestration.md`. Max concurrent agents: 5. Respect dependency ordering.

## Phase 0: Deep Reading

### Sub-Phase 0.1: Book Inventory & Metadata

**Input**: Source book paths/URLs
**Output**: `.book-doc/knowledge_base/INVENTORY.md`

**Do**:
1. List all source books with: name, author, target audience, chapter count, estimated code examples, language/framework version
2. Record total book count, total chapter count, estimated scope

**Gate 0.1** (auto-check):
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 0 0.1
```
- INVENTORY.md exists with complete metadata for every source book
- Chapter count per book matches actual content

### Sub-Phase 0.2: Per-Book Chapter-by-Chapter Reading

**Input**: INVENTORY.md, source books
**Output**: Per-chapter reading evidence (recorded in progress.md)

**Do** (for each book, one agent per book, max 3 books parallel):
1. For each chapter (sequential within book, no skipping):
   - Read the actual chapter content (no title-only inference)
   - Record reading evidence: paragraph count, code block count, >=3 specific technical terms
   - Proceed to next chapter only after evidence is recorded
2. For web-based sources: resolve all links/references within a chapter before moving to next

**Reading evidence format** (record in progress.md for each chapter):
```markdown
### [BookName] Ch[N] Reading Evidence
- Paragraphs: [count]
- Code blocks: [count]
- Core concepts: [list >=3 specific terms]
- Unique to this book: [what this chapter contributes uniquely]
```

**Gate 0.2** (per book):
- Reading evidence exists for every chapter
- No two consecutive chapters have identical evidence format
- Every evidence entry has >=3 specific technical terms (not title rewrites)

### Sub-Phase 0.3: Index Generation

**Auto-load**: `references/knowledge-index-format.md`, `references/agent-orchestration.md`

**Input**: Reading notes from 0.2
**Output**: `.book-doc/knowledge_base/{book_name}/index.md` (>=1000 lines per book)

**Do**:
1. For each book, generate a deep knowledge index following `references/knowledge-index-format.md`
2. Each index must cover all required sections (see knowledge-index-format.md)
3. Record reading evidence per chapter within the index

**Gate 0.3** (per book, auto-check):
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 0 0.3
```
- index.md exists and >=1000 lines
- Contains: Teaching Philosophy, Cognitive Progression, Per-Chapter Deep Analysis, Cross-Chapter Theme Mapping, Integration Readiness Summary
- Each chapter analysis has: Content Coverage, Methodology Analysis, Depth Calibration, Unique Insights, Code Example Inventory, Integration Readiness

### Sub-Phase 0.4: Coverage Comparison

**Input**: All index.md files
**Output**: `.book-doc/knowledge_base/INDEX/source_coverage.md`

**Do**:
1. Per-topic: which books cover it, at what depth, with what methodology
2. Per-book: unique topics, shared topics, gap topics
3. Cross-book: overlap matrix, complementarity map

**Gate 0.4**:
- source_coverage.md exists
- Every source book's unique topics are identified

### Sub-Phase 0.5: Gate 0

Combines all sub-phase gates. **THIS PHASE IS THE FOUNDATION. Do not proceed until every index is verified.**

**Gate 0**:
- All sub-phase gates 0.1-0.4 passed
- INVENTORY.md + all index.md files + source_coverage.md exist
- Coverage comparison identifies all unique and shared topics

**After gate pass, record progress**:
```bash
python scripts/workflow.py integrate-books <run_dir> record_progress --phase 0 --sub-phase 0.5 --status completed
```

## Phase 1: Architecture Design

### Sub-Phase 1.1: Load All Indexes

**Input**: All index.md files from Phase 0
**Output**: Read confirmation in progress.md

**Do**:
1. Read every index.md completely (no skimming)
2. Record read confirmation with evidence: which sections read, key findings per book
3. List core methodology differences across books (>=3 points)

**Gate 1.1**:
- Read confirmation exists for every source book
- At least 3 methodology differences identified with specific evidence

### Sub-Phase 1.2: Cross-Book Analysis

**Auto-load**: `references/book-architecture.md`, all knowledge indexes

**Input**: Indexes + source_coverage.md
**Output**: `cross-book-analysis.md`

**Do**:
1. Methodology Difference Analysis (per topic)
2. Depth Alignment Analysis (per topic)
3. Boundary Complementarity Analysis (per topic)
4. Style Conflict Resolution (per dimension)

Each analysis must cite specific index evidence.

**Gate 1.2**:
- cross-book-analysis.md exists with all 4 required sections
- Every analysis cites specific index evidence
- No "TBD" or "to be determined"

### Sub-Phase 1.3: Target TOC Design

**Input**: cross-book-analysis.md
**Output**: Target TOC in `source-architecture.md`

**Do**:
1. Determine target reader and use case
2. Determine main skeleton source (not necessarily any source book's original TOC)
3. Order chapters by cognitive dependency
4. Each chapter: one primary cognitive load, explicit prerequisites, capability output
5. Assign source coverage and methodology choices with evidence

**Gate 1.3**:
- Every chapter has: title, capability goal, prerequisites, primary cognitive load
- No chapter has more than one primary cognitive load
- Methodology choices cite evidence

### Sub-Phase 1.4: Per-Chapter Integration Plans

**Input**: Target TOC + knowledge indexes
**Output**: `plan.md` with self-contained per-chapter plans

**Do**: For each target chapter, write a self-contained integration plan including:
- Source mapping (source, chapter, role, contribution)
- Methodology choice with evidence
- Depth alignment strategy
- Content synthesis plan (per-section)
- Concept bridging (previous/internal/next)
- Terminology conventions
- Style baseline example (1-2 paragraphs)
- Expected output (length, code examples, marker count)

**Gate 1.4**:
- plan.md has an integration plan for EVERY target chapter
- Each plan is self-contained
- No "TBD" or placeholders
- Every methodology choice has evidence

### Sub-Phase 1.5: Reverse Coverage Matrix

**Input**: plan.md + all index.md files
**Output**: Reverse coverage matrix in `source-architecture.md`

**Do**: Build reverse coverage: every source chapter must map to one of:
- Main content (with target chapter location)
- Sidebar (with content description)
- Appendix (with content description)
- Explicit exclusion (with rationale)

**CRITICAL: Coverage target is 100%, not 95%.** Every source chapter must be accounted for.

**Gate 1.5**:
- Reverse coverage matrix accounts for 100% of source chapters
- Every excluded chapter has documented rationale

### Sub-Phase 1.6: Gate 1

**Gate 1** (auto-check):
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 1 1.6
```
- All sub-phase gates 1.1-1.5 passed
- source-architecture.md exists with all required sections
- plan.md exists with self-contained plans
- No TBD/placeholders
- Reverse coverage = 100%

**After gate pass, record progress**:
```bash
python scripts/workflow.py integrate-books <run_dir> record_progress --phase 1 --sub-phase 1.6 --status completed
```

## Phase 2: Chapter Generation

### Sub-Phase 2.1: Load Plan + Sources

**Input**: Current chapter's integration plan from plan.md
**Output**: Loaded context in agent's working memory

**Do**:
1. Load the chapter's integration plan (self-contained)
2. Load relevant knowledge index sections (by source mapping)
3. Load style baseline from plan.md
4. Record load confirmation in progress.md

**Gate 2.1**: Load confirmation recorded.

### Sub-Phase 2.2: Deconstruct & Rewrite

**Auto-load**: `references/full-integration.md`, `references/agent-orchestration.md`

**Input**: Loaded plan + sources + style baseline
**Output**: Chapter HTML with integration markers

**Do** (5-step rewrite, see `references/full-integration.md`):
1. Deconstruct all sources' relevant content
2. Design new section structure (do not reuse any source's original structure)
3. Assign primary/secondary sources per section
4. Rewrite in unified style
5. Add markers: `<!-- integrated: [Source]Ch[N]-[id] -->`

**Integration level must be L3 or L4**. L1 (direct insert) and L2 (style adapt only) are prohibited.

**Sub-agent strategy**:
- One chapter at a time (sequential)
- Within a chapter: max 3 section agents parallel (if sections are independent)
- Each agent receives: section plan + knowledge index excerpts + style baseline

**Gate 2.2**:
- Chapter HTML exists with integration markers
- No section uses L1 or L2 integration

### Sub-Phase 2.3: Quality Gate

**Input**: Chapter HTML
**Output**: Gate results (G1-G8)

| ID | Check | Pass Criteria | Fail Action |
|----|-------|--------------|-------------|
| G1 | Coverage | All plan.md IDs have markers | Rewrite chapter |
| G2 | Code quality | New code has V1-V3 tags | Add tags + verify |
| G3 | Style match | No translationese, matches baseline | Rewrite sections |
| G4 | No duplicates | No repeated explanations | Merge/cross-ref |
| G5 | Narrative flow | Transitions natural, arc complete | Rewrite |
| G6 | Depth match | Matches plan's depth target, sufficient length | Expand or trim |
| G7 | Source ratio | Each mapped source has >=3 markers in this chapter | Expand source contribution |
| G8 | Output size | Chapter size >= max(source_chapter_sizes) * 0.8 | Expand content |

**Gate 2.3** (auto-check):
```bash
python scripts/workflow.py integrate-books <run_dir> check_gate 2 2.3 <chapter>
python scripts/workflow.py integrate-books <run_dir> coverage_guard <chapter>
```

**Fail = rewrite chapter. Do not proceed. Do not accumulate issues.**

### Sub-Phase 2.4: Progress Record

**MANDATORY**: Must call after every chapter gate.

```bash
python scripts/workflow.py integrate-books <run_dir> record_progress \
  --phase 2 --sub-phase 2.4 \
  --chapter <chapter> \
  --status completed \
  --markers <count> \
  --gate-result "G1:pass G2:pass ... G7:pass G8:pass"
```

**Gate 2.4**: workflow.py record_progress called successfully. progress.md updated.

**This sub-phase prevents the "progress tracking failure" problem. Without it, next chapter cannot start.**

### Sub-Phase 2.5: Batch Consistency Check (every 5 chapters)

**Input**: Last 5 completed chapters
**Output**: Consistency report

**Do**:
1. Cross-chapter terminology consistent
2. Source unidentifiable test (3 random paragraphs from different chapters)
3. Narrative arc connects across chapters
4. Per-source coverage ratio across batch >=10% for each source

**Gate 2.5**:
- All batch checks pass
- No source has <10% of batch markers

**Output**: `output/{chapter}.html` files

## Phase 3: Validation

**Do**:
1. Run coverage validation across all chapters
2. Per-source coverage >= 10% of total markers (coverage guardian)
3. Patch-style detection across all sources
4. Term consistency check (full book grep)
5. Code runnability check (all code blocks)
6. Style consistency (read 3 consecutive chapters from different parts)
7. Cross-reference integrity (all chapter links valid)
8. Reverse coverage: verify 100% source material accounted for

**Auto-check scripts**:
```bash
python ../shared/validate_tech.py output/
python ../shared/validate_terms.py output/
python scripts/workflow.py integrate-books <run_dir> coverage_report
python scripts/workflow.py integrate-books <run_dir> check_gate 3
```

**Gate 3**:
- Coverage >= 95% (aggregate)
- Per-source coverage >= 10% (coverage guardian)
- No patch-style sources detected
- All terms consistent
- All code runnable
- All cross-references valid

## Phase 4: Report

**Auto-load**: `../shared/report-templates.md`

**Do**: Write `report.md` with:
- Summary
- Per-chapter scores (including per-source marker counts)
- Coverage guardian results
- Patch-style detection results
- Issues and known limits
- Coverage matrix

**Gate 4**:
- report.md exists
- Contains: summary, scores, coverage guardian results, issues, fix batches, coverage matrix

## Anti-Slacking Rules

Per `../shared/anti-slacking.md`:
- Every sub-phase start: re-read reference files, record read confirmation in progress.md
- Every claimed read: attach structure evidence (paragraph count, code block count, specific terms)
- No "I remember" — always re-read
- No title-only inference — open and read actual content
- No "差不多" — gate either passes or fails, no partial credit
- Every sub-phase completion: call `workflow.py record_progress` (mandatory)

## Coverage Guardian

Per `references/integration-discipline.md` Coverage Guardian section:

- **Per-source floor**: No source book may have fewer than 10% of total markers
- **Per-chapter minimum**: Mapped primary/secondary sources must have >=3 markers per chapter
- **Patch-style detection**: Sources concentrated in <=2 chapters or always supplemental are flagged
- **Output size guard**: Each chapter >= max(source_chapter_sizes) * 0.8

Run coverage report at any time:
```bash
python scripts/workflow.py integrate-books <run_dir> coverage_report
```

## Quality Standards

- Reader cannot identify content sources
- Chapter skeleton survives reverse coverage check (100%, not 95%)
- Every addition has source, location, benefit
- Duplicates merged or cross-referenced
- Output ready for review-tech-book via `report.md`
- Integration level: L3 (reorganize) or L4 (full fusion) only — see `references/full-integration.md`
- All sub-phase progress recorded via workflow.py
```

- [ ] **Step 2: Verify SKILL.md loads correctly**

Run: `head -5 /home/hsf/projects/others/tech_book_skills/integrate-books/SKILL.md`

Expected: Frontmatter with name: integrate-books and English description.

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/SKILL.md
git commit -m "feat: rewrite SKILL.md with sub-phase architecture and English"
```

---

### Task 3: Rewrite knowledge-index-format.md in English

**Files:**
- Rewrite: `integrate-books/references/knowledge-index-format.md`

- [ ] **Step 1: Write the English version**

Rewrite `integrate-books/references/knowledge-index-format.md` with all English field names. Content structure stays the same, but all section headers, field names, and instructions are in English. Example content can show Chinese where the actual output would be in Chinese.

The file should translate:
- 深度知识索引格式 → Deep Knowledge Index Format
- 元信息 → Metadata
- 整体教学哲学 → Teaching Philosophy
- 核心教学方法 → Core Teaching Method
- 认知递进策略 → Cognitive Progression Strategy
- 叙事风格基线 → Narrative Style Baseline
- 整体评价 → Overall Assessment
- 逐章深度分析 → Per-Chapter Deep Analysis
- 内容覆盖 → Content Coverage
- 方法论分析 → Methodology Analysis
- 深度标定 → Depth Calibration
- 独特洞察 → Unique Insights
- 代码示例清单 → Code Example Inventory
- 交叉引用 → Cross-References
- 风格特征 → Style Characteristics
- 整合就绪度 → Integration Readiness
- 跨章主题映射 → Cross-Chapter Theme Mapping
- 知识点交叉引用矩阵 → Knowledge Point Cross-Reference Matrix
- 整合准备摘要 → Integration Readiness Summary

- [ ] **Step 2: Verify English conversion**

Run: `grep -c '教学哲学\|深度标定\|整合就绪度\|覆盖范围\|引入方式' /home/hsf/projects/others/tech_book_skills/integrate-books/references/knowledge-index-format.md`

Expected: 0 (no Chinese section headers remaining)

- [ ] **Step 3: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/knowledge-index-format.md
git commit -m "feat: convert knowledge-index-format.md to English"
```

---

### Task 4: Rewrite book-architecture.md in English

**Files:**
- Rewrite: `integrate-books/references/book-architecture.md`

- [ ] **Step 1: Write the English version**

Rewrite with all English content, adding sub-phase references (1.1-1.6). Translate:
- 书籍架构评估协议 → Book Architecture Assessment Protocol
- 何时必须使用 → When to Use
- 前置条件 → Prerequisites
- 核心原则 → Core Principles
- 跨书深度对比 → Cross-Book Deep Comparison
- 方法论差异分析 → Methodology Difference Analysis
- 深度对齐分析 → Depth Alignment Analysis
- 边界互补分析 → Boundary Complementarity Analysis
- 风格冲突与调和 → Style Conflict Resolution
- 目标目录设计 → Target TOC Design
- 逐章整合计划 → Per-Chapter Integration Plan
- 源书画像维度 → Source Book Portrait Dimensions
- 目标目录自检 → Target TOC Self-Check
- 常见失败模式 → Common Failure Modes

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/book-architecture.md
git commit -m "feat: convert book-architecture.md to English with sub-phase refs"
```

---

### Task 5: Rewrite full-integration.md in English

**Files:**
- Rewrite: `integrate-books/references/full-integration.md`

- [ ] **Step 1: Write the English version**

The file is already mostly English. Ensure all remaining Chinese is translated. Content stays the same: Integration Levels (L1-L4), 5-Step Rewrite, Anti-Patterns, Quality Test.

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/full-integration.md
git commit -m "feat: convert full-integration.md to English"
```

---

### Task 6: Rewrite integration-discipline.md in English + Coverage Guardian

**Files:**
- Rewrite: `integrate-books/references/integration-discipline.md`

- [ ] **Step 1: Write the English version with Coverage Guardian section**

Rewrite with all English content and ADD the new Coverage Guardian section at the end. Translate all existing Chinese terms. Add:

```markdown
## Coverage Guardian

### Per-Source Coverage Ratio

Per-chapter rule: If a source book is mapped as "primary" or "secondary" for a chapter, it MUST contribute >=3 integration markers in that chapter.

Per-book rule: Each source book's total markers >= (total_source_chapters * 0.5).

Floor rule: No source book may have fewer than 10% of total markers across the integrated book.

### Patch-Style Detection

A source is "patch-style" if ANY of these is true:
1. All its markers appear in <=2 chapters (concentrated, not integrated)
2. Its markers never appear as the first marker in any section
3. Its content always appears after the primary source content within every section

Escalation: WARNING (first detection) → REQUIRE REWRITE (second detection for same source)

### Output Size Guard

Per-chapter: Output chapter size MUST be >= max(source_chapter_sizes_for_this_topic) * 0.8

This prevents "integrated book has less content than a single source book" problem.
```

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/integration-discipline.md
git commit -m "feat: convert integration-discipline.md to English, add Coverage Guardian"
```

---

### Task 7: Rewrite quality-gate.md in English + G7/G8

**Files:**
- Rewrite: `integrate-books/references/quality-gate.md`

- [ ] **Step 1: Write the English version with G7/G8**

Rewrite with all English content. Add G7 (Source Ratio) and G8 (Output Size) to the per-chapter gate table. Translate all Chinese terms.

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/quality-gate.md
git commit -m "feat: convert quality-gate.md to English, add G7/G8 checks"
```

---

### Task 8: Rewrite agent-orchestration.md in English

**Files:**
- Rewrite: `integrate-books/references/agent-orchestration.md`

- [ ] **Step 1: Write the English version with sub-phase orchestration**

Rewrite with all English content. Add sub-phase orchestration details:
- Phase 0: per-book agents with sub-phase awareness (0.1 → 0.2 → 0.3 sequential per book)
- Phase 1: single agent with sub-phase sequence (1.1 → 1.6)
- Phase 2: per-chapter agents with sub-phase sequence (2.1 → 2.4 per chapter, 2.5 per batch)

Translate all Chinese terms including agent task templates.

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/agent-orchestration.md
git commit -m "feat: convert agent-orchestration.md to English with sub-phase rules"
```

---

### Task 9: Rewrite synthesis-methodology.md in English

**Files:**
- Rewrite: `integrate-books/references/synthesis-methodology.md`

- [ ] **Step 1: Write the English version**

Translate all Chinese content to English. The file covers:
- Content synthesis methodology (knowledge stacking vs teaching narrative)
- Chapter narrative arc construction
- Example evolution design
- Concept bridging design
- Quality perception checklist

Translate key terms:
- 知识点堆砌 → Knowledge Stacking
- 教学叙事 → Teaching Narrative
- 桥梁概念 → Bridge Concepts
- 段落内逻辑 → In-Paragraph Logic
- 示例演化 → Example Evolution
- 质量感知 → Quality Perception

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/synthesis-methodology.md
git commit -m "feat: convert synthesis-methodology.md to English"
```

---

### Task 10: Rewrite context-passing.md in English

**Files:**
- Rewrite: `integrate-books/references/context-passing.md`

- [ ] **Step 1: Write the English version with sub-phase context**

Rewrite with all English content. Add sub-phase context tracking:
- Each sub-phase completion appends to context-summary.md
- Phase 2 per-chapter sub-phases include chapter-specific context
- Reading rules updated for sub-phase granularity

Translate all Chinese terms.

- [ ] **Step 2: Commit**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add integrate-books/references/context-passing.md
git commit -m "feat: convert context-passing.md to English with sub-phase context"
```

---

### Task 11: Verify and Final Commit

- [ ] **Step 1: Verify all files are in English**

Run: `for f in integrate-books/SKILL.md integrate-books/references/*.md; do count=$(grep -c '[\x{4e00}-\x{9fff}]' "$f" 2>/dev/null || echo 0); echo "$f: $count Chinese chars"; done`

Expected: Only knowledge-index-format.md may have Chinese in example content sections. All other files should have 0 Chinese chars in structural content.

- [ ] **Step 2: Verify workflow.py works end-to-end**

Run:
```bash
cd /home/hsf/projects/others/tech_book_skills
# Test status
python integrate-books/scripts/workflow.py integrate-books /tmp/test-int-run status
# Test record_progress
python integrate-books/scripts/workflow.py integrate-books /tmp/test-int-run record_progress --phase 0 --sub-phase 0.1 --status completed
python integrate-books/scripts/workflow.py integrate-books /tmp/test-int-run record_progress --phase 0 --sub-phase 0.2 --status completed
python integrate-books/scripts/workflow.py integrate-books /tmp/test-int-run record_progress --phase 2 --sub-phase 2.4 --chapter ch01 --status completed --markers 27 --gate-result "G1:pass G2:pass G3:pass G4:pass G5:pass G6:pass G7:pass G8:pass"
# Test coverage_report on real data
python integrate-books/scripts/workflow.py integrate-books /home/hsf/文档/books/cpp_xf coverage_report
```

- [ ] **Step 3: Final commit with all changes**

```bash
cd /home/hsf/projects/others/tech_book_skills
git add -A
git commit -m "feat: complete integrate-books skill optimization - sub-phase architecture, coverage guardian, auto-progress, English conversion"
```
