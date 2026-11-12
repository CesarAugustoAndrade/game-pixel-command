"""
Large-Scale Formation Battle Renderer
Renders 8-12 unit battles with formation blocks and soldier sprites.
"""

import pygame
import math
from typing import List, Optional, Dict, Tuple
from src.entities.unit import Unit
from src.battle.battlefield_grid import BattlefieldGrid, BattlePosition
from src.core.constants import *


class FormationBattleRenderer:
    """
    Renders large-scale formation battles with soldier sprite blocks.

    Features:
    - 8-12 units per side
    - Formation blocks with multiple soldier sprites
    - Commander UI panel
    - Battlefield visualization
    - Spatial positioning
    """

    def __init__(self, screen: pygame.Surface, battlefield: BattlefieldGrid):
        """
        Initialize formation renderer.

        Args:
            screen: Pygame screen surface
            battlefield: Battlefield grid system
        """
        self.screen = screen
        self.battlefield = battlefield

        # Soldier sprite dimensions
        self.soldier_size = 12  # 12x12 pixel soldiers
        self.soldier_spacing = 2  # Pixels between soldiers

        # Formation block settings
        self.max_soldiers_displayed = 25  # Visual cap per unit
        self.formation_tightness = 1.5  # Spacing multiplier (1.0=tight, 2.0=loose)

        # Colors
        self.color_player = (80, 130, 255)  # Blue
        self.color_enemy = (255, 90, 90)  # Red
        self.color_selected = (255, 255, 100)  # Yellow
        self.color_hover = (255, 255, 255)  # White
        self.color_dead = (80, 80, 80)  # Gray
        self.color_battlefield = (70, 90, 60)  # Green plains
        self.color_grid = (90, 110, 80)  # Lighter green

        # Fonts
        self.font_tiny = pygame.font.Font(None, 16)
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 26)
        self.font_large = pygame.font.Font(None, 42)

    def render_frame(
        self,
        player_units: List[Tuple[Unit, BattlePosition]],
        enemy_units: List[Tuple[Unit, BattlePosition]],
        selected_unit: Optional[Unit] = None,
        hover_unit: Optional[Unit] = None,
        turn_info: Optional[Dict] = None,
        commander_data: Optional[Dict] = None
    ):
        """
        Render complete battle frame.

        Args:
            player_units: List of (unit, position) tuples for player
            enemy_units: List of (unit, position) tuples for enemy
            selected_unit: Currently selected unit
            hover_unit: Unit under mouse
            turn_info: Turn/phase information
            commander_data: Commander info for UI panel
        """
        # Clear screen
        self.screen.fill((40, 40, 40))  # Dark background

        # Render battlefield
        self._render_battlefield()

        # Render all units
        self._render_formations(enemy_units, "enemy", selected_unit, hover_unit)
        self._render_formations(player_units, "player", selected_unit, hover_unit)

        # Render VS line
        self._render_vs_line()

        # Render turn indicator
        if turn_info:
            self._render_turn_indicator(turn_info)

        # Render commander panel
        if commander_data:
            self._render_commander_panel(commander_data)

        # Render selected unit info
        if selected_unit:
            self._render_selected_info(selected_unit)

    def _render_battlefield(self):
        """Render the battlefield background and grid."""
        # Battlefield area
        bf_rect = pygame.Rect(
            self.battlefield.screen_offset_x,
            self.battlefield.screen_offset_y,
            self.battlefield.WIDTH,
            self.battlefield.HEIGHT
        )

        # Fill battlefield
        pygame.draw.rect(self.screen, self.color_battlefield, bf_rect)

        # Draw subtle grid lines every 100 pixels
        for x in range(0, self.battlefield.WIDTH, 100):
            screen_x = self.battlefield.screen_offset_x + x
            pygame.draw.line(
                self.screen,
                self.color_grid,
                (screen_x, self.battlefield.screen_offset_y),
                (screen_x, self.battlefield.screen_offset_y + self.battlefield.HEIGHT),
                1
            )

        for y in range(0, self.battlefield.HEIGHT, 100):
            screen_y = self.battlefield.screen_offset_y + y
            pygame.draw.line(
                self.screen,
                self.color_grid,
                (self.battlefield.screen_offset_x, screen_y),
                (self.battlefield.screen_offset_x + self.battlefield.WIDTH, screen_y),
                1
            )

        # Draw zone boundaries (faint lines)
        zone_color = (90, 110, 80, 100)

        # Player deployment zone
        player_zone_x = self.battlefield.screen_offset_x + self.battlefield.PLAYER_DEPLOYMENT_X[1]
        pygame.draw.line(
            self.screen,
            zone_color,
            (player_zone_x, self.battlefield.screen_offset_y),
            (player_zone_x, self.battlefield.screen_offset_y + self.battlefield.HEIGHT),
            2
        )

        # Enemy deployment zone
        enemy_zone_x = self.battlefield.screen_offset_x + self.battlefield.ENEMY_DEPLOYMENT_X[0]
        pygame.draw.line(
            self.screen,
            zone_color,
            (enemy_zone_x, self.battlefield.screen_offset_y),
            (enemy_zone_x, self.battlefield.screen_offset_y + self.battlefield.HEIGHT),
            2
        )

        # Border
        pygame.draw.rect(self.screen, (100, 120, 90), bf_rect, 2)

    def _render_formations(
        self,
        units: List[Tuple[Unit, BattlePosition]],
        side: str,
        selected_unit: Optional[Unit],
        hover_unit: Optional[Unit]
    ):
        """Render all formation blocks for one side."""
        for unit, position in units:
            if not unit.unit_component:
                continue

            self._render_formation_block(unit, position, side, selected_unit, hover_unit)

    def _render_formation_block(
        self,
        unit: Unit,
        position: BattlePosition,
        side: str,
        selected_unit: Optional[Unit],
        hover_unit: Optional[Unit]
    ):
        """
        Render a single unit as a formation block of soldier sprites.

        Args:
            unit: The unit to render
            position: Unit's battlefield position
            side: "player" or "enemy"
            selected_unit: Selected unit
            hover_unit: Hovered unit
        """
        is_selected = (unit == selected_unit)
        is_hover = (unit == hover_unit)
        is_dead = not unit.is_alive()

        # Get screen position
        screen_x, screen_y = position.to_screen(self.battlefield)

        # Determine unit color
        unit_color = self.color_player if side == "player" else self.color_enemy

        if is_dead:
            unit_color = self.color_dead

        # Get formation layout
        soldier_positions = self._get_formation_layout(unit, position)

        # Render each soldier sprite
        for s_x, s_y in soldier_positions:
            self._render_soldier_sprite(s_x, s_y, unit_color, is_selected, is_hover)

        # Render unit label
        self._render_unit_label(unit, screen_x, screen_y - 20, unit_color, is_selected)

        # Render health bar above formation
        if unit.unit_component:
            self._render_unit_health_bar(unit, screen_x, screen_y - 35)

        # Render selection indicator
        if is_selected:
            self._render_selection_indicator(screen_x, screen_y, soldier_positions)

    def _get_formation_layout(
        self,
        unit: Unit,
        position: BattlePosition
    ) -> List[Tuple[int, int]]:
        """
        Calculate soldier sprite positions based on formation type.

        Args:
            unit: The unit
            position: Unit's position

        Returns:
            List of (screen_x, screen_y) positions for each soldier sprite
        """
        if not unit.unit_component or not unit.formation_component:
            return []

        # Get formation type
        formation_type = unit.formation_component.formation_type.lower()

        # Calculate how many soldiers to display
        troop_count = unit.unit_component.count
        max_count = unit.unit_component.max_count
        display_count = min(self.max_soldiers_displayed, max(1, int((troop_count / max_count) * self.max_soldiers_displayed)))

        # Get screen center
        center_x, center_y = position.to_screen(self.battlefield)

        # Generate formation shape
        soldiers = []

        if formation_type == "line":
            # Wide line formation (10 wide × 2-3 deep)
            rows = min(3, (display_count + 9) // 10)
            cols = min(10, display_count)

            for row in range(rows):
                for col in range(cols // rows):
                    x = center_x - (cols * (self.soldier_size + self.soldier_spacing)) // 2 + col * (self.soldier_size + self.soldier_spacing)
                    y = center_y - (rows * (self.soldier_size + self.soldier_spacing)) // 2 + row * (self.soldier_size + self.soldier_spacing)
                    soldiers.append((x, y))
                    if len(soldiers) >= display_count:
                        break
                if len(soldiers) >= display_count:
                    break

        elif formation_type == "phalanx":
            # Tight phalanx (8 wide × 3 deep, tight spacing)
            rows = min(3, (display_count + 7) // 8)
            cols = min(8, display_count)
            tight_spacing = 1  # Very tight

            for row in range(rows):
                for col in range(cols // rows):
                    x = center_x - (cols * (self.soldier_size + tight_spacing)) // 2 + col * (self.soldier_size + tight_spacing)
                    y = center_y - (rows * (self.soldier_size + tight_spacing)) // 2 + row * (self.soldier_size + tight_spacing)
                    soldiers.append((x, y))
                    if len(soldiers) >= display_count:
                        break
                if len(soldiers) >= display_count:
                    break

        elif formation_type == "wedge":
            # Wedge/triangle formation (1,3,5,7,9...)
            row = 0
            soldiers_placed = 0

            while soldiers_placed < display_count:
                row_size = min(1 + row * 2, display_count - soldiers_placed)

                for col in range(row_size):
                    x = center_x - (row_size * (self.soldier_size + self.soldier_spacing)) // 2 + col * (self.soldier_size + self.soldier_spacing)
                    y = center_y - (5 * (self.soldier_size + self.soldier_spacing)) // 2 + row * (self.soldier_size + self.soldier_spacing)
                    soldiers.append((x, y))
                    soldiers_placed += 1
                    if soldiers_placed >= display_count:
                        break

                row += 1

        elif formation_type == "column":
            # Column formation (4 wide × 5+ deep)
            rows = (display_count + 3) // 4
            cols = 4

            for row in range(rows):
                for col in range(min(cols, display_count - row * cols)):
                    x = center_x - (cols * (self.soldier_size + self.soldier_spacing)) // 2 + col * (self.soldier_size + self.soldier_spacing)
                    y = center_y - (rows * (self.soldier_size + self.soldier_spacing)) // 2 + row * (self.soldier_size + self.soldier_spacing)
                    soldiers.append((x, y))
                    if len(soldiers) >= display_count:
                        break
                if len(soldiers) >= display_count:
                    break

        elif formation_type == "skirmish":
            # Loose skirmish formation (scattered)
            rows = min(4, (display_count + 4) // 5)
            cols = min(6, display_count)
            loose_spacing = 6  # Extra spacing

            for row in range(rows):
                for col in range(cols // rows):
                    x = center_x - (cols * (self.soldier_size + loose_spacing)) // 2 + col * (self.soldier_size + loose_spacing)
                    y = center_y - (rows * (self.soldier_size + loose_spacing)) // 2 + row * (self.soldier_size + loose_spacing)
                    soldiers.append((x, y))
                    if len(soldiers) >= display_count:
                        break
                if len(soldiers) >= display_count:
                    break

        else:
            # Default: Square formation
            side_length = int(math.sqrt(display_count)) + 1

            for row in range(side_length):
                for col in range(side_length):
                    if len(soldiers) >= display_count:
                        break
                    x = center_x - (side_length * (self.soldier_size + self.soldier_spacing)) // 2 + col * (self.soldier_size + self.soldier_spacing)
                    y = center_y - (side_length * (self.soldier_size + self.soldier_spacing)) // 2 + row * (self.soldier_size + self.soldier_spacing)
                    soldiers.append((x, y))
                if len(soldiers) >= display_count:
                    break

        return soldiers[:display_count]

    def _render_soldier_sprite(
        self,
        x: int,
        y: int,
        color: Tuple[int, int, int],
        is_selected: bool,
        is_hover: bool
    ):
        """Render a single soldier sprite (small colored square)."""
        # Soldier body
        pygame.draw.rect(self.screen, color, (x, y, self.soldier_size, self.soldier_size))

        # Add outline if selected or hovered
        if is_selected:
            pygame.draw.rect(self.screen, self.color_selected, (x, y, self.soldier_size, self.soldier_size), 1)
        elif is_hover:
            pygame.draw.rect(self.screen, self.color_hover, (x, y, self.soldier_size, self.soldier_size), 1)

    def _render_unit_label(
        self,
        unit: Unit,
        x: int,
        y: int,
        color: Tuple[int, int, int],
        is_selected: bool
    ):
        """Render unit type label above formation."""
        if not unit.unit_component:
            return

        unit_type = unit.unit_component.unit_type.replace('_', ' ').title()

        label_surf = self.font_tiny.render(unit_type, True, color if not is_selected else self.color_selected)
        label_rect = label_surf.get_rect(center=(x, y))

        # Background
        bg_rect = label_rect.inflate(4, 2)
        pygame.draw.rect(self.screen, (20, 20, 20, 180), bg_rect)

        self.screen.blit(label_surf, label_rect)

    def _render_unit_health_bar(self, unit: Unit, x: int, y: int):
        """Render health/troops bar above unit."""
        if not unit.unit_component:
            return

        troop_pct = unit.unit_component.count / unit.unit_component.max_count

        bar_width = 60
        bar_height = 4

        # Background
        pygame.draw.rect(self.screen, (40, 40, 40), (x - bar_width // 2, y, bar_width, bar_height))

        # Fill
        fill_width = int(bar_width * troop_pct)

        if troop_pct > 0.6:
            bar_color = (60, 200, 80)  # Green
        elif troop_pct > 0.3:
            bar_color = (220, 200, 60)  # Yellow
        else:
            bar_color = (220, 60, 60)  # Red

        if fill_width > 0:
            pygame.draw.rect(self.screen, bar_color, (x - bar_width // 2, y, fill_width, bar_height))

        # Border
        pygame.draw.rect(self.screen, (100, 100, 100), (x - bar_width // 2, y, bar_width, bar_height), 1)

    def _render_selection_indicator(
        self,
        x: int,
        y: int,
        soldier_positions: List[Tuple[int, int]]
    ):
        """Render selection circle around formation."""
        if not soldier_positions:
            return

        # Calculate bounding box
        min_x = min(pos[0] for pos in soldier_positions) - 5
        max_x = max(pos[0] for pos in soldier_positions) + self.soldier_size + 5
        min_y = min(pos[1] for pos in soldier_positions) - 5
        max_y = max(pos[1] for pos in soldier_positions) + self.soldier_size + 5

        # Draw selection rectangle
        rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        pygame.draw.rect(self.screen, self.color_selected, rect, 2)

    def _render_vs_line(self):
        """Render VS dividing line in center."""
        center_x = self.battlefield.screen_offset_x + self.battlefield.WIDTH // 2

        # Vertical line
        pygame.draw.line(
            self.screen,
            (255, 255, 100),
            (center_x, self.battlefield.screen_offset_y),
            (center_x, self.battlefield.screen_offset_y + self.battlefield.HEIGHT),
            2
        )

        # VS text
        vs_surf = self.font_large.render("VS", True, (255, 255, 100))
        vs_rect = vs_surf.get_rect(center=(center_x, self.battlefield.screen_offset_y - 30))

        bg_rect = vs_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (30, 30, 30), bg_rect)

        self.screen.blit(vs_surf, vs_rect)

    def _render_turn_indicator(self, turn_info: Dict):
        """Render turn indicator at top."""
        phase = turn_info.get('phase', 'BATTLE')
        turn_num = turn_info.get('turn', 1)

        turn_text = f"{phase} - Turn {turn_num}"
        turn_color = self.color_player if "PLAYER" in phase.upper() else self.color_enemy

        text_surf = self.font_medium.render(turn_text, True, turn_color)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 25))

        # Background
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (20, 20, 20), bg_rect)
        pygame.draw.rect(self.screen, turn_color, bg_rect, 2)

        self.screen.blit(text_surf, text_rect)

    def _render_commander_panel(self, commander_data: Dict):
        """Render commander UI panel (bottom-left)."""
        panel_x = 20
        panel_y = SCREEN_HEIGHT - 140
        panel_width = 200
        panel_height = 120

        # Panel background
        pygame.draw.rect(self.screen, (25, 25, 35), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, self.color_player, (panel_x, panel_y, panel_width, panel_height), 2)

        # Commander name
        commander_name = commander_data.get('name', 'Commander')
        name_surf = self.font_small.render(commander_name, True, (255, 255, 255))
        self.screen.blit(name_surf, (panel_x + 10, panel_y + 10))

        # Abilities (placeholder)
        abilities_text = "Abilities:"
        abilities_surf = self.font_tiny.render(abilities_text, True, (200, 200, 200))
        self.screen.blit(abilities_surf, (panel_x + 10, panel_y + 40))

        # Ability list (placeholder)
        ability_y = panel_y + 60
        for i, ability in enumerate(commander_data.get('abilities', [])[:3]):
            ability_text = f"- {ability.get('name', 'Ability')}"
            ability_surf = self.font_tiny.render(ability_text, True, (180, 180, 180))
            self.screen.blit(ability_surf, (panel_x + 15, ability_y))
            ability_y += 18

    def _render_selected_info(self, unit: Unit):
        """Render detailed info panel for selected unit."""
        panel_x = SCREEN_WIDTH - 220
        panel_y = SCREEN_HEIGHT - 140
        panel_width = 200
        panel_height = 120

        # Panel background
        pygame.draw.rect(self.screen, (30, 30, 30), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, self.color_selected, (panel_x, panel_y, panel_width, panel_height), 2)

        # Unit name
        if unit.unit_component:
            unit_name = unit.unit_component.unit_type.replace('_', ' ').title()
            name_surf = self.font_small.render(unit_name, True, (255, 255, 255))
            self.screen.blit(name_surf, (panel_x + 10, panel_y + 10))

        # Stats
        y_offset = panel_y + 35
        if unit.unit_component:
            troop_text = f"Troops: {unit.unit_component.count}/{unit.unit_component.max_count}"
            troop_surf = self.font_tiny.render(troop_text, True, (200, 200, 200))
            self.screen.blit(troop_surf, (panel_x + 10, y_offset))
            y_offset += 18

        if unit.stats_component:
            stats_text = f"ATK: {unit.stats_component.attack}  DEF: {unit.stats_component.defense}"
            stats_surf = self.font_tiny.render(stats_text, True, (200, 200, 200))
            self.screen.blit(stats_surf, (panel_x + 10, y_offset))
            y_offset += 18

        if unit.morale_component:
            morale_text = f"Morale: {unit.morale_component.current}/100"
            morale_surf = self.font_tiny.render(morale_text, True, (200, 200, 200))
            self.screen.blit(morale_surf, (panel_x + 10, y_offset))
            y_offset += 18

        if unit.formation_component:
            formation_text = f"Formation: {unit.formation_component.formation_type.title()}"
            formation_surf = self.font_tiny.render(formation_text, True, (180, 180, 180))
            self.screen.blit(formation_surf, (panel_x + 10, y_offset))

    def render_victory_banner(self, victor: str):
        """Render victory/defeat banner."""
        banner_text = "VICTORY!" if victor == "player" else "DEFEAT!"
        banner_color = (255, 215, 0) if victor == "player" else (220, 60, 60)

        text_surf = self.font_large.render(banner_text, True, banner_color)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Background
        bg_rect = text_rect.inflate(60, 40)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(self.screen, banner_color, bg_rect, 4)

        self.screen.blit(text_surf, text_rect)

    def get_unit_at_position(
        self,
        mouse_pos: Tuple[int, int],
        all_units: List[Tuple[Unit, BattlePosition]]
    ) -> Optional[Unit]:
        """
        Get which unit (if any) is at mouse position.

        Args:
            mouse_pos: Mouse (x, y)
            all_units: All units with positions

        Returns:
            Unit at position or None
        """
        # Convert to battlefield coordinates
        bf_pos = self.battlefield.screen_to_battlefield(mouse_pos[0], mouse_pos[1])
        if not bf_pos:
            return None

        # Find closest unit within click threshold
        click_threshold = 40  # pixels
        closest_unit = None
        closest_dist = click_threshold

        for unit, position in all_units:
            if not unit.is_alive():
                continue

            distance = bf_pos.distance_to(position)
            if distance < closest_dist:
                closest_dist = distance
                closest_unit = unit

        return closest_unit
