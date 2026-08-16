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

## 启动文档站

安装 Node.js 22 或更高版本后执行：

```bash
npm install
npm run docs:dev
```
