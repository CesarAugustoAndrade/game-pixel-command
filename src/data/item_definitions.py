"""
Item definitions for weapons, armor, and special equipment.
All items are historically accurate for the Classical Age.
"""

from typing import Dict, List

# Item rarities affect stat multipliers
ITEM_RARITIES = {
    "common": {
        "color": (200, 200, 200),
        "stat_multiplier": 1.0,
        "drop_weight": 60,
    },
    "rare": {
        "color": (100, 150, 255),
        "stat_multiplier": 1.3,
        "drop_weight": 25,
    },
    "epic": {
        "color": (200, 100, 255),
        "stat_multiplier": 1.6,
        "drop_weight": 12,
    },
    "legendary": {
        "color": (255, 180, 50),
        "stat_multiplier": 2.0,
        "drop_weight": 3,
    },
}

# Weapon Definitions
WEAPON_TEMPLATES = {
    # Swords
    "gladius": {
        "name": "Gladius",
        "type": "sword",
        "description": "Roman short sword, deadly in close combat",
        "attack_bonus": 2,
        "defense_bonus": 1,
        "required_unit_types": ["infantry", "spearman", "cavalry"],
        "historical_note": "Standard weapon of the Roman legionary",
    },
    "xiphos": {
        "name": "Xiphos",
        "type": "sword",
        "description": "Greek short sword with leaf-shaped blade",
        "attack_bonus": 2,
        "defense_bonus": 0,
        "damage_bonus": 1,
        "required_unit_types": ["infantry", "spearman"],
        "historical_note": "Secondary weapon of Greek hoplites",
    },
    "kopis": {
        "name": "Kopis",
        "type": "sword",
        "description": "Curved forward-slashing Greek sword",
        "attack_bonus": 3,
        "defense_bonus": 0,
        "morale_bonus": 5,
        "required_unit_types": ["cavalry", "infantry"],
        "historical_note": "Favored by cavalry for its slashing power",
    },
    "falcata": {
        "name": "Falcata",
        "type": "sword",
        "description": "Iberian curved sword with exceptional cutting power",
        "attack_bonus": 4,
        "armor_penetration": 1,
        "required_unit_types": ["infantry"],
        "historical_note": "Could reportedly cut through helmets",
    },

    # Spears
    "dory": {
        "name": "Dory",
        "type": "spear",
        "description": "Long Greek spear used in phalanx formation",
        "attack_bonus": 1,
        "defense_bonus": 3,
        "formation_bonus": 2,
        "required_unit_types": ["spearman"],
        "historical_note": "Primary weapon of hoplite phalanx",
    },
    "sarissa": {
        "name": "Sarissa",
        "type": "spear",
        "description": "Macedonian pike, up to 6 meters long",
        "attack_bonus": 2,
        "defense_bonus": 4,
        "formation_bonus": 3,
        "range_bonus": 1,
        "required_unit_types": ["spearman"],
        "historical_note": "Revolutionary weapon of Alexander's phalanx",
    },
    "pilum": {
        "name": "Pilum",
        "type": "javelin",
        "description": "Roman throwing spear that bends on impact",
        "attack_bonus": 3,
        "range_bonus": 1,
        "armor_penetration": 2,
        "required_unit_types": ["infantry"],
        "historical_note": "Designed to pierce shields and bend",
    },

    # Bows
    "composite_bow": {
        "name": "Composite Bow",
        "type": "bow",
        "description": "Persian composite bow made from horn, wood, and sinew",
        "attack_bonus": 3,
        "range_bonus": 1,
        "accuracy_bonus": 1,
        "required_unit_types": ["archer"],
        "historical_note": "Superior power and range to simple bows",
    },
    "cretan_bow": {
        "name": "Cretan Bow",
        "type": "bow",
        "description": "Precision bow used by renowned Cretan archers",
        "attack_bonus": 2,
        "accuracy_bonus": 2,
        "critical_chance": 5,
        "required_unit_types": ["archer"],
        "historical_note": "Cretans were legendary archers",
    },

    # Other Weapons
    "sling": {
        "name": "Sling",
        "type": "ranged",
        "description": "Simple but deadly ranged weapon",
        "attack_bonus": 1,
        "range_bonus": 1,
        "ammunition_efficient": True,
        "required_unit_types": ["archer"],
        "historical_note": "Balearic slingers were highly valued",
    },
}

