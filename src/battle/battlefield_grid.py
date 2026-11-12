"""
Battlefield grid with pixel-based positioning for large-scale battles.
Supports 8-12 units per side with flexible positioning.
"""

from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass
from enum import Enum


class BattlefieldZone(Enum):
    """Zones on the battlefield."""
    PLAYER_DEPLOYMENT = "player_deployment"
    PLAYER_FORWARD = "player_forward"
    NEUTRAL = "neutral"
    ENEMY_FORWARD = "enemy_forward"
    ENEMY_DEPLOYMENT = "enemy_deployment"


@dataclass
class BattlePosition:
    """
    Pixel-based position on battlefield.
    """
    x: int  # Pixel x-coordinate (0-1000)
    y: int  # Pixel y-coordinate (0-500)
    facing: float = 0.0  # Direction in degrees (0=right, 90=down, 180=left, 270=up)

    def distance_to(self, other: 'BattlePosition') -> float:
        """Calculate distance to another position."""
        import math
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def angle_to(self, other: 'BattlePosition') -> float:
        """Calculate angle to another position in degrees."""
        import math
        dx = other.x - self.x
        dy = other.y - self.y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        return angle_deg % 360

    def is_in_arc(self, other: 'BattlePosition', arc_width: float = 90.0) -> bool:
        """
        Check if another position is in this position's facing arc.

        Args:
            other: Target position
            arc_width: Width of arc in degrees (default 90° = front quarter)

        Returns:
            True if target is in facing arc
        """
        angle_to_target = self.angle_to(other)
        angle_diff = abs((angle_to_target - self.facing + 180) % 360 - 180)
        return angle_diff <= arc_width / 2

    def to_screen(self, battlefield: 'BattlefieldGrid') -> Tuple[int, int]:
        """Convert battlefield coordinates to screen coordinates."""
        screen_x = battlefield.screen_offset_x + self.x
        screen_y = battlefield.screen_offset_y + self.y
        return (screen_x, screen_y)


class BattlefieldGrid:
    """
    Large battlefield with pixel-based positioning.

    Battlefield dimensions: 1000x500 pixels
    Screen: 1280x720 pixels (battlefield centered)

    Zones:
    - Player deployment: x=0-300 (left side)
    - Player forward: x=300-450
    - Neutral zone: x=450-550 (center)
    - Enemy forward: x=550-700
    - Enemy deployment: x=700-1000 (right side)
    """

    # Battlefield dimensions
    WIDTH = 1000
    HEIGHT = 500

    # Zone boundaries (x-coordinates)
    PLAYER_DEPLOYMENT_X = (0, 300)
    PLAYER_FORWARD_X = (300, 450)
    NEUTRAL_X = (450, 550)
    ENEMY_FORWARD_X = (550, 700)
    ENEMY_DEPLOYMENT_X = (700, 1000)

    # Screen positioning (battlefield centered on 1280x720 screen)
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    def __init__(self):
        """Initialize battlefield grid."""
        # Center battlefield on screen
        self.screen_offset_x = (self.SCREEN_WIDTH - self.WIDTH) // 2
        self.screen_offset_y = (self.SCREEN_HEIGHT - self.HEIGHT) // 2

        # Track unit positions
        self.unit_positions: Dict[int, BattlePosition] = {}  # unit_id -> position

    def get_zone(self, position: BattlePosition) -> BattlefieldZone:
        """Get the zone for a given position."""
        x = position.x

        if self.PLAYER_DEPLOYMENT_X[0] <= x < self.PLAYER_DEPLOYMENT_X[1]:
            return BattlefieldZone.PLAYER_DEPLOYMENT
        elif self.PLAYER_FORWARD_X[0] <= x < self.PLAYER_FORWARD_X[1]:
            return BattlefieldZone.PLAYER_FORWARD
        elif self.NEUTRAL_X[0] <= x < self.NEUTRAL_X[1]:
            return BattlefieldZone.NEUTRAL
        elif self.ENEMY_FORWARD_X[0] <= x < self.ENEMY_FORWARD_X[1]:
            return BattlefieldZone.ENEMY_FORWARD
        else:
            return BattlefieldZone.ENEMY_DEPLOYMENT

    def is_valid_position(self, position: BattlePosition, side: str) -> bool:
        """
        Check if a position is valid for a unit on the given side.

        Args:
            position: Position to check
            side: "player" or "enemy"

        Returns:
            True if position is valid
        """
        # Check bounds
        if not (0 <= position.x < self.WIDTH and 0 <= position.y < self.HEIGHT):
            return False

        zone = self.get_zone(position)

        # Player units can be in player zones or neutral
        if side == "player":
            return zone in [
                BattlefieldZone.PLAYER_DEPLOYMENT,
                BattlefieldZone.PLAYER_FORWARD,
                BattlefieldZone.NEUTRAL
            ]
        # Enemy units can be in enemy zones or neutral
        else:
            return zone in [
                BattlefieldZone.ENEMY_DEPLOYMENT,
                BattlefieldZone.ENEMY_FORWARD,
                BattlefieldZone.NEUTRAL
            ]

    def place_unit(self, unit_id: int, position: BattlePosition):
        """
        Place a unit at a position.

        Args:
            unit_id: Unit identifier
            position: Battle position
        """
        self.unit_positions[unit_id] = position

    def get_unit_position(self, unit_id: int) -> Optional[BattlePosition]:
        """Get position of a unit."""
        return self.unit_positions.get(unit_id)

    def remove_unit(self, unit_id: int):
        """Remove a unit from the battlefield."""
        if unit_id in self.unit_positions:
            del self.unit_positions[unit_id]

    def get_units_in_range(
        self,
        position: BattlePosition,
        range_pixels: float,
        exclude_ids: Optional[List[int]] = None
    ) -> List[int]:
        """
        Get all units within range of a position.

        Args:
            position: Center position
            range_pixels: Range in pixels
            exclude_ids: Unit IDs to exclude

        Returns:
            List of unit IDs within range
        """
        exclude_ids = exclude_ids or []
        units_in_range = []

        for unit_id, unit_pos in self.unit_positions.items():
            if unit_id in exclude_ids:
                continue

            if position.distance_to(unit_pos) <= range_pixels:
                units_in_range.append(unit_id)

        return units_in_range

    def get_units_in_zone(self, zone: BattlefieldZone) -> List[int]:
        """Get all units in a specific zone."""
        units = []
        for unit_id, position in self.unit_positions.items():
            if self.get_zone(position) == zone:
                units.append(unit_id)
        return units

    def screen_to_battlefield(self, screen_x: int, screen_y: int) -> Optional[BattlePosition]:
        """
        Convert screen coordinates to battlefield position.

        Args:
            screen_x: Screen x-coordinate
            screen_y: Screen y-coordinate

        Returns:
            BattlePosition if valid, None otherwise
        """
        battlefield_x = screen_x - self.screen_offset_x
        battlefield_y = screen_y - self.screen_offset_y

        if 0 <= battlefield_x < self.WIDTH and 0 <= battlefield_y < self.HEIGHT:
            return BattlePosition(battlefield_x, battlefield_y)

        return None

    def get_default_facing(self, side: str) -> float:
        """
        Get default facing direction for a side.

        Args:
            side: "player" or "enemy"

        Returns:
            Facing angle in degrees
        """
        # Player units face right (toward enemy)
        if side == "player":
            return 0.0
        # Enemy units face left (toward player)
        else:
            return 180.0

    def clear(self):
        """Clear all unit positions."""
        self.unit_positions.clear()
