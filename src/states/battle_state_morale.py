"""
Morale-Driven Warfare Battle State
Three-phase tactical battle system focused on psychological warfare.

Phases:
1. SKIRMISH: Light units probe enemy, winner gains momentum
2. DECISION: Loser makes critical choice (Retreat/Counter/Selective)
3. ENGAGEMENT: Full battle with commander stats and morale mechanics
"""

import pygame
from enum import Enum
from typing import List, Optional, Dict, Any
from src.core.state_manager import GameState
from src.core.event_system import EventSystem
from src.core.constants import *
from src.core.morale_constants import *
from src.entities.army import Army
from src.entities.unit import Unit
from src.battle.morale_system import MoraleSystem
from src.battle.combat_calculator import CombatCalculator
from src.battle.turn_manager import TurnManager
from src.data.commander_data import get_morale_warfare_stats
import random


class BattlePhase(Enum):
    """Three-phase battle structure"""
    SKIRMISH = "skirmish"
    DECISION = "decision"
    ENGAGEMENT = "engagement"
    VICTORY = "victory"
    DEFEAT = "defeat"


class DecisionChoice(Enum):
    """Player decision after losing skirmish"""
    RETREAT = "retreat"          # Defensive: stabilize morale, defensive position
    COUNTER_COMMIT = "counter"   # Aggressive: risk/reward counter-attack
    SELECTIVE = "selective"       # Tactical: commit elite units


