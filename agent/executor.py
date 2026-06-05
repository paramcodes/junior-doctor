"""
Action executor for the agent.
"""
import logging
from agent.actions import AgentAction
from schemas.state import AgentState

from tools.reconciliation import reconcile_medications
from tools.conflict_detector import detect_conflicts
from tools.validator import validate_state

logger = logging.getLogger(__name__)


def execute_action(action: AgentAction, state: AgentState) -> AgentState:
    """
    Execute a single deterministic action against the current state.
    Handles failures gracefully to ensure the agent loop does not crash unexpectedly.
    
    Args:
        action: The AgentAction to execute.
        state: The current AgentState.
        
    Returns:
        AgentState: The resulting state after execution (or original state on failure).
    """
    logger.info(f"Executing action: {action.value}")
    
    try:
        if action == AgentAction.RECONCILE:
            return reconcile_medications(state)
        elif action == AgentAction.DETECT_CONFLICTS:
            return detect_conflicts(state)
        elif action == AgentAction.VALIDATE:
            return validate_state(state)
        else:
            logger.error(f"Unknown action requested: {action}")
            return state
    except Exception as e:
        logger.error(f"Action {action.value} failed gracefully: {e}")
        # Graceful failure handling: Do not corrupt the state
        return state
