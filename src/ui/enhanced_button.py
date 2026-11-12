"""
Enhanced button widget with sprite support and classical styling.
"""

import pygame
from typing import Callable, Optional
from src.ui.widgets.widget import Widget
from src.core.constants import *


class EnhancedButton(Widget):
    """
    Enhanced button with sprite support for classical UI theme.
    Supports normal, hover, pressed, and disabled states.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        callback: Optional[Callable] = None,
        sprite_normal: Optional[pygame.Surface] = None,
        sprite_hover: Optional[pygame.Surface] = None,
        sprite_pressed: Optional[pygame.Surface] = None,
        icon: Optional[pygame.Surface] = None,
        tooltip_text: str = "",
    ):
        """
        Initialize enhanced button.

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
            text: Button text
            callback: Function to call when clicked
            sprite_normal: Normal state sprite
            sprite_hover: Hover state sprite
            sprite_pressed: Pressed state sprite
            icon: Optional icon to display
            tooltip_text: Tooltip text on hover
        """
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback

        # Sprite assets
        self.sprite_normal = sprite_normal
        self.sprite_hover = sprite_hover
        self.sprite_pressed = sprite_pressed
        self.icon = icon
        self.tooltip_text = tooltip_text

        # Fallback colors if no sprites
        self.color_normal = (139, 69, 19)  # Saddle brown
        self.color_hover = (160, 82, 45)   # Sienna
        self.color_pressed = (101, 67, 33) # Dark brown
        self.text_color = (245, 222, 179)  # Wheat

        # Animation
        self.press_offset = 0
        self.glow_alpha = 0

    def on_click(self, pos: tuple) -> None:
        """Handle button click."""
        if self.callback:
            self.callback()

    def update(self, delta_time: float) -> None:
        """Update button animations."""
        super().update(delta_time)

        # Animate press effect
        if self.is_pressed:
            self.press_offset = 3
        else:
            self.press_offset = 0

        # Animate glow effect on hover
        if self.is_hovered:
            self.glow_alpha = min(100, self.glow_alpha + 300 * delta_time)
        else:
            self.glow_alpha = max(0, self.glow_alpha - 300 * delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """Render enhanced button."""
        # Calculate render rect with press offset
        render_rect = self.rect.copy()
        render_rect.y += self.press_offset

        # Draw shadow for depth
        if not self.is_pressed:
            shadow_rect = self.rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 60))
            screen.blit(shadow_surface, shadow_rect.topleft)

        # Determine which sprite/color to use
        if self.is_pressed and self.sprite_pressed:
            sprite = self.sprite_pressed
        elif self.is_hovered and self.sprite_hover:
            sprite = self.sprite_hover
        elif self.sprite_normal:
            sprite = self.sprite_normal
        else:
            sprite = None

        # Draw button background
        if sprite:
            # Scale sprite to button size
            scaled_sprite = pygame.transform.scale(sprite, (render_rect.width, render_rect.height))
            screen.blit(scaled_sprite, render_rect.topleft)
        else:
            # Fallback to colored rectangle
            color = (
                self.color_pressed if self.is_pressed
                else self.color_hover if self.is_hovered
                else self.color_normal
            )
            pygame.draw.rect(screen, color, render_rect, border_radius=5)

            # Add border
            border_color = (180, 150, 100) if self.is_hovered else (120, 90, 60)
            pygame.draw.rect(screen, border_color, render_rect, 3, border_radius=5)

        # Draw glow effect when hovered
        if self.glow_alpha > 0:
            glow_surface = pygame.Surface((render_rect.width, render_rect.height), pygame.SRCALPHA)
            glow_color = (255, 215, 0, int(self.glow_alpha))
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), 3, border_radius=5)
            screen.blit(glow_surface, render_rect.topleft)

        # Draw icon if provided
        icon_offset = 0
        if self.icon:
            icon_y = render_rect.centery - self.icon.get_height() // 2
            icon_x = render_rect.x + 10
            screen.blit(self.icon, (icon_x, icon_y))
            icon_offset = self.icon.get_width() + 15

        # Draw text
        if self.text:
            font = pygame.font.Font(None, 32)
            text_surface = font.render(self.text, True, self.text_color)

            # Add shadow to text
            shadow_surface = font.render(self.text, True, (20, 15, 10))
            shadow_rect = shadow_surface.get_rect(
                center=(render_rect.centerx + icon_offset // 2 + 2, render_rect.centery + 2)
            )
            screen.blit(shadow_surface, shadow_rect)

            # Draw main text
            text_rect = text_surface.get_rect(
                center=(render_rect.centerx + icon_offset // 2, render_rect.centery)
            )
            screen.blit(text_surface, text_rect)
