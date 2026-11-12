"""
State management system using a state stack.
"""

from typing import List, Optional
import pygame


class GameState:
    """
    Abstract base class for all game states.
    """

    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.is_active = False

    def on_enter(self) -> None:
        """Called when state becomes active."""
        self.is_active = True

    def on_exit(self) -> None:
        """Called when state becomes inactive."""
        self.is_active = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events."""
        pass

    def update(self, delta_time: float) -> None:
        """Update state logic."""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render state to screen."""
        pass


class StateManager:
    """
    Manages game states using a stack-based approach.
    Supports pushing, popping, and replacing states.
    """

    def __init__(self):
        self._state_stack: List[GameState] = []

    def push_state(self, state: GameState) -> None:
        """
        Push a new state onto the stack.
        The current state (if any) remains in the background.
        """
        if self._state_stack:
            self._state_stack[-1].on_exit()

        self._state_stack.append(state)
        state.on_enter()

    def pop_state(self) -> Optional[GameState]:
        """
        Pop the current state from the stack.
        Returns the popped state or None if stack is empty.
        """
        if not self._state_stack:
            return None

        state = self._state_stack.pop()
        state.on_exit()

        if self._state_stack:
            self._state_stack[-1].on_enter()

        return state

    def change_state(self, state: GameState) -> None:
        """
        Replace the current state with a new state.
        """
        if self._state_stack:
            self.pop_state()
        self.push_state(state)

    def get_current_state(self) -> Optional[GameState]:
        """Get the currently active state."""
        return self._state_stack[-1] if self._state_stack else None

    def clear_states(self) -> None:
        """Clear all states from the stack."""
        while self._state_stack:
            self.pop_state()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Delegate event handling to the current state."""
        if self._state_stack:
            self._state_stack[-1].handle_event(event)

    def update(self, delta_time: float) -> None:
        """Update the current state."""
        if self._state_stack:
            self._state_stack[-1].update(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """Render the current state."""
        if self._state_stack:
            self._state_stack[-1].render(screen)
