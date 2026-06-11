#!/usr/bin/env python3
"""
Workflow orchestrator for integrate-books skill (v3).
Ensures phases execute in order, gates pass before proceeding.

Phase structure (v3):
  Phase 0: Deep Reading & Knowledge Indexing (5 sub-phases)
  Phase 1: Architecture Design (6 sub-phases)
  Phase 2: Chapter Generation (5 sub-phases per chapter)
  Phase 3: Validation (4 sub-phases)
  Phase 4: Report (2 sub-phases)

Features:
  - Sub-phase tracking with progress blocking
  - CoverageGuardian for per-source coverage checks
  - Auto-progress recording to progress.md
  - Gate checkers for each sub-phase
"""
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# Sub-phase definitions
SUB_PHASES = {
    "0": ["0.1", "0.2", "0.3", "0.4", "0.5"],
    "1": ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"],
    "2": ["2.1", "2.2", "2.3", "2.4", "2.5"],
    "3": ["3.1", "3.2", "3.3", "3.4"],
    "4": ["4.1", "4.2"],
}

# Source aliases for marker identification
SOURCE_ALIASES = {
    "will": "Will",
    "willch": "Will",
    "stroustrup": "Stroustrup",
    "stroustrupch": "Stroustrup",
    "cookbook": "Cookbook",
    "cookbookch": "Cookbook",
    "lowlatency": "LowLatency",
    "lowlatencych": "LowLatency",
    "mindset": "Mindset",
    "mindsetch": "Mindset",
    "stepbystep": "StepByStep",
    "stepbystepch": "StepByStep",
}

# Known sources
KNOWN_SOURCES = ["Will", "Stroustrup", "Cookbook", "LowLatency", "Mindset", "StepByStep"]


