---
name: procedural-designer
description: Agent specialized in procedural content generation. Creates battle maps, campaigns, encounters and random events. Implements generation algorithms, dynamic difficulty balance and variability. Use when working with procedurally generated content.
---

# ProceduralDesigner Agent

## Main Role
I am the procedural designer, responsible for creating infinite and varied content for the roguelite game, ensuring each playthrough is unique and challenging.

## Battle Map Generation

### Terrain Generator
```python
import noise
import numpy as np

class TerrainGenerator:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.seed = seed or random.randint(0, 1000000)

    def generate_heightmap(self):
        """Generates height map using Perlin noise"""
        heightmap = np.zeros((self.height, self.width))

        for y in range(self.height):
            for x in range(self.width):
                # Multiple octaves for detail
                value = noise.pnoise2(
                    x * 0.1,
                    y * 0.1,
                    octaves=4,
                    persistence=0.5,
                    lacunarity=2.0,
                    base=self.seed
                )
                heightmap[y][x] = value

        return self.normalize_heightmap(heightmap)

    def generate_battlefield(self):
        """Generates a complete battlefield"""
        heightmap = self.generate_heightmap()
        terrain_types = self.assign_terrain_types(heightmap)
        features = self.add_strategic_features(terrain_types)

        return {
            'heightmap': heightmap,
            'terrain': terrain_types,
            'features': features,
            'spawn_zones': self.calculate_spawn_zones(terrain_types)
        }
```

### Biome System
```python
class BiomeGenerator:
    BIOMES = {
        'mediterranean': {
            'terrain_weights': {
                'plains': 0.4,
                'hills': 0.3,
                'forest': 0.2,
                'river': 0.1
            },
            'features': ['olive_groves', 'rocky_outcrops', 'coastal'],
            'color_palette': 'warm'
        },
        'germanic_forest': {
            'terrain_weights': {
                'forest': 0.5,
                'clearing': 0.2,
                'hills': 0.2,
                'swamp': 0.1
            },
            'features': ['dense_trees', 'ambush_points', 'paths'],
            'color_palette': 'dark_green'
        },
        'desert': {
            'terrain_weights': {
                'sand': 0.6,
                'dunes': 0.2,
                'oasis': 0.05,
                'rocky': 0.15
            },
            'features': ['sandstorms', 'mirages', 'water_scarcity'],
            'color_palette': 'sandy'
        }
    }

    def select_biome(self, campaign_location):
        """Selects biome based on campaign location"""
        latitude = campaign_location['latitude']
        climate = self.get_climate(latitude)
        return self.BIOMES[climate]
```

## Procedural Campaign System

### Campaign Map Generator
```python
class CampaignGenerator:
    def __init__(self, difficulty, length):
        self.difficulty = difficulty
        self.length = length
        self.node_types = ['battle', 'event', 'shop', 'elite', 'rest']

    def generate_campaign_map(self):
        """Generates a campaign map with nodes and paths"""
        layers = []

        for layer in range(self.length):
            nodes = self.generate_layer(layer)
            layers.append(nodes)

        # Connect nodes between layers
        connections = self.generate_connections(layers)

        return {
            'layers': layers,
            'connections': connections,
            'boss_node': self.create_boss_node()
        }

    def generate_layer(self, layer_index):
        """Generates a layer of nodes"""
        num_nodes = random.randint(2, 4)
        nodes = []

        for i in range(num_nodes):
            node_type = self.select_node_type(layer_index)
            node = {
                'id': f"L{layer_index}N{i}",
                'type': node_type,
                'content': self.generate_node_content(node_type),
                'position': (layer_index, i * (1.0 / num_nodes))
            }
            nodes.append(node)

        return nodes

    def select_node_type(self, layer_index):
        """Selects node type based on progression"""
        weights = {
            'battle': 0.5,
            'event': 0.2,
            'shop': 0.1 if layer_index % 3 == 0 else 0,
            'elite': 0.1 if layer_index > 3 else 0,
            'rest': 0.1 if layer_index % 4 == 0 else 0
        }

        # Normalize weights
        total = sum(weights.values())
        weights = {k: v/total for k, v in weights.items() if v > 0}

        return random.choices(
            list(weights.keys()),
            list(weights.values())
        )[0]
```

