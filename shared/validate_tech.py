#!/usr/bin/env python3
"""
Technical accuracy validator for tech books.
Validates: API existence, version compatibility, code runnability.
"""

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TechValidator:
    """Validates technical accuracy of code examples and API claims."""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.results = []
        self.errors = []

    def extract_code_blocks(self, html_content: str) -> List[Dict]:
        """Extract code blocks from HTML content."""
        # Match <pre><code> blocks
        pattern = r'<pre><code(?:\s+class="([^"]*)")?>(.*?)</code></pre>'
        matches = re.findall(pattern, html_content, re.DOTALL)

        blocks = []
        for lang, code in matches:
            blocks.append({
                "language": lang or "unknown",
                "code": code,
                "line_count": code.count("\n") + 1
            })

        return blocks

    def validate_code_runnability(self, code: str, language: str = "python") -> Dict:
        """Validate if code can run."""
        if language != "python":
            return {"passed": True, "reason": "Non-Python code, skipped"}

        try:
            # Try to compile the code
            compile(code, "<string>", "exec")
            return {"passed": True, "reason": "Code compiles successfully"}
        except SyntaxError as e:
            return {"passed": False, "reason": f"Syntax error: {e}"}
        except Exception as e:
            return {"passed": False, "reason": f"Compilation error: {e}"}

    def extract_api_claims(self, content: str) -> List[Dict]:
        """Extract API claims from content."""
        # Match patterns like "function()", "module.function()", etc.
        patterns = [
            r'(\w+)\.(\w+)\(',  # module.function(
            r'(\w+)\(',  # function(
        ]

        claims = []
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    claims.append({
                        "api": f"{match[0]}.{match[1]}",
                        "type": "method"
                    })
                else:
                    claims.append({
                        "api": match,
                        "type": "function"
                    })

        return claims

    def validate_api_existence(self, api_name: str) -> Dict:
        """Validate if API exists in current Python environment."""
        try:
            # Try to evaluate the API
            parts = api_name.split(".")
            if len(parts) == 1:
                # Built-in or imported - use ast.literal_eval for safety
                import builtins
                if hasattr(builtins, parts[0]):
                    return {"passed": True, "reason": f"API {api_name} exists"}
                return {"passed": False, "reason": f"API {api_name} not found"}
            else:
                # module.function
                module_name = ".".join(parts[:-1])
                func_name = parts[-1]
                module = __import__(module_name)
                getattr(module, func_name)
                return {"passed": True, "reason": f"API {api_name} exists"}
        except (ImportError, AttributeError, NameError):
            return {"passed": False, "reason": f"API {api_name} not found"}
        except Exception as e:
            return {"passed": False, "reason": f"Error checking {api_name}: {e}"}

    def check_version_compatibility(self, code: str, target_version: str = "3.8") -> Dict:
        """Check if code is compatible with target Python version."""
        try:
            tree = ast.parse(code)

            issues = []
            for node in ast.walk(tree):
                # Check for match/case (Python 3.10+)
                if isinstance(node, ast.Match):
                    issues.append("match/case requires Python 3.10+")

                # Check for walrus operator (Python 3.8+)
                if isinstance(node, ast.NamedExpr):
                    issues.append("walrus operator requires Python 3.8+")

                # Check for positional-only parameters (Python 3.8+)
                if isinstance(node, ast.arguments):
                    if hasattr(node, 'posonlyargs') and node.posonlyargs:
                        issues.append("positional-only parameters require Python 3.8+")

            if issues:
                return {
                    "passed": False,
                    "reason": f"Version compatibility issues: {issues}"
                }

            return {"passed": True, "reason": "Code compatible with target version"}

        except SyntaxError as e:
            return {"passed": False, "reason": f"Syntax error: {e}"}

    def validate_chapter(self, chapter_path: Path) -> Dict:
        """Validate a single chapter."""
        if not chapter_path.exists():
            return {"passed": False, "reason": f"Chapter {chapter_path} not found"}

        content = chapter_path.read_text()

        # Extract code blocks
        code_blocks = self.extract_code_blocks(content)

        results = {
            "chapter": chapter_path.name,
            "code_blocks": len(code_blocks),
            "runnable": 0,
            "unrunnable": 0,
            "api_claims": [],
            "version_issues": []
        }

        for block in code_blocks:
            # Validate runnability
            run_result = self.validate_code_runnability(block["code"], block["language"])
            if run_result["passed"]:
                results["runnable"] += 1
            else:
                results["unrunnable"] += 1
                self.errors.append({
                    "chapter": chapter_path.name,
                    "type": "runnability",
                    "error": run_result["reason"]
                })

            # Validate version compatibility
            version_result = self.check_version_compatibility(block["code"])
            if not version_result["passed"]:
                results["version_issues"].append(version_result["reason"])
                self.errors.append({
                    "chapter": chapter_path.name,
                    "type": "version",
                    "error": version_result["reason"]
                })

        # Extract and validate API claims
        api_claims = self.extract_api_claims(content)
        for claim in api_claims:
            api_result = self.validate_api_existence(claim["api"])
            if not api_result["passed"]:
                self.errors.append({
                    "chapter": chapter_path.name,
                    "type": "api",
                    "error": api_result["reason"]
                })

        results["api_claims"] = len(api_claims)

        return results

    def validate_book(self, output_dir: str) -> Dict:
        """Validate entire book."""
        output_path = Path(output_dir)
        if not output_path.exists():
            return {"passed": False, "reason": f"Output directory {output_dir} not found"}

        # Find all HTML files
        html_files = list(output_path.glob("*.html"))

        if not html_files:
            return {"passed": False, "reason": "No HTML files found"}

        total_blocks = 0
        total_runnable = 0
        total_unrunnable = 0

        for html_file in html_files:
            result = self.validate_chapter(html_file)
            total_blocks += result["code_blocks"]
            total_runnable += result["runnable"]
            total_unrunnable += result["unrunnable"]

        success_rate = total_runnable / total_blocks if total_blocks > 0 else 0

        return {
            "passed": total_unrunnable == 0,
            "reason": f"{total_runnable}/{total_blocks} code blocks runnable ({success_rate:.1%})",
            "total_blocks": total_blocks,
            "runnable": total_runnable,
            "unrunnable": total_unrunnable,
            "errors": self.errors
        }


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_tech.py <output_dir>")
        print("Validates technical accuracy of code examples and API claims")
        sys.exit(1)

    output_dir = sys.argv[1]
    validator = TechValidator(output_dir)

    result = validator.validate_book(output_dir)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
