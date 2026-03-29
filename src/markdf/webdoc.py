from __future__ import annotations

from importlib import resources

from jinja2 import Template
from pygments.formatters import HtmlFormatter

from .theme import Theme


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


def build_full_html(*, body_html: str, theme: Theme, base_url: str) -> str:
    base_css = resources.files("markdf").joinpath("static").joinpath("base.css").read_text(encoding="utf-8")
    doc_tpl = resources.files("markdf").joinpath("static").joinpath("document.html.j2").read_text(encoding="utf-8")
    pygments_css = HtmlFormatter(style=theme.code_style).get_style_defs(".codehilite")

    css = "\n".join([
        _css_vars(theme),
        base_css,
        theme.style_css,
        pygments_css,
    ])

    html = Template(doc_tpl).render(css=css, body_html=body_html, base_url=base_url)
    return html

