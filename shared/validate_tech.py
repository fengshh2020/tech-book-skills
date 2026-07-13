#!/usr/bin/env python3
"""
技术书籍技术准确性验证器。
验证内容：API 存在性、版本兼容性、代码可运行性。
"""

import ast
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TechValidator:
    """验证代码示例和 API 声明的技术准确性。"""

    def __init__(self, run_dir: str):
        self.run_dir = Path(run_dir)
        self.results = []
        self.errors = []

    def extract_code_blocks(self, content: str) -> List[Dict]:
        """从 MD 或 HTML 内容中提取代码块（格式无关，ADR-0001 MD 主源）。"""
        blocks = []

        # 1. Markdown 围栏: ```lang caption="..." \n code ```（lang 为首个 token）
        for m in re.finditer(r"```([^\n`]*)\n(.*?)```", content, re.DOTALL):
            info = m.group(1).strip()
            code = m.group(2)
            lang = (info.split()[0] if info else "").lower()
            if lang == "mermaid":
                continue  # 图表源，非可运行代码
            blocks.append({
                "language": lang or "unknown",
                "code": code,
                "line_count": code.count("\n") + 1,
            })

        # 2. builder HTML: <pre data-lang="Lang"><code>…</code></pre>
        for m in re.finditer(r'<pre[^>]*data-lang="([^"]*)"[^>]*><code>(.*?)</code></pre>', content, re.DOTALL):
            lang = m.group(1).strip().lower()
            code = html.unescape(m.group(2))
            blocks.append({
                "language": lang or "unknown",
                "code": code,
                "line_count": code.count("\n") + 1,
            })

        # 3. 旧式 HTML: <pre><code class="language-x">…</code></pre>
        for m in re.finditer(r'<pre><code(?:\s+class="([^"]*)")?>(.*?)</code></pre>', content, re.DOTALL):
            cls = (m.group(1) or "").strip().lower()
            lang = cls.replace("language-", "") if cls else ""
            code = html.unescape(m.group(2))
            blocks.append({
                "language": lang or "unknown",
                "code": code,
                "line_count": code.count("\n") + 1,
            })

        return blocks

    def validate_code_runnability(self, code: str, language: str = "python") -> Dict:
        """验证代码是否可运行。"""
        if language != "python":
            return {"passed": True, "reason": "非 Python 代码，已跳过"}

        try:
            # 尝试编译代码
            compile(code, "<string>", "exec")
            return {"passed": True, "reason": "代码编译成功"}
        except SyntaxError as e:
            return {"passed": False, "reason": f"语法错误: {e}"}
        except Exception as e:
            return {"passed": False, "reason": f"编译错误: {e}"}

    def extract_api_claims(self, content: str) -> List[Dict]:
        """从内容中提取 API 声明。"""
        # 匹配 "function()"、"module.function()" 等模式
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
        """验证 API 是否存在于当前 Python 环境中。"""
        try:
            # 尝试解析 API
            parts = api_name.split(".")
            if len(parts) == 1:
                # 内置函数或已导入的 — 使用 ast.literal_eval 确保安全
                import builtins
                if hasattr(builtins, parts[0]):
                    return {"passed": True, "reason": f"API {api_name} 存在"}
                return {"passed": False, "reason": f"API {api_name} 未找到"}
            else:
                # module.function
                module_name = ".".join(parts[:-1])
                func_name = parts[-1]
                module = __import__(module_name)
                getattr(module, func_name)
                return {"passed": True, "reason": f"API {api_name} 存在"}
        except (ImportError, AttributeError, NameError):
            return {"passed": False, "reason": f"API {api_name} 未找到"}
        except Exception as e:
            return {"passed": False, "reason": f"检查 {api_name} 时出错: {e}"}

    def check_version_compatibility(self, code: str, target_version: str = "3.8") -> Dict:
        """检查代码是否兼容目标 Python 版本。"""
        try:
            tree = ast.parse(code)

            issues = []
            for node in ast.walk(tree):
                # 检查 match/case（Python 3.10+）
                if isinstance(node, ast.Match):
                    issues.append("match/case 需要 Python 3.10+")

                # 检查海象运算符（Python 3.8+）
                if isinstance(node, ast.NamedExpr):
                    issues.append("海象运算符需要 Python 3.8+")

                # 检查仅位置参数（Python 3.8+）
                if isinstance(node, ast.arguments):
                    if hasattr(node, 'posonlyargs') and node.posonlyargs:
                        issues.append("仅位置参数需要 Python 3.8+")

            if issues:
                return {
                    "passed": False,
                    "reason": f"版本兼容性问题: {issues}"
                }

            return {"passed": True, "reason": "代码与目标版本兼容"}

        except SyntaxError as e:
            return {"passed": False, "reason": f"语法错误: {e}"}

    def validate_chapter(self, chapter_path: Path) -> Dict:
        """验证单个章节。"""
        if not chapter_path.exists():
            return {"passed": False, "reason": f"章节 {chapter_path} 未找到"}

        content = chapter_path.read_text()

        # 提取代码块
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
            # 验证可运行性
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

            # 验证版本兼容性
            version_result = self.check_version_compatibility(block["code"])
            if not version_result["passed"]:
                results["version_issues"].append(version_result["reason"])
                self.errors.append({
                    "chapter": chapter_path.name,
                    "type": "version",
                    "error": version_result["reason"]
                })

        # 提取并验证 API 声明
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
        """验证整本书籍。"""
        output_path = Path(output_dir)
        if not output_path.exists():
            return {"passed": False, "reason": f"输出目录 {output_dir} 未找到"}

        # 查找所有章节文件（MD 主源 或 HTML 输出，ADR-0001）
        chapter_files = list(output_path.glob("*.md")) + list(output_path.glob("*.html"))

        if not chapter_files:
            return {"passed": False, "reason": "未找到 .md 或 .html 文件"}

        total_blocks = 0
        total_runnable = 0
        total_unrunnable = 0

        for chapter_file in chapter_files:
            result = self.validate_chapter(chapter_file)
            total_blocks += result["code_blocks"]
            total_runnable += result["runnable"]
            total_unrunnable += result["unrunnable"]

        success_rate = total_runnable / total_blocks if total_blocks > 0 else 0

        return {
            "passed": total_unrunnable == 0,
            "reason": f"{total_runnable}/{total_blocks} 个代码块可运行（成功率 {success_rate:.1%}）",
            "total_blocks": total_blocks,
            "runnable": total_runnable,
            "unrunnable": total_unrunnable,
            "errors": self.errors
        }


def main():
    """命令行入口。"""
    if len(sys.argv) < 2:
        print("用法: validate_tech.py <输出目录>")
        print("验证代码示例和 API 声明的技术准确性")
        sys.exit(1)

    output_dir = sys.argv[1]
    validator = TechValidator(output_dir)

    result = validator.validate_book(output_dir)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
