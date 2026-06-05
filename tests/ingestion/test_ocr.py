"""
Tests for OCR module.
"""
from unittest.mock import patch, MagicMock
from schemas.page import Page
from ingestion.ocr import apply_ocr_to_page, apply_ocr_fallback


@patch("ingestion.ocr.fitz.open")
@patch("ingestion.ocr.pytesseract.image_to_string")
def test_apply_ocr_to_page_no_text(mock_image_to_string, mock_fitz_open):
    """
    Test applying OCR to a page that lacks text.
    """
    mock_image_to_string.return_value = "Extracted OCR Text"
    
    # Mock PyMuPDF behavior
    mock_doc = MagicMock()
    mock_pdf_page = MagicMock()
    mock_pix = MagicMock()
    
    mock_pix.alpha = False
    mock_pix.width = 100
    mock_pix.height = 100
    mock_pix.samples = b"dummy_samples"
    
    mock_pdf_page.get_pixmap.return_value = mock_pix
    mock_doc.__getitem__.return_value = mock_pdf_page
    mock_fitz_open.return_value = mock_doc
    
    page = Page(
        page_number=1,
        text="",
        has_text=False,
        ocr_applied=False
    )
    
    updated_page = apply_ocr_to_page("dummy.pdf", page)
    
    assert updated_page.text == "Extracted OCR Text"
    assert updated_page.has_text is False
    assert updated_page.ocr_applied is True
    
    mock_fitz_open.assert_called_once_with("dummy.pdf")
    mock_pdf_page.get_pixmap.assert_called_once_with(dpi=300)


def test_apply_ocr_to_page_with_text():
    """
    Test that OCR is skipped if the page already has native text.
    """
    page = Page(
        page_number=1,
        text="Native text",
        has_text=True,
        ocr_applied=False
    )
    
    updated_page = apply_ocr_to_page("dummy.pdf", page)
    
    assert updated_page.text == "Native text"
    assert updated_page.ocr_applied is False


@patch("ingestion.ocr.apply_ocr_to_page")
def test_apply_ocr_fallback(mock_apply_ocr):
    """
    Test the fallback function over multiple pages.
    """
    page1 = Page(page_number=1, text="Text 1", has_text=True, ocr_applied=False)
    page2 = Page(page_number=2, text="", has_text=False, ocr_applied=False)
    
    mock_apply_ocr.side_effect = [
        page1, 
        Page(page_number=2, text="OCR Text", has_text=False, ocr_applied=True)
    ]
    
    pages = [page1, page2]
    updated_pages = apply_ocr_fallback("dummy.pdf", pages)
    
    assert len(updated_pages) == 2
    assert updated_pages[0].ocr_applied is False
    assert updated_pages[1].ocr_applied is True
    assert updated_pages[1].text == "OCR Text"
    
    assert mock_apply_ocr.call_count == 2
