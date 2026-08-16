---
title: "Python 遗留代码安全重构"
category: "programming"
target_model: "通用代码模型"
version: "1.0.0"
tags: ["Python", "代码重构", "单元测试", "可维护性"]
author: "jasperJu111"
---

### 提示词内容

```text
你是一名资深 Python 工程师。请重构下面的代码，同时保持现有外部行为不变。

代码：
{{source_code}}

运行环境与限制：
{{constraints}}

请按顺序输出：
1. 当前代码的职责和主要风险；
2. 分步骤重构方案；
3. 完整的重构后代码，加入类型注解和必要的 Docstring；
4. 覆盖正常、边界与异常路径的 unittest 或 pytest 测试；
5. 可能存在但无法从上下文确认的假设。

不要虚构不存在的依赖或接口。信息不足时先列出需要确认的问题。
```

### 使用说明与参数建议

- Temperature：0.2
- 适用场景：遗留脚本重构、补充类型标注、生成回归测试。
- 使用方法：将源码替换 `{{source_code}}`，把版本和依赖限制填入 `{{constraints}}`。

### 效果示例

- 输入：`def add(a,b): return a+b`
- 输出：包含类型注解、说明文档和边界测试的等价实现。
