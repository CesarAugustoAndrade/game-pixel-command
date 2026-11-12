"""
Tooltip System for Classical Army Roguelike

Provides contextual information display for units, terrain, and UI elements.
Features parchment-style backgrounds and dynamic content sizing.
"""

import pygame
import os
from typing import Optional, List, Tuple, Dict, Any
from .bitmap_font import BitmapFontManager

class Tooltip:
    """
    Individual tooltip instance with content and styling.
    """

    def __init__(self, content: List[str], position: Tuple[int, int] = (0, 0)):
        """
        Initialize a tooltip.

        Args:
            content: List of text lines to display
            position: Screen position for the tooltip
        """
        self.content = content
        self.position = position
        self.visible = False
        self.surface = None
        self.background = None

        # Styling
        self.padding = 8
        self.line_spacing = 2
        self.background_color = (238, 223, 204, 240)  # Parchment
        self.border_color = (101, 67, 33)  # Dark brown
        self.text_color = (40, 30, 20)  # Dark brown text

        # Font manager
        self.font_manager = BitmapFontManager()

    def update_content(self, content: List[str]):
        """Update tooltip content."""
        self.content = content
        self.surface = None  # Force regeneration

    def render(self) -> pygame.Surface:
        """Render the tooltip surface."""
        if self.surface and self.content:
            return self.surface

        if not self.content:
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        # Calculate size based on content
        font = self.font_manager.get_font('small')
        max_width = 0
        total_height = 0

        for line in self.content:
            width, height = font.get_text_size(line)
            max_width = max(max_width, width)
            total_height += height + self.line_spacing

        # Add padding
        tooltip_width = max_width + self.padding * 2
        tooltip_height = total_height + self.padding * 2 - self.line_spacing

        # Create surface
        self.surface = pygame.Surface((tooltip_width, tooltip_height + 6), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))

        # Draw background (try to load sprite, fallback to generated)
        background_path = 'assets/sprites/ui/tooltips/tooltip_medium.png'
        if os.path.exists(background_path):
            try:
                bg_image = pygame.image.load(background_path)
                # Scale to fit content
                bg_image = pygame.transform.scale(bg_image, (tooltip_width, tooltip_height + 6))
                self.surface.blit(bg_image, (0, 0))
            except:
                self._draw_parchment_background(self.surface, tooltip_width, tooltip_height)
        else:
            self._draw_parchment_background(self.surface, tooltip_width, tooltip_height)

        # Render text lines
        y_offset = self.padding
        for line in self.content:
            text_surface = font.render_text(line, self.text_color)
            x_pos = (tooltip_width - text_surface.get_width()) // 2  # Center text
            self.surface.blit(text_surface, (x_pos, y_offset))
            y_offset += font.char_height + self.line_spacing

        return self.surface

    def _draw_parchment_background(self, surface: pygame.Surface, width: int, height: int):
        """Draw a parchment-style background."""
        # Main body
        pygame.draw.rect(surface, self.background_color,
                        (1, 1, width - 2, height - 2))
        pygame.draw.rect(surface, self.border_color,
                        (1, 1, width - 2, height - 2), 1)

        # Pointer triangle at bottom
        pointer_x = width // 2
        pygame.draw.polygon(surface, self.background_color,
                          [(pointer_x - 4, height - 1),
                           (pointer_x + 4, height - 1),
                           (pointer_x, height + 5)])
        # Pointer outline
        pygame.draw.lines(surface, self.border_color, False,
                         [(pointer_x - 4, height - 1),
                          (pointer_x, height + 5),
                          (pointer_x + 4, height - 1)], 1)

    def set_position(self, x: int, y: int):
        """Set tooltip position."""
        self.position = (x, y)

    def draw(self, screen: pygame.Surface):
        """Draw the tooltip on screen."""
        if not self.visible or not self.content:
            return

        surface = self.render()
        if surface:
            # Adjust position to keep tooltip on screen
            x, y = self.position
            tooltip_rect = surface.get_rect()

            # Keep within screen bounds
            screen_rect = screen.get_rect()
            if x + tooltip_rect.width > screen_rect.width:
                x = screen_rect.width - tooltip_rect.width - 5
            if y + tooltip_rect.height > screen_rect.height:
                y = self.position[1] - tooltip_rect.height - 10  # Show above cursor

            screen.blit(surface, (x, y))


