"""
Agent state schema for the discharge summary generation system.
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from schemas.evidence import Evidence
from schemas.page import Page
from schemas.review import ReviewFlag


class AgentState(BaseModel):
    """
    Represents the state of the agent during the extraction and generation loop.
    Contains all aggregated evidence and pages.
    """
    pages: List[Page] = Field(default_factory=list, description="Extracted pages from the document.")
    diagnoses: List[Evidence] = Field(default_factory=list, description="Extracted diagnoses.")
    medications: List[Evidence] = Field(default_factory=list, description="Extracted medications.")
    allergies: List[Evidence] = Field(default_factory=list, description="Extracted allergies.")
    procedures: List[Evidence] = Field(default_factory=list, description="Extracted procedures.")
    pending_results: List[Evidence] = Field(default_factory=list, description="Extracted pending results.")
    review_flags: List['ReviewFlag'] = Field(default_factory=list, description="Flags for clinician review (Sprint 3).")
    execution_trace: List[str] = Field(default_factory=list, description="Trace of agent execution steps (Sprint 4).")

    
    aggregated_evidence: Dict[str, List[Evidence]] = Field(
        default_factory=dict, 
        description="Aggregated evidence grouped by category."
    )
