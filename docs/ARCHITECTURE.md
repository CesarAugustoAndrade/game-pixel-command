# Architecture Documentation

## Overview

Classical Army Roguelite is built using a modular architecture with clear separation of concerns.

## Core Systems

### Game Loop ([src/core/game.py](../src/core/game.py))
- Main game loop running at 60 FPS
- Handles events, updates, and rendering
- Coordinates all game systems

### State Management ([src/core/state_manager.py](../src/core/state_manager.py))
- Stack-based state machine
- Supports state transitions (push, pop, change)
- States: Main Menu, Campaign Map, Battle, Army Management

### Event System ([src/core/event_system.py](../src/core/event_system.py))
- Pub/sub event bus for decoupled communication
- Systems can emit and subscribe to events
- Common events: unit_died, turn_start, morale_changed

### Resource Management ([src/core/engine.py](../src/core/engine.py))
- Loads and caches sprites, sounds, fonts
- Prevents duplicate loading
- Easy resource access throughout codebase

## Battle System

### Hex Grid ([src/battle/hex_grid.py](../src/battle/hex_grid.py))
- Axial coordinate system for hexagonal grid
- Neighbor finding, distance calculation
- Terrain types and occupation tracking

### Combat Calculator ([src/battle/combat_calculator.py](../src/battle/combat_calculator.py))
- Damage calculations with modifiers
- Critical hits, flanking bonuses
- Terrain effects on combat

### Turn Manager ([src/battle/turn_manager.py](../src/battle/turn_manager.py))
- Turn order management
- Action economy (action points)
- Victory condition checking

### Morale System ([src/battle/morale_system.py](../src/battle/morale_system.py))
- Morale tracking and effects
- Breaking and routing mechanics
- Morale-based combat modifiers

### Pathfinding ([src/battle/pathfinding.py](../src/battle/pathfinding.py))
- A* pathfinding on hex grid
- Movement cost based on terrain
- Reachable cell calculation

## Entity Component System

### Entity ([src/entities/entity.py](../src/entities/entity.py))
- Base entity class
- Component container
- Unique ID generation

### Components ([src/entities/components.py](../src/entities/components.py))
- Pure data containers
- Position, Stats, Morale, Movement, etc.
- Composable unit construction

### Systems ([src/entities/systems.py](../src/entities/systems.py))
- Logic that operates on entities with specific components
- Movement, Combat, Morale, Formation, AI systems

### Unit ([src/entities/unit.py](../src/entities/unit.py))
- Composite entity representing military unit
- Combines multiple components
- Type-specific stats and abilities

## Procedural Generation

### Campaign Generator ([src/procgen/campaign_generator.py](../src/procgen/campaign_generator.py))
- Layered node-based campaign maps
- Different node types (battle, merchant, rest, boss)
- Progressive difficulty

### Battle Map Generator ([src/procgen/battle_map_generator.py](../src/procgen/battle_map_generator.py))
- Terrain generation for tactical battles
- Multiple terrain types
- Deployment zone designation

### Encounter Generator ([src/procgen/encounter_generator.py](../src/procgen/encounter_generator.py))
- Enemy army composition
- Difficulty scaling
- Elite and boss encounters

## UI System

### UI Manager ([src/ui/ui_manager.py](../src/ui/ui_manager.py))
- Manages all UI widgets
- Event routing to widgets
- Render order management

### Widgets ([src/ui/widgets/](../src/ui/widgets/))
- Base widget class with event handling
- Button, Panel implementations
- Extensible widget system

## Data Flow

1. **Input** → Events (pygame) → State Manager → Current State
2. **Update** → Current State → Game Systems → Entities
3. **Render** → Entities → Sprites → Screen
4. **Events** → Game Systems → Event Bus → Subscribed Systems

## Design Patterns

- **State Pattern**: Game states (menu, battle, etc.)
- **Component Pattern**: ECS for flexible entity composition
- **Observer Pattern**: Event system for decoupled communication
- **Singleton**: Resource manager, save system
- **Strategy Pattern**: AI behaviors, formation bonuses

## Extension Points

- Add new unit types in [src/data/unit_definitions.py](../src/data/unit_definitions.py)
- Add new game states in [src/states/](../src/states/)
- Add new components in [src/entities/components.py](../src/entities/components.py)
- Add new systems in [src/entities/systems.py](../src/entities/systems.py)
- Add new terrain types in constants and map generator
