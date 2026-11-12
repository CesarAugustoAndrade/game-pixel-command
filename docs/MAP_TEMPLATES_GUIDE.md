# Battle Map Templates - Visual Guide

## Quick Reference for Map Types

---

## 1. Plains Encounter 🌾

```
Template: "plains_encounter"
Difficulty: ⭐⭐ (Beginner-friendly)
Tactical Focus: Maneuver warfare, tank battles
```

### ASCII Representation (20x15 hex grid)
```
Enemy Cities       Enemy Base         Enemy Cities
     ◆                 ■                   ◆
          🌲                    🌲
                🏔️       🌲      🏔️
     🌲                                🌲
              🌲  Neutral Cities  🌲
                    ◆ ◆ ◆
     🏔️                                🏔️
          🌲                    🌲
                🌲        🌲
     🌲
Player Cities      Player Base        Player Cities
     ◆                 ■                   ◆
```

### Terrain Distribution
- **Plains:** 60% (open maneuver space)
- **Forest:** 25% (4 clusters for cover)
- **Hills:** 15% (2 clusters for high ground)

### Building Placement
- **3 Neutral Cities** in center (contested)
- **1 Base** per side (unit production)
- **2 Cities** per side (safe income)

### Tactical Considerations
- Control center cities for economic advantage
- Use forest clusters for infantry cover
- Capture hills for defensive bonuses
- Wide frontage allows flanking maneuvers
- Tank-heavy armies excel here

---

## 2. Forest Ambush 🌲

```
Template: "forest_ambush"
Difficulty: ⭐⭐⭐ (Intermediate)
Tactical Focus: Infantry warfare, ambush tactics
```

### ASCII Representation
```
🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲🌲🌲     🌲🌲🌲🌲🌲    🌲🌲🌲🌲    🌲🌲
🌲■ Pl        🌲🌲⛰️⛰️🌲🌲        ■ En🌲
🌲   🌲     🌲🌲🌲⛰️⛰️🌲🌲🌲    🌲   🌲
🌲🌲   🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲   🌲🌲
🌲🌲🌲   Path══════════Path  🌲🌲🌲
🌲🌲🌲     ◆  Center  ◆     🌲🌲🌲
🌲🌲🌲🌲    ════◆════    🌲🌲🌲🌲
🌲🌲   🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲   🌲🌲
🌲   🌲     🌲🌲⛰️⛰️🌲🌲🌲🌲    🌲   🌲
🌲     🌲        ⛰️⛰️            🌲
🌲🌲🌲     🌲🌲🌲🌲🌲    🌲🌲🌲🌲    🌲🌲
🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
```

### Terrain Distribution
- **Forest:** 70% (dense woodland)
- **Plains:** 20% (paths and clearings)
- **Mountains:** 10% (obstacles)

### Building Placement
- **3 Neutral Cities** in central clearing
- **1 Base** per side (rear areas)
- No other starting cities (economic pressure)

### Tactical Considerations
- Infantry units move faster through forest
- Ambush enemies in narrow paths
- Control central clearing = control map
- Mountains block movement, force bottlenecks
- Cavalry and chariots struggle in dense forest

---

## 3. Mountain Pass ⛰️

```
Template: "mountain_pass"
Difficulty: ⭐⭐⭐⭐ (Advanced)
Tactical Focus: Defensive warfare, chokepoint control
```

### ASCII Representation
```
⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️
⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️
⛰️⛰️⛰️⛰️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️⛰️⛰️⛰️⛰️
⛰️⛰️■🏔️         ◆ ▲        🏔️■⛰️⛰️
⛰️⛰️ 🏔️   ══════════════   🏔️ ⛰️⛰️
⛰️⛰️🏔️         ◆ ▲        🏔️⛰️⛰️
⛰️⛰️  Pass═════════════Pass  ⛰️⛰️
⛰️⛰️🏔️         ◆          🏔️⛰️⛰️
⛰️⛰️⛰️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️⛰️⛰️⛰️⛰️⛰️
⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️
```

