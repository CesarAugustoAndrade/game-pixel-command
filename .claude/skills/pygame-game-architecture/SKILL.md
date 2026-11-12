---
name: pygame-game-architecture
description: Comprehensive guide for building robust Pygame game architecture. Use when creating a new Pygame game, refactoring game structure, implementing game loops, state management, ECS (Entity Component System), event systems, resource management, or performance optimization for Pygame projects.
---

# Pygame Game Architecture Skill

## Overview

This skill provides battle-tested patterns and architecture for building maintainable, scalable Pygame games. Focus on modularity, performance, and code organization suitable for roguelike/roguelite games.

## Core Architecture Patterns

### 1. Entity Component System (ECS)

ECS separates data (Components) from behavior (Systems) and entities (IDs).

```python
# components.py
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Velocity:
    dx: float
    dy: float

@dataclass
class Sprite:
    image: any
    rect: any

@dataclass
class Health:
    current: int
    maximum: int

@dataclass
class Combat:
    attack: int
    defense: int
    range: int
```

```python
# entity_manager.py
from typing import Dict, Set, Type, Any
from collections import defaultdict

class EntityManager:
    def __init__(self):
        self.next_entity_id = 0
        self.entities: Set[int] = set()
        self.components: Dict[Type, Dict[int, Any]] = defaultdict(dict)
    
    def create_entity(self) -> int:
        """Create new entity and return its ID"""
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        self.entities.add(entity_id)
        return entity_id
    
    def destroy_entity(self, entity_id: int):
        """Remove entity and all its components"""
        if entity_id in self.entities:
            self.entities.remove(entity_id)
            for component_dict in self.components.values():
                component_dict.pop(entity_id, None)
    
    def add_component(self, entity_id: int, component: Any):
        """Add component to entity"""
        component_type = type(component)
        self.components[component_type][entity_id] = component
    
    def get_component(self, entity_id: int, component_type: Type) -> Any:
        """Get specific component from entity"""
        return self.components[component_type].get(entity_id)
    
    def has_component(self, entity_id: int, component_type: Type) -> bool:
        """Check if entity has component"""
        return entity_id in self.components[component_type]
    
    def get_entities_with(self, *component_types: Type) -> Set[int]:
        """Get all entities that have ALL specified components"""
        if not component_types:
            return set()
        
        result = set(self.components[component_types[0]].keys())
        for comp_type in component_types[1:]:
            result &= set(self.components[comp_type].keys())
        return result
```

```python
# systems.py
class System:
    """Base class for all systems"""
    def update(self, entity_manager: EntityManager, delta_time: float):
        pass
    
    def render(self, entity_manager: EntityManager, screen):
        pass

class MovementSystem(System):
    def update(self, entity_manager: EntityManager, delta_time: float):
        entities = entity_manager.get_entities_with(Position, Velocity)
        
        for entity_id in entities:
            pos = entity_manager.get_component(entity_id, Position)
            vel = entity_manager.get_component(entity_id, Velocity)
            
            pos.x += vel.dx * delta_time
            pos.y += vel.dy * delta_time

class RenderSystem(System):
    def render(self, entity_manager: EntityManager, screen):
        entities = entity_manager.get_entities_with(Position, Sprite)
        
        for entity_id in entities:
            pos = entity_manager.get_component(entity_id, Position)
            sprite = entity_manager.get_component(entity_id, Sprite)
            
            screen.blit(sprite.image, (pos.x, pos.y))
```

### 2. Game State Management

Use state stack for managing game modes (menu, battle, inventory, etc.).

```python
# game_state.py
from abc import ABC, abstractmethod
from typing import Optional
import pygame

class GameState(ABC):
    """Abstract base class for game states"""
    
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def enter(self):
        """Called when state becomes active"""
        pass
    
    @abstractmethod
    def exit(self):
        """Called when state becomes inactive"""
        pass
    
    @abstractmethod
    def update(self, delta_time: float):
        """Update logic"""
        pass
    
    @abstractmethod
    def render(self, screen):
        """Render to screen"""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events"""
        pass

class StateManager:
    """Manages game state stack"""
    
    def __init__(self):
        self.states = []
    
    def push(self, state: GameState):
        """Add new state to stack"""
        if self.states:
            self.states[-1].exit()
        state.enter()
        self.states.append(state)
    
    def pop(self) -> Optional[GameState]:
        """Remove and return current state"""
        if self.states:
            state = self.states.pop()
            state.exit()
            if self.states:
                self.states[-1].enter()
            return state
        return None
    
    def change(self, state: GameState):
        """Replace current state"""
        if self.states:
            self.pop()
        self.push(state)
    
    def update(self, delta_time: float):
        """Update current state"""
        if self.states:
            self.states[-1].update(delta_time)
    
    def render(self, screen):
        """Render current state"""
        if self.states:
            self.states[-1].render(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Pass event to current state"""
        if self.states:
            self.states[-1].handle_event(event)
```

