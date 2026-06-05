"""
Page schema for document representation.
"""
from pydantic import BaseModel, Field


class Page(BaseModel):
    """
    Represents a single page extracted from a PDF document.
    """
    page_number: int = Field(..., description="The 1-indexed page number within the document.")
    text: str = Field(..., description="The text content extracted from the page.")
    has_text: bool = Field(..., description="True if the page originally contained extractable text before any OCR.")
    ocr_applied: bool = Field(False, description="True if OCR was applied to extract text from this page.")
