"""
Morale-driven warfare system constants.
All parametrized values for the three-phase morale battle system.
"""

# ============================================================================
# CORE MORALE SYSTEM
# ============================================================================

# Morale pool limits
MORALE_MAX = 100  # Starting morale for both armies
MORALE_CRITICAL_THRESHOLD = 25  # Below this: units slower, miss more, reduced effectiveness
MORALE_ZERO = 0  # Army retreats in defeat

# Morale thresholds
MORALE_BREAK_THRESHOLD = 40  # Units start becoming demoralized
MORALE_ROUT_THRESHOLD = 20  # Rout checks begin
ROUT_CHECK_THRESHOLD = 15  # Route checks trigger at this morale
MORALE_GAP_DOMINANCE_THRESHOLD = 30  # If gap exceeds this, losing army suffers penalties

# Morale bleed
MORALE_BLEED_RATE = 2  # Per turn morale loss when losing momentum
MORALE_TURN_LIMIT_PERCENT = 50  # Desperation timer (if morale < this for N turns)

# ============================================================================
# PHASE 1: SKIRMISH
# ============================================================================

# Deployment
SKIRMISHER_DEPLOYMENT_COUNT = 2  # Units per side in skirmish phase
SKIRMISH_DURATION = 5  # Time units for skirmish resolution

# Combat parameters
SKIRMISHER_BASE_DAMAGE = 10  # Base damage per skirmisher
SKIRMISHER_ACCURACY = 0.75  # Hit chance (75%)

# Morale outcomes
SKIRMISH_WIN_MORALE_BONUS = 10  # Winner gains this morale
SKIRMISH_LOSS_MORALE_DAMAGE = 15  # Loser loses this morale
SKIRMISH_PURSUIT_UNIT_COUNT = 2  # Units winner can activate for pursuit

# ============================================================================
# PHASE 2: DECISION POINT
# ============================================================================

# Option A: Retreat & Stabilize (Defensive)
DEFENSIVE_POSITION_DAMAGE_REDUCTION = 0.3  # 30% damage reduction
COMMANDER_DEFENSIVE_MULTIPLIER = 1.5  # Commander defensive bonuses scale by this

# Option B: Counter-Commit (Aggressive)
COUNTER_COMMIT_UNIT_COUNT = 3  # Units deployed for counter-commit
COUNTERCOMMIT_WIN_MORALE_SWING = 25  # Morale gained if win
COUNTERCOMMIT_LOSS_MORALE_PENALTY = 30  # Morale lost if lose (catastrophic)

# Option C: Selective Engagement (Tactical)
SELECTIVE_UNIT_COUNT = 2  # Elite/reserve units committed
SELECTIVE_WIN_MORALE_GAIN = 15  # Morale gained if win
SELECTIVE_LOSS_MORALE_HIT = 10  # Morale lost if lose
UNIT_ELITE_BONUS = 1.3  # Elite units are 30% more effective

# ============================================================================
# PHASE 3: ENGAGEMENT (Power Phase)
# ============================================================================

# Commander stats and effects
COMMANDER_LEADERSHIP = 100  # Max leadership stat (0-100)
COMMANDER_TACTICS = 100  # Max tactics stat (0-100)
COMMANDER_MARTIAL_PROWESS = 100  # Max martial prowess (0-100)
COMMANDER_PRESENCE = 100  # Max presence stat (0-100)

# Commander stat scaling
COMMANDER_STAT_SCALING_FACTOR = 0.01  # Each point = 1% effect
LEADERSHIP_MITIGATION_PERCENT = 0.25  # Max 25% morale loss reduction (at 100 Leadership)
TACTICS_FLANK_MULTIPLIER = 1.5  # Max 50% flank damage bonus (at 100 Tactics)
MARTIAL_DAMAGE_MULTIPLIER = 2.0  # Max 100% personal damage bonus (at 100 Martial)
PRESENCE_BUFF_PERCENT = 0.20  # Max 20% buff to nearby units (at 100 Presence)

# Commander dueling
COMMANDER_DUEL_WIN_MORALE_SWING = 20  # Morale gained for winning duel
COMMANDER_DUEL_LOSS_MORALE_PENALTY = 25  # Morale lost for losing duel
COMMANDER_DEFEAT_MORALE_DAMAGE = 35  # Morale damage if commander eliminated
UNIT_CONFUSION_DURATION = 2  # Turns units confused after commander loss

# ============================================================================
# UNIT TYPES & STATS
# ============================================================================

# Heavy Infantry
HEAVY_INFANTRY_HP = 150
HEAVY_INFANTRY_DAMAGE = 25
HEAVY_INFANTRY_ARMOR = 10
HEAVY_INFANTRY_SPEED = 2

# Light Infantry / Skirmishers
LIGHT_INFANTRY_HP = 80
LIGHT_INFANTRY_DAMAGE = 15
LIGHT_INFANTRY_SPEED = 4
MORALE_DAMAGE_PER_HIT = 2  # Light infantry inflicts morale damage

# Cavalry
CAVALRY_HP = 100
CAVALRY_DAMAGE = 30
CAVALRY_SPEED = 6
CAVALRY_CHARGE_DAMAGE_MULTIPLIER = 2.0  # Double damage on charge
CAVALRY_MORALE_PRESSURE = 5  # Morale damage from cavalry presence

# Archers
ARCHER_HP = 60
ARCHER_DAMAGE = 20
ARCHER_RANGE = 400  # pixels
ARCHER_CLOSE_COMBAT_PENALTY = 0.5  # 50% effectiveness in melee

