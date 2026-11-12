"""
Base widget class for all UI elements.
"""

import pygame
from typing import Tuple, Optional, Callable


class Widget:
    """
    Base class for all UI widgets.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize widget.

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True

        # State
        self.is_hovered = False
        self.is_pressed = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event

        Returns:
            True if event was consumed
        """
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.on_mouse_down(event.pos)
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed:
                self.is_pressed = False
                if self.rect.collidepoint(event.pos):
                    self.on_click(event.pos)
                return True

        return False

    def on_mouse_down(self, pos: Tuple[int, int]) -> None:
        """Called when mouse button is pressed on widget."""
        pass

    def on_click(self, pos: Tuple[int, int]) -> None:
        """Called when widget is clicked."""
        pass

    def update(self, delta_time: float) -> None:
        """Update widget logic."""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render widget to screen."""
        pass

    def set_position(self, x: int, y: int) -> None:
        """Set widget position."""
        self.rect.x = x
        self.rect.y = y

    def set_size(self, width: int, height: int) -> None:
        """Set widget size."""
        self.rect.width = width
        self.rect.height = height