# Armor Definitions
ARMOR_TEMPLATES = {
    # Heavy Armor
    "lorica_segmentata": {
        "name": "Lorica Segmentata",
        "type": "heavy_armor",
        "description": "Segmented plate armor of the Roman legions",
        "defense_bonus": 4,
        "armor_bonus": 3,
        "movement_penalty": 1,
        "morale_bonus": 5,
        "required_unit_types": ["infantry"],
        "historical_note": "Iconic armor of Roman legionaries",
    },
    "bronze_cuirass": {
        "name": "Bronze Cuirass",
        "type": "heavy_armor",
        "description": "Molded bronze breastplate",
        "defense_bonus": 3,
        "armor_bonus": 2,
        "morale_bonus": 3,
        "required_unit_types": ["infantry", "spearman", "cavalry"],
        "historical_note": "Expensive armor for elite warriors",
    },
    "linothorax": {
        "name": "Linothorax",
        "type": "medium_armor",
        "description": "Layered linen armor, surprisingly effective",
        "defense_bonus": 2,
        "armor_bonus": 1,
        "movement_penalty": 0,
        "morale_bonus": 2,
        "required_unit_types": ["infantry", "spearman"],
        "historical_note": "Worn by Alexander the Great",
    },

    # Shields
    "aspis": {
        "name": "Aspis",
        "type": "shield",
        "description": "Large round shield of Greek hoplites",
        "defense_bonus": 5,
        "armor_bonus": 2,
        "formation_bonus": 3,
        "required_unit_types": ["spearman", "infantry"],
        "historical_note": "Core of the hoplite's defensive power",
    },
    "scutum": {
        "name": "Scutum",
        "type": "shield",
        "description": "Rectangular curved shield of Roman legions",
        "defense_bonus": 4,
        "armor_bonus": 2,
        "formation_bonus": 2,
        "morale_bonus": 3,
        "required_unit_types": ["infantry"],
        "historical_note": "Allowed Roman testudo formation",
    },
    "pelta": {
        "name": "Pelta",
        "type": "shield",
        "description": "Crescent-shaped light shield",
        "defense_bonus": 2,
        "armor_bonus": 1,
        "movement_penalty": 0,
        "required_unit_types": ["infantry", "archer"],
        "historical_note": "Used by peltast skirmishers",
    },

    # Helmets
    "corinthian_helmet": {
        "name": "Corinthian Helmet",
        "type": "helmet",
        "description": "Full-face bronze helmet",
        "defense_bonus": 2,
        "armor_bonus": 2,
        "morale_bonus": 3,
        "vision_penalty": 1,
        "required_unit_types": ["spearman", "infantry"],
        "historical_note": "Iconic Greek helmet design",
    },
    "galea": {
        "name": "Galea",
        "type": "helmet",
        "description": "Roman legionary helmet with neck guard",
        "defense_bonus": 2,
        "armor_bonus": 1,
        "morale_bonus": 2,
        "required_unit_types": ["infantry", "cavalry"],
        "historical_note": "Practical Roman helmet design",
    },
    "phrygian_helmet": {
        "name": "Phrygian Helmet",
        "type": "helmet",
        "description": "Forward-curving helmet",
        "defense_bonus": 1,
        "armor_bonus": 1,
        "morale_bonus": 2,
        "required_unit_types": ["infantry", "cavalry"],
        "historical_note": "Popular in eastern Mediterranean",
    },
}

