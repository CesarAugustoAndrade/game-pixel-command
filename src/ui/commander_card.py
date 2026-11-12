"""
Commander card widget - displays commander portrait and info in a styled card.
"""

import pygame
from typing import Optional
from src.ui.widgets.widget import Widget
from src.data.commander_data import get_commander_data


class CommanderCard(Widget):
    """
    Visual card displaying commander portrait, name, and key stats.
    Classical theme with decorative elements.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        commander_id: str,
        panel_sprite: Optional[pygame.Surface] = None,
        corner_decorations: Optional[list] = None,
    ):
        """
        Initialize commander card.

        Args:
            x: X position
            y: Y position
            width: Width (recommended: 320-400)
            height: Height (recommended: 120-150)
            commander_id: Commander ID to display
            panel_sprite: Background panel sprite
            corner_decorations: List of corner decoration sprites [TL, TR, BL, BR]
        """
        super().__init__(x, y, width, height)
        self.commander_id = commander_id
        self.commander_data = get_commander_data(commander_id)

        self.panel_sprite = panel_sprite
        self.corner_decorations = corner_decorations or []

        # Animation state
        self.glow_alpha = 0
        self.selected = False

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.selected = selected

    def update(self, delta_time: float) -> None:
        """Update card animations."""
        super().update(delta_time)

        # Animate glow when hovered or selected
        if self.is_hovered or self.selected:
            self.glow_alpha = min(120, self.glow_alpha + 400 * delta_time)
        else:
            self.glow_alpha = max(0, self.glow_alpha - 400 * delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """Render commander card."""
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 80))
        screen.blit(shadow_surface, shadow_rect.topleft)

        # Draw background panel
        if self.panel_sprite:
            scaled_panel = pygame.transform.scale(
                self.panel_sprite, (self.rect.width, self.rect.height)
            )
            screen.blit(scaled_panel, self.rect.topleft)
        else:
            # Fallback: stone-like gradient
            panel_surface = pygame.Surface((self.rect.width, self.rect.height))
            panel_surface.fill((90, 75, 60))
            # Add texture noise
            for i in range(100):
                x = pygame.math.Vector2(
                    self.rect.width * (hash(f"{i}x") % 100) / 100,
                    self.rect.height * (hash(f"{i}y") % 100) / 100
                )
                color_var = 10 + (hash(f"{i}c") % 20)
                pygame.draw.circle(panel_surface, (80 + color_var, 65 + color_var, 50 + color_var), x, 1)
            screen.blit(panel_surface, self.rect.topleft)

        # Draw border
        border_color = (120, 90, 60)
        pygame.draw.rect(screen, border_color, self.rect, 3)

        # Draw selection/hover glow
        if self.glow_alpha > 0:
            glow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            glow_color = (255, 215, 0, int(self.glow_alpha)) if self.selected else (200, 170, 120, int(self.glow_alpha))
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), 4)
            screen.blit(glow_surface, self.rect.topleft)

        # Draw corner decorations
        if self.corner_decorations:
            positions = [
                (self.rect.left, self.rect.top),  # Top-left
                (self.rect.right, self.rect.top),  # Top-right (flip H)
                (self.rect.left, self.rect.bottom),  # Bottom-left (flip V)
                (self.rect.right, self.rect.bottom),  # Bottom-right (flip both)
            ]

            for i, corner in enumerate(self.corner_decorations[:4]):
                if corner:
                    decorated = corner.copy()
                    # Flip corners as needed
                    if i == 1:  # Top-right
                        decorated = pygame.transform.flip(decorated, True, False)
                    elif i == 2:  # Bottom-left
                        decorated = pygame.transform.flip(decorated, False, True)
                    elif i == 3:  # Bottom-right
                        decorated = pygame.transform.flip(decorated, True, True)

                    # Adjust position based on corner
                    pos = list(positions[i])
                    if i % 2 == 1:  # Right side
                        pos[0] -= decorated.get_width()
                    if i >= 2:  # Bottom
                        pos[1] -= decorated.get_height()

                    screen.blit(decorated, pos)

        # Draw commander portrait placeholder (left side)
        portrait_size = min(self.rect.height - 20, 80)
        portrait_rect = pygame.Rect(
            self.rect.x + 10,
            self.rect.y + (self.rect.height - portrait_size) // 2,
            portrait_size,
            portrait_size
        )

        # Draw portrait background
        pygame.draw.rect(screen, (60, 50, 40), portrait_rect)
        pygame.draw.rect(screen, (180, 150, 100), portrait_rect, 2)

        # Draw commander icon placeholder (will be replaced with actual portraits)
        icon_font = pygame.font.Font(None, 48)
        icon_text = icon_font.render(self.commander_data.get("name", "?")[0], True, (200, 180, 150))
        icon_rect = icon_text.get_rect(center=portrait_rect.center)
        screen.blit(icon_text, icon_rect)

        # Draw commander info (right side)
        info_x = portrait_rect.right + 15
        info_y = self.rect.y + 10
        info_width = self.rect.width - portrait_size - 35

        # Commander name
        name_font = pygame.font.Font(None, 28)
        name_text = name_font.render(
            self.commander_data.get("name", "Unknown"), True, (255, 215, 0)
        )
        screen.blit(name_text, (info_x, info_y))

        # Commander title
        title_font = pygame.font.Font(None, 18)
        title_text = title_font.render(
            self.commander_data.get("title", ""), True, (200, 200, 200)
        )
        screen.blit(title_text, (info_x, info_y + 25))

        # Key stats (compact display)
        stats = self.commander_data.get("stats", {})
        stat_y = info_y + 50
        stat_font = pygame.font.Font(None, 16)

        # Show top 3 stats
        top_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:3]
        for i, (stat_name, stat_value) in enumerate(top_stats):
            stat_display = f"{stat_name.replace('_', ' ').title()[:8]}: {stat_value}"
            stat_text = stat_font.render(stat_display, True, (180, 180, 180))

            # Draw stat bar
            bar_width = 50
            bar_height = 8
            bar_x = info_x + 90
            bar_y = stat_y + i * 20 + 3

            # Background
            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
            # Fill
            fill_width = int((stat_value / 100) * bar_width)
            bar_color = self._get_stat_color(stat_value)
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
            # Border
            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 1)

            screen.blit(stat_text, (info_x, stat_y + i * 20))

    def _get_stat_color(self, value: int) -> tuple:
        """Get color for stat value."""
        if value >= 90:
            return (255, 215, 0)  # Gold
        elif value >= 70:
            return (100, 200, 100)  # Green
        elif value >= 50:
            return (200, 200, 100)  # Yellow
        else:
            return (200, 100, 100)  # Red
