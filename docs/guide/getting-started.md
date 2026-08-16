# 快速开始

## 克隆项目

```bash
git clone https://github.com/jasperJu111/Prompt-Manager-CN.git
cd Prompt-Manager-CN
```

## 查看与搜索

```bash
python3 src/manager.py list
python3 src/manager.py search "代码"
python3 src/manager.py search "文案" --category creative-writing
```

## 校验与导出

```bash
python3 src/manager.py validate
python3 src/manager.py export prompt-catalog.json
```

CLI 只使用 Python 标准库，不需要额外安装依赖。

## 填写变量

`fill` 会识别提示词中的 `{{变量名}}`，在终端中询问尚未提供的变量，并输出可直接使用的完整提示词：

```bash
python3 src/manager.py fill prompts/programming/python-refactor.md
```

也可以通过 `--set` 预填变量，并用 `--output` 或 `-o` 保存结果：

```bash
python3 src/manager.py fill prompts/programming/python-refactor.md \
  --set source_code="def add(a, b): return a + b" \
  --set constraints="Python 3.9，无第三方依赖" \
  -o filled-python-refactor.txt
```

## 查看统计

```bash
python3 src/manager.py stats
python3 src/manager.py stats --json
```

统计信息包括提示词总数、分类、目标模型、变量使用情况和热门标签。

## 启动文档站

安装 Node.js 22 或更高版本后执行：

```bash
npm install
npm run docs:dev
```