### Terrain Distribution
- **Mountains:** 60% (impassable walls)
- **Plains:** 25% (the pass itself)
- **Hills:** 15% (high ground on edges)

### Building Placement
- **1 City** center of pass (key objective)
- **2 Forts** at strategic positions (defensive)
- **1 Base** per side (ends of pass)

### Tactical Considerations
- Extremely narrow frontage (3-hex width)
- High ground on pass edges crucial
- Forts provide +4 defense stars
- Impossible to flank
- Ranged units dominate
- Breakthrough attempts very difficult
- Defensive armies excel

---

## 4. River Crossing 🌊

```
Template: "river_crossing"
Difficulty: ⭐⭐⭐ (Intermediate)
Tactical Focus: Bridge control, two-front warfare
```

### ASCII Representation
```
     ◆         ~~     🏔️      ◆
Player  🌲     ~~       🏔️   Enemy
City          ~~              City

■ Player     ══◆══     Enemy ■
Base    🌲   Bridge   🏔️    Base
            ~~═══~~

     🌲       ~~       🏔️
            ~~═══~~
            ══◆══
     🌲     ~~═══~~    🏔️

Player  🌲   ~~═══~~   🏔️   Enemy
City        ══◆══           City
     ◆         ~~     🏔️      ◆
```

### Terrain Distribution
- **Plains:** 50% (open terrain)
- **Water:** 20% (river barrier)
- **Forest:** 20% (flanking cover)
- **Hills:** 10% (defensive positions)

### Building Placement
- **3 Neutral Cities** at bridge crossings
- **3 Cities** per side (starting income)
- **1 Base** per side

### Tactical Considerations
- River divides battlefield completely
- Only 3 crossing points (chokepoints)
- Control bridges = control game
- Can split forces between bridges
- Flanking through multiple crossings
- Buildings near bridges = defensive anchors
- Creates natural two-front battle

---

## 5. Siege Battle 🏰

```
Template: "siege_battle"
Difficulty: ⭐⭐⭐⭐⭐ (Expert)
Tactical Focus: Assault/defense, asymmetric warfare
```

### ASCII Representation
```
Attacker (Player) Side    |  Defender (Enemy) Side
                          |
  ◆         🌲           |  ⛰️⛰️⛰️⛰️⛰️⛰️⛰️
                          |  ⛰️           ◆
  ■ Player      🌲       |  ⛰️   🏔️  Enemy
                          |  ⛰️      🏔️  HQ
        🌲                |  ⛰️ ▲ Gate   ★
                          |  ⛰️══════🏔️
        🌲    🌲          |  ⛰️      🏔️
                          |  ⛰️   🏔️      ◆
  ◆         🌲           |  ⛰️⛰️⛰️⛰️⛰️⛰️⛰️
```