class SubPhaseWorkflowLock:
    """Manages workflow state with sub-phase tracking and progress blocking."""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.state_file = self.run_dir / ".workflow_state.json"
        self.progress_file = self.run_dir / "progress.md"
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "current_phase": None,
            "current_sub_phase": None,
            "completed_phases": [],
            "completed_sub_phases": {},
            "gates": {},
            "chapters_completed": [],
            "chapters_failed": [],
            "chapter_sub_phases": {},  # {chapter: {sub_phase: status}}
            "markers_count": {},
            "last_updated": None,
        }

    def _save_state(self):
        self.state["last_updated"] = datetime.now().isoformat()
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def _update_progress_md(self):
        """Auto-update progress.md with current state."""
        lines = [
            "# Integration Progress",
            "",
            f"**Last Updated**: {self.state.get('last_updated', 'N/A')}",
            "",
            "## Phase Status",
            "",
        ]

        for phase in ["0", "1", "2", "3", "4"]:
            status = "completed" if phase in self.state["completed_phases"] else "pending"
            lines.append(f"- Phase {phase}: **{status}**")

            # Sub-phase details
            sub_phases = SUB_PHASES.get(phase, [])
            completed_subs = self.state["completed_sub_phases"].get(phase, [])
            for sp in sub_phases:
                sp_status = "completed" if sp in completed_subs else "pending"
                lines.append(f"  - {sp}: {sp_status}")

        lines.extend([
            "",
            "## Chapter Progress",
            "",
        ])

        for ch in self.state["chapters_completed"]:
            lines.append(f"- {ch}: completed")
        for ch in self.state["chapters_failed"]:
            lines.append(f"- {ch}: failed (needs retry)")

        lines.extend([
            "",
            "## Marker Statistics",
            "",
        ])

        for source, count in self.state.get("markers_count", {}).items():
            lines.append(f"- {source}: {count} markers")

        self.progress_file.write_text("\n".join(lines))

    def can_enter_phase(self, phase: str) -> bool:
        """Check if phase can be entered (previous phase completed)."""
        if phase not in SUB_PHASES:
            return False

        phase_idx = list(SUB_PHASES.keys()).index(phase)
        if phase_idx == 0:
            return True

        prev_phase = list(SUB_PHASES.keys())[phase_idx - 1]
        return prev_phase in self.state["completed_phases"]

    def can_enter_sub_phase(self, phase: str, sub_phase: str, chapter: Optional[str] = None) -> Tuple[bool, str]:
        """Check if sub-phase can be entered (previous sub-phase completed)."""
        if phase not in SUB_PHASES:
            return False, f"Unknown phase: {phase}"

        sub_phases = SUB_PHASES[phase]
        if sub_phase not in sub_phases:
            return False, f"Unknown sub-phase: {sub_phase}"

        # Check phase entry
        if not self.can_enter_phase(phase):
            phase_idx = list(SUB_PHASES.keys()).index(phase)
            prev_phase = list(SUB_PHASES.keys())[phase_idx - 1]
            return False, f"Cannot enter Phase {phase}. Phase {prev_phase} not completed."

        # For Phase 2, check chapter-specific progress
        if phase == "2" and chapter:
            chapter_state = self.state["chapter_sub_phases"].get(chapter, {})
            sub_idx = sub_phases.index(sub_phase)

            if sub_idx == 0:
                # First sub-phase: check if previous chapter's 2.4 is done
                chapters_done = self.state["chapters_completed"]
                if chapters_done:
                    last_chapter = chapters_done[-1]
                    last_chapter_state = self.state["chapter_sub_phases"].get(last_chapter, {})
                    if "2.4" not in last_chapter_state or last_chapter_state["2.4"] != "completed":
                        return False, f"Previous chapter {last_chapter} sub-phase 2.4 not completed"
            else:
                # Check previous sub-phase in same chapter
                prev_sub = sub_phases[sub_idx - 1]
                if prev_sub not in chapter_state or chapter_state[prev_sub] != "completed":
                    return False, f"Sub-phase {prev_sub} not completed for chapter {chapter}"
        else:
            # Non-chapter phases: check previous sub-phase
            completed_subs = self.state["completed_sub_phases"].get(phase, [])
            sub_idx = sub_phases.index(sub_phase)

            if sub_idx > 0:
                prev_sub = sub_phases[sub_idx - 1]
                if prev_sub not in completed_subs:
                    return False, f"Sub-phase {prev_sub} not completed"

        return True, "OK"

    def record_progress(self, phase: str, sub_phase: str, status: str,
                       chapter: Optional[str] = None, markers: int = 0,
                       gate_result: Optional[Dict] = None):
        """Record sub-phase completion and auto-update progress.md.

        Enforces progress blocking: cannot record completion for a sub-phase
        unless the previous sub-phase is already completed.
        """
        # Enforce progress blocking for completion status
        if status == "completed":
            can_enter, reason = self.can_enter_sub_phase(phase, sub_phase, chapter)
            if not can_enter:
                raise ValueError(f"Progress blocked: {reason}")

        # Initialize phase sub-phases if needed
        if phase not in self.state["completed_sub_phases"]:
            self.state["completed_sub_phases"][phase] = []

        # Record sub-phase completion
        if status == "completed" and sub_phase not in self.state["completed_sub_phases"][phase]:
            self.state["completed_sub_phases"][phase].append(sub_phase)

        # Update current sub-phase tracking
        self.state["current_sub_phase"] = sub_phase

        # For Phase 2, record chapter-specific progress
        if phase == "2" and chapter:
            if chapter not in self.state["chapter_sub_phases"]:
                self.state["chapter_sub_phases"][chapter] = {}
            self.state["chapter_sub_phases"][chapter][sub_phase] = status

            # If 2.5 completed, mark chapter as done
            if sub_phase == "2.5" and status == "completed":
                if chapter not in self.state["chapters_completed"]:
                    self.state["chapters_completed"].append(chapter)
                if chapter in self.state["chapters_failed"]:
                    self.state["chapters_failed"].remove(chapter)

        # Record gate result
        if gate_result:
            gate_key = f"{phase}.{sub_phase}" + (f".{chapter}" if chapter else "")
            self.state["gates"][gate_key] = gate_result

        # Update markers count
        if markers > 0:
            if "markers_count" not in self.state:
                self.state["markers_count"] = {}
            self.state["markers_count"][phase] = self.state["markers_count"].get(phase, 0) + markers

        # Check if all sub-phases completed for this phase
        all_subs = SUB_PHASES.get(phase, [])
        completed_subs = self.state["completed_sub_phases"].get(phase, [])
        if all(sp in completed_subs for sp in all_subs):
            if phase not in self.state["completed_phases"]:
                self.state["completed_phases"].append(phase)
            self.state["current_phase"] = phase

        self._save_state()
        self._update_progress_md()

    def get_status(self) -> Dict:
        """Get current workflow status."""
        return {
            "current_phase": self.state["current_phase"],
            "current_sub_phase": self.state["current_sub_phase"],
            "completed_phases": self.state["completed_phases"],
            "completed_sub_phases": self.state["completed_sub_phases"],
            "chapters_completed": self.state["chapters_completed"],
            "chapters_failed": self.state["chapters_failed"],
            "chapter_sub_phases": self.state["chapter_sub_phases"],
            "markers_count": self.state.get("markers_count", {}),
        }


