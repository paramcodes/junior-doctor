"""
Tests for deterministic agent planner.
"""
from schemas.state import AgentState
from agent.actions import AgentAction
from agent.planner import create_plan


def test_create_plan():
    """Test that the planner always returns the exact sequence of required steps."""
    state = AgentState()
    plan = create_plan(state)
    
    assert len(plan) == 3
    assert plan[0] == AgentAction.RECONCILE
    assert plan[1] == AgentAction.DETECT_CONFLICTS
    assert plan[2] == AgentAction.VALIDATE
