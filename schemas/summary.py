"""
Discharge summary schemas.
"""
from pydantic import BaseModel, Field


class DischargeSummary(BaseModel):
    """
    Represents the structure of the final discharge summary.
    """
    markdown_content: str = Field(..., description="The fully generated markdown text of the summary.")