# Unit effectiveness matrix (multipliers)
ARCHER_EFFECTIVENESS_VS_HEAVY = 0.8  # Archers 80% vs heavy armor
SPEAR_EFFECTIVENESS_VS_CAVALRY = 1.4  # Spears 140% vs cavalry
CAVALRY_EFFECTIVENESS_VS_ARCHER = 1.3  # Cavalry 130% vs archers
HEAVY_EFFECTIVENESS_VS_LIGHT = 1.2  # Heavy 120% vs light

# ============================================================================
# COMBAT MODIFIERS
# ============================================================================

# Positioning
FLANK_DAMAGE_MULTIPLIER = 1.5  # 50% bonus damage from flank
REAR_ATTACK_MULTIPLIER = 2.0  # 100% bonus damage from rear
SURROUNDED_MORALE_PENALTY = 10  # Morale damage when surrounded

# Momentum system
MOMENTUM_MORALE_GAIN_PER_TURN = 3  # Winning side gains per turn
MOMENTUM_MORALE_LOSS_PER_TURN = 5  # Losing side loses per turn

# Morale effectiveness curve
MORALE_EFFECTIVENESS_CURVE = {
    100: 1.0,  # Full effectiveness
    75: 0.95,
    50: 0.85,
    MORALE_CRITICAL_THRESHOLD: 0.70,  # 30% penalty
    MORALE_ROUT_THRESHOLD: 0.50,  # 50% penalty
    10: 0.30,  # 70% penalty
    0: 0.10,  # 90% penalty (barely functional)
}

# Demoralized states
DEMORALIZED_EFFECTIVENESS_PENALTY = 0.3  # 30% penalty when demoralized
ROUT_CHANCE_PERCENT = 0.25  # 25% chance per turn to rout at low morale

# ============================================================================
# MORALE DAMAGE SOURCES
# ============================================================================

# Base morale losses
BASE_UNIT_MORALE_LOSS = 5  # Base morale loss per unit eliminated
UNIT_TIER_MULTIPLIER = {
    "basic": 1.0,
    "veteran": 1.5,
    "elite": 2.0,
    "legendary": 3.0,
}

# Tactical outcomes
CHARGE_MORALE_DAMAGE = 10  # Successful cavalry charge
FAILED_DEFENSE_MORALE_DAMAGE = 12  # Failed to hold defensive position
FLANK_SUCCESS_MORALE_DAMAGE = 8  # Successful flanking maneuver
AMBUSH_MORALE_DAMAGE = 15  # Successful ambush

# Cascading effects
MORALE_CASCADE_THRESHOLD = 40  # Below this, morale losses increase
MORALE_CASCADE_MULTIPLIER = 1.5  # 50% more morale loss below threshold

# ============================================================================
# VICTORY CONDITIONS
# ============================================================================

# Victory types
VICTORY_MORALE_COLLAPSE = "morale_collapse"  # Enemy morale = 0
VICTORY_ELIMINATION = "elimination"  # All enemy units destroyed
VICTORY_ROUT = "rout"  # Commander defeated + low morale
VICTORY_TERRITORIAL = "territorial"  # Extended game mode

# Victory rewards multipliers
MORALE_VICTORY_REWARD_MULTIPLIER = 1.3  # 30% bonus for morale victory
ELIMINATION_VICTORY_REWARD_MULTIPLIER = 1.5  # 50% bonus for total elimination
FLAWLESS_VICTORY_MULTIPLIER = 2.0  # Double rewards if no morale lost

# ============================================================================
# AI DECISION WEIGHTS
# ============================================================================

# Decision point AI weights (for enemy choices)
AI_RETREAT_WEIGHT_BASE = 1.0
AI_COUNTER_COMMIT_WEIGHT_BASE = 1.5  # AI slightly favors aggression
AI_SELECTIVE_WEIGHT_BASE = 1.2

# Modifiers based on morale state
AI_DESPERATE_AGGRESSION_BONUS = 2.0  # When morale < 30, AI more likely to commit
AI_CAUTIOUS_RETREAT_BONUS = 1.5  # When morale > 60, AI more likely to stabilize

# Commander personality modifiers
AI_AGGRESSIVE_COMMANDER_WEIGHT = 2.0
AI_DEFENSIVE_COMMANDER_WEIGHT = 0.5
AI_BALANCED_COMMANDER_WEIGHT = 1.0

# ============================================================================
# TUNING PARAMETERS
# ============================================================================

# Balance knobs (adjust these for testing)
GLOBAL_MORALE_DAMAGE_MULTIPLIER = 1.0  # Scale all morale damage
GLOBAL_MORALE_RECOVERY_MULTIPLIER = 1.0  # Scale morale recovery
COMMANDER_STAT_POWER_SCALING = 1.0  # Scale commander stat effects
UNIT_EFFECTIVENESS_SCALING = 1.0  # Scale unit matchup bonuses

# Game feel
MORALE_DAMAGE_ANIMATION_DURATION = 0.5  # Seconds for morale damage popup
PHASE_TRANSITION_DELAY = 1.0  # Seconds between phases
DECISION_TIMER_DURATION = 30.0  # Seconds to make decision (0 = unlimited)

# Debug flags
DEBUG_MORALE_SYSTEM = False  # Print morale calculations
DEBUG_PHASE_TRANSITIONS = False  # Print phase changes
DEBUG_COMMANDER_STATS = False  # Print commander effects
