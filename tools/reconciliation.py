"""
Medication reconciliation tool.
"""
import logging
from collections import defaultdict
from typing import Dict, List

from schemas.state import AgentState
from schemas.evidence import Evidence
from schemas.medication import Medication
from schemas.review import ReviewFlag

logger = logging.getLogger(__name__)


def reconcile_medications(state: AgentState) -> AgentState:
    """
    Deterministically reconcile admission vs discharge medications.
    Detects discrepancies such as missing discharge status or new discharge medications.
    """
    logger.info("Starting deterministic medication reconciliation.")
    
    # Group medications by standardized name (case-insensitive)
    meds_by_name: Dict[str, List[Evidence]] = defaultdict(list)
    for ev in state.medications:
        med: Medication = ev.fact
        if med.name and med.name.lower() != "not documented":
            meds_by_name[med.name.lower()].append(ev)
            
    for name, ev_list in meds_by_name.items():
        admission_meds = []
        discharge_meds = []
        
        for ev in ev_list:
            status = ev.fact.context.status.lower()
            if "admission" in status:
                admission_meds.append(ev)
            elif "discharge" in status:
                discharge_meds.append(ev)
                
        # Rule 1: Present on admission, absent on discharge
        if admission_meds and not discharge_meds:
            state.review_flags.append(ReviewFlag(
                severity="MEDIUM",
                reason=f"Medication '{name.title()}' found on Admission but not on Discharge.",
                missing_information=f"Discharge status for {name.title()}"
            ))
            
        # Rule 2: Present on discharge, absent on admission
        if not admission_meds and discharge_meds:
            state.review_flags.append(ReviewFlag(
                severity="LOW",
                reason=f"New medication '{name.title()}' prescribed at Discharge with no Admission record."
            ))
            
    logger.info(f"Medication reconciliation complete. Added flags if discrepancies found.")
    return state
