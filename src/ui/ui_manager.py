"""
UI Manager - coordinates all UI elements.
"""

import pygame
from typing import List
from src.ui.widgets.widget import Widget


class UIManager:
    """
    Manages all UI elements and handles UI event routing.
    """

    def __init__(self):
        """Initialize UI manager."""
        self.widgets: List[Widget] = []
        self.focused_widget = None

    def add_widget(self, widget: Widget) -> None:
        """
        Add a widget to the UI manager.

        Args:
            widget: Widget to add
        """
        self.widgets.append(widget)

    def remove_widget(self, widget: Widget) -> None:
        """
        Remove a widget from the UI manager.

        Args:
            widget: Widget to remove
        """
        if widget in self.widgets:
            self.widgets.remove(widget)
            if self.focused_widget == widget:
                self.focused_widget = None

    def clear_widgets(self) -> None:
        """Remove all widgets."""
        self.widgets.clear()
        self.focused_widget = None

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event for UI.

        Args:
            event: Pygame event

        Returns:
            True if event was consumed by UI, False otherwise
        """
        # Handle events in reverse order (top widgets first)
        for widget in reversed(self.widgets):
            if not widget.visible or not widget.enabled:
                continue

            if widget.handle_event(event):
                return True

        return False

    def update(self, delta_time: float) -> None:
        """
        Update all widgets.

        Args:
            delta_time: Time since last update
        """
        for widget in self.widgets:
            if widget.visible:
                widget.update(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """
        Render all widgets.

        Args:
            screen: Surface to render to
        """
        for widget in self.widgets:
            if widget.visible:
                widget.render(screen)
