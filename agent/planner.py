"""
Deterministic planner for the agent.
"""
from typing import List
from agent.actions import AgentAction
from schemas.state import AgentState


def create_plan(state: AgentState) -> List[AgentAction]:
    """
    Deterministically plan the sequence of actions based on the current state.
    
    Args:
        state: The current AgentState.
        
    Returns:
        List[AgentAction]: A deterministic list of actions to execute.
    """
    # The pipeline executes sequentially without branching in Sprint 4
    return [
        AgentAction.RECONCILE,
        AgentAction.DETECT_CONFLICTS,
        AgentAction.VALIDATE
    ]
