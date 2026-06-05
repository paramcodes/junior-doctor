"""
Integration tests for Sprint 5 outputs.
"""
import os
from unittest.mock import patch, MagicMock

from schemas.state import AgentState
from schemas.review import ReviewFlag
from outputs.summary_generator import generate_summary
from outputs.trace_exporter import export_trace
from outputs.review_flag_exporter import export_review_flags


@patch("outputs.summary_generator.genai.GenerativeModel")
def test_export_pipeline(mock_generative_model, tmp_path):
    """
    Test generating all final output files.
    """
    # 1. Setup mock state
    state = AgentState()
    state.execution_trace = ["Step 1", "Step 2"]
    state.review_flags.append(ReviewFlag(severity="HIGH", reason="Missing dosage"))
    
    # Setup paths in a temporary directory
    summary_path = tmp_path / "summary.md"
    trace_path = tmp_path / "trace.md"
    flags_path = tmp_path / "review_flags.md"
    
    # 2. Mock Gemini to prevent API calls
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "# Mock Discharge Summary"
    mock_model.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_model
    
    # 3. Execute exporters
    generate_summary(state, output_path=str(summary_path))
    export_trace(state, output_path=str(trace_path))
    export_review_flags(state, output_path=str(flags_path))
    
    # 4. Verify outputs
    assert os.path.exists(summary_path)
    with open(summary_path, "r") as f:
        assert "# Mock Discharge Summary" in f.read()
        
    assert os.path.exists(trace_path)
    with open(trace_path, "r") as f:
        trace_content = f.read()
        assert "# Agent Execution Trace" in trace_content
        assert "- Step 1" in trace_content
        
    assert os.path.exists(flags_path)
    with open(flags_path, "r") as f:
        flags_content = f.read()
        assert "# Clinician Review Flags" in flags_content
        assert "Missing dosage" in flags_content