class CoverageGuardian:
    """Per-source coverage checking, patch-style detection, chapter coverage guards."""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.output_dir = self.run_dir / "output"

    def _extract_source_from_marker(self, marker: str) -> Optional[str]:
        """Extract source name from integration marker.

        Handles formats:
          - WillCh4-...
          - [Will]Ch4-...
          - willCh4-...
          - Will-Ch4-...
        """
        # Remove leading <!-- integrated: and trailing -->
        marker = marker.replace("<!-- integrated:", "").replace("-->", "").strip()

        # Try [Source] format
        bracket_match = re.match(r'\[([^\]]+)\]', marker)
        if bracket_match:
            source = bracket_match.group(1)
            return SOURCE_ALIASES.get(source.lower(), source.title())

        # Try SourceCh or Source-Ch format
        for pattern in [r'^([A-Za-z]+)Ch', r'^([A-Za-z]+)-Ch', r'^([A-Za-z]+)_Ch']:
            match = re.match(pattern, marker)
            if match:
                source = match.group(1)
                return SOURCE_ALIASES.get(source.lower(), source.title())

        # Try to match known sources directly
        for source in KNOWN_SOURCES:
            if marker.lower().startswith(source.lower()):
                return source

        return None

    def count_markers_per_source(self) -> Dict[str, int]:
        """Count integration markers per source across all chapters."""
        counts = defaultdict(int)

        if not self.output_dir.exists():
            return dict(counts)

        for chapter_file in self.output_dir.glob("*.html"):
            content = chapter_file.read_text()
            markers = re.findall(r'<!-- integrated:.*?-->', content)
            for marker in markers:
                source = self._extract_source_from_marker(marker)
                if source:
                    counts[source] += 1

        return dict(counts)

    def get_chapter_markers(self, chapter: str) -> Dict[str, List[str]]:
        """Get markers per source for a specific chapter."""
        chapter_file = self.output_dir / f"{chapter}.html"
        if not chapter_file.exists():
            return {}

        content = chapter_file.read_text()
        markers = re.findall(r'<!-- integrated:.*?-->', content)

        by_source = defaultdict(list)
        for marker in markers:
            source = self._extract_source_from_marker(marker)
            if source:
                by_source[source].append(marker)

        return dict(by_source)

    def check_coverage_ratio(self) -> Tuple[bool, Dict]:
        """Check per-source coverage ratio (floor: 10%).

        Returns: (passed, details)
        """
        counts = self.count_markers_per_source()
        if not counts:
            return False, {"reason": "No markers found", "counts": {}}

        total = sum(counts.values())
        issues = []
        ratios = {}

        for source, count in counts.items():
            ratio = count / total if total > 0 else 0
            ratios[source] = {"count": count, "ratio": f"{ratio:.1%}"}
            if ratio < 0.10:
                issues.append(f"{source}: {count} markers ({ratio:.1%} < 10% floor)")

        passed = len(issues) == 0
        return passed, {
            "passed": passed,
            "total_markers": total,
            "ratios": ratios,
            "issues": issues,
        }

    def detect_patch_style(self) -> Tuple[bool, Dict]:
        """Detect patch-style integration (source concentrated in <=2 chapters).

        Returns: (is_patch_style, details)
        """
        source_chapters = defaultdict(set)

        if not self.output_dir.exists():
            return False, {"reason": "Output directory not found"}

        for chapter_file in self.output_dir.glob("*.html"):
            chapter_name = chapter_file.stem
            content = chapter_file.read_text()
            markers = re.findall(r'<!-- integrated:.*?-->', content)
            for marker in markers:
                source = self._extract_source_from_marker(marker)
                if source:
                    source_chapters[source].add(chapter_name)

        total_chapters = len(list(self.output_dir.glob("*.html")))
        patch_sources = []

        for source, chapters in source_chapters.items():
            if len(chapters) <= 2 and total_chapters > 2:
                patch_sources.append({
                    "source": source,
                    "chapters": list(chapters),
                    "chapter_count": len(chapters),
                })

        is_patch = len(patch_sources) > 0
        return is_patch, {
            "is_patch_style": is_patch,
            "total_chapters": total_chapters,
            "patch_sources": patch_sources,
            "source_chapter_distribution": {s: list(ch) for s, ch in source_chapters.items()},
        }

    def check_first_marker_position(self) -> Dict:
        """Check if each source is ever the first marker in a section.

        Patch-style sources are never first.
        """
        first_markers = defaultdict(list)

        if not self.output_dir.exists():
            return {}

        for chapter_file in self.output_dir.glob("*.html"):
            content = chapter_file.read_text()
            # Find sections by splitting on h2/h3 tags (including their content)
            # Use re.DOTALL so . matches newlines within heading tags
            sections = re.split(r'<h[23][^>]*>.*?</h[23]>', content, flags=re.DOTALL)
            for i, section in enumerate(sections[1:], 1):  # Skip pre-first-section content
                marker_match = re.search(r'<!-- integrated:.*?-->', section)
                if marker_match:
                    source = self._extract_source_from_marker(marker_match.group())
                    if source:
                        first_markers[source].append(f"{chapter_file.stem}:section{i}")

        never_first = []
        for source in KNOWN_SOURCES:
            if source not in first_markers:
                never_first.append(source)

        return {
            "sources_as_first_marker": {s: len(v) for s, v in first_markers.items()},
            "never_first": never_first,
        }

    def check_chapter_coverage(self, chapter: str) -> Tuple[bool, Dict]:
        """G7: Each source >=3 markers in chapter, G8: Size guard.

        Returns: (passed, details)
        """
        markers_by_source = self.get_chapter_markers(chapter)

        issues = []
        for source in KNOWN_SOURCES:
            count = len(markers_by_source.get(source, []))
            if count < 3:
                issues.append(f"G7: {source} has only {count} markers (min 3)")

        # G8: Size guard - check chapter file size
        chapter_file = self.output_dir / f"{chapter}.html"
        if chapter_file.exists():
            size = chapter_file.stat().st_size
            line_count = len(chapter_file.read_text().splitlines())
            if size < 10000:  # 10KB minimum
                issues.append(f"G8: Chapter size {size} bytes < 10KB minimum")
            if line_count < 100:
                issues.append(f"G8: Chapter has only {line_count} lines < 100 minimum")
        else:
            issues.append(f"Chapter file {chapter}.html not found")

        passed = len(issues) == 0
        return passed, {
            "passed": passed,
            "chapter": chapter,
            "markers_by_source": {s: len(m) for s, m in markers_by_source.items()},
            "issues": issues,
        }

    def generate_coverage_report(self) -> Dict:
        """Generate comprehensive coverage report."""
        ratio_passed, ratio_details = self.check_coverage_ratio()
        is_patch, patch_details = self.detect_patch_style()
        first_marker_info = self.check_first_marker_position()

        return {
            "per_source_coverage": ratio_details,
            "patch_style_detection": patch_details,
            "first_marker_analysis": first_marker_info,
            "summary": {
                "ratio_check_passed": ratio_passed,
                "patch_style_detected": is_patch,
                "recommendations": [],
            }
        }


