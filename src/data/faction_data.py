"""
Faction definitions and bonuses.
"""

FACTION_DATA = {
    "rome": {
        "name": "Roman Republic",
        "description": "Masters of discipline and engineering",
        "color": (200, 50, 50),
        "bonuses": {
            "infantry_defense": 1.1,
            "morale": 1.1,
            "construction_speed": 1.2,
        },
        "unique_units": ["roman_legionary"],
        "starting_resources": {
            "gold": 500,
            "food": 200,
        },
    },
    "greece": {
        "name": "Greek City-States",
        "description": "Disciplined phalanx formations and citizen militias",
        "color": (50, 100, 200),
        "bonuses": {
            "spearman_defense": 1.2,
            "phalanx_bonus": 1.3,
            "experience_gain": 1.15,
            "formation_bonus": 1.15,
        },
        "unique_units": ["greek_hoplite", "spartan_champion", "sacred_band", "thessalian_cavalry"],
        "starting_resources": {
            "gold": 450,
            "food": 180,
        },
    },
    "persia": {
        "name": "Persian Empire",
        "description": "Vast empire with diverse troops and skilled archers",
        "color": (150, 100, 200),
        "bonuses": {
            "archer_damage": 1.15,
            "archer_range": 1,
            "army_size": 1.2,
        },
        "unique_units": ["persian_immortal", "persian_archer"],
        "starting_resources": {
            "gold": 600,
            "food": 150,
        },
    },
    "carthage": {
        "name": "Carthage",
        "description": "Maritime traders with mercenary armies and war elephants",
        "color": (100, 200, 100),
        "bonuses": {
            "mercenary_cost": 0.85,
            "cavalry_speed": 1.1,
            "gold_income": 1.2,
        },
        "unique_units": ["war_elephant"],
        "starting_resources": {
            "gold": 700,
            "food": 120,
        },
    },
}


def get_faction_data(faction: str) -> dict:
    """
    Get faction data by name.

    Args:
        faction: Faction name

    Returns:
        Faction data dict
    """
    return FACTION_DATA.get(faction, {})


def get_faction_bonus(faction: str, bonus_type: str) -> float:
    """
    Get a specific bonus for a faction.

    Args:
        faction: Faction name
        bonus_type: Type of bonus

    Returns:
        Bonus multiplier (1.0 = no bonus)
    """
    faction_data = get_faction_data(faction)
    bonuses = faction_data.get("bonuses", {})
    return bonuses.get(bonus_type, 1.0)
