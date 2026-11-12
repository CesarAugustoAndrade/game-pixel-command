---
name: procedural-generation
description: Comprehensive procedural content generation for roguelike games. Use when generating random maps, dungeons, campaigns, terrain with Perlin/Simplex noise, enemy placement, loot systems, difficulty scaling, event generation, or any procedural content for roguelike/roguelite games.
---

# Procedural Generation Skill

## Overview

Complete procedural generation system for roguelike games including terrain generation, enemy placement, loot systems, and campaign structure. Uses noise functions and balanced random algorithms.

## Noise-Based Terrain Generation

### Perlin Noise for Natural Terrain

```python
# terrain_generation.py
import noise
import numpy as np
from enum import Enum
from typing import List, Tuple
import random

class TerrainType(Enum):
    WATER = 0
    SAND = 1
    GRASS = 2
    FOREST = 3
    HILLS = 4
    MOUNTAINS = 5

class BiomeType(Enum):
    MEDITERRANEAN = "mediterranean"
    GERMANIC_FOREST = "germanic_forest"
    EGYPTIAN_DESERT = "egyptian_desert"
    PERSIAN_HIGHLANDS = "persian_highlands"
    STEPPE = "steppe"

class TerrainGenerator:
    def __init__(self, width: int, height: int, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
    
    def generate_heightmap(self, octaves: int = 6, persistence: float = 0.5,
                          lacunarity: float = 2.0, scale: float = 100.0) -> np.ndarray:
        """
        Generate heightmap using Perlin noise
        
        octaves: Number of noise layers (more = more detail)
        persistence: Amplitude decrease per octave (lower = smoother)
        lacunarity: Frequency increase per octave (higher = more varied)
        scale: Overall zoom level (higher = more zoomed out)
        """
        heightmap = np.zeros((self.height, self.width))
        
        for y in range(self.height):
            for x in range(self.width):
                value = noise.pnoise2(
                    x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=self.width,
                    repeaty=self.height,
                    base=self.seed
                )
                # Normalize to 0-1 range
                heightmap[y][x] = (value + 1) / 2
        
        return heightmap
    
    def heightmap_to_terrain(self, heightmap: np.ndarray) -> np.ndarray:
        """Convert heightmap to discrete terrain types"""
        terrain = np.zeros((self.height, self.width), dtype=int)
        
        for y in range(self.height):
            for x in range(self.width):
                h = heightmap[y][x]
                
                if h < 0.3:
                    terrain[y][x] = TerrainType.WATER.value
                elif h < 0.4:
                    terrain[y][x] = TerrainType.SAND.value
                elif h < 0.6:
                    terrain[y][x] = TerrainType.GRASS.value
                elif h < 0.75:
                    terrain[y][x] = TerrainType.FOREST.value
                elif h < 0.85:
                    terrain[y][x] = TerrainType.HILLS.value
                else:
                    terrain[y][x] = TerrainType.MOUNTAINS.value
        
        return terrain
    
    def generate_biome_map(self, temperature_scale: float = 150.0,
                          moisture_scale: float = 150.0) -> np.ndarray:
        """
        Generate biome map using temperature and moisture
        """
        temperature = self.generate_heightmap(
            octaves=4, 
            scale=temperature_scale,
            persistence=0.6
        )
        
        moisture = self.generate_heightmap(
            octaves=4,
            scale=moisture_scale,
            persistence=0.6
        )
        
        biomes = np.zeros((self.height, self.width), dtype=object)
        
        for y in range(self.height):
            for x in range(self.width):
                t = temperature[y][x]
                m = moisture[y][x]
                
                if t > 0.7:  # Hot
                    if m < 0.3:
                        biomes[y][x] = BiomeType.EGYPTIAN_DESERT
                    else:
                        biomes[y][x] = BiomeType.MEDITERRANEAN
                elif t > 0.4:  # Temperate
                    if m < 0.4:
                        biomes[y][x] = BiomeType.STEPPE
                    else:
                        biomes[y][x] = BiomeType.GERMANIC_FOREST
                else:  # Cold
                    biomes[y][x] = BiomeType.PERSIAN_HIGHLANDS
        
        return biomes
    
    def apply_erosion(self, heightmap: np.ndarray, iterations: int = 5) -> np.ndarray:
        """
        Simulate erosion for more natural terrain
        """
        eroded = heightmap.copy()
        
        for _ in range(iterations):
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    # Get neighbors
                    neighbors = [
                        eroded[y-1][x], eroded[y+1][x],
                        eroded[y][x-1], eroded[y][x+1]
                    ]
                    
                    avg = sum(neighbors) / len(neighbors)
                    
                    # Smooth towards average
                    eroded[y][x] = eroded[y][x] * 0.7 + avg * 0.3
        
        return eroded
    
    def place_rivers(self, heightmap: np.ndarray, num_rivers: int = 3) -> List[List[Tuple[int, int]]]:
        """
        Generate rivers from high to low elevation
        """
        rivers = []
        
        for _ in range(num_rivers):
            # Start at random high point
            high_points = np.where(heightmap > 0.7)
            if len(high_points[0]) == 0:
                continue
            
            idx = random.randint(0, len(high_points[0]) - 1)
            y, x = high_points[0][idx], high_points[1][idx]
            
            river = [(x, y)]
            visited = {(x, y)}
            
            # Flow downhill
            for _ in range(100):  # Max river length
                # Find lowest neighbor
                neighbors = [
                    (x-1, y), (x+1, y), (x, y-1), (x, y+1),
                    (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)
                ]
                
                valid_neighbors = [
                    (nx, ny) for nx, ny in neighbors
                    if 0 <= nx < self.width and 0 <= ny < self.height
                    and (nx, ny) not in visited
                ]
                
                if not valid_neighbors:
                    break
                
                # Move to lowest neighbor with some randomness
                lowest = min(valid_neighbors, key=lambda p: heightmap[p[1]][p[0]])
                if random.random() < 0.8:  # 80% follow lowest
                    x, y = lowest
                else:  # 20% random for natural variation
                    x, y = random.choice(valid_neighbors)
                
                river.append((x, y))
                visited.add((x, y))
                
                # Stop at water
                if heightmap[y][x] < 0.3:
                    break
            
            rivers.append(river)
        
        return rivers
```

