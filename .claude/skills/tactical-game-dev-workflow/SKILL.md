---
name: tactical-game-dev-workflow
description: Complete workflow for developing tactical combat game systems from concept to production. Covers requirements analysis, architecture design, implementation, visualization, and documentation. Use when building real-time or turn-based tactical combat systems, strategy game prototypes, morale-based victory conditions, or grid-based battle systems.
---

# SKILL: Tactical Game System Development Workflow

## Skill Metadata

**Skill Name:** `tactical-game-dev-workflow`
**Version:** 1.0.0
**Category:** Game Development / System Architecture
**Difficulty:** Intermediate to Advanced
**Prerequisites:** Python programming, basic game development concepts
**Output:** Complete, production-ready game system with documentation

## Skill Description

This skill enables the development of complete tactical combat game systems from concept to production. It covers the entire workflow: requirements analysis, architecture design, implementation, testing, visualization, and comprehensive documentation.

**Use this skill when:**
- Building real-time or turn-based tactical combat systems
- Creating strategy game prototypes
- Implementing morale-based victory conditions
- Developing grid-based battle systems
- Designing entity management systems for games

## Reference Implementation

See the `references/` directory for complete working examples:
- `combat_game_state.py` - Complete game state management system
- `combat_renderer.py` - Pygame rendering and visualization system

These files demonstrate all concepts in this workflow with ~1,500 lines of production-ready code.

## Skill Phases

### Phase 1: Requirements Analysis and Design (15% of time)

#### Inputs Required
- Visual reference (image, mockup, or description)
- Core mechanics description
- Performance requirements
- Platform/technology constraints

#### Process Steps

**Step 1.1: Extract Visual Elements**
```
From reference image, identify:
□ Map/battlefield layout and dimensions
□ Unit types and visual representation
□ UI elements and placement
□ Color schemes and visual style
□ Commander/leader representations
□ Special features (castles, terrain)
```

**Step 1.2: Define Core Mechanics**
```
Document:
□ Combat resolution method (real-time/turn-based)
□ Victory conditions
□ Unit statistics and attributes
□ Movement and positioning rules
□ Special abilities or mechanics
□ Phase/turn structure
```

**Step 1.3: Architecture Planning**
```
Design:
□ Data structure hierarchy
□ System boundaries and responsibilities
□ Update loop and timing
□ State machine for game phases
□ Event system for communication
□ Rendering pipeline separation
```

**Step 1.4: Technical Specification**
```
Define:
□ Programming language and version
□ Required libraries/frameworks
□ Target performance (FPS, unit count)
□ File structure and organization
□ Naming conventions
□ Documentation standards
```

#### Deliverables
- Technical specification document
- Architecture diagrams
- Data structure definitions
- Implementation roadmap

---

### Phase 2: Core System Implementation (35% of time)

#### Step 2.1: Foundation Data Structures

**Create Base Classes:**
```python
# Template structure

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

# 1. Define enums for states and types
class UnitType(Enum):
    """All unit types in the game"""
    INFANTRY = "infantry"
    CAVALRY = "cavalry"
    SKIRMISHER = "skirmisher"
    SIEGE = "siege"

class UnitStance(Enum):
    """Possible unit states"""
    ATTACKING = "attacking"
    HOLDING = "holding"
    ROUTING = "routing"
    DESTROYED = "destroyed"

# 2. Create position/location system
@dataclass
class GridPosition:
    """Spatial positioning"""
    x: int
    y: int

    def distance_to(self, other: 'GridPosition') -> float:
        """Calculate distance"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# 3. Define game entities
@dataclass
class Unit:
    """Individual unit representation"""
    unit_id: str
    position: GridPosition
    health: int
    max_health: int
    attack_power: int
    defense: int
    morale: int

    def take_damage(self, damage: int) -> bool:
        """Apply damage, return True if destroyed"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        self.morale -= actual_damage // 2

        if self.health <= 0:
            return True
        return False

    def can_attack(self) -> bool:
        """Check if unit can perform attack"""
        return self.health > 0 and self.morale > 20

# 4. Create container classes
@dataclass
class Army:
    """Collection of units"""
    units: List[Unit]

    def calculate_morale(self) -> int:
        """Compute army morale"""
        if not self.units:
            return 0
        alive_units = [u for u in self.units if u.health > 0]
        if not alive_units:
            return 0
        return sum(u.morale for u in alive_units) // len(alive_units)

    def get_alive_units(self) -> List[Unit]:
        """Filter for active units"""
        return [u for u in self.units if u.health > 0]
```

