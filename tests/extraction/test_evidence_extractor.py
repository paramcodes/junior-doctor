"""
Tests for Gemini evidence extractor.
"""
import json
from unittest.mock import patch, MagicMock

from schemas.page import Page
from schemas.medication import Medication
from extraction.evidence_extractor import extract_evidence_from_page


@patch("extraction.evidence_extractor.genai.GenerativeModel")
def test_extract_evidence_from_page_success(mock_generative_model):
    """
    Test successful extraction with mocked Gemini response.
    """
    mock_model = MagicMock()
    mock_response = MagicMock()
    
    mock_json = {
        "diagnoses": [{"fact": "Hypertension", "source_text": "History of Hypertension"}],
        "medications": [{
            "name": "Lisinopril", 
            "dosage": "10mg", 
            "frequency": "Daily", 
            "route": "PO", 
            "status": "Admission", 
            "source_text": "Lisinopril 10mg PO Daily"
        }],
        "allergies": [],
        "procedures": [],
        "pending_results": []
    }
    
    mock_response.text = json.dumps(mock_json)
    mock_model.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_model
    
    page = Page(page_number=1, text="History of Hypertension. Lisinopril 10mg PO Daily.", has_text=True, ocr_applied=False)
    state = extract_evidence_from_page(page, "dummy.pdf")
    
    assert len(state.diagnoses) == 1
    assert state.diagnoses[0].fact == "Hypertension"
    assert state.diagnoses[0].source_text == "History of Hypertension"
    
    assert len(state.medications) == 1
    med_fact = state.medications[0].fact
    assert isinstance(med_fact, Medication)
    assert med_fact.name == "Lisinopril"
    assert med_fact.context.dosage == "10mg"
    assert state.medications[0].source_text == "Lisinopril 10mg PO Daily"


def test_extract_evidence_empty_page():
    """
    Test extraction skips empty pages.
    """
    page = Page(page_number=1, text="   ", has_text=False, ocr_applied=False)
    state = extract_evidence_from_page(page, "dummy.pdf")
    
    # Empty page should just return a state with that page appended, no extraction
    assert len(state.pages) == 1
    assert len(state.diagnoses) == 0
    assert len(state.medications) == 0


@patch("extraction.evidence_extractor.genai.GenerativeModel")
def test_extract_evidence_failure(mock_generative_model):
    """
    Test graceful handling of Gemini API failure.
    """
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API Error")
    mock_generative_model.return_value = mock_model
    
    page = Page(page_number=1, text="Some text", has_text=True, ocr_applied=False)
    state = extract_evidence_from_page(page, "dummy.pdf")
    
    assert len(state.pages) == 1
    assert len(state.diagnoses) == 0
