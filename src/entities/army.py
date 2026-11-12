"""
Army - collection of units under a player/faction's command.
"""

from typing import List, Dict, Any
from src.entities.unit import Unit


class Army:
    """
    Represents an army - a collection of units and resources.
    """

    def __init__(self, faction: str, is_player: bool = False):
        """
        Initialize army.

        Args:
            faction: Faction this army belongs to
            is_player: Whether this is the player's army
        """
        self.faction = faction
        self.is_player = is_player
        self.units: List[Unit] = []

        # Resources
        self.gold = 0
        self.food = 0
        self.supplies = 0

        # Commander system
        self.commander_name = "Commander"
        self.commander_id = None  # Commander ID from commander_data
        self.commander_bonuses = {}  # Commander bonuses
        self.commander_abilities = []  # Commander abilities
        self.commander_stats = {}  # Commander stats
        self.banner = None  # Visual identifier

    def set_commander(self, commander_id: str) -> None:
        """
        Set commander for this army and apply bonuses.

        Args:
            commander_id: Commander ID from commander_data
        """
        from src.data.commander_data import get_commander_data, apply_commander_bonuses

        # Apply commander to army
        apply_commander_bonuses(self, commander_id)

    def get_commander_bonus(self, bonus_type: str) -> float:
        """
        Get a specific commander bonus value.

        Args:
            bonus_type: Type of bonus (e.g., 'morale', 'movement')

        Returns:
            Bonus value (0.0 if not found)
        """
        return self.commander_bonuses.get(bonus_type, 0.0)

    def add_unit(self, unit: Unit) -> None:
        """
        Add a unit to the army.

        Args:
            unit: Unit to add
        """
        self.units.append(unit)

    def remove_unit(self, unit: Unit) -> None:
        """
        Remove a unit from the army.

        Args:
            unit: Unit to remove
        """
        if unit in self.units:
            self.units.remove(unit)

    def get_total_strength(self) -> int:
        """
        Calculate total army strength.

        Returns:
            Total troop count across all units
        """
        total = 0
        for unit in self.units:
            unit_comp = unit.get_component("UnitComponent")
            if unit_comp:
                total += unit_comp.count
        return total

    def get_average_morale(self) -> float:
        """
        Calculate average morale across all units.

        Returns:
            Average morale (0-100)
        """
        if not self.units:
            return 0.0

        total_morale = 0
        for unit in self.units:
            morale_comp = unit.get_component("MoraleComponent")
            if morale_comp:
                total_morale += morale_comp.current

        return total_morale / len(self.units)

    def get_units_by_type(self, unit_type: str) -> List[Unit]:
        """
        Get all units of a specific type.

        Args:
            unit_type: Type of unit to filter

        Returns:
            List of matching units
        """
        matching_units = []
        for unit in self.units:
            unit_comp = unit.get_component("UnitComponent")
            if unit_comp and unit_comp.unit_type == unit_type:
                matching_units.append(unit)
        return matching_units

    def is_defeated(self) -> bool:
        """
        Check if army is defeated (no units or all routed).

        Returns:
            True if army is defeated
        """
        if not self.units:
            return True

        # Check if all units are routed or dead
        for unit in self.units:
            if unit.is_alive():
                morale_comp = unit.get_component("MoraleComponent")
                if not morale_comp or not morale_comp.is_routed:
                    return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize army to dictionary.

        Returns:
            Dict representation of army
        """
        return {
            "faction": self.faction,
            "is_player": self.is_player,
            "commander_name": self.commander_name,
            "commander_id": self.commander_id,
            "gold": self.gold,
            "food": self.food,
            "supplies": self.supplies,
            "unit_count": len(self.units),
            "total_strength": self.get_total_strength(),
            "average_morale": self.get_average_morale(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Army":
        """
        Deserialize army from dictionary.

        Args:
            data: Dict representation

        Returns:
            Army instance
        """
        army = Army(data["faction"], data["is_player"])
        army.commander_name = data.get("commander_name", "Commander")
        army.commander_id = data.get("commander_id", None)
        army.gold = data.get("gold", 0)
        army.food = data.get("food", 0)
        army.supplies = data.get("supplies", 0)

        # Reapply commander bonuses if commander exists
        if army.commander_id:
            army.set_commander(army.commander_id)

        # Units would need to be deserialized separately
        return army
