"""
Tests for Medication Reconciliation tool.
"""
from schemas.state import AgentState
from schemas.evidence import Evidence
from schemas.medication import Medication, MedicationContext
from tools.reconciliation import reconcile_medications


def test_reconcile_medications_discontinued():
    """Test rule: Present on admission, absent on discharge."""
    state = AgentState()
    
    med = Medication(
        name="Aspirin", 
        context=MedicationContext(dosage="81mg", frequency="Daily", route="PO", status="Admission")
    )
    state.medications.append(Evidence(fact=med, page_number=1, source_document="doc", source_text="test"))
    
    reconciled_state = reconcile_medications(state)
    
    assert len(reconciled_state.review_flags) == 1
    flag = reconciled_state.review_flags[0]
    assert flag.severity == "MEDIUM"
    assert "Admission but not on Discharge" in flag.reason


def test_reconcile_medications_new_discharge():
    """Test rule: Present on discharge, absent on admission."""
    state = AgentState()
    
    med = Medication(
        name="Lisinopril", 
        context=MedicationContext(dosage="10mg", frequency="Daily", route="PO", status="Discharge")
    )
    state.medications.append(Evidence(fact=med, page_number=1, source_document="doc", source_text="test"))
    
    reconciled_state = reconcile_medications(state)
    
    assert len(reconciled_state.review_flags) == 1
    flag = reconciled_state.review_flags[0]
    assert flag.severity == "LOW"
    assert "New medication" in flag.reason
