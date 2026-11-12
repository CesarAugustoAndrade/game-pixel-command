"""
Battle system module.
New formation-based (4v4) system.
"""

from src.battle.position_grid import FormationGrid, PositionSlot
from src.battle.targeting_system import TargetingSystem
from src.battle.combat_calculator import CombatCalculator
from src.battle.turn_manager import TurnManager
from src.battle.morale_system import MoraleSystem

__all__ = [
    'FormationGrid',
    'PositionSlot',
    'TargetingSystem',
    'CombatCalculator',
    'TurnManager',
    'MoraleSystem',
]
