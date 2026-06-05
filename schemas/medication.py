"""
Medication schemas for clinical evidence extraction.
"""
from pydantic import BaseModel, Field


class MedicationContext(BaseModel):
    """
    Clinical context around a medication, including dosage, frequency, route, and status.
    """
    dosage: str = Field(..., description="The dosage of the medication. Use 'Not Documented' if missing.")
    frequency: str = Field(..., description="How often the medication is taken. Use 'Not Documented' if missing.")
    route: str = Field(..., description="Route of administration. Use 'Not Documented' if missing.")
    status: str = Field(..., description="Status of the medication (e.g., 'Admission', 'Discharge', 'Discontinued'). Use 'Not Documented' if missing.")


class Medication(BaseModel):
    """
    Medication representation with its clinical context.
    """
    name: str = Field(..., description="The name of the medication.")
    context: MedicationContext = Field(..., description="Clinical context for the medication.")