class GateChecker:
    """Specific gate checkers for each sub-phase."""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.kb_dir = self.run_dir / ".book-doc" / "knowledge_base"

    # Phase 0 gates
    def check_0_1(self) -> Dict:
        """0.1: Source inventory check - all source books identified."""
        if not self.kb_dir.exists():
            return {"passed": False, "reason": "Knowledge base directory not found"}

        source_dirs = [d.name for d in self.kb_dir.iterdir() if d.is_dir() and d.name != "INDEX"]
        if len(source_dirs) < 2:
            return {"passed": False, "reason": f"Only {len(source_dirs)} source directories found (min 2)"}

        return {"passed": True, "reason": f"Found {len(source_dirs)} source directories: {', '.join(source_dirs)}"}

    def check_0_2(self) -> Dict:
        """0.2: TOC extraction - each source has toc.md."""
        if not self.kb_dir.exists():
            return {"passed": False, "reason": "Knowledge base directory not found"}

        issues = []
        for source_dir in self.kb_dir.iterdir():
            if source_dir.is_dir() and source_dir.name != "INDEX":
                toc_file = source_dir / "toc.md"
                if not toc_file.exists():
                    issues.append(f"{source_dir.name}: missing toc.md")

        if issues:
            return {"passed": False, "reason": "; ".join(issues)}
        return {"passed": True, "reason": "All sources have toc.md"}

    def check_0_3(self) -> Dict:
        """0.3: Knowledge indexing started - index.md exists for each source."""
        if not self.kb_dir.exists():
            return {"passed": False, "reason": "Knowledge base directory not found"}

        issues = []
        for source_dir in self.kb_dir.iterdir():
            if source_dir.is_dir() and source_dir.name != "INDEX":
                index_file = source_dir / "index.md"
                if not index_file.exists():
                    issues.append(f"{source_dir.name}: missing index.md")
                else:
                    line_count = len(index_file.read_text().splitlines())
                    if line_count < 100:
                        issues.append(f"{source_dir.name}: index.md only {line_count} lines (min 100)")

        if issues:
            return {"passed": False, "reason": "; ".join(issues)}
        return {"passed": True, "reason": "All sources have index.md with >=100 lines"}

    def check_0_4(self) -> Dict:
        """0.4: Cross-source mapping - INDEX directory with cross-reference files."""
        index_dir = self.kb_dir / "INDEX"
        if not index_dir.exists():
            return {"passed": False, "reason": "INDEX directory not found"}

        required_files = ["topic_index.md", "source_coverage.md"]
        missing = [f for f in required_files if not (index_dir / f).exists()]

        if missing:
            return {"passed": False, "reason": f"INDEX missing: {missing}"}
        return {"passed": True, "reason": "INDEX directory complete with cross-references"}

    def check_0_5(self) -> Dict:
        """0.5: Knowledge indexes complete - each >=1000 lines with required sections."""
        if not self.kb_dir.exists():
            return {"passed": False, "reason": "Knowledge base directory not found"}

        issues = []
        index_files = list(self.kb_dir.glob("*/index.md"))
        index_files = [f for f in index_files if f.parent.name != "INDEX"]

        if not index_files:
            return {"passed": False, "reason": "No knowledge index files found"}

        for idx_file in index_files:
            book_name = idx_file.parent.name
            line_count = len(idx_file.read_text().splitlines())

            if line_count < 1000:
                issues.append(f"{book_name}: {line_count} lines (min 1000)")

            content = idx_file.read_text()
            required = ["整体教学哲学", "逐章深度分析", "跨章主题映射", "整合准备摘要"]
            missing = [s for s in required if s not in content]
            if missing:
                issues.append(f"{book_name}: missing sections: {missing}")

        if issues:
            return {"passed": False, "reason": "; ".join(issues)}

        return {"passed": True, "reason": f"{len(index_files)} knowledge indexes verified, all >=1000 lines"}

    # Phase 1 gates
    def check_1_1(self) -> Dict:
        """1.1: Book portraits drafted - source-architecture.md has Book portraits section."""
        arch_file = self.run_dir / "source-architecture.md"
        if not arch_file.exists():
            return {"passed": False, "reason": "source-architecture.md not found"}

        content = arch_file.read_text()
        if "Book portraits" not in content and "书籍画像" not in content:
            return {"passed": False, "reason": "source-architecture.md missing Book portraits section"}

        return {"passed": True, "reason": "Book portraits section found"}

    def check_1_2(self) -> Dict:
        """1.2: Knowledge graph created - source-architecture.md has Knowledge graph section."""
        arch_file = self.run_dir / "source-architecture.md"
        if not arch_file.exists():
            return {"passed": False, "reason": "source-architecture.md not found"}

        content = arch_file.read_text()
        if "Knowledge graph" not in content and "知识图谱" not in content:
            return {"passed": False, "reason": "source-architecture.md missing Knowledge graph section"}

        return {"passed": True, "reason": "Knowledge graph section found"}

    def check_1_3(self) -> Dict:
        """1.3: TOC synthesis - source-architecture.md has Table of contents section."""
        arch_file = self.run_dir / "source-architecture.md"
        if not arch_file.exists():
            return {"passed": False, "reason": "source-architecture.md not found"}

        content = arch_file.read_text()
        if "Table of contents" not in content and "目录合成" not in content:
            return {"passed": False, "reason": "source-architecture.md missing Table of contents section"}

        return {"passed": True, "reason": "Table of contents section found"}

    def check_1_4(self) -> Dict:
        """1.4: Coverage matrix - source-architecture.md has Coverage matrix section."""
        arch_file = self.run_dir / "source-architecture.md"
        if not arch_file.exists():
            return {"passed": False, "reason": "source-architecture.md not found"}

        content = arch_file.read_text()
        if "Coverage matrix" not in content and "覆盖矩阵" not in content:
            return {"passed": False, "reason": "source-architecture.md missing Coverage matrix section"}

        return {"passed": True, "reason": "Coverage matrix section found"}

    def check_1_5(self) -> Dict:
        """1.5: Methodology analysis - source-architecture.md has methodology section."""
        arch_file = self.run_dir / "source-architecture.md"
        if not arch_file.exists():
            return {"passed": False, "reason": "source-architecture.md not found"}

        content = arch_file.read_text()
        if "方法论" not in content and "Methodology" not in content:
            return {"passed": False, "reason": "source-architecture.md missing methodology section"}

        return {"passed": True, "reason": "Methodology section found"}

    def check_1_6(self) -> Dict:
        """1.6: Per-chapter plans - plan.md with all chapter integration plans."""
        plan_file = self.run_dir / "plan.md"
        if not plan_file.exists():
            return {"passed": False, "reason": "plan.md not found"}

        content = plan_file.read_text()

        # Check for per-chapter integration plans
        chapter_plans = re.findall(r'## 第 \d+ 章整合计划', content)
        if not chapter_plans:
            chapter_plans = re.findall(r'## Ch\d+ Integration Plan', content)

        if not chapter_plans:
            return {"passed": False, "reason": "plan.md has no per-chapter integration plans"}

        # Check for TBD / placeholder content
        tbd_count = content.count("TBD") + content.count("待定")
        if tbd_count > 0:
            return {"passed": False, "reason": f"plan.md has {tbd_count} TBD/待定 placeholders"}

        # Check each plan has required fields
        plan_required = ["来源映射", "方法论选择", "深度对齐", "内容合成方案", "术语约定"]
        plan_required_en = ["Source map", "Methodology", "Depth", "Synthesis", "Terms"]
        plan_missing = []
        for req, req_en in zip(plan_required, plan_required_en):
            if req not in content and req_en not in content:
                plan_missing.append(req)

        if plan_missing:
            return {"passed": False, "reason": f"plan.md missing required fields: {plan_missing}"}

        return {"passed": True, "reason": f"plan.md has {len(chapter_plans)} chapter plans with all required fields"}

    # Phase 2 gates (per chapter)
    def check_2_1(self, chapter: str) -> Dict:
        """2.1: Chapter outline created - chapter outline file exists."""
        outline_file = self.run_dir / "outlines" / f"{chapter}.md"
        if not outline_file.exists():
            return {"passed": False, "reason": f"Outline file {chapter}.md not found in outlines/"}

        content = outline_file.read_text()
        if len(content.splitlines()) < 20:
            return {"passed": False, "reason": f"Outline too short: {len(content.splitlines())} lines (min 20)"}

        return {"passed": True, "reason": f"Chapter outline created with {len(content.splitlines())} lines"}

    def check_2_2(self, chapter: str) -> Dict:
        """2.2: Source mapping - outline has source references for each section."""
        outline_file = self.run_dir / "outlines" / f"{chapter}.md"
        if not outline_file.exists():
            return {"passed": False, "reason": f"Outline file {chapter}.md not found"}

        content = outline_file.read_text()
        # Check for source references
        source_refs = 0
        for source in KNOWN_SOURCES:
            source_refs += content.count(source)

        if source_refs < 3:
            return {"passed": False, "reason": f"Only {source_refs} source references in outline (min 3)"}

        return {"passed": True, "reason": f"Outline has {source_refs} source references"}

    def check_2_3(self, chapter: str) -> Dict:
        """2.3: Content drafted - chapter HTML exists with basic structure."""
        chapter_file = self.run_dir / "output" / f"{chapter}.html"
        if not chapter_file.exists():
            return {"passed": False, "reason": f"Chapter file {chapter}.html not found"}

        content = chapter_file.read_text()
        # Check basic HTML structure
        if "<html" not in content.lower() or "</html>" not in content.lower():
            return {"passed": False, "reason": "Chapter file missing HTML structure"}

        # Check for headings
        headings = len(re.findall(r'<h[1-6]', content, re.IGNORECASE))
        if headings < 3:
            return {"passed": False, "reason": f"Only {headings} headings (min 3)"}

        return {"passed": True, "reason": f"Chapter HTML created with {headings} headings"}

    def check_2_4(self, chapter: str) -> Dict:
        """2.4: Integration markers added - G1, G2, G3 checks."""
        chapter_file = self.run_dir / "output" / f"{chapter}.html"
        if not chapter_file.exists():
            return {"passed": False, "reason": f"Chapter file {chapter}.html not found"}

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

        issues = []
        if markers == 0:
            issues.append("No integration markers (G1)")
        if code_blocks > 0 and verified_blocks < code_blocks:
            issues.append(f"Code not fully verified: {verified_blocks}/{code_blocks} (G2)")
        if hits > 0:
            issues.append(f"Translationese detected: {hits} hits (G3)")

        if issues:
            return {"passed": False, "reason": "; ".join(issues), "details": results}

        return {"passed": True, "reason": f"Markers: {markers}, Code: {verified_blocks}/{code_blocks}, Translationese: {hits}", "details": results}

    def check_2_5(self, chapter: str) -> Dict:
        """2.5: Chapter validated - G6, G7, G8 checks."""
        chapter_file = self.run_dir / "output" / f"{chapter}.html"
        if not chapter_file.exists():
            return {"passed": False, "reason": f"Chapter file {chapter}.html not found"}

        content = chapter_file.read_text()
        line_count = len(content.splitlines())

        # G6: Depth check
        if line_count < 50:
            return {"passed": False, "reason": f"Chapter too short: {line_count} lines (G6)"}

        # G7, G8: Coverage checks
        guardian = CoverageGuardian(str(self.run_dir))
        coverage_passed, coverage_details = guardian.check_chapter_coverage(chapter)

        if not coverage_passed:
            return {"passed": False, "reason": "; ".join(coverage_details["issues"]), "details": coverage_details}

        return {"passed": True, "reason": f"Chapter validated: {line_count} lines, coverage OK", "details": coverage_details}

    # Phase 3 gates
    def check_3_1(self) -> Dict:
        """3.1: All chapters generated - check chapter count."""
        output_dir = self.run_dir / "output"
        if not output_dir.exists():
            return {"passed": False, "reason": "Output directory not found"}

        chapters = list(output_dir.glob("*.html"))
        if len(chapters) < 1:
            return {"passed": False, "reason": "No chapter files found"}

        return {"passed": True, "reason": f"Found {len(chapters)} chapter files"}

    def check_3_2(self) -> Dict:
        """3.2: Cross-chapter consistency - batch check."""
        output_dir = self.run_dir / "output"
        if not output_dir.exists():
            return {"passed": False, "reason": "Output directory not found"}

        chapters = sorted(output_dir.glob("*.html"))
        if len(chapters) < 2:
            return {"passed": True, "reason": "Less than 2 chapters, batch check not needed"}

        # Cross-chapter terminology consistency
        all_content = ""
        for ch in chapters:
            all_content += ch.read_text() + "\n"

        # Check for duplicate explanations
        paragraphs = re.findall(r'<p>(.*?)</p>', all_content, re.DOTALL)
        seen = set()
        duplicates = []
        for p in paragraphs:
            normalized = p.strip()[:100]
            if normalized in seen:
                duplicates.append(normalized[:50])
            seen.add(normalized)

        if len(duplicates) > 3:
            return {"passed": False, "reason": f"Found {len(duplicates)} duplicate paragraphs across chapters"}

        return {"passed": True, "reason": f"Batch check passed: {len(chapters)} chapters, {len(duplicates)} minor duplicates"}

    def check_3_3(self) -> Dict:
        """3.3: Coverage validation - >=95% coverage."""
        coverage_file = self.run_dir / ".book-doc" / "knowledge_base" / "INDEX" / "source_coverage.md"
        coverage = 0
        if coverage_file.exists():
            content = coverage_file.read_text()
            match = re.search(r'Coverage:\s*(\d+)%', content)
            if match:
                coverage = int(match.group(1))

        if coverage < 95:
            return {"passed": False, "reason": f"Coverage {coverage}% < 95%"}

        return {"passed": True, "reason": f"Coverage {coverage}% >= 95%"}

    def check_3_4(self) -> Dict:
        """3.4: Final validation - all gates passed."""
        # Check all previous phase 3 gates
        gates = [
            self.check_3_1(),
            self.check_3_2(),
            self.check_3_3(),
        ]

        failed = [g for g in gates if not g["passed"]]
        if failed:
            return {"passed": False, "reason": f"Previous gates failed: {[g['reason'] for g in failed]}"}

        return {"passed": True, "reason": "All Phase 3 gates passed"}

    # Phase 4 gates
    def check_4_1(self) -> Dict:
        """4.1: Report drafted - report.md exists with required sections."""
        report_file = self.run_dir / "report.md"
        if not report_file.exists():
            return {"passed": False, "reason": "report.md not found"}

        content = report_file.read_text()
        required = ["Summary", "Scores", "Issues", "Fix batches"]
        required_cn = ["摘要", "评分", "问题", "修复"]
        missing = []
        for req, req_cn in zip(required, required_cn):
            if req not in content and req_cn not in content:
                missing.append(req)

        if missing:
            return {"passed": False, "reason": f"report.md missing: {missing}"}

        return {"passed": True, "reason": "report.md has all required sections"}

    def check_4_2(self) -> Dict:
        """4.2: Report finalized - all sections complete, no TBD."""
        report_file = self.run_dir / "report.md"
        if not report_file.exists():
            return {"passed": False, "reason": "report.md not found"}

        content = report_file.read_text()
        tbd_count = content.count("TBD") + content.count("待定")
        if tbd_count > 0:
            return {"passed": False, "reason": f"report.md has {tbd_count} TBD/待定 placeholders"}

        return {"passed": True, "reason": "report.md finalized, no TBD placeholders"}

    def check_gate(self, phase: str, sub_phase: str, chapter: Optional[str] = None) -> Dict:
        """Dispatch to appropriate gate checker."""
        checker_name = f"check_{phase}_{sub_phase.split('.')[-1]}"
        checker = getattr(self, checker_name, None)

        if not checker:
            return {"passed": True, "reason": f"Gate {phase}.{sub_phase} not implemented"}

        # Phase 2 gates need chapter parameter
        if phase == "2" and chapter:
            return checker(chapter)
        elif phase == "2":
            return {"passed": False, "reason": "Phase 2 gates require chapter parameter"}

        return checker()


def main():
    """CLI entry point."""
    if len(sys.argv) < 4:
        print("Usage: workflow.py <skill_dir> <run_dir> <command> [args]")
        print("Commands:")
        print("  status                                    - Show current workflow status")
        print("  check_gate <phase> [<sub_phase>] [chapter] - Check if a gate passes")
        print("  record_progress --phase N --sub-phase N [--chapter name]")
        print("            --status completed|failed [--markers count] [--gate-result json]")
        print("  coverage_report                           - Per-source coverage report")
        print("  coverage_guard <chapter>                  - Per-chapter coverage check")
        print("Phases: 0, 1, 2, 3, 4")
        print("Sub-phases: 0.1-0.5, 1.1-1.6, 2.1-2.5, 3.1-3.4, 4.1-4.2")
        sys.exit(1)

    skill_dir = sys.argv[1]
    run_dir = sys.argv[2]
    command = sys.argv[3]

    lock = SubPhaseWorkflowLock(run_dir)
    checker = GateChecker(run_dir)
    guardian = CoverageGuardian(run_dir)

    if command == "status":
        status = lock.get_status()
        print("=== Workflow Status ===")
        print(f"Current phase: {status['current_phase'] or 'Not started'}")
        print(f"Current sub-phase: {status['current_sub_phase'] or 'N/A'}")
        print(f"Completed phases: {status['completed_phases']}")
        print("")
        print("=== Sub-phase Progress ===")
        for phase, subs in SUB_PHASES.items():
            completed = status['completed_sub_phases'].get(phase, [])
            phase_status = "completed" if phase in status['completed_phases'] else "in-progress" if completed else "pending"
            print(f"Phase {phase}: {phase_status}")
            for sp in subs:
                sp_status = "completed" if sp in completed else "pending"
                print(f"  {sp}: {sp_status}")
        print("")
        print("=== Chapter Progress ===")
        print(f"Completed: {status['chapters_completed']}")
        print(f"Failed: {status['chapters_failed']}")
        if status['chapter_sub_phases']:
            print("Chapter sub-phase details:")
            for ch, subs in status['chapter_sub_phases'].items():
                print(f"  {ch}: {subs}")
        print("")
        print("=== Marker Statistics ===")
        for source, count in status.get('markers_count', {}).items():
            print(f"  {source}: {count} markers")

    elif command == "check_gate":
        if len(sys.argv) < 5:
            print("Usage: workflow.py <skill_dir> <run_dir> check_gate <phase> [<sub_phase>] [chapter]")
            sys.exit(1)

        phase = sys.argv[4]
        sub_phase = sys.argv[5] if len(sys.argv) > 5 else None
        chapter = sys.argv[6] if len(sys.argv) > 6 else None

        # If no sub_phase specified, check all sub-phases for the phase
        if not sub_phase:
            sub_phases = SUB_PHASES.get(phase, [])
            if not sub_phases:
                print(f"ERROR: Unknown phase: {phase}")
                sys.exit(1)

            print(f"=== Checking all Phase {phase} gates ===")
            all_passed = True
            for sp in sub_phases:
                can_enter, reason = lock.can_enter_sub_phase(phase, sp, chapter)
                if not can_enter:
                    print(f"SKIP {sp}: {reason}")
                    continue

                result = checker.check_gate(phase, sp, chapter)
                status = "PASS" if result["passed"] else "FAIL"
                print(f"{status} {sp}: {result['reason']}")
                if not result["passed"]:
                    all_passed = False

            sys.exit(0 if all_passed else 1)

        # Check specific sub-phase
        can_enter, reason = lock.can_enter_sub_phase(phase, sub_phase, chapter)
        if not can_enter:
            print(f"ERROR: Cannot enter sub-phase {sub_phase}. {reason}")
            sys.exit(1)

        result = checker.check_gate(phase, sub_phase, chapter)
        if result["passed"]:
            print(f"PASS: Gate {phase}.{sub_phase} passed. {result['reason']}")
        else:
            print(f"FAIL: Gate {phase}.{sub_phase} failed. {result['reason']}")
            if "details" in result:
                print(f"Details: {result['details']}")
            sys.exit(1)

    elif command == "record_progress":
        # Parse arguments
        args = sys.argv[4:]
        params = {
            "phase": None,
            "sub_phase": None,
            "chapter": None,
            "status": None,
            "markers": 0,
            "gate_result": None,
        }

        i = 0
        while i < len(args):
            if args[i] == "--phase" and i + 1 < len(args):
                params["phase"] = args[i + 1]
                i += 2
            elif args[i] == "--sub-phase" and i + 1 < len(args):
                params["sub_phase"] = args[i + 1]
                i += 2
            elif args[i] == "--chapter" and i + 1 < len(args):
                params["chapter"] = args[i + 1]
                i += 2
            elif args[i] == "--status" and i + 1 < len(args):
                params["status"] = args[i + 1]
                i += 2
            elif args[i] == "--markers" and i + 1 < len(args):
                params["markers"] = int(args[i + 1])
                i += 2
            elif args[i] == "--gate-result" and i + 1 < len(args):
                params["gate_result"] = json.loads(args[i + 1])
                i += 2
            else:
                i += 1

        if not params["phase"] or not params["sub_phase"] or not params["status"]:
            print("ERROR: --phase, --sub-phase, and --status are required")
            sys.exit(1)

        try:
            lock.record_progress(
                params["phase"],
                params["sub_phase"],
                params["status"],
                params["chapter"],
                params["markers"],
                params["gate_result"],
            )
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        print(f"Recorded: Phase {params['phase']}, Sub-phase {params['sub_phase']}, Status: {params['status']}")
        if params["chapter"]:
            print(f"  Chapter: {params['chapter']}")
        print(f"Progress file updated: {lock.progress_file}")

    elif command == "coverage_report":
        report = guardian.generate_coverage_report()
        print("=== Coverage Report ===")
        print("")
        print("--- Per-Source Coverage ---")
        ratios = report["per_source_coverage"].get("ratios", {})
        for source, data in ratios.items():
            print(f"  {source}: {data['count']} markers ({data['ratio']})")
        if report["per_source_coverage"].get("issues"):
            print(f"Issues: {report['per_source_coverage']['issues']}")
        print("")
        print("--- Patch-Style Detection ---")
        patch = report["patch_style_detection"]
        if patch["is_patch_style"]:
            print("WARNING: Patch-style integration detected!")
            for ps in patch["patch_sources"]:
                print(f"  {ps['source']}: only in {ps['chapters']}")
        else:
            print("OK: No patch-style integration detected")
        print("")
        print("--- First Marker Analysis ---")
        first = report["first_marker_analysis"]
        if first:
            for source, count in first.get("sources_as_first_marker", {}).items():
                print(f"  {source}: first marker in {count} sections")
            if first.get("never_first"):
                print(f"  WARNING - Never first in any section: {first['never_first']}")
        else:
            print("  No data available")
        print("")
        print("--- Summary ---")
        summary = report["summary"]
        print(f"Ratio check: {'PASS' if summary['ratio_check_passed'] else 'FAIL'}")
        print(f"Patch-style: {'DETECTED' if summary['patch_style_detected'] else 'OK'}")

    elif command == "coverage_guard":
        if len(sys.argv) < 5:
            print("Usage: workflow.py <skill_dir> <run_dir> coverage_guard <chapter>")
            sys.exit(1)

        chapter = sys.argv[4]
        passed, details = guardian.check_chapter_coverage(chapter)
        print(f"=== Coverage Guard for {chapter} ===")
        print(f"Status: {'PASS' if passed else 'FAIL'}")
        print("")
        print("--- Markers by Source ---")
        for source, count in details.get("markers_by_source", {}).items():
            status = "OK" if count >= 3 else "LOW"
            print(f"  {source}: {count} markers [{status}]")
        if details.get("issues"):
            print("")
            print("--- Issues ---")
            for issue in details["issues"]:
                print(f"  {issue}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
