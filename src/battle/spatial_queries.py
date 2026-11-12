"""
Spatial query system for large-scale battles.
Handles flanking detection, line-of-sight, and spatial unit relationships.
"""

from typing import List, Optional, Tuple
from src.entities.unit import Unit
from src.battle.battlefield_grid import BattlefieldGrid, BattlePosition
import math


class SpatialQuerySystem:
    """
    Performs spatial queries for battlefield tactics.
    """

    def __init__(self, battlefield: BattlefieldGrid):
        """
        Initialize spatial query system.

        Args:
            battlefield: Battlefield grid
        """
        self.battlefield = battlefield

        # Tactical constants
        self.FLANKING_ARC = 120.0  # Degrees (rear 120° arc)
        self.FORMATION_RADIUS = 80.0  # Pixels (units within this are "in formation")

    def is_flanking(
        self,
        attacker: Unit,
        target: Unit,
        attacker_position: BattlePosition,
        target_position: BattlePosition
    ) -> bool:
        """
        Detect if attacker is flanking target.

        Flanking occurs when:
        1. Attacker is in target's rear arc (120° behind)

        Args:
            attacker: Attacking unit
            target: Target unit
            attacker_position: Attacker's position
            target_position: Target's position

        Returns:
            True if flanking
        """
        # Calculate angle from target to attacker
        angle_to_attacker = target_position.angle_to(attacker_position)

        # Calculate angle difference from target's facing
        facing_diff = abs((angle_to_attacker - target_position.facing + 180) % 360 - 180)

        # Flanking if attacker is in rear arc (120° to 240° from facing)
        return facing_diff > self.FLANKING_ARC / 2

    def is_surrounded(
        self,
        unit: Unit,
        unit_position: BattlePosition,
        enemies: List[Tuple[Unit, BattlePosition]]
    ) -> bool:
        """
        Detect if a unit is surrounded by enemies.

        Surrounded = enemies on opposite sides (180° apart)

        Args:
            unit: The unit
            unit_position: Unit's position
            enemies: List of (enemy_unit, enemy_position) tuples

        Returns:
            True if surrounded
        """
        if len(enemies) < 2:
            return False

        # Get angles to all enemies
        enemy_angles = []
        for enemy, enemy_pos in enemies:
            if not enemy.is_alive():
                continue
            angle = unit_position.angle_to(enemy_pos)
            enemy_angles.append(angle)

        if len(enemy_angles) < 2:
            return False

        # Check if any two enemies are roughly opposite (160-200° apart)
        for i, angle1 in enumerate(enemy_angles):
            for angle2 in enemy_angles[i+1:]:
                angle_diff = abs((angle1 - angle2 + 180) % 360 - 180)
                if 160 <= angle_diff <= 200:
                    return True

        return False

    def has_line_of_sight(
        self,
        shooter: Unit,
        shooter_position: BattlePosition,
        target: Unit,
        target_position: BattlePosition,
        all_units: List[Tuple[Unit, BattlePosition]]
    ) -> bool:
        """
        Check if shooter has line of sight to target.

        LOS is blocked if another unit is between shooter and target.

        Args:
            shooter: Shooting unit
            shooter_position: Shooter's position
            target: Target unit
            target_position: Target's position
            all_units: All units and positions on battlefield

        Returns:
            True if LOS exists
        """
        # Simple LOS: Check if any unit is close to the line between shooter and target
        for unit, unit_pos in all_units:
            # Skip shooter and target
            if unit.id == shooter.id or unit.id == target.id:
                continue

            # Skip dead units
            if not unit.is_alive():
                continue

            # Check if unit is between shooter and target
            if self._is_point_near_line(
                unit_pos,
                shooter_position,
                target_position,
                threshold=40.0  # 40 pixel threshold
            ):
                return False  # LOS blocked

        return True  # LOS clear

    def _is_point_near_line(
        self,
        point: BattlePosition,
        line_start: BattlePosition,
        line_end: BattlePosition,
        threshold: float
    ) -> bool:
        """
        Check if a point is near a line segment.

        Args:
            point: Point to check
            line_start: Line segment start
            line_end: Line segment end
            threshold: Distance threshold in pixels

        Returns:
            True if point is within threshold of line
        """
        # Vector from line_start to line_end
        dx = line_end.x - line_start.x
        dy = line_end.y - line_start.y
        line_length_sq = dx * dx + dy * dy

        if line_length_sq == 0:
            # Line is a point
            return point.distance_to(line_start) <= threshold

        # Parameter t: how far along the line is the closest point to 'point'
        # t = 0 means line_start, t = 1 means line_end
        t = max(0, min(1, (
            (point.x - line_start.x) * dx +
            (point.y - line_start.y) * dy
        ) / line_length_sq))

        # Closest point on line segment
        closest_x = line_start.x + t * dx
        closest_y = line_start.y + t * dy

        # Distance from point to closest point on line
        dist_sq = (point.x - closest_x) ** 2 + (point.y - closest_y) ** 2
        distance = math.sqrt(dist_sq)

        return distance <= threshold

    def get_allies_in_formation(
        self,
        unit: Unit,
        unit_position: BattlePosition,
        all_allies: List[Tuple[Unit, BattlePosition]]
    ) -> List[Unit]:
        """
        Get allied units within formation radius.

        Args:
            unit: The unit
            unit_position: Unit's position
            all_allies: All allied units and positions

        Returns:
            List of units in formation
        """
        in_formation = []

        for ally, ally_pos in all_allies:
            if ally.id == unit.id:
                continue

            if not ally.is_alive():
                continue

            distance = unit_position.distance_to(ally_pos)
            if distance <= self.FORMATION_RADIUS:
                in_formation.append(ally)

        return in_formation

    def get_nearest_enemy(
        self,
        unit_position: BattlePosition,
        enemies: List[Tuple[Unit, BattlePosition]]
    ) -> Optional[Tuple[Unit, BattlePosition, float]]:
        """
        Get the nearest enemy unit.

        Args:
            unit_position: Reference position
            enemies: List of (enemy_unit, enemy_position) tuples

        Returns:
            Tuple of (nearest_enemy, position, distance) or None
        """
        nearest = None
        nearest_dist = float('inf')

        for enemy, enemy_pos in enemies:
            if not enemy.is_alive():
                continue

            distance = unit_position.distance_to(enemy_pos)
            if distance < nearest_dist:
                nearest_dist = distance
                nearest = (enemy, enemy_pos, distance)

        return nearest

    def get_vulnerable_targets(
        self,
        attacker_position: BattlePosition,
        enemies: List[Tuple[Unit, BattlePosition]]
    ) -> List[Tuple[Unit, BattlePosition]]:
        """
        Get enemies that are vulnerable (in rear arc, isolated, etc.).

        Args:
            attacker_position: Attacker's position
            enemies: All enemy units and positions

        Returns:
            List of vulnerable (unit, position) tuples
        """
        vulnerable = []

        for enemy, enemy_pos in enemies:
            if not enemy.is_alive():
                continue

            # Check if enemy is facing away (vulnerable to flank)
            angle_to_attacker = enemy_pos.angle_to(attacker_position)
            facing_diff = abs((angle_to_attacker - enemy_pos.facing + 180) % 360 - 180)

            if facing_diff > 90:  # Rear or flank (90°+)
                vulnerable.append((enemy, enemy_pos))

        return vulnerable

    def calculate_formation_cohesion(
        self,
        units: List[Tuple[Unit, BattlePosition]]
    ) -> float:
        """
        Calculate formation cohesion (0.0 to 1.0).

        Higher cohesion = units are closer together

        Args:
            units: List of (unit, position) tuples

        Returns:
            Cohesion value (0.0 = scattered, 1.0 = tight formation)
        """
        if len(units) <= 1:
            return 1.0

        # Calculate average distance between all units
        total_distance = 0.0
        pair_count = 0

        for i, (unit1, pos1) in enumerate(units):
            if not unit1.is_alive():
                continue

            for (unit2, pos2) in units[i+1:]:
                if not unit2.is_alive():
                    continue

                total_distance += pos1.distance_to(pos2)
                pair_count += 1

        if pair_count == 0:
            return 1.0

        avg_distance = total_distance / pair_count

        # Normalize: ideal formation = 80px between units
        # Cohesion = 1.0 when avg_distance = 80
        # Cohesion decreases as distance increases
        ideal_distance = 80.0
        cohesion = min(1.0, ideal_distance / max(1.0, avg_distance))

        return cohesion

    def get_flanking_bonus(
        self,
        attacker: Unit,
        target: Unit,
        attacker_position: BattlePosition,
        target_position: BattlePosition,
        allies: List[Tuple[Unit, BattlePosition]]
    ) -> float:
        """
        Calculate flanking damage bonus.

        Args:
            attacker: Attacking unit
            target: Target unit
            attacker_position: Attacker's position
            target_position: Target's position
            allies: Attacker's allies

        Returns:
            Damage multiplier (1.0 = no bonus, 1.3 = +30% damage)
        """
        bonus = 1.0

        # Basic flanking: +20% damage
        if self.is_flanking(attacker, target, attacker_position, target_position):
            bonus += 0.2

        # Pincer attack: +10% additional (ally engaging from opposite side)
        for ally, ally_pos in allies:
            if not ally.is_alive():
                continue

            if ally.id == attacker.id:
                continue

            # Check if ally is engaging from opposite side
            angle_to_ally = target_position.angle_to(ally_pos)
            angle_to_attacker = target_position.angle_to(attacker_position)

            angle_diff = abs((angle_to_ally - angle_to_attacker + 180) % 360 - 180)

            if 120 < angle_diff < 240:  # Opposite sides (±60° tolerance)
                # Check if ally is close enough to be threatening
                if ally_pos.distance_to(target_position) < 200:
                    bonus += 0.1
                    break  # Only count one pincer bonus

        return bonus
