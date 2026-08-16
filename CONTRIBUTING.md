# 参与贡献

感谢你帮助完善提示管理器-CN。项目欢迎新增提示词、修正文档、报告问题和改进管理工具。

## 提交提示词

1. Fork 本仓库并创建分支，例如 `feat/add-interview-prompt`。
2. 复制 `templates/prompt_template.md` 到正确的 `prompts/<category>/` 目录。
3. 使用小写英文和连字符命名文件，例如 `python-code-review.md`。
4. 填写全部元数据，确保 `category` 与目录名称完全一致。
5. 提示词应当原创、可复用、目标清晰，并包含参数建议和效果示例。
6. 不得提交密码、API Key、个人隐私、受版权保护的长篇内容或用于明显伤害他人的指令。
7. 本地运行校验和测试后再发起 Pull Request。

```bash
python3 src/manager.py validate
python3 -m unittest discover -s tests -v
```

## 支持的分类

| 分类 | 目录 | 示例用途 |
| --- | --- | --- |
| 编程开发 | `programming` | 重构、测试、代码审查 |
| 创意写作 | `creative-writing` | 文案、故事、脚本 |
| 视觉艺术 | `visual-art` | 图像生成、视觉策划 |
| 音频音乐 | `audio-music` | 音乐创作、播客制作 |
| 生产力 | `productivity` | 会议、计划、知识整理 |

## 版本规则

- 修正文案、参数或示例：递增修订号，例如 `1.0.0` → `1.0.1`。
- 增加兼容能力且保持原用法：递增次版本号，例如 `1.0.0` → `1.1.0`。
- 不兼容的结构变化：递增主版本号，例如 `1.0.0` → `2.0.0`。

## Commit 建议

```text
feat: 新增 Python 代码审查提示词
fix: 修正视觉艺术模板的参数说明
docs: 完善贡献指南
test: 增加元数据校验测试
```

提交 Pull Request 即表示你同意以本项目的 MIT License 发布你的贡献。
