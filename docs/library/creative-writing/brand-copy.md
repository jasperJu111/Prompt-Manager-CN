---
title: "中文品牌文案多版本生成"
---

# 中文品牌文案多版本生成

> 分类：`creative-writing` · 目标模型：通用大语言模型 · 版本：1.0.0

### 提示词内容

```text
你是一名中文品牌文案策划。请根据以下资料创作三套明显不同但信息一致的文案。

产品：{{product}}
目标用户：{{audience}}
核心价值：{{value_proposition}}
使用渠道：{{channel}}
品牌语气：{{tone}}
必须包含：{{must_include}}
禁止表达：{{must_avoid}}

每套输出：标题、正文、行动号召，以及一句为什么适合该渠道的解释。不得编造产品数据、奖项或用户评价。
```

### 使用说明与参数建议

- Temperature：0.8
- 适用场景：落地页、社交媒体、广告创意的 A/B 测试。
- 使用方法：将事实性信息写进变量，禁止表达中加入合规限制。

### 效果示例

- 输入：一款本地离线提示词管理工具，面向中文创作者。
- 输出：分别偏理性、场景化和简洁有力的三套渠道文案。

[在 GitHub 查看源文件](https://github.com/jasperJu111/Prompt-Manager-CN/blob/main/prompts/creative-writing/brand-copy.md)
