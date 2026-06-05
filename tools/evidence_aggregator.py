"""
Evidence aggregation tool.
"""
import logging
from typing import List

from schemas.state import AgentState

logger = logging.getLogger(__name__)


def aggregate_states(states: List[AgentState]) -> AgentState:
    """
    Merge multiple AgentStates (e.g., from multiple pages) into a single aggregated AgentState.
    
    Args:
        states (List[AgentState]): A list of state objects extracted from individual pages.
        
    Returns:
        AgentState: A unified state with all evidence combined.
    """
    logger.info(f"Aggregating {len(states)} evidence states.")
    aggregated = AgentState()
    
    for state in states:
        aggregated.pages.extend(state.pages)
        aggregated.diagnoses.extend(state.diagnoses)
        aggregated.medications.extend(state.medications)
        aggregated.allergies.extend(state.allergies)
        aggregated.procedures.extend(state.procedures)
        aggregated.pending_results.extend(state.pending_results)
        
    # Group evidence in aggregated_evidence dict for convenience
    aggregated.aggregated_evidence = {
        "diagnoses": aggregated.diagnoses,
        "medications": aggregated.medications,
        "allergies": aggregated.allergies,
        "procedures": aggregated.procedures,
        "pending_results": aggregated.pending_results
    }
    
    logger.info("Evidence aggregation complete.")
    return aggregated
