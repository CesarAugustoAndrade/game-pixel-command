# ⚔️ Advance Wars Battle Visual Examples

## 🗺️ Example Battle Map

```
═══════════════════════════════════════════════════════════════════════
║                    ADVANCE WARS - BATTLE MAP                         ║
║                      (Fog of War: OFF)                               ║
═══════════════════════════════════════════════════════════════════════

Player 1 (Orange Star) vs Player 2 (Blue Moon)

═════════════════════════════════════════════════════════════════════════

🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️
🏔️🏛️🏭🏭░░░░░░░░░░░░░░░░🏭🏭🏛️🏔️  ← Player 2 Base
🏔️🏭░░░░░░░░░░░░░░░░░░░░░░🏭🏔️
🏔️░░░░░░🌲🌲🌲░░░░🌲🌲🌲░░░░░░🏔️
🏔️░░░░░🌲🌲🌲🌲░░🌲🌲🌲🌲░░░░░🏔️
🏔️░░░░🌲🌲🌿🌲🌲🌲🌲🌿🌲🌲░░░░🏔️
🏔️░░░░🌲🌲🌲🌲⛟🌲🌲🌲🌲░░░░🏔️  ← Blue Recon
🏔️░░░░░🌲🌲🌲🌲🌲🌲🌲🌲░░░░░🏔️
🏔️░░░░░░🌲🌲🌲🌲🌲🌲░░░░░░░🏔️
🏔️░░░░░░░░░░░░░░░░░░░░░░░🏔️
🏔️🏘️🏘️🏘️░░░░░░░░░░░░🏘️🏘️🏘️🏔️  ← Neutral Cities
🏔️🏘️▓▓🏘️░░░░░░░░░░░░🏘️▓▓🏘️🏔️  ← Contested Center
🏔️🏘️🏘️🏘️░░░░░░░░░░░░🏘️🏘️🏘️🏔️
🏔️░░░░░░░░░░░░░░░░░░░░░░░🏔️
🏔️░░░░░░🌲🌲🌲🌲🌲🌲░░░░░░░🏔️
🏔️░░░░░🌲🌲🌲🌲🌲🌲🌲🌲░░░░░🏔️
🏔️░░░░🌲🌲🚜🌲🌲🌲🌲🌲🌲🌲░░░░🏔️  ← Orange Mech
🏔️░░░░🌲🌲🌲🌲🌲🌲🌲🌲🌲░░░░░🏔️
🏔️░░░░░🌲🌲🌲🌲░░🌲🌲🌲🌲░░░░░🏔️
🏔️░░░░░░🌲🌲🌲░░░🌲🌲🌲░░░░░░🏔️
🏔️🏭░░░░░░░░░░░░░░░░░░░░░░🏭🏔️
🏔️🏛️🏭🏭░░░░░░░░░░░░░░░░🏭🏭🏛️🏔️  ← Player 1 Base
🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

═══════════════════════════════════════════════════════════════════════

Legend:
🏛️ = HQ (Capture to win!)
🏭 = Base (Produces ground units)
🏘️ = City (Provides income: 1000G/turn)
▓▓ = Units (various types)
🌲 = Forest (2★ defense, blocks vision)
🏔️ = Mountain (4★ defense, infantry only)
░░ = Plain (0★ defense, easy movement)

═══════════════════════════════════════════════════════════════════════
Current Turn: Day 5
Player 1 Funds: 8,000G (8 properties)
Player 2 Funds: 7,000G (7 properties)
═══════════════════════════════════════════════════════════════════════
```

---

## ⚔️ Combat Example: Tank vs Infantry

