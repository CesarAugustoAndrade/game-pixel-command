"""
Turn management system for tactical combat.
"""

from typing import List, Dict, Any, Optional
from src.core.event_system import EventSystem, EVENT_TURN_START, EVENT_TURN_END


class TurnManager:
    """
    Manages turn order and action economy in tactical battles.
    """

    def __init__(self, event_system: EventSystem):
        """
        Initialize turn manager.

        Args:
            event_system: Event system for broadcasting turn events
        """
        self.event_system = event_system
        self.current_turn = 0
        self.current_faction = None
        self.turn_order: List[str] = []
        self.units: Dict[int, Dict[str, Any]] = {}

    def initialize_battle(self, factions: List[str], units: Dict[int, Dict[str, Any]]) -> None:
        """
        Initialize a new battle.

        Args:
            factions: List of faction names in turn order
            units: Dict mapping unit IDs to unit data
        """
        self.current_turn = 1
        self.turn_order = factions
        self.current_faction = factions[0] if factions else None
        self.units = units

        # Initialize unit action points
        for unit_id, unit in self.units.items():
            unit["actions_remaining"] = unit.get("max_actions", 2)
            unit["has_moved"] = False

        # Broadcast battle start
        self.event_system.emit(EVENT_TURN_START, {
            "turn": self.current_turn,
            "faction": self.current_faction,
        })

    def end_turn(self) -> None:
        """End the current faction's turn and advance to next faction."""
        # Broadcast turn end
        self.event_system.emit(EVENT_TURN_END, {
            "turn": self.current_turn,
            "faction": self.current_faction,
        })

        # Get current faction index
        current_index = self.turn_order.index(self.current_faction)

        # Advance to next faction
        next_index = (current_index + 1) % len(self.turn_order)
        self.current_faction = self.turn_order[next_index]

        # If we've cycled back to first faction, increment turn counter
        if next_index == 0:
            self.current_turn += 1

        # Refresh units for new faction
        self._refresh_faction_units(self.current_faction)

        # Broadcast new turn start
        self.event_system.emit(EVENT_TURN_START, {
            "turn": self.current_turn,
            "faction": self.current_faction,
        })

    def _refresh_faction_units(self, faction: str) -> None:
        """
        Refresh action points and status for all units of a faction.

        Args:
            faction: Faction name
        """
        for unit_id, unit in self.units.items():
            if unit.get("faction") == faction:
                # Restore action points
                unit["actions_remaining"] = unit.get("max_actions", 2)
                unit["has_moved"] = False

                # Apply turn-based effects (regeneration, damage over time, etc.)
                self._apply_turn_effects(unit)

    def _apply_turn_effects(self, unit: Dict[str, Any]) -> None:
        """
        Apply turn-based effects to a unit.

        Args:
            unit: Unit data
        """
        # TODO: Implement status effects, regeneration, damage over time, etc.
        pass

    def can_unit_act(self, unit_id: int) -> bool:
        """
        Check if a unit can perform actions this turn.

        Args:
            unit_id: Unit ID

        Returns:
            True if unit can act, False otherwise
        """
        unit = self.units.get(unit_id)
        if not unit:
            return False

        # Check if it's this unit's faction's turn
        if unit.get("faction") != self.current_faction:
            return False

        # Check if unit has actions remaining
        if unit.get("actions_remaining", 0) <= 0:
            return False

        # Check if unit is routed or incapacitated
        if unit.get("is_routed", False):
            return False

        return True

    def consume_action(self, unit_id: int, action_cost: int = 1) -> bool:
        """
        Consume action points for a unit action.

        Args:
            unit_id: Unit ID
            action_cost: Number of action points to consume

        Returns:
            True if action was consumed, False if not enough actions
        """
        unit = self.units.get(unit_id)
        if not unit:
            return False

        actions = unit.get("actions_remaining", 0)
        if actions < action_cost:
            return False

        unit["actions_remaining"] = actions - action_cost
        return True

    def get_active_units(self) -> List[int]:
        """
        Get all unit IDs for the current faction.

        Returns:
            List of unit IDs
        """
        active_units = []
        for unit_id, unit in self.units.items():
            if unit.get("faction") == self.current_faction:
                active_units.append(unit_id)
        return active_units

    def is_battle_over(self) -> Optional[str]:
        """
        Check if the battle is over.

        Returns:
            Winning faction name if battle is over, None otherwise
        """
        # Count active (non-routed) units per faction
        faction_units = {}
        for unit in self.units.values():
            if not unit.get("is_routed", False) and unit.get("count", 0) > 0:
                faction = unit.get("faction")
                faction_units[faction] = faction_units.get(faction, 0) + 1

        # If only one faction has units left, they win
        if len(faction_units) == 1:
            return list(faction_units.keys())[0]

        # If no factions have units, it's a draw (should be rare)
        if len(faction_units) == 0:
            return "draw"

        return None
