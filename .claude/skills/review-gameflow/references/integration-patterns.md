# Integration Patterns for Classical Army Roguelite

This reference provides common patterns for integrating game systems together.

## Table of Contents
1. [State-to-State Data Passing](#state-to-state-data-passing)
2. [Event-Driven Communication](#event-driven-communication)
3. [Component-Based Entity Modifications](#component-based-entity-modifications)
4. [Procedural Content Integration](#procedural-content-integration)
5. [UI-to-Game-Logic Connections](#ui-to-game-logic-connections)
6. [Save/Load Integration](#saveload-integration)
7. [Equipment System Integration](#equipment-system-integration)
8. [AI Integration Patterns](#ai-integration-patterns)

---

## State-to-State Data Passing

### Pattern: Constructor Data Injection

The most direct way to pass data between states when transitioning.

**When to use:**
- Transitioning from Campaign Map to Battle
- Passing battle results back to Campaign Map
- Sharing player army across states

**Example: Campaign Map → Battle State**

```python
# In campaign_map.py
def _trigger_encounter(self):
    """Trigger a battle encounter."""
    # Generate enemy army
    enemy_army = self.encounter_generator.generate_encounter(
        difficulty=self.difficulty_level,
        is_elite=random.random() < 0.1
    )

    # Create battle state with both armies
    from src.states.battle import BattleState
    battle_state = BattleState(
        self.state_manager,
        self.engine,
        player_army=self.player_army,
        enemy_army=enemy_army,
        battle_difficulty=self.difficulty_level
    )

    # Push battle state
    self.state_manager.push_state(battle_state)
```

**Example: Battle → Campaign Map (Return Results)**

```python
# In battle.py
def _end_battle(self, result: str):
    """End battle and return to campaign map."""
    self.battle_result = result

    # Calculate rewards
    self.rewards = calculate_battle_rewards(
        difficulty=self.battle_difficulty,
        is_elite=self.is_elite,
        is_boss=self.is_boss,
        casualties=self.player_casualties,
        starting_strength=self.player_starting_strength
    )

    # Pop back to campaign map
    # The campaign map can access self.player_army which was modified
    self.state_manager.pop_state()

# In campaign_map.py
def on_resume(self):
    """Called when returning from battle."""
    super().on_resume()

    # Check if we just returned from battle
    # Access battle results if available
    # Apply rewards to player army
    pass
```

**Better Pattern: Callback Functions**

```python
# In campaign_map.py
def _trigger_encounter(self):
    """Trigger a battle encounter."""
    enemy_army = self.encounter_generator.generate_encounter(
        difficulty=self.difficulty_level
    )

    battle_state = BattleState(
        self.state_manager,
        self.engine,
        player_army=self.player_army,
        enemy_army=enemy_army,
        on_battle_end=self._on_battle_complete  # Callback
    )

    self.state_manager.push_state(battle_state)

def _on_battle_complete(self, result: str, rewards: dict):
    """Handle battle completion."""
    if result == "victory":
        self._apply_rewards(rewards)
        self.difficulty_level += 1
    elif result == "defeat":
        # Handle defeat
        pass
```

---

## Event-Driven Communication

### Pattern: Event System for Loose Coupling

Use events when systems need to react to actions without direct references.

**When to use:**
- Combat events (unit died, morale changed)
- Achievement triggers
- UI updates from game state changes
- Audio cues

**Example: Morale Change Event**

```python
# In combat_calculator.py
def calculate_damage(self, attacker, defender, terrain):
    """Calculate damage and emit events."""
    damage = self._calculate_base_damage(attacker, defender)

    # Apply damage
    defender.hp -= damage

    # Emit event for other systems to react
    self.event_system.emit("unit_damaged", {
        "unit": defender,
        "damage": damage,
        "attacker": attacker
    })

    if defender.hp <= 0:
        self.event_system.emit("unit_died", {
            "unit": defender,
            "killer": attacker
        })

# In morale_system.py
def __init__(self, event_system):
    self.event_system = event_system

    # Subscribe to relevant events
    self.event_system.subscribe("unit_died", self._on_unit_died)
    self.event_system.subscribe("unit_damaged", self._on_unit_damaged)

def _on_unit_died(self, event_data):
    """React to unit death - affect nearby unit morale."""
    dead_unit = event_data["unit"]

    # Find nearby allies and reduce their morale
    for unit in self._find_nearby_units(dead_unit, same_faction=True):
        self.modify_morale(unit, -10)

# In ui_manager.py (hypothetical)
def __init__(self, event_system):
    self.event_system = event_system

    # Subscribe to events for UI updates
    self.event_system.subscribe("unit_damaged", self._show_damage_number)
    self.event_system.subscribe("morale_changed", self._update_morale_bar)

def _show_damage_number(self, event_data):
    """Display floating damage number."""
    damage = event_data["damage"]
    unit = event_data["unit"]
    # Create floating text effect
    pass
```

**Benefits:**
- Decoupled systems
- Easy to add new reactions to events
- No circular dependencies

---

## Component-Based Entity Modifications

### Pattern: Component Queries and Modifications

When working with entities that have components.

**When to use:**
- Applying equipment bonuses
- Status effects
- Buff/debuff systems

**Example: Equipment Bonuses in Combat**

```python
# In combat_calculator.py
def calculate_damage(self, attacker: Unit, defender: Unit, terrain):
    """Calculate damage with equipment bonuses."""
    base_attack = attacker.attack

    # Query equipment component for bonuses
    if hasattr(attacker, 'equipment') and attacker.equipment:
        equipment_bonus = attacker.equipment.get_stat_bonus('attack')
        base_attack += equipment_bonus

    base_defense = defender.defense

    if hasattr(defender, 'equipment') and defender.equipment:
        equipment_bonus = defender.equipment.get_stat_bonus('defense')
        base_defense += equipment_bonus

    # Continue with damage calculation
    damage = max(1, base_attack - base_defense)

    return damage
```

**Example: Status Effect System**

```python
# In unit.py
class Unit(Entity):
    def __init__(self, ...):
        super().__init__()
        self.status_effects = []  # List of active effects

    def get_effective_stat(self, stat_name: str) -> int:
        """Get stat value with all modifiers applied."""
        base_value = getattr(self, stat_name, 0)

        # Apply equipment bonuses
        if hasattr(self, 'equipment') and self.equipment:
            base_value += self.equipment.get_stat_bonus(stat_name)

        # Apply status effect modifiers
        for effect in self.status_effects:
            base_value = effect.modify_stat(stat_name, base_value)

        return base_value

# In combat_calculator.py
def calculate_damage(self, attacker, defender, terrain):
    """Calculate damage using effective stats."""
    attack = attacker.get_effective_stat('attack')
    defense = defender.get_effective_stat('defense')

    damage = max(1, attack - defense)
    return damage
```

---

## Procedural Content Integration

### Pattern: Generator → Game State Integration

Connecting procedural generation to game states.

**When to use:**
- Generating battle maps
- Creating encounters
- Spawning items/rewards

**Example: Battle Map Generation Integration**

```python
# In battle.py
def _initialize_battle_map(self):
    """Generate and initialize battle map."""
    from src.procgen.battle_map_generator import BattleMapGenerator

    # Create generator
    map_gen = BattleMapGenerator(
        grid_width=self.grid.width,
        grid_height=self.grid.height
    )

    # Generate terrain data
    terrain_data = map_gen.generate_map(
        biome="plains",
        difficulty=self.battle_difficulty
    )

    # Apply terrain to hex grid
    for (q, r), terrain_type in terrain_data.items():
        cell = self.grid.get_cell(q, r)
        if cell:
            cell.terrain = terrain_type

    # Get strategic positions from generator
    player_spawn = map_gen.get_player_spawn_area()
    enemy_spawn = map_gen.get_enemy_spawn_area()

    # Use for unit deployment
    self._deploy_units(self.player_army, player_spawn)
    self._deploy_units(self.enemy_army, enemy_spawn)
```

**Example: Loot Integration**

```python
# In battle.py
def _calculate_rewards(self):
    """Calculate and generate battle rewards."""
    from src.procgen.loot_tables import calculate_battle_rewards
    from src.procgen.item_generator import ItemGenerator

    # Calculate base rewards
    rewards = calculate_battle_rewards(
        difficulty=self.battle_difficulty,
        is_elite=self.is_elite,
        casualties=self.player_casualties,
        starting_strength=self.player_starting_strength
    )

    # Generate item drops
    if rewards['item_drops'] > 0:
        item_gen = ItemGenerator()
        rewards['items'] = []

        for _ in range(rewards['item_drops']):
            item = item_gen.generate_item(
                level=self.battle_difficulty,
                rarity_bias=rewards.get('rarity_bonus', 0)
            )
            rewards['items'].append(item)

    return rewards

def _apply_rewards_to_army(self, rewards: dict):
    """Apply rewards to player army."""
    # Add gold
    self.player_army.gold += rewards.get('gold', 0)

    # Add XP to units
    xp_per_unit = rewards.get('xp', 0) // len(self.player_army.units)
    for unit in self.player_army.units:
        unit.add_experience(xp_per_unit)

    # Add items to inventory
    for item in rewards.get('items', []):
        self.player_army.add_item_to_inventory(item)

    # Add recruited units
    for unit_type in rewards.get('recruits', []):
        new_unit = self._create_unit_from_type(unit_type)
        self.player_army.add_unit(new_unit)
```

---

## UI-to-Game-Logic Connections

### Pattern: UI Event Handlers

Connecting UI widgets to game logic.

**When to use:**
- Button clicks
- Menu selections
- Interactive UI elements

**Example: Army Management UI Integration**

```python
# In army_management.py
def _create_equipment_ui(self):
    """Create UI for equipment management."""
    from src.ui.button import Button

    # Create equipment slot buttons
    for slot_name in ["weapon", "armor", "accessory"]:
        slot_button = Button(
            x=100, y=100,
            width=120, height=40,
            text=slot_name.capitalize(),
            on_click=lambda s=slot_name: self._on_equipment_slot_click(s)
        )
        self.equipment_buttons[slot_name] = slot_button

    # Create item buttons from inventory
    self._refresh_inventory_ui()

def _on_equipment_slot_click(self, slot_name: str):
    """Handle equipment slot click."""
    if self.selected_unit:
        current_item = self.selected_unit.equipment.get_slot(slot_name)

        # Show item selection dialog
        self._show_item_selector(
            slot_name,
            on_select=lambda item: self._equip_item(slot_name, item)
        )

def _equip_item(self, slot_name: str, item):
    """Equip item to unit."""
    if self.selected_unit:
        # Unequip current item (back to inventory)
        old_item = self.selected_unit.equipment.unequip(slot_name)
        if old_item:
            self.player_army.add_item_to_inventory(old_item)

        # Equip new item
        self.selected_unit.equipment.equip(slot_name, item)

        # Remove from inventory
        self.player_army.remove_item_from_inventory(item)

        # Refresh UI
        self._refresh_equipment_ui()
        self._refresh_unit_stats_ui()
```

**Example: Battle UI Integration**

```python
# In battle.py
def _handle_hex_click(self, hex_pos: Tuple[int, int]):
    """Handle hex grid click."""
    if self.selected_unit:
        # Check if clicked hex is a valid move destination
        if hex_pos in self.reachable_cells:
            self._move_unit(self.selected_unit, hex_pos)

        # Check if clicked hex has an enemy to attack
        elif hex_pos in self._get_attackable_positions():
            target = self._get_unit_at_position(hex_pos)
            if target and target.faction != self.selected_unit.faction:
                self._attack_unit(self.selected_unit, target)
    else:
        # Try to select unit at clicked hex
        unit = self._get_unit_at_position(hex_pos)
        if unit and self._can_select_unit(unit):
            self._select_unit(unit)

def _select_unit(self, unit: Unit):
    """Select a unit and show movement/attack options."""
    self.selected_unit = unit

    # Calculate reachable cells
    self.reachable_cells = self.pathfinder.get_reachable_cells(
        unit.position,
        unit.movement_range
    )

    # Calculate attack targets
    self.targets_in_range = self._get_units_in_range(
        unit.position,
        unit.attack_range,
        enemy_only=True
    )

    # Trigger UI update
    self.event_system.emit("unit_selected", {"unit": unit})
```

---

## Save/Load Integration

### Pattern: Serialization with State Managers

**When to use:**
- Implementing save/load system
- Preserving game state between sessions

**Example: Serializable Army**

```python
# In army.py
class Army:
    def to_dict(self) -> dict:
        """Convert army to serializable dictionary."""
        return {
            "faction": self.faction,
            "commander": self.commander.to_dict() if self.commander else None,
            "units": [unit.to_dict() for unit in self.units],
            "gold": self.gold,
            "inventory": [item.to_dict() for item in self.inventory],
            "position": self.position
        }

    @staticmethod
    def from_dict(data: dict) -> 'Army':
        """Create army from dictionary."""
        army = Army(faction=data["faction"])

        if data["commander"]:
            from src.entities.commander import Commander
            army.commander = Commander.from_dict(data["commander"])

        for unit_data in data["units"]:
            from src.entities.unit import Unit
            unit = Unit.from_dict(unit_data)
            army.add_unit(unit)

        army.gold = data["gold"]

        for item_data in data["inventory"]:
            from src.entities.equipment_system import Item
            item = Item.from_dict(item_data)
            army.add_item_to_inventory(item)

        army.position = data["position"]

        return army

# In campaign_map.py
def save_game(self, save_file: str):
    """Save current game state."""
    save_data = {
        "version": "1.0",
        "player_army": self.player_army.to_dict(),
        "player_position": self.player_position,
        "difficulty_level": self.difficulty_level,
        "total_steps": self.total_steps,
        "map_seed": self.map_generator.seed,
        "timestamp": time.time()
    }

    with open(save_file, 'w') as f:
        json.dump(save_data, f, indent=2)

def load_game(self, save_file: str):
    """Load game state."""
    with open(save_file, 'r') as f:
        save_data = json.load(f)

    # Restore player army
    from src.entities.army import Army
    self.player_army = Army.from_dict(save_data["player_army"])

    # Restore game state
    self.player_position = save_data["player_position"]
    self.difficulty_level = save_data["difficulty_level"]
    self.total_steps = save_data["total_steps"]

    # Regenerate map with same seed
    self.map_generator.seed = save_data["map_seed"]
    self._generate_map()
```

---

## Equipment System Integration

### Pattern: Equipment Effects in Combat

**Current Gap:** Equipment system exists but bonuses not applied in combat.

**Implementation:**

```python
# In entities/unit.py
class Unit(Entity):
    def get_combat_stat(self, stat_name: str) -> int:
        """Get stat value for combat calculations."""
        # Base stat
        base_value = getattr(self, stat_name, 0)

        # Add equipment bonuses
        if hasattr(self, 'equipment') and self.equipment:
            bonus = self.equipment.get_total_bonus(stat_name)
            base_value += bonus

        # Add commander aura bonuses
        if self.army and self.army.commander:
            aura_bonus = self.army.commander.get_aura_bonus(stat_name)
            base_value += aura_bonus

        # Add formation bonuses
        if self.formation:
            formation_bonus = self.formation.get_stat_bonus(stat_name)
            base_value += formation_bonus

        return base_value

# In battle/combat_calculator.py
def calculate_damage(self, attacker: Unit, defender: Unit, terrain, flanking=False):
    """Calculate damage with all modifiers."""
    # Use combat stats instead of raw stats
    attack = attacker.get_combat_stat('attack')
    defense = defender.get_combat_stat('defense')

    # Terrain modifier
    if terrain == "hills":
        defense *= 1.2

    # Flanking bonus
    if flanking:
        attack *= 1.5

    damage = max(1, int(attack - defense))
    return damage
```

---

## AI Integration Patterns

### Pattern: AI System Using Game State

**When to use:**
- Enemy AI decision-making
- Tactical AI for units

**Example: AI System Integration**

```python
# In entities/systems.py
class AISystem:
    def process_unit_turn(self, unit: Unit, game_state):
        """Process AI turn for a unit."""
        # Gather information from game state
        grid = game_state.grid
        enemies = game_state.get_enemy_units(unit.faction)
        allies = game_state.get_friendly_units(unit.faction)

        # Make tactical decision
        action = self._decide_action(unit, enemies, allies, grid)

        # Execute action
        if action["type"] == "move_and_attack":
            target = action["target"]
            move_pos = self._find_best_attack_position(unit, target, grid)

            # Move unit
            game_state.move_unit(unit, move_pos)

            # Attack target
            game_state.attack(unit, target)

        elif action["type"] == "retreat":
            safe_pos = self._find_safe_position(unit, enemies, grid)
            game_state.move_unit(unit, safe_pos)

    def _decide_action(self, unit, enemies, allies, grid):
        """Decide best action using utility AI."""
        # Calculate utility scores for different actions
        best_action = None
        best_score = -float('inf')

        # Consider attacking each enemy
        for enemy in enemies:
            if self._can_reach_and_attack(unit, enemy, grid):
                score = self._evaluate_attack(unit, enemy, allies)
                if score > best_score:
                    best_score = score
                    best_action = {
                        "type": "move_and_attack",
                        "target": enemy
                    }

        # Consider retreating if low health
        if unit.hp < unit.max_hp * 0.3:
            retreat_score = 50  # High priority when low health
            if retreat_score > best_score:
                best_action = {"type": "retreat"}

        return best_action
```

---

## Common Integration Mistakes to Avoid

### 1. Circular Dependencies

**Problem:**
```python
# battle.py
from src.states.campaign_map import CampaignMapState

# campaign_map.py
from src.states.battle import BattleState
```

**Solution:** Use late imports or dependency injection
```python
# campaign_map.py
def _trigger_encounter(self):
    from src.states.battle import BattleState  # Import only when needed
    battle = BattleState(...)
```

### 2. Tight Coupling

**Problem:**
```python
# combat_calculator.py
class CombatCalculator:
    def __init__(self):
        self.ui_manager = UIManager()  # Direct dependency
```

**Solution:** Use events for loose coupling
```python
class CombatCalculator:
    def __init__(self, event_system):
        self.event_system = event_system

    def calculate_damage(self, ...):
        damage = ...
        self.event_system.emit("damage_dealt", {"damage": damage})
```

### 3. Missing Data Validation

**Problem:**
```python
def apply_equipment_bonus(self, unit):
    bonus = unit.equipment.weapon.attack_bonus  # May crash if None
```

**Solution:** Validate data
```python
def apply_equipment_bonus(self, unit):
    if not hasattr(unit, 'equipment') or not unit.equipment:
        return 0

    weapon = unit.equipment.get_slot('weapon')
    if not weapon:
        return 0

    return weapon.get_stat_bonus('attack')
```

### 4. State Leakage

**Problem:**
```python
# Shared mutable state
global_unit_list = []

def create_battle():
    global_unit_list.append(unit)  # State persists across battles
```

**Solution:** Encapsulate state in objects
```python
class Battle:
    def __init__(self):
        self.units = []  # Instance-specific state
```

---

## Integration Testing Checklist

After implementing an integration:

- [ ] Does data flow correctly between systems?
- [ ] Are edge cases handled (None values, empty lists)?
- [ ] Do events fire when expected?
- [ ] Is state properly cleaned up when switching states?
- [ ] Are UI elements updated when game state changes?
- [ ] Does the integration work in both directions (if applicable)?
- [ ] Are there any performance issues with the integration?
- [ ] Is the integration documented in code comments?