```
═══════════════════════════════════════════════════════════════════════
                    COMBAT SCENARIO
═══════════════════════════════════════════════════════════════════════

Before Attack:

    🌲🌲🌲
    🌲🌲🌲
    🌲🌲🌲
       ↓
    ░░🪖░░  ← Infantry (10 HP) in Forest (2★ defense)
       ↑
    ░░▓░░
    ░░░░░
    ░░🛡️░░  ← Tank (10 HP) on Plain (0★ defense)

═══════════════════════════════════════════════════════════════════════

DAMAGE CALCULATION:

Attacker: Tank (10 HP)
Target: Infantry (10 HP) in Forest

1. Base Damage: 75% (Tank vs Infantry from chart)
2. Attacker HP Multiplier: 10/10 = 1.0
3. Pre-Defense Damage: 75% × 1.0 = 75%

4. Terrain Defense: Forest = 2 stars
   Defense Reduction: 2★ × 10 HP / 100 = 20%
   Defense Multiplier: 1.0 - 0.20 = 0.80

5. Final Damage: 75% × 0.80 = 60%
   Damage Dealt: 6 HP

COUNTER-ATTACK:

Attacker: Infantry (4 HP remaining)
Target: Tank (10 HP) on Plain

1. Base Damage: 55% (Infantry vs Tank from chart)
2. Attacker HP Multiplier: 4/10 = 0.4
3. Terrain Defense: Plain = 0 stars = no reduction
4. Final Damage: 55% × 0.4 × 1.0 = 22%
   Damage Dealt: 2 HP

═══════════════════════════════════════════════════════════════════════

After Combat:

    🌲🌲🌲
    🌲🌲🌲
    🌲🌲🌲
       
    ░░🪖░░  ← Infantry: 4 HP remaining
       💥 Counter-attack!
    ░░░░░
    
    ░░🛡️░░  ← Tank: 8 HP remaining

═══════════════════════════════════════════════════════════════════════

Result:
- Tank dealt 6 damage (75% → 60% after defense)
- Infantry counter-attacked for 2 damage (low HP reduced damage)
- Tank won the trade (6 vs 2 damage)
- Infantry survived in forest but severely weakened

Key Lessons:
✓ Terrain matters! (Forest saved infantry from death)
✓ HP affects damage dealt (4 HP infantry = weak counter)
✓ Always check damage calculator before attacking
✓ Sometimes retreating is better than dying

═══════════════════════════════════════════════════════════════════════
```

---

## 🎯 Movement & Attack Range Example

```
═══════════════════════════════════════════════════════════════════════
                    UNIT RANGES VISUALIZATION
═══════════════════════════════════════════════════════════════════════

TANK - Selected Unit

Movement Range (shown in blue):

    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️
    🏔️░░░░░░░░🏔️
    🏔️░🟦🟦🟦🟦░░🏔️
    🏔️🟦🟦🟦🟦🟦░░🏔️
    🏔️🟦🟦🛡️🟦🟦░░🏔️  ← Tank here (Movement: 6)
    🏔️🟦🟦🟦🟦🟦░░🏔️
    🏔️░🟦🟦🟦🟦░░🏔️
    🏔️░░░░░░░░🏔️
    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

Attack Range (after moving, shown in red):

    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️
    🏔️░░░░🟥░░░🏔️
    🏔️░░░░🟥░░░🏔️
    🏔️░░░🟥🛡️🟥░░🏔️  ← If tank moves here
    🏔️░░░░🟥░░░🏔️
    🏔️░░░░░░░░🏔️
    🏔️░░░░░░░░🏔️
    🏔️░░░░░░░░🏔️
    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

═══════════════════════════════════════════════════════════════════════

ARTILLERY - Indirect Unit

Movement Range:

    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️
    🏔️░░░░░░░░░░🏔️
    🏔️░░░🟦🟦🟦░░░🏔️
    🏔️░░🟦🟦🟦🟦🟦░░🏔️
    🏔️░░🟦🟦🏻🟦🟦░░🏔️  ← Artillery (Movement: 5)
    🏔️░░🟦🟦🟦🟦🟦░░🏔️
    🏔️░░░🟦🟦🟦░░░🏔️
    🏔️░░░░░░░░░░🏔️
    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

Attack Range (Range 2-3, after moving):

    🏔️🏔️🏔️🏔️🟥🟥🟥🏔️🏔️🏔️
    🏔️🏔️🏔️🟥🟥🟥🟥🟥🏔️🏔️
    🏔️🏔️🟥🟥🟥🟥🟥🟥🟥🏔️
    🏔️🟥🟥🟥░░░░🟥🟥🟥🏔️  ← Min range 2!
    🏔️🟥🟥░░🏻░░🟥🟥🏔️  ← Artillery here
    🏔️🟥🟥🟥░░░░🟥🟥🟥🏔️
    🏔️🏔️🟥🟥🟥🟥🟥🟥🟥🏔️
    🏔️🏔️🏔️🟥🟥🟥🟥🟥🏔️🏔️
    🏔️🏔️🏔️🏔️🟥🟥🟥🏔️🏔️🏔️
    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

Note: Artillery cannot attack adjacent tiles! (Min range: 2)

═══════════════════════════════════════════════════════════════════════
```

