"""
Simple 2x2 grid system for formation battles.
Replaces hex grid with slot-based positioning (4v4 battles).
"""

from enum import Enum
from typing import Optional, List, Tuple
from dataclasses import dataclass


class BattleSide(Enum):
    """Which side of the battlefield"""
    PLAYER = "player"
    ENEMY = "enemy"


class GridPosition(Enum):
    """4 positions per side in 2x2 grid"""
    FRONT_LEFT = (0, 0)
    FRONT_RIGHT = (0, 1)
    BACK_LEFT = (1, 0)
    BACK_RIGHT = (1, 1)


@dataclass
class PositionSlot:
    """A single slot in the formation grid"""
    row: int  # 0=front, 1=back
    col: int  # 0=left, 1=right
    side: str  # "player" or "enemy"
    occupied_by: Optional[int] = None  # Unit ID

    def is_front_row(self) -> bool:
        """Check if this slot is in front row"""
        return self.row == 0

    def is_back_row(self) -> bool:
        """Check if this slot is in back row"""
        return self.row == 1

    def get_position_tuple(self) -> Tuple[int, int]:
        """Get (row, col) tuple"""
        return (self.row, self.col)


class FormationGrid:
    """
    Manages both player and enemy formation grids.
    Each side has 4 slots in a 2x2 grid.
    """

    def __init__(self):
        """Initialize empty grids for both sides"""
        self.player_slots = self._create_slots("player")
        self.enemy_slots = self._create_slots("enemy")

    def _create_slots(self, side: str) -> List[PositionSlot]:
        """Create 4 slots (2x2 grid) for a side"""
        slots = []
        for row in range(2):
            for col in range(2):
                slots.append(PositionSlot(row, col, side))
        return slots

    def get_slot(self, row: int, col: int, side: str) -> Optional[PositionSlot]:
        """Get a specific slot"""
        slots = self.player_slots if side == "player" else self.enemy_slots
        for slot in slots:
            if slot.row == row and slot.col == col:
                return slot
        return None

    def place_unit(self, unit_id: int, row: int, col: int, side: str) -> bool:
        """
        Place a unit in a slot.

        Returns:
            True if successful, False if slot occupied
        """
        slot = self.get_slot(row, col, side)
        if slot and slot.occupied_by is None:
            slot.occupied_by = unit_id
            return True
        return False

    def remove_unit(self, row: int, col: int, side: str):
        """Remove unit from a slot"""
        slot = self.get_slot(row, col, side)
        if slot:
            slot.occupied_by = None

    def get_unit_at(self, row: int, col: int, side: str) -> Optional[int]:
        """Get unit ID at a slot"""
        slot = self.get_slot(row, col, side)
        return slot.occupied_by if slot else None

    def is_front_row_empty(self, side: str) -> bool:
        """
        Check if entire front row is empty.
        Used for breakthrough mechanics (melee can hit back row).
        """
        slots = self.player_slots if side == "player" else self.enemy_slots
        front_row = [s for s in slots if s.row == 0]
        return all(s.occupied_by is None for s in front_row)

    def get_all_slots(self, side: str) -> List[PositionSlot]:
        """Get all slots for a side"""
        return self.player_slots if side == "player" else self.enemy_slots

    def get_occupied_slots(self, side: str) -> List[PositionSlot]:
        """Get only occupied slots for a side"""
        slots = self.player_slots if side == "player" else self.enemy_slots
        return [s for s in slots if s.occupied_by is not None]

    def count_units(self, side: str) -> int:
        """Count units on a side"""
        return len(self.get_occupied_slots(side))

    def is_slot_valid(self, row: int, col: int) -> bool:
        """Check if row/col is valid (0-1 range)"""
        return 0 <= row < 2 and 0 <= col < 2

    def clear_all(self):
        """Clear all units from both sides"""
        for slot in self.player_slots + self.enemy_slots:
            slot.occupied_by = None
