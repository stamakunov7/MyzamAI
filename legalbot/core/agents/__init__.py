"""
Multi-Agent System for LegalBot+
"""

from .legal_expert import LegalExpertAgent
from .summarizer import SummarizerAgent
from .translator import TranslatorAgent
from .reviewer_agent import ReviewerAgent
from .user_interface_agent import UserInterfaceAgent

__all__ = [
    'LegalExpertAgent',
    'SummarizerAgent',
    'TranslatorAgent',
    'ReviewerAgent',
    'UserInterfaceAgent'
]

