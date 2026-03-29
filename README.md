# markdf

把 Markdown 文档转换成排版精致的竖版 A4 PDF。

## 安装

```bash
pip install -e .
python3 -m playwright install chromium
```

## 命令行

```bash
python3 -m markdf render README.md -o out.pdf --theme default --title "示例文档"
python3 -m markdf render report2.md -o report.pdf --theme default --footer "人工智能商业模式战略分析引擎 Beta"
python3 -m markdf list-themes
python3 -m markdf init-theme ./my-theme
python3 -m markdf render input.md -o out.pdf --theme-dir ./my-theme
```

## Python API

```python
from pathlib import Path
from markdf import render_pdf

render_pdf(
    input_path=Path("input.md"),
    output_path=Path("out.pdf"),
    theme_name="default",
    title="标题",
)
```

## 主题扩展约定

一个主题目录至少包含：

- `theme.json`
- `style.css`

`theme.json` 示例：

```json
{
  "name": "my-theme",
  "palette": {
    "bg": "#ffffff",
    "text": "#111827",
    "muted": "#6b7280",
    "primary": "#2563eb",
    "border": "#e5e7eb",
    "code_bg": "#0b1020"
  },
  "fonts": {
    "sans": "PingFang SC, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
    "serif": "Songti SC, Noto Serif CJK SC, serif",
    "mono": "SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace"
  },
  "code_style": "monokai"
}
```

`style.css` 里可以使用 CSS 变量（由 `palette/fonts` 注入）：

- `--md-bg --md-text --md-muted --md-primary --md-border --md-code-bg`
- `--md-font-sans --md-font-serif --md-font-mono`

