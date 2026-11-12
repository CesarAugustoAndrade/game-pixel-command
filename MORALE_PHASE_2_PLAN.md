# Morale System - Phase 2 Enhancement Plan

## Overview
The morale-driven battle system (Phase 1) is fully functional with three-phase structure and basic combat. Phase 2 adds depth by integrating commander stats, morale-based effectiveness penalties, dueling mechanics, and tactical positioning bonuses.

## Current Status (Phase 1 - Complete)
✅ Three-phase battle structure (Skirmish → Decision → Engagement)
✅ Army-level morale pool (0-100 scale)
✅ Morale state machine (normal → shaken → critical → routing → defeated)
✅ Casualties → morale damage conversion
✅ Momentum effects (winning side gains, losing side loses)
✅ Victory rewards with multipliers

## Phase 2 Features (High Priority)

### 1. **Commander Stats Integration** (Impact: HIGH)
**Purpose**: Make commanders meaningful in battle outcomes

**Files to Modify**:
- `src/states/battle_state_morale.py` - Apply commander stats during combat
- `src/battle/morale_system.py` - Add methods to apply stat-based modifiers
- `src/battle/combat_calculator.py` - Accept morale effectiveness modifier

**Implementation Details**:

#### A. Leadership Stat (Reduces Morale Loss)
- **Effect**: Up to 25% reduction in morale damage taken (at 100 leadership)
- **Formula**: `morale_loss = base_loss * (1 - leadership * 0.0025)`
- **Application**: Reduce casualty-based morale damage
- **Example**: Alexander (98 leadership) reduces morale loss by ~24.5%

#### B. Tactics Stat (Increases Flank Damage)
- **Effect**: Up to 50% bonus damage when flanking (at 100 tactics)
- **Formula**: `flank_damage = base_damage * (1 + tactics * 0.005)`
- **Application**: Apply when attacker has flanking position
- **Example**: Alexander (95 tactics) gets ~47.5% flank bonus

#### C. Martial Prowess Stat (Personal Combat Bonus)
- **Effect**: Up to 100% bonus to commander's personal combat damage (at 100 prowess)
- **Formula**: `commander_damage = base_damage * (1 + martial_prowess * 0.01)`
- **Application**: Commander can engage in personal duels
- **Example**: Alexander (90 martial) deals 90% more damage in duels

#### D. Presence Stat (Buff Nearby Units)
- **Effect**: Up to 20% effectiveness buff to nearby units (at 100 presence)
- **Formula**: `unit_effectiveness = base * (1 + presence * 0.002)`
- **Application**: Units within 2 grid spaces of commander get bonus
- **Example**: Alexander (92 presence) buffs nearby units by ~18.4%

### 2. **Morale Effectiveness Modifier in Combat** (Impact: HIGH)
**Purpose**: Low morale hurts combat effectiveness, creating spiral dynamics

**Files to Modify**:
- `src/states/battle_state_morale.py` - Pass morale modifier to combat
- `src/battle/combat_calculator.py` - Apply modifier to damage calculations

**Implementation Details**:
- Use existing `MORALE_EFFECTIVENESS_CURVE` from `morale_constants.py`
- Curve: 100 morale = 1.0x, 50 morale = 0.85x, 0 morale = 0.1x effectiveness
- Apply to attacker damage: `final_damage = base_damage * effectiveness_modifier`
- Makes losing battles snowball (lower morale → less damage → more casualties → lower morale)

### 3. **Commander Dueling System** (Impact: MEDIUM)
**Purpose**: Allow commanders to engage in personal combat for high morale swings

**Files to Create**:
- `src/battle/dueling_system.py` - New system for commander duels

**Implementation Details**:
- Trigger conditions:
  - Player presses 'D' with commander selected
  - Select enemy commander as target
  - Duel resolves immediately
- Combat calculation:
  - Base: Commander martial prowess vs opponent martial prowess
  - Modifiers: Health, morale, equipment bonuses
  - Winner: 20 morale gain, loser: 25 morale loss (COMMANDER_DUEL_WIN/LOSS_MORALE_SWING)
  - Defeated commander: 35 morale damage to their army + unit confusion
- UI: Show duel prompt, display odds, show result with dramatic text

### 4. **Flanking Detection & Bonuses** (Impact: MEDIUM)
**Purpose**: Reward tactical positioning for increased damage

**Files to Modify**:
- `src/states/battle_state_morale.py` - Detect flanking positions
- `src/battle/position_grid.py` - Add flanking detection method

**Implementation Details**:
- Flanking definition: Attacker has allies on 2+ sides of defender
- Rear attack: Attacker on opposite side from main defender group
- Damage multipliers:
  - Flank: 1.5x damage (FLANK_DAMAGE_MULTIPLIER)
  - Rear: 2.0x damage (REAR_ATTACK_MULTIPLIER)
- Morale effects: Flanked unit takes SURROUNDED_MORALE_PENALTY (-10 morale)
- Apply morale reduction scaling from tactical_morale_constants

### 5. **Formation Bonuses** (Impact: MEDIUM)
**Purpose**: Incentivize grouped unit formations

**Files to Modify**:
- `src/states/battle_state_morale.py` - Calculate formation bonuses
- `src/battle/position_grid.py` - Detect unit groupings

**Implementation Details**:
- Formation detection: 3+ units within 2 grid spaces of each other
- Formation types:
  - **Phalanx**: Heavy units (infantry/spearman) adjacent = +15% defense
  - **Skirmish**: Light units spread = +20% movement, -10% defense
  - **Cavalry Wedge**: Cavalry + light infantry = +25% charge damage
