"""
Commander definitions with stats, bonuses, and special abilities.
Based on historical military leaders from the classical era.
"""

COMMANDER_DATA = {
    "alexander": {
        "name": "Alexander the Great",
        "title": "King of Macedon",
        "faction": "greece",
        "description": "The most successful military commander in ancient history. Never lost a battle.",
        "era": "334-323 BCE",

        # Core Stats (0-100 scale)
        "stats": {
            "leadership": 98,
            "tactics": 95,
            "cavalry_command": 100,
            "infantry_command": 85,
            "siege": 90,
            "bravery": 100,
        },

        # Morale Warfare Stats (for morale-driven battles)
        "morale_warfare_stats": {
            "leadership": 98,      # Reduces morale loss by up to 25% (at 100)
            "tactics": 95,         # Increases flank damage by up to 50% (at 100)
            "martial_prowess": 90, # Personal combat damage bonus up to 100% (at 100)
            "presence": 92,        # Buffs nearby units by up to 20% (at 100)
        },

        # Army-wide bonuses
        "bonuses": {
            "morale": 25,                    # +25 morale to all units
            "movement": 2,                   # +2 hexes movement
            "cavalry_flanking": 0.20,        # +20% damage when cavalry flanks
            "formation_bonus": 0.15,         # +15% when units in formation
            "experience_gain": 0.50,         # +50% XP gain
            "first_turn_movement": 2,        # +2 extra movement first turn
        },

        # Special Abilities
        "abilities": [
            {
                "id": "companion_charge",
                "name": "Companion Charge",
                "type": "active",
                "uses_per_battle": 1,
                "cooldown": 0,
                "range": 8,
                "description": "Alexander personally leads cavalry in devastating charge. 200% damage, breakthrough on kill.",
                "effects": {
                    "damage_multiplier": 2.0,
                    "morale_shock": True,
                    "breakthrough": True,
                    "aoe_morale_buff": 10,  # +10 morale to allies for 3 turns
                }
            },
            {
                "id": "hammer_and_anvil",
                "name": "Hammer and Anvil",
                "type": "active",
                "uses_per_battle": 3,
                "cooldown": 4,
                "range": 0,  # Global
                "description": "Coordinate phalanx (anvil) and cavalry (hammer) for devastating combo.",
                "effects": {
                    "infantry_locks_enemy": True,
                    "cavalry_flank_bonus": 0.30,
                    "target_defense_reduction": 0.40,
                    "duration": 2,
                }
            },
            {
                "id": "oblique_assault",
                "name": "Oblique Assault",
                "type": "active",
                "uses_per_battle": 2,
                "cooldown": 5,
                "range": 0,  # Global
                "description": "Concentrate forces on one flank while refusing the other.",
                "effects": {
                    "strong_flank_attack": 0.20,
                    "strong_flank_movement": 1,
                    "weak_flank_defense": 0.15,
                    "duration": 3,
                }
            },
            {
                "id": "macedonian_legacy",
                "name": "Macedonian Legacy",
                "type": "passive",
                "description": "Personal leadership inspires nearby troops.",
                "effects": {
                    "aura_range": 6,
                    "morale_bonus_6hex": 15,
                    "attack_bonus_3hex": 0.10,
                    "enemy_intimidation": -5,
                }
            },
            {
                "id": "forced_march",
                "name": "Forced March",
                "type": "passive",
                "description": "Army moves at incredible speed.",
                "effects": {
                    "campaign_movement": 0.30,
                    "battle_movement": 1,
                    "cavalry_extra_movement": 1,
                }
            },
            {
                "id": "student_of_aristotle",
                "name": "Student of Aristotle",
                "type": "passive",
                "description": "Learns faster and masters terrain.",
                "effects": {
                    "xp_gain": 0.50,
                    "terrain_vision": True,
                    "no_terrain_penalty": True,
                }
            }
        ],

        # Personality traits (for events/narrative)
        "traits": {
            "positive": ["strategic_genius", "bold", "inspirational", "educated", "restless"],
            "negative": ["reckless", "impulsive", "ambitious", "theatrical"]
        },

        # Starting units for campaign
        "starting_units": [
            {"unit": "companion_cavalry", "count": 2},
            {"unit": "greek_hoplite", "count": 4},
            {"unit": "peltast", "count": 2},
            {"unit": "thessalian_cavalry", "count": 2},
            {"unit": "cretan_archer", "count": 1},
        ],

        # Visual/flavor
        "quote": "There is nothing impossible to him who will try.",
        "color": [255, 215, 0],  # Gold
        "icon": "alexander_portrait",  # Asset path (to be created)

        # Unlock conditions
        "unlock": {
            "type": "default",  # Available by default for Greece
            "requirement": None
        }
    },

    # Placeholder for future commanders
    "leonidas": {
        "name": "Leonidas I",
        "title": "King of Sparta",
        "faction": "greece",
        "description": "The legendary Spartan king who held Thermopylae against impossible odds.",
        "era": "480 BCE",

        "stats": {
            "leadership": 95,
            "tactics": 80,
            "cavalry_command": 40,
            "infantry_command": 100,
            "siege": 50,
            "bravery": 100,
        },

        # Morale Warfare Stats (for morale-driven battles)
        "morale_warfare_stats": {
            "leadership": 95,      # Unyielding leadership
            "tactics": 80,         # Defensive tactics specialist
            "martial_prowess": 100, # Legendary warrior prowess
            "presence": 90,        # Inspiring presence (Spartan aura)
        },

        "bonuses": {
            "morale": 30,
            "spearman_defense": 0.30,
            "last_stand_bonus": 0.50,  # +50% when outnumbered
            "spartan_units_cost": -0.20,
        },

        "abilities": [
            {
                "id": "thermopylae_stand",
                "name": "Thermopylae Stand",
                "type": "active",
                "uses_per_battle": 1,
                "description": "Hold a chokepoint with unbreakable defense. Cannot retreat but immune to morale loss.",
                "effects": {
                    "defense_multiplier": 2.0,
                    "immune_to_morale_loss": True,
                    "cannot_retreat": True,
                    "duration": 5,
                }
            }
        ],

        "starting_units": [
            {"unit": "spartan_champion", "count": 3},
            {"unit": "greek_hoplite", "count": 4},
            {"unit": "peltast", "count": 1},
        ],

        "quote": "Come back with your shield, or on it.",
        "color": [139, 0, 0],  # Dark red
        "icon": "leonidas_portrait",

        "unlock": {
            "type": "achievement",
            "requirement": "Hold position against 3:1 odds for 10 turns"
        }
    }
}


