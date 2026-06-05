"""
PDF ingestion module.
"""
import logging
from typing import List
import fitz  # PyMuPDF

from schemas.page import Page

logger = logging.getLogger(__name__)


def extract_pages(pdf_path: str) -> List[Page]:
    """
    Extract text and metadata from each page of a PDF file.

    Args:
        pdf_path (str): The file path to the PDF.

    Returns:
        List[Page]: A list of Page schema objects containing the text and metadata.
    
    Raises:
        Exception: If the PDF cannot be opened.
    """
    logger.info(f"Opening PDF document: {pdf_path}")
    pages = []
    
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logger.error(f"Failed to open PDF document: {pdf_path}. Error: {e}")
        raise

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        
        has_text = len(text) > 0
        
        # page_num is 0-indexed in PyMuPDF, but our schema expects 1-indexed
        page_obj = Page(
            page_number=page_num + 1,
            text=text,
            has_text=has_text,
            ocr_applied=False
        )
        pages.append(page_obj)
        
    doc.close()
    logger.info(f"Successfully extracted {len(pages)} pages from {pdf_path}")
    
    return pages
