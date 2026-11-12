# Next Steps for Morale System Development

## Current State
- ✅ Phase 1: Complete three-phase morale battle system
- ✅ Phase 2 (Partial): Morale effectiveness + Leadership stats implemented
- ⏳ Phase 2 (Remaining): 5 more features to implement

## Immediate Actions

### 1. Test Current Implementation
Run the game and verify Phase 2 changes work:
```bash
python main.py
```

**What to Look For**:
- ✅ Battles still start and complete without errors
- ✅ Morale bar updates correctly during combat
- ✅ Victory rewards still calculated
- ✅ Campaign map still responds to input

### 2. Verify Morale Effectiveness
During an engagement phase:
- Watch unit damage numbers
- At 100 morale: damage should be normal
- At 50 morale: damage should be ~15% reduced (0.85x)
- At 20 morale: damage should be ~50% reduced (0.5x)

### 3. Verify Leadership Mitigation
- Alexander should have better morale defense than default enemies
- After taking casualties, morale should drop less with good leadership

## Phase 2 Remaining Work

### Priority 1: Formation Bonuses
**Effort**: 2-3 hours | **Impact**: HIGH

When to implement: Next (highest value for effort)

**What it does**:
- 3+ units grouped together get bonuses
- Phalanx (heavy units): +15% defense
- Skirmish (light units): +20% movement, -10% defense
- Cavalry Wedge (cavalry + light): +25% charge damage

**Files to modify**:
- `src/states/battle_state_morale.py` - Add formation detection in update loop
- `src/battle/position_grid.py` - Add formation detection method
- `src/core/morale_constants.py` - Add formation bonus constants (if not present)

**Entry point**: After _apply_momentum_effects(), add _apply_formation_bonuses()

### Priority 2: Flanking Detection
**Effort**: 3-4 hours | **Impact**: MEDIUM-HIGH

When to implement: After formations

**What it does**:
- Detect when attacker has allies on 2+ sides of defender
- Increase damage by 1.5x (regular flank) or 2.0x (rear)
- Apply Tactics stat bonus to flank damage

**Files to modify**:
- `src/states/battle_state_morale.py` - Add flanking detection in _execute_morale_combat()
- `src/battle/position_grid.py` - Add flanking detection method
- `src/battle/morale_system.py` - Already has get_tactics_flank_bonus()

**Entry point**: In _execute_morale_combat(), after morale effectiveness but before casualty application

### Priority 3: Commander Dueling
**Effort**: 3-4 hours | **Impact**: MEDIUM

When to implement: After flanking

**What it does**:
- Commanders can engage in personal combat
- Martial Prowess stat affects duel outcome
- Winner gets morale swing (+20), loser gets (-25)
- Defeated commander: -35 morale to army, units confused

**Files to create**:
- `src/battle/dueling_system.py` - New duel resolution system

**Files to modify**:
- `src/states/battle_state_morale.py` - Add duel handler
- `src/battle/morale_system.py` - Already has duel morale methods

**Entry point**: In _handle_engagement_input(), add 'D' key for duel

### Priority 4: Army Rout System
**Effort**: 2-3 hours | **Impact**: MEDIUM

When to implement: After dueling

**What it does**:
- At morale ≤ 15, army has 25% chance per turn to rout
- Routed units flee instead of fight
- Battle ends with partial army survival

**Files to modify**:
- `src/states/battle_state_morale.py` - Add rout check in _check_victory()
- `src/battle/morale_system.py` - Already has rout mechanics

**Entry point**: In _check_victory(), after morale collapse check

### Priority 5: Presence Buff
**Effort**: 2-3 hours | **Impact**: MEDIUM

When to implement: After formations (can be parallel)

**What it does**:
- Units within 2 grid spaces of commander get effectiveness buff
- At 100 presence: +20% effectiveness
- Stacks with morale effectiveness

**Files to modify**:
- `src/states/battle_state_morale.py` - Add presence buff calculation
- `src/battle/morale_system.py` - Already has get_presence_buff()

**Entry point**: In _execute_morale_combat(), after all other modifiers

### Priority 6: Battle Logger
**Effort**: 2-3 hours | **Impact**: LOW-MEDIUM

When to implement: Last (polish/UX)

**What it does**:
- Log all battle events
- Display last 5-10 events on screen
- Show detailed combat feedback

**Files to create**:
- `src/battle/battle_logger.py` - New logging system

**Files to modify**:
- `src/states/battle_state_morale.py` - Add log calls throughout

**Entry point**: Initialize logger in __init__(), log events in every action

## Implementation Roadmap

### Week 1
- [ ] Formation Bonuses (Thurs)
- [ ] Flanking Detection (Fri-Sat)