---

## 🏘️ Capture Mechanics Example

```
═══════════════════════════════════════════════════════════════════════
                    CITY CAPTURE SEQUENCE
═══════════════════════════════════════════════════════════════════════

Day 1: Infantry arrives at neutral city

    ░░░░░
    ░🏘️🏘️🏘️
    ░🏘️🏘️🏘️  ← Neutral City
    ░🏘️🏘️🏘️
       ↓
    ░░🪖░░  ← Infantry (10 HP) - WAIT
    
    Action: Move onto city, select CAPTURE
    Capture Progress: 10 HP added (10/20)

═══════════════════════════════════════════════════════════════════════

Day 2: Continue capturing

    ░░░░░
    ░🏘️⏳🏘️  ← Capturing... (10/20)
    ░🏘️🪖🏘️  ← Infantry stays on city
    ░🏘️🏘️🏘️
    
    Action: Select CAPTURE again
    Capture Progress: +10 HP = 20/20 ✓ CAPTURED!

═══════════════════════════════════════════════════════════════════════

Day 3: City captured!

    ░░░░░
    ░🏘️🏘️🏘️
    ░🏘️🪖🏘️  ← Orange Star City (Player 1)
    ░🏘️🏘️🏘️  ← Now provides 1,000G income per turn!
                 Heals 2 HP per turn if damaged
    
    Player 1: +1,000G per turn
    Infantry can now move away safely

═══════════════════════════════════════════════════════════════════════

INTERRUPTION SCENARIO:

Day 1: Start capture (10/20)
    🏘️⏳🏘️
    🏘️🪖🏘️  ← Infantry capturing

Day 2: Enemy attacks!
    🏘️⏳🏘️
    🏘️🪖🏘️  ← Infantry (5 HP after taking damage)
        💥
    ░🛡️░  ← Enemy Tank attacked

Day 3: Continue capture
    🏘️⏳🏘️
    🏘️🪖🏘️  ← Infantry (5 HP) continues
    
    Capture Progress: 10/20 + 5 HP = 15/20
    
    Need 5 more HP to capture!
    (Capture progress based on current HP)

═══════════════════════════════════════════════════════════════════════

KEY CAPTURE RULES:

✓ Only Infantry and Mech can capture
✓ Takes 20 HP total to capture (2 turns at full HP)
✓ Capture progress = Unit's current HP
✓ Progress saved if unit leaves and returns
✓ Damaged units capture slower!
✓ Enemy can interrupt by attacking
✓ Capturing HQ = Instant Victory!

═══════════════════════════════════════════════════════════════════════
```

---

## 👨‍✈️ CO Power Activation Example