### Cellular Automata for Caves/Forests

```python
# cellular_automata.py

class CellularAutomata:
    def __init__(self, width: int, height: int, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        self.grid = None
    
    def generate_cave(self, fill_probability: float = 0.45, 
                     iterations: int = 5) -> np.ndarray:
        """
        Generate cave-like structures using cellular automata
        """
        # Initialize with random noise
        self.grid = np.random.random((self.height, self.width)) < fill_probability
        
        # Apply CA rules
        for _ in range(iterations):
            self.grid = self._apply_cave_rules(self.grid)
        
        return self.grid
    
    def _apply_cave_rules(self, grid: np.ndarray) -> np.ndarray:
        """
        CA rules: cell becomes wall if 5+ neighbors are walls
        """
        new_grid = grid.copy()
        
        for y in range(self.height):
            for x in range(self.width):
                wall_count = self._count_walls(grid, x, y, 1)
                
                if wall_count >= 5:
                    new_grid[y][x] = True
                else:
                    new_grid[y][x] = False
        
        return new_grid
    
    def _count_walls(self, grid: np.ndarray, x: int, y: int, radius: int) -> int:
        """Count wall tiles in radius"""
        count = 0
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                
                # Out of bounds = wall
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                    count += 1
                elif grid[ny][nx]:
                    count += 1
        
        return count
    
    def generate_forest_patches(self, density: float = 0.3,
                               iterations: int = 3) -> np.ndarray:
        """
        Generate clustered forest areas
        """
        self.grid = np.random.random((self.height, self.width)) < density
        
        for _ in range(iterations):
            new_grid = self.grid.copy()
            
            for y in range(self.height):
                for x in range(self.width):
                    neighbors = self._count_walls(self.grid, x, y, 1)
                    
                    # Grow forests where neighbors exist
                    if neighbors >= 4:
                        new_grid[y][x] = True
                    elif neighbors <= 2:
                        new_grid[y][x] = False
            
            self.grid = new_grid
        
        return self.grid
```

## Campaign Generation

### Node-Based Campaign Structure

