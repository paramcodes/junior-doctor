"""
Tests for Page schema.
"""
from schemas.page import Page


def test_page_schema_creation():
    """
    Test creating a valid Page object.
    """
    page = Page(
        page_number=1,
        text="Sample text",
        has_text=True,
        ocr_applied=False
    )
    
    assert page.page_number == 1
    assert page.text == "Sample text"
    assert page.has_text is True
    assert page.ocr_applied is False


def test_page_schema_with_ocr():
    """
    Test creating a Page object that had OCR applied.
    """
    page = Page(
        page_number=2,
        text="OCR Extracted Text",
        has_text=False,
        ocr_applied=True
    )
    
    assert page.page_number == 2
    assert page.text == "OCR Extracted Text"
    assert page.has_text is False
    assert page.ocr_applied is True