```
═══════════════════════════════════════════════════════════════════════
                    MAX'S CO POWER - "MAX FORCE"
═══════════════════════════════════════════════════════════════════════

Situation: Player stuck at chokepoint, needs breakthrough

Before CO Power:

    🏔️🏔️🏔️🌊🌊🏔️🏔️🏔️
    🏔️░░░░░░░░🏔️
    🏔️░░🛡️🛡️🛡️░░🏔️  ← Orange Tanks (Average HP)
    🏔️░░🪖🪖░░░🏔️  ← Infantry support
    🏔️░░░░░░░░🏔️
    🏔️░░░░░░░░🏔️  ← Bridge chokepoint
    🏔️░░░⛟⛟░░🏔️  ← Enemy defense line
    🏔️░░🛡️🛡️🛡️░░🏔️  ← Blue Tanks blocking
    🏔️░░░░░░░░🏔️
    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

Power Meter: ★★★☆☆☆ (3/6 stars - CO Power ready!)

═══════════════════════════════════════════════════════════════════════

MAX ACTIVATES "MAX FORCE":

    💥💥💥 CO POWER ACTIVATED! 💥💥💥
    
    Effect: All DIRECT combat units
    - +50% Attack power
    - +2 Movement range
    - Lasts this turn only!

═══════════════════════════════════════════════════════════════════════

During CO Power Turn:

    🏔️🏔️🏔️🌊🌊🏔️🏔️🏔️
    🏔️⚡⚡⚡⚡⚡⚡⚡🏔️
    🏔️⚡🛡️🛡️🛡️⚡⚡🏔️  ← Tanks boosted! +50% ATK!
    🏔️⚡🪖🪖⚡⚡⚡🏔️           +2 Movement!
    🏔️⚡⚡⚡⚡⚡⚡🏔️
    🏔️⚡⚡⚡⚡⚡⚡🏔️  ← Can reach AND destroy enemies!
    🏔️⚡⚡💀💀⚡⚡🏔️  ← Enemy Recons destroyed
    🏔️⚡⚡💀💀💀⚡🏔️  ← Enemy Tanks destroyed
    🏔️⚡⚡⚡⚡⚡⚡🏔️
    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

Actions taken:
1. Tanks moved forward (+2 range reached enemies)
2. Attacked with +50% damage (destroyed enemy line!)
3. Infantry moved up to capture opened territory

═══════════════════════════════════════════════════════════════════════

After CO Power Turn:

    🏔️🏔️🏔️🌊🌊🏔️🏔️🏔️
    🏔️░░░░░░░░🏔️
    🏔️░░░░░░░░🏔️
    🏔️░░░░░░░░🏔️
    🏔️░░🛡️🛡️🛡️░░🏔️  ← Tanks advanced!
    🏔️░░🪖🪖░░░🏔️  ← Chokepoint broken!
    🏔️░░░░░░░░🏔️  ← Enemy line destroyed
    🏔️░░░░░░░░🏔️
    🏔️░░░░░░░░🏔️
    🏔️🏔️🏔️🏔️🏔️🏔️🏔️🏔️

Result:
✓ Breakthrough achieved
✓ 4 enemy units destroyed
✓ Chokepoint secured
✓ Ready to advance on enemy HQ

Power Meter: ☆☆☆☆☆☆ (0/6 stars - reset)

═══════════════════════════════════════════════════════════════════════

CO POWER STRATEGY:

⏰ WHEN TO USE:
- Critical moment (breakthrough needed)
- Large battle with many units
- Defensive last stand
- Race for HQ capture

❌ WHEN NOT TO USE:
- Cleanup after winning
- Only 1-2 units benefit
- No immediate threat
- Could save for Super CO Power

💡 PRO TIP: Combine CO Power with mass attack!
           More units = more benefit from +50% attack

═══════════════════════════════════════════════════════════════════════
```

---

## 🌫️ Fog of War Example

