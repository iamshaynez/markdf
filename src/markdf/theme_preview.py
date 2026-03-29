from __future__ import annotations

from importlib import resources

from pygments.formatters import HtmlFormatter

from .theme import Theme


_SAMPLE_MARKDOWN = """
# 主题预览（{theme_name}）

段落含有 [链接](https://example.com) 与 `行内代码`，以及 **加粗** 与 *斜体*。

---

## 引用

> 这是引用块，用于展示边框、背景、圆角与分页避免规则。
>
> 第二行，包含 `code` 与 [link](https://example.com)。

## 列表

- 无序列表 A
- 无序列表 B
  - 二级项 B.1
  - 二级项 B.2

1. 有序列表 1
2. 有序列表 2

### 任务列表

- [x] 已完成
- [ ] 未完成

## 表格

| 列A | 列B | 列C |
| --- | --- | --- |
| 1   | 文本 | `code` |
| 2   | **粗体** | *斜体* |

## 代码块（codehilite）

```python
def hello(name: str) -> str:
    return f\"Hi, {{name}}\"
```

#### 小标题（h4）

这里有脚注[^1]。

[^1]: 脚注内容。
""".lstrip()


def _css_vars(theme: Theme) -> str:
    p = theme.palette
    f = theme.fonts
    return (
        ":root{"
        f"--md-bg:{p['bg']};"
        f"--md-text:{p['text']};"
        f"--md-muted:{p['muted']};"
        f"--md-primary:{p['primary']};"
        f"--md-border:{p['border']};"
        f"--md-code-bg:{p['code_bg']};"
        f"--md-font-sans:{f['sans']};"
        f"--md-font-serif:{f['serif']};"
        f"--md-font-mono:{f['mono']};"
        "}"
    )


def build_theme_preview_html(theme: Theme) -> str:
    from .transform import markdown_to_html

    base_css = resources.files("markdf").joinpath("static").joinpath("base.css").read_text(encoding="utf-8")
    pygments_css = HtmlFormatter(style=theme.code_style).get_style_defs(".codehilite")
    body_html = markdown_to_html(_SAMPLE_MARKDOWN.format(theme_name=theme.name))

    css = "\n".join([
        _css_vars(theme),
        base_css,
        pygments_css,
    ])

    return (
        "<!doctype html>\n"
        "<html lang=\"zh-CN\">\n"
        "  <head>\n"
        "    <meta charset=\"utf-8\" />\n"
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
        f"    <title>markdf theme preview: {theme.name}</title>\n"
        "    <style>\n"
        f"{css}\n"
        "    </style>\n"
        "    <link rel=\"stylesheet\" href=\"./style.css\" />\n"
        "  </head>\n"
        "  <body>\n"
        "    <div class=\"md-page\">\n"
        "      <article class=\"md-body\">\n"
        f"{body_html}\n"
        "      </article>\n"
        "    </div>\n"
        "  </body>\n"
        "</html>\n"
    )
