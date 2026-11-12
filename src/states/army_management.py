"""
Army management state - upgrade and equip units.
"""

import pygame
from src.core.state_manager import GameState
from src.core.constants import *


class ArmyManagementState(GameState):
    """
    Army management state - manage units, equipment, and upgrades.
    """

    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.army = None  # Player's army
        self.selected_unit_index = 0
        self.menu_sections = ["Units", "Equipment", "Upgrades"]
        self.selected_section = 0

    def on_enter(self) -> None:
        """Initialize army management when entering."""
        super().on_enter()
        # TODO: Load player's army
        self._load_test_army()

    def _load_test_army(self) -> None:
        """Load a test army for development."""
        # Placeholder implementation
        self.army = {
            "units": [
                {"name": "Roman Legionary", "count": 50, "morale": 80},
                {"name": "Greek Hoplite", "count": 30, "morale": 75},
                {"name": "Persian Archer", "count": 20, "morale": 70},
            ],
            "equipment": [],
            "resources": {"gold": 500, "food": 100},
        }

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle army management input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: Return to previous state
                pass
            elif event.key == pygame.K_LEFT:
                self.selected_section = (self.selected_section - 1) % len(
                    self.menu_sections
                )
            elif event.key == pygame.K_RIGHT:
                self.selected_section = (self.selected_section + 1) % len(
                    self.menu_sections
                )
            elif event.key == pygame.K_UP:
                if self.army and "units" in self.army:
                    self.selected_unit_index = (self.selected_unit_index - 1) % len(
                        self.army["units"]
                    )
            elif event.key == pygame.K_DOWN:
                if self.army and "units" in self.army:
                    self.selected_unit_index = (self.selected_unit_index + 1) % len(
                        self.army["units"]
                    )

    def update(self, delta_time: float) -> None:
        """Update army management logic."""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render the army management screen."""
        screen.fill((25, 25, 35))

        # Render section tabs
        self._render_tabs(screen)

        # Render current section content
        if self.menu_sections[self.selected_section] == "Units":
            self._render_units_section(screen)
        elif self.menu_sections[self.selected_section] == "Equipment":
            self._render_equipment_section(screen)
        elif self.menu_sections[self.selected_section] == "Upgrades":
            self._render_upgrades_section(screen)

        # Render resources
        self._render_resources(screen)

    def _render_tabs(self, screen: pygame.Surface) -> None:
        """Render section tabs."""
        tab_width = 200
        tab_height = 50
        start_x = 50

        font = pygame.font.Font(None, 36)

        for i, section in enumerate(self.menu_sections):
            x = start_x + i * (tab_width + 10)
            y = 20

            # Draw tab background
            color = COLOR_UI_PRIMARY if i == self.selected_section else COLOR_UI_SECONDARY
            pygame.draw.rect(screen, color, (x, y, tab_width, tab_height))

            # Draw tab text
            text = font.render(section, True, COLOR_TEXT_DARK)
            text_rect = text.get_rect(center=(x + tab_width // 2, y + tab_height // 2))
            screen.blit(text, text_rect)

    def _render_units_section(self, screen: pygame.Surface) -> None:
        """Render the units section."""
        font = pygame.font.Font(None, 32)
        y_offset = 100

        if not self.army or "units" not in self.army:
            text = font.render("No units in army", True, COLOR_TEXT)
            screen.blit(text, (50, y_offset))
            return

        for i, unit in enumerate(self.army["units"]):
            y = y_offset + i * 60

            # Highlight selected unit
            if i == self.selected_unit_index:
                pygame.draw.rect(
                    screen, COLOR_UI_SECONDARY, (40, y - 5, 600, 50), 2
                )

            # Render unit info
            unit_text = f"{unit['name']}: {unit['count']} troops (Morale: {unit['morale']})"
            text = font.render(unit_text, True, COLOR_TEXT)
            screen.blit(text, (50, y))

    def _render_equipment_section(self, screen: pygame.Surface) -> None:
        """Render the equipment section."""
        font = pygame.font.Font(None, 32)
        text = font.render("Equipment (Coming Soon)", True, COLOR_TEXT)
        screen.blit(text, (50, 100))

    def _render_upgrades_section(self, screen: pygame.Surface) -> None:
        """Render the upgrades section."""
        font = pygame.font.Font(None, 32)
        text = font.render("Upgrades (Coming Soon)", True, COLOR_TEXT)
        screen.blit(text, (50, 100))

    def _render_resources(self, screen: pygame.Surface) -> None:
        """Render player resources."""
        if not self.army or "resources" not in self.army:
            return

        font = pygame.font.Font(None, 28)
        resources = self.army["resources"]

        y = screen.get_height() - 50
        text = f"Gold: {resources.get('gold', 0)}  Food: {resources.get('food', 0)}"
        text_surface = font.render(text, True, COLOR_UI_PRIMARY)
        screen.blit(text_surface, (50, y))
