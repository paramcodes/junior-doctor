"""
Tests for Evidence schema.
"""
from schemas.evidence import Evidence


def test_evidence_schema_creation():
    """
    Test creating a valid Evidence object.
    """
    evidence = Evidence(
        fact="Patient has hypertension",
        page_number=1,
        source_document="summary.pdf",
        source_text="Hx: hypertension."
    )
    
    assert evidence.fact == "Patient has hypertension"
    assert evidence.page_number == 1
    assert evidence.source_document == "summary.pdf"
    assert evidence.source_text == "Hx: hypertension."


def test_evidence_not_documented():
    """
    Test Evidence object for missing information scenario.
    """
    evidence = Evidence(
        fact="Not Documented",
        page_number=2,
        source_document="summary.pdf",
        source_text=""
    )
    
    assert evidence.fact == "Not Documented"
    assert evidence.page_number == 2
    assert evidence.source_document == "summary.pdf"
    assert evidence.source_text == ""
