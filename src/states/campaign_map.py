"""
Campaign map state - Pokemon Emerald-style tile-based world navigation.
"""

import pygame
from src.core.state_manager import GameState
from src.core.constants import *
from src.procgen.tile_map_generator import TileMapGenerator, TileType
from src.procgen.encounter_generator import EncounterGenerator
from src.entities.army import Army
from src.entities.unit import Unit
import random
import os


class CampaignMapState(GameState):
    """
    Campaign map state where player navigates a Pokemon Emerald-style tile-based world.
    """

    # Tile size in pixels
    TILE_SIZE = 16

    # Tile colors (Pokemon Emerald-inspired palette)
    TILE_COLORS = {
        TileType.GRASS: (120, 200, 80),           # Light green
        TileType.TALL_GRASS: (80, 160, 60),       # Dark green
        TileType.WATER: (64, 160, 224),           # Blue
        TileType.DEEP_WATER: (32, 96, 192),       # Deep blue
        TileType.SAND: (240, 224, 160),           # Beige
        TileType.TREE: (40, 100, 40),             # Dark green
        TileType.PATH: (192, 176, 144),           # Brown
        TileType.FLOWER: (255, 160, 200),         # Pink
        TileType.ROCK: (128, 128, 128),           # Gray
        TileType.BUILDING: (180, 80, 60),         # Red-brown
        TileType.TOWN: (200, 200, 200),           # Light gray
        TileType.LEDGE: (160, 140, 100),          # Brown
    }

    def __init__(self, state_manager, game_engine=None):
        super().__init__(state_manager)
        self.engine = game_engine
        self.player_position = [0, 0]  # Tile coordinates
        self.camera_offset = [0, 0]    # Pixel offset

        # Map generator and tiles
        self.map_generator = None
        self.tile_map = None

        # Player sprite color (placeholder)
        self.player_color = (255, 200, 0)  # Yellow

        # Movement
        self.move_cooldown = 0
        self.move_delay = 0.15  # Seconds between moves

        # Army and encounter system
        self.player_army = None
        self.encounter_generator = None
        self.steps_since_encounter = 0
        self.encounter_rate = 10  # Average steps before encounter
        self.difficulty_level = 1  # Increases as player progresses
        self.total_steps = 0  # Track total steps for difficulty scaling

        # Sprite assets
        self.sprites = {}
        self.player_sprite = None
        self._load_sprites()

    def _load_sprites(self) -> None:
        """Load terrain and unit sprites."""
        # Define terrain sprite mappings
        terrain_mappings = {
            TileType.GRASS: 'grass_0.png',
            TileType.TALL_GRASS: 'grass_1.png',
            TileType.WATER: 'water_0.png',
            TileType.DEEP_WATER: 'water_1.png',
            TileType.SAND: 'sand_0.png',
            TileType.TREE: 'forest_0.png',
            TileType.PATH: 'sand_1.png',  # Using sand as path
            TileType.FLOWER: 'grass_2.png',  # Using grass variant
            TileType.ROCK: 'mountain_0.png',
            TileType.BUILDING: 'mountain_1.png',  # Placeholder
            TileType.TOWN: 'mountain_2.png',  # Placeholder
            TileType.LEDGE: 'mountain_0.png',  # Using mountain
        }

        # Load terrain sprites
        for tile_type, filename in terrain_mappings.items():
            sprite_path = os.path.join('assets', 'sprites', 'terrain', filename)
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale to TILE_SIZE if needed (sprites are 16x16, same as our tile size)
                if sprite.get_width() != self.TILE_SIZE or sprite.get_height() != self.TILE_SIZE:
                    sprite = pygame.transform.scale(sprite, (self.TILE_SIZE, self.TILE_SIZE))
                self.sprites[tile_type] = sprite
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
                # Create a colored fallback if sprite loading fails
                fallback = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
                fallback.fill(self.TILE_COLORS.get(tile_type, (255, 0, 255)))
                self.sprites[tile_type] = fallback

        # Load player sprite (use a hoplite for now)
        player_sprite_path = os.path.join('assets', 'sprites', 'units', 'greek', 'hoplite.png')
        try:
            self.player_sprite = pygame.image.load(player_sprite_path)
            if self.player_sprite.get_width() != self.TILE_SIZE or self.player_sprite.get_height() != self.TILE_SIZE:
                self.player_sprite = pygame.transform.scale(self.player_sprite, (self.TILE_SIZE, self.TILE_SIZE))
        except pygame.error as e:
            print(f"Could not load player sprite: {e}")
            # Create fallback player sprite
            self.player_sprite = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
            self.player_sprite.fill(self.player_color)

    def on_enter(self) -> None:
        """Initialize campaign when entering or resuming from battle."""
        super().on_enter()

        # Generate map only on first entry
        if self.map_generator is None:
            self._generate_pokemon_map()

        # Initialize army and encounter system if not already done
        if self.player_army is None:
            self._create_starting_army()
        else:
            # Returning from battle - check army status
            self._check_army_status()

        if self.encounter_generator is None:
            self.encounter_generator = EncounterGenerator(seed=random.randint(0, 999999))

    def _generate_pokemon_map(self) -> None:
        """Generate Pokemon Emerald-style tile map."""
        seed = random.randint(0, 999999)
        self.map_generator = TileMapGenerator(seed=seed)

        # Generate map (80x45 tiles = 1280x720 pixels at 16px per tile, perfect 16:9 fit)
        self.tile_map = self.map_generator.generate_map(
            width=80,
            height=45,
            num_towns=5,
            water_level=0.25,
            forest_density=0.35
        )

        # Set player starting position at first town
        spawn_x, spawn_y = self.map_generator.get_spawn_location()
        self.player_position = [spawn_x, spawn_y]

        # Center camera on player
        self._center_camera_on_player()

    def _center_camera_on_player(self) -> None:
        """Center the camera on the player with bounds clamping."""
        screen_center_x = SCREEN_WIDTH // 2
        screen_center_y = SCREEN_HEIGHT // 2

        player_pixel_x = self.player_position[0] * self.TILE_SIZE
        player_pixel_y = self.player_position[1] * self.TILE_SIZE

        # Calculate desired camera position (center on player)
        self.camera_offset[0] = screen_center_x - player_pixel_x - self.TILE_SIZE // 2
        self.camera_offset[1] = screen_center_y - player_pixel_y - self.TILE_SIZE // 2

        # Clamp camera to prevent showing empty space beyond map boundaries
        map_pixel_width = self.map_generator.width * self.TILE_SIZE
        map_pixel_height = self.map_generator.height * self.TILE_SIZE

        # Clamp X: Keep map filling screen horizontally
        # camera_offset[0] should be in range [SCREEN_WIDTH - map_width, 0]
        min_offset_x = SCREEN_WIDTH - map_pixel_width
        max_offset_x = 0
        self.camera_offset[0] = max(min_offset_x, min(max_offset_x, self.camera_offset[0]))

        # Clamp Y: Keep map filling screen vertically
        # camera_offset[1] should be in range [SCREEN_HEIGHT - map_height, 0]
        min_offset_y = SCREEN_HEIGHT - map_pixel_height
        max_offset_y = 0
        self.camera_offset[1] = max(min_offset_y, min(max_offset_y, self.camera_offset[1]))

    def _create_starting_army(self) -> None:
        """Create player's starting army based on faction/commander."""
        # Get faction from engine if available
        faction = "greece"  # Default
        if self.engine and hasattr(self.engine, 'selected_faction'):
            faction = self.engine.selected_faction

        # Create player army
        self.player_army = Army(faction=faction, is_player=True)

        # Set commander info
        if self.engine and hasattr(self.engine, 'selected_commander'):
            self.player_army.commander_id = self.engine.selected_commander

        # Define starting units based on faction
        faction_units = {
            "greece": ["spearman", "spearman", "archer"],
            "rome": ["infantry", "infantry", "spearman"],
            "persia": ["archer", "archer", "cavalry"],
            "carthage": ["cavalry", "spearman", "archer"],
        }

        starting_units = faction_units.get(faction, ["infantry", "infantry", "spearman"])

        # Create units (note: positions will be assigned when battle starts)
        for i, unit_type in enumerate(starting_units):
            unit = Unit(
                unit_type=unit_type,
                faction="player",
                position=(0, 0),  # Placeholder position
                count=100,  # Full strength unit
                is_player=True
            )
            self.player_army.add_unit(unit)

        print(f"Created starting army for {faction}: {len(self.player_army.units)} units")

    def _check_army_status(self) -> None:
        """Check army status after returning from battle."""
        if not self.player_army:
            return

        # Check if player was defeated
        if self.player_army.is_defeated():
            print("GAME OVER! All units lost.")
            # TODO: Implement game over screen or restart
            # For now, recreate starting army
            self._create_starting_army()
            return

        # Report casualties and surviving units
        alive_units = [u for u in self.player_army.units if u.is_alive()]
        print(f"Battle complete! {len(alive_units)} units survived.")

        # Calculate total remaining strength
        total_strength = self.player_army.get_total_strength()
        print(f"   Total army strength: {total_strength} troops")

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle campaign map input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to main menu
                from src.states.main_menu import MainMenuState
                self.state_manager.change_state(MainMenuState(self.state_manager))

            elif event.key == pygame.K_RETURN:
                # Interact with current tile
                self._interact_with_tile()

    def _move_player(self, dx: int, dy: int) -> None:
        """
        Move player in a direction.

        Args:
            dx: X direction (-1, 0, 1)
            dy: Y direction (-1, 0, 1)
        """
        new_x = self.player_position[0] + dx
        new_y = self.player_position[1] + dy

        # Check bounds
        if not (0 <= new_x < self.map_generator.width and 0 <= new_y < self.map_generator.height):
            return

        # Check if tile is walkable
        tile = self.map_generator.get_tile(new_x, new_y)
        if not tile or not tile.walkable:
            return

        # Move player
        self.player_position[0] = new_x
        self.player_position[1] = new_y

        # Update camera to follow player smoothly
        self._center_camera_on_player()

        # Track total steps for difficulty scaling
        self.total_steps += 1

        # Check for encounters on all terrain types
        self._check_encounter()

    def _check_encounter(self) -> None:
        """Check if a random encounter occurs."""
        self.steps_since_encounter += 1

        # Random encounter chance
        if random.randint(0, self.encounter_rate) < self.steps_since_encounter:
            self.steps_since_encounter = 0
            print("Wild battle encounter!")

            # Calculate difficulty based on progress (1-10 scale)
            self.difficulty_level = min(10, 1 + self.total_steps // 20)

            # Get player army strength
            player_strength = self.player_army.get_total_strength()

            # Select random enemy faction
            enemy_factions = ["persia", "carthage", "rome", "greece"]
            enemy_faction = random.choice(enemy_factions)

            # Generate encounter using EncounterGenerator
            encounter_data = self.encounter_generator.generate_encounter(
                difficulty=self.difficulty_level,
                faction=enemy_faction,
                player_strength=player_strength
            )

            # Create enemy army
            enemy_army = Army(faction=enemy_faction, is_player=False)

            # Convert enemy definitions to Unit objects
            for enemy_def in encounter_data["units"]:
                unit = Unit(
                    unit_type=enemy_def["type"],
                    faction="enemy",
                    position=(0, 0),  # Position will be set in battle
                    count=enemy_def["count"],
                    is_player=False
                )

                # Assign AI type based on unit type
                ai_comp = unit.get_component("AIComponent")
                if ai_comp:
                    unit_type_str = enemy_def["type"].lower()

                    # Cavalry is aggressive
                    if "cavalry" in unit_type_str or "horse" in unit_type_str:
                        ai_comp.ai_type = "aggressive"
                        ai_comp.target_priority = "weakest"  # Chase down weak targets

                    # Archers are defensive
                    elif "archer" in unit_type_str or "bow" in unit_type_str:
                        ai_comp.ai_type = "defensive"
                        ai_comp.target_priority = "nearest"  # Stay back, shoot nearest

                    # Spearmen are balanced
                    elif "spear" in unit_type_str or "pike" in unit_type_str:
                        ai_comp.ai_type = "balanced"
                        ai_comp.target_priority = "strongest"  # Focus on threats

                    # Infantry is balanced
                    elif "infantry" in unit_type_str or "legion" in unit_type_str:
                        ai_comp.ai_type = "balanced"
                        ai_comp.target_priority = "nearest"

                    # Default: balanced with nearest priority
                    else:
                        ai_comp.ai_type = "balanced"
                        ai_comp.target_priority = "nearest"

                enemy_army.add_unit(unit)

            print(f"Encounter: {len(enemy_army.units)} {enemy_faction} units (difficulty {self.difficulty_level})")

            # Transition to battle using morale-driven warfare system
            self._start_battle(enemy_army, battle_mode="morale")

    def _start_battle(self, enemy_army: Army, battle_mode: str = "morale") -> None:
        """
        Start a tactical battle with the given enemy army.

        Args:
            enemy_army: The enemy army to fight
            battle_mode: "morale" (3-phase strategic, default) or "formation" (4v4 fast, legacy)
        """
        from src.states.battle_state_formation import BattleStateFormation
        from src.states.battle_state_morale import BattleStateMorale

        # Calculate difficulty based on campaign progression
        difficulty = max(1, self.total_steps // 20)

        # Create appropriate battle state based on mode
        if battle_mode == "morale":
            # Strategic morale-driven battle (3-phase)
            battle_state = BattleStateMorale(
                self.state_manager,
                player_army=self.player_army,
                enemy_army=enemy_army,
                difficulty=difficulty,
                player_commander_id="alexander",  # TODO: Get from player profile
                enemy_commander_id="leonidas"     # TODO: Generate enemy commander
            )
        else:
            # Fast formation battle (4v4)
            battle_state = BattleStateFormation(
                self.state_manager,
                player_army=self.player_army,
                enemy_army=enemy_army,
                difficulty=difficulty
            )

        # Push battle state (allows returning to campaign after battle)
        self.state_manager.push_state(battle_state)

        # When battle ends, control returns here
        # Check army status on return
        self._check_army_status()

    def _interact_with_tile(self) -> None:
        """Interact with the current tile."""
        x, y = self.player_position
        tile = self.map_generator.get_tile(x, y)

        if tile.type == TileType.BUILDING:
            print("Entered building - Shop/Rest area")
            # TODO: Open building menu
        elif tile.type == TileType.PATH:
            print("On a route")
        else:
            print(f"Standing on {tile.type.value}")

    def update(self, delta_time: float) -> None:
        """Update campaign logic."""
        # Update move cooldown
        self.move_cooldown = max(0, self.move_cooldown - delta_time)

        # Handle continuous movement
        if self.move_cooldown <= 0:
            keys = pygame.key.get_pressed()
            moved = False

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self._move_player(0, -1)
                moved = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self._move_player(0, 1)
                moved = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self._move_player(-1, 0)
                moved = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self._move_player(1, 0)
                moved = True

            if moved:
                self.move_cooldown = self.move_delay

    def render(self, screen: pygame.Surface) -> None:
        """Render the Pokemon Emerald-style campaign map."""
        # Fill with sky blue background
        screen.fill((135, 206, 235))

        # Calculate visible tile range
        cam_x, cam_y = self.camera_offset

        start_x = max(0, -cam_x // self.TILE_SIZE - 1)
        start_y = max(0, -cam_y // self.TILE_SIZE - 1)
        end_x = min(self.map_generator.width, start_x + SCREEN_WIDTH // self.TILE_SIZE + 2)
        end_y = min(self.map_generator.height, start_y + SCREEN_HEIGHT // self.TILE_SIZE + 2)

        # Render tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.map_generator.get_tile(x, y)
                if not tile:
                    continue

                # Calculate screen position
                screen_x = x * self.TILE_SIZE + cam_x
                screen_y = y * self.TILE_SIZE + cam_y

                # Get tile sprite or fallback to color
                sprite = self.sprites.get(tile.type)

                if sprite:
                    # Draw sprite
                    screen.blit(sprite, (screen_x, screen_y))
                else:
                    # Fallback to colored rectangle if no sprite
                    color = self.TILE_COLORS.get(tile.type, (255, 0, 255))  # Magenta for unknown
                    pygame.draw.rect(
                        screen,
                        color,
                        (screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE)
                    )

                # Add simple border for path/building tiles
                if tile.type in [TileType.PATH, TileType.BUILDING]:
                    border_color = (0, 0, 0, 64)  # Semi-transparent black
                    pygame.draw.rect(
                        screen,
                        border_color,
                        (screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE),
                        1
                    )

        # Render player
        player_screen_x = self.player_position[0] * self.TILE_SIZE + cam_x
        player_screen_y = self.player_position[1] * self.TILE_SIZE + cam_y

        if self.player_sprite:
            # Draw player sprite
            screen.blit(self.player_sprite, (player_screen_x, player_screen_y))
        else:
            # Fallback to circle if no sprite
            pygame.draw.circle(
                screen,
                self.player_color,
                (player_screen_x + self.TILE_SIZE // 2, player_screen_y + self.TILE_SIZE // 2),
                self.TILE_SIZE // 2 - 2
            )

            # Draw player outline
            pygame.draw.circle(
                screen,
                (0, 0, 0),
                (player_screen_x + self.TILE_SIZE // 2, player_screen_y + self.TILE_SIZE // 2),
                self.TILE_SIZE // 2 - 2,
                2
            )

        # Render UI
        self._render_ui(screen)

    def _render_ui(self, screen: pygame.Surface) -> None:
        """Render campaign map UI."""
        # Semi-transparent panel at top
        panel = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        screen.blit(panel, (0, 0))

        # Title
        font_large = pygame.font.Font(None, 36)
        title = font_large.render("Campaign Map", True, COLOR_TEXT)
        screen.blit(title, (20, 10))

        # Position info
        font_small = pygame.font.Font(None, 24)
        pos_text = font_small.render(
            f"Position: ({self.player_position[0]}, {self.player_position[1]})",
            True,
            COLOR_TEXT
        )
        screen.blit(pos_text, (20, 38))

        # Current tile info
        tile = self.map_generator.get_tile(self.player_position[0], self.player_position[1])
        tile_info = font_small.render(
            f"Terrain: {tile.type.value.replace('_', ' ').title()}",
            True,
            COLOR_TEXT
        )
        screen.blit(tile_info, (300, 38))

        # Controls hint at bottom
        controls_text = font_small.render(
            "Arrow Keys/WASD: Move | Enter: Interact | ESC: Menu",
            True,
            (220, 220, 220)
        )
        controls_rect = controls_text.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 10)
        screen.blit(controls_text, controls_rect)
