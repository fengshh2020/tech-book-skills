#!/usr/bin/env python3
"""
review-tech-book 技能的工作流编排器。
确保各阶段按顺序执行，门控检查通过后才继续下一阶段。
"""
import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional


class ReviewPhaseLock:
    """确保审阅阶段按顺序执行。"""

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
        """检查是否可以进入指定阶段。"""
        phase_order = ["1", "2", "3", "4", "fix"]
        if phase not in phase_order:
            return False

        idx = phase_order.index(phase)
        if idx == 0:
            return True

        prev_phase = phase_order[idx - 1]
        return prev_phase in self.state["completed_phases"]

    def mark_complete(self, phase: str, results: Dict):
        """标记阶段为已完成。"""
        self.state["completed_phases"].append(phase)
        self.state["current_phase"] = phase
        if "findings" in results:
            self.state["findings"][phase] = results["findings"]
        if "scores" in results:
            self.state["scores"][phase] = results["scores"]
        self._save_state()


def check_phase1_gate(run_dir: str) -> Dict:
    """检查阶段 1 门控：扫描完成。"""
    findings_file = Path(run_dir) / "findings" / "phase1.md"
    if not findings_file.exists():
        return {"passed": False, "reason": "findings/phase1.md 未找到"}

    content = findings_file.read_text()

    # 检查必要章节
    required = ["Target reader", "Learning path", "Anomalies", "Validation"]
    missing = [r for r in required if r not in content]
    if missing:
        return {"passed": False, "reason": f"缺少章节: {missing}"}

    return {"passed": True, "reason": "所有必要章节均已存在"}


def check_phase2_gate(run_dir: str) -> Dict:
    """检查阶段 2 门控：所有章节已阅读。"""
    findings_file = Path(run_dir) / "findings" / "phase2.md"
    if not findings_file.exists():
        return {"passed": False, "reason": "findings/phase2.md 未找到"}

    content = findings_file.read_text()

    # 统计有阅读证据的章节数
    chapters = re.findall(r'### (?:Skim|Deep):\s*Ch\d+', content)
    if len(chapters) < 1:
        return {"passed": False, "reason": "未找到章节阅读记录"}

    # 检查引用
    quotes = content.count("**Quote**:")
    if quotes < 1:
        return {"passed": False, "reason": "未找到带引用的发现"}

    return {"passed": True, "reason": f"已阅读 {len(chapters)} 个章节，{quotes} 条带引用的发现"}


def check_phase4_gate(run_dir: str) -> Dict:
    """检查阶段 4 门控：报告完成。"""
    report_file = Path(run_dir) / "report.md"
    if not report_file.exists():
        return {"passed": False, "reason": "report.md 未找到"}

    content = report_file.read_text()

    # 检查必要章节
    required = ["Executive summary", "Score overview", "Top 3", "Learning path"]
    missing = [r for r in required if r not in content]
    if missing:
        return {"passed": False, "reason": f"缺少章节: {missing}"}

    return {"passed": True, "reason": "所有必要章节均已存在"}


def check_fix_gate(run_dir: str) -> Dict:
    """检查修复模式门控：所有批次已应用。"""
    fix_report = Path(run_dir) / "fix-report.md"
    if not fix_report.exists():
        return {"passed": False, "reason": "fix-report.md 未找到"}

    content = fix_report.read_text()

    # 检查批次完成情况
    batches = ["P0", "P1", "P2", "P3"]
    completed = [b for b in batches if f"{b} complete" in content]

    if len(completed) < 4:
        return {"passed": False, "reason": f"仅完成 {len(completed)}/4 个批次"}

    return {"passed": True, "reason": "全部 4 个批次已完成"}


def main():
    """命令行入口。"""
    if len(sys.argv) < 3:
        print("用法: review_workflow.py <运行目录> <命令> [参数]")
        print("命令: status, check_gate <阶段>")
        sys.exit(1)

    run_dir = sys.argv[1]
    command = sys.argv[2]

    lock = ReviewPhaseLock(run_dir)

    if command == "status":
        print(f"当前阶段: {lock.state['current_phase']}")
        print(f"已完成阶段: {lock.state['completed_phases']}")

    elif command == "check_gate":
        phase = sys.argv[3]
        if not lock.can_enter(phase):
            print(f"错误: 无法进入阶段 {phase}。前一阶段尚未完成。")
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
            result = {"passed": True, "reason": "门控检查尚未实现"}

        lock.mark_complete(phase, result)

        if result["passed"]:
            print(f"通过: 阶段 {phase} 门控检查已通过。{result['reason']}")
        else:
            print(f"失败: 阶段 {phase} 门控检查未通过。{result['reason']}")
            sys.exit(1)

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
