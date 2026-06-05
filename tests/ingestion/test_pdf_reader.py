"""
Tests for PDF reader module.
"""
import pytest
from unittest.mock import patch, MagicMock

from ingestion.pdf_reader import extract_pages


@patch("ingestion.pdf_reader.fitz.open")
def test_extract_pages_success(mock_fitz_open):
    """
    Test successful extraction of text from a PDF.
    """
    # Mock the fitz document and pages
    mock_doc = MagicMock()
    mock_page_1 = MagicMock()
    mock_page_1.get_text.return_value = "Page 1 Text"
    
    mock_page_2 = MagicMock()
    mock_page_2.get_text.return_value = ""  # Empty page
    
    # Configure mock doc to behave like a list of pages
    mock_doc.__len__.return_value = 2
    mock_doc.__getitem__.side_effect = [mock_page_1, mock_page_2]
    mock_fitz_open.return_value = mock_doc
    
    pages = extract_pages("dummy.pdf")
    
    assert len(pages) == 2
    
    assert pages[0].page_number == 1
    assert pages[0].text == "Page 1 Text"
    assert pages[0].has_text is True
    assert pages[0].ocr_applied is False
    
    assert pages[1].page_number == 2
    assert pages[1].text == ""
    assert pages[1].has_text is False
    assert pages[1].ocr_applied is False
    
    mock_fitz_open.assert_called_once_with("dummy.pdf")
    mock_doc.close.assert_called_once()


@patch("ingestion.pdf_reader.fitz.open")
def test_extract_pages_failure(mock_fitz_open):
    """
    Test failure handling when opening a PDF.
    """
    mock_fitz_open.side_effect = Exception("Cannot open file")
    
    with pytest.raises(Exception, match="Cannot open file"):
        extract_pages("invalid.pdf")