### Terrain Distribution
- **Plains:** 45% (attacker's approach)
- **Mountains:** 30% (fortified walls)
- **Hills:** 15% (defender's interior)
- **Forest:** 10% (attacker's cover)

### Building Placement
- **1 Enemy HQ** (victory objective)
- **1 Fort** at gate (defensive strongpoint)
- **2 Enemy Cities** inside fort
- **1 Player Base** + **2 Cities** (attacker)

### Tactical Considerations
- **Most asymmetric map**
- Attacker must breach walls
- Defender has terrain advantage
- Gates are critical chokepoints
- HQ capture = instant victory
- Hardest map for attacker
- Rewards creative tactics
- Use forests to approach safely
- Concentrate forces at gates
- Defender can counter-attack

---

## Map Selection Guidelines

### For New Players
1. **Plains Encounter** - Learn basics
2. **River Crossing** - Learn bridges
3. **Forest Ambush** - Learn terrain types

### For Experienced Players
1. **Mountain Pass** - Test defensive skills
2. **Siege Battle** - Ultimate challenge

### For Variety
- **Random Template** - Game auto-selects
- Each template plays completely differently
- All templates balanced for fairness

---

## Terrain Legend

| Symbol | Terrain | Movement Cost | Defense Stars |
|--------|---------|---------------|---------------|
| `══`   | Plains  | 1 | ⭐ (none) |
| `🌲`   | Forest  | 2 | ⭐⭐ (2 stars) |
| `🏔️`   | Hills   | 2 | ⭐⭐⭐ (3 stars) |
| `⛰️`   | Mountains | Impassable | ⭐⭐⭐⭐ (4 stars) |
| `~~`   | Water   | Impassable | none |

---

## Building Legend

| Symbol | Building | Owner | Effect |
|--------|----------|-------|--------|
| `◆`    | City     | Colored | Income + Healing |
| `■`    | Base     | Colored | Unit Production |
| `★`    | HQ       | Colored | Victory Objective |
| `▲`    | Fort     | Colored | Defensive +2 stars |

**Colors:**
- 🔵 Blue = Player owned
- 🔴 Red = Enemy owned
- ⚪ Gray = Neutral (uncaptured)

---

## Advanced Tactics by Template

### Plains Encounter
- **Opening:** Rush center cities with fast units
- **Mid-game:** Control hills for defensive line
- **Late-game:** Tank pushes with infantry support

### Forest Ambush
- **Opening:** Infantry through forest paths
- **Mid-game:** Control central clearing
- **Late-game:** Ambush reinforcements in woods

### Mountain Pass
- **Opening:** Secure high ground on edges
- **Mid-game:** Hold forts at all costs
- **Late-game:** Ranged barrage, then push

### River Crossing
- **Opening:** Race to capture bridge cities
- **Mid-game:** Defend 2 bridges, push 1
- **Late-game:** Multi-front coordination

### Siege Battle
- **Attacker:** Use forests to approach, concentrate at gate
- **Defender:** Hold gate with best units, counter-attack flanks

---

## Map Generation Tips

### To Always Use Specific Template
```python
# In battle.py, line 106, replace:
template = map_generator.get_random_template()

# With:
template = "plains_encounter"  # Or any other template name
```

### To Add Weight to Certain Templates
```python
# In battle_map_generator.py, line 529, modify:
def get_random_template(self):
    templates = [
        "plains_encounter",  # Appears 3x as often
        "plains_encounter",
        "plains_encounter",
        "forest_ambush",
        "mountain_pass",
        "river_crossing",
        "siege_battle",
    ]
    return random.choice(templates)
```

---

## Future Template Ideas

### Coastal Assault 🏖️
- Beach landing scenario
- Water on one edge
- Defenders on high ground
- Asymmetric like siege

### Urban Warfare 🏛️
- City streets (narrow passages)
- Buildings as cover
- Multiple objectives
- Close-quarters combat

### Open Desert 🏜️
- Minimal cover
- Sandstorms reduce vision
- Oasis objectives
- Mobility-focused

### Highland Battle 🗻
- Multiple elevation levels
- Rain affects movement
- Hill forts everywhere
- Vertical tactics

---

## Troubleshooting

**Problem:** Map looks too random
- **Solution:** Check that template is being selected, not falling back to default

**Problem:** Buildings spawn on water
- **Solution:** _add_building() automatically fixes terrain, check it's being called

**Problem:** Too many forests/mountains
- **Solution:** Adjust blob radius in template methods (decrease radius parameter)

**Problem:** Not enough variety
- **Solution:** Add randomness to blob positions within templates

---

## Performance Notes

- Map generation: ~30-50ms
- No impact on FPS
- Pre-rendered terrain still cached
- Buildings render quickly (lightweight)

---

**End of Guide**

*For implementation details, see:*
- `src/procgen/battle_map_generator.py`
- `BATTLE_MAP_TRANSFORMATION_REPORT.md`
