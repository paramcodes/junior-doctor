"""
Tests for agent loop.
"""
from unittest.mock import patch
from schemas.state import AgentState
from agent.actions import AgentAction
from agent.loop import run_agent_loop


@patch("agent.loop.create_plan")
@patch("agent.loop.execute_action")
def test_run_agent_loop_success(mock_execute, mock_plan):
    """Test standard execution of the agent loop."""
    state = AgentState()
    mock_plan.return_value = [AgentAction.RECONCILE, AgentAction.VALIDATE]
    mock_execute.return_value = state
    
    result = run_agent_loop(state)
    
    assert mock_execute.call_count == 2
    assert hasattr(result, "execution_trace")
    assert any("Agent loop started" in t for t in result.execution_trace)
    assert any("Step 2 completed successfully" in t for t in result.execution_trace)


@patch("agent.loop.create_plan")
@patch("agent.loop.execute_action")
def test_run_agent_loop_max_steps(mock_execute, mock_plan):
    """Test step limit enforcement."""
    state = AgentState()
    # Provide a plan larger than MAX_STEPS (which is 10)
    mock_plan.return_value = [AgentAction.VALIDATE] * 15
    mock_execute.return_value = state
    
    result = run_agent_loop(state)
    
    # Should only execute exactly 10 times due to step limit
    assert mock_execute.call_count == 10
    assert any("Max steps (10) reached" in t for t in result.execution_trace)