```python
# campaign_generation.py
from dataclasses import dataclass
from typing import List, Dict, Set, Optional
from enum import Enum

class NodeType(Enum):
    BATTLE = "battle"
    ELITE_BATTLE = "elite_battle"
    BOSS = "boss"
    MERCHANT = "merchant"
    REST = "rest"
    EVENT = "event"
    TREASURE = "treasure"

@dataclass
class CampaignNode:
    id: int
    type: NodeType
    level: int  # Depth in campaign
    connections: List[int]  # IDs of connected nodes
    difficulty: int
    rewards: Dict[str, any]
    completed: bool = False

class CampaignGenerator:
    def __init__(self, seed: int = None):
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        self.nodes: Dict[int, CampaignNode] = {}
        self.next_id = 0
    
    def generate_campaign(self, depth: int = 15, 
                         width_min: int = 3, 
                         width_max: int = 5) -> Dict[int, CampaignNode]:
        """
        Generate branching campaign structure
        
        Returns dict of node_id -> CampaignNode
        """
        self.nodes.clear()
        self.next_id = 0
        
        # Create start node
        start_node = self._create_node(NodeType.REST, 0, 1)
        prev_level_nodes = [start_node.id]
        
        # Generate levels
        for level in range(1, depth):
            # Determine width for this level
            width = random.randint(width_min, width_max)
            
            # Boss level has single node
            if level == depth - 1:
                width = 1
                node_type = NodeType.BOSS
            else:
                node_type = None  # Will be determined randomly
            
            # Create nodes for this level
            current_level_nodes = []
            for _ in range(width):
                if node_type is None:
                    chosen_type = self._choose_node_type(level, depth)
                else:
                    chosen_type = node_type
                
                difficulty = self._calculate_difficulty(level, depth)
                node = self._create_node(chosen_type, level, difficulty)
                current_level_nodes.append(node.id)
            
            # Connect to previous level
            self._connect_levels(prev_level_nodes, current_level_nodes)
            
            prev_level_nodes = current_level_nodes
        
        return self.nodes
    
    def _create_node(self, node_type: NodeType, level: int, difficulty: int) -> CampaignNode:
        """Create new campaign node"""
        node = CampaignNode(
            id=self.next_id,
            type=node_type,
            level=level,
            connections=[],
            difficulty=difficulty,
            rewards=self._generate_rewards(node_type, level, difficulty)
        )
        
        self.nodes[self.next_id] = node
        self.next_id += 1
        
        return node
    
    def _choose_node_type(self, level: int, max_depth: int) -> NodeType:
        """Choose node type based on level and probabilities"""
        # Define probabilities
        weights = {
            NodeType.BATTLE: 50,
            NodeType.ELITE_BATTLE: 10 if level > 3 else 0,
            NodeType.MERCHANT: 15,
            NodeType.REST: 10,
            NodeType.EVENT: 12,
            NodeType.TREASURE: 3
        }
        
        # Increase elite battles in later levels
        if level > max_depth * 0.6:
            weights[NodeType.ELITE_BATTLE] += 10
        
        # Force rest sites periodically
        if level % 5 == 0:
            return NodeType.REST
        
        return random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
    
    def _calculate_difficulty(self, level: int, max_depth: int) -> int:
        """Calculate difficulty (1-10) based on progression"""
        base_difficulty = 1 + (level / max_depth) * 9
        variance = random.uniform(-0.5, 0.5)
        
        return max(1, min(10, int(base_difficulty + variance)))
    
    def _generate_rewards(self, node_type: NodeType, level: int, difficulty: int) -> Dict:
        """Generate rewards for node"""
        rewards = {
            'gold': 0,
            'items': [],
            'experience': 0
        }
        
        if node_type == NodeType.BATTLE:
            rewards['gold'] = random.randint(10, 30) * level
            rewards['experience'] = 50 * level
            if random.random() < 0.3:  # 30% chance for item
                rewards['items'].append(self._generate_item(level))
        
        elif node_type == NodeType.ELITE_BATTLE:
            rewards['gold'] = random.randint(30, 60) * level
            rewards['experience'] = 100 * level
            rewards['items'].append(self._generate_item(level, rare=True))
        
        elif node_type == NodeType.BOSS:
            rewards['gold'] = 500 * level
            rewards['experience'] = 500 * level
            rewards['items'].extend([
                self._generate_item(level, rare=True),
                self._generate_item(level, rare=True)
            ])
        
        elif node_type == NodeType.TREASURE:
            rewards['gold'] = random.randint(50, 100) * level
            rewards['items'].append(self._generate_item(level))
        
        return rewards
    
    def _generate_item(self, level: int, rare: bool = False) -> Dict:
        """Generate random item"""
        rarity_roll = random.random()
        
        if rare or rarity_roll > 0.8:
            rarity = "epic"
            power = level * random.uniform(1.5, 2.0)
        elif rarity_roll > 0.5:
            rarity = "rare"
            power = level * random.uniform(1.0, 1.5)
        else:
            rarity = "common"
            power = level * random.uniform(0.8, 1.2)
        
        return {
            'name': f"Item_L{level}",
            'rarity': rarity,
            'power': int(power),
            'type': random.choice(['weapon', 'armor', 'artifact'])
        }
    
    def _connect_levels(self, prev_nodes: List[int], current_nodes: List[int]):
        """Connect previous level to current level"""
        # Each current node connects to 1-2 previous nodes
        for current_id in current_nodes:
            num_connections = random.randint(1, min(2, len(prev_nodes)))
            connected_prev = random.sample(prev_nodes, num_connections)
            
            for prev_id in connected_prev:
                self.nodes[prev_id].connections.append(current_id)
```

