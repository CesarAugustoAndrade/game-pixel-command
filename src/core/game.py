"""
Main game class and game loop.
"""

import pygame
from src.core.engine import GameEngine
from src.core.state_manager import StateManager
from src.core.event_system import EventSystem
from src.core.constants import *


class Game:
    """
    Main game class that orchestrates the game loop and systems.
    """

    def __init__(self):
        """Initialize the game."""
        self.engine = GameEngine()  # Config loaded automatically
        self.state_manager = StateManager()
        self.event_system = EventSystem()

        self.is_running = False

    def initialize(self) -> None:
        """
        Initialize game systems and load initial state.
        Override this to set up initial game state.
        """
        # This will be implemented when we create the actual states
        pass

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Handle escape key (pause/back)
                    pass

            # Delegate to state manager
            self.state_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        """
        Update game logic.

        Args:
            delta_time: Time elapsed since last frame (in seconds)
        """
        self.state_manager.update(delta_time)

    def render(self) -> None:
        """Render the current frame."""
        # Clear screen
        self.engine.screen.fill(COLOR_BACKGROUND)

        # Render current state
        self.state_manager.render(self.engine.screen)

        # Debug info
        if self.engine.config.get('debug', 'show_fps', False):
            self._render_fps()

        # Update display
        pygame.display.flip()

    def _render_fps(self) -> None:
        """Render FPS counter."""
        font = self.engine.resource_manager.get_font(16)
        fps = int(self.engine.clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, COLOR_TEXT)
        self.engine.screen.blit(fps_text, (10, 10))

    def run(self) -> None:
        """
        Main game loop.
        """
        self.initialize()
        self.is_running = True

        while self.is_running:
            # Get delta time and limit frame rate (from config)
            fps_target = self.engine.get_fps_target()
            delta_time = self.engine.get_delta_time(fps_target)

            # Main game loop steps
            self.handle_events()
            self.update(delta_time)
            self.render()

        # Cleanup
        self.engine.quit()
