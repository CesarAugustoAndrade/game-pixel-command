"""
Settings state - configure game settings.
"""

import pygame
from src.core.state_manager import GameState
from src.core.constants import *
from src.ui.ui_manager import UIManager
from src.ui.button import Button
from src.ui.panel import Panel


class SettingsState(GameState):
    """
    Settings menu state for configuring game options.
    """

    def __init__(self, state_manager, game_engine):
        super().__init__(state_manager)
        self.engine = game_engine
        self.ui_manager = UIManager()
        self.main_panel = None
        self.buttons = []

        # Store temporary settings
        self.temp_settings = {}

    def on_enter(self) -> None:
        """Initialize settings UI when entering."""
        super().on_enter()
        self._load_current_settings()
        self._create_ui()

    def on_exit(self) -> None:
        """Cleanup when exiting."""
        super().on_exit()
        self.ui_manager.clear_widgets()

    def _load_current_settings(self) -> None:
        """Load current settings from config."""
        config = self.engine.config

        self.temp_settings = {
            'display_width': config.get('display', 'width', 1280),
            'display_height': config.get('display', 'height', 720),
            'fullscreen': config.get('display', 'fullscreen', False),
            'vsync': config.get('display', 'vsync', True),
            'fps': config.get('display', 'fps', 60),
            'master_volume': config.get('audio', 'master_volume', 0.8),
            'music_volume': config.get('audio', 'music_volume', 0.6),
            'sfx_volume': config.get('audio', 'sfx_volume', 0.7),
            'difficulty': config.get('gameplay', 'difficulty', 'normal'),
            'tutorial': config.get('gameplay', 'tutorial_enabled', True),
        }

    def _create_ui(self) -> None:
        """Create settings UI elements."""
        self.ui_manager.clear_widgets()

        screen_width = SCREEN_WIDTH
        screen_height = SCREEN_HEIGHT
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Create main panel
        panel_width = 700
        panel_height = 500
        self.main_panel = Panel(
            center_x - panel_width // 2,
            center_y - panel_height // 2,
            panel_width,
            panel_height,
            background_color=(30, 30, 40, 220),
            border_color=COLOR_UI_PRIMARY
        )

        # Create buttons for different setting sections
        button_width = 200
        button_height = 50
        button_spacing = 60
        start_y = center_y - 150

        # Display Settings Section
        self._create_section_label("DISPLAY", center_x, start_y - 40)

        # Resolution buttons
        res_button = Button(
            center_x - 250,
            start_y,
            button_width,
            button_height,
            text="Resolution",
            callback=self._cycle_resolution
        )
        self.buttons.append(res_button)
        self.ui_manager.add_widget(res_button)

        # Fullscreen toggle
        fullscreen_button = Button(
            center_x + 50,
            start_y,
            button_width,
            button_height,
            text="Fullscreen: " + ("ON" if self.temp_settings['fullscreen'] else "OFF"),
            callback=self._toggle_fullscreen
        )
        self.buttons.append(fullscreen_button)
        self.ui_manager.add_widget(fullscreen_button)

        # Audio Settings Section
        self._create_section_label("AUDIO", center_x, start_y + button_spacing - 20)

        # Master volume
        vol_down = Button(
            center_x - 250,
            start_y + button_spacing,
            80,
            button_height,
            text="-",
            callback=lambda: self._adjust_volume('master', -0.1)
        )
        self.ui_manager.add_widget(vol_down)

        vol_up = Button(
            center_x + 170,
            start_y + button_spacing,
            80,
            button_height,
            text="+",
            callback=lambda: self._adjust_volume('master', 0.1)
        )
        self.ui_manager.add_widget(vol_up)

        # Gameplay Settings Section
        self._create_section_label("GAMEPLAY", center_x, start_y + button_spacing * 2 - 20)

        # Difficulty
        diff_button = Button(
            center_x - 250,
            start_y + button_spacing * 2,
            button_width,
            button_height,
            text=f"Difficulty: {self.temp_settings['difficulty'].capitalize()}",
            callback=self._cycle_difficulty
        )
        self.buttons.append(diff_button)
        self.ui_manager.add_widget(diff_button)

        # Tutorial toggle
        tutorial_button = Button(
            center_x + 50,
            start_y + button_spacing * 2,
            button_width,
            button_height,
            text="Tutorial: " + ("ON" if self.temp_settings['tutorial'] else "OFF"),
            callback=self._toggle_tutorial
        )
        self.buttons.append(tutorial_button)
        self.ui_manager.add_widget(tutorial_button)

        # Action buttons at bottom
        apply_button = Button(
            center_x - 220,
            center_y + 180,
            button_width,
            button_height,
            text="Apply",
            callback=self._apply_settings
        )
        self.ui_manager.add_widget(apply_button)

        cancel_button = Button(
            center_x + 20,
            center_y + 180,
            button_width,
            button_height,
            text="Back",
            callback=self._go_back
        )
        self.ui_manager.add_widget(cancel_button)

    def _create_section_label(self, text: str, x: int, y: int) -> None:
        """Helper to create section labels (rendered directly, not as widgets)."""
        # Store label info for rendering
        if not hasattr(self, 'labels'):
            self.labels = []
        self.labels.append((text, x, y))

    def _cycle_resolution(self) -> None:
        """Cycle through common resolutions."""
        resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]
        current = (self.temp_settings['display_width'], self.temp_settings['display_height'])

        try:
            current_index = resolutions.index(current)
            next_index = (current_index + 1) % len(resolutions)
        except ValueError:
            next_index = 0

        self.temp_settings['display_width'], self.temp_settings['display_height'] = resolutions[next_index]
        self._refresh_ui()

    def _toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        self.temp_settings['fullscreen'] = not self.temp_settings['fullscreen']
        self._refresh_ui()

    def _adjust_volume(self, volume_type: str, delta: float) -> None:
        """Adjust volume level."""
        key = f'{volume_type}_volume'
        if key in self.temp_settings:
            new_value = max(0.0, min(1.0, self.temp_settings[key] + delta))
            self.temp_settings[key] = new_value
            self._refresh_ui()

    def _cycle_difficulty(self) -> None:
        """Cycle through difficulty levels."""
        difficulties = ["easy", "normal", "hard", "veteran"]
        current = self.temp_settings['difficulty']

        try:
            current_index = difficulties.index(current)
            next_index = (current_index + 1) % len(difficulties)
        except ValueError:
            next_index = 1  # default to normal

        self.temp_settings['difficulty'] = difficulties[next_index]
        self._refresh_ui()

    def _toggle_tutorial(self) -> None:
        """Toggle tutorial setting."""
        self.temp_settings['tutorial'] = not self.temp_settings['tutorial']
        self._refresh_ui()

    def _apply_settings(self) -> None:
        """Apply settings and save to config."""
        config = self.engine.config

        # Apply display settings
        config.set('display', 'width', self.temp_settings['display_width'])
        config.set('display', 'height', self.temp_settings['display_height'])
        config.set('display', 'fullscreen', self.temp_settings['fullscreen'])
        config.set('display', 'vsync', self.temp_settings['vsync'])

        # Apply audio settings
        config.set('audio', 'master_volume', self.temp_settings['master_volume'])
        config.set('audio', 'music_volume', self.temp_settings['music_volume'])
        config.set('audio', 'sfx_volume', self.temp_settings['sfx_volume'])

        # Apply gameplay settings
        config.set('gameplay', 'difficulty', self.temp_settings['difficulty'])
        config.set('gameplay', 'tutorial_enabled', self.temp_settings['tutorial'])

        # Save config to file
        config.save_config()

        # Apply display settings to engine (requires restart for some settings)
        # self.engine.apply_display_settings()

        print("Settings applied and saved")
        self._go_back()

    def _refresh_ui(self) -> None:
        """Refresh UI to show updated values."""
        self._create_ui()

    def _go_back(self) -> None:
        """Return to previous state."""
        self.state_manager.pop_state()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle settings input."""
        if self.ui_manager.handle_event(event):
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._go_back()

    def update(self, delta_time: float) -> None:
        """Update settings logic."""
        self.ui_manager.update(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """Render the settings menu."""
        # Clear background (semi-transparent overlay)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Render main panel
        if self.main_panel:
            self.main_panel.render(screen)

        # Render title
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render("SETTINGS", True, COLOR_UI_PRIMARY)
        title_rect = title_text.get_rect(center=(center_x, center_y - 220))
        screen.blit(title_text, title_rect)

        # Render section labels
        if hasattr(self, 'labels'):
            label_font = pygame.font.Font(None, 32)
            for text, x, y in self.labels:
                label_surface = label_font.render(text, True, COLOR_UI_SECONDARY)
                label_rect = label_surface.get_rect(center=(x, y))
                screen.blit(label_surface, label_rect)

        # Render dynamic value labels
        self._render_value_labels(screen)

        # Render UI widgets
        self.ui_manager.render(screen)

    def _render_value_labels(self, screen: pygame.Surface) -> None:
        """Render current setting values."""
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        start_y = center_y - 150

        value_font = pygame.font.Font(None, 28)

        # Resolution value
        res_text = f"{self.temp_settings['display_width']}x{self.temp_settings['display_height']}"
        res_surface = value_font.render(res_text, True, COLOR_TEXT)
        res_rect = res_surface.get_rect(center=(center_x - 150, start_y + 65))
        screen.blit(res_surface, res_rect)

        # Volume value
        vol_text = f"Master: {int(self.temp_settings['master_volume'] * 100)}%"
        vol_surface = value_font.render(vol_text, True, COLOR_TEXT)
        vol_rect = vol_surface.get_rect(center=(center_x, start_y + 125))
        screen.blit(vol_surface, vol_rect)
