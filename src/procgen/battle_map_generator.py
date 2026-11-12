"""
Advance Wars-style tactical battle map generation.

Design Philosophy:
- Strategic Intent: Every map tells a tactical story
- Natural Flow: Terrain clusters realistically (forests group, mountains form ranges)
- Balanced Asymmetry: Fair but interesting starting positions
- Tactical Depth: Multiple valid strategies per map
- Visual Clarity: Terrain is immediately recognizable
"""

import random
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from src.battle.hex_grid import HexGrid, HexCell


@dataclass
class Building:
    """Capturable building on the battlefield."""
    q: int
    r: int
    building_type: str  # 'city', 'base', 'hq', 'fort'
    owner: Optional[str] = None  # None = neutral, 'player', 'enemy'
    capture_points: int = 20  # HP needed to capture
    income: int = 1000  # Income per turn if owned

    def __hash__(self):
        return hash((self.q, self.r))


class BattleMapGenerator:
    """
    Generates Advance Wars-quality tactical battle maps.

    Features:
    - Strategic terrain placement (no random scatter)
    - Capturable objectives (cities, bases, HQ)
    - Natural terrain clustering
    - Balanced deployment zones
    - Multiple map templates with different tactical themes
    """

    def __init__(self, seed: int = None):
        """
        Initialize battle map generator.

        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

        self.buildings: List[Building] = []

    def generate_map(
        self,
        width: int,
        height: int,
        hex_size: int,
        template: str = "plains_encounter"
    ) -> Tuple[HexGrid, List[Building]]:
        """
        Generate a tactical battle map using a template.

        Args:
            width: Map width in hexes
            height: Map height in hexes
            hex_size: Hex size in pixels
            template: Map template to use

        Returns:
            (HexGrid, List of Buildings)
        """
        grid = HexGrid(width, height, hex_size)
        self.buildings = []

        # Generate based on template
        if template == "plains_encounter":
            self._generate_plains_encounter(grid)
        elif template == "forest_ambush":
            self._generate_forest_ambush(grid)
        elif template == "mountain_pass":
            self._generate_mountain_pass(grid)
        elif template == "river_crossing":
            self._generate_river_crossing(grid)
        elif template == "siege_battle":
            self._generate_siege_battle(grid)
        else:
            # Default to plains encounter
            self._generate_plains_encounter(grid)

        return grid, self.buildings

    # ========================================================================
    # MAP TEMPLATE 1: PLAINS ENCOUNTER
    # Theme: Open battlefield with scattered cover and contested center
    # ========================================================================

    def _generate_plains_encounter(self, grid: HexGrid) -> None:
        """
        Generate an open plains battle with:
        - Mostly open terrain for maneuver warfare
        - Strategic forests for cover
        - Hills for high ground advantage
        - Contested cities in center
        """
        # 1. Start with plains base
        for cell in grid.cells.values():
            cell.terrain = "plains"

        # 2. Add strategic forest clusters (not random scatter!)
        forest_centers = [
            (grid.width // 4, grid.height // 3),
            (grid.width * 3 // 4, grid.height * 2 // 3),
            (grid.width // 2, grid.height // 6),
            (grid.width // 2, grid.height * 5 // 6),
        ]

        for center_q, center_r in forest_centers:
            self._create_terrain_blob(grid, center_q, center_r, "forest", radius=3)

        # 3. Add hill clusters for high ground
        hill_centers = [
            (grid.width // 3, grid.height // 2),
            (grid.width * 2 // 3, grid.height // 2),
        ]

        for center_q, center_r in hill_centers:
            self._create_terrain_blob(grid, center_q, center_r, "hills", radius=2)

        # 4. Place capturable buildings
        # Center cities (contested)
        self._add_building(grid, grid.width // 2, grid.height // 2, "city", owner=None)
        self._add_building(grid, grid.width // 2 - 2, grid.height // 2, "city", owner=None)
        self._add_building(grid, grid.width // 2 + 2, grid.height // 2, "city", owner=None)

        # Player side
        self._add_building(grid, 2, grid.height // 2, "base", owner="player")
        self._add_building(grid, 1, grid.height // 4, "city", owner="player")
        self._add_building(grid, 1, grid.height * 3 // 4, "city", owner="player")

        # Enemy side
        self._add_building(grid, grid.width - 3, grid.height // 2, "base", owner="enemy")
        self._add_building(grid, grid.width - 2, grid.height // 4, "city", owner="enemy")
        self._add_building(grid, grid.width - 2, grid.height * 3 // 4, "city", owner="enemy")

    # ========================================================================
    # MAP TEMPLATE 2: FOREST AMBUSH
    # Theme: Dense woodland with clearings, favors infantry and ambush tactics
    # ========================================================================

    def _generate_forest_ambush(self, grid: HexGrid) -> None:
        """
        Generate a forest battlefield with:
        - Dense forest covering most of map
        - Strategic clearings for battles
        - Mountain ranges as barriers
        - Hidden paths through woods
        """
        # 1. Start with dense forest
        for cell in grid.cells.values():
            cell.terrain = "forest"

        # 2. Create central clearing (main battlefield)
        center_q, center_r = grid.width // 2, grid.height // 2
        self._create_terrain_blob(grid, center_q, center_r, "plains", radius=4)

        # 3. Create paths through forest (plains corridors)
        # Horizontal path
        for q in range(grid.width):
            for r in range(grid.height // 2 - 1, grid.height // 2 + 2):
                cell = grid.get_cell(q, r)
                if cell and random.random() < 0.6:
                    cell.terrain = "plains"

        # Vertical paths (narrower)
        for r in range(grid.height):
            for q in range(grid.width // 4 - 1, grid.width // 4 + 2):
                cell = grid.get_cell(q, r)
                if cell and random.random() < 0.4:
                    cell.terrain = "plains"
            for q in range(grid.width * 3 // 4 - 1, grid.width * 3 // 4 + 2):
                cell = grid.get_cell(q, r)
                if cell and random.random() < 0.4:
                    cell.terrain = "plains"

        # 4. Add mountain obstacles
        mountain_positions = [
            (grid.width // 3, grid.height // 3),
            (grid.width * 2 // 3, grid.height * 2 // 3),
        ]

        for mq, mr in mountain_positions:
            self._create_terrain_blob(grid, mq, mr, "mountains", radius=2)

        # 5. Place buildings
        # Center clearing buildings
        self._add_building(grid, center_q, center_r, "city", owner=None)
        self._add_building(grid, center_q - 2, center_r, "city", owner=None)
        self._add_building(grid, center_q + 2, center_r, "city", owner=None)

        # Safe rear bases
        self._add_building(grid, 2, grid.height // 2, "base", owner="player")
        self._add_building(grid, grid.width - 3, grid.height // 2, "base", owner="enemy")

    # ========================================================================
    # MAP TEMPLATE 3: MOUNTAIN PASS
    # Theme: Narrow chokepoint through mountains, defensive battle
    # ========================================================================

    def _generate_mountain_pass(self, grid: HexGrid) -> None:
        """
        Generate a mountain pass with:
        - Mountain ranges creating natural walls
        - Narrow central passage (chokepoint)
        - High ground positions
        - Defensive strongpoints
        """
        # 1. Fill with mountains
        for cell in grid.cells.values():
            cell.terrain = "mountains"

        # 2. Create the pass (snaking path through center)
        pass_width = 3
        for q in range(grid.width):
            # Sinusoidal pass through center
            offset = int(2 * random.random() - 1)  # Random wobble
            for r in range(grid.height // 2 - pass_width // 2 + offset,
                          grid.height // 2 + pass_width // 2 + offset + 1):
                cell = grid.get_cell(q, r)
                if cell:
                    cell.terrain = "plains"

        # 3. Add hills on pass edges (high ground)
        for q in range(grid.width):
            for r_offset in [-pass_width // 2 - 1, pass_width // 2 + 1]:
                r = grid.height // 2 + r_offset
                cell = grid.get_cell(q, r)
                if cell and cell.terrain == "mountains":
                    cell.terrain = "hills"

        # 4. Create wider areas (battle zones)
        battle_zones = [
            (grid.width // 3, grid.height // 2),
            (grid.width * 2 // 3, grid.height // 2),
        ]

        for bq, br in battle_zones:
            self._create_terrain_blob(grid, bq, br, "plains", radius=3)

        # 5. Place buildings at strategic points
        # Center of pass
        self._add_building(grid, grid.width // 2, grid.height // 2, "city", owner=None)

        # Fort positions (defensive)
        self._add_building(grid, grid.width // 3, grid.height // 2, "fort", owner=None)
        self._add_building(grid, grid.width * 2 // 3, grid.height // 2, "fort", owner=None)

        # Bases at ends of pass
        self._add_building(grid, 3, grid.height // 2, "base", owner="player")
        self._add_building(grid, grid.width - 4, grid.height // 2, "base", owner="enemy")

    # ========================================================================
    # MAP TEMPLATE 4: RIVER CROSSING
    # Theme: River divides battlefield, limited crossing points
    # ========================================================================

    def _generate_river_crossing(self, grid: HexGrid) -> None:
        """
        Generate a river crossing battle with:
        - River running through map (barrier)
        - Bridges as chokepoints
        - Open terrain on both sides
        - Buildings on both banks
        """
        # 1. Start with plains
        for cell in grid.cells.values():
            cell.terrain = "plains"

        # 2. Create river (vertical through center)
        river_width = 2
        for q in range(grid.width // 2 - river_width // 2,
                      grid.width // 2 + river_width // 2 + 1):
            for r in range(grid.height):
                cell = grid.get_cell(q, r)
                if cell:
                    cell.terrain = "water"

        # 3. Create bridge crossings (plains through water)
        bridge_positions = [
            grid.height // 4,
            grid.height // 2,
            grid.height * 3 // 4,
        ]

        for bridge_r in bridge_positions:
            for q in range(grid.width // 2 - 1, grid.width // 2 + 2):
                cell = grid.get_cell(q, bridge_r)
                if cell:
                    cell.terrain = "plains"

        # 4. Add terrain variety on both banks
        # Forests
        forest_positions = [
            (grid.width // 4, grid.height // 3),
            (grid.width * 3 // 4, grid.height * 2 // 3),
        ]

        for fq, fr in forest_positions:
            self._create_terrain_blob(grid, fq, fr, "forest", radius=3)

        # Hills
        hill_positions = [
            (grid.width // 6, grid.height // 2),
            (grid.width * 5 // 6, grid.height // 2),
        ]

        for hq, hr in hill_positions:
            self._create_terrain_blob(grid, hq, hr, "hills", radius=2)

        # 5. Place buildings
        # Bridges are key strategic points
        for bridge_r in bridge_positions:
            self._add_building(grid, grid.width // 2, bridge_r, "city", owner=None)

        # Player bank
        self._add_building(grid, 2, grid.height // 2, "base", owner="player")
        self._add_building(grid, 3, grid.height // 4, "city", owner="player")
        self._add_building(grid, 3, grid.height * 3 // 4, "city", owner="player")

        # Enemy bank
        self._add_building(grid, grid.width - 3, grid.height // 2, "base", owner="enemy")
        self._add_building(grid, grid.width - 4, grid.height // 4, "city", owner="enemy")
        self._add_building(grid, grid.width - 4, grid.height * 3 // 4, "city", owner="enemy")

    # ========================================================================
    # MAP TEMPLATE 5: SIEGE BATTLE
    # Theme: One side has fortifications, attacker vs defender
    # ========================================================================

    def _generate_siege_battle(self, grid: HexGrid) -> None:
        """
        Generate an asymmetric siege battle with:
        - Fortified position on one side
        - Open approach for attacker
        - Defensive terrain for defender
        - Walls and chokepoints
        """
        # 1. Start with plains
        for cell in grid.cells.values():
            cell.terrain = "plains"

        # 2. Create fortified zone (right side)
        fort_boundary = grid.width * 2 // 3

        # Mountain wall
        for r in range(grid.height):
            if r < grid.height // 3 or r > grid.height * 2 // 3:
                # Wall sections
                for q in range(fort_boundary, fort_boundary + 2):
                    cell = grid.get_cell(q, r)
                    if cell:
                        cell.terrain = "mountains"

        # 3. Create gates (openings in wall)
        gate_positions = [
            grid.height // 2,
        ]

        for gate_r in gate_positions:
            for q in range(fort_boundary, fort_boundary + 2):
                cell = grid.get_cell(q, gate_r)
                if cell:
                    cell.terrain = "plains"

        # 4. Fortified interior (hills for defense bonus)
        for q in range(fort_boundary + 2, grid.width - 1):
            for r in range(grid.height // 3, grid.height * 2 // 3 + 1):
                cell = grid.get_cell(q, r)
                if cell and random.random() < 0.4:
                    cell.terrain = "hills"

        # 5. Attacker's approach (some cover)
        forest_positions = [
            (grid.width // 4, grid.height // 4),
            (grid.width // 4, grid.height * 3 // 4),
            (grid.width // 2, grid.height // 6),
            (grid.width // 2, grid.height * 5 // 6),
        ]

        for fq, fr in forest_positions:
            self._create_terrain_blob(grid, fq, fr, "forest", radius=2)

        # 6. Place buildings
        # Fortified strongpoint (defender)
        self._add_building(grid, grid.width - 3, grid.height // 2, "hq", owner="enemy")
        self._add_building(grid, fort_boundary + 1, grid.height // 2, "fort", owner="enemy")
        self._add_building(grid, grid.width - 4, grid.height // 3, "city", owner="enemy")
        self._add_building(grid, grid.width - 4, grid.height * 2 // 3, "city", owner="enemy")

        # Attacker's camp
        self._add_building(grid, 2, grid.height // 2, "base", owner="player")
        self._add_building(grid, 3, grid.height // 3, "city", owner="player")
        self._add_building(grid, 3, grid.height * 2 // 3, "city", owner="player")

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _create_terrain_blob(
        self,
        grid: HexGrid,
        center_q: int,
        center_r: int,
        terrain: str,
        radius: int
    ) -> None:
        """
        Create a natural-looking terrain cluster.
        Uses distance from center with randomness for organic shape.
        """
        for q in range(max(0, center_q - radius), min(grid.width, center_q + radius + 1)):
            for r in range(max(0, center_r - radius), min(grid.height, center_r + radius + 1)):
                cell = grid.get_cell(q, r)
                if not cell:
                    continue

                # Calculate distance from center
                distance = grid.distance(center_q, center_r, q, r)

                # Probability decreases with distance (organic edges)
                probability = max(0, 1.0 - (distance / (radius + 1)))
                probability += random.uniform(-0.2, 0.2)  # Random variation

                if random.random() < probability:
                    cell.terrain = terrain

    def _add_building(
        self,
        grid: HexGrid,
        q: int,
        r: int,
        building_type: str,
        owner: Optional[str] = None
    ) -> None:
        """
        Add a building at the specified position.
        Ensures the terrain is appropriate (not water/mountain).
        """
        cell = grid.get_cell(q, r)
        if not cell:
            return

        # Ensure buildable terrain
        if cell.terrain in ["water", "mountains"]:
            cell.terrain = "plains"

        # Create building
        building = Building(
            q=q,
            r=r,
            building_type=building_type,
            owner=owner
        )

        self.buildings.append(building)

    def _smooth_terrain_edges(self, grid: HexGrid, iterations: int = 1) -> None:
        """
        Smooth terrain using cellular automata for more natural look.
        Optional - call after initial generation if desired.
        """
        for _ in range(iterations):
            changes = []

            for cell in grid.cells.values():
                neighbors = grid.get_neighbors(cell.q, cell.r)

                # Count terrain types in neighborhood
                terrain_counts = {}
                for neighbor in neighbors:
                    t = neighbor.terrain
                    terrain_counts[t] = terrain_counts.get(t, 0) + 1

                # If isolated, become like neighbors
                if terrain_counts.get(cell.terrain, 0) <= 1:
                    most_common = max(terrain_counts.items(), key=lambda x: x[1])[0]
                    changes.append((cell.q, cell.r, most_common))

            # Apply changes
            for q, r, terrain in changes:
                cell = grid.get_cell(q, r)
                if cell:
                    cell.terrain = terrain

    def place_deployment_zones(
        self, grid: HexGrid
    ) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """
        Designate deployment zones for player and enemy.
        Ensures units spawn on valid terrain.

        Args:
            grid: Battle grid

        Returns:
            (player_zones, enemy_zones) lists of (q, r) positions
        """
        player_zones = []
        enemy_zones = []

        # Player deploys on left side (columns 0-2)
        for r in range(grid.height):
            for q in range(min(3, grid.width)):
                cell = grid.get_cell(q, r)
                if cell and cell.terrain not in ["mountains", "water"]:
                    player_zones.append((q, r))

        # Enemy deploys on right side (last 3 columns)
        for r in range(grid.height):
            for q in range(max(0, grid.width - 3), grid.width):
                cell = grid.get_cell(q, r)
                if cell and cell.terrain not in ["mountains", "water"]:
                    enemy_zones.append((q, r))

        return player_zones, enemy_zones

    def get_random_template(self) -> str:
        """Get a random map template for variety."""
        templates = [
            "plains_encounter",
            "forest_ambush",
            "mountain_pass",
            "river_crossing",
            "siege_battle",
        ]
        return random.choice(templates)
