"""
Conflict detector tool.
"""
import logging
from collections import defaultdict

from schemas.state import AgentState
from schemas.review import Conflict, ReviewFlag
from schemas.medication import Medication

logger = logging.getLogger(__name__)


def detect_conflicts(state: AgentState) -> AgentState:
    """
    Deterministically detect conflicting information without choosing a winner.
    Creates Conflict objects and ReviewFlags instead.
    """
    logger.info("Starting deterministic conflict detection.")
    
    # Check for Medication Dosage/Frequency Conflicts within the same status
    meds_by_name_and_status = defaultdict(list)
    for ev in state.medications:
        med: Medication = ev.fact
        if med.name and med.name.lower() != "not documented":
            key = (med.name.lower(), med.context.status.lower())
            meds_by_name_and_status[key].append(ev)
            
    for (name, status), ev_list in meds_by_name_and_status.items():
        if len(ev_list) > 1:
            # Evaluate dosage conflicts
            dosages = {ev.fact.context.dosage.lower() for ev in ev_list if ev.fact.context.dosage.lower() != "not documented"}
            if len(dosages) > 1:
                conflict = Conflict(
                    field="Medication Dosage",
                    conflicting_evidence=ev_list,
                    description=f"Conflicting dosages found for {name.title()} ({status}): {', '.join(dosages)}"
                )
                state.review_flags.append(ReviewFlag(
                    severity="HIGH",
                    reason=f"Multiple conflicting dosages found for {name.title()}.",
                    conflict=conflict
                ))
            
            # Evaluate frequency conflicts
            freqs = {ev.fact.context.frequency.lower() for ev in ev_list if ev.fact.context.frequency.lower() != "not documented"}
            if len(freqs) > 1:
                conflict = Conflict(
                    field="Medication Frequency",
                    conflicting_evidence=ev_list,
                    description=f"Conflicting frequencies found for {name.title()} ({status}): {', '.join(freqs)}"
                )
                state.review_flags.append(ReviewFlag(
                    severity="HIGH",
                    reason=f"Multiple conflicting frequencies found for {name.title()}.",
                    conflict=conflict
                ))

    logger.info(f"Conflict detection complete. Flags count: {len(state.review_flags)}")
    return state
