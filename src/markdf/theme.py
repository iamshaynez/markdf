from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from importlib import resources


class ThemeNotFoundError(RuntimeError):
    pass


@dataclass(frozen=True)
class Theme:
    name: str
    palette: dict[str, str]
    fonts: dict[str, str]
    code_style: str
    style_css: str

    @staticmethod
    def list_builtin() -> list[str]:
        base = resources.files("markdf").joinpath("themes")
        names: list[str] = []
        for entry in base.iterdir():
            if entry.is_dir() and entry.joinpath("theme.json").is_file() and entry.joinpath("style.css").is_file():
                names.append(entry.name)
        return sorted(names)


def _load_theme_from_dir(theme_dir: Path) -> Theme:
    theme_json_path = theme_dir / "theme.json"
    style_css_path = theme_dir / "style.css"
    if not theme_json_path.is_file() or not style_css_path.is_file():
        raise ThemeNotFoundError(f"主题目录缺少 theme.json/style.css: {theme_dir}")
    raw = json.loads(theme_json_path.read_text(encoding="utf-8"))
    return _build_theme(raw, style_css_path.read_text(encoding="utf-8"))


def _build_theme(raw: dict[str, Any], style_css: str) -> Theme:
    name = str(raw.get("name") or "theme")
    palette = dict(raw.get("palette") or {})
    fonts = dict(raw.get("fonts") or {})
    code_style = str(raw.get("code_style") or "default")

    palette_defaults = {
        "bg": "#ffffff",
        "text": "#0f172a",
        "muted": "#64748b",
        "primary": "#2563eb",
        "border": "#e2e8f0",
        "code_bg": "#0b1020",
    }
    fonts_defaults = {
        "sans": "PingFang SC, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
        "serif": "Songti SC, Noto Serif CJK SC, serif",
        "mono": "SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace",
    }

    merged_palette = {**palette_defaults, **{k: str(v) for k, v in palette.items()}}
    merged_fonts = {**fonts_defaults, **{k: str(v) for k, v in fonts.items()}}

    return Theme(
        name=name,
        palette=merged_palette,
        fonts=merged_fonts,
        code_style=code_style,
        style_css=style_css,
    )


def load_theme(*, theme_name: str, theme_dir: Optional[Path] = None) -> Theme:
    if theme_dir is not None:
        return _load_theme_from_dir(theme_dir)

    base = resources.files("markdf").joinpath("themes").joinpath(theme_name)
    if not base.is_dir():
        raise ThemeNotFoundError(f"找不到主题: {theme_name}")
    theme_json = json.loads(base.joinpath("theme.json").read_text(encoding="utf-8"))
    style_css = base.joinpath("style.css").read_text(encoding="utf-8")
    return _build_theme(theme_json, style_css)


def init_theme_skeleton(target_dir: Path, *, name: str = "my-theme") -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    raw_theme = {
        "name": name,
        "palette": {
            "bg": "#ffffff",
            "text": "#111827",
            "muted": "#6b7280",
            "primary": "#2563eb",
            "border": "#e5e7eb",
            "code_bg": "#0b1020",
        },
        "fonts": {
            "sans": "PingFang SC, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
            "serif": "Songti SC, Noto Serif CJK SC, serif",
            "mono": "SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace",
        },
        "code_style": "monokai",
    }
    (target_dir / "theme.json").write_text(
        json.dumps(
            raw_theme,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    style_css = """
:root {
  --md-radius: 10px;
}
""".lstrip()
    (target_dir / "style.css").write_text(style_css, encoding="utf-8")

    from .theme_preview import build_theme_preview_html

    preview_html = build_theme_preview_html(_build_theme(raw_theme, style_css))
    (target_dir / "preview.html").write_text(preview_html, encoding="utf-8")
