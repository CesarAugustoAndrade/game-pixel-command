"""
Pokemon Emerald-style tile-based map generator for campaign/overworld.
Creates colorful, tile-based maps with grass, water, trees, paths, and towns.
"""

import random
from typing import List, Tuple, Dict, Set
from src.procgen.noise import SimpleNoise
from enum import Enum


class TileType(Enum):
    """Tile types for Pokemon Emerald-style map."""
    GRASS = "grass"
    TALL_GRASS = "tall_grass"
    WATER = "water"
    DEEP_WATER = "deep_water"
    SAND = "sand"
    TREE = "tree"
    PATH = "path"
    FLOWER = "flower"
    ROCK = "rock"
    BUILDING = "building"
    TOWN = "town"
    LEDGE = "ledge"


class Tile:
    """Represents a single tile in the map."""

    def __init__(self, x: int, y: int, tile_type: TileType):
        """
        Initialize tile.

        Args:
            x: X coordinate
            y: Y coordinate
            tile_type: Type of tile
        """
        self.x = x
        self.y = y
        self.type = tile_type
        self.walkable = tile_type not in [
            TileType.WATER, TileType.DEEP_WATER, TileType.TREE,
            TileType.ROCK, TileType.BUILDING
        ]
        self.encounter_zone = tile_type in [TileType.TALL_GRASS, TileType.WATER]

        # Visual properties
        self.variant = 0  # For tile variations