```python
# Example states
class MenuState(GameState):
    def enter(self):
        print("Entering menu")
    
    def exit(self):
        print("Exiting menu")
    
    def update(self, delta_time: float):
        pass
    
    def render(self, screen):
        screen.fill((0, 0, 0))
        # Render menu
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.state_manager.push(BattleState(self.game))

class BattleState(GameState):
    def enter(self):
        # Initialize battle
        self.entity_manager = EntityManager()
        self.systems = [MovementSystem(), RenderSystem()]
    
    def exit(self):
        pass
    
    def update(self, delta_time: float):
        for system in self.systems:
            system.update(self.entity_manager, delta_time)
    
    def render(self, screen):
        for system in self.systems:
            system.render(self.entity_manager, screen)
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state_manager.pop()
```

### 3. Event System

Decouple systems with event-driven communication.

```python
# event_system.py
from typing import Callable, Dict, List, Any
from enum import Enum

class EventType(Enum):
    """Define your game events"""
    UNIT_DIED = "unit_died"
    BATTLE_WON = "battle_won"
    ITEM_COLLECTED = "item_collected"
    ABILITY_USED = "ability_used"

class Event:
    def __init__(self, event_type: EventType, data: Dict[str, Any] = None):
        self.type = event_type
        self.data = data or {}

class EventManager:
    def __init__(self):
        self.listeners: Dict[EventType, List[Callable]] = {}
    
    def subscribe(self, event_type: EventType, callback: Callable):
        """Register listener for event type"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type: EventType, callback: Callable):
        """Remove listener"""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
    
    def emit(self, event: Event):
        """Trigger event and notify all listeners"""
        if event.type in self.listeners:
            for callback in self.listeners[event.type]:
                callback(event)

# Usage example
event_manager = EventManager()

def on_unit_died(event: Event):
    unit_id = event.data['unit_id']
    print(f"Unit {unit_id} has died!")

event_manager.subscribe(EventType.UNIT_DIED, on_unit_died)
event_manager.emit(Event(EventType.UNIT_DIED, {'unit_id': 42}))
```

### 4. Resource Management

Centralized loading and caching of assets.

```python
# resource_manager.py
import pygame
from typing import Dict, Optional
from pathlib import Path

class ResourceManager:
    def __init__(self, base_path: str = "assets"):
        self.base_path = Path(base_path)
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
    
    def load_image(self, name: str, path: str, 
                   convert_alpha: bool = True) -> pygame.Surface:
        """Load and cache image"""
        if name not in self.images:
            full_path = self.base_path / path
            image = pygame.image.load(str(full_path))
            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            self.images[name] = image
        return self.images[name]
    
    def get_image(self, name: str) -> Optional[pygame.Surface]:
        """Get cached image"""
        return self.images.get(name)
    
    def load_sound(self, name: str, path: str) -> pygame.mixer.Sound:
        """Load and cache sound"""
        if name not in self.sounds:
            full_path = self.base_path / path
            self.sounds[name] = pygame.mixer.Sound(str(full_path))
        return self.sounds[name]
    
    def get_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """Get cached sound"""
        return self.sounds.get(name)
    
    def load_font(self, name: str, path: str, size: int) -> pygame.font.Font:
        """Load and cache font"""
        key = f"{name}_{size}"
        if key not in self.fonts:
            full_path = self.base_path / path
            self.fonts[key] = pygame.font.Font(str(full_path), size)
        return self.fonts[key]
    
    def get_font(self, name: str, size: int) -> Optional[pygame.font.Font]:
        """Get cached font"""
        key = f"{name}_{size}"
        return self.fonts.get(key)
```

### 5. Object Pooling

Reuse objects to reduce garbage collection overhead.

```python
# object_pool.py
from typing import List, Callable, TypeVar, Generic

T = TypeVar('T')

class ObjectPool(Generic[T]):
    def __init__(self, factory: Callable[[], T], initial_size: int = 10):
        self.factory = factory
        self.available: List[T] = []
        self.in_use: List[T] = []
        
        # Pre-populate pool
        for _ in range(initial_size):
            self.available.append(factory())
    
    def acquire(self) -> T:
        """Get object from pool"""
        if not self.available:
            obj = self.factory()
        else:
            obj = self.available.pop()
        
        self.in_use.append(obj)
        return obj
    
    def release(self, obj: T):
        """Return object to pool"""
        if obj in self.in_use:
            self.in_use.remove(obj)
            self.available.append(obj)
    
    def release_all(self):
        """Return all objects to pool"""
        self.available.extend(self.in_use)
        self.in_use.clear()

# Usage for particle systems
class Particle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.active = False

particle_pool = ObjectPool(Particle, initial_size=100)

# Get particle
particle = particle_pool.acquire()
particle.x = 100
particle.y = 200
particle.active = True

# Return when done
particle.active = False
particle_pool.release(particle)
```

