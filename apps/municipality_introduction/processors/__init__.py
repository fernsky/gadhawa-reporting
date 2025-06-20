"""
Economics processors package for Lungri Rural Municipality.
"""

from .remittance_expenses import RemittanceExpensesProcessor
from .manager import EconomicsManager, get_economics_manager

__all__ = [
    "RemittanceExpensesProcessor",
    "EconomicsManager",
    "get_economics_manager",
]
