"""
Execution trace exporter.
"""
import logging
from schemas.state import AgentState

logger = logging.getLogger(__name__)


def export_trace(state: AgentState, output_path: str = "trace.md") -> None:
    """
    Export the agent's execution trace to a markdown file.
    """
    logger.info("Exporting execution trace.")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Agent Execution Trace\n\n")
        
        trace = getattr(state, "execution_trace", [])
        if not trace:
            f.write("*No trace available.*\n")
        else:
            for step in trace:
                f.write(f"- {step}\n")
                
    logger.info(f"Trace successfully written to {output_path}")