class BattleStateMorale(GameState):
    """
    Morale-driven warfare battle state.

    Flow:
    1. Deploy skirmishers → Skirmish combat
    2. Loser makes decision → Apply consequences
    3. Full engagement → Commander stats, morale mechanics
    4. Victory via morale collapse or elimination
    """

    def __init__(
        self,
        state_manager,
        player_army: Army,
        enemy_army: Army,
        difficulty: int = 1,
        player_commander_id: Optional[str] = None,
        enemy_commander_id: Optional[str] = None
    ):
        """
        Initialize morale-driven battle.

        Args:
            state_manager: Game state manager
            player_army: Player's army
            enemy_army: Enemy army
            difficulty: Battle difficulty (1-10)
            player_commander_id: Player's commander ID
            enemy_commander_id: Enemy commander ID
        """
        super().__init__(state_manager)

        self.player_army = player_army
        self.enemy_army = enemy_army
        self.difficulty = difficulty

        # Commander IDs
        self.player_commander_id = player_commander_id or "alexander"  # Default
        self.enemy_commander_id = enemy_commander_id or "leonidas"

        # Get commander stats
        self.player_commander_stats = get_morale_warfare_stats(self.player_commander_id)
        self.enemy_commander_stats = get_morale_warfare_stats(self.enemy_commander_id)

        # Battle systems
        self.event_system = EventSystem()
        self.morale_system = MoraleSystem(self.event_system)
        self.combat_calculator = CombatCalculator()
        self.turn_manager = TurnManager(self.event_system)

        # Initialize army morale
        self.morale_system.initialize_army_morale(self.player_army)
        self.morale_system.initialize_army_morale(self.enemy_army)

        # Battle state
        self.phase = BattlePhase.SKIRMISH
        self.turn_number = 1
        self.current_turn = "player"  # "player" or "enemy"

        # Skirmish phase data
        self.skirmish_winner: Optional[str] = None  # "player" or "enemy"
        self.skirmish_units_player: List[Unit] = []
        self.skirmish_units_enemy: List[Unit] = []

        # Decision phase data
        self.awaiting_decision_from: Optional[str] = None  # "player" or "enemy"
        self.player_decision: Optional[DecisionChoice] = None
        self.enemy_decision: Optional[DecisionChoice] = None

        # Engagement phase data
        self.engaged_units_player: List[Unit] = []
        self.engaged_units_enemy: List[Unit] = []
        self.momentum_player: int = 0  # -100 to +100
        self.momentum_enemy: int = 0

        # UI state
        self.selected_unit: Optional[Unit] = None
        self.hover_unit: Optional[Unit] = None
        self.decision_buttons: List[Dict] = []

        # Battle outcome
        self.victor: Optional[str] = None
        self.victory_type: Optional[str] = None  # "morale_collapse", "elimination", "rout"

    def on_enter(self, **kwargs):
        """Called when entering battle state"""
        # Start with skirmish phase
        self._start_skirmish_phase()

    # ========================================================================
    # PHASE 1: SKIRMISH
    # ========================================================================

    def _start_skirmish_phase(self):
        """Initialize and start skirmish phase."""
        self.phase = BattlePhase.SKIRMISH

        if DEBUG_PHASE_TRANSITIONS:
            print("\n=== SKIRMISH PHASE START ===")

        # Deploy skirmisher units
        self._deploy_skirmishers()

        # Resolve skirmish combat
        self._resolve_skirmish_combat()

        # Determine winner
        self._determine_skirmish_winner()

        # Apply morale effects
        self._apply_skirmish_morale_effects()

        # Transition to decision phase
        self._transition_to_decision_phase()

    def _deploy_skirmishers(self):
        """Deploy skirmisher units for both sides."""
        # Get light units from each army for skirmishing
        self.skirmish_units_player = self._get_skirmisher_units(
            self.player_army,
            SKIRMISHER_DEPLOYMENT_COUNT
        )

        self.skirmish_units_enemy = self._get_skirmisher_units(
            self.enemy_army,
            SKIRMISHER_DEPLOYMENT_COUNT
        )

    def _get_skirmisher_units(self, army: Army, count: int) -> List[Unit]:
        """
        Get skirmisher units from army.

        Args:
            army: Army to get units from
            count: Number of skirmishers to deploy

        Returns:
            List of light/skirmisher units
        """
        # Prioritize actual skirmisher units
        skirmishers = []

        for unit in army.units:
            if not unit.is_alive():
                continue

            unit_type = unit.unit_component.unit_type.lower()

            # Check for skirmisher/light unit types
            if any(keyword in unit_type for keyword in ["skirmisher", "light", "peltast", "javelin"]):
                skirmishers.append(unit)

            if len(skirmishers) >= count:
                break

        # If not enough skirmishers, use any fast units
        if len(skirmishers) < count:
            for unit in army.units:
                if unit not in skirmishers and unit.is_alive():
                    skirmishers.append(unit)
                    if len(skirmishers) >= count:
                        break

        return skirmishers[:count]

    def _resolve_skirmish_combat(self):
        """Resolve skirmish combat between light units."""
        # Simple combat: compare total strength with commander bonuses
        player_strength = self._calculate_skirmish_strength(
            self.skirmish_units_player,
            self.player_commander_stats
        )

        enemy_strength = self._calculate_skirmish_strength(
            self.skirmish_units_enemy,
            self.enemy_commander_stats
        )

        if DEBUG_MORALE_SYSTEM:
            print(f"Skirmish strength - Player: {player_strength}, Enemy: {enemy_strength}")

        # Apply casualties based on strength difference
        if player_strength > enemy_strength:
            # Player wins skirmish
            damage_to_enemy = int((player_strength - enemy_strength) * 0.3)
            self._apply_skirmish_casualties(self.skirmish_units_enemy, damage_to_enemy)
        else:
            # Enemy wins skirmish
            damage_to_player = int((enemy_strength - player_strength) * 0.3)
            self._apply_skirmish_casualties(self.skirmish_units_player, damage_to_player)

    def _calculate_skirmish_strength(self, units: List[Unit], commander_stats: Dict) -> float:
        """
        Calculate total skirmish strength.

        Args:
            units: Skirmisher units
            commander_stats: Commander morale warfare stats

        Returns:
            Total strength value
        """
        base_strength = 0.0

        for unit in units:
            if not unit.is_alive():
                continue

            # Base strength from troop count
            count = unit.unit_component.count
            base_strength += count * SKIRMISHER_BASE_DAMAGE

        # Apply commander tactics bonus
        tactics_bonus = 1.0 + (commander_stats["tactics"] * COMMANDER_STAT_SCALING_FACTOR * 0.5)

        return base_strength * tactics_bonus * SKIRMISHER_ACCURACY

    def _apply_skirmish_casualties(self, units: List[Unit], damage: int):
        """
        Apply casualties to skirmisher units.

        Args:
            units: Units to damage
            damage: Total damage to distribute
        """
        remaining_damage = damage

        for unit in units:
            if remaining_damage <= 0:
                break

            if not unit.is_alive():
                continue

            casualties = min(remaining_damage, unit.unit_component.count)
            unit.take_casualties(casualties)
            remaining_damage -= casualties

    def _determine_skirmish_winner(self):
        """Determine who won the skirmish."""
        player_alive = sum(1 for u in self.skirmish_units_player if u.is_alive())
        enemy_alive = sum(1 for u in self.skirmish_units_enemy if u.is_alive())

        if player_alive > enemy_alive:
            self.skirmish_winner = "player"
        elif enemy_alive > player_alive:
            self.skirmish_winner = "enemy"
        else:
            # Tie: check casualties
            player_casualties = sum(
                u.unit_component.max_count - u.unit_component.count
                for u in self.skirmish_units_player
            )
            enemy_casualties = sum(
                u.unit_component.max_count - u.unit_component.count
                for u in self.skirmish_units_enemy
            )

            self.skirmish_winner = "player" if player_casualties < enemy_casualties else "enemy"

    def _apply_skirmish_morale_effects(self):
        """Apply morale changes from skirmish outcome."""
        if self.skirmish_winner == "player":
            # Player wins
            self.morale_system.apply_morale_damage_source(
                self.player_army,
                "skirmish_win"
            )
            self.morale_system.apply_morale_damage_source(
                self.enemy_army,
                "skirmish_loss"
            )
            self.awaiting_decision_from = "enemy"

        else:
            # Enemy wins
            self.morale_system.apply_morale_damage_source(
                self.enemy_army,
                "skirmish_win"
            )
            self.morale_system.apply_morale_damage_source(
                self.player_army,
                "skirmish_loss"
            )
            self.awaiting_decision_from = "player"

    def _transition_to_decision_phase(self):
        """Move to decision phase."""
        self.phase = BattlePhase.DECISION

        if DEBUG_PHASE_TRANSITIONS:
            print(f"\n=== DECISION PHASE START ===")
            print(f"Awaiting decision from: {self.awaiting_decision_from}")

        # If player needs to decide, show UI
        # If enemy needs to decide, make AI decision immediately
        if self.awaiting_decision_from == "enemy":
            self._make_enemy_decision()

    # ========================================================================
    # PHASE 2: DECISION POINT
    # ========================================================================

    def _make_player_decision(self, choice: DecisionChoice):
        """
        Process player's decision choice.

        Args:
            choice: Player's decision
        """
        self.player_decision = choice

        if DEBUG_PHASE_TRANSITIONS:
            print(f"Player chose: {choice.value}")

        # Apply decision consequences
        self._apply_decision_consequences("player", choice)

        # Transition to engagement
        self._transition_to_engagement_phase()

    def _make_enemy_decision(self):
        """AI makes decision for enemy."""
        # AI decision logic based on commander personality and morale state
        enemy_morale = self.morale_system.get_army_morale(self.enemy_army)

        # Base weights
        weights = {
            DecisionChoice.RETREAT: AI_RETREAT_WEIGHT_BASE,
            DecisionChoice.COUNTER_COMMIT: AI_COUNTER_COMMIT_WEIGHT_BASE,
            DecisionChoice.SELECTIVE: AI_SELECTIVE_WEIGHT_BASE,
        }

        # Modify weights based on morale
        if enemy_morale < 30:
            # Desperate: more likely to commit
            weights[DecisionChoice.COUNTER_COMMIT] *= AI_DESPERATE_AGGRESSION_BONUS
        elif enemy_morale > 60:
            # Confident: more likely to stabilize
            weights[DecisionChoice.RETREAT] *= AI_CAUTIOUS_RETREAT_BONUS

        # Choose based on weights
        choices = list(weights.keys())
        choice_weights = list(weights.values())
        choice = random.choices(choices, weights=choice_weights)[0]

        self.enemy_decision = choice

        if DEBUG_PHASE_TRANSITIONS:
            print(f"Enemy chose: {choice.value}")

        # Apply decision consequences
        self._apply_decision_consequences("enemy", choice)

        # Transition to engagement
        self._transition_to_engagement_phase()

    def _apply_decision_consequences(self, side: str, choice: DecisionChoice):
        """
        Apply consequences of decision choice.

        Args:
            side: "player" or "enemy"
            choice: Decision made
        """
        army = self.player_army if side == "player" else self.enemy_army

        if choice == DecisionChoice.RETREAT:
            # Defensive: stabilize morale, get defensive bonus
            army.defensive_stance = True
            army.defensive_bonus = DEFENSIVE_POSITION_DAMAGE_REDUCTION

        elif choice == DecisionChoice.COUNTER_COMMIT:
            # Aggressive: deploy units, risk/reward
            army.counter_committing = True
            army.units_committed = COUNTER_COMMIT_UNIT_COUNT

        elif choice == DecisionChoice.SELECTIVE:
            # Tactical: deploy elite units
            army.selective_engagement = True
            army.units_committed = SELECTIVE_UNIT_COUNT

    def _transition_to_engagement_phase(self):
        """Move to main engagement phase."""
        self.phase = BattlePhase.ENGAGEMENT

        if DEBUG_PHASE_TRANSITIONS:
            print("\n=== ENGAGEMENT PHASE START ===")

        # Deploy main armies
        self._deploy_main_forces()

        # Start player turn
        self._start_player_turn()

    # ========================================================================
    # PHASE 3: ENGAGEMENT
    # ========================================================================

    def _deploy_main_forces(self):
        """Deploy main army units for engagement."""
        # All alive units join engagement
        self.engaged_units_player = [u for u in self.player_army.units if u.is_alive()]
        self.engaged_units_enemy = [u for u in self.enemy_army.units if u.is_alive()]

    def _start_player_turn(self):
        """Start player's turn in engagement."""
        self.current_turn = "player"
        self.selected_unit = None

    def _end_player_turn(self):
        """End player turn, start enemy turn."""
        self.selected_unit = None
        self._execute_enemy_turn()

    def _execute_enemy_turn(self):
        """Execute enemy turn (AI)."""
        self.current_turn = "enemy"

        # Each alive enemy unit attacks
        for enemy_unit in self.engaged_units_enemy:
            if not enemy_unit.is_alive():
                continue

            # Find target
            valid_targets = [u for u in self.engaged_units_player if u.is_alive()]
            if not valid_targets:
                break

            # Target weakest
            target = min(valid_targets, key=lambda u: u.unit_component.count)

            # Execute attack with morale mechanics
            self._execute_morale_combat(enemy_unit, target)

        # Apply momentum effects
        self._apply_momentum_effects()

        # Check victory
        if not self._check_victory():
            # Return to player turn
            self.turn_number += 1
            self._start_player_turn()

    def _unit_to_dict(self, unit: Unit) -> Dict[str, Any]:
        """
        Convert Unit object to dictionary format for CombatCalculator.

        Args:
            unit: Unit entity

        Returns:
            Dictionary with unit data
        """
        unit_comp = unit.unit_component
        stats_comp = unit.stats_component

        return {
            "unit_type": unit_comp.unit_type if unit_comp else "infantry",
            "count": unit_comp.count if unit_comp else 0,
            "max_count": unit_comp.max_count if unit_comp else 100,
            "attack": stats_comp.attack if stats_comp else 10,
            "defense": stats_comp.defense if stats_comp else 10,
        }

    def _execute_morale_combat(self, attacker: Unit, defender: Unit):
        """
        Execute combat with morale damage.

        Args:
            attacker: Attacking unit
            defender: Defending unit
        """
        # Convert units to dict format for combat calculator
        attacker_dict = self._unit_to_dict(attacker)
        defender_dict = self._unit_to_dict(defender)

        # Calculate combat
        result = self.combat_calculator.resolve_combat_with_counter(
            attacker_dict,
            defender_dict,
            attacker_terrain="plains",
            defender_terrain="plains",
            can_counter=True
        )

        # Apply morale effectiveness modifier to attacker damage
        # Low morale reduces damage output (creates spiral effect)
        attacker_army = self.player_army if attacker in self.player_army.units else self.enemy_army
        attacker_effectiveness = self.morale_system.get_army_effectiveness_modifier(attacker_army)

        # Apply casualties to defender
        base_defender_damage = result.get("attacker_damage_dealt", 0)
        defender_damage = int(base_defender_damage * attacker_effectiveness)
        defender.take_casualties(defender_damage)

        # Apply morale damage to defender's army
        defender_army = self.player_army if defender in self.player_army.units else self.enemy_army

        # Morale damage from casualties (with Leadership mitigation)
        if defender_damage > 0:
            base_morale_loss = int(defender_damage * 0.1)  # 10% of casualties as morale loss

            # Get correct commander stats based on which army defender belongs to
            if defender in self.player_army.units:
                commander_stats = self.player_commander_stats
            else:
                commander_stats = self.enemy_commander_stats

            # Apply Leadership stat to reduce morale loss
            leadership = commander_stats.get("leadership", 50)
            mitigated_loss = self.morale_system.apply_leadership_mitigation(
                defender_army, base_morale_loss, leadership
            )
            self.morale_system.modify_army_morale(
                defender_army,
                mitigated_loss,
                reason="casualties"
            )

        # If unit eliminated, extra morale damage
        if not defender.is_alive():
            self.morale_system.apply_morale_damage_source(
                defender_army,
                "unit_lost",
                multiplier=1.0
            )

        # Handle counter-attack damage (if defender can counter)
        base_counter_damage = result.get("defender_damage_dealt", 0)
        if base_counter_damage > 0 and defender.is_alive():
            # Apply defender's morale effectiveness to counter-attack damage
            defender_effectiveness = self.morale_system.get_army_effectiveness_modifier(defender_army)
            counter_damage = int(base_counter_damage * defender_effectiveness)

            # Apply counter-attack casualties to attacker
            attacker.take_casualties(counter_damage)

            # Apply morale damage to attacker's army from counter-attack (with Leadership mitigation)
            if counter_damage > 0:
                base_counter_morale_loss = int(counter_damage * 0.1)

                # Get correct commander stats for attacker
                if attacker in self.player_army.units:
                    attacker_commander_stats = self.player_commander_stats
                else:
                    attacker_commander_stats = self.enemy_commander_stats

                # Apply Leadership stat to reduce morale loss
                attacker_leadership = attacker_commander_stats.get("leadership", 50)
                mitigated_counter_loss = self.morale_system.apply_leadership_mitigation(
                    attacker_army, base_counter_morale_loss, attacker_leadership
                )
                self.morale_system.modify_army_morale(
                    attacker_army,
                    mitigated_counter_loss,
                    reason="casualties_counter"
                )

            # Check if attacker eliminated by counter-attack
            if not attacker.is_alive():
                self.morale_system.apply_morale_damage_source(
                    attacker_army,
                    "unit_lost",
                    multiplier=1.0
                )

    def _apply_momentum_effects(self):
        """Apply momentum morale effects each turn."""
        player_morale = self.morale_system.get_army_morale(self.player_army)
        enemy_morale = self.morale_system.get_army_morale(self.enemy_army)

        if player_morale > enemy_morale:
            # Player has momentum
            self.morale_system.apply_momentum_effects(self.player_army, self.enemy_army)
        else:
            # Enemy has momentum
            self.morale_system.apply_momentum_effects(self.enemy_army, self.player_army)

    # ========================================================================
    # VICTORY / DEFEAT
    # ========================================================================

    def _check_victory(self) -> bool:
        """
        Check if battle is over.

        Returns:
            True if battle ended
        """
        # Check morale collapse
        if self.morale_system.is_army_defeated(self.enemy_army):
            self._handle_victory("morale_collapse")
            return True

        if self.morale_system.is_army_defeated(self.player_army):
            self._handle_defeat("morale_collapse")
            return True

        # Check elimination
        player_alive = any(u.is_alive() for u in self.player_army.units)
        enemy_alive = any(u.is_alive() for u in self.enemy_army.units)

        if not enemy_alive:
            self._handle_victory("elimination")
            return True

        if not player_alive:
            self._handle_defeat("elimination")
            return True

        return False

    def _handle_victory(self, victory_type: str):
        """
        Handle player victory.

        Args:
            victory_type: Type of victory
        """
        self.phase = BattlePhase.VICTORY
        self.victor = "player"
        self.victory_type = victory_type

        if DEBUG_PHASE_TRANSITIONS:
            print(f"\n=== VICTORY ({victory_type}) ===")

    def _handle_defeat(self, defeat_type: str):
        """
        Handle player defeat.

        Args:
            defeat_type: Type of defeat
        """
        self.phase = BattlePhase.DEFEAT
        self.victor = "enemy"
        self.victory_type = defeat_type

        if DEBUG_PHASE_TRANSITIONS:
            print(f"\n=== DEFEAT ({defeat_type}) ===")

    # ========================================================================
    # INPUT HANDLING
    # ========================================================================

    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        # Victory/defeat screen
        if self.phase in [BattlePhase.VICTORY, BattlePhase.DEFEAT]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state_manager.pop_state()
            return

        # Decision phase
        if self.phase == BattlePhase.DECISION:
            if self.awaiting_decision_from == "player":
                self._handle_decision_input(event)
            return

        # Engagement phase
        if self.phase == BattlePhase.ENGAGEMENT and self.current_turn == "player":
            self._handle_engagement_input(event)

    def _handle_decision_input(self, event: pygame.event.Event):
        """Handle decision phase input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self._make_player_decision(DecisionChoice.RETREAT)
            elif event.key == pygame.K_2:
                self._make_player_decision(DecisionChoice.COUNTER_COMMIT)
            elif event.key == pygame.K_3:
                self._make_player_decision(DecisionChoice.SELECTIVE)

    def _handle_engagement_input(self, event: pygame.event.Event):
        """Handle engagement phase input."""
        if event.type == pygame.KEYDOWN:
            # End turn with SPACE
            if event.key == pygame.K_SPACE:
                self._end_player_turn()
            # ESC to deselect
            elif event.key == pygame.K_ESCAPE:
                self.selected_unit = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left click to select unit
            if event.button == 1:
                self._handle_unit_click(event.pos)

    def _handle_unit_click(self, pos: tuple):
        """
        Handle unit selection on click.

        Args:
            pos: Mouse position (x, y)
        """
        # TODO: Implement unit click detection
        # For now, just cycle through player units with each click
        if not self.engaged_units_player:
            return

        # Find next alive unit
        if self.selected_unit and self.selected_unit in self.engaged_units_player:
            idx = self.engaged_units_player.index(self.selected_unit)
            idx = (idx + 1) % len(self.engaged_units_player)
            self.selected_unit = self.engaged_units_player[idx]
        else:
            self.selected_unit = self.engaged_units_player[0] if self.engaged_units_player else None

    # ========================================================================
    # UPDATE & RENDER
    # ========================================================================

    def update(self, dt: float):
        """Update battle state."""
        # Mostly turn-based, minimal real-time updates
        pass

    def render(self, screen: pygame.Surface):
        """Render battle."""
        # Clear screen
        screen.fill((30, 30, 40))

        # Render based on phase
        if self.phase == BattlePhase.SKIRMISH:
            self._render_skirmish(screen)
        elif self.phase == BattlePhase.DECISION:
            self._render_decision(screen)
        elif self.phase == BattlePhase.ENGAGEMENT:
            self._render_engagement(screen)
        elif self.phase in [BattlePhase.VICTORY, BattlePhase.DEFEAT]:
            self._render_outcome(screen)

    def _render_skirmish(self, screen: pygame.Surface):
        """Render skirmish phase."""
        font = pygame.font.Font(None, 48)
        text = font.render("SKIRMISH PHASE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    def _render_decision(self, screen: pygame.Surface):
        """Render decision phase."""
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)

        # Title
        title = font_large.render("DECISION POINT", True, (255, 200, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Instructions
        if self.awaiting_decision_from == "player":
            instructions = [
                "You lost the skirmish! Choose your response:",
                "",
                "[1] RETREAT & STABILIZE - Defensive position, stop morale bleed",
                "[2] COUNTER-COMMIT - Risk everything on counter-attack",
                "[3] SELECTIVE ENGAGEMENT - Deploy elite units tactically"
            ]

            y = 200
            for line in instructions:
                text = font_small.render(line, True, (200, 200, 200))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                screen.blit(text, text_rect)
                y += 40

    def _render_engagement(self, screen: pygame.Surface):
        """Render engagement phase."""
        # Render title and turn info
        font_large = pygame.font.Font(None, 36)
        text = font_large.render(f"ENGAGEMENT - Turn {self.turn_number}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(text, text_rect)

        # Render morale bars
        self._render_morale_bars(screen)

        # Render unit lists
        self._render_unit_lists(screen)

        # Render instructions
        font_small = pygame.font.Font(None, 20)
        instructions = "SPACE: End Turn | ESC: Deselect | Click: Cycle Units"
        inst_text = font_small.render(instructions, True, (150, 150, 150))
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(inst_text, inst_rect)

    def _render_unit_lists(self, screen: pygame.Surface):
        """Render unit lists for both armies."""
        font_small = pygame.font.Font(None, 18)

        # Player units (left side)
        player_y = 120
        player_text = font_small.render("PLAYER UNITS:", True, (80, 130, 255))
        screen.blit(player_text, (20, player_y))

        for i, unit in enumerate(self.engaged_units_player):
            if not unit.is_alive():
                continue

            is_selected = unit == self.selected_unit
            color = (255, 255, 100) if is_selected else (200, 200, 200)

            unit_type = unit.unit_component.unit_type.title()
            unit_text = f"  {unit_type}: {unit.unit_component.count}/{unit.unit_component.max_count}"
            text = font_small.render(unit_text, True, color)
            screen.blit(text, (20, player_y + 25 + i * 22))

        # Enemy units (right side)
        enemy_y = 120
        enemy_text = font_small.render("ENEMY UNITS:", True, (255, 90, 90))
        screen.blit(enemy_text, (SCREEN_WIDTH - 200, enemy_y))

        for i, unit in enumerate(self.engaged_units_enemy):
            if not unit.is_alive():
                continue

            unit_type = unit.unit_component.unit_type.title()
            unit_text = f"  {unit_type}: {unit.unit_component.count}/{unit.unit_component.max_count}"
            text = font_small.render(unit_text, True, (200, 100, 100))
            screen.blit(text, (SCREEN_WIDTH - 200, enemy_y + 25 + i * 22))

    def _render_morale_bars(self, screen: pygame.Surface):
        """Render army morale bars."""
        player_morale = self.morale_system.get_army_morale(self.player_army)
        enemy_morale = self.morale_system.get_army_morale(self.enemy_army)

        bar_width = 300
        bar_height = 30

        # Player morale (bottom-left)
        player_x = 50
        player_y = SCREEN_HEIGHT - 100

        pygame.draw.rect(screen, (40, 40, 40), (player_x, player_y, bar_width, bar_height))
        player_fill = int(bar_width * (player_morale / MORALE_MAX))
        pygame.draw.rect(screen, (80, 130, 255), (player_x, player_y, player_fill, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, bar_width, bar_height), 2)

        font = pygame.font.Font(None, 20)
        label = font.render(f"Player Morale: {player_morale}", True, (255, 255, 255))
        screen.blit(label, (player_x, player_y - 25))

        # Enemy morale (bottom-right)
        enemy_x = SCREEN_WIDTH - 350
        enemy_y = SCREEN_HEIGHT - 100

        pygame.draw.rect(screen, (40, 40, 40), (enemy_x, enemy_y, bar_width, bar_height))
        enemy_fill = int(bar_width * (enemy_morale / MORALE_MAX))
        pygame.draw.rect(screen, (255, 90, 90), (enemy_x, enemy_y, enemy_fill, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (enemy_x, enemy_y, bar_width, bar_height), 2)

        label = font.render(f"Enemy Morale: {enemy_morale}", True, (255, 255, 255))
        screen.blit(label, (enemy_x, enemy_y - 25))

    def _render_outcome(self, screen: pygame.Surface):
        """Render victory/defeat screen."""
        font = pygame.font.Font(None, 72)

        if self.phase == BattlePhase.VICTORY:
            text = font.render("VICTORY!", True, (255, 215, 0))
        else:
            text = font.render("DEFEAT", True, (220, 60, 60))

        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

        # Show victory type
        font_small = pygame.font.Font(None, 32)
        subtext = font_small.render(f"({self.victory_type.replace('_', ' ').title()})", True, (200, 200, 200))
        subtext_rect = subtext.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(subtext, subtext_rect)

        # Instructions
        font_tiny = pygame.font.Font(None, 24)
        instructions = font_tiny.render("Press SPACE to continue", True, (150, 150, 150))
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instructions, instructions_rect)

    def on_exit(self):
        """Called when leaving battle state."""
        # Apply battle rewards based on outcome
        if self.victor == "player":
            self._apply_victory_rewards()

        # Clean up dead units
        self.player_army.units = [u for u in self.player_army.units if u.is_alive()]

        # TODO: Update campaign difficulty/balance based on victory type

    def _apply_victory_rewards(self):
        """
        Apply rewards for victory.

        Rewards vary based on victory type:
        - Morale collapse: 1.3x multiplier (strategic victory)
        - Elimination: 1.5x multiplier (total victory)
        """
        from src.procgen.loot_tables import calculate_battle_rewards

        # Convert enemy units to dict format for reward calculation
        enemy_units_dict = []
        for unit in self.enemy_army.units:
            if unit.unit_component:
                enemy_units_dict.append({
                    "unit_type": unit.unit_component.unit_type,
                    "count": unit.unit_component.count,
                })

        # Calculate base rewards
        rewards = calculate_battle_rewards(
            enemy_faction=self.enemy_army.faction,
            enemy_units=enemy_units_dict,
            difficulty=self.difficulty
        )

        # Apply victory type multiplier
        if self.victory_type == "morale_collapse":
            gold_multiplier = 1.3
            xp_multiplier = 1.2
        elif self.victory_type == "elimination":
            gold_multiplier = 1.5
            xp_multiplier = 1.3
        else:  # rout
            gold_multiplier = 1.4
            xp_multiplier = 1.25

        # Apply rewards to army
        self.player_army.gold += int(rewards.get("gold", 0) * gold_multiplier)

        # Add items to player inventory (TODO: implement inventory)
        # battle_items = rewards.get("items", [])

        if DEBUG_PHASE_TRANSITIONS:
            print(f"\n=== VICTORY REWARDS ===")
            print(f"Gold: {int(rewards.get('gold', 0) * gold_multiplier)}")
            print(f"Victory Type: {self.victory_type}")
