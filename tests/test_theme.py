from pathlib import Path

from markdf.theme import load_theme


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
