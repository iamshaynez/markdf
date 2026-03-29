from markdf.renderer import _build_footer_template, _build_header_template


def test_header_template_escapes():
    html = _build_header_template(title="A&B<>")
    assert "A&amp;B" in html
    assert "&lt;&gt;" in html


def test_footer_template_left_text_and_pages():
    html = _build_footer_template(left_text="机密")
    assert "机密" in html
    assert "pageNumber" in html
    assert "totalPages" in html

