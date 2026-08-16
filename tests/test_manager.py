import argparse
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.manager import (
    DEFAULT_PROMPTS_DIR,
    command_docs,
    command_fill,
    command_stats,
    filter_prompts,
    find_variables,
    load_all_prompts,
    validate_prompt,
    validate_repository,
)


class ManagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompts = load_all_prompts(DEFAULT_PROMPTS_DIR)

    def test_repository_prompts_are_valid(self):
        self.assertEqual(validate_repository(DEFAULT_PROMPTS_DIR), {})

    def test_initial_library_has_every_category(self):
        categories = {prompt.category for prompt in self.prompts}
        self.assertEqual(
            categories,
            {"programming", "creative-writing", "visual-art", "audio-music", "productivity"},
        )

    def test_search_matches_title_tags_and_content(self):
        matches = filter_prompts(self.prompts, "Python")
        self.assertTrue(any(prompt.path == "programming/python-refactor.md" for prompt in matches))

    def test_category_filter(self):
        matches = filter_prompts(self.prompts, category="visual-art")
        self.assertTrue(matches)
        self.assertTrue(all(prompt.category == "visual-art" for prompt in matches))

    def test_validation_reports_non_string_category(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_dir = Path(temp_dir)
            path = self._write_prompt(prompts_dir, category='["programming"]')

            errors = validate_prompt(path, prompts_dir)

        self.assertTrue(any("category 必须是" in error for error in errors))

    def test_validation_rejects_unclosed_prompt_block(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_dir = Path(temp_dir)
            path = self._write_prompt(prompts_dir, close_fence=False)

            errors = validate_prompt(path, prompts_dir)

        self.assertIn("提示词正文必须放在完整的 ```text 代码块中", errors)

    def test_validation_allows_markdown_heading_inside_prompt_block(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            prompts_dir = Path(temp_dir)
            path = self._write_prompt(prompts_dir, content="请输出：\n### 分析结果")

            errors = validate_prompt(path, prompts_dir)

        self.assertEqual(errors, [])

    def test_docs_escape_titles_and_remove_stale_pages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            prompts_dir = project_root / "prompts"
            title = '包含"引号"的标题'
            self._write_prompt(prompts_dir, title=title)
            stale_page = project_root / "docs" / "library" / "programming" / "stale.md"
            stale_page.parent.mkdir(parents=True)
            stale_page.write_text("stale", encoding="utf-8")
            output = project_root / "docs" / "prompts" / "index.md"
            args = argparse.Namespace(prompts_dir=prompts_dir, output=output)

            with patch("src.manager.PROJECT_ROOT", project_root):
                result = command_docs(args)

            generated_page = project_root / "docs" / "library" / "programming" / "example.md"
            generated_text = generated_page.read_text(encoding="utf-8")
            stale_page_exists = stale_page.exists()

        self.assertEqual(result, 0)
        self.assertIn(f"title: {json.dumps(title, ensure_ascii=False)}", generated_text)
        self.assertFalse(stale_page_exists)

    def test_find_variables_preserves_order_and_supports_chinese(self):
        variables = find_variables("{{name}} / {{ name }} / {{主题}} / {{target-model}}")

        self.assertEqual(variables, ["name", "主题", "target-model"])

    def test_fill_replaces_variables_from_command_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            prompts_dir = project_root / "prompts"
            self._write_prompt(prompts_dir, content="你好，{{name}}！主题是 {{主题}}。")
            args = argparse.Namespace(
                path="prompts/programming/example.md",
                prompts_dir=prompts_dir,
                values=["name=小明", "主题=提示词管理"],
                output=None,
            )
            output = StringIO()

            with patch("src.manager.PROJECT_ROOT", project_root), redirect_stdout(output):
                result = command_fill(args)

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "你好，小明！主题是 提示词管理。\n")

    def test_stats_json_reports_library_totals(self):
        args = argparse.Namespace(prompts_dir=DEFAULT_PROMPTS_DIR, json=True)
        output = StringIO()

        with redirect_stdout(output):
            result = command_stats(args)

        report = json.loads(output.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(report["total"], len(self.prompts))
        self.assertEqual(sum(report["categories"].values()), len(self.prompts))
        self.assertIn("source_code", report["variables"])

    @staticmethod
    def _write_prompt(
        prompts_dir: Path,
        *,
        title: str = "测试提示词",
        category: str = '"programming"',
        content: str = "测试内容",
        close_fence: bool = True,
    ) -> Path:
        path = prompts_dir / "programming" / "example.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        closing = "```\n" if close_fence else ""
        path.write_text(
            "\n".join(
                [
                    "---",
                    f"title: {json.dumps(title, ensure_ascii=False)}",
                    f"category: {category}",
                    'target_model: "测试模型"',
                    'version: "1.0.0"',
                    'tags: ["测试"]',
                    'author: "测试作者"',
                    "---",
                    "",
                    "### 提示词内容",
                    "",
                    "```text",
                    content,
                    closing.rstrip("\n"),
                    "",
                    "### 使用说明与参数建议",
                    "",
                    "测试说明。",
                ]
            ),
            encoding="utf-8",
        )
        return path


if __name__ == "__main__":
    unittest.main()
