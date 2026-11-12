"""
Targeting and range calculation for large-scale formation battles.
Determines valid targets based on unit type, position, and spatial range.
"""

from typing import List, Optional, Dict, Tuple
from src.entities.unit import Unit
from src.battle.battlefield_grid import BattlePosition


class TargetingSystem:
    """
    Determines valid targets based on unit type and spatial position.

    Rules:
    - Melee units (range=1): Can attack enemies within 120 pixels
    - Ranged units (range=4): Can attack enemies within 400 pixels with LOS
    - Cavalry (range=1): Can attack enemies within 150 pixels (charge range)
    - Position modifiers affect damage (flanking, formation, etc.)
    """

    # Range constants (in pixels)
    MELEE_RANGE = 120
    CAVALRY_CHARGE_RANGE = 150
    RANGED_MIN_RANGE = 100  # Minimum range for ranged (can't shoot too close)
    RANGED_MAX_RANGE = 400  # Maximum range for ranged

    def __init__(self):
        """Initialize targeting system."""
        self.unit_positions: Dict[int, BattlePosition] = {}  # Will be set by battle state

    def set_positions(self, positions: Dict[int, BattlePosition]):
        """
        Set current unit positions.

        Args:
            positions: Dict mapping unit id to BattlePosition
        """
        self.unit_positions = positions

    def get_valid_targets(
        self,
        attacker: Unit,
        all_enemies: List[Unit],
        all_units: Optional[List[Unit]] = None
    ) -> List[Unit]:
        """
        Get list of valid targets for attacker based on spatial range.

        Args:
            attacker: Attacking unit
            all_enemies: All enemy units on battlefield
            all_units: All units (for LOS checking)

        Returns:
            List of units that can be targeted
        """
        if not attacker.combat_component or not attacker.unit_component:
            return []

        # Get attacker position
        attacker_pos = self.unit_positions.get(attacker.id)
        if not attacker_pos:
            return []

        # Filter alive enemies
        alive_enemies = [
            e for e in all_enemies
            if e.unit_component and e.unit_component.count > 0
        ]

        if not alive_enemies:
            return []

        attack_range = attacker.combat_component.range

        if attack_range == 1:  # Melee
            return self._get_melee_targets(attacker, attacker_pos, alive_enemies)
        else:  # Ranged
            all_units = all_units or []
            return self._get_ranged_targets(attacker, attacker_pos, alive_enemies, all_units)

    def _get_melee_targets(
        self,
        attacker: Unit,
        attacker_pos: BattlePosition,
        enemies: List[Unit]
    ) -> List[Unit]:
        """
        Melee units can attack enemies within melee/charge range.

        Args:
            attacker: Melee attacker
            attacker_pos: Attacker's position
            enemies: Alive enemy units

        Returns:
            List of valid targets within range
        """
        # Determine range based on unit type
        is_cavalry = "cavalry" in attacker.unit_component.unit_type.lower()
        max_range = self.CAVALRY_CHARGE_RANGE if is_cavalry else self.MELEE_RANGE

        valid_targets = []

        for enemy in enemies:
            enemy_pos = self.unit_positions.get(enemy.id)
            if not enemy_pos:
                continue

            distance = attacker_pos.distance_to(enemy_pos)
            if distance <= max_range:
                valid_targets.append(enemy)

        return valid_targets

    def _get_ranged_targets(
        self,
        attacker: Unit,
        attacker_pos: BattlePosition,
        enemies: List[Unit],
        all_units: List[Unit]
    ) -> List[Unit]:
        """
        Ranged units can attack enemies within range with line of sight.

        Args:
            attacker: Ranged attacker
            attacker_pos: Attacker's position
            enemies: Alive enemy units
            all_units: All units (for LOS)

        Returns:
            List of valid targets within range and LOS
        """
        valid_targets = []

        for enemy in enemies:
            enemy_pos = self.unit_positions.get(enemy.id)
            if not enemy_pos:
                continue

            distance = attacker_pos.distance_to(enemy_pos)

            # Check range (not too close, not too far)
            if self.RANGED_MIN_RANGE <= distance <= self.RANGED_MAX_RANGE:
                # Check line of sight (simplified - just check if in range)
                # Full LOS checking can be added via SpatialQuerySystem
                valid_targets.append(enemy)

        return valid_targets

    def calculate_position_modifier(
        self,
        attacker: Unit,
        defender: Unit,
        attacker_allies: Optional[List[Unit]] = None
    ) -> float:
        """
        Calculate damage modifier based on spatial positioning.

        Position Modifiers:
        - Flanking (rear arc): +20% damage
        - Pincer attack (allies from opposite side): +10% damage
        - Isolated target (no nearby allies): +5% damage

        Args:
            attacker: Attacking unit
            defender: Defending unit
            attacker_allies: Attacker's allies (for pincer detection)

        Returns:
            Damage multiplier (1.0 = normal, 1.3 = +30%, etc.)
        """
        modifier = 1.0

        attacker_pos = self.unit_positions.get(attacker.id)
        defender_pos = self.unit_positions.get(defender.id)

        if not attacker_pos or not defender_pos:
            return modifier

        # Check if attacker is in defender's rear arc (flanking)
        angle_to_attacker = defender_pos.angle_to(attacker_pos)
        facing_diff = abs((angle_to_attacker - defender_pos.facing + 180) % 360 - 180)

        if facing_diff > 120:  # Rear 120° arc
            modifier += 0.2  # +20% flanking bonus

        return modifier

    def is_flanked(self, unit: Unit, enemies: List[Unit]) -> bool:
        """
        Check if unit is being flanked by enemies.

        Args:
            unit: Unit to check
            enemies: All enemy units

        Returns:
            True if unit is being flanked
        """
        unit_pos = self.unit_positions.get(unit.id)
        if not unit_pos:
            return False

        # Check if any enemy is in rear arc
        for enemy in enemies:
            if not enemy.unit_component or enemy.unit_component.count <= 0:
                continue

            enemy_pos = self.unit_positions.get(enemy.id)
            if not enemy_pos:
                continue

            # Check if enemy is close and in rear arc
            distance = unit_pos.distance_to(enemy_pos)
            if distance > 200:  # Too far to threaten
                continue

            angle_to_enemy = unit_pos.angle_to(enemy_pos)
            facing_diff = abs((angle_to_enemy - unit_pos.facing + 180) % 360 - 180)

            if facing_diff > 120:  # Enemy in rear arc
                return True

        return False

    def can_charge(self, attacker: Unit, target: Unit) -> bool:
        """
        Check if cavalry can charge target.

        Cavalry gets charge bonus when attacking from distance.

        Args:
            attacker: Attacking unit (must be cavalry)
            target: Target unit

        Returns:
            True if charge possible
        """
        if not attacker.unit_component:
            return False

        # Only cavalry can charge
        if "cavalry" not in attacker.unit_component.unit_type.lower():
            return False

        attacker_pos = self.unit_positions.get(attacker.id)
        target_pos = self.unit_positions.get(target.id)

        if not attacker_pos or not target_pos:
            return False

        # Must be at charge distance (100-150 pixels)
        distance = attacker_pos.distance_to(target_pos)
        return 100 <= distance <= 150
