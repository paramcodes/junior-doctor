"""
Main agent loop for execution.
"""
import logging
from schemas.state import AgentState
from agent.planner import create_plan
from agent.executor import execute_action

logger = logging.getLogger(__name__)

# Hard limit to prevent infinite loops (as required by step limits constraint)
MAX_STEPS = 10


def run_agent_loop(state: AgentState) -> AgentState:
    """
    Run the deterministic agent loop with step limits and trace logging.
    
    Args:
        state: The initial AgentState.
        
    Returns:
        AgentState: The finalized AgentState after all planning and execution.
    """
    logger.info("Starting agent loop.")
    
    # Initialize execution trace if not present
    if getattr(state, "execution_trace", None) is None:
        state.execution_trace = []
        
    state.execution_trace.append("Agent loop started.")
    
    try:
        plan = create_plan(state)
        state.execution_trace.append(f"Plan created: {[a.value for a in plan]}")
        
        steps_taken = 0
        for action in plan:
            if steps_taken >= MAX_STEPS:
                logger.warning(f"Max steps ({MAX_STEPS}) reached. Terminating loop to guarantee safety.")
                state.execution_trace.append(f"Loop terminated: Max steps ({MAX_STEPS}) reached.")
                break
                
            state.execution_trace.append(f"Executing step {steps_taken + 1}: {action.value}")
            state = execute_action(action, state)
            state.execution_trace.append(f"Step {steps_taken + 1} completed successfully.")
            
            steps_taken += 1
            
        state.execution_trace.append("Agent loop completed normally.")
    except Exception as e:
        logger.error(f"Agent loop encountered catastrophic failure: {e}")
        state.execution_trace.append(f"Agent loop aborted due to error: {e}")
        
    logger.info("Agent loop finished.")
    return state
