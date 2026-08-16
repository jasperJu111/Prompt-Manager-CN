#!/usr/bin/env python3
"""提示管理器-CN：提示词检索、校验、导出和文档生成工具。"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPTS_DIR = PROJECT_ROOT / "prompts"
ALLOWED_CATEGORIES = {
    "programming",
    "creative-writing",
    "visual-art",
    "audio-music",
    "productivity",
}
REQUIRED_FIELDS = {"title", "category", "target_model", "version", "tags", "author"}
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class PromptRecord:
    path: str
    title: str
    category: str
    target_model: str
    version: str
    tags: list[str]
    author: str
    content: str


def _parse_value(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return ""
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return raw


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """解析项目使用的简单 YAML Frontmatter，不依赖第三方库。"""
    match = FRONTMATTER_PATTERN.search(text)
    if not match:
        raise ValueError("缺少由 --- 包围的 YAML Frontmatter")
    metadata: dict[str, Any] = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"第 {line_number} 行不是 key: value 格式")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"第 {line_number} 行的字段名为空")
        if key in metadata:
            raise ValueError(f"字段 {key!r} 重复")
        metadata[key] = _parse_value(raw_value)
    return metadata, text[match.end() :].strip()


def load_prompt(path: Path, prompts_dir: Path = DEFAULT_PROMPTS_DIR) -> PromptRecord:
    metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    relative_path = path.resolve().relative_to(prompts_dir.resolve()).as_posix()
    return PromptRecord(
        path=relative_path,
        title=str(metadata.get("title", "")),
        category=str(metadata.get("category", "")),
        target_model=str(metadata.get("target_model", "")),
        version=str(metadata.get("version", "")),
        tags=metadata.get("tags", []) if isinstance(metadata.get("tags"), list) else [],
        author=str(metadata.get("author", "")),
        content=body,
    )


def discover_prompt_paths(prompts_dir: Path = DEFAULT_PROMPTS_DIR) -> list[Path]:
    if not prompts_dir.exists():
        return []
    return sorted(path for path in prompts_dir.rglob("*.md") if path.is_file())


def load_all_prompts(prompts_dir: Path = DEFAULT_PROMPTS_DIR) -> list[PromptRecord]:
    return [load_prompt(path, prompts_dir) for path in discover_prompt_paths(prompts_dir)]


def validate_prompt(path: Path, prompts_dir: Path = DEFAULT_PROMPTS_DIR) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text)
    except (OSError, UnicodeError, ValueError) as exc:
        return [str(exc)]

    missing = sorted(REQUIRED_FIELDS - metadata.keys())
    if missing:
        errors.append("缺少字段：" + ", ".join(missing))

    category = metadata.get("category")
    if category not in ALLOWED_CATEGORIES:
        errors.append(f"category 必须是：{', '.join(sorted(ALLOWED_CATEGORIES))}")
    try:
        expected_category = path.resolve().relative_to(prompts_dir.resolve()).parts[0]
        if category and category != expected_category:
            errors.append(f"category={category!r} 与目录 {expected_category!r} 不一致")
    except (ValueError, IndexError):
        errors.append("文件不在 prompts 目录中")

    if not isinstance(metadata.get("title"), str) or not metadata.get("title", "").strip():
        errors.append("title 必须是非空字符串")
    if not isinstance(metadata.get("target_model"), str) or not metadata.get("target_model", "").strip():
        errors.append("target_model 必须是非空字符串")
    if not isinstance(metadata.get("author"), str) or not metadata.get("author", "").strip():
        errors.append("author 必须是非空字符串")
    version = metadata.get("version", "")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        errors.append("version 必须使用 x.y.z 格式")
    tags = metadata.get("tags")
    if not isinstance(tags, list) or not tags or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        errors.append("tags 必须是至少包含一个非空字符串的列表")
    if "### 提示词内容" not in body:
        errors.append("正文缺少“### 提示词内容”标题")
    if "```text" not in body:
        errors.append("提示词正文必须放在 ```text 代码块中")
    return errors


def validate_repository(prompts_dir: Path = DEFAULT_PROMPTS_DIR) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}
    for path in discover_prompt_paths(prompts_dir):
        errors = validate_prompt(path, prompts_dir)
        if errors:
            results[path.relative_to(prompts_dir).as_posix()] = errors
    return results


def filter_prompts(
    prompts: Iterable[PromptRecord], keyword: str = "", category: str | None = None
) -> list[PromptRecord]:
    needle = keyword.casefold().strip()
    matches = []
    for prompt in prompts:
        if category and prompt.category != category:
            continue
        haystack = "\n".join(
            [prompt.title, prompt.category, prompt.target_model, " ".join(prompt.tags), prompt.content]
        ).casefold()
        if not needle or needle in haystack:
            matches.append(prompt)
    return matches


def command_list(args: argparse.Namespace) -> int:
    prompts = filter_prompts(load_all_prompts(args.prompts_dir), category=args.category)
    if not prompts:
        print("没有找到提示词。")
        return 0
    for prompt in prompts:
        print(f"[{prompt.category}] {prompt.title}  v{prompt.version}")
        print(f"  {prompt.path} · {', '.join(prompt.tags)}")
    print(f"\n共 {len(prompts)} 个提示词")
    return 0


def command_search(args: argparse.Namespace) -> int:
    prompts = filter_prompts(load_all_prompts(args.prompts_dir), args.keyword, args.category)
    if args.json:
        print(json.dumps([asdict(prompt) for prompt in prompts], ensure_ascii=False, indent=2))
    elif not prompts:
        print(f"未找到包含“{args.keyword}”的提示词。")
    else:
        for prompt in prompts:
            print(f"[{prompt.category}] {prompt.title}")
            print(f"  {prompt.path} · 目标模型：{prompt.target_model}")
        print(f"\n找到 {len(prompts)} 个结果")
    return 0


def command_show(args: argparse.Namespace) -> int:
    path = (PROJECT_ROOT / args.path).resolve()
    try:
        path.relative_to(args.prompts_dir.resolve())
    except ValueError:
        print("错误：只能查看 prompts 目录中的文件。", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"错误：文件不存在：{args.path}", file=sys.stderr)
        return 2
    print(path.read_text(encoding="utf-8"))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    paths = discover_prompt_paths(args.prompts_dir)
    if not paths:
        print("错误：prompts 目录中没有 Markdown 提示词。", file=sys.stderr)
        return 1
    failures = validate_repository(args.prompts_dir)
    if not failures:
        print(f"✅ 校验通过：{len(paths)} 个提示词格式正确。")
        return 0
    print(f"❌ {len(failures)} 个文件校验失败：", file=sys.stderr)
    for relative_path, errors in failures.items():
        print(f"\n{relative_path}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
    return 1


def command_export(args: argparse.Namespace) -> int:
    prompts = load_all_prompts(args.prompts_dir)
    output = Path(args.output)
    if not output.is_absolute():
        output = PROJECT_ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    records = [asdict(prompt) for prompt in prompts]
    if args.format == "jsonl":
        payload = "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n"
    else:
        payload = json.dumps(records, ensure_ascii=False, indent=2) + "\n"
    output.write_text(payload, encoding="utf-8")
    print(f"✅ 已导出 {len(records)} 个提示词到 {output}")
    return 0


def command_docs(args: argparse.Namespace) -> int:
    prompts = load_all_prompts(args.prompts_dir)
    output = Path(args.output)
    if not output.is_absolute():
        output = PROJECT_ROOT / output
    library_dir = PROJECT_ROOT / "docs" / "library"
    lines = ["# 提示词目录", "", "此页面由 `python3 src/manager.py docs` 自动生成。", ""]
    for category in sorted(ALLOWED_CATEGORIES):
        category_prompts = [prompt for prompt in prompts if prompt.category == category]
        lines.extend([f"## {category}", ""])
        for prompt in category_prompts:
            source_path = args.prompts_dir / prompt.path
            page_path = library_dir / Path(prompt.path)
            page_path.parent.mkdir(parents=True, exist_ok=True)
            page_path.write_text(
                "\n".join(
                    [
                        "---",
                        f'title: "{prompt.title}"',
                        "---",
                        "",
                        f"# {prompt.title}",
                        "",
                        f"> 分类：`{prompt.category}` · 目标模型：{prompt.target_model} · 版本：{prompt.version}",
                        "",
                        source_path.read_text(encoding="utf-8").split("---", 2)[-1].strip(),
                        "",
                        "[在 GitHub 查看源文件]("
                        f"https://github.com/jasperJu111/Prompt-Manager-CN/blob/main/prompts/{prompt.path})",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            local_url = f"/library/{Path(prompt.path).with_suffix('').as_posix()}"
            lines.extend(
                [
                    f"### [{prompt.title}]({local_url})",
                    "",
                    f"- 目标模型：{prompt.target_model}",
                    f"- 版本：{prompt.version}",
                    f"- 标签：{', '.join(prompt.tags)}",
                    f"- 作者：{prompt.author}",
                    "",
                ]
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 已生成文档索引和 {len(prompts)} 个详情页：{output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="提示管理器-CN 命令行工具")
    parser.set_defaults(prompts_dir=DEFAULT_PROMPTS_DIR)
    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="列出提示词")
    list_parser.add_argument("--category", choices=sorted(ALLOWED_CATEGORIES))
    list_parser.set_defaults(func=command_list)
    search_parser = subparsers.add_parser("search", help="按关键词搜索")
    search_parser.add_argument("keyword")
    search_parser.add_argument("--category", choices=sorted(ALLOWED_CATEGORIES))
    search_parser.add_argument("--json", action="store_true", help="输出 JSON")
    search_parser.set_defaults(func=command_search)
    show_parser = subparsers.add_parser("show", help="显示完整提示词文件")
    show_parser.add_argument("path", help="相对于项目根目录的路径")
    show_parser.set_defaults(func=command_show)
    validate_parser = subparsers.add_parser("validate", help="校验全部提示词")
    validate_parser.set_defaults(func=command_validate)
    export_parser = subparsers.add_parser("export", help="导出提示词目录")
    export_parser.add_argument("output")
    export_parser.add_argument("--format", choices=("json", "jsonl"), default="json")
    export_parser.set_defaults(func=command_export)
    docs_parser = subparsers.add_parser("docs", help="生成 VitePress 提示词目录")
    docs_parser.add_argument("output", nargs="?", default="docs/prompts/index.md")
    docs_parser.set_defaults(func=command_docs)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
