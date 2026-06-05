"""
Review flags exporter.
"""
import logging
from schemas.state import AgentState

logger = logging.getLogger(__name__)


def export_review_flags(state: AgentState, output_path: str = "review_flags.md") -> None:
    """
    Export all clinical review flags and conflicts to a markdown file for clinician review.
    """
    logger.info("Exporting review flags.")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Clinician Review Flags\n\n")
        
        if not state.review_flags:
            f.write("*No review flags generated. Validation passed cleanly.*\n")
        else:
            for i, flag in enumerate(state.review_flags, 1):
                f.write(f"## Flag {i}: [{flag.severity}]\n")
                f.write(f"**Reason:** {flag.reason}\n\n")
                
                if flag.missing_information:
                    f.write(f"**Missing Info:** {flag.missing_information}\n\n")
                    
                if getattr(flag, "conflict", None):
                    f.write(f"**Conflict Field:** {flag.conflict.field}\n\n")
                    f.write(f"**Conflict Details:** {flag.conflict.description}\n\n")
                
                f.write("---\n\n")
                
    logger.info(f"Review flags successfully written to {output_path}")