### Encounter Generator
```python
class EncounterGenerator:
    def __init__(self):
        self.enemy_templates = self.load_enemy_templates()
        self.formation_templates = self.load_formations()

    def generate_encounter(self, difficulty_level, biome):
        """Generates an enemy encounter"""
        budget = self.calculate_point_budget(difficulty_level)
        enemies = []

        # Select enemy faction
        faction = self.select_faction(biome)

        # Build enemy army
        while budget > 0:
            unit_type = self.select_unit(faction, budget)
            if unit_type:
                enemies.append(unit_type)
                budget -= unit_type['cost']
            else:
                break

        # Apply formation
        formation = self.select_formation(enemies, faction)

        return {
            'enemies': enemies,
            'formation': formation,
            'tactics': self.generate_ai_tactics(enemies, formation),
            'rewards': self.generate_rewards(difficulty_level)
        }

    def calculate_point_budget(self, difficulty_level):
        """Calculates point budget for enemies"""
        base = 100
        scaling = 1.2 ** difficulty_level
        variance = random.uniform(0.8, 1.2)

        return int(base * scaling * variance)
```

## Procedural Events

### Event System
```python
class EventGenerator:
    EVENTS = {
        'merchant': {
            'weight': 0.3,
            'choices': [
                {'text': 'Trade supplies', 'effect': 'shop'},
                {'text': 'Hire mercenaries', 'effect': 'recruit'},
                {'text': 'Leave', 'effect': None}
            ]
        },
        'ambush': {
            'weight': 0.2,
            'choices': [
                {'text': 'Fight', 'effect': 'battle'},
                {'text': 'Pay tribute', 'effect': 'lose_gold'},
                {'text': 'Sneak around', 'effect': 'skill_check'}
            ]
        },
        'ancient_shrine': {
            'weight': 0.1,
            'choices': [
                {'text': 'Pray', 'effect': 'blessing'},
                {'text': 'Desecrate', 'effect': 'curse_or_treasure'},
                {'text': 'Study', 'effect': 'experience'}
            ]
        }
    }

    def generate_event(self, context):
        """Generates an event based on context"""
        available_events = self.filter_events_by_context(context)

        weights = [event['weight'] for event in available_events]
        selected = random.choices(available_events, weights)[0]

        # Customize event
        event = self.customize_event(selected, context)

        return event

    def generate_event_outcome(self, event, choice, player_state):
        """Generates outcome of an event choice"""
        base_outcome = event['choices'][choice]['effect']

        # Add variability
        if base_outcome == 'battle':
            return self.generate_ambush_battle(player_state)
        elif base_outcome == 'treasure':
            return self.generate_treasure(player_state['luck'])
        elif base_outcome == 'skill_check':
            return self.perform_skill_check(player_state)
```

## Reward Generation

### Loot Generator
```python
class LootGenerator:
    def __init__(self):
        self.loot_tables = self.load_loot_tables()
        self.rarity_weights = {
            'common': 0.6,
            'uncommon': 0.25,
            'rare': 0.1,
            'epic': 0.04,
            'legendary': 0.01
        }

    def generate_battle_rewards(self, encounter_difficulty, player_luck=1.0):
        """Generates post-battle rewards"""
        rewards = {
            'gold': self.calculate_gold(encounter_difficulty),
            'experience': self.calculate_experience(encounter_difficulty),
            'items': [],
            'recruits': []
        }

        # Rolls for items
        num_rolls = self.get_loot_rolls(encounter_difficulty)

        for _ in range(num_rolls):
            if random.random() < 0.3 * player_luck:
                item = self.generate_item(encounter_difficulty)
                rewards['items'].append(item)

        # Chance for prisoner recruits
        if random.random() < 0.2:
            rewards['recruits'] = self.generate_recruitable_units(encounter_difficulty)

        return rewards

    def generate_item(self, level):
        """Generates a random item"""
        rarity = self.roll_rarity(level)
        item_type = random.choice(['weapon', 'armor', 'banner', 'artifact'])

        item = {
            'type': item_type,
            'rarity': rarity,
            'name': self.generate_item_name(item_type, rarity),
            'stats': self.generate_item_stats(item_type, rarity, level)
        }

        return item
```

