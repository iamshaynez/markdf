from markdf.transform import markdown_to_html


def test_markdown_to_html_basic():
    html = markdown_to_html("# 标题\n\n- a\n- b\n\n```python\nprint('x')\n```\n")
    assert "<h1" in html
    assert "<ul" in html
    assert "codehilite" in html