- Duration: Formation bonus lasts until units spread out
- Visual feedback: Highlight units in formation, show "FORMATION ACTIVE"

### 6. **Army Rout & Auto-Retreat** (Impact: MEDIUM)
**Purpose**: Prevent infinite battles at 0 morale; create surrender conditions

**Files to Modify**:
- `src/states/battle_state_morale.py` - Implement rout checks
- `src/battle/morale_system.py` - Enhanced state transitions

**Implementation Details**:
- Rout trigger: Army morale ≤ ROUT_CHECK_THRESHOLD (15)
- Rout roll: Each turn, army has ROUT_CHANCE_PERCENT (25%) to rout
- Routed unit behavior:
  - Units attempt to flee (move away from enemies)
  - Can't attack or perform actions
  - -50% damage if forced to fight
- Rout consequences:
  - Battle ends (player loses)
  - Army can regroup on campaign map (50% units survive)
  - Reputation hit (if tracked)
- Surrender option: Player can surrender at low morale instead of fighting to death

### 7. **Battle Logger / Combat Feedback** (Impact: LOW-MEDIUM)
**Purpose**: Show combat events clearly for player understanding

**Files to Create/Modify**:
- `src/battle/battle_logger.py` - New logging system
- `src/states/battle_state_morale.py` - Integrate logging calls

**Implementation Details**:
- Log events:
  - Unit attacked unit → "Greek Cavalry attacks Spartan Infantry (45 damage)"
  - Flanking detected → "Flanking maneuver detected! +50% damage"
  - Morale change → "Army morale: 100 → 85 (-15 from casualties)"
  - Unit elimination → "Spartan Infantry eliminated!"
  - Commander duel → "Alexander vs Leonidas! Alexander wins (+20 morale)"
  - Formation bonus → "Phalanx formation activated (+15% defense)"
  - Army routing → "Enemy army routing! Accepting surrender..."
- Display: On-screen log (bottom-left, 5-10 most recent events)
- Scrollable history available with 'L' key

## Implementation Priority

### Tier 1 (Complete First - Most Impact)
1. **Morale Effectiveness Modifier** - Easy to add, high impact on gameplay
2. **Commander Stats Integration** - Medium effort, makes commanders matter
3. **Formation Bonuses** - Medium effort, rewards strategy

### Tier 2 (Complete Next - Polish)
4. **Flanking Detection** - Medium effort, adds tactical depth
5. **Commander Dueling** - Medium effort, dramatic moments
6. **Army Rout System** - Medium effort, prevents soft locks

### Tier 3 (Polish & Feedback)
7. **Battle Logger** - Low priority, but greatly improves UX

## Testing Strategy

### Unit Tests
```python
# Test morale effectiveness curve
assert get_morale_modifier(100) == 1.0
assert get_morale_modifier(50) == 0.85
assert get_morale_modifier(0) == 0.1

# Test commander stat scaling
assert leadership_reduction(98) ≈ 0.245  # 24.5% reduction
assert tactics_flank_bonus(95) ≈ 0.475   # 47.5% bonus

# Test flanking detection
assert is_flanking(attacker, defender, grid) == True  # 2+ allies
assert flank_damage_multiplier(defender) == 1.5
```

### Integration Tests
```python
# Full battle with morale feedback
1. Start battle at 100/100 morale
2. Take casualties, morale drops
3. At low morale, combat damage reduced (effectiveness curve)
4. Commander uses leadership to mitigate losses
5. Flank enemy, get 1.5x damage
6. Army routs at 15 morale
```

### Gameplay Tests
- ✅ Battles with low morale should be harder (damage reduced)
- ✅ Alexander should outperform other commanders (higher stats)
- ✅ Formation of 3+ units should show bonus
- ✅ Routing army should try to flee, not fight
- ✅ Commander duel should be high-stakes moment

## Estimated Effort

| Feature | Effort | Impact | Priority |
|---------|--------|--------|----------|
| Morale Effectiveness | 1-2 hours | HIGH | 1 |
| Commander Stats | 2-3 hours | HIGH | 1 |
| Formation Bonuses | 2-3 hours | HIGH | 1 |
| Flanking | 3-4 hours | MEDIUM | 2 |
| Dueling | 3-4 hours | MEDIUM | 2 |
| Rout System | 2-3 hours | MEDIUM | 2 |
| Battle Logger | 2-3 hours | LOW-MEDIUM | 3 |
| **TOTAL** | **15-20 hours** | - | - |

## Success Criteria

- [ ] Commander stats visibly affect battle outcomes
- [ ] Morale-driven spiral effect (low morale → less damage → more losses → lower morale)
- [ ] Formation bonuses encourage tactical positioning
- [ ] Flanking gives meaningful advantage
- [ ] Commander duels create dramatic moments
- [ ] Armies rout instead of fighting to death
- [ ] Battle log shows all important events clearly
- [ ] All tests passing
- [ ] No performance degradation

## Future Phase 3 (Out of Scope)

These features build on Phase 2 but are deferred:
- Commander abilities (Companion Charge, Hammer & Anvil)
- Special unit types with unique mechanics
- Environmental effects (weather, terrain effects)
- Multi-battle campaigns with army recovery
- Morale state effects on unit rendering
- Sound effects for critical events
- Animated morale bars

## Notes

- Commander stats are already defined in `commander_data.py`
- Morale constants already include all needed values
- Position grid system supports flanking detection
- Combat calculator can be extended for modifiers
- All UI components ready for log display
