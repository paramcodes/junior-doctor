"""
Validation tool for missing information.
"""
import logging
from schemas.state import AgentState
from schemas.review import ReviewFlag
from schemas.medication import Medication

logger = logging.getLogger(__name__)


def validate_state(state: AgentState) -> AgentState:
    """
    Validate state deterministically to ensure required information is present.
    Generates ReviewFlags for missing critical fields.
    """
    logger.info("Starting deterministic validation.")
    
    # Validate entire categories
    if not state.diagnoses:
        state.review_flags.append(ReviewFlag(
            severity="HIGH",
            reason="No diagnoses found in the document.",
            missing_information="Diagnoses list"
        ))
        
    if not state.medications:
        state.review_flags.append(ReviewFlag(
            severity="HIGH",
            reason="No medications found in the document.",
            missing_information="Medications list"
        ))
    else:
        # Validate individual critical fields within medications
        for ev in state.medications:
            med: Medication = ev.fact
            if med.name.lower() != "not documented":
                if med.context.dosage.lower() == "not documented":
                    state.review_flags.append(ReviewFlag(
                        severity="MEDIUM",
                        reason=f"Dosage missing for medication '{med.name}'.",
                        missing_information=f"Dosage for {med.name}"
                    ))
                if med.context.status.lower() == "not documented":
                    state.review_flags.append(ReviewFlag(
                        severity="MEDIUM",
                        reason=f"Status (Admission/Discharge) missing for medication '{med.name}'.",
                        missing_information=f"Status for {med.name}"
                    ))
                
    logger.info("Validation complete.")
    return state
