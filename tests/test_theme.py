from pathlib import Path

from markdf.theme import init_theme_skeleton, load_theme


def test_load_builtin_theme():
    t = load_theme(theme_name="default")
    assert t.palette["bg"]
    assert "h1" in t.style_css


def test_load_custom_theme(tmp_path: Path):
    (tmp_path / "theme.json").write_text(
        """
{
  \"name\": \"x\",
  \"palette\": {\"bg\": \"#fff\"},
  \"fonts\": {\"sans\": \"Arial\"},
  \"code_style\": \"monokai\"
}
""".lstrip(),
        encoding="utf-8",
    )
    (tmp_path / "style.css").write_text("h1{color:red}", encoding="utf-8")
    t = load_theme(theme_name="ignored", theme_dir=tmp_path)
    assert t.name == "x"
    assert t.palette["bg"] == "#fff"


def test_init_theme_skeleton_writes_preview(tmp_path: Path):
    init_theme_skeleton(tmp_path, name="demo")
    assert (tmp_path / "theme.json").is_file()
    assert (tmp_path / "style.css").is_file()
    preview = tmp_path / "preview.html"
    assert preview.is_file()

    html = preview.read_text(encoding="utf-8")
    assert "markdf theme preview: demo" in html
    assert "href=\"./style.css\"" in html
    assert "--md-bg:" in html
    assert "class='codehilite'" in html
