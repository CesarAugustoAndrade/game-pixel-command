"""
Commander selection state for choosing a leader before campaign.
Polished UI with classical theme, stone panels, bronze buttons, and decorative elements.
"""

import pygame
from src.core.state_manager import GameState
from src.core.constants import *
from src.ui.ui_manager import UIManager
from src.ui.enhanced_button import EnhancedButton
from src.ui.enhanced_panel import EnhancedPanel
from src.ui.commander_card import CommanderCard
from src.ui.tooltip import Tooltip
from src.data.commander_data import get_commanders_by_faction, get_commander_data
from src.data.faction_data import get_faction_data, FACTION_DATA


class CommanderSelectionState(GameState):
    """
    Commander selection screen - choose faction and commander for campaign.
    """

    def __init__(self, state_manager, game_engine=None):
        super().__init__(state_manager)
        self.engine = game_engine
        self.ui_manager = UIManager()

        # Selection state
        self.selected_faction = "greece"  # Default to Greece (has Alexander)
        self.selected_commander = None
        self.available_commanders = []

        # UI elements
        self.faction_buttons = []
        self.commander_cards = []
        self.confirm_button = None
        self.back_button = None

        # Panels
        self.main_panel = None
        self.title_panel = None
        self.faction_panel = None
        self.commander_panel = None
        self.details_panel = None

        # UI assets
        self.stone_panel_sprite = None
        self.bronze_button_normal = None
        self.bronze_button_hover = None
        self.bronze_button_pressed = None
        self.corner_decorations = []
        self.parchment_sprite = None

        # Tooltip
        self.tooltip = None
        self.tooltip_timer = 0

    def on_enter(self) -> None:
        """Initialize commander selection when entering."""
        super().on_enter()
        self._load_ui_assets()
        self._load_commanders()
        self._create_ui()

    def on_exit(self) -> None:
        """Cleanup when exiting."""
        super().on_exit()
        self.ui_manager.clear_widgets()

    def _load_ui_assets(self) -> None:
        """Load UI sprites and assets for classical theme."""
        try:
            # Load stone panel sprite
            self.stone_panel_sprite = pygame.image.load(
                "assets/sprites/ui/panels/stone_panel_large.png"
            ).convert_alpha()

            # Load bronze button sprites
            self.bronze_button_normal = pygame.image.load(
                "assets/sprites/ui/buttons/bronze_button_large_normal.png"
            ).convert_alpha()
            self.bronze_button_hover = pygame.image.load(
                "assets/sprites/ui/buttons/bronze_button_large_hover.png"
            ).convert_alpha()
            self.bronze_button_pressed = pygame.image.load(
                "assets/sprites/ui/buttons/bronze_button_large_pressed.png"
            ).convert_alpha()

            # Load Greek corner decorations
            corner_sprite = pygame.image.load(
                "assets/sprites/ui/decorative/corner_greek_32.png"
            ).convert_alpha()
            self.corner_decorations = [corner_sprite] * 4

            # Load parchment for details panel
            self.parchment_sprite = pygame.image.load(
                "assets/sprites/ui/panels/parchment_dialog.png"
            ).convert_alpha()

        except Exception as e:
            print(f"Warning: Could not load some UI assets: {e}")
            # Will fall back to programmatic rendering

    def _load_commanders(self) -> None:
        """Load available commanders for selected faction."""
        self.available_commanders = get_commanders_by_faction(self.selected_faction)
        if self.available_commanders:
            self.selected_commander = self.available_commanders[0]
        else:
            self.selected_commander = None

    def _create_ui(self) -> None:
        """Create polished commander selection UI with classical theme."""
        self.ui_manager.clear_widgets()

        screen_width = SCREEN_WIDTH
        screen_height = SCREEN_HEIGHT

        # ===== TITLE BANNER =====
        title_panel_height = 80
        self.title_panel = EnhancedPanel(
            0, 0,
            screen_width, title_panel_height,
            sprite=self.parchment_sprite,
            border_color=(139, 69, 19),
            border_width=3
        )

        # ===== THREE-COLUMN LAYOUT: Factions | Commanders | Details =====

        panel_padding = 20
        panel_spacing = 15
        panel_top = title_panel_height + 20
        panel_bottom_margin = 110

        # Calculate panel dimensions for 3 columns
        total_width = screen_width - (2 * panel_padding)
        available_width = total_width - (2 * panel_spacing)

        # LEFT: Faction Selection Panel (narrower)
        faction_panel_width = 220
        faction_panel_x = panel_padding

        # CENTER: Commander Cards Panel (wider)
        commander_panel_width = 380
        commander_panel_x = faction_panel_x + faction_panel_width + panel_spacing

        # RIGHT: Details Panel (remaining space)
        details_panel_width = total_width - faction_panel_width - commander_panel_width - (2 * panel_spacing)
        details_panel_x = commander_panel_x + commander_panel_width + panel_spacing

        panel_height = screen_height - panel_top - panel_bottom_margin

        # Create Faction Panel with stone texture
        self.faction_panel = EnhancedPanel(
            faction_panel_x, panel_top,
            faction_panel_width, panel_height,
            sprite=self.stone_panel_sprite,
            border_color=(180, 150, 100),
            border_width=3,
            corner_decorations=self.corner_decorations
        )

        # Create faction buttons with bronze styling
        button_width = faction_panel_width - 20
        button_height = 60
        button_spacing = 70
        start_y = panel_top + 50

        self.faction_buttons = []
        for i, (faction_id, faction_data) in enumerate(FACTION_DATA.items()):
            button = EnhancedButton(
                faction_panel_x + 10,
                start_y + i * button_spacing,
                button_width,
                button_height,
                text=faction_data["name"],
                callback=lambda f=faction_id: self._select_faction(f),
                sprite_normal=self.bronze_button_normal,
                sprite_hover=self.bronze_button_hover,
                sprite_pressed=self.bronze_button_pressed,
                tooltip_text=faction_data.get("description", "")
            )

            # Tint button with faction color
            faction_color = faction_data["color"]
            button.color_normal = faction_color
            button.color_hover = tuple(min(c + 30, 255) for c in faction_color)

            self.faction_buttons.append(button)
            self.ui_manager.add_widget(button)

        # Create Commander Panel with stone texture
        self.commander_panel = EnhancedPanel(
            commander_panel_x, panel_top,
            commander_panel_width, panel_height,
            sprite=self.stone_panel_sprite,
            border_color=(180, 150, 100),
            border_width=3,
            corner_decorations=self.corner_decorations
        )

        # Create commander cards (will be populated dynamically)
        self._update_commander_cards()

        # Create Details Panel with parchment texture
        self.details_panel = EnhancedPanel(
            details_panel_x, panel_top,
            details_panel_width, panel_height,
            sprite=self.parchment_sprite,
            border_color=(180, 150, 100),
            border_width=3,
            corner_decorations=self.corner_decorations
        )

        # ===== BOTTOM ACTION BUTTONS =====
        action_button_width = 220
        action_button_height = 60
        button_y = screen_height - 80

        # Back button (left side)
        self.back_button = EnhancedButton(
            40, button_y,
            action_button_width, action_button_height,
            text="BACK TO MENU",
            callback=self._go_back,
            sprite_normal=self.bronze_button_normal,
            sprite_hover=self.bronze_button_hover,
            sprite_pressed=self.bronze_button_pressed
        )
        self.back_button.color_normal = (139, 69, 19)
        self.ui_manager.add_widget(self.back_button)

        # Confirm button (right side)
        self.confirm_button = EnhancedButton(
            screen_width - action_button_width - 40, button_y,
            action_button_width, action_button_height,
            text="START CAMPAIGN",
            callback=self._confirm_selection,
            sprite_normal=self.bronze_button_normal,
            sprite_hover=self.bronze_button_hover,
            sprite_pressed=self.bronze_button_pressed
        )
        self.confirm_button.color_normal = (184, 134, 11)  # Dark goldenrod
        self.confirm_button.color_hover = (218, 165, 32)   # Goldenrod
        self.ui_manager.add_widget(self.confirm_button)

    def _create_title_text(self, text: str, x: int, y: int) -> None:
        """Helper to create title text labels."""
        # This is just for visual reference, actual rendering in render() method
        pass

    def _update_commander_cards(self) -> None:
        """Update commander cards based on selected faction."""
        # Remove old commander cards
        for card in self.commander_cards:
            self.ui_manager.remove_widget(card)
        self.commander_cards.clear()

        # Reload commanders for faction
        self._load_commanders()

        # Create new commander cards
        card_width = self.commander_panel.rect.width - 30
        card_height = 120
        card_spacing = 130
        start_y = self.commander_panel.rect.y + 50

        for i, commander_id in enumerate(self.available_commanders):
            commander_data = get_commander_data(commander_id)

            card = CommanderCard(
                self.commander_panel.rect.x + 15,
                start_y + i * card_spacing,
                card_width,
                card_height,
                commander_id,
                panel_sprite=self.stone_panel_sprite,
                corner_decorations=self.corner_decorations
            )

            # Make card clickable
            original_on_click = card.on_click

            def make_callback(cmd_id):
                def callback(pos):
                    self._select_commander(cmd_id)
                return callback

            card.on_click = make_callback(commander_id)

            self.commander_cards.append(card)
            self.ui_manager.add_widget(card)

    def _select_faction(self, faction_id: str) -> None:
        """Handle faction selection."""
        if self.selected_faction != faction_id:
            self.selected_faction = faction_id
            self._update_commander_cards()
            print(f"Selected faction: {faction_id}")

    def _select_commander(self, commander_id: str) -> None:
        """Handle commander selection."""
        self.selected_commander = commander_id
        print(f"Selected commander: {commander_id}")

    def _confirm_selection(self) -> None:
        """Confirm selection and start campaign."""
        if self.selected_commander:
            commander_data = get_commander_data(self.selected_commander)
            print(f"Starting campaign with {commander_data['name']} of {self.selected_faction}")

            # Store selection in engine for campaign
            if self.engine:
                self.engine.selected_faction = self.selected_faction
                self.engine.selected_commander = self.selected_commander

            # Transition to campaign map (Pokemon Emerald-style overworld)
            from src.states.campaign_map import CampaignMapState
            if self.engine:
                campaign_state = CampaignMapState(self.state_manager, self.engine)
                self.state_manager.change_state(campaign_state)
        else:
            print("Please select a commander first!")

    def _go_back(self) -> None:
        """Go back to main menu."""
        self.state_manager.pop_state()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle commander selection input."""
        # Let UI manager handle events first
        if self.ui_manager.handle_event(event):
            return

        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._go_back()
            elif event.key == pygame.K_RETURN:
                self._confirm_selection()

    def update(self, delta_time: float) -> None:
        """Update commander selection logic."""
        self.ui_manager.update(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """Render the polished commander selection screen."""
        # Clear background with classical atmosphere
        screen.fill((25, 20, 15))

        # Add atmospheric gradient background
        self._draw_enhanced_background(screen)

        # Render title panel
        if self.title_panel:
            self.title_panel.render(screen)
            self._render_title_text(screen)

        # Render main panels
        if self.faction_panel:
            self.faction_panel.render(screen)
        if self.commander_panel:
            self.commander_panel.render(screen)
        if self.details_panel:
            self.details_panel.render(screen)

        # Render panel titles with decorative styling
        self._render_panel_titles(screen)

        # Render UI widgets (buttons and cards)
        self.ui_manager.render(screen)

        # Update commander card selection states
        self._update_card_selection_states()

        # Render commander details
        if self.selected_commander:
            self._render_commander_details(screen)

        # Render tooltip if hovering
        self._render_tooltip(screen)

    def _draw_enhanced_background(self, screen: pygame.Surface) -> None:
        """Draw enhanced atmospheric background with classical feel."""
        width = screen.get_width()
        height = screen.get_height()

        # Rich gradient from warm brown to dark
        for y in range(height):
            progress = y / height
            # Warm brown to deep black gradient
            r = int(40 * (1 - progress))
            g = int(30 * (1 - progress))
            b = int(20 * (1 - progress))
            color = (r, g, b)
            pygame.draw.line(screen, color, (0, y), (width, y))

        # Add subtle vignette effect
        vignette = pygame.Surface((width, height), pygame.SRCALPHA)
        for i in range(100):
            alpha = int(i * 1.5)
            margin = i * 3
            rect = pygame.Rect(margin, margin, width - 2 * margin, height - 2 * margin)
            pygame.draw.rect(vignette, (0, 0, 0, alpha), rect, 1)
        screen.blit(vignette, (0, 0))

    def _render_title_text(self, screen: pygame.Surface) -> None:
        """Render main title text on title banner."""
        title_font = pygame.font.Font(None, 56)
        subtitle_font = pygame.font.Font(None, 24)

        # Main title
        title_text = title_font.render("CHOOSE YOUR COMMANDER", True, (139, 69, 19))
        title_shadow = title_font.render("CHOOSE YOUR COMMANDER", True, (20, 15, 10))

        title_x = (SCREEN_WIDTH - title_text.get_width()) // 2
        title_y = 15

        screen.blit(title_shadow, (title_x + 3, title_y + 3))
        screen.blit(title_text, (title_x, title_y))

    def _render_panel_titles(self, screen: pygame.Surface) -> None:
        """Render decorative titles above panels."""
        title_font = pygame.font.Font(None, 24)

        titles = [
            ("YOUR FACTION", self.faction_panel.rect.x, self.faction_panel.rect.y + 15),
            ("AVAILABLE COMMANDERS", self.commander_panel.rect.x, self.commander_panel.rect.y + 15),
            ("DETAILS & ABILITIES", self.details_panel.rect.x, self.details_panel.rect.y + 15)
        ]

        for text, x, y in titles:
            # Draw text with golden color and shadow
            text_shadow = title_font.render(text, True, (20, 15, 10))
            text_surface = title_font.render(text, True, (255, 215, 0))

            # Center text within panel
            panel_width = (
                self.faction_panel.rect.width if "FACTION" in text
                else self.commander_panel.rect.width if "COMMANDER" in text
                else self.details_panel.rect.width
            )
            text_x = x + (panel_width - text_surface.get_width()) // 2

            screen.blit(text_shadow, (text_x + 2, y + 2))
            screen.blit(text_surface, (text_x, y))

            # Draw decorative line under title
            line_y = y + 25
            line_start_x = x + 10
            line_end_x = x + panel_width - 10
            pygame.draw.line(screen, (180, 150, 100), (line_start_x, line_y), (line_end_x, line_y), 2)

    def _render_commander_details(self, screen: pygame.Surface) -> None:
        """Render detailed information about selected commander."""
        commander_data = get_commander_data(self.selected_commander)
        if not commander_data:
            return

        panel_x = self.details_panel.rect.x + 20
        panel_y = self.details_panel.rect.y + 20
        line_height = 25

        # Font setup
        title_font = pygame.font.Font(None, 36)
        regular_font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 20)

        y_offset = 0

        # Commander name and title
        name_surface = title_font.render(commander_data["name"], True, (255, 215, 0))
        screen.blit(name_surface, (panel_x, panel_y + y_offset))
        y_offset += 40

        title_surface = small_font.render(commander_data["title"], True, (180, 180, 180))
        screen.blit(title_surface, (panel_x, panel_y + y_offset))
        y_offset += 30

        # Era
        era_surface = small_font.render(f"Era: {commander_data['era']}", True, (150, 150, 150))
        screen.blit(era_surface, (panel_x, panel_y + y_offset))
        y_offset += 30

        # Quote
        quote_surface = small_font.render(f'"{commander_data["quote"]}"', True, (200, 200, 150))
        # Word wrap quote if needed
        self._render_wrapped_text(screen, commander_data["quote"], panel_x, panel_y + y_offset,
                                   self.details_panel.rect.width - 40, small_font, (200, 200, 150))
        y_offset += 50

        # Stats
        stats_title = regular_font.render("STATS:", True, COLOR_UI_PRIMARY)
        screen.blit(stats_title, (panel_x, panel_y + y_offset))
        y_offset += 30

        stats = commander_data.get("stats", {})
        stat_names = {
            "leadership": "Leadership",
            "tactics": "Tactics",
            "cavalry_command": "Cavalry Cmd",
            "infantry_command": "Infantry Cmd",
            "siege": "Siege",
            "bravery": "Bravery"
        }

        for stat_id, stat_name in stat_names.items():
            if stat_id in stats:
                value = stats[stat_id]
                stat_text = f"{stat_name}: {value}"
                stat_surface = small_font.render(stat_text, True, (200, 200, 200))
                screen.blit(stat_surface, (panel_x, panel_y + y_offset))

                # Draw stat bar
                bar_x = panel_x + 150
                bar_y = panel_y + y_offset + 5
                bar_width = 150
                bar_height = 12

                # Background bar
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                # Filled bar
                fill_width = int((value / 100) * bar_width)
                bar_color = self._get_stat_color(value)
                pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
                # Border
                pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 1)

                y_offset += 22

        y_offset += 10

        # Bonuses
        bonuses_title = regular_font.render("BONUSES:", True, COLOR_UI_PRIMARY)
        screen.blit(bonuses_title, (panel_x, panel_y + y_offset))
        y_offset += 30

        bonuses = commander_data.get("bonuses", {})
        bonus_count = 0
        for bonus_id, value in bonuses.items():
            if bonus_count >= 4:  # Limit display
                more_text = small_font.render("... and more", True, (150, 150, 150))
                screen.blit(more_text, (panel_x, panel_y + y_offset))
                break

            bonus_display = self._format_bonus(bonus_id, value)
            bonus_surface = small_font.render(f"+ {bonus_display}", True, (100, 200, 100))
            screen.blit(bonus_surface, (panel_x, panel_y + y_offset))
            y_offset += 22
            bonus_count += 1

    def _render_wrapped_text(self, screen: pygame.Surface, text: str, x: int, y: int,
                            max_width: int, font: pygame.font.Font, color: tuple) -> None:
        """Render text with word wrapping."""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            screen.blit(line_surface, (x, y + i * 20))

    def _get_stat_color(self, value: int) -> tuple:
        """Get color for stat bar based on value."""
        if value >= 90:
            return (255, 215, 0)  # Gold
        elif value >= 70:
            return (100, 200, 100)  # Green
        elif value >= 50:
            return (200, 200, 100)  # Yellow
        else:
            return (200, 100, 100)  # Red

    def _format_bonus(self, bonus_id: str, value: float) -> str:
        """Format bonus for display."""
        bonus_names = {
            "morale": "Morale",
            "movement": "Movement",
            "cavalry_flanking": "Cavalry Flanking",
            "formation_bonus": "Formation Bonus",
            "experience_gain": "XP Gain",
        }

        name = bonus_names.get(bonus_id, bonus_id.replace("_", " ").title())

        # Format value
        if isinstance(value, float) and value < 1:
            value_str = f"+{int(value * 100)}%"
        else:
            value_str = f"+{value}"

        return f"{name} {value_str}"

    def _update_card_selection_states(self) -> None:
        """Update selection state of commander cards."""
        for card in self.commander_cards:
            card.set_selected(card.commander_id == self.selected_commander)

    def _render_tooltip(self, screen: pygame.Surface) -> None:
        """Render tooltip for hovered elements."""
        mouse_pos = pygame.mouse.get_pos()

        # Check if hovering over commander card
        for card in self.commander_cards:
            if card.rect.collidepoint(mouse_pos) and card.is_hovered:
                commander_data = card.commander_data

                # Create tooltip with commander quote
                quote = commander_data.get("quote", "")
                if quote:
                    self._render_floating_tooltip(screen, quote, mouse_pos)
                return

        # Check if hovering over faction button
        for i, button in enumerate(self.faction_buttons):
            if button.rect.collidepoint(mouse_pos) and button.is_hovered:
                faction_id = list(FACTION_DATA.keys())[i]
                faction_data = FACTION_DATA[faction_id]

                tooltip_text = faction_data.get("description", "")
                if tooltip_text:
                    self._render_floating_tooltip(screen, tooltip_text, mouse_pos)
                return

    def _render_floating_tooltip(self, screen: pygame.Surface, text: str, mouse_pos: tuple) -> None:
        """Render a floating tooltip near mouse cursor."""
        # Create tooltip surface
        tooltip_font = pygame.font.Font(None, 20)
        padding = 10
        max_width = 300

        # Word wrap text
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if tooltip_font.size(test_line)[0] <= max_width - 2 * padding:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Calculate tooltip size
        line_height = 22
        tooltip_width = max(tooltip_font.size(line)[0] for line in lines) + 2 * padding
        tooltip_height = len(lines) * line_height + 2 * padding

        # Position tooltip (avoid going off screen)
        tooltip_x = mouse_pos[0] + 15
        tooltip_y = mouse_pos[1] + 15

        if tooltip_x + tooltip_width > SCREEN_WIDTH:
            tooltip_x = mouse_pos[0] - tooltip_width - 15
        if tooltip_y + tooltip_height > SCREEN_HEIGHT:
            tooltip_y = mouse_pos[1] - tooltip_height - 15

        # Draw tooltip background (parchment style)
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)

        # Shadow
        shadow_rect = tooltip_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 100))
        screen.blit(shadow_surface, shadow_rect.topleft)

        # Background
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height))
        tooltip_surface.fill((230, 220, 190))
        screen.blit(tooltip_surface, tooltip_rect.topleft)

        # Border
        pygame.draw.rect(screen, (139, 69, 19), tooltip_rect, 2)

        # Render text lines
        for i, line in enumerate(lines):
            line_surface = tooltip_font.render(line, True, (50, 40, 30))
            line_y = tooltip_y + padding + i * line_height
            screen.blit(line_surface, (tooltip_x + padding, line_y))
