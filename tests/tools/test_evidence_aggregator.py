"""
Tests for evidence aggregator tool.
"""
from schemas.state import AgentState
from schemas.page import Page
from schemas.evidence import Evidence
from tools.evidence_aggregator import aggregate_states


def test_aggregate_states():
    """
    Test aggregation of multiple AgentState objects.
    """
    # State 1
    state1 = AgentState()
    state1.pages.append(Page(page_number=1, text="P1", has_text=True, ocr_applied=False))
    state1.diagnoses.append(Evidence(fact="D1", page_number=1, source_document="doc", source_text="d1"))
    
    # State 2
    state2 = AgentState()
    state2.pages.append(Page(page_number=2, text="P2", has_text=True, ocr_applied=False))
    state2.diagnoses.append(Evidence(fact="D2", page_number=2, source_document="doc", source_text="d2"))
    state2.allergies.append(Evidence(fact="A1", page_number=2, source_document="doc", source_text="a1"))
    
    aggregated = aggregate_states([state1, state2])
    
    assert len(aggregated.pages) == 2
    assert len(aggregated.diagnoses) == 2
    assert len(aggregated.allergies) == 1
    
    assert aggregated.diagnoses[0].fact == "D1"
    assert aggregated.diagnoses[1].fact == "D2"
    
    # Check if aggregated dictionary is populated correctly
    assert len(aggregated.aggregated_evidence["diagnoses"]) == 2
    assert len(aggregated.aggregated_evidence["allergies"]) == 1