## Enemy Placement

### Weighted Random Spawning

```python
# enemy_spawning.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class EnemyTemplate:
    name: str
    level_min: int
    level_max: int
    weight: int  # Spawn probability weight
    strength: int
    group_size_min: int
    group_size_max: int
    biome_affinity: List[BiomeType]

class EnemySpawner:
    def __init__(self):
        self.enemy_templates = self._create_enemy_templates()
    
    def _create_enemy_templates(self) -> List[EnemyTemplate]:
        """Define enemy types"""
        return [
            EnemyTemplate(
                name="Greek Hoplite",
                level_min=1,
                level_max=5,
                weight=30,
                strength=3,
                group_size_min=3,
                group_size_max=6,
                biome_affinity=[BiomeType.MEDITERRANEAN, BiomeType.GERMANIC_FOREST]
            ),
            EnemyTemplate(
                name="Persian Immortal",
                level_min=3,
                level_max=8,
                weight=20,
                strength=5,
                group_size_min=2,
                group_size_max=4,
                biome_affinity=[BiomeType.PERSIAN_HIGHLANDS, BiomeType.STEPPE]
            ),
            EnemyTemplate(
                name="Roman Legionary",
                level_min=4,
                level_max=10,
                weight=25,
                strength=6,
                group_size_min=4,
                group_size_max=8,
                biome_affinity=[BiomeType.MEDITERRANEAN, BiomeType.GERMANIC_FOREST]
            ),
            EnemyTemplate(
                name="Egyptian Archer",
                level_min=2,
                level_max=7,
                weight=25,
                strength=4,
                group_size_min=3,
                group_size_max=5,
                biome_affinity=[BiomeType.EGYPTIAN_DESERT, BiomeType.MEDITERRANEAN]
            ),
            EnemyTemplate(
                name="Barbarian Berserker",
                level_min=5,
                level_max=12,
                weight=15,
                strength=8,
                group_size_min=2,
                group_size_max=3,
                biome_affinity=[BiomeType.GERMANIC_FOREST, BiomeType.STEPPE]
            )
        ]
    
    def spawn_enemies(self, battle_level: int, biome: BiomeType, 
                     difficulty_modifier: float = 1.0) -> List[Dict]:
        """
        Generate enemy group for battle
        
        Returns list of enemy dicts with type, position, stats
        """
        # Filter valid enemies for this level and biome
        valid_enemies = [
            e for e in self.enemy_templates
            if e.level_min <= battle_level <= e.level_max
            and biome in e.biome_affinity
        ]
        
        if not valid_enemies:
            # Fallback to any level-appropriate enemies
            valid_enemies = [
                e for e in self.enemy_templates
                if e.level_min <= battle_level <= e.level_max
            ]
        
        # Calculate total enemy strength budget
        strength_budget = int(battle_level * 10 * difficulty_modifier)
        
        # Select enemies within budget
        enemies = []
        while strength_budget > 0 and valid_enemies:
            # Weighted random selection
            enemy_type = random.choices(
                valid_enemies,
                weights=[e.weight for e in valid_enemies]
            )[0]
            
            # Determine group size
            group_size = random.randint(
                enemy_type.group_size_min,
                enemy_type.group_size_max
            )
            
            # Check if we can afford this group
            group_strength = enemy_type.strength * group_size
            if group_strength > strength_budget * 1.2:
                # Try smaller group or different enemy
                group_size = max(1, strength_budget // enemy_type.strength)
                if group_size == 0:
                    break
            
            # Add enemies to group
            for _ in range(group_size):
                enemies.append({
                    'type': enemy_type.name,
                    'level': battle_level,
                    'strength': enemy_type.strength
                })
                strength_budget -= enemy_type.strength
        
        return enemies
    
    def place_on_grid(self, enemies: List[Dict], grid: HexGrid, 
                     deployment_zone: List[Hex]) -> Dict[Hex, Dict]:
        """
        Place enemies on battlefield grid
        
        Returns dict of Hex -> enemy dict
        """
        placements = {}
        available_positions = deployment_zone.copy()
        random.shuffle(available_positions)
        
        for enemy, pos in zip(enemies, available_positions):
            if grid.is_walkable(pos):
                placements[pos] = enemy
        
        return placements
```

