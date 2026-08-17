<div align="center">

# 提示词管理器-CN

面向中文开发者与创作者的开源 AI 提示词库、检索工具与协作规范。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Validate prompts](https://github.com/jasperJu111/Prompt-Manager-CN/actions/workflows/validate.yml/badge.svg)](https://github.com/jasperJu111/Prompt-Manager-CN/actions/workflows/validate.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

## 项目简介

提示词管理器-CN 用统一的 Markdown + YAML Frontmatter 格式保存提示词，兼顾人类阅读、Git 版本管理和程序化检索。项目不收集账号信息，也不调用任何模型 API；所有工具都可以在本地离线运行。

## 主要功能

- 五类中文提示词：编程、创意写作、视觉艺术、音频音乐和生产力。
- 零第三方 Python 依赖的 CLI：列表、搜索、查看、变量填写、统计、校验和 JSON 导出。
- 标准化元数据：标题、分类、目标模型、语义化版本、标签和作者。
- GitHub Actions 自动检查提示词格式并运行单元测试。
- VitePress 文档站，可自动生成提示词目录并部署到 GitHub Pages。
- Issue 模板和贡献指南，方便社区提交提示词与改进建议。

## 目录结构

```text
Prompt-Manager-CN/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── docs/                    # VitePress 文档站
├── prompts/
│   ├── programming/
│   ├── creative-writing/
│   ├── visual-art/
│   ├── audio-music/
│   └── productivity/
├── src/
│   └── manager.py           # 检索、校验、导出和文档生成
├── templates/
│   └── prompt_template.md
├── tests/
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## 快速开始

```bash
git clone https://github.com/jasperJu111/Prompt-Manager-CN.git
cd Prompt-Manager-CN
python3 src/manager.py list
```

按关键词搜索：

```bash
python3 src/manager.py search "代码重构"
python3 src/manager.py search "文案" --category creative-writing
```

校验全部提示词：

```bash
python3 src/manager.py validate
```

导出为 JSON：

```bash
python3 src/manager.py export prompt-catalog.json
```

查看某个提示词的完整内容：

```bash
python3 src/manager.py show prompts/programming/python-refactor.md
```

交互填写提示词中的 `{{变量}}`，未通过 `--set` 提供的变量会在终端中依次询问：

```bash
python3 src/manager.py fill prompts/programming/python-refactor.md
python3 src/manager.py fill prompts/programming/python-refactor.md \
  --set source_code="def add(a, b): return a + b" \
  --set constraints="Python 3.9，无第三方依赖" \
  --output filled-python-refactor.txt
```

查看提示词库的分类、模型、变量和热门标签统计：

```bash
python3 src/manager.py stats
python3 src/manager.py stats --json
```

## 文档网站

需要 Node.js 22 或更高版本。

```bash
npm install
npm run docs:dev
```

构建静态文档：

```bash
npm run docs:build
```

## 提示词格式

每个提示词都是独立的 `.md` 文件。复制 [标准模板](templates/prompt_template.md)，修改元数据和正文即可。`category` 必须与所在目录一致，`version` 使用 `主版本.次版本.修订号` 格式。

## 参与贡献

欢迎提交高质量中文提示词、修复文档或改进工具。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并运行：

```bash
python3 src/manager.py validate
python3 -m unittest discover -s tests -v
```

## 路线图

- [x] 标准提示词模板与五类目录
- [x] 本地 CLI 检索、校验与 JSON 导出
- [x] 自动化测试和文档构建
- [ ] 为提示词增加质量评分与兼容性记录
- [x] 支持变量占位符交互填写
- [ ] 开发轻量 Web 检索界面
- [ ] 建立社区审核与版本发布节奏

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