def get_commander_data(commander_id: str) -> dict:
    """
    Get commander data by ID.

    Args:
        commander_id: Commander ID (e.g., 'alexander')

    Returns:
        Commander data dict or empty dict if not found
    """
    return COMMANDER_DATA.get(commander_id, {})


def get_commanders_by_faction(faction: str) -> list:
    """
    Get all commanders available to a faction.

    Args:
        faction: Faction name

    Returns:
        List of commander IDs
    """
    commanders = []
    for cmd_id, cmd_data in COMMANDER_DATA.items():
        if cmd_data.get("faction") == faction:
            commanders.append(cmd_id)
    return commanders


def get_all_commanders() -> dict:
    """
    Get all commander data.

    Returns:
        Dictionary of all commanders
    """
    return COMMANDER_DATA


def get_morale_warfare_stats(commander_id: str) -> dict:
    """
    Get morale warfare stats for a commander.

    Args:
        commander_id: Commander ID

    Returns:
        Dict with leadership, tactics, martial_prowess, presence (0-100 scale)
    """
    commander = get_commander_data(commander_id)

    # Return morale warfare stats if available
    if "morale_warfare_stats" in commander:
        return commander["morale_warfare_stats"]

    # Fall back to regular stats if morale warfare stats not defined
    stats = commander.get("stats", {})
    return {
        "leadership": stats.get("leadership", 50),
        "tactics": stats.get("tactics", 50),
        "martial_prowess": stats.get("bravery", 50),  # Use bravery as fallback
        "presence": stats.get("leadership", 50) // 2 + 25,  # Derive from leadership
    }


def apply_commander_bonuses(army, commander_id: str):
    """
    Apply commander bonuses to an army.

    Args:
        army: Army object
        commander_id: Commander ID
    """
    commander = get_commander_data(commander_id)
    if not commander:
        return

    # Store commander data on army
    army.commander_id = commander_id
    army.commander_name = commander["name"]
    army.commander_bonuses = commander.get("bonuses", {})
    army.commander_abilities = commander.get("abilities", [])
    army.commander_stats = commander.get("stats", {})
