"""
Evidence schema for extracted clinical facts.
"""
from typing import Any
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """
    Represents an extracted clinical fact with strict provenance.
    """
    fact: Any = Field(..., description="The extracted clinical fact. Use 'Not Documented' if missing.")
    page_number: int = Field(..., description="The 1-indexed page number where the fact was found.")
    source_document: str = Field(..., description="The name or identifier of the source document.")
    source_text: str = Field(..., description="The exact text snippet from which the fact was extracted.")
