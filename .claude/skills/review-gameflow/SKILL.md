---
name: review-gameflow
description: Diagnostic skill for analyzing the current game flow and mechanics implementation status in Classical Army Roguelite. Use when the user asks to review what mechanics are implemented, diagnose game flow, identify missing features, check implementation completeness, or propose feature integrations. Helps understand the current state of the game, what's working, what's incomplete, and what needs to be added.
---

# Review Gameflow - Diagnostic & Integration Planner

This skill provides a comprehensive diagnostic workflow for analyzing the Classical Army Roguelite game implementation, identifying completed mechanics, finding gaps, and proposing integrations.

## When to Use This Skill

Use this skill when:
- User asks to review current game mechanics
- User wants to know what's implemented vs. planned
- User requests an audit of game systems
- User asks what features are missing or incomplete
- User wants suggestions for next features to implement
- Planning integration between existing systems

## Diagnostic Workflow

Follow this systematic approach to analyze the game:

### Step 1: Core Systems Audit

Check the foundational systems in order:

1. **Game Loop & State Management**
   - Read [src/core/game.py](src/core/game.py) - Main game loop
   - Read [src/core/engine.py](src/core/engine.py) - Engine systems
   - Read [src/core/state_manager.py](src/core/state_manager.py) - State transitions
   - Check: Does the game loop run? Are states switching properly?

2. **Event System**
   - Read [src/core/event_system.py](src/core/event_system.py)
   - Check: Is event pub/sub working? Are events being fired/handled?

3. **Configuration & Resources**
   - Read [src/core/config_manager.py](src/core/config_manager.py)
   - Read [src/utils/asset_loader.py](src/utils/asset_loader.py)
   - Check: Are configs loading? Are resources managed properly?

### Step 2: Game States Audit

Examine each game state for completeness:

1. **Main Menu State**
   - Read [src/states/main_menu.py](src/states/main_menu.py)
   - Check: Menu navigation, button functionality, state transitions

2. **Campaign Map State**
   - Read [src/states/campaign_map.py](src/states/campaign_map.py)
   - Read [src/procgen/tile_map_generator.py](src/procgen/tile_map_generator.py)
   - Check: Map generation, player movement, encounters, sprite rendering

3. **Battle State**
   - Read [src/states/battle.py](src/states/battle.py)
   - Check: Battle initialization, unit deployment, turn flow, victory/defeat conditions

4. **Army Management State**
   - Read [src/states/army_management.py](src/states/army_management.py)
   - Check: Unit roster display, equipment system integration, upgrade mechanics

5. **Commander Selection State**
   - Read [src/states/commander_selection.py](src/states/commander_selection.py)
   - Check: Commander generation, ability display, selection flow

### Step 3: Battle Systems Audit

Deep dive into combat mechanics:

1. **Hex Grid System**
   - Read [src/battle/hex_grid.py](src/battle/hex_grid.py)
   - Check: Hex coordinate math, cell data structure, terrain types

2. **Combat Calculator**
   - Read [src/battle/combat_calculator.py](src/battle/combat_calculator.py)
   - Check: Damage formulas, terrain bonuses, flanking, unit matchups

3. **Morale System**
   - Read [src/battle/morale_system.py](src/battle/morale_system.py)
   - Check: Morale calculations, breaking points, routing behavior

4. **Turn Manager**
   - Read [src/battle/turn_manager.py](src/battle/turn_manager.py)
   - Check: Initiative system, turn order, action points

5. **Pathfinding**
   - Read [src/battle/pathfinding.py](src/battle/pathfinding.py)
   - Check: A* implementation, movement cost, reachability calculation

6. **Formations**
   - Read [src/battle/formations.py](src/battle/formations.py)
   - Check: Formation types, bonuses, positioning logic

7. **AI System**
   - Read [src/entities/systems.py](src/entities/systems.py)
   - Check: AI decision-making, target selection, tactical behavior

### Step 4: Entity & Component Audit

Review the entity architecture:

1. **Entity Base**
   - Read [src/entities/entity.py](src/entities/entity.py)
   - Check: Component attachment, entity lifecycle

2. **Components**
   - Read [src/entities/components.py](src/entities/components.py)
   - Check: Available components, data structures

3. **Unit System**
   - Read [src/entities/unit.py](src/entities/unit.py)
   - Check: Unit stats, abilities, equipment slots

4. **Army System**
   - Read [src/entities/army.py](src/entities/army.py)
   - Check: Army composition, commander integration, army-level stats

5. **Equipment System**
   - Read [src/entities/equipment_system.py](src/entities/equipment_system.py)
   - Check: Item types, stat bonuses, equipment mechanics

### Step 5: Procedural Generation Audit

Examine content generation systems:

1. **Campaign Generation**
   - Read [src/procgen/campaign_generator.py](src/procgen/campaign_generator.py)
   - Check: Campaign structure, progression curve, node types

2. **Battle Map Generation**
   - Read [src/procgen/battle_map_generator.py](src/procgen/battle_map_generator.py)
   - Check: Terrain generation, strategic placement, variety

3. **Encounter Generation**
   - Read [src/procgen/encounter_generator.py](src/procgen/encounter_generator.py)
   - Check: Enemy army generation, difficulty scaling, variety

4. **Event System**
   - Read [src/procgen/event_system.py](src/procgen/event_system.py)
   - Read [src/data/event_definitions.py](src/data/event_definitions.py)
   - Check: Event types, choices, consequences

5. **Loot & Rewards**
   - Read [src/procgen/loot_tables.py](src/procgen/loot_tables.py)
   - Read [src/procgen/item_generator.py](src/procgen/item_generator.py)
   - Check: Item generation, rarity system, reward calculation

6. **Commander Generation**
   - Read [src/procgen/commander_generator.py](src/procgen/commander_generator.py)
   - Check: Commander abilities, personality traits, generated variety

### Step 6: Data & Content Audit

Review static data definitions:

1. **Unit Definitions**
   - Read [src/data/unit_definitions.py](src/data/unit_definitions.py)
   - Check: Unit variety, faction diversity, balance

2. **Faction Data**
   - Read [src/data/faction_data.py](src/data/faction_data.py)
   - Check: Faction traits, unit rosters, unique mechanics

3. **Commander Data**
   - Read [src/data/commander_data.py](src/data/commander_data.py)
   - Check: Historical commanders, abilities, flavor

4. **Item Definitions**
   - Read [src/data/item_definitions.py](src/data/item_definitions.py)
   - Check: Item types, effects, historical authenticity

### Step 7: UI/UX Audit

Check user interface systems:

1. **UI Manager**
   - Read [src/ui/ui_manager.py](src/ui/ui_manager.py)
   - Check: Widget management, rendering, event handling

2. **Widget System**
   - Read [src/ui/widgets/widget.py](src/ui/widgets/widget.py)
   - Read [src/ui/button.py](src/ui/button.py)
   - Read [src/ui/panel.py](src/ui/panel.py)
   - Check: Widget types, interaction, styling

3. **Visual Assets**
   - Read [src/art/sprite_generator.py](src/art/sprite_generator.py)
   - Read [src/art/palettes.py](src/art/palettes.py)
   - Check: Sprite generation, color schemes, visual consistency

### Step 8: Integration Points Analysis

After auditing systems, identify integration opportunities:

For detailed integration patterns and mechanics tracking, read:
- [references/mechanics-checklist.md](references/mechanics-checklist.md) - Complete list of expected mechanics
- [references/integration-patterns.md](references/integration-patterns.md) - Common integration strategies

## Output Format

After completing the diagnostic workflow, provide a structured report:

### 1. Implementation Status Summary

Organize findings into three categories:

**✅ Fully Implemented**
- List systems that are complete and functional
- Include file references

**⚠️ Partially Implemented**
- List systems with basic structure but missing features
- Note what's missing
- Include file references

**❌ Not Implemented**
- List planned features not yet started
- Reference README.md roadmap

### 2. Critical Gaps

Identify the most important missing pieces:
- Systems that block core gameplay
- Features referenced but not implemented
- Integration points that are broken

### 3. Integration Opportunities

Propose specific integrations:
- How existing systems can work together
- Missing connections between implemented features
- Next logical steps for development

### 4. Priority Recommendations

Suggest next steps in order of importance:
1. Critical gaps that break core loops
2. High-value integrations using existing code
3. Polish and enhancement opportunities

## Example Diagnostic Output

```markdown
## Game Flow Diagnostic Report

### ✅ Fully Implemented (Core Gameplay Loop Working)

**State Management & Game Loop**
- [src/core/game.py](src/core/game.py) - Main loop: ✅ Working
- [src/core/state_manager.py](src/core/state_manager.py) - State stack: ✅ Working
- [src/core/engine.py](src/core/engine.py) - Pygame integration: ✅ Working

**Battle System (90% Complete)**
- [src/battle/hex_grid.py](src/battle/hex_grid.py) - Hex grid: ✅ Functional
- [src/battle/combat_calculator.py](src/battle/combat_calculator.py) - Combat math: ✅ Complete
- [src/battle/morale_system.py](src/battle/morale_system.py) - Morale: ✅ Working
- [src/battle/pathfinding.py](src/battle/pathfinding.py) - A* pathfinding: ✅ Working
- [src/battle/turn_manager.py](src/battle/turn_manager.py) - Turn system: ✅ Working

**Campaign Map (80% Complete)**
- [src/states/campaign_map.py](src/states/campaign_map.py) - Map state: ✅ Working
- [src/procgen/tile_map_generator.py](src/procgen/tile_map_generator.py) - Terrain: ✅ Working
- [src/procgen/encounter_generator.py](src/procgen/encounter_generator.py) - Encounters: ✅ Working

### ⚠️ Partially Implemented

**Army Management (40% Complete)**
- [src/states/army_management.py](src/states/army_management.py) - Basic UI exists
- Missing: Equipment interaction, upgrade system, detailed unit inspection
- Gap: Not connected to battle rewards or equipment drops

**Formation System (30% Complete)**
- [src/battle/formations.py](src/battle/formations.py) - Data structures exist
- Missing: Formation bonuses not applied in combat
- Gap: No UI for selecting/changing formations

**Save System (0% Complete)**
- Mentioned in [README.md](README.md) Phase 4
- No implementation found
- Critical gap: No persistence between sessions

### ❌ Not Implemented

**Roguelite Meta-Progression**
- No unlock system between runs
- No persistent upgrades
- No permadeath implementation

**Tutorial System**
- No onboarding for new players
- No contextual hints during battle
- Affects accessibility

**Sound & Music**
- No audio system
- No sound effects or music

### 🔗 Integration Opportunities

1. **Battle Rewards → Army Management**
   - [src/states/battle.py](src/states/battle.py):59 calculates rewards
   - [src/states/army_management.py](src/states/army_management.py) needs to receive them
   - Connect: Pass rewards when transitioning from battle to army management

2. **Equipment System → Combat Calculator**
   - [src/entities/equipment_system.py](src/entities/equipment_system.py) has stat bonuses
   - [src/battle/combat_calculator.py](src/battle/combat_calculator.py) doesn't use them
   - Connect: Query equipment bonuses during damage calculation

3. **Formation System → Battle Deployment**
   - [src/battle/formations.py](src/battle/formations.py) has formation templates
   - [src/states/battle.py](src/states/battle.py) deploys units without formations
   - Connect: Apply formation templates during unit placement

### 📋 Priority Recommendations

**Priority 1: Complete Core Loop (1-2 days)**
1. Integrate battle rewards into army management
2. Connect equipment bonuses to combat calculations
3. Add basic save/load functionality

**Priority 2: Polish Existing Features (2-3 days)**
1. Complete formation system integration
2. Enhance army management UI
3. Add visual feedback for equipment effects

**Priority 3: Add Roguelite Elements (3-5 days)**
1. Implement permadeath
2. Create meta-progression system
3. Add unlockable commanders/units

**Priority 4: Content & Polish (ongoing)**
1. Add sound effects and music
2. Create tutorial system
3. Balance difficulty curve
```

## Tips for Effective Diagnostics

1. **Follow the Data Flow**: Trace how data moves from generation → storage → display → modification
2. **Check Integration Points**: Look for TODOs, placeholder comments, or empty functions
3. **Test State Transitions**: Verify each state can enter/exit properly and data persists
4. **Validate Complete Loops**: Ensure actions have consequences (e.g., battle → rewards → upgrades → next battle)
5. **Look for Orphaned Systems**: Identify implemented features that aren't connected to anything

## Common Integration Patterns

See [references/integration-patterns.md](references/integration-patterns.md) for detailed examples of:
- State-to-state data passing
- Event-driven system communication
- Component-based entity modifications
- Procedural content integration
- UI-to-game-logic connections
