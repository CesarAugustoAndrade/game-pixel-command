"""
Unit entity - represents a military unit in combat.
"""

from typing import Dict, Any
from src.entities.entity import Entity
from src.entities.components import *


class Unit(Entity):
    """
    Represents a military unit with all necessary components.
    """

    def __init__(
        self,
        unit_type: str,
        faction: str,
        position: tuple,
        count: int = 100,
        is_player: bool = False,
    ):
        """
        Initialize a unit.

        Args:
            unit_type: Type of unit (infantry, cavalry, archer, etc.)
            faction: Faction this unit belongs to
            position: (row, col) starting position in formation grid
            count: Number of soldiers in unit
            is_player: Whether this is a player-controlled unit
        """
        super().__init__()

        # Add all necessary components
        self.add_component(PositionComponent(row=position[0], col=position[1], side="player" if is_player else "enemy"))
        self.add_component(UnitComponent(unit_type=unit_type, count=count, max_count=count))
        self.add_component(FactionComponent(faction=faction, is_player_controlled=is_player))

        # Add stats based on unit type
        stats = self._get_unit_stats(unit_type)
        self.add_component(StatsComponent(**stats))

        # Add default components
        self.add_component(MoraleComponent())
        self.add_component(MovementComponent())
        self.add_component(CombatComponent())
        self.add_component(FormationComponent())
        self.add_component(EquipmentComponent())

        # Add AI component if not player controlled
        if not is_player:
            self.add_component(AIComponent())

        # Add sprite component (placeholder)
        self.add_component(SpriteComponent(sprite_path=f"assets/sprites/units/{unit_type}.png"))

    def _get_unit_stats(self, unit_type: str) -> Dict[str, int]:
        """
        Get default stats for a unit type.

        Args:
            unit_type: Type of unit

        Returns:
            Dict of stat values
        """
        # Default stats by unit type
        stats_by_type = {
            "infantry": {
                "attack": 12,
                "defense": 14,
                "health": 120,
                "max_health": 120,
                "armor": 5,
                "damage_min": 2,
                "damage_max": 8,
            },
            "cavalry": {
                "attack": 16,
                "defense": 10,
                "health": 100,
                "max_health": 100,
                "armor": 3,
                "damage_min": 3,
                "damage_max": 12,
            },
            "archer": {
                "attack": 14,
                "defense": 8,
                "health": 80,
                "max_health": 80,
                "armor": 2,
                "damage_min": 2,
                "damage_max": 6,
            },
            "spearman": {
                "attack": 10,
                "defense": 16,
                "health": 110,
                "max_health": 110,
                "armor": 6,
                "damage_min": 2,
                "damage_max": 7,
            },
        }

        return stats_by_type.get(
            unit_type,
            {
                "attack": 10,
                "defense": 10,
                "health": 100,
                "max_health": 100,
                "armor": 0,
                "damage_min": 1,
                "damage_max": 6,
            },
        )

    def get_display_name(self) -> str:
        """Get display name for this unit."""
        unit_comp = self.get_component(UnitComponent)
        faction_comp = self.get_component(FactionComponent)

        if unit_comp and faction_comp:
            return f"{faction_comp.faction.capitalize()} {unit_comp.unit_type.capitalize()}"
        return "Unknown Unit"

    def is_alive(self) -> bool:
        """Check if unit still has troops."""
        unit_comp = self.get_component(UnitComponent)
        return unit_comp and unit_comp.count > 0

    def take_casualties(self, casualties: int) -> int:
        """
        Apply casualties to unit.

        Args:
            casualties: Number of casualties

        Returns:
            Actual casualties applied
        """
        unit_comp = self.get_component(UnitComponent)
        if not unit_comp:
            return 0

        actual_casualties = min(casualties, unit_comp.count)
        unit_comp.count -= actual_casualties

        return actual_casualties

    # ========================================================================
    # Component Property Accessors (for convenience)
    # ========================================================================

    @property
    def stats_component(self):
        """Get stats component."""
        return self.get_component(StatsComponent)

    @property
    def position_component(self):
        """Get position component."""
        return self.get_component(PositionComponent)

    @property
    def unit_component(self):
        """Get unit component."""
        return self.get_component(UnitComponent)

    @property
    def faction_component(self):
        """Get faction component."""
        return self.get_component(FactionComponent)

    @property
    def morale_component(self):
        """Get morale component."""
        return self.get_component(MoraleComponent)

    @property
    def movement_component(self):
        """Get movement component."""
        return self.get_component(MovementComponent)

    @property
    def combat_component(self):
        """Get combat component."""
        return self.get_component(CombatComponent)

    @property
    def ai_component(self):
        """Get AI component."""
        return self.get_component(AIComponent)

    @property
    def formation_component(self):
        """Get formation component."""
        return self.get_component(FormationComponent)

    @property
    def equipment_component(self):
        """Get equipment component."""
        return self.get_component(EquipmentComponent)

    @property
    def sprite_component(self):
        """Get sprite component."""
        return self.get_component(SpriteComponent)
