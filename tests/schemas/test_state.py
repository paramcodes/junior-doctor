"""
Tests for AgentState schema.
"""
from schemas.state import AgentState
from schemas.page import Page
from schemas.evidence import Evidence


def test_agent_state_initialization():
    """
    Test empty AgentState creation.
    """
    state = AgentState()
    assert len(state.pages) == 0
    assert len(state.diagnoses) == 0
    assert len(state.medications) == 0
    assert len(state.allergies) == 0
    assert len(state.procedures) == 0
    assert len(state.pending_results) == 0
    assert len(state.review_flags) == 0
    assert isinstance(state.aggregated_evidence, dict)


def test_agent_state_with_data():
    """
    Test AgentState with data appended.
    """
    state = AgentState()
    
    page = Page(page_number=1, text="Sample", has_text=True, ocr_applied=False)
    state.pages.append(page)
    
    evidence = Evidence(fact="Hypertension", page_number=1, source_document="doc", source_text="HTN")
    state.diagnoses.append(evidence)
    
    assert len(state.pages) == 1
    assert len(state.diagnoses) == 1
    assert state.diagnoses[0].fact == "Hypertension"
