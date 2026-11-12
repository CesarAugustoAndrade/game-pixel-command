"""
Historical unit type definitions with stats and attributes.
"""

UNIT_DEFINITIONS = {
    # Infantry Units
    "roman_legionary": {
        "name": "Roman Legionary",
        "type": "infantry",
        "description": "Elite heavy infantry of Rome, masters of formation combat",
        "attack": 14,
        "defense": 16,
        "health": 130,
        "armor": 6,
        "morale": 90,
        "movement": 3,
        "range": 1,
        "cost": 150,
        "upkeep": 10,
        "special_abilities": ["testudo_formation", "pilum_throw"],
    },
    "greek_hoplite": {
        "name": "Greek Hoplite",
        "type": "spearman",
        "description": "Disciplined spearmen fighting in phalanx formation",
        "attack": 12,
        "defense": 18,
        "health": 120,
        "armor": 7,
        "morale": 85,
        "movement": 2,
        "range": 1,
        "cost": 140,
        "upkeep": 9,
        "special_abilities": ["phalanx", "shield_wall"],
    },
    "persian_immortal": {
        "name": "Persian Immortal",
        "type": "infantry",
        "description": "Elite Persian warriors, never fewer than 10,000",
        "attack": 15,
        "defense": 14,
        "health": 125,
        "armor": 5,
        "morale": 95,
        "movement": 3,
        "range": 2,
        "cost": 160,
        "upkeep": 11,
        "special_abilities": ["bow_and_spear", "immortal_will"],
    },
    # Cavalry Units
    "companion_cavalry": {
        "name": "Companion Cavalry",
        "type": "cavalry",
        "description": "Alexander's elite shock cavalry",
        "attack": 18,
        "defense": 10,
        "health": 110,
        "armor": 4,
        "morale": 90,
        "movement": 5,
        "range": 1,
        "cost": 200,
        "upkeep": 15,
        "special_abilities": ["wedge_charge", "devastating_impact"],
    },
    "numidian_cavalry": {
        "name": "Numidian Cavalry",
        "type": "cavalry",
        "description": "Light cavalry from North Africa, masters of skirmishing",
        "attack": 14,
        "defense": 8,
        "health": 90,
        "armor": 2,
        "morale": 75,
        "movement": 6,
        "range": 1,
        "cost": 120,
        "upkeep": 8,
        "special_abilities": ["hit_and_run", "feigned_retreat"],
    },
    # Ranged Units
    "cretan_archer": {
        "name": "Cretan Archer",
        "type": "archer",
        "description": "Renowned archers from Crete",
        "attack": 16,
        "defense": 7,
        "health": 75,
        "armor": 1,
        "morale": 70,
        "movement": 3,
        "range": 4,
        "cost": 100,
        "upkeep": 7,
        "special_abilities": ["precision_shot", "flaming_arrows"],
    },
    "persian_archer": {
        "name": "Persian Archer",
        "type": "archer",
        "description": "Composite bow masters from Persia",
        "attack": 15,
        "defense": 6,
        "health": 70,
        "armor": 2,
        "morale": 65,
        "movement": 3,
        "range": 4,
        "cost": 90,
        "upkeep": 6,
        "special_abilities": ["arrow_storm", "mobile_archery"],
    },
    # Special Units
    "war_elephant": {
        "name": "War Elephant",
        "type": "monster",
        "description": "Massive war elephants that terrify infantry",
        "attack": 22,
        "defense": 20,
        "health": 300,
        "armor": 10,
        "morale": 100,
        "movement": 3,
        "range": 1,
        "cost": 400,
        "upkeep": 30,
        "special_abilities": ["trample", "terror"],
    },
    # Greek Units
    "spartan_champion": {
        "name": "Spartan Champion",
        "type": "spearman",
        "description": "Elite Spartan warriors trained from childhood in the agoge",
        "attack": 18,
        "defense": 22,
        "health": 130,
        "armor": 8,
        "morale": 100,
        "movement": 3,
        "range": 1,
        "cost": 200,
        "upkeep": 15,
        "special_abilities": ["laconic_discipline", "spartan_phalanx", "stand_and_die", "lambda_shield"],
    },
    "peltast": {
        "name": "Peltast",
        "type": "infantry",
        "description": "Light skirmisher armed with javelins and crescent shield",
        "attack": 12,
        "defense": 9,
        "health": 65,
        "armor": 1,
        "morale": 70,
        "movement": 5,
        "range": 3,
        "cost": 40,
        "upkeep": 3,
        "special_abilities": ["skirmisher_tactics", "hit_and_run", "javelin_storm"],
    },
    "rhodian_slinger": {
        "name": "Rhodian Slinger",
        "type": "archer",
        "description": "Expert slingers from Rhodes with deadly accuracy",
        "attack": 11,
        "defense": 7,
        "health": 60,
        "armor": 0,
        "morale": 65,
        "movement": 4,
        "range": 4,
        "cost": 40,
        "upkeep": 4,
        "special_abilities": ["outrange", "accurate_bombardment", "suppress_archers"],
    },
    "prodromoi": {
        "name": "Prodromoi",
        "type": "cavalry",
        "description": "Light scout cavalry armed with javelins",
        "attack": 13,
        "defense": 11,
        "health": 75,
        "armor": 2,
        "morale": 75,
        "movement": 7,
        "range": 2,
        "cost": 95,
        "upkeep": 7,
        "special_abilities": ["scouting", "swift_strike", "pursuit"],
    },
    "thessalian_cavalry": {
        "name": "Thessalian Cavalry",
        "type": "cavalry",
        "description": "Heavy shock cavalry from the plains of Thessaly",
        "attack": 17,
        "defense": 14,
        "health": 90,
        "armor": 4,
        "morale": 85,
        "movement": 6,
        "range": 1,
        "cost": 150,
        "upkeep": 12,
        "special_abilities": ["devastating_charge", "hammer_and_anvil", "noble_warriors"],
    },
    "sacred_band": {
        "name": "Sacred Band",
        "type": "infantry",
        "description": "Elite Theban warriors, 150 pairs of lovers fighting as one",
        "attack": 20,
        "defense": 20,
        "health": 120,
        "armor": 7,
        "morale": 100,
        "movement": 4,
        "range": 1,
        "cost": 220,
        "upkeep": 18,
        "special_abilities": ["paired_lovers", "unbreakable_bond", "oblique_order", "inspire_heroism"],
    },
}


def get_unit_definition(unit_id: str) -> dict:
    """
    Get unit definition by ID.

    Args:
        unit_id: Unit type ID

    Returns:
        Unit definition dict
    """
    return UNIT_DEFINITIONS.get(unit_id, {})


def get_units_by_faction(faction: str) -> list:
    """
    Get available unit types for a faction.

    Args:
        faction: Faction name

    Returns:
        List of unit IDs
    """
    faction_units = {
        "rome": ["roman_legionary", "cretan_archer", "numidian_cavalry"],
        "greece": ["greek_hoplite", "spartan_champion", "peltast", "cretan_archer", "rhodian_slinger", "prodromoi", "thessalian_cavalry", "companion_cavalry", "sacred_band"],
        "persia": ["persian_immortal", "persian_archer", "war_elephant"],
        "carthage": ["greek_hoplite", "numidian_cavalry", "war_elephant"],
    }

    return faction_units.get(faction, [])
