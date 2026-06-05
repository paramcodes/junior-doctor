"""
Agent actions definitions.
"""
from enum import Enum


class AgentAction(str, Enum):
    """
    Defines the available deterministic actions for the agent.
    """
    RECONCILE = "RECONCILE"
    DETECT_CONFLICTS = "DETECT_CONFLICTS"
    VALIDATE = "VALIDATE"