class TileMapGenerator:
    """
    Generates Pokemon Emerald-style tile-based overworld maps.
    Features routes, towns, water bodies, forests, and decorative elements.
    """

    def __init__(self, seed: int = None):
        """
        Initialize tile map generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        self.noise = SimpleNoise(seed)
        self.width = 0
        self.height = 0
        self.tiles: List[List[Tile]] = []
        self.towns: List[Tuple[int, int]] = []
        self.routes: List[List[Tuple[int, int]]] = []

    def generate_map(
        self,
        width: int = 80,
        height: int = 60,
        num_towns: int = 5,
        water_level: float = 0.3,
        forest_density: float = 0.4
    ) -> List[List[Tile]]:
        """
        Generate a complete Pokemon Emerald-style map.

        Args:
            width: Map width in tiles
            height: Map height in tiles
            num_towns: Number of towns to generate
            water_level: Amount of water (0.0-1.0)
            forest_density: Density of trees (0.0-1.0)

        Returns:
            2D list of Tile objects
        """
        self.width = width
        self.height = height

        # Initialize empty map with grass
        self._initialize_base_terrain()

        # Generate base terrain using noise
        self._generate_terrain_base(water_level)

        # Generate water bodies
        self._generate_water_bodies()

        # Generate towns at strategic locations
        self._generate_towns(num_towns)

        # Create paths/routes between towns
        self._generate_routes()

        # Add forests and trees
        self._add_forests(forest_density)

        # Add beaches around water
        self._add_beaches()

        # Add decorative elements
        self._add_decorations()

        # Smooth transitions between biomes
        self._smooth_terrain()

        return self.tiles

    def _initialize_base_terrain(self) -> None:
        """Initialize map with base grass tiles."""
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = Tile(x, y, TileType.GRASS)
                row.append(tile)
            self.tiles.append(row)

    def _generate_terrain_base(self, water_level: float) -> None:
        """
        Generate base terrain using noise.

        Args:
            water_level: Threshold for water generation
        """
        scale = 0.08  # Noise scale - smaller = larger features

        for y in range(self.height):
            for x in range(self.width):
                # Get noise value
                noise_val = self.noise.noise2d(x * scale, y * scale)

                # Normalize to 0-1
                noise_val = (noise_val + 1) / 2

                # Determine terrain type based on noise
                if noise_val < water_level:
                    self.tiles[y][x].type = TileType.WATER
                elif noise_val < water_level + 0.05:
                    self.tiles[y][x].type = TileType.SAND
                else:
                    # Mix of grass and tall grass
                    if random.random() < 0.3:
                        self.tiles[y][x].type = TileType.TALL_GRASS
                    else:
                        self.tiles[y][x].type = TileType.GRASS

    def _generate_water_bodies(self) -> None:
        """Create lakes and deep water areas."""
        # Add some deep water in the center of large water bodies
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.tiles[y][x].type == TileType.WATER:
                    # Count water neighbors
                    water_neighbors = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if self.tiles[y + dy][x + dx].type == TileType.WATER:
                                water_neighbors += 1

                    # If surrounded by water, make it deep water
                    if water_neighbors >= 7:
                        self.tiles[y][x].type = TileType.DEEP_WATER

    def _generate_towns(self, num_towns: int) -> None:
        """
        Generate town locations.

        Args:
            num_towns: Number of towns to place
        """
        self.towns = []
        attempts = 0
        max_attempts = num_towns * 10

        while len(self.towns) < num_towns and attempts < max_attempts:
            attempts += 1

            # Random location
            x = random.randint(5, self.width - 6)
            y = random.randint(5, self.height - 6)

            # Check if location is suitable (on grass, far from other towns)
            if not self._is_suitable_town_location(x, y):
                continue

            # Place town (3x3 area)
            self._place_town(x, y)
            self.towns.append((x, y))

    def _is_suitable_town_location(self, x: int, y: int) -> bool:
        """
        Check if location is suitable for a town.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if suitable
        """
        # Check if on land
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                tile = self.tiles[y + dy][x + dx]
                if tile.type in [TileType.WATER, TileType.DEEP_WATER]:
                    return False

        # Check distance from other towns
        for town_x, town_y in self.towns:
            dist = ((x - town_x) ** 2 + (y - town_y) ** 2) ** 0.5
            if dist < 15:  # Minimum distance between towns
                return False

        return True

    def _place_town(self, center_x: int, center_y: int) -> None:
        """
        Place a town at the given location.

        Args:
            center_x: Center X coordinate
            center_y: Center Y coordinate
        """
        # Clear 5x5 area and place town tiles
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                x, y = center_x + dx, center_y + dy

                # Center is the main building
                if dx == 0 and dy == 0:
                    self.tiles[y][x].type = TileType.BUILDING
                # Edges are grass, inner area is path
                elif abs(dx) <= 1 and abs(dy) <= 1:
                    self.tiles[y][x].type = TileType.PATH
                else:
                    self.tiles[y][x].type = TileType.GRASS

    def _generate_routes(self) -> None:
        """Generate paths connecting towns."""
        self.routes = []

        # Connect each town to nearest unconnected town
        connected = set()

        for i, (x1, y1) in enumerate(self.towns):
            if i == 0:
                connected.add(i)

            # Find nearest connected town
            min_dist = float('inf')
            nearest = None

            for j in connected:
                x2, y2 = self.towns[j]
                dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest = j

            if nearest is not None:
                x2, y2 = self.towns[nearest]
                route = self._create_path(x1, y1, x2, y2)
                self.routes.append(route)
                connected.add(i)

    def _create_path(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> List[Tuple[int, int]]:
        """
        Create a path between two points.

        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates

        Returns:
            List of path coordinates
        """
        path = []
        x, y = x1, y1

        # Simple path - move horizontally then vertically
        while x != x2:
            path.append((x, y))
            x += 1 if x < x2 else -1

            # Place path tile if not water
            if self.tiles[y][x].type not in [TileType.WATER, TileType.DEEP_WATER]:
                self.tiles[y][x].type = TileType.PATH

        while y != y2:
            path.append((x, y))
            y += 1 if y < y2 else -1

            # Place path tile if not water
            if self.tiles[y][x].type not in [TileType.WATER, TileType.DEEP_WATER]:
                self.tiles[y][x].type = TileType.PATH

        return path

    def _add_forests(self, density: float) -> None:
        """
        Add forest areas with trees.

        Args:
            density: Tree density (0.0-1.0)
        """
        # Use noise to create forest patches
        scale = 0.12

        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]

                # Only place trees on grass
                if tile.type not in [TileType.GRASS, TileType.TALL_GRASS]:
                    continue

                # Don't place trees near paths or towns
                if self._is_near_path_or_town(x, y, radius=2):
                    continue

                # Use noise for natural-looking forests
                noise_val = self.noise.noise2d(x * scale + 100, y * scale + 100)
                noise_val = (noise_val + 1) / 2

                if noise_val > (1 - density):
                    tile.type = TileType.TREE

    def _add_beaches(self) -> None:
        """Add sand beaches around water bodies."""
        changes = []

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                tile = self.tiles[y][x]

                # Add sand next to water
                if tile.type in [TileType.GRASS, TileType.TALL_GRASS]:
                    # Check if adjacent to water
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        neighbor = self.tiles[y + dy][x + dx]
                        if neighbor.type in [TileType.WATER, TileType.DEEP_WATER]:
                            changes.append((x, y, TileType.SAND))
                            break

        # Apply changes
        for x, y, tile_type in changes:
            self.tiles[y][x].type = tile_type

    def _add_decorations(self) -> None:
        """Add decorative elements like flowers and rocks."""
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]

                # Add flowers to grass
                if tile.type == TileType.GRASS and random.random() < 0.05:
                    tile.type = TileType.FLOWER

                # Add occasional rocks
                if tile.type == TileType.GRASS and random.random() < 0.02:
                    if not self._is_near_path_or_town(x, y, radius=3):
                        tile.type = TileType.ROCK

    def _smooth_terrain(self) -> None:
        """Smooth terrain transitions using cellular automata."""
        # Smooth tall grass
        for _ in range(2):
            changes = []

            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    tile = self.tiles[y][x]

                    if tile.type == TileType.TALL_GRASS:
                        # Count grass neighbors
                        grass_neighbors = 0
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if self.tiles[y + dy][x + dx].type == TileType.GRASS:
                                    grass_neighbors += 1

                        # Convert to grass if mostly surrounded by grass
                        if grass_neighbors > 5:
                            changes.append((x, y, TileType.GRASS))

            # Apply changes
            for x, y, tile_type in changes:
                self.tiles[y][x].type = tile_type

    def _is_near_path_or_town(self, x: int, y: int, radius: int = 2) -> bool:
        """
        Check if location is near a path or town.

        Args:
            x: X coordinate
            y: Y coordinate
            radius: Check radius

        Returns:
            True if near path or town
        """
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    tile_type = self.tiles[ny][nx].type
                    if tile_type in [TileType.PATH, TileType.BUILDING, TileType.TOWN]:
                        return True
        return False

    def get_tile(self, x: int, y: int) -> Tile:
        """
        Get tile at coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Tile or None if out of bounds
        """
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.tiles[y][x]
        return None

    def get_spawn_location(self) -> Tuple[int, int]:
        """
        Get a suitable spawn location for the player.

        Returns:
            (x, y) coordinates
        """
        # Spawn at first town if available
        if self.towns:
            return self.towns[0]

        # Otherwise find a grass tile
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x].type == TileType.GRASS:
                    return (x, y)

        return (self.width // 2, self.height // 2)

    def get_encounter_zones(self) -> List[Tuple[int, int]]:
        """
        Get all tiles that can trigger encounters.

        Returns:
            List of (x, y) coordinates
        """
        zones = []
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x].encounter_zone:
                    zones.append((x, y))
        return zones