# 🏛️ Classical Army Roguelite - Claude Project Structure

## 📋 Project Description
Game set in the Classical Age, featuring a procedural campaign map where you move your character across a roguelike-style world. Along the way, you encounter enemies, items, and allies who can join your army. When you run into an enemy force, the game shifts into a fast-paced, hex-based battle between two classical armies.

There's also a dedicated scene for managing and upgrading your troops — equipping them with weapons, armor, food, and other supplies typical of the era, all of which improve their morale and overall performance in battle.

> **✨ NEW:** Joyful tactical battle system implemented! Experience hex-based combat with perfect information, deterministic outcomes, and satisfying visual feedback. Built using the `tactical-game-dev-workflow` skill with focus on player agency and tactical mastery.

## 🎮 Core Game Features
- **Turn-Based Tactical Combat**: Hexagonal/grid battle system with classical era units
- **Roguelite Elements**: Procedural maps, permadeath, meta progression
- **Historical Factions**: Rome, Greece, Persia, Carthage, each with unique units
- **Morale System**: Units can flee or surrender based on morale
- **Tactical Terrain**: Hills, rivers, forests affect combat
- **Procedural Campaigns**: Generated campaign maps with battle nodes

## 🏗️ Project Architecture

### Main Folder Structure
```
classical-army-roguelite/
├── .claude/                    # Agent and skill configuration
├── src/                        # Main source code
│   ├── core/                  # Base game system
│   ├── entities/              # Units, heroes, armies
│   ├── systems/               # Game systems
│   ├── ui/                    # User interface
│   ├── data/                  # Data definitions
│   └── utils/                 # Utilities
├── assets/                     # Game resources
│   ├── sprites/               # Graphics
│   ├── sounds/                # Sound effects
│   └── data/                  # Configuration JSONs
├── tests/                      # Unit tests
└── docs/                       # Documentation
```

## 🤖 Specialized Agents

### 1. **game-architect** - System Architect
- Designs overall game architecture
- Defines ECS (Entity-Component-System) systems
- Structures game loop and game states
- Manages module integration

### 2. **battle-engineer** - Combat Engineer
- Implements tactical combat system
- Manages battle grid/hexagonal system
- Calculates damage, morale, flanking
- Manages turns and actions

### 3. **procedural-designer** - Procedural Designer
- Generates battle maps
- Creates procedural campaigns
- Designs random encounters
- Balances dynamic difficulty

### 4. **pixelart-artist** - Pixel Art Artist
- Creates pixel art sprites and animations
- Designs unit visuals
- Creates terrain tiles
- Implements visual effects

### 5. **ui-ux-designer** - UI/UX Designer
- Designs user interface
- Implements menus and HUD
- Creates UI widgets
- Manages battle animations and player feedback

### 6. **tactical-gamedev** - Master Tactical Game Developer
- Comprehensive game system design and implementation
- Real-time combat systems and state management
- Morale systems and advanced combat mechanics
- Complete documentation and architecture design
- Integration of all game systems with best practices

## 🛠️ Specialized Skills

### Core Skills

#### 1. **pygame-game-architecture**
- Base Pygame game structure
- Game design patterns
- Optimized game loop
- State management

#### 2. **tactical-game-dev-workflow**
- Complete tactical combat development workflow
- Requirements analysis to production
- Game state management patterns
- Rendering system architecture
- ~1,200 lines of reference code (combat_game_state.py + combat_renderer.py)

#### 3. **tactical-combat-system**
- Tactical combat implementation
- Grid/hexagonal system
- Combat calculations
- Line of sight and range

#### 4. **procedural-generation**
- Procedural generation algorithms
- Noise functions (Perlin, Simplex)
- Terrain generation
- Enemy placement

#### 5. **classical-units-database**
- Historical units database
- Balanced statistics
- Historical descriptions
- Counter-unit relationships

#### 6. **roguelite-mechanics**
- Permadeath system
- Meta-game progression
- Unlocks and persistence
- Run modifiers

### Technical Skills

#### 7. **sprite-management**
- Sprite loading and management
- Sprite animations
- Sprite sheets
- Visual effects

#### 8. **pathfinding-algorithms**
- A* for movement
- Dijkstra for influence
- Flow fields for groups
- Tactical navigation

#### 9. **save-system**
- State serialization
- Data compression
- Save versioning
- Cloud saves (optional)

#### 10. **ai-behavior-trees**
- Behavior trees
- State machines
- Utility AI
- Tactical decision-making

#### 11. **performance-optimization**
- Python profiling
- Pygame optimization
- Memory management
- Batching techniques

### Content Skills

#### 12. **historical-accuracy**
- Historical references
- Weaponry and tactics
- Battle formations
- Cultural context

#### 13. **sound-design**
- Audio integration
- Sound effects
- Ambient music
- Dynamic audio

#### 14. **particle-effects**
- Particle system
- Combat effects
- Environmental effects
- Particle optimization

#### 15. **localization-system**
- Multi-language support
- String management
- Text formatting
- International fonts

#### 16. **tutorial-system**
- Interactive tutorials
- Contextual tooltips
- Strategy guides
- Player onboarding

## 📊 Workflow

### Phase 1: Foundation (Weeks 1-2)
1. game-architect establishes base architecture✅
2. ui-ux-designer creates main menu and basic navigation✅
3. Implement configuration system and resource management✅

### Phase 2: Core Gameplay (Weeks 3-6)
1. battle-engineer develops combat system✅
2. Define initial units and factions in data files✅
3. procedural-designer creates basic map generator with Pokemon Emerald-style tile-based design ✅
4. create skirmish battles when encounter an enemy.✅
5. Implement basic enemy AI behaviors✅

### Phase 3: Content and Polish (Weeks 7-10)

1. procedural-designer expands procedural generation 🔄 (IN PROGRESS)

   - ✅ Item/loot generation system with rarities (common, rare, epic, legendary)
   - ✅ Battle reward system (gold, XP, items, recruits)
   - ✅ Equipment system with stat bonuses
   - ✅ Event system with 15+ historical events and choices
   - ✅ Enemy commander generation with abilities
   - ⏳ Formation templates (pending)
   - ⏳ Dynamic difficulty tracking (pending)
   - ⏳ Biome system with multiple types (pending)

2. pixelart-artist creates unit sprites and terrain tiles ✅
3. ui-ux-designer refines interface and adds effects
4. Balance and test difficulty progression

### Phase 4: Meta-Game (Weeks 11-12)
1. Implement complete save system
2. procedural-designer adds campaign system
3. Final balancing of progression curves
4. All: testing and final polish

## 🎯 Quality Objectives
- **Performance**: Stable 60 FPS on modest hardware
- **Accessibility**: Intuitive controls, clear tutorials
- **Replayability**: High variability in each run
- **Balance**: All factions viable, multiple strategies
- **Polish**: Smooth animations, clear player feedback

## 📚 Resources and References
- Pygame Documentation
- Game Programming Patterns (book)
- Total War series (mechanics inspiration)
- Slay the Spire (roguelite structure)
- Historical warfare references

## 🚀 Quick Start Commands
```bash
# Initialize project
python setup.py init

# Run game
python main.py

# Run tests
pytest tests/

# Generate build
python build.py --platform=windows
```
