from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from .theme import Theme, ThemeNotFoundError, load_theme
from .transform import markdown_to_html
from .webdoc import build_full_html


@dataclass(frozen=True)
class RenderOptions:
    theme_name: str = "default"
    theme_dir: Optional[Path] = None
    title: Optional[str] = None
    footer_text: Optional[str] = None
    header: bool = True
    footer: bool = True


def _escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _build_header_template(*, title: str) -> str:
    safe_title = _escape_html(title)
    return (
        "<div style='font-size:9px; width:100%; padding:0 12mm; color:#6b7280; "
        "font-family:var(--md-font-sans)'>"
        f"<span>{safe_title}</span>"
        "</div>"
    )


def _build_footer_template(*, left_text: Optional[str]) -> str:
    left_html = ""
    if left_text:
        safe_left = _escape_html(left_text)
        left_html = f"<span>{safe_left}</span>"

    return (
        "<div style='font-size:9px; width:100%; padding:0 12mm; color:#6b7280; "
        "font-family:var(--md-font-sans); display:flex; justify-content:space-between'>"
        f"{left_html}"
        "<span><span class='pageNumber'></span>/<span class='totalPages'></span></span>"
        "</div>"
    )


def list_builtin_themes() -> list[str]:
    return Theme.list_builtin()


def render_pdf(*, input_path: Path, output_path: Path, options: RenderOptions | None = None) -> None:
    if options is None:
        options = RenderOptions()

    footer_enabled = options.footer or bool(options.footer_text)

    markdown_text = input_path.read_text(encoding="utf-8")
    theme = load_theme(theme_name=options.theme_name, theme_dir=options.theme_dir)
    body_html = markdown_to_html(markdown_text)
    base_url = input_path.parent.as_uri() + "/"
    full_html = build_full_html(body_html=body_html, theme=theme, base_url=base_url)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="markdf_") as td:
        td_path = Path(td)
        html_path = td_path / "document.html"
        html_path.write_text(full_html, encoding="utf-8")

        file_url = html_path.as_uri()

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(file_url, wait_until="load")

                header_template = ""
                footer_template = ""
                if options.header:
                    header_title = options.title or input_path.stem
                    header_template = _build_header_template(title=header_title)
                if footer_enabled:
                    footer_template = _build_footer_template(left_text=options.footer_text)

                page.pdf(
                    path=str(output_path),
                    format="A4",
                    print_background=True,
                    display_header_footer=options.header or footer_enabled,
                    header_template=header_template,
                    footer_template=footer_template,
                    margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"},
                    prefer_css_page_size=True,
                )

                browser.close()
        except PlaywrightError as e:
            raise RuntimeError("Playwright 渲染失败。请先执行: python -m playwright install chromium") from e
