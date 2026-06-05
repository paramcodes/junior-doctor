"""
Tests for Conflict Detector tool.
"""
from schemas.state import AgentState
from schemas.evidence import Evidence
from schemas.medication import Medication, MedicationContext
from tools.conflict_detector import detect_conflicts


def test_detect_dosage_conflict():
    """Test detection of conflicting dosages for same medication and status."""
    state = AgentState()
    
    med1 = Medication(
        name="Metoprolol", 
        context=MedicationContext(dosage="50mg", frequency="Daily", route="PO", status="Admission")
    )
    med2 = Medication(
        name="Metoprolol", 
        context=MedicationContext(dosage="100mg", frequency="Daily", route="PO", status="Admission")
    )
    
    state.medications.append(Evidence(fact=med1, page_number=1, source_document="doc", source_text="test"))
    state.medications.append(Evidence(fact=med2, page_number=2, source_document="doc", source_text="test2"))
    
    state = detect_conflicts(state)
    
    assert len(state.review_flags) == 1
    flag = state.review_flags[0]
    assert flag.severity == "HIGH"
    assert flag.conflict is not None
    assert flag.conflict.field == "Medication Dosage"
    assert len(flag.conflict.conflicting_evidence) == 2


def test_no_conflict():
    """Test that non-conflicting evidence doesn't create flags."""
    state = AgentState()
    
    med1 = Medication(
        name="Metoprolol", 
        context=MedicationContext(dosage="50mg", frequency="Daily", route="PO", status="Admission")
    )
    med2 = Medication(
        name="Metoprolol", 
        context=MedicationContext(dosage="50mg", frequency="Daily", route="PO", status="Admission")
    )
    
    state.medications.append(Evidence(fact=med1, page_number=1, source_document="doc", source_text="test"))
    state.medications.append(Evidence(fact=med2, page_number=2, source_document="doc", source_text="test2"))
    
    state = detect_conflicts(state)
    
    assert len(state.review_flags) == 0