```
═══════════════════════════════════════════════════════════════════════
                    FOG OF WAR - VISION MECHANICS
═══════════════════════════════════════════════════════════════════════

Player View WITH Fog of War:

    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← Unknown (black fog)
    ▓▓▓▓░░░░░░░░▓▓▓▓▓▓▓▓
    ▓▓▓░░░░░░░░░░▓▓▓▓▓▓▓
    ▓▓░░░░⛟░░░░░░▓▓▓▓▓▓  ← Recon (Vision: 5)
    ▓▓░░░░░░░░░░░░▓▓▓▓▓▓
    ▓▓░░░░░░░░░░░░░▓▓▓▓▓  ← Large vision radius
    ▓▓▓░░░░🛡️░░░░░░▓▓▓▓▓  ← Tank (Vision: 3)
    ▓▓▓▓░░░░░░░░░▓▓▓▓▓▓▓
    ▓▓▓▓▓░░░░░░░▓▓▓▓▓▓▓▓
    ▓▓▓▓▓▓░░░🪖░▓▓▓▓▓▓▓▓  ← Infantry (Vision: 2)
    ▓▓▓▓▓▓▓░░░▓▓▓▓▓▓▓▓▓▓
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

═══════════════════════════════════════════════════════════════════════

Enemy Units Hidden in Fog:

    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    ▓▓▓▓🛡️🛡️💣▓▓▓▓▓▓▓▓▓  ← Enemy tanks + artillery
    ▓▓▓▓░░░░░░░░▓▓▓▓▓▓▓▓     PLAYER CAN'T SEE!
    ▓▓▓░░░░░░░░░░▓▓▓▓▓▓▓
    ▓▓░░░░⛟░░░░░░▓▓▓▓▓▓  ← Your recon
    ▓▓░░░░░░░░░░░░▓▓▓▓▓▓
    ▓▓░░░░░░░░░░░░░▓▓▓▓▓
    ▓▓▓░░░░🛡️░░░░░░▓▓▓▓▓
    ▓▓▓▓░░░░░░░░░▓▓▓▓▓▓▓
    ▓▓▓▓▓░░░░░░░▓▓▓▓▓▓▓▓
    ▓▓▓▓▓▓░░░🪖░▓▓▓▓▓▓▓▓
    ▓▓▓▓▓▓▓🪖🪖▓▓▓▓▓▓▓▓▓  ← Enemy infantry hiding!
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     Ready to ambush!
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

═══════════════════════════════════════════════════════════════════════

STEALTH SUBMARINE EXAMPLE:

Player View:

    🌊🌊🌊🌊🌊🌊🌊🌊  ← Ocean (clear water)
    🌊🌊🌊🌊🌊🌊🌊🌊
    🌊🌊🚢🌊🌊🌊🌊🌊  ← Cruiser (can see submarines)
    🌊🌊🌊░░░🌊🌊🌊
    🌊🌊░░░░░🌊🌊🌊
    🌊🌊░░💀░░🌊🌊🌊  ← Spotted enemy sub! (Diving)
    🌊🌊░░░░░🌊🌊🌊  
    🌊🌊🌊░░░🌊🌊🌊
    🌊🌊🌊🌊🌊🌊🌊🌊

Without Cruiser:

    🌊🌊🌊🌊🌊🌊🌊🌊  ← Ocean looks clear
    🌊🌊🌊🌊🌊🌊🌊🌊
    🌊🌊🌊🌊🌊🌊🌊🌊
    🌊🌊🌊🌊🌊🌊🌊🌊  ← SUB IS HERE BUT INVISIBLE!
    🌊🌊🌊🌊🌊🌊🌊🌊     Will attack by surprise!
    🌊🌊🌊💀🌊🌊🌊🌊
    🌊🌊🌊🌊🌊🌊🌊🌊
    🌊🌊🌊🌊🌊🌊🌊🌊
    🌊🌊🌊🌊🌊🌊🌊🌊

═══════════════════════════════════════════════════════════════════════

FOG OF WAR TACTICS:

🔍 SCOUTING:
- Use Recon (5 vision) to scout ahead
- Infantry on mountains get +3 vision
- Cruisers detect submarines

🪖 AMBUSHES:
- Hide artillery in forests
- Position units outside enemy vision
- Attack from fog = surprise!

💣 BLUFFING:
- Show weak units, hide strong units
- Fake retreat, then ambush
- Mind games are key!

⚠️ DANGER ZONES:
- Never move into fog without scouting
- Assume fog contains enemies
- Artillery can fire from fog (range 2-3)

═══════════════════════════════════════════════════════════════════════
```

---

## 📊 Turn Economy Example

