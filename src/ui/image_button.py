"""
Image Button UI widget - button using sprite images.
"""

import pygame
from typing import Callable, Optional, Tuple
from src.ui.widgets.widget import Widget


class ImageButton(Widget):
    """
    Button widget that uses sprite images instead of programmatic rendering.
    """

    def __init__(
        self,
        x: int,
        y: int,
        sprite: pygame.Surface,
        callback: Optional[Callable] = None,
        hover_brightness: float = 1.2,
        pressed_brightness: float = 0.9,
    ):
        """
        Initialize image button.

        Args:
            x: X position
            y: Y position
            sprite: Button sprite image
            callback: Function to call when clicked
            hover_brightness: Brightness multiplier when hovered (default 1.2)
            pressed_brightness: Brightness multiplier when pressed (default 0.9)
        """
        # Initialize with sprite dimensions
        width = sprite.get_width()
        height = sprite.get_height()
        super().__init__(x, y, width, height)

        self.sprite = sprite
        self.callback = callback
        self.hover_brightness = hover_brightness
        self.pressed_brightness = pressed_brightness

        # Create hover and pressed versions
        self._create_state_sprites()

    def _create_state_sprites(self) -> None:
        """Create brightness-adjusted versions for different states."""
        # Normal sprite (original)
        self.normal_sprite = self.sprite.copy()

        # Hover sprite (brightened)
        self.hover_sprite = self._adjust_brightness(self.sprite, self.hover_brightness)

        # Pressed sprite (darkened)
        self.pressed_sprite = self._adjust_brightness(self.sprite, self.pressed_brightness)

    def _adjust_brightness(self, surface: pygame.Surface, factor: float) -> pygame.Surface:
        """
        Adjust brightness of a surface.

        Args:
            surface: Surface to adjust
            factor: Brightness factor (1.0 = no change, >1.0 brighter, <1.0 darker)

        Returns:
            New surface with adjusted brightness
        """
        # Create a copy
        adjusted = surface.copy()

        # Create a white surface for brightening or black for darkening
        if factor > 1.0:
            # Brightening: blend with white
            overlay = pygame.Surface(adjusted.get_size(), pygame.SRCALPHA)
            alpha = int(min(255, (factor - 1.0) * 128))  # Scale alpha based on factor
            overlay.fill((255, 255, 255, alpha))
            adjusted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        elif factor < 1.0:
            # Darkening: multiply by factor
            overlay = pygame.Surface(adjusted.get_size(), pygame.SRCALPHA)
            overlay.fill((int(factor * 255), int(factor * 255), int(factor * 255), 255))
            adjusted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return adjusted

    def on_click(self, pos: Tuple[int, int]) -> None:
        """Handle button click."""
        if self.callback:
            self.callback()

    def render(self, screen: pygame.Surface) -> None:
        """Render the image button."""
        # Select sprite based on state
        if self.is_pressed:
            sprite_to_render = self.pressed_sprite
        elif self.is_hovered:
            sprite_to_render = self.hover_sprite
        else:
            sprite_to_render = self.normal_sprite

        # Draw the sprite
        screen.blit(sprite_to_render, self.rect.topleft)

        # Optional: Draw subtle outline when hovered
        if self.is_hovered and not self.is_pressed:
            pygame.draw.rect(screen, (255, 255, 200, 100), self.rect, 2)