# Special Equipment / Artifacts
ARTIFACT_TEMPLATES = {
    # Legendary Weapons
    "sword_of_leonidas": {
        "name": "Sword of Leonidas",
        "type": "artifact_weapon",
        "description": "Legendary blade of the Spartan king",
        "attack_bonus": 8,
        "morale_bonus": 15,
        "leadership_bonus": 3,
        "special_effect": "inspire_nearby_units",
        "required_unit_types": ["infantry", "spearman"],
        "min_rarity": "legendary",
    },
    "spear_of_achilles": {
        "name": "Spear of Achilles",
        "type": "artifact_weapon",
        "description": "The great Pelian spear",
        "attack_bonus": 10,
        "armor_penetration": 5,
        "critical_chance": 15,
        "required_unit_types": ["spearman", "infantry"],
        "min_rarity": "legendary",
    },
    "bow_of_odysseus": {
        "name": "Bow of Odysseus",
        "type": "artifact_weapon",
        "description": "Only the cunning can string this bow",
        "attack_bonus": 7,
        "range_bonus": 2,
        "accuracy_bonus": 5,
        "special_effect": "never_miss",
        "required_unit_types": ["archer"],
        "min_rarity": "legendary",
    },

    # Blessed Items
    "aegis_of_athena": {
        "name": "Aegis of Athena",
        "type": "artifact_armor",
        "description": "Shield bearing the head of Medusa",
        "defense_bonus": 10,
        "armor_bonus": 5,
        "morale_bonus": 20,
        "special_effect": "fear_aura",
        "required_unit_types": ["spearman", "infantry"],
        "min_rarity": "legendary",
    },
    "helm_of_hades": {
        "name": "Helm of Hades",
        "type": "artifact_armor",
        "description": "The helm of invisibility",
        "defense_bonus": 5,
        "armor_bonus": 3,
        "special_effect": "stealth",
        "required_unit_types": ["infantry", "cavalry"],
        "min_rarity": "legendary",
    },

    # Magic Items (rare finds)
    "oracle_pendant": {
        "name": "Oracle's Pendant",
        "type": "artifact_trinket",
        "description": "Grants prophetic visions",
        "accuracy_bonus": 3,
        "critical_chance": 10,
        "special_effect": "foresight",
        "min_rarity": "epic",
    },
    "laurel_wreath": {
        "name": "Golden Laurel Wreath",
        "type": "artifact_trinket",
        "description": "Symbol of victory and honor",
        "morale_bonus": 10,
        "leadership_bonus": 2,
        "experience_bonus": 1.2,
        "min_rarity": "rare",
    },
    "blessed_standard": {
        "name": "Blessed Legion Standard",
        "type": "artifact_banner",
        "description": "Consecrated battle standard",
        "morale_bonus": 15,
        "leadership_bonus": 3,
        "special_effect": "rally",
        "required_unit_types": ["infantry"],
        "min_rarity": "epic",
    },
    "wine_of_dionysus": {
        "name": "Wine of Dionysus",
        "type": "artifact_consumable",
        "description": "Divine wine that inspires berserker rage",
        "attack_bonus": 10,
        "morale_bonus": 20,
        "defense_penalty": 5,
        "special_effect": "berserk",
        "single_use": True,
        "min_rarity": "rare",
    },
}


def get_all_items_by_type(item_type: str) -> Dict[str, dict]:
    """
    Get all items of a specific type.

    Args:
        item_type: "weapon", "armor", or "artifact"

    Returns:
        Dictionary of item templates
    """
    if item_type == "weapon":
        return WEAPON_TEMPLATES
    elif item_type == "armor":
        return ARMOR_TEMPLATES
    elif item_type == "artifact":
        return ARTIFACT_TEMPLATES
    else:
        return {}


def get_item_template(item_id: str) -> dict:
    """
    Get item template by ID.

    Args:
        item_id: Item identifier

    Returns:
        Item template dictionary
    """
    all_items = {**WEAPON_TEMPLATES, **ARMOR_TEMPLATES, **ARTIFACT_TEMPLATES}
    return all_items.get(item_id, {})


def get_items_for_unit_type(unit_type: str) -> List[str]:
    """
    Get compatible items for a unit type.

    Args:
        unit_type: Unit type (infantry, cavalry, archer, etc.)

    Returns:
        List of compatible item IDs
    """
    compatible_items = []
    all_items = {**WEAPON_TEMPLATES, **ARMOR_TEMPLATES, **ARTIFACT_TEMPLATES}

    for item_id, item_data in all_items.items():
        required_types = item_data.get("required_unit_types", [])
        if not required_types or unit_type in required_types:
            compatible_items.append(item_id)

    return compatible_items