### Week 2
- [ ] Commander Dueling (Mon-Tue)
- [ ] Army Rout System (Wed)
- [ ] Presence Buff (Thu)

### Week 3
- [ ] Battle Logger (Mon-Tue)
- [ ] Playtesting & Balance (Wed-Fri)
- [ ] Polish & Optimization (Fri-Sat)

## Code Patterns to Follow

### Adding a New Effect

1. **Define Constants** in `morale_constants.py`
2. **Add Method** to `morale_system.py` (if system-level)
3. **Call Method** in `battle_state_morale.py` (in combat flow)
4. **Test Thoroughly** before moving on

### Example: Formation Bonuses
```python
# Step 1: Constants
PHALANX_DEFENSE_BONUS = 0.15
SKIRMISH_MOVEMENT_BONUS = 0.20

# Step 2: Method in morale_system.py
def apply_formation_bonus(self, unit, formation_type):
    """Apply formation bonuses"""
    if formation_type == "phalanx":
        return PHALANX_DEFENSE_BONUS
    # ...

# Step 3: Call in battle_state_morale.py
formation = self._detect_formation(unit)
bonus = self.morale_system.apply_formation_bonus(unit, formation)

# Step 4: Test
assert get_formation_bonus("phalanx") == 0.15
```

## Testing Each Feature

### Formation Bonuses
- [ ] 3+ units grouped together get bonus
- [ ] Phalanx formations actually reduce damage taken
- [ ] Breaking formation removes bonus
- [ ] Only valid unit types get formation bonuses

### Flanking Detection
- [ ] Flanking multiplier applies correctly (1.5x)
- [ ] Rear attacks apply (2.0x)
- [ ] Tactics stat increases flank damage
- [ ] Non-flanking attacks unaffected

### Commander Dueling
- [ ] Duels can be initiated
- [ ] Martial Prowess affects duel outcome
- [ ] Morale swings are correct (+20/-25)
- [ ] Defeated commander causes army morale penalty

### Army Rout
- [ ] At morale ≤ 15, rout checks trigger
- [ ] Routed units flee (move away)
- [ ] Routed units can't attack
- [ ] Battle ends correctly on rout

### Presence Buff
- [ ] Units near commander get buff
- [ ] Buff scales with Presence stat
- [ ] Buff stacks with morale effectiveness
- [ ] Buff removed when out of range

### Battle Logger
- [ ] All events logged
- [ ] Display shows recent events
- [ ] Log doesn't impact performance
- [ ] Can scroll through history

## Common Pitfalls to Avoid

1. **Forgetting to check unit alive status** before applying effects
2. **Wrong army assignment** when applying morale (player vs enemy)
3. **Double-applying modifiers** (morale + effectiveness + formation)
4. **Forgetting to handle ties** in comparison logic
5. **Not updating rendering** when state changes

## Resources Available

- `MORALE_PHASE_2_PLAN.md` - Detailed design document
- `MORALE_SYSTEM_OVERVIEW.md` - Architecture and integration points
- `MORALE_PHASE_2_STATUS.md` - Current implementation status
- `src/core/morale_constants.py` - All parametrized values
- `src/battle/morale_system.py` - Core morale logic

## Quick Reference: File Locations

| Feature | File | Lines |
|---------|------|-------|
| Morale states | morale_system.py | 264-290 |
| Effectiveness curve | morale_constants.py | 132-141 |
| Casualty morale loss | battle_state_morale.py | 543-562 |
| Momentum effects | morale_system.py | 418-448 |
| Commander stats | commander_data.py | 24-30 |
| Leadership methods | morale_system.py | 493-576 |
| Position grid | position_grid.py | Full file |
| Combat resolution | battle_state_morale.py | 509-583 |

## Questions to Ask When Stuck

1. **Is the unit still alive?** Check `unit.is_alive()`
2. **Which army is this?** Check `if unit in self.player_army.units`
3. **What morale value is used?** Check `morale_system.get_army_morale(army)`
4. **Are constants defined?** Check `morale_constants.py`
5. **Is it a dict or Unit object?** Check `_unit_to_dict()` conversion

## Success Criteria for Phase 2

- [ ] All 5 remaining features implemented
- [ ] 50+ playtesting hours completed
- [ ] No crashes or infinite loops
- [ ] All features feel balanced
- [ ] Performance acceptable (60 FPS)
- [ ] New players understand morale importance
- [ ] Speedrunners find optimal strategies

## Victory Conditions

Upon completion of Phase 2, the morale system will have:

✅ Strategic depth comparable to professional wargames
✅ Meaningful commander differentiation
✅ Interesting tactical choices
✅ Clear feedback on game state
✅ Balanced difficulty curve
✅ Replayability through varied strategies

---

**Ready to start?** Pick Formation Bonuses first - it's the quickest win with high impact!
