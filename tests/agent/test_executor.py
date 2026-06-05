"""
Tests for deterministic agent executor.
"""
from unittest.mock import patch
from schemas.state import AgentState
from agent.actions import AgentAction
from agent.executor import execute_action


@patch("agent.executor.reconcile_medications")
def test_execute_action_reconcile(mock_reconcile):
    state = AgentState()
    mock_reconcile.return_value = state
    
    result = execute_action(AgentAction.RECONCILE, state)
    
    mock_reconcile.assert_called_once_with(state)
    assert result == state


@patch("agent.executor.detect_conflicts")
def test_execute_action_detect_conflicts(mock_detect_conflicts):
    state = AgentState()
    mock_detect_conflicts.return_value = state
    
    result = execute_action(AgentAction.DETECT_CONFLICTS, state)
    
    mock_detect_conflicts.assert_called_once_with(state)
    assert result == state


@patch("agent.executor.validate_state")
def test_execute_action_validate(mock_validate):
    state = AgentState()
    mock_validate.return_value = state
    
    result = execute_action(AgentAction.VALIDATE, state)
    
    mock_validate.assert_called_once_with(state)
    assert result == state


@patch("agent.executor.reconcile_medications")
def test_execute_action_failure_handled_gracefully(mock_reconcile):
    state = AgentState()
    # Simulate a crash during execution
    mock_reconcile.side_effect = Exception("Crash")
    
    # Execution should handle the failure without raising and return the current state
    result = execute_action(AgentAction.RECONCILE, state)
    assert result == state