class TooltipManager:
    """
    Manages all tooltips in the game.
    """

    def __init__(self):
        """Initialize tooltip manager."""
        self.active_tooltip = None
        self.hover_delay = 500  # Milliseconds before showing tooltip
        self.hover_start = 0
        self.hover_target = None
        self.tooltip_cache = {}  # Cache for frequently used tooltips

        # Default tooltip templates
        self.templates = {
            'unit': self._create_unit_tooltip,
            'terrain': self._create_terrain_tooltip,
            'ability': self._create_ability_tooltip,
            'resource': self._create_resource_tooltip,
        }

    def update(self, mouse_pos: Tuple[int, int], hover_target: Optional[Any] = None):
        """
        Update tooltip system.

        Args:
            mouse_pos: Current mouse position
            hover_target: Object being hovered over
        """
        current_time = pygame.time.get_ticks()

        if hover_target != self.hover_target:
            # Changed hover target
            self.hover_target = hover_target
            self.hover_start = current_time
            if self.active_tooltip:
                self.active_tooltip.visible = False

        if hover_target and not self.active_tooltip:
            # Check if enough time has passed
            if current_time - self.hover_start >= self.hover_delay:
                # Create and show tooltip
                self.show_tooltip_for(hover_target, mouse_pos)

        elif self.active_tooltip:
            # Update tooltip position
            self.active_tooltip.set_position(mouse_pos[0] + 10, mouse_pos[1] + 10)

    def show_tooltip_for(self, target: Any, mouse_pos: Tuple[int, int]):
        """
        Show tooltip for a specific target.

        Args:
            target: The object to show tooltip for
            mouse_pos: Mouse position for tooltip placement
        """
        content = self._generate_content_for(target)
        if content:
            if self.active_tooltip:
                self.active_tooltip.update_content(content)
            else:
                self.active_tooltip = Tooltip(content, mouse_pos)
            self.active_tooltip.visible = True
            self.active_tooltip.set_position(mouse_pos[0] + 10, mouse_pos[1] + 10)

    def hide_tooltip(self):
        """Hide the active tooltip."""
        if self.active_tooltip:
            self.active_tooltip.visible = False

    def _generate_content_for(self, target: Any) -> Optional[List[str]]:
        """
        Generate tooltip content based on target type.

        Args:
            target: The object to generate content for

        Returns:
            List of content lines or None
        """
        # Check if target has tooltip info
        if hasattr(target, 'tooltip_info'):
            info = target.tooltip_info
            if isinstance(info, dict):
                if 'type' in info and info['type'] in self.templates:
                    return self.templates[info['type']](info)
                elif 'lines' in info:
                    return info['lines']

        # Check target type directly
        if hasattr(target, '__class__'):
            class_name = target.__class__.__name__
            if class_name == 'Unit':
                return self._create_unit_tooltip({'unit': target})
            elif class_name == 'Tile':
                return self._create_terrain_tooltip({'tile': target})

        return None

    def _create_unit_tooltip(self, info: Dict) -> List[str]:
        """Create tooltip for a unit."""
        lines = []

        if 'unit' in info:
            unit = info['unit']
            # Unit name and type
            lines.append(f"{getattr(unit, 'name', 'Unit')}")
            lines.append(f"Type: {getattr(unit, 'unit_type', 'Infantry')}")
            lines.append("")  # Empty line

            # Stats
            if hasattr(unit, 'count'):
                lines.append(f"Troops: {unit.count}")
            if hasattr(unit, 'morale'):
                lines.append(f"Morale: {unit.morale}%")
            if hasattr(unit, 'attack'):
                lines.append(f"Attack: {unit.attack}")
            if hasattr(unit, 'defense'):
                lines.append(f"Defense: {unit.defense}")
            if hasattr(unit, 'movement'):
                lines.append(f"Move: {unit.movement}")

        return lines

    def _create_terrain_tooltip(self, info: Dict) -> List[str]:
        """Create tooltip for terrain."""
        lines = []

        if 'tile' in info:
            tile = info['tile']
            # Terrain type
            terrain_type = getattr(tile, 'type', 'Unknown')
            lines.append(terrain_type.value.replace('_', ' ').title())

            # Movement cost
            if hasattr(tile, 'movement_cost'):
                lines.append(f"Move Cost: {tile.movement_cost}")

            # Defense bonus
            if hasattr(tile, 'defense_bonus'):
                if tile.defense_bonus != 0:
                    bonus_str = f"+{tile.defense_bonus}" if tile.defense_bonus > 0 else str(tile.defense_bonus)
                    lines.append(f"Defense: {bonus_str}")

            # Special properties
            if hasattr(tile, 'blocks_vision') and tile.blocks_vision:
                lines.append("Blocks Vision")

        elif 'terrain_type' in info:
            lines.append(info['terrain_type'])
            if 'move_cost' in info:
                lines.append(f"Move Cost: {info['move_cost']}")
            if 'defense' in info:
                lines.append(f"Defense: {info['defense']}")

        return lines

    def _create_ability_tooltip(self, info: Dict) -> List[str]:
        """Create tooltip for an ability."""
        lines = []

        lines.append(info.get('name', 'Ability'))
        if 'description' in info:
            # Word wrap description
            desc = info['description']
            words = desc.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) < 20:  # Max line width
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())

        if 'cost' in info:
            lines.append("")
            lines.append(f"Cost: {info['cost']}")
        if 'cooldown' in info:
            lines.append(f"Cooldown: {info['cooldown']} turns")

        return lines

    def _create_resource_tooltip(self, info: Dict) -> List[str]:
        """Create tooltip for a resource."""
        lines = []

        resource_name = info.get('name', 'Resource')
        lines.append(resource_name)

        if 'amount' in info:
            lines.append(f"Amount: {info['amount']}")
        if 'description' in info:
            lines.append(info['description'])

        return lines

    def draw(self, screen: pygame.Surface):
        """Draw active tooltip."""
        if self.active_tooltip:
            self.active_tooltip.draw(screen)


# Global tooltip manager instance
tooltip_manager = TooltipManager()


def show_tooltip(content: List[str], position: Tuple[int, int]):
    """
    Quick function to show a tooltip.

    Args:
        content: List of text lines
        position: Screen position
    """
    global tooltip_manager
    if tooltip_manager.active_tooltip:
        tooltip_manager.active_tooltip.update_content(content)
    else:
        tooltip_manager.active_tooltip = Tooltip(content, position)
    tooltip_manager.active_tooltip.visible = True
    tooltip_manager.active_tooltip.set_position(position[0], position[1])


def hide_tooltip():
    """Quick function to hide tooltip."""
    global tooltip_manager
    tooltip_manager.hide_tooltip()