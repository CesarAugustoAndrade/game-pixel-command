"""
Formation Battle State
4v4 battle system with linear formations (2x2 grid per side).
Replaces hex-based battle system with simpler, faster combat.
"""

import pygame
from enum import Enum
from typing import List, Optional, Tuple, Dict
from src.core.state_manager import GameState
from src.core.event_system import EventSystem
from src.core.constants import *
from src.entities.army import Army
from src.entities.unit import Unit
from src.entities.components import PositionComponent
from src.battle.position_grid import FormationGrid, BattleSide
from src.battle.battlefield_grid import BattlefieldGrid, BattlePosition
from src.battle.targeting_system import TargetingSystem
from src.battle.combat_calculator import CombatCalculator
from src.battle.morale_system import MoraleSystem
from src.battle.turn_manager import TurnManager
from src.battle.formation_battle_renderer import FormationBattleRenderer
from src.procgen.loot_tables import calculate_battle_rewards


class BattlePhase(Enum):
    """Battle phases"""
    DEPLOYMENT = "deployment"
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    VICTORY = "victory"
    DEFEAT = "defeat"


class ActionMode(Enum):
    """Player action modes"""
    SELECT = "select"  # Selecting a unit
    ATTACK = "attack"  # Choosing attack target


class BattleStateFormation(GameState):
    """
    Formation-based battle state (4v4).
    Simplified from hex-grid system.
    """

    def __init__(self, state_manager, player_army: Army, enemy_army: Army, difficulty: int = 1):
        """
        Initialize formation battle.

        Args:
            state_manager: Game state manager
            player_army: Player's army
            enemy_army: Enemy army to fight
            difficulty: Battle difficulty level
        """
        super().__init__(state_manager)

        self.player_army = player_army
        self.enemy_army = enemy_army
        self.difficulty = difficulty

        # Battle systems
        self.event_system = EventSystem()
        self.formation_grid = FormationGrid()  # Logical slot-based positioning
        self.battlefield_grid = BattlefieldGrid()  # Visual pixel-based positioning
        self.targeting_system = TargetingSystem()
        self.combat_calculator = CombatCalculator()
        self.morale_system = MoraleSystem(self.event_system)
        self.turn_manager = TurnManager(self.event_system)
        self.renderer = None  # Initialized in on_enter

        # Unit position mapping (unit -> BattlePosition)
        self.unit_positions: Dict[Unit, BattlePosition] = {}

        # Battle state
        self.phase = BattlePhase.DEPLOYMENT
        self.turn_number = 1
        self.current_turn = "player"  # "player" or "enemy"

        # Player interaction
        self.action_mode = ActionMode.SELECT
        self.selected_unit: Optional[Unit] = None
        self.hover_unit: Optional[Unit] = None

        # Battle outcome
        self.victor: Optional[str] = None

    def on_enter(self, **kwargs):
        """Called when entering battle state"""
        # Initialize renderer
        screen = pygame.display.get_surface()
        self.renderer = FormationBattleRenderer(screen, self.battlefield_grid)

        # Deploy armies
        self._deploy_armies()

        # Start player turn
        self.phase = BattlePhase.PLAYER_TURN
        self._start_player_turn()

    def _deploy_armies(self):
        """
        Deploy units to formation grid.
        Player: Left side (4 units)
        Enemy: Right side (4 units)
        """
        # Auto-deploy player units (can be made interactive later)
        player_units = [u for u in self.player_army.units
                       if u.stats_component and u.stats_component.health > 0][:4]

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]  # Front-left, front-right, back-left, back-right

        for i, unit in enumerate(player_units):
            if i >= 4:
                break
            row, col = positions[i]
            self._place_unit(unit, row, col, "player")

        # Auto-deploy enemy units
        enemy_units = [u for u in self.enemy_army.units
                      if u.stats_component and u.stats_component.health > 0][:4]

        for i, unit in enumerate(enemy_units):
            if i >= 4:
                break
            row, col = positions[i]
            self._place_unit(unit, row, col, "enemy")

    def _place_unit(self, unit: Unit, row: int, col: int, side: str):
        """
        Place a unit in formation grid.

        Args:
            unit: Unit to place
            row: 0=front, 1=back
            col: 0=left, 1=right
            side: "player" or "enemy"
        """
        # Update unit's position component
        if unit.position_component:
            unit.position_component.row = row
            unit.position_component.col = col
            unit.position_component.side = side
        else:
            unit.add_component(PositionComponent(row=row, col=col, side=side))

        # Place in logical grid
        self.formation_grid.place_unit(id(unit), row, col, side)

        # Create visual position
        battle_pos = self._grid_to_battlefield_position(row, col, side)
        self.unit_positions[unit] = battle_pos
        self.battlefield_grid.place_unit(id(unit), battle_pos)

    def _grid_to_battlefield_position(self, row: int, col: int, side: str) -> BattlePosition:
        """
        Convert 2x2 grid position to pixel-based battlefield position.

        Args:
            row: 0=front, 1=back
            col: 0=left, 1=right
            side: "player" or "enemy"

        Returns:
            BattlePosition for rendering
        """
        if side == "player":
            # Player deployment zone: x=0-300
            x = 200 if row == 0 else 100  # Front row forward, back row back
            y = 175 if col == 0 else 325  # Left lower, right higher
            facing = 0.0  # Face right (toward enemy)
        else:
            # Enemy deployment zone: x=700-1000
            x = 800 if row == 0 else 900  # Front row forward, back row back
            y = 175 if col == 0 else 325
            facing = 180.0  # Face left (toward player)

        return BattlePosition(x=x, y=y, facing=facing)

    def _remove_unit(self, unit: Unit):
        """Remove unit from grid (when killed)"""
        if not unit.position_component:
            return

        pos = unit.position_component
        self.formation_grid.remove_unit(pos.row, pos.col, pos.side)

        # Remove from battlefield grid
        if unit in self.unit_positions:
            self.battlefield_grid.remove_unit(id(unit))
            del self.unit_positions[unit]

    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        # Handle victory/defeat screen
        if self.phase in [BattlePhase.VICTORY, BattlePhase.DEFEAT]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Return to campaign map
                self.state_manager.pop_state()
            return

        # Only handle player turn input
        if self.phase != BattlePhase.PLAYER_TURN:
            return

        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_left_click(event.pos)
            elif event.button == 3:  # Right click
                self._handle_right_click()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._handle_right_click()  # Cancel action

    def _handle_mouse_motion(self, mouse_pos: Tuple[int, int]):
        """Handle mouse movement (hover effects)"""
        # Get all units with positions
        all_units = [(unit, pos) for unit, pos in self.unit_positions.items()]

        # Check which unit is at mouse position
        self.hover_unit = self.renderer.get_unit_at_position(mouse_pos, all_units)

    def _handle_left_click(self, mouse_pos: Tuple[int, int]):
        """Handle left mouse click"""
        # Get all units with positions
        all_units = [(unit, pos) for unit, pos in self.unit_positions.items()]

        # Check which unit was clicked
        clicked_unit = self.renderer.get_unit_at_position(mouse_pos, all_units)

        if not clicked_unit:
            return

        # Determine which side this unit is on
        unit_side = None
        if clicked_unit in self.player_army.units:
            unit_side = "player"
        elif clicked_unit in self.enemy_army.units:
            unit_side = "enemy"

        if self.action_mode == ActionMode.SELECT:
            # Select player unit
            if unit_side == "player":
                if clicked_unit.stats_component and clicked_unit.stats_component.health > 0:
                    self._select_unit(clicked_unit)

        elif self.action_mode == ActionMode.ATTACK:
            # Attack enemy unit
            if unit_side == "enemy" and self.selected_unit:
                # Check if valid target
                valid_targets = self.targeting_system.get_valid_targets(
                    self.selected_unit,
                    self.enemy_army.units
                )
                if clicked_unit in valid_targets:
                    self._execute_attack(self.selected_unit, clicked_unit)

    def _handle_right_click(self):
        """Handle right click (cancel action)"""
        if self.action_mode == ActionMode.ATTACK:
            # Cancel attack, return to select mode
            self.action_mode = ActionMode.SELECT
        else:
            # Deselect unit
            self.selected_unit = None

    def _select_unit(self, unit: Unit):
        """
        Select a unit for action.

        Args:
            unit: Unit to select
        """
        self.selected_unit = unit
        self.action_mode = ActionMode.ATTACK  # Ready to attack

    def _get_unit_at(self, units: List[Unit], row: int, col: int, side: str) -> Optional[Unit]:
        """Find unit at specific position"""
        for unit in units:
            if (unit.position_component and
                unit.position_component.row == row and
                unit.position_component.col == col and
                unit.position_component.side == side):
                return unit
        return None

    def _execute_attack(self, attacker: Unit, target: Unit):
        """
        Execute an attack.

        Args:
            attacker: Attacking unit
            target: Target unit
        """
        if not attacker.unit_component or not target.unit_component:
            return

        # Convert units to dict format for combat calculator
        attacker_data = {
            "unit_type": attacker.unit_component.unit_type,
            "count": attacker.unit_component.count,
            "max_count": attacker.unit_component.max_count,
        }

        target_data = {
            "unit_type": target.unit_component.unit_type,
            "count": target.unit_component.count,
            "max_count": target.unit_component.max_count,
        }

        # Calculate combat with counter-attack
        result = self.combat_calculator.resolve_combat_with_counter(
            attacker_data,
            target_data,
            attacker_terrain="plains",
            defender_terrain="plains",
            can_counter=True
        )

        # Apply casualties to target
        target_casualties = result['attacker_damage_dealt']
        target.take_casualties(target_casualties)

        # Apply counter-attack casualties to attacker
        attacker_casualties = result['defender_damage_dealt']
        attacker.take_casualties(attacker_casualties)

        # Check if target was eliminated
        if not target.is_alive():
            self._remove_unit(target)

            # Morale boost for attacker (if still alive)
            if attacker.is_alive() and attacker.morale_component:
                attacker.morale_component.current = min(100, attacker.morale_component.current + 10)

        # Check if attacker was eliminated by counter-attack
        if not attacker.is_alive():
            self._remove_unit(attacker)

        # Unit has attacked, deselect
        self.selected_unit = None
        self.action_mode = ActionMode.SELECT

        # Check if any units left
        self._check_victory()

    def _start_player_turn(self):
        """Start player's turn"""
        self.current_turn = "player"
        self.phase = BattlePhase.PLAYER_TURN

        # Reset action state
        self.selected_unit = None
        self.action_mode = ActionMode.SELECT

    def _end_player_turn(self):
        """End player turn, start enemy turn"""
        self.selected_unit = None
        self.action_mode = ActionMode.SELECT

        self.phase = BattlePhase.ENEMY_TURN
        self._execute_enemy_turn()

    def _execute_enemy_turn(self):
        """Execute enemy turn (AI)"""
        self.current_turn = "enemy"

        # Simple AI: Each alive enemy attacks a random valid target
        enemy_units = [u for u in self.enemy_army.units
                      if u.stats_component and u.stats_component.health > 0]

        for enemy_unit in enemy_units:
            # Get valid targets
            valid_targets = self.targeting_system.get_valid_targets(
                enemy_unit,
                self.player_army.units
            )

            if not valid_targets:
                continue

            # Pick target (prioritize weakest)
            target = min(valid_targets, key=lambda u: u.stats_component.health)

            # Execute attack
            self._execute_ai_attack(enemy_unit, target)

        # Check victory after enemy turn
        self._check_victory()

        # Return to player turn
        if self.phase == BattlePhase.ENEMY_TURN:  # If not victory/defeat
            self.turn_number += 1
            self._start_player_turn()

    def _execute_ai_attack(self, attacker: Unit, target: Unit):
        """AI unit attacks player unit"""
        if not attacker.stats_component or not target.stats_component:
            return

        # Calculate combat
        result = self.combat_calculator.calculate_combat(attacker, target)

        # Apply damage
        target.stats_component.health -= result['defender_damage']

        if target.stats_component.health <= 0:
            target.stats_component.health = 0
            self._remove_unit(target)

        # Counter-attack
        if (result.get('defender_survives', False) and
            result.get('attacker_damage', 0) > 0 and
            attacker.stats_component):
            attacker.stats_component.health -= result['attacker_damage']

            if attacker.stats_component.health <= 0:
                attacker.stats_component.health = 0
                self._remove_unit(attacker)

    def _check_victory(self):
        """Check if battle is over"""
        player_alive = any(u.stats_component and u.stats_component.health > 0
                          for u in self.player_army.units)
        enemy_alive = any(u.stats_component and u.stats_component.health > 0
                         for u in self.enemy_army.units)

        if not enemy_alive:
            # Player wins
            self.victor = "player"
            self.phase = BattlePhase.VICTORY
        elif not player_alive:
            # Player loses
            self.victor = "enemy"
            self.phase = BattlePhase.DEFEAT

    def update(self, dt: float):
        """Update battle state"""
        # No real-time updates needed (turn-based)
        pass

    def render(self, screen: pygame.Surface):
        """Render battle"""
        if not self.renderer:
            return

        # Prepare unit lists with positions
        player_units = [(unit, self.unit_positions[unit])
                       for unit in self.player_army.units
                       if unit in self.unit_positions]
        enemy_units = [(unit, self.unit_positions[unit])
                      for unit in self.enemy_army.units
                      if unit in self.unit_positions]

        # Prepare turn info
        turn_info = {
            "phase": self.phase.value.upper().replace('_', ' '),
            "turn": self.turn_number
        }

        # Render battle
        self.renderer.render_frame(player_units, enemy_units, self.selected_unit, self.hover_unit, turn_info)

        # Render victory banner if needed
        if self.phase in [BattlePhase.VICTORY, BattlePhase.DEFEAT]:
            self.renderer.render_victory_banner(self.victor)

            # Show "Press SPACE to continue"
            font = pygame.font.Font(None, 24)
            text = font.render("Press SPACE to continue", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(text, text_rect)

    def on_exit(self):
        """Called when leaving battle state"""
        if self.victor == "player":
            # Apply rewards
            rewards = calculate_battle_rewards(self.enemy_army, self.difficulty)
            self.player_army.gold += rewards.get('gold', 0)

            # Remove dead units
            self.player_army.units = [u for u in self.player_army.units
                                     if u.stats_component and u.stats_component.health > 0]

        # Enemy army is destroyed or player defeated
        pass
