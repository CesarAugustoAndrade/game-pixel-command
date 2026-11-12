"""
Panel UI widget - container for other widgets.
"""

import pygame
from typing import List
from src.ui.widgets.widget import Widget
from src.core.constants import *


class Panel(Widget):
    """
    Panel widget - container for organizing other widgets.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        background_color: tuple = None,
        border_color: tuple = None,
    ):
        """
        Initialize panel.

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
            background_color: Background color (None for transparent)
            border_color: Border color (None for no border)
        """
        super().__init__(x, y, width, height)

        self.background_color = background_color or (40, 40, 50)
        self.border_color = border_color
        self.children: List[Widget] = []

    def add_child(self, widget: Widget) -> None:
        """
        Add a child widget to the panel.

        Args:
            widget: Widget to add
        """
        self.children.append(widget)

    def remove_child(self, widget: Widget) -> None:
        """
        Remove a child widget from the panel.

        Args:
            widget: Widget to remove
        """
        if widget in self.children:
            self.children.remove(widget)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for panel and children."""
        # Let children handle events first
        for child in reversed(self.children):
            if child.visible and child.enabled:
                if child.handle_event(event):
                    return True

        # Panel itself doesn't consume events
        return False

    def update(self, delta_time: float) -> None:
        """Update panel and children."""
        for child in self.children:
            if child.visible:
                child.update(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """Render panel and children."""
        # Draw background
        if self.background_color:
            # Support for alpha transparency
            if len(self.background_color) == 4:
                # Create a surface with alpha support
                panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                panel_surface.fill(self.background_color)
                screen.blit(panel_surface, self.rect.topleft)
            else:
                pygame.draw.rect(screen, self.background_color, self.rect, border_radius=8)

        # Draw border
        if self.border_color:
            pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)

        # Render children
        for child in self.children:
            if child.visible:
                child.render(screen)