**Checklist:**
- [ ] All enums defined for types and states
- [ ] Position system with distance calculation
- [ ] Unit class with all attributes
- [ ] Army/collection management
- [ ] Map/battlefield representation
- [ ] Type hints on all methods
- [ ] Docstrings for public API

#### Step 2.2: Game State Management

**Create Main State Controller:**
```python
class BattleState:
    """Central game state manager"""

    def __init__(self):
        """Initialize all subsystems"""
        self.phase = BattlePhase.DEPLOYMENT
        self.battle_time = 0.0
        self.battle_map = BattleMap()
        self.armies = []
        self.projectiles = []
        self.particle_effects = []

    def initialize_battle(self):
        """Set up initial game state"""
        # Deploy armies, set up terrain, etc.
        pass

    def update(self, delta_time: float):
        """Main update loop"""
        self.battle_time += delta_time

        # Update all subsystems
        self._update_units(delta_time)
        self._update_projectiles(delta_time)
        self._update_effects(delta_time)

        # Process game logic
        self._process_phase_logic()

        # Check victory conditions
        self._check_victory_conditions()

    def _update_units(self, dt: float):
        """Update all unit timers and states"""
        for army in self.armies:
            for unit in army.units:
                unit.update(dt)

    def _process_phase_logic(self):
        """Execute current phase logic"""
        if self.phase == BattlePhase.SKIRMISH:
            self._process_skirmish_phase()
        elif self.phase == BattlePhase.ENGAGEMENT:
            self._process_engagement_phase()

    def _check_victory_conditions(self):
        """Evaluate win/loss conditions"""
        for army in self.armies:
            if army.calculate_morale() < 30:
                self.phase = BattlePhase.MORALE_BREAK
```

**Checklist:**
- [ ] State machine for game phases
- [ ] Update loop with delta-time
- [ ] Subsystem update methods
- [ ] Victory condition checking
- [ ] Event logging system
- [ ] State serialization (save/load)

#### Step 2.3: Combat Resolution Engine

**Implement Combat Mechanics:**
```python
def _execute_attack(self, attacker: Unit, target: Unit):
    """Execute an attack from one unit to another"""
    if attacker.range > 1:
        # Ranged attack - create projectile
        self._fire_projectile(attacker, target)
    else:
        # Melee attack - instant damage
        was_destroyed = target.take_damage(attacker.attack_power)
        attacker.reset_attack_cooldown()

        # Combat effects
        self.particle_effects.append(
            ParticleEffect("sparks", target.position, lifetime=0.4)
        )

        if was_destroyed:
            self.log_event(f"{attacker.unit_id} destroyed {target.unit_id}!", "victory")
```

**Checklist:**
- [ ] Attack validation logic
- [ ] Damage calculation formula
- [ ] Defense/armor mechanics
- [ ] Projectile creation (for ranged)
- [ ] Effect spawning
- [ ] Combat logging
- [ ] Cooldown management

---

### Phase 3: Visualization Layer (20% of time)

#### Step 3.1: Rendering System Setup

**Create Rendering Framework:**
```python
import pygame

class BattleRenderer:
    """Main rendering system"""

    def __init__(self, screen_width: int, screen_height: int):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.cell_size = 40  # Grid cell size in pixels
        self.fonts = self._load_fonts()
        self.colors = self._define_color_palette()

    def render_frame(self, battle_state: BattleState):
        """Render complete frame"""
        # Clear screen
        self.screen.fill(self.colors['background'])

        # Render layers (back to front)
        self._render_terrain(battle_state.battle_map)
        self._render_grid(battle_state.battle_map)
        self._render_units(battle_state.armies)
        self._render_projectiles(battle_state.projectiles)
        self._render_effects(battle_state.effects)
        self._render_ui(battle_state)

        # Update display
        pygame.display.flip()

    def _grid_to_screen(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """Convert grid coordinates to screen pixels"""
        return (grid_x * self.cell_size, grid_y * self.cell_size)
```

**Checklist:**
- [ ] Pygame initialization
- [ ] Color palette definition
- [ ] Font loading
- [ ] Coordinate conversion functions
- [ ] Layer rendering order
- [ ] Frame update logic

---

### Phase 4: Testing and Examples (10% of time)

#### Create Usage Examples