```
═══════════════════════════════════════════════════════════════════════
                    ECONOMIC WARFARE - TURN BY TURN
═══════════════════════════════════════════════════════════════════════

TURN 1 - Opening Moves:

Player 1 (Orange Star):
├─ Properties: 5 (HQ + 3 Bases + 1 City) = 5,000G income
├─ Starting Funds: 10,000G
├─ Build: Infantry × 3 (3,000G)
├─ Remaining: 7,000G
└─ Strategy: Infantry spam for property grab

Player 2 (Blue Moon):
├─ Properties: 5 (HQ + 3 Bases + 1 City) = 5,000G income
├─ Starting Funds: 10,000G
├─ Build: Infantry × 2 (2,000G), Recon (4,000G)
├─ Remaining: 4,000G
└─ Strategy: Infantry + scout

═══════════════════════════════════════════════════════════════════════

TURN 3 - Property Race:

Player 1:
├─ Properties: 8 (captured 3 cities!) = 8,000G income
├─ Funds: 12,000G
├─ Build: Tank (7,000G), Infantry (1,000G)
├─ Remaining: 4,000G
└─ Advantage: +3 properties = +3,000G/turn

Player 2:
├─ Properties: 5 (no captures yet) = 5,000G income
├─ Funds: 9,000G
├─ Build: Tank (7,000G)
├─ Remaining: 2,000G
└─ Disadvantage: Behind in economy!

═══════════════════════════════════════════════════════════════════════

TURN 6 - Mid Game:

Player 1:
├─ Properties: 12 = 12,000G/turn
├─ Funds: 18,000G
├─ Army Value: ~45,000G (6 tanks, 8 infantry)
├─ Build: Med Tank (16,000G)
└─ Position: Dominant economy + army

Player 2:
├─ Properties: 8 = 8,000G/turn
├─ Funds: 10,000G
├─ Army Value: ~32,000G (4 tanks, 5 infantry)
├─ Build: Artillery (6,000G) + Infantry (1,000G)
└─ Position: Defensive, trying to survive

═══════════════════════════════════════════════════════════════════════

ECONOMIC ADVANTAGE CALCULATION:

Turn 1-5 difference: +3,000G/turn × 5 turns = 15,000G advantage
Turn 6-10 difference: +4,000G/turn × 5 turns = 20,000G advantage

Total accumulated advantage: 35,000G

This translates to:
- 5 extra Tanks (35,000G / 7,000G)
- OR 2 extra Med Tanks (35,000G / 16,000G)
- OR 1 Neotank + 1 Tank

Player 1 can field significantly larger army!

═══════════════════════════════════════════════════════════════════════

KEY ECONOMIC PRINCIPLES:

💰 INCOME SOURCES:
- Each property = 1,000G/turn
- Capture early = Compound advantage
- Control 60% of properties = Usually win

📊 FUND MANAGEMENT:
- Always keep 3,000-5,000G reserve
- Don't overspend on expensive units early
- Infantry (1,000G) > saving for Neotank (22,000G)

⚔️ VALUE TRADING:
- Kill 7,000G tank with 1,000G infantry = Great trade!
- Trade evenly when ahead (preserve advantage)
- Take risky trades when behind (need to catch up)

🏘️ PROPERTY DENIAL:
- Capture enemy properties = Hurts their economy
- Protecting your properties = Preserve income
- Contested properties = High priority!

═══════════════════════════════════════════════════════════════════════

COMEBACK MECHANICS:

If behind economically:
1. Force unfavorable trades (artillery, bombers)
2. Use CO Power at critical moment
3. Rush enemy HQ (risky but can win)
4. Guerrilla tactics (hit and run)
5. Deny enemy properties (prevent snowball)

═══════════════════════════════════════════════════════════════════════
```

---

## 🎯 Summary

These visual examples demonstrate:

✅ **Map layout** - Properties, terrain, positioning  
✅ **Combat mechanics** - Damage formula in action  
✅ **Movement/Attack ranges** - Direct vs Indirect units  
✅ **Capture system** - Turn-by-turn progression  
✅ **CO Powers** - Game-changing effects  
✅ **Fog of War** - Vision, stealth, tactics  
✅ **Turn Economy** - Income, property advantage  

Every Advance Wars battle is a complex puzzle of positioning, economy, and timing! ⚔️🗺️💯
