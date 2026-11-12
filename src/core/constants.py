"""
Game constants and configuration values.
"""

# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Classical Army Roguelite"

# Grid/Battle settings
HEX_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15

# UI Colors (RGB)
COLOR_BACKGROUND = (20, 20, 30)
COLOR_UI_PRIMARY = (180, 150, 100)
COLOR_UI_SECONDARY = (100, 80, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DARK = (50, 50, 50)
COLOR_BUTTON_HOVER = (200, 170, 120)
COLOR_GRID = (100, 100, 120)

# Faction colors
FACTION_COLORS = {
    "rome": (200, 50, 50),
    "greece": (50, 100, 200),
    "persia": (150, 100, 200),
    "carthage": (100, 200, 100),
}

# Game states
STATE_MAIN_MENU = "main_menu"
STATE_CAMPAIGN_MAP = "campaign_map"
STATE_BATTLE = "battle"
STATE_ARMY_MANAGEMENT = "army_management"
STATE_PAUSE = "pause"

# Combat constants (Advance Wars style - deterministic)
# Unit type matchup damage percentages (attacker vs defender)
UNIT_MATCHUPS = {
    "cavalry": {
        "archer": 120,      # Cavalry counters archers hard
        "infantry": 85,     # Infantry defends okay vs cavalry
        "spearman": 55,     # Spearmen HARD counter cavalry
        "cavalry": 100,     # Even matchup
        "monster": 40,      # Elephants scary
    },
    "archer": {
        "cavalry": 45,      # Weak vs cavalry charges
        "infantry": 105,    # Good vs unarmored infantry
        "spearman": 80,     # Spearmen have shields
        "archer": 100,      # Even matchup
        "monster": 30,      # Can't penetrate thick hide
    },
    "infantry": {
        "cavalry": 70,      # Vulnerable to charges
        "archer": 95,       # Armor helps vs arrows
        "spearman": 110,    # Swords beat spears up close
        "infantry": 100,    # Even matchup
        "monster": 50,      # Tough fight
    },
    "spearman": {
        "cavalry": 130,     # Anti-cavalry specialists
        "archer": 70,       # Vulnerable to ranged
        "infantry": 90,     # Swords can get inside reach
        "spearman": 100,    # Even matchup
        "monster": 60,      # Long spears help somewhat
    },
    "monster": {
        "cavalry": 110,     # Tramples horses
        "archer": 140,      # Dominates light troops
        "infantry": 125,    # Crushes infantry
        "spearman": 115,    # Hard to stop
        "monster": 100,     # Even matchup
    },
}

# Terrain defense stars (each star = 10% damage reduction) - Advance Wars style
TERRAIN_DEFENSE_STARS = {
    "plains": 0,        # No bonus - open terrain
    "forest": 2,        # 20% damage reduction - cover from trees
    "hills": 3,         # 30% damage reduction - elevation advantage
    "mountains": 4,     # 40% damage reduction - fortified high ground
    "water": 0,         # No bonus (impassable to most units)
}

# Simplified morale states and modifiers
MORALE_STATES = {
    "high_morale": {    # 3+ allies nearby, high HP
        "damage_bonus": 1.15,   # +15% damage
        "defense_bonus": 1.1,   # +10% defense
    },
    "normal": {
        "damage_bonus": 1.0,
        "defense_bonus": 1.0,
    },
    "shaken": {         # Unit below 50% HP
        "damage_bonus": 0.9,    # -10% damage
        "defense_bonus": 0.9,   # -10% defense
    },
    "broken": {         # Unit below 25% HP or isolated
        "damage_bonus": 0.75,   # -25% damage
        "defense_bonus": 0.85,  # -15% defense
    },
}

# Morale system
MORALE_MAX = 100
MORALE_BREAK_THRESHOLD = 30
MORALE_ROUT_THRESHOLD = 10
MORALE_LOSS_ON_DEATH = 5
MORALE_GAIN_ON_KILL = 3

# Unit movement
MOVEMENT_POINTS_BASE = 3
TERRAIN_MOVEMENT_COST = {
    "plains": 1,
    "forest": 2,
    "hills": 2,
    "mountains": 3,
    "water": 999,  # Impassable by default
}

# File paths
PATH_ASSETS = "assets"
PATH_SPRITES = "assets/sprites"
PATH_SOUNDS = "assets/sounds"
PATH_MUSIC = "assets/music"
PATH_DATA = "assets/data"
PATH_SAVES = "saves"

# Debug settings
DEBUG_MODE = False
DEBUG_SHOW_GRID = True
DEBUG_SHOW_FPS = True
DEBUG_SHOW_PATHS = False