**Example Template:**
```python
"""
Example: Basic Battle Simulation
"""

def example_basic_battle():
    """Demonstrate basic battle setup and simulation"""
    print("\n" + "="*60)
    print("EXAMPLE: Basic Battle Simulation")
    print("="*60)

    # Setup
    battle = BattleState()
    battle.initialize_battle()

    # Simulate battle
    for i in range(100):
        battle.update(0.1)  # 10 seconds total

    # Show results
    summary = battle.get_state_summary()
    print(f"\nResults:")
    print(f"  Phase: {summary['phase']}")
    print(f"  Attacker Morale: {summary['attacker_morale']}/100")
    print(f"  Defender Morale: {summary['defender_morale']}/100")
    print(f"  Battle Duration: {summary['battle_time']:.1f}s")
```

**Checklist:**
- [ ] Basic simulation example
- [ ] Command system example
- [ ] Combat mechanics demonstration
- [ ] Morale system showcase
- [ ] Full battle example
- [ ] Performance test

---

### Phase 5: Documentation (15% of time)

#### README.md Structure

```markdown
# [Project Name]

## Overview
[Brief description of the system]

## Features
- Real-time tactical combat
- Morale-based victory conditions
- Unit formations and positioning
- Projectile physics with arcing trajectories
- Particle effects system

## Installation
```bash
pip install pygame
python main.py
```

## Quick Start
```python
from combat_game_state import create_sample_battle
from combat_renderer import BattleRenderer

# Create battle
battle = create_sample_battle()
renderer = BattleRenderer()
renderer.initialize_pygame()

# Game loop
while running:
    battle.update(dt)
    renderer.render_frame(battle)
```

## Core Mechanics
### Combat Resolution
[Detailed explanation]

### Morale System
[Detailed explanation]

## API Reference
[Documentation of all public methods]

## Customization
[How to modify and extend]
```

**Checklist:**
- [ ] Clear project description
- [ ] Feature list
- [ ] Installation steps
- [ ] Quick start code
- [ ] Mechanics explained
- [ ] API reference
- [ ] Examples included
- [ ] Customization guide

---

## Skill Outputs

### Primary Outputs
1. **Complete codebase** (~1,000-2,000 lines)
   - Core game state system
   - Rendering/visualization layer
   - Example demonstrations

2. **Documentation suite** (~5,000-10,000 words)
   - README.md
   - QUICKSTART.md
   - ARCHITECTURE.md
   - Code comments and docstrings

3. **Working examples** (5-10 examples)
   - Basic usage
   - Advanced features
   - Performance tests

### Quality Metrics
- 60 FPS with target entity count
- Zero critical bugs
- 100% of features documented
- All examples working
- Code coverage >80% (if tests included)

---

## Common Pitfalls and Solutions

### Pitfall 1: Poor Performance
**Problem:** Game slows down with many units
**Solution:**
- Use spatial partitioning
- Implement object pooling
- Profile and optimize hot paths
- Consider LOD for distant units

### Pitfall 2: Spaghetti Code
**Problem:** Systems become tightly coupled
**Solution:**
- Maintain clear boundaries
- Use interfaces/protocols
- Separate concerns (MVC pattern)
- Regular refactoring

### Pitfall 3: Incomplete Documentation
**Problem:** Users can't understand how to use system
**Solution:**
- Write docs as you code
- Include many examples
- Create troubleshooting guide
- Test documentation with fresh eyes

### Pitfall 4: Feature Creep
**Problem:** Project never finishes
**Solution:**
- Define MVP clearly
- Track future enhancements separately
- Deliver working system first
- Iterate in versions

---

## Success Patterns

### Pattern 1: Bottom-Up Implementation
- Start with data structures
- Build systems on solid foundation
- Test each layer before moving up
- Refactor as needed

### Pattern 2: Separation of Concerns
- Game logic independent of rendering
- Clear interfaces between systems
- Testable components
- Easy to extend

### Pattern 3: Progressive Disclosure
- Simple examples first
- Gradually introduce complexity
- Quick start for beginners
- Deep dive for advanced users

### Pattern 4: Quality Over Quantity
- Well-tested core features
- Comprehensive documentation
- Clean, maintainable code
- Better than many half-baked features

---

## Integration with Pixel Command Project

This skill works alongside:
- **pygame-game-architecture**: Base architecture patterns
- **battle-engineer**: Combat implementation details
- **procedural-generation**: Map and content generation
- **tactical-gamedev agent**: Overall system design and documentation

Use this skill when you need a complete, production-ready tactical combat system from scratch with full documentation.

---

**Skill Version:** 1.0.0
**Last Updated:** 2025-11-04
**Maintained By:** TacticalGameDev Agent
**License:** Open for educational and commercial use