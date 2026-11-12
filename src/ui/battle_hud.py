"""
Battle HUD System for Classical Army Roguelike

Professional corner-based HUD with stone panels, action buttons,
unit info displays, and resource tracking.
"""

import pygame
import os
from typing import Optional, Dict, List, Tuple, Any
from .bitmap_font import BitmapFontManager
from .tooltip import TooltipManager

class HUDPanel:
    """Base class for HUD panels with stone texture background."""

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize HUD panel.

        Args:
            x, y: Panel position
            width, height: Panel dimensions
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.font_manager = BitmapFontManager()
        self.visible = True

        # Try to load stone panel background
        self.background = None
        self._load_background()

    def _load_background(self):
        """Load stone panel background."""
        panel_path = 'assets/sprites/ui/panels/stone_panel_medium.png'
        if os.path.exists(panel_path):
            try:
                self.background = pygame.image.load(panel_path)
                self.background = pygame.transform.scale(self.background,
                                                        (self.rect.width, self.rect.height))
            except:
                self.background = None

    def draw_background(self):
        """Draw panel background."""
        if self.background:
            self.surface.blit(self.background, (0, 0))
        else:
            # Fallback to simple stone color
            pygame.draw.rect(self.surface, (120, 108, 96), self.surface.get_rect())
            pygame.draw.rect(self.surface, (73, 65, 58), self.surface.get_rect(), 2)

    def draw(self, screen: pygame.Surface):
        """Draw the panel to screen."""
        if self.visible:
            screen.blit(self.surface, self.rect.topleft)


class TurnIndicator(HUDPanel):
    """Turn and resource indicator panel (top-left corner)."""

    def __init__(self):
        """Initialize turn indicator."""
        super().__init__(10, 10, 200, 80)
        self.turn_number = 1
        self.current_phase = "Player Turn"
        self.resources = {
            'gold': 100,
            'supplies': 50,
            'morale': 75,
        }

    def update(self, turn: int, phase: str, resources: Optional[Dict] = None):
        """Update turn information."""
        self.turn_number = turn
        self.current_phase = phase
        if resources:
            self.resources.update(resources)
        self._render()

    def _render(self):
        """Render the turn indicator."""
        self.surface.fill((0, 0, 0, 0))
        self.draw_background()

        # Turn number (use Roman numerals for classical feel)
        font = self.font_manager.get_font('medium')
        turn_text = font.render_number(self.turn_number, (255, 215, 0), use_roman=True)
        turn_label = self.font_manager.get_font('small').render_text("Turn", (200, 200, 200))

        self.surface.blit(turn_label, (10, 10))
        self.surface.blit(turn_text, (50, 8))

        # Phase
        phase_text = self.font_manager.get_font('small').render_text(self.current_phase, (255, 255, 255))
        self.surface.blit(phase_text, (10, 30))

        # Resources
        y = 50
        for resource, amount in self.resources.items():
            # Try to load resource icon
            icon_path = f'assets/sprites/ui/icons/resource_{resource}.png'
            if os.path.exists(icon_path):
                try:
                    icon = pygame.image.load(icon_path)
                    icon = pygame.transform.scale(icon, (16, 16))
                    self.surface.blit(icon, (10, y))
                except:
                    pass

            # Resource amount
            text = self.font_manager.get_font('small').render_text(str(amount), (255, 255, 255))
            self.surface.blit(text, (30, y + 2))
            y += 20


class ActionBar(HUDPanel):
    """Action button bar (bottom-right corner)."""

    def __init__(self):
        """Initialize action bar."""
        super().__init__(520, 440, 260, 60)
        self.buttons = []
        self.selected_action = None
        self._create_buttons()

    def _create_buttons(self):
        """Create action buttons."""
        button_types = ['move', 'sword', 'shield', 'end_turn']
        button_names = ['Move', 'Attack', 'Defend', 'End Turn']

        x = 10
        for btn_type, btn_name in zip(button_types, button_names):
            button_rect = pygame.Rect(x, 10, 40, 40)

            # Load button sprite
            sprite_path = f'assets/sprites/ui/buttons/icon_button_{btn_type}.png'
            sprite = None
            if os.path.exists(sprite_path):
                try:
                    sprite = pygame.image.load(sprite_path)
                    sprite = pygame.transform.scale(sprite, (40, 40))
                except:
                    pass

            self.buttons.append({
                'type': btn_type,
                'name': btn_name,
                'rect': button_rect,
                'sprite': sprite,
                'enabled': True,
                'hover': False,
            })
            x += 50

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle click on action bar.

        Returns:
            Action type if button clicked, None otherwise
        """
        # Convert to local coordinates
        local_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)

        for button in self.buttons:
            if button['rect'].collidepoint(local_pos) and button['enabled']:
                self.selected_action = button['type']
                return button['type']
        return None

    def update_hover(self, mouse_pos: Tuple[int, int]):
        """Update hover state for buttons."""
        local_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

        for button in self.buttons:
            button['hover'] = button['rect'].collidepoint(local_pos)

    def set_enabled(self, action: str, enabled: bool):
        """Enable/disable specific action."""
        for button in self.buttons:
            if button['type'] == action:
                button['enabled'] = enabled
                break

    def render(self):
        """Render the action bar."""
        self.surface.fill((0, 0, 0, 0))
        self.draw_background()

        for button in self.buttons:
            # Draw button
            if button['sprite']:
                # Apply state effects
                sprite = button['sprite'].copy()
                if not button['enabled']:
                    # Darken disabled buttons
                    dark = pygame.Surface(sprite.get_size())
                    dark.set_alpha(128)
                    dark.fill((0, 0, 0))
                    sprite.blit(dark, (0, 0))
                elif button['hover']:
                    # Brighten hovered buttons
                    bright = pygame.Surface(sprite.get_size())
                    bright.set_alpha(64)
                    bright.fill((255, 255, 255))
                    sprite.blit(bright, (0, 0))

                self.surface.blit(sprite, button['rect'].topleft)
            else:
                # Fallback rectangle
                color = (100, 100, 100) if button['enabled'] else (50, 50, 50)
                pygame.draw.rect(self.surface, color, button['rect'])

            # Highlight selected action
            if button['type'] == self.selected_action:
                pygame.draw.rect(self.surface, (255, 215, 0), button['rect'], 2)

    def draw(self, screen: pygame.Surface):
        """Draw action bar."""
        self.render()
        super().draw(screen)


class UnitInfoPanel(HUDPanel):
    """Detailed unit information panel (right side)."""

    def __init__(self):
        """Initialize unit info panel."""
        # Position in top-right corner: x will be set dynamically based on screen width
        super().__init__(1070, 10, 200, 180)  # Moved to top-right, smaller height
        self.selected_unit = None
        self.enemy_unit = None

    def set_unit(self, unit: Any, is_enemy: bool = False):
        """Set the unit to display."""
        if is_enemy:
            self.enemy_unit = unit
        else:
            self.selected_unit = unit
        self._render()

    def _render(self):
        """Render unit information."""
        self.surface.fill((0, 0, 0, 0))

        # Only draw background and content if there's a unit to show
        if not self.selected_unit and not self.enemy_unit:
            return

        self.draw_background()

        y_offset = 10

        # Render selected unit info
        if self.selected_unit:
            self._render_unit_info(self.selected_unit, y_offset, "Selected")
            y_offset = 95

        # Render enemy unit info if in combat preview
        if self.enemy_unit:
            self._render_unit_info(self.enemy_unit, y_offset, "Target")

    def _render_unit_info(self, unit: Any, y_start: int, title: str):
        """Render information for a single unit (ECS-aware)."""
        font_small = self.font_manager.get_font('small')

        # Title
        title_surface = font_small.render_text(title, (255, 215, 0))
        self.surface.blit(title_surface, (10, y_start))
        y = y_start + 15

        # Handle ECS components
        unit_comp = None
        stats_comp = None

        if hasattr(unit, 'get_component'):
            # ECS unit - get components
            from src.entities.components import UnitComponent, StatsComponent
            unit_comp = unit.get_component(UnitComponent)
            stats_comp = unit.get_component(StatsComponent)

        # Unit type
        if unit_comp and hasattr(unit_comp, 'unit_type'):
            type_text = font_small.render_text(unit_comp.unit_type.title(), (255, 255, 255))
            self.surface.blit(type_text, (10, y))
            y += 12
        elif hasattr(unit, 'unit_type'):
            type_text = font_small.render_text(unit.unit_type.title(), (255, 255, 255))
            self.surface.blit(type_text, (10, y))
            y += 12

        # Unit count/health
        if unit_comp and hasattr(unit_comp, 'count'):
            count_text = font_small.render_text(f"Troops: {unit_comp.count}", (200, 200, 200))
            self.surface.blit(count_text, (10, y))
            y += 12
        elif hasattr(unit, 'count'):
            count_text = font_small.render_text(f"Troops: {unit.count}", (200, 200, 200))
            self.surface.blit(count_text, (10, y))
            y += 12

        # Stats
        if stats_comp:
            attack = stats_comp.attack if hasattr(stats_comp, 'attack') else 0
            defense = stats_comp.defense if hasattr(stats_comp, 'defense') else 0

            atk_text = font_small.render_text(f"ATK: {attack}", (200, 200, 200))
            self.surface.blit(atk_text, (10, y))
            y += 12

            def_text = font_small.render_text(f"DEF: {defense}", (200, 200, 200))
            self.surface.blit(def_text, (10, y))
            y += 12

    def _draw_health_bar(self, x: int, y: int, width: int, height: int, fill_percent: float):
        """Draw a health bar."""
        # Try to load health bar sprite
        bar_path = f'assets/sprites/ui/bars/health_bar_medium_{"full" if fill_percent > 0.75 else "50"}.png'
        if os.path.exists(bar_path):
            try:
                bar_sprite = pygame.image.load(bar_path)
                bar_sprite = pygame.transform.scale(bar_sprite, (width, height))
                self.surface.blit(bar_sprite, (x, y))
                return
            except:
                pass

        # Fallback to simple bar
        pygame.draw.rect(self.surface, (40, 20, 20), (x, y, width, height))
        fill_width = int(width * fill_percent)
        if fill_percent > 0.66:
            color = (0, 200, 0)
        elif fill_percent > 0.33:
            color = (200, 200, 0)
        else:
            color = (200, 0, 0)
        pygame.draw.rect(self.surface, color, (x, y, fill_width, height))
        pygame.draw.rect(self.surface, (0, 0, 0), (x, y, width, height), 1)


class BattleHUD:
    """Main battle HUD manager."""

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize battle HUD.

        Args:
            screen_width, screen_height: Screen dimensions
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Create HUD components
        self.turn_indicator = TurnIndicator()
        self.action_bar = ActionBar()
        self.unit_info_panel = UnitInfoPanel()

        # Tooltip manager
        self.tooltip_manager = TooltipManager()

        # Visual feedback
        self.damage_numbers = []
        self.combat_messages = []

    def update(self, mouse_pos: Tuple[int, int], game_state: Dict):
        """
        Update HUD with game state.

        Args:
            mouse_pos: Current mouse position
            game_state: Dictionary containing game state info
        """
        # Update turn indicator
        if 'turn' in game_state:
            self.turn_indicator.update(
                game_state.get('turn', 1),
                game_state.get('phase', 'Player Turn'),
                game_state.get('resources')
            )

        # Update action bar hover
        self.action_bar.update_hover(mouse_pos)

        # Update selected unit
        if 'selected_unit' in game_state:
            self.unit_info_panel.set_unit(game_state['selected_unit'])

        # Update tooltips
        hover_target = game_state.get('hover_target')
        self.tooltip_manager.update(mouse_pos, hover_target)

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle click on HUD elements.

        Returns:
            Action type if action button clicked, None otherwise
        """
        # Check action bar
        action = self.action_bar.handle_click(pos)
        if action:
            return action

        return None

    def add_damage_number(self, damage: int, position: Tuple[int, int],
                         color: Tuple[int, int, int] = (255, 0, 0)):
        """Add floating damage number."""
        self.damage_numbers.append({
            'damage': damage,
            'position': list(position),
            'color': color,
            'timer': 60,  # Frames to display
            'velocity': [0, -2],  # Upward float
        })

    def add_combat_message(self, message: str, duration: int = 120):
        """Add combat message to display."""
        self.combat_messages.append({
            'text': message,
            'timer': duration,
        })

    def update_animations(self):
        """Update animated elements."""
        # Update damage numbers
        for dmg in self.damage_numbers[:]:
            dmg['position'][1] += dmg['velocity'][1]
            dmg['timer'] -= 1
            dmg['velocity'][1] *= 0.95  # Slow down

            if dmg['timer'] <= 0:
                self.damage_numbers.remove(dmg)

        # Update combat messages
        for msg in self.combat_messages[:]:
            msg['timer'] -= 1
            if msg['timer'] <= 0:
                self.combat_messages.remove(msg)

    def draw(self, screen: pygame.Surface):
        """Draw all HUD elements."""
        # Draw panels
        self.turn_indicator.draw(screen)
        self.action_bar.draw(screen)
        self.unit_info_panel.draw(screen)

        # Draw floating damage numbers
        font = BitmapFontManager().get_font('medium')
        for dmg in self.damage_numbers:
            alpha = min(255, dmg['timer'] * 4)
            text = font.render_text(str(dmg['damage']), dmg['color'])
            text.set_alpha(alpha)
            screen.blit(text, dmg['position'])

        # Draw combat messages
        y = 100
        for msg in self.combat_messages:
            alpha = min(255, msg['timer'] * 2)
            text = font.render_text(msg['text'], (255, 255, 255))
            text.set_alpha(alpha)
            x = (self.screen_width - text.get_width()) // 2
            screen.blit(text, (x, y))
            y += 20

        # Draw tooltips (always on top)
        self.tooltip_manager.draw(screen)