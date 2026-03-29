from __future__ import annotations

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound


def _highlight(code: str, lang: str | None) -> str:
    try:
        if lang:
            lexer = get_lexer_by_name(lang, stripall=False)
        else:
            lexer = guess_lexer(code)
    except ClassNotFound:
        return "<pre><code>" + _escape_html(code) + "</code></pre>"

    formatter = HtmlFormatter(nowrap=True)
    html = highlight(code, lexer, formatter)
    return "<pre class='codehilite'><code>" + html + "</code></pre>"


def _escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


class _Renderer(RendererHTML):
    def fence(self, tokens, idx, options, env):
        token = tokens[idx]
        info = (token.info or "").strip()
        lang = info.split()[0] if info else None
        return _highlight(token.content, lang)


def markdown_to_html(markdown_text: str) -> str:
    md = (
        MarkdownIt("gfm-like", renderer_cls=_Renderer)
        .use(tasklists_plugin, enabled=True)
        .use(footnote_plugin)
    )
    return md.render(markdown_text)
