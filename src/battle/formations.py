"""
Formation system for unit positioning and bonuses.
"""

from typing import List, Tuple, Dict, Any
from enum import Enum


class FormationType(Enum):
    """Types of military formations."""

    NONE = "none"
    LINE = "line"
    COLUMN = "column"
    WEDGE = "wedge"
    SQUARE = "square"
    SKIRMISH = "skirmish"


class Formation:
    """
    Represents a military formation with associated bonuses and requirements.
    """

    def __init__(self, formation_type: FormationType):
        """
        Initialize formation.

        Args:
            formation_type: Type of formation
        """
        self.formation_type = formation_type
        self.bonuses = self._get_formation_bonuses()
        self.required_positions = self._get_required_positions()

    def _get_formation_bonuses(self) -> Dict[str, float]:
        """
        Get stat bonuses for this formation.

        Returns:
            Dict of stat modifiers
        """
        bonuses = {
            FormationType.NONE: {},
            FormationType.LINE: {
                "defense": 1.2,
                "attack": 1.0,
                "morale": 1.1,
            },
            FormationType.COLUMN: {
                "defense": 0.9,
                "attack": 1.3,
                "morale": 1.0,
                "charge_bonus": 1.5,
            },
            FormationType.WEDGE: {
                "defense": 0.8,
                "attack": 1.4,
                "morale": 0.9,
                "charge_bonus": 2.0,
                "armor_penetration": 1.3,
            },
            FormationType.SQUARE: {
                "defense": 1.5,
                "attack": 0.7,
                "morale": 1.2,
                "anti_cavalry": 2.0,
            },
            FormationType.SKIRMISH: {
                "defense": 0.8,
                "attack": 0.9,
                "morale": 0.9,
                "mobility": 1.5,
                "ranged_defense": 1.3,
            },
        }

        return bonuses.get(self.formation_type, {})

    def _get_required_positions(self) -> List[Tuple[int, int]]:
        """
        Get required relative positions for units in formation.

        Returns:
            List of (dq, dr) relative positions
        """
        positions = {
            FormationType.NONE: [(0, 0)],
            FormationType.LINE: [
                (-1, 0),
                (0, 0),
                (1, 0),
            ],
            FormationType.COLUMN: [
                (0, -1),
                (0, 0),
                (0, 1),
            ],
            FormationType.WEDGE: [
                (0, 0),
                (-1, 1),
                (1, 1),
                (-1, 2),
                (0, 2),
                (1, 2),
            ],
            FormationType.SQUARE: [
                (-1, -1),
                (0, -1),
                (1, -1),
                (-1, 0),
                (0, 0),
                (1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
            ],
            FormationType.SKIRMISH: [
                (-2, 0),
                (0, 0),
                (2, 0),
            ],
        }

        return positions.get(self.formation_type, [(0, 0)])

    def get_bonus(self, stat: str) -> float:
        """
        Get bonus for a specific stat.

        Args:
            stat: Stat name

        Returns:
            Modifier value (1.0 = no change)
        """
        return self.bonuses.get(stat, 1.0)

    def apply_bonuses_to_unit(self, unit: Dict[str, Any]) -> None:
        """
        Apply formation bonuses to a unit's stats.

        Args:
            unit: Unit data dict
        """
        for stat, modifier in self.bonuses.items():
            if stat in unit:
                unit[f"{stat}_modified"] = unit[stat] * modifier


class FormationManager:
    """
    Manages formations for groups of units.
    """

    def __init__(self):
        """Initialize formation manager."""
        self.unit_formations: Dict[int, Formation] = {}

    def set_unit_formation(
        self, unit_id: int, formation_type: FormationType
    ) -> None:
        """
        Set formation for a unit.

        Args:
            unit_id: Unit ID
            formation_type: Type of formation
        """
        self.unit_formations[unit_id] = Formation(formation_type)

    def get_unit_formation(self, unit_id: int) -> Formation:
        """
        Get formation for a unit.

        Args:
            unit_id: Unit ID

        Returns:
            Formation object
        """
        return self.unit_formations.get(unit_id, Formation(FormationType.NONE))

    def check_formation_integrity(
        self, unit_id: int, unit_positions: Dict[int, Tuple[int, int]]
    ) -> bool:
        """
        Check if a unit is maintaining its formation.

        Args:
            unit_id: Unit to check
            unit_positions: Dict mapping unit IDs to positions

        Returns:
            True if formation is maintained
        """
        formation = self.get_unit_formation(unit_id)

        if formation.formation_type == FormationType.NONE:
            return True

        # Get unit position
        if unit_id not in unit_positions:
            return False

        unit_pos = unit_positions[unit_id]

        # Check if required positions are occupied by friendly units
        # This is a simplified check - real implementation would be more complex
        required = formation.required_positions
        return len(required) > 0  # Placeholder

    def get_formation_modifier(
        self, unit_id: int, stat: str, is_in_formation: bool = True
    ) -> float:
        """
        Get formation modifier for a unit stat.

        Args:
            unit_id: Unit ID
            stat: Stat name
            is_in_formation: Whether unit is maintaining formation

        Returns:
            Modifier value
        """
        if not is_in_formation:
            return 1.0

        formation = self.get_unit_formation(unit_id)
        return formation.get_bonus(stat)
