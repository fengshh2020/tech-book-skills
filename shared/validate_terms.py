#!/usr/bin/env python3
"""
Terminology consistency manager for tech books.
Manages: glossary, cross-book term conflicts, first-appearance rules.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class TerminologyManager:
    """Manages terminology consistency across books."""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.glossary_file = self.run_dir / ".book-doc" / "glossary.md"
        self.glossary = self._load_glossary()

    def _load_glossary(self) -> Dict[str, Dict]:
        """Load glossary from file."""
        if not self.glossary_file.exists():
            return {}

        content = self.glossary_file.read_text()
        glossary = {}

        # Parse glossary entries
        # Format: | English | Chinese | First Appearance | Status |
        lines = content.split("\n")
        for line in lines:
            if line.startswith("|") and "English" not in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    english = parts[1]
                    chinese = parts[2]
                    first_appearance = parts[3]
                    status = parts[4] if len(parts) > 4 else "pending"

                    glossary[english.lower()] = {
                        "english": english,
                        "chinese": chinese,
                        "first_appearance": first_appearance,
                        "status": status
                    }

        return glossary

    def _save_glossary(self):
        """Save glossary to file."""
        self.glossary_file.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "# Glossary",
            "",
            "| English | Chinese | First Appearance | Status |",
            "|---------|---------|------------------|--------|"
        ]

        for term in sorted(self.glossary.values(), key=lambda x: x["english"]):
            lines.append(
                f"| {term['english']} | {term['chinese']} | {term['first_appearance']} | {term['status']} |"
            )

        self.glossary_file.write_text("\n".join(lines))

    def extract_terms(self, content: str) -> List[Dict]:
        """Extract terms from content."""
        terms = []

        # Find terms in format "中文（english）"
        pattern = r'([一-鿿]+)（([a-zA-Z_]+)）'
        matches = re.findall(pattern, content)

        for chinese, english in matches:
            terms.append({
                "chinese": chinese,
                "english": english,
                "type": "first_appearance"
            })

        # Find terms in format "english（中文）"
        pattern = r'([a-zA-Z_]+)（([一-鿿]+)）'
        matches = re.findall(pattern, content)

        for english, chinese in matches:
            terms.append({
                "chinese": chinese,
                "english": english,
                "type": "first_appearance"
            })

        return terms

    def check_term_consistency(self, content: str, chapter: str) -> List[Dict]:
        """Check term consistency in content."""
        issues = []

        # Check each glossary term
        for english, term in self.glossary.items():
            chinese = term["chinese"]

            # Count occurrences
            english_count = len(re.findall(rf'\b{re.escape(english)}\b', content, re.IGNORECASE))
            chinese_count = content.count(chinese)

            # Check first appearance rule
            if english_count > 0 or chinese_count > 0:
                # Should have "中文（english）" on first appearance
                first_pattern = rf'{re.escape(chinese)}（{re.escape(english)}）'
                first_matches = re.findall(first_pattern, content)

                if not first_matches and (english_count > 0 or chinese_count > 0):
                    issues.append({
                        "type": "missing_first_appearance",
                        "term": english,
                        "chinese": chinese,
                        "chapter": chapter,
                        "reason": f"Term '{chinese}（{english}）' not found with proper first-appearance annotation"
                    })

        return issues

    def check_cross_book_conflicts(self, other_glossaries: List[Dict]) -> List[Dict]:
        """Check for conflicts between glossaries."""
        conflicts = []

        for other in other_glossaries:
            for english, term in other.items():
                if english in self.glossary:
                    if self.glossary[english]["chinese"] != term["chinese"]:
                        conflicts.append({
                            "type": "translation_conflict",
                            "term": english,
                            "this_translation": self.glossary[english]["chinese"],
                            "other_translation": term["chinese"],
                            "reason": f"Term '{english}' has different translations"
                        })

        return conflicts

    def validate_chapter(self, chapter_path: Path) -> Dict:
        """Validate terminology in a chapter."""
        if not chapter_path.exists():
            return {"passed": False, "reason": f"Chapter {chapter_path} not found"}

        content = chapter_path.read_text()

        # Extract terms
        terms = self.extract_terms(content)

        # Check consistency
        issues = self.check_term_consistency(content, chapter_path.name)

        # Update glossary with new terms
        for term in terms:
            english = term["english"].lower()
            if english not in self.glossary:
                self.glossary[english] = {
                    "english": term["english"],
                    "chinese": term["chinese"],
                    "first_appearance": chapter_path.name,
                    "status": "found"
                }

        self._save_glossary()

        return {
            "passed": len(issues) == 0,
            "reason": f"{len(issues)} terminology issues found" if issues else "All terms consistent",
            "terms_found": len(terms),
            "issues": issues
        }

    def validate_book(self, output_dir: str) -> Dict:
        """Validate terminology across entire book."""
        output_path = Path(output_dir)
        if not output_path.exists():
            return {"passed": False, "reason": f"Output directory {output_dir} not found"}

        html_files = list(output_path.glob("*.html"))

        if not html_files:
            return {"passed": False, "reason": "No HTML files found"}

        total_issues = 0
        all_issues = []

        for html_file in html_files:
            result = self.validate_chapter(html_file)
            total_issues += len(result.get("issues", []))
            all_issues.extend(result.get("issues", []))

        return {
            "passed": total_issues == 0,
            "reason": f"{total_issues} terminology issues across {len(html_files)} chapters",
            "total_issues": total_issues,
            "issues": all_issues
        }


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: validate_terms.py <output_dir>")
        print("Validates terminology consistency in tech books")
        sys.exit(1)

    output_dir = sys.argv[1]
    manager = TerminologyManager(output_dir)

    result = manager.validate_book(output_dir)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