### 6. Main Game Loop

Efficient game loop with fixed timestep for physics.

```python
# game.py
import pygame
import sys

class Game:
    def __init__(self, width: int = 1280, height: int = 720, fps: int = 60):
        pygame.init()
        
        # Display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Classical Army Roguelite")
        
        # Timing
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.delta_time = 0
        
        # Core systems
        self.state_manager = StateManager()
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        
        # Running flag
        self.running = True
    
    def run(self):
        """Main game loop with fixed timestep"""
        accumulator = 0
        fixed_dt = 1.0 / 60.0  # Fixed physics timestep
        
        while self.running:
            # Frame timing
            self.delta_time = self.clock.tick(self.fps) / 1000.0
            accumulator += self.delta_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state_manager.handle_event(event)
            
            # Fixed timestep updates (physics)
            while accumulator >= fixed_dt:
                self.state_manager.update(fixed_dt)
                accumulator -= fixed_dt
            
            # Render
            self.screen.fill((0, 0, 0))
            self.state_manager.render(self.screen)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    # Initialize first state
    game.state_manager.push(MenuState(game))
    game.run()
```

## Performance Optimization

### Dirty Rectangle Rendering

Only update changed screen areas:

```python
class DirtyRectRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.dirty_rects = []
    
    def add_dirty_rect(self, rect):
        self.dirty_rects.append(rect)
    
    def update_display(self):
        if self.dirty_rects:
            pygame.display.update(self.dirty_rects)
            self.dirty_rects.clear()
        else:
            pygame.display.flip()
```

### Spatial Partitioning

Use quadtree for efficient collision detection:

```python
class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary  # pygame.Rect
        self.capacity = capacity
        self.entities = []
        self.divided = False
        self.children = []
    
    def subdivide(self):
        x, y, w, h = self.boundary
        hw, hh = w // 2, h // 2
        
        self.children = [
            QuadTree(pygame.Rect(x, y, hw, hh), self.capacity),
            QuadTree(pygame.Rect(x + hw, y, hw, hh), self.capacity),
            QuadTree(pygame.Rect(x, y + hh, hw, hh), self.capacity),
            QuadTree(pygame.Rect(x + hw, y + hh, hw, hh), self.capacity)
        ]
        self.divided = True
    
    def insert(self, entity):
        if not self.boundary.collidepoint(entity.x, entity.y):
            return False
        
        if len(self.entities) < self.capacity:
            self.entities.append(entity)
            return True
        
        if not self.divided:
            self.subdivide()
        
        for child in self.children:
            if child.insert(entity):
                return True
        
        return False
    
    def query(self, range_rect):
        found = []
        
        if not self.boundary.colliderect(range_rect):
            return found
        
        for entity in self.entities:
            if range_rect.collidepoint(entity.x, entity.y):
                found.append(entity)
        
        if self.divided:
            for child in self.children:
                found.extend(child.query(range_rect))
        
        return found
```

## Best Practices

1. **Keep frame rate independent**: Use delta_time for all movement/animation
2. **Separate logic from rendering**: Update in one pass, render in another
3. **Profile regularly**: Use cProfile to identify bottlenecks
4. **Batch draw calls**: Group similar sprites together
5. **Pre-calculate when possible**: Cache expensive computations
6. **Use appropriate data structures**: QuadTree for spatial queries, sets for membership
7. **Limit scope**: Systems only access components they need

## Common Pitfalls

- Creating new objects every frame (use pooling)
- Not converting images (call convert() or convert_alpha())
- Rendering everything (use camera culling)
- Polling input inefficiently (cache key state)
- Tight coupling between systems
- Loading resources during gameplay (preload in states)

## Project Structure

```
project/
├── main.py                 # Entry point
├── game.py                 # Main game class
├── config.py               # Configuration constants
├── components/
│   ├── __init__.py
│   ├── position.py
│   ├── combat.py
│   └── ...
├── systems/
│   ├── __init__.py
│   ├── movement.py
│   ├── combat.py
│   └── ...
├── states/
│   ├── __init__.py
│   ├── menu.py
│   ├── battle.py
│   └── ...
├── managers/
│   ├── __init__.py
│   ├── entity_manager.py
│   ├── resource_manager.py
│   └── event_manager.py
└── assets/
    ├── images/
    ├── sounds/
    └── fonts/
```

This architecture provides a solid foundation for building complex, maintainable Pygame games while maintaining performance and flexibility.