## Difficulty Scaling

### Adaptive Difficulty System

```python
# difficulty_scaling.py

class DifficultyManager:
    def __init__(self):
        self.player_performance = {
            'battles_won': 0,
            'battles_lost': 0,
            'average_health_remaining': 1.0,
            'turns_per_battle': [],
            'units_lost': 0
        }
        self.current_modifier = 1.0
    
    def record_battle(self, won: bool, health_remaining: float, 
                     turns: int, units_lost: int):
        """Record battle results"""
        if won:
            self.player_performance['battles_won'] += 1
        else:
            self.player_performance['battles_lost'] += 1
        
        self.player_performance['average_health_remaining'] = (
            self.player_performance['average_health_remaining'] * 0.7 +
            health_remaining * 0.3
        )
        self.player_performance['turns_per_battle'].append(turns)
        self.player_performance['units_lost'] += units_lost
        
        self._update_difficulty()
    
    def _update_difficulty(self):
        """Adjust difficulty based on performance"""
        total_battles = (self.player_performance['battles_won'] + 
                        self.player_performance['battles_lost'])
        
        if total_battles < 3:
            return  # Not enough data
        
        win_rate = self.player_performance['battles_won'] / total_battles
        
        # Adjust based on win rate
        if win_rate > 0.8:
            # Player winning too easily
            self.current_modifier = min(1.5, self.current_modifier + 0.05)
        elif win_rate < 0.4:
            # Player struggling
            self.current_modifier = max(0.5, self.current_modifier - 0.05)
        
        # Consider health remaining
        if self.player_performance['average_health_remaining'] > 0.8:
            self.current_modifier = min(1.5, self.current_modifier + 0.02)
        elif self.player_performance['average_health_remaining'] < 0.3:
            self.current_modifier = max(0.5, self.current_modifier - 0.02)
    
    def get_difficulty_modifier(self) -> float:
        """Get current difficulty multiplier"""
        return self.current_modifier
    
    def get_scaled_stats(self, base_stats: Dict) -> Dict:
        """Apply difficulty scaling to enemy stats"""
        return {
            key: int(value * self.current_modifier)
            for key, value in base_stats.items()
        }
```

## Best Practices

1. **Seed everything**: Allow replay of same generated content
2. **Test extremes**: Verify generation at min/max parameters
3. **Balance rewards**: Use spreadsheets to model economy
4. **Preview generation**: Add debug visualization
5. **Layer noise**: Combine multiple noise layers for complexity
6. **Clamp values**: Prevent impossible/broken results
7. **Performance**: Cache generated content, don't regenerate
8. **Variety**: Add random variation to prevent repetition

This system provides robust procedural generation with natural-looking results and balanced gameplay.
