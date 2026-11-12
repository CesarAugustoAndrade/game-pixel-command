"""
Component definitions for ECS architecture.
Components are pure data containers with no logic.
"""

from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class PositionComponent:
    """
    Position in formation grid.
    Changed from hex coordinates to simple 2x2 grid per side.
    """

    row: int  # 0=front row, 1=back row
    col: int  # 0=left, 1=right
    side: str = "player"  # "player" or "enemy"

    # Backward compatibility properties (for old hex code)
    @property
    def x(self) -> int:
        """Alias for col (backward compatibility)"""
        return self.col

    @x.setter
    def x(self, value: int):
        self.col = value

    @property
    def y(self) -> int:
        """Alias for row (backward compatibility)"""
        return self.row

    @y.setter
    def y(self, value: int):
        self.row = value

    # Legacy hex coordinate support (deprecated)
    @property
    def q(self) -> int:
        return self.col

    @property
    def r(self) -> int:
        return self.row


@dataclass
class SpriteComponent:
    """Visual representation."""

    sprite_path: str
    scale: Tuple[int, int] = (32, 32)
    offset: Tuple[int, int] = (0, 0)


@dataclass
class StatsComponent:
    """Combat statistics."""

    attack: int = 10
    defense: int = 10
    health: int = 100
    max_health: int = 100
    armor: int = 0
    damage_min: int = 1
    damage_max: int = 6


@dataclass
class MoraleComponent:
    """Morale and psychological state."""

    current: int = 100
    max_morale: int = 100
    is_broken: bool = False
    is_routed: bool = False


@dataclass
class MovementComponent:
    """Movement capabilities."""

    movement_points: int = 3
    max_movement: int = 3
    has_moved: bool = False


@dataclass
class UnitComponent:
    """Unit-specific data."""

    unit_type: str  # "infantry", "cavalry", "archer", etc.
    count: int = 100  # Number of soldiers in unit
    max_count: int = 100
    experience: int = 0
    veterancy: int = 0  # 0=raw, 1=regular, 2=veteran, 3=elite


@dataclass
class FactionComponent:
    """Faction/allegiance."""

    faction: str  # "rome", "greece", "persia", "carthage"
    is_player_controlled: bool = False


@dataclass
class CombatComponent:
    """Combat-related data."""

    range: int = 1  # Attack range in hexes
    actions_remaining: int = 2
    max_actions: int = 2
    can_attack: bool = True
    can_move: bool = True


@dataclass
class FormationComponent:
    """Formation data."""

    formation_type: str = "none"
    formation_position: int = 0  # Position within formation
    in_formation: bool = False


@dataclass
class EquipmentComponent:
    """Equipment and gear."""

    weapon: Optional[str] = None
    armor: Optional[str] = None
    special_equipment: list = None

    def __post_init__(self):
        if self.special_equipment is None:
            self.special_equipment = []


@dataclass
class AbilityComponent:
    """Special abilities."""

    abilities: list = None
    cooldowns: dict = None

    def __post_init__(self):
        if self.abilities is None:
            self.abilities = []
        if self.cooldowns is None:
            self.cooldowns = {}


@dataclass
class AIComponent:
    """AI behavior data."""

    ai_type: str = "aggressive"  # "aggressive", "defensive", "balanced"
    target_priority: str = "nearest"  # "nearest", "weakest", "strongest"
    target_unit_id: Optional[int] = None


@dataclass
class StatusEffectComponent:
    """Status effects (buffs/debuffs)."""

    effects: list = None
    durations: dict = None

    def __post_init__(self):
        if self.effects is None:
            self.effects = []
        if self.durations is None:
            self.durations = {}


@dataclass
class HeroComponent:
    """Hero/commander-specific data."""

    name: str = "Unknown Hero"
    level: int = 1
    experience: int = 0
    hero_abilities: list = None
    command_radius: int = 3  # Affects units within this range

    def __post_init__(self):
        if self.hero_abilities is None:
            self.hero_abilities = []
