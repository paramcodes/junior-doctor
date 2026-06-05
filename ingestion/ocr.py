"""
OCR module for fallback text extraction.
"""
import logging
from typing import List
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

from schemas.page import Page

logger = logging.getLogger(__name__)


def apply_ocr_to_page(pdf_path: str, page_obj: Page) -> Page:
    """
    Apply OCR to a specific page of a PDF if it lacks extractable text.

    Args:
        pdf_path (str): Path to the PDF file.
        page_obj (Page): The Page object to process.

    Returns:
        Page: The updated Page object containing OCR text if applied.
    """
    if page_obj.has_text:
        logger.debug(f"Page {page_obj.page_number} already has native text, skipping OCR.")
        return page_obj

    logger.info(f"Applying OCR to page {page_obj.page_number} of {pdf_path}")
    try:
        doc = fitz.open(pdf_path)
        # Convert 1-indexed page_number to 0-indexed for PyMuPDF
        pdf_page = doc[page_obj.page_number - 1]
        
        # Render the page to a pixmap
        pix = pdf_page.get_pixmap(dpi=300)
        
        # Convert the pixmap to a PIL Image
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        
        # Apply OCR
        text = pytesseract.image_to_string(img).strip()
        
        # Update the page object
        page_obj.text = text
        page_obj.ocr_applied = True
        
        doc.close()
    except Exception as e:
        logger.error(f"Failed to apply OCR to page {page_obj.page_number}. Error: {e}")
        # Log the error but continue execution gracefully
    
    return page_obj


def apply_ocr_fallback(pdf_path: str, pages: List[Page]) -> List[Page]:
    """
    Iterate over a list of pages and apply OCR to any that lack text.

    Args:
        pdf_path (str): Path to the PDF file.
        pages (List[Page]): The initial list of extracted pages.

    Returns:
        List[Page]: The updated list of pages, potentially with OCR text.
    """
    updated_pages = []
    for page in pages:
        updated_page = apply_ocr_to_page(pdf_path, page)
        updated_pages.append(updated_page)
    return updated_pages
