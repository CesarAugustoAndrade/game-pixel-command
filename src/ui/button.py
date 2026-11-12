"""
Button UI widget.
"""

import pygame
from typing import Callable, Optional, Tuple
from src.ui.widgets.widget import Widget
from src.core.constants import *


class Button(Widget):
    """
    Clickable button widget.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        callback: Optional[Callable] = None,
    ):
        """
        Initialize button.

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
            text: Button text
            callback: Function to call when clicked
        """
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback

        # Colors
        self.color_normal = COLOR_UI_SECONDARY
        self.color_hover = COLOR_BUTTON_HOVER
        self.color_pressed = COLOR_UI_PRIMARY
        self.text_color = COLOR_TEXT

    def on_click(self, pos: Tuple[int, int]) -> None:
        """Handle button click."""
        if self.callback:
            self.callback()

    def render(self, screen: pygame.Surface) -> None:
        """Render button with enhanced visuals."""
        # Determine color based on state
        if self.is_pressed:
            color = self.color_pressed
            offset = 2
        elif self.is_hovered:
            color = self.color_hover
            offset = 0
        else:
            color = self.color_normal
            offset = 0

        # Draw shadow for depth
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect)

        # Draw button background
        button_rect = self.rect.copy()
        button_rect.y += offset
        pygame.draw.rect(screen, color, button_rect, border_radius=5)

        # Draw border with different thickness when hovered
        border_width = 3 if self.is_hovered else 2
        pygame.draw.rect(screen, COLOR_UI_PRIMARY, button_rect, border_width, border_radius=5)

        # Draw text
        if self.text:
            font = pygame.font.Font(None, 40)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

            # Add subtle glow effect when hovered
            if self.is_hovered:
                glow_surface = font.render(self.text, True, COLOR_BUTTON_HOVER)
                glow_surface.set_alpha(50)
                glow_rect = glow_surface.get_rect(center=(button_rect.centerx + 1, button_rect.centery + 1))
                screen.blit(glow_surface, glow_rect)
