"""
Tests for Medication and MedicationContext schemas.
"""
from schemas.medication import Medication, MedicationContext


def test_medication_creation():
    """
    Test valid creation of a Medication model.
    """
    context = MedicationContext(
        dosage="50mg",
        frequency="BID",
        route="PO",
        status="Admission"
    )
    
    med = Medication(
        name="Metoprolol",
        context=context
    )
    
    assert med.name == "Metoprolol"
    assert med.context.dosage == "50mg"
    assert med.context.frequency == "BID"
    assert med.context.route == "PO"
    assert med.context.status == "Admission"


def test_medication_missing_fields():
    """
    Test Medication creation when some fields are missing (should default to 'Not Documented' properly when provided by logic).
    """
    context = MedicationContext(
        dosage="Not Documented",
        frequency="Not Documented",
        route="Not Documented",
        status="Not Documented"
    )
    
    med = Medication(
        name="Unknown Med",
        context=context
    )
    
    assert med.context.dosage == "Not Documented"
    assert med.context.status == "Not Documented"
