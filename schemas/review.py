"""
Review and Conflict schemas.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

from schemas.evidence import Evidence


class Conflict(BaseModel):
    """
    Represents a conflict between two or more pieces of clinical evidence.
    """
    field: str = Field(..., description="The field where conflict occurred (e.g., 'Medication Dosage').")
    conflicting_evidence: List[Evidence] = Field(..., description="The list of evidence objects that are in conflict.")
    description: str = Field(..., description="A deterministic description of the conflict.")


class ReviewFlag(BaseModel):
    """
    A flag requiring clinician review due to conflict or missing critical information.
    """
    severity: str = Field(..., description="Severity of the flag: 'HIGH', 'MEDIUM', 'LOW'.")
    reason: str = Field(..., description="Reason the flag was generated.")
    conflict: Optional[Conflict] = Field(None, description="The associated conflict, if any.")
    missing_information: Optional[str] = Field(None, description="Description of what information is missing, if applicable.")
