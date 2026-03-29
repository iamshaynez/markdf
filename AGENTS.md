# 项目代理指南（markdf）

## 项目目标

`markdf` 用于把 Markdown 文档渲染为排版精致的竖版 A4 PDF。

- 渲染链路：Markdown → HTML（内置样式 + 主题 CSS）→ Playwright/Chromium 打印为 PDF
- 重点：主题可扩展、分页尽量避免切断块元素、表格/列表/代码块有一致的视觉风格

## 仓库结构

- `src/markdf/`：主包源码
- `src/markdf/static/`：基础样式与 HTML 模板
- `src/markdf/themes/`：内置主题（每个主题 `theme.json + style.css`）
- `tests/`：单元测试

## 开发环境

- 使用 `python3`
- 需要 Playwright 的 Chromium（首次渲染前安装）

```bash
python3 -m pip install -e .
python3 -m playwright install chromium
```

## 常用命令

- 运行测试：

```bash
python3 -m pytest -q
```

- 查看内置主题：

```bash
python3 -m markdf list-themes
```

- 渲染 PDF：

```bash
python3 -m markdf render input.md -o out.pdf --theme default
python3 -m markdf render input.md -o out.pdf --footer "机密 · 内部使用"
```

- 生成主题骨架：

```bash
python3 -m markdf init-theme ./my-theme
python3 -m markdf render input.md -o out.pdf --theme-dir ./my-theme
```

## 代码修改约束

- 不扩张目标：只实现用户明确要求的功能变更或 bug 修复
- 不引入新依赖：除非确有必要且能说明理由与替代方案
- 改动后必须跑测试：至少 `python3 -m pytest -q`
- 输出与文案使用中文（包括提交信息）

## 主题与样式约定

- 主题由 `theme.json` 定义：`palette/fonts/code_style`
- 主题 CSS 使用注入的 CSS 变量（例如 `--md-bg`、`--md-primary`、`--md-font-sans`）
- 基础排版规则在 `src/markdf/static/base.css`，避免把主题逻辑写进渲染代码

## 渲染注意事项

- PDF 输出固定为 A4 竖版，CSS `@page` 与 Playwright `format="A4"` 保持一致
- 页眉/页脚通过 Playwright 的 `header_template/footer_template` 注入，内容需做 HTML 转义

