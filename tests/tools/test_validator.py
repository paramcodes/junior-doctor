"""
Tests for Validator tool.
"""
from schemas.state import AgentState
from schemas.evidence import Evidence
from schemas.medication import Medication, MedicationContext
from tools.validator import validate_state


def test_validate_missing_categories():
    """Test validation flags when entire categories are missing."""
    state = AgentState()
    
    state = validate_state(state)
    
    # Should flag missing diagnoses and missing medications
    assert len(state.review_flags) == 2
    reasons = [flag.reason for flag in state.review_flags]
    assert any("No diagnoses found" in r for r in reasons)
    assert any("No medications found" in r for r in reasons)


def test_validate_missing_dosage():
    """Test validation flags when a medication is missing dosage."""
    state = AgentState()
    
    state.diagnoses.append(Evidence(fact="Test", page_number=1, source_document="doc", source_text="test"))
    
    med = Medication(
        name="Aspirin", 
        context=MedicationContext(dosage="Not Documented", frequency="Daily", route="PO", status="Admission")
    )
    state.medications.append(Evidence(fact=med, page_number=1, source_document="doc", source_text="test"))
    
    state = validate_state(state)
    
    assert len(state.review_flags) == 1
    assert "Dosage missing" in state.review_flags[0].reason