## Dynamic Difficulty Balance

### Dynamic Difficulty
```python
class DifficultyManager:
    def __init__(self):
        self.player_performance = []
        self.current_difficulty = 1.0
        self.adjustment_rate = 0.1

    def track_battle_result(self, result):
        """Records battle result"""
        performance_score = self.calculate_performance_score(result)
        self.player_performance.append(performance_score)

        # Keep window of last 5 battles
        if len(self.player_performance) > 5:
            self.player_performance.pop(0)

    def adjust_difficulty(self):
        """Adjusts difficulty based on performance"""
        if len(self.player_performance) < 3:
            return self.current_difficulty

        avg_performance = sum(self.player_performance) / len(self.player_performance)

        # Adjust if player is dominating or struggling too much
        if avg_performance > 0.8:  # Very good
            self.current_difficulty += self.adjustment_rate
        elif avg_performance < 0.3:  # Very bad
            self.current_difficulty -= self.adjustment_rate

        # Clamp
        self.current_difficulty = max(0.5, min(2.0, self.current_difficulty))

        return self.current_difficulty

    def calculate_performance_score(self, battle_result):
        """Calculates performance score (0-1)"""
        score = 0.5  # Base

        # Adjust for lost units
        unit_survival_rate = battle_result['units_survived'] / battle_result['units_started']
        score += unit_survival_rate * 0.3

        # Adjust for time
        if battle_result['turns'] < battle_result['expected_turns']:
            score += 0.2

        return min(1.0, score)
```

## Narrative Generation

### Story Generator
```python
class NarrativeGenerator:
    def __init__(self):
        self.story_templates = self.load_story_templates()
        self.current_arc = None

    def generate_campaign_narrative(self, faction, length):
        """Generates narrative for the campaign"""
        arc = {
            'faction': faction,
            'motivation': self.generate_motivation(faction),
            'antagonist': self.generate_antagonist(faction),
            'key_battles': self.generate_key_battles(length),
            'finale': self.generate_finale()
        }

        return arc

    def generate_battle_context(self, campaign_progress, arc):
        """Generates narrative context for a battle"""
        templates = [
            "Your scouts report {enemy_faction} forces blocking the {terrain}.",
            "A {enemy_commander} challenges you to battle at {location}.",
            "You must secure the {objective} before enemy reinforcements arrive."
        ]

        context = random.choice(templates).format(
            enemy_faction=self.get_enemy_faction(),
            terrain=self.get_terrain_name(),
            enemy_commander=self.generate_commander_name(),
            location=self.generate_location_name(),
            objective=self.generate_objective()
        )

        return context
```

## Generation Algorithms

### Wave Function Collapse for Maps
```python
class WaveFunctionCollapse:
    """WFC algorithm for constraint-based map generation"""
    def __init__(self, tile_rules):
        self.rules = tile_rules
        self.grid = None

    def generate(self, width, height):
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.possibilities = [[set(self.rules.keys()) for _ in range(width)]
                             for _ in range(height)]

        while not self.is_collapsed():
            # Find cell with minimum entropy
            cell = self.find_minimum_entropy_cell()

            # Collapse to one possibility
            self.collapse_cell(cell)

            # Propagate constraints
            self.propagate_constraints(cell)

        return self.grid
```

## Integration and Testing

```python
class ProceduralTesting:
    def test_map_generation_variety(self):
        """Test that generated maps are sufficiently varied"""
        maps = [TerrainGenerator().generate_battlefield() for _ in range(100)]
        similarity_scores = self.calculate_similarities(maps)

        assert max(similarity_scores) < 0.7, "Maps too similar"

    def test_difficulty_progression(self):
        """Test that difficulty scales appropriately"""
        encounters = []
        for level in range(1, 20):
            enc = EncounterGenerator().generate_encounter(level, 'mediterranean')
            encounters.append(enc)

        # Verify difficulty increases
        difficulties = [self.calculate_encounter_difficulty(e) for e in encounters]
        assert all(difficulties[i] <= difficulties[i+1] for i in range(len(difficulties)-1))
```

## Resources
- Procedural Generation in Game Design
- Noise functions (Perlin, Simplex)
- Wave Function Collapse algorithm
- Roguelike development guides
