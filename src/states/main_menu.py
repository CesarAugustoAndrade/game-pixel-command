"""
Main menu state with UI widgets.
"""

import pygame
from src.core.state_manager import GameState
from src.core.constants import *
from src.ui.ui_manager import UIManager
from src.ui.button import Button
from src.ui.panel import Panel


class MainMenuState(GameState):
    """
    Main menu state - first screen shown when game starts.
    """

    def __init__(self, state_manager, game_engine=None):
        super().__init__(state_manager)
        self.engine = game_engine
        self.ui_manager = UIManager()
        self.title_panel = None
        self.buttons = []
        self.background_image = None
        self.background_rect = None

    def on_enter(self) -> None:
        """Initialize menu when entering."""
        super().on_enter()
        self._load_background()
        self._create_ui()

    def _load_background(self) -> None:
        """Load and scale the menu background image using ResourceManager."""
        try:
            # Get screen dimensions from config
            screen_width = self.engine.config.get('display', 'width', SCREEN_WIDTH) if self.engine else SCREEN_WIDTH
            screen_height = self.engine.config.get('display', 'height', SCREEN_HEIGHT) if self.engine else SCREEN_HEIGHT

            # Load the background image using ResourceManager
            if self.engine:
                image_path = self.engine.resource_manager.get_sprite_path("ui", "menu -image.png")
                self.background_image = self.engine.resource_manager.load_sprite(image_path)
            else:
                # Fallback to direct loading if no engine
                image_path = "assets/sprites/ui/menu -image.png"
                self.background_image = pygame.image.load(image_path)

            # Get image dimensions
            img_width, img_height = self.background_image.get_size()
            img_aspect = img_width / img_height
            screen_aspect = screen_width / screen_height

            # Scale to cover the screen
            if img_aspect > screen_aspect:
                # Image is wider than screen
                new_height = screen_height
                new_width = int(new_height * img_aspect)
            else:
                # Image is taller than screen
                new_width = screen_width
                new_height = int(new_width / img_aspect)

            # Scale the image
            self.background_image = pygame.transform.smoothscale(
                self.background_image,
                (new_width, new_height)
            )

            # Center the image
            x = (screen_width - new_width) // 2
            y = (screen_height - new_height) // 2
            self.background_rect = pygame.Rect(x, y, new_width, new_height)

            print(f"Background image loaded successfully via ResourceManager")
        except Exception as e:
            print(f"Warning: Could not load background image: {e}")
            self.background_image = None

    def on_exit(self) -> None:
        """Cleanup when exiting."""
        super().on_exit()
        self.ui_manager.clear_widgets()

    def _create_ui(self) -> None:
        """Create menu UI elements."""
        self.ui_manager.clear_widgets()

        screen_width = SCREEN_WIDTH
        screen_height = SCREEN_HEIGHT
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Create title panel
        panel_width = 600
        panel_height = 120
        self.title_panel = Panel(
            center_x - panel_width // 2,
            center_y - 250,
            panel_width,
            panel_height,
            background_color=(30, 30, 40, 180),
            border_color=COLOR_UI_PRIMARY
        )

        # Create menu buttons
        button_width = 300
        button_height = 60
        button_spacing = 70
        menu_start_y = center_y - 50

        menu_items = [
            ("New Campaign", self._start_new_campaign),
            ("Continue", self._continue_game),
            ("Settings", self._open_settings),
            ("Quit", self._quit_game)
        ]

        self.buttons = []
        for i, (text, callback) in enumerate(menu_items):
            button = Button(
                center_x - button_width // 2,
                menu_start_y + i * button_spacing,
                button_width,
                button_height,
                text=text,
                callback=callback
            )
            self.buttons.append(button)
            self.ui_manager.add_widget(button)

    def _start_new_campaign(self) -> None:
        """Start a new campaign."""
        # Open commander selection screen
        from src.states.commander_selection import CommanderSelectionState
        if self.engine:
            commander_state = CommanderSelectionState(self.state_manager, self.engine)
            self.state_manager.push_state(commander_state)
        else:
            print("Warning: Cannot start commander selection - engine not available")

    def _continue_game(self) -> None:
        """Continue saved game."""
        # TODO: Load saved game
        print("Loading saved game...")

    def _open_settings(self) -> None:
        """Open settings menu."""
        from src.states.settings import SettingsState
        if self.engine:
            settings_state = SettingsState(self.state_manager, self.engine)
            self.state_manager.push_state(settings_state)
        else:
            print("Warning: Cannot open settings - engine not available")

    def _quit_game(self) -> None:
        """Quit the game."""
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle menu input."""
        # Let UI manager handle events first
        if self.ui_manager.handle_event(event):
            return

        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._quit_game()

    def update(self, delta_time: float) -> None:
        """Update menu logic."""
        self.ui_manager.update(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """Render the main menu."""
        # Clear background
        screen.fill(COLOR_BACKGROUND)

        # Draw background image if loaded
        if self.background_image and self.background_rect:
            screen.blit(self.background_image, self.background_rect)
            # Add dark overlay to make UI elements more visible
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(80)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
        else:
            # Fallback: Add subtle background pattern if no image
            self._draw_background_pattern(screen)

        # Get screen center
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        # Render title panel background
        if self.title_panel:
            self.title_panel.render(screen)

        # Render title text with shadow
        title_font = pygame.font.Font(None, 72)

        # Draw shadow
        shadow_text = title_font.render("CLASSICAL ARMY", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(center_x + 3, center_y - 217))
        screen.blit(shadow_text, shadow_rect)

        # Draw title
        title_text = title_font.render("CLASSICAL ARMY", True, COLOR_UI_PRIMARY)
        title_rect = title_text.get_rect(center=(center_x, center_y - 220))
        screen.blit(title_text, title_rect)

        # Render subtitle with shadow
        subtitle_font = pygame.font.Font(None, 36)

        shadow_subtitle = subtitle_font.render("Roguelite", True, (0, 0, 0))
        shadow_sub_rect = shadow_subtitle.get_rect(center=(center_x + 2, center_y - 168))
        screen.blit(shadow_subtitle, shadow_sub_rect)

        subtitle_text = subtitle_font.render("Roguelite", True, COLOR_UI_SECONDARY)
        subtitle_rect = subtitle_text.get_rect(center=(center_x, center_y - 170))
        screen.blit(subtitle_text, subtitle_rect)

        # Render UI widgets (buttons)
        self.ui_manager.render(screen)

        # Render version info
        version_font = pygame.font.Font(None, 24)
        version_text = version_font.render("v0.1.0 Alpha", True, (100, 100, 120))
        version_rect = version_text.get_rect(bottomright=(screen.get_width() - 10, screen.get_height() - 10))
        screen.blit(version_text, version_rect)

    def _draw_background_pattern(self, screen: pygame.Surface) -> None:
        """Draw decorative background pattern."""
        # Draw subtle diagonal lines
        for i in range(0, screen.get_width() + screen.get_height(), 100):
            start_x = i
            start_y = 0
            end_x = 0
            end_y = i
            pygame.draw.line(screen, (30, 30, 40), (start_x, start_y), (end_x, end_y), 1)
