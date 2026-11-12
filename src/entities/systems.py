"""
ECS Systems that operate on entities with specific components.
Systems contain the logic that operates on component data.
"""

from typing import List
from src.entities.entity import Entity
from src.entities.components import *
from src.core.event_system import EventSystem


class System:
    """Base class for all systems."""

    def __init__(self, event_system: EventSystem):
        """
        Initialize system.

        Args:
            event_system: Event system for broadcasting events
        """
        self.event_system = event_system

    def update(self, entities: List[Entity], delta_time: float) -> None:
        """
        Update system logic.

        Args:
            entities: List of all entities
            delta_time: Time since last update
        """
        pass


class MovementSystem(System):
    """Handles unit movement."""

    def move_unit(
        self, entity: Entity, target_q: int, target_r: int, cost: int
    ) -> bool:
        """
        Move a unit to a new position.

        Args:
            entity: Entity to move
            target_q: Target q coordinate
            target_r: Target r coordinate
            cost: Movement cost

        Returns:
            True if movement successful
        """
        pos = entity.get_component(PositionComponent)
        movement = entity.get_component(MovementComponent)

        if not pos or not movement:
            return False

        # Check if enough movement points
        if movement.movement_points < cost:
            return False

        # Move unit
        pos.q = target_q
        pos.r = target_r
        movement.movement_points -= cost
        movement.has_moved = True

        return True

    def refresh_movement(self, entity: Entity) -> None:
        """Restore movement points for a unit."""
        movement = entity.get_component(MovementComponent)
        if movement:
            movement.movement_points = movement.max_movement
            movement.has_moved = False


class CombatSystem(System):
    """Handles combat between units."""

    def can_attack(self, attacker: Entity, defender: Entity, distance: int) -> bool:
        """
        Check if attacker can attack defender.

        Args:
            attacker: Attacking entity
            defender: Defending entity
            distance: Distance between units

        Returns:
            True if attack is valid
        """
        combat = attacker.get_component(CombatComponent)
        if not combat:
            return False

        # Check range
        if distance > combat.range:
            return False

        # Check actions
        if combat.actions_remaining <= 0:
            return False

        # Check if can attack
        if not combat.can_attack:
            return False

        return True


class MoraleSystem(System):
    """Handles morale calculations and effects."""

    def update_morale(self, entity: Entity, change: int) -> None:
        """
        Update unit morale.

        Args:
            entity: Entity to update
            change: Morale change
        """
        morale = entity.get_component(MoraleComponent)
        if not morale:
            return

        morale.current = max(0, min(morale.max_morale, morale.current + change))

        # Check for morale break
        if morale.current < 30:
            morale.is_broken = True
        if morale.current < 10:
            morale.is_routed = True


class FormationSystem(System):
    """Manages unit formations."""

    def apply_formation_bonuses(self, entity: Entity) -> None:
        """
        Apply formation bonuses to unit stats.

        Args:
            entity: Entity in formation
        """
        formation = entity.get_component(FormationComponent)
        if not formation or not formation.in_formation:
            return

        # TODO: Apply bonuses based on formation type
        pass


class AISystem(System):
    """Handles AI decision making for enemy units."""

    def __init__(self, event_system: EventSystem, grid=None, pathfinder=None):
        """
        Initialize AI system.

        Args:
            event_system: Event system
            grid: HexGrid for positioning
            pathfinder: PathFinder for movement
        """
        super().__init__(event_system)
        self.grid = grid
        self.pathfinder = pathfinder

    def update(self, entities: List[Entity], delta_time: float) -> None:
        """
        Update AI for all AI-controlled units.

        Args:
            entities: All entities
            delta_time: Time since last update
        """
        for entity in entities:
            if not entity.is_active:
                continue

            ai = entity.get_component(AIComponent)
            faction = entity.get_component(FactionComponent)

            if ai and faction and not faction.is_player_controlled:
                self._process_ai(entity, entities)

    def process_unit_ai(self, unit: Entity, all_units: List[Entity], grid, pathfinder):
        """
        Process AI for a unit and return decision.

        Args:
            unit: Unit to process
            all_units: All units in battle
            grid: Battle grid
            pathfinder: Pathfinder instance

        Returns:
            Tuple of (action_type, target):
            - ("attack", target_unit)
            - ("move", (q, r))
            - ("hold", None)
        """
        self.grid = grid
        self.pathfinder = pathfinder

        ai = unit.get_component(AIComponent)
        if not ai:
            return ("hold", None)

        # Get enemy targets (player units)
        targets = self._get_enemy_targets(unit, all_units)
        if not targets:
            return ("hold", None)

        # Select best target based on priority
        selected_target = self._select_target(unit, targets, ai.target_priority)

        # Make decision based on AI type
        if ai.ai_type == "aggressive":
            return self._aggressive_behavior(unit, selected_target, all_units)
        elif ai.ai_type == "defensive":
            return self._defensive_behavior(unit, selected_target, all_units)
        else:  # balanced
            return self._balanced_behavior(unit, selected_target, all_units)

    def _process_ai(self, entity: Entity, all_entities: List[Entity]) -> None:
        """
        Process AI for a single entity.

        Args:
            entity: Entity to process
            all_entities: All entities in scene
        """
        # This is called by update() but we now use process_unit_ai() from battle
        pass

    def _get_enemy_targets(self, unit: Entity, all_units: List[Entity]) -> List[Entity]:
        """
        Get list of enemy targets for this unit.

        Args:
            unit: AI unit
            all_units: All units

        Returns:
            List of enemy units
        """
        faction = unit.get_component(FactionComponent)
        if not faction:
            return []

        targets = []
        for other in all_units:
            if not other.is_active:
                continue

            other_faction = other.get_component(FactionComponent)
            if not other_faction:
                continue

            # Enemy if different faction
            if other_faction.faction != faction.faction:
                targets.append(other)

        return targets

    def _select_target(self, unit: Entity, targets: List[Entity], priority: str) -> Entity:
        """
        Select best target based on priority.

        Args:
            unit: AI unit
            targets: Available targets
            priority: Target priority ("nearest", "weakest", "strongest")

        Returns:
            Selected target or None
        """
        if not targets:
            return None

        pos = unit.get_component(PositionComponent)
        if not pos:
            return targets[0]

        if priority == "weakest":
            # Target unit with lowest troop count
            return min(targets, key=lambda t: self._get_unit_strength(t))

        elif priority == "strongest":
            # Target unit with highest troop count (eliminate threats)
            return max(targets, key=lambda t: self._get_unit_strength(t))

        else:  # "nearest" (default)
            # Target closest enemy
            return min(targets, key=lambda t: self._get_distance(unit, t))

    def _get_unit_strength(self, unit: Entity) -> int:
        """Get unit's current strength (troop count)."""
        unit_comp = unit.get_component(UnitComponent)
        return unit_comp.count if unit_comp else 0

    def _get_distance(self, unit1: Entity, unit2: Entity) -> float:
        """Calculate distance between two units."""
        pos1 = unit1.get_component(PositionComponent)
        pos2 = unit2.get_component(PositionComponent)

        if not pos1 or not pos2 or not self.grid:
            return float('inf')

        return self.grid.distance(pos1.q, pos1.r, pos2.q, pos2.r)

    def _aggressive_behavior(self, unit: Entity, target: Entity, all_units: List[Entity]):
        """
        Aggressive AI: Always attack or advance toward enemy.

        Args:
            unit: AI unit
            target: Selected target
            all_units: All units

        Returns:
            Action tuple
        """
        # Check if target in attack range
        distance = self._get_distance(unit, target)
        combat = unit.get_component(CombatComponent)

        if combat and distance <= combat.range:
            return ("attack", target)

        # Move toward target
        target_pos = target.get_component(PositionComponent)
        if target_pos:
            move_pos = self._find_move_toward(unit, target_pos)
            if move_pos:
                return ("move", move_pos)

        return ("hold", None)

    def _defensive_behavior(self, unit: Entity, target: Entity, all_units: List[Entity]):
        """
        Defensive AI: Only attack when safe, retreat if wounded.

        Args:
            unit: AI unit
            target: Selected target
            all_units: All units

        Returns:
            Action tuple
        """
        # Check unit health
        unit_comp = unit.get_component(UnitComponent)
        health_percent = unit_comp.count / unit_comp.max_count if unit_comp else 1.0

        # If heavily wounded, try to retreat
        if health_percent < 0.5:
            retreat_pos = self._find_retreat_position(unit, all_units)
            if retreat_pos:
                return ("move", retreat_pos)
            return ("hold", None)

        # If healthy and target in range, attack weak enemies
        distance = self._get_distance(unit, target)
        combat = unit.get_component(CombatComponent)

        if combat and distance <= combat.range:
            target_strength = self._get_unit_strength(target)
            # Only attack if target is weak
            if target_strength < 50:
                return ("attack", target)

        # Hold position
        return ("hold", None)

    def _balanced_behavior(self, unit: Entity, target: Entity, all_units: List[Entity]):
        """
        Balanced AI: Attack when opportune, retreat when wounded.

        Args:
            unit: AI unit
            target: Selected target
            all_units: All units

        Returns:
            Action tuple
        """
        # Check unit health
        unit_comp = unit.get_component(UnitComponent)
        health_percent = unit_comp.count / unit_comp.max_count if unit_comp else 1.0

        # Check if target in attack range
        distance = self._get_distance(unit, target)
        combat = unit.get_component(CombatComponent)

        # If in range, attack
        if combat and distance <= combat.range:
            return ("attack", target)

        # If wounded, be cautious
        if health_percent < 0.4:
            # Hold position if low health
            return ("hold", None)

        # If healthy, advance
        if health_percent > 0.6:
            target_pos = target.get_component(PositionComponent)
            if target_pos:
                move_pos = self._find_move_toward(unit, target_pos)
                if move_pos:
                    return ("move", move_pos)

        return ("hold", None)

    def _find_move_toward(self, unit: Entity, target_pos: PositionComponent):
        """
        Find next position to move toward target.

        Args:
            unit: Moving unit
            target_pos: Target position

        Returns:
            Tuple (q, r) or None
        """
        if not self.pathfinder or not self.grid:
            return None

        pos = unit.get_component(PositionComponent)
        movement = unit.get_component(MovementComponent)

        if not pos or not movement or movement.movement_points <= 0:
            return None

        # Find path to target
        path = self.pathfinder.find_path(
            (pos.q, pos.r),
            (target_pos.q, target_pos.r),
            movement.movement_points
        )

        # Return next step in path
        if path and len(path) > 1:
            return path[1]  # First step after current position

        return None

    def _find_retreat_position(self, unit: Entity, all_units: List[Entity]):
        """
        Find safe position to retreat to.

        Args:
            unit: Retreating unit
            all_units: All units

        Returns:
            Tuple (q, r) or None
        """
        pos = unit.get_component(PositionComponent)
        if not pos or not self.grid:
            return None

        # Find enemies
        enemies = self._get_enemy_targets(unit, all_units)
        if not enemies:
            return None

        # Get average enemy position
        enemy_positions = [e.get_component(PositionComponent) for e in enemies]
        enemy_positions = [p for p in enemy_positions if p]

        if not enemy_positions:
            return None

        avg_enemy_q = sum(p.q for p in enemy_positions) / len(enemy_positions)
        avg_enemy_r = sum(p.r for p in enemy_positions) / len(enemy_positions)

        # Move away from average enemy position
        retreat_q = pos.q + (pos.q - int(avg_enemy_q))
        retreat_r = pos.r + (pos.r - int(avg_enemy_r))

        # Clamp to grid bounds
        retreat_q = max(0, min(self.grid.width - 1, retreat_q))
        retreat_r = max(0, min(self.grid.height - 1, retreat_r))

        # Check if position is valid and not occupied
        cell = self.grid.get_cell(retreat_q, retreat_r)
        if cell and not cell.occupied:
            return (retreat_q, retreat_r)

        return None
