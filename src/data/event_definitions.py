"""
Event definitions for roguelite encounters.
Historical events themed for Classical Age warfare.
"""

from typing import Dict, List

# Event templates with choices and outcomes
EVENT_TEMPLATES = {
    # Shrine and Religious Events
    "shrine_of_ares": {
        "name": "Shrine of Ares",
        "description": "Your army discovers a weathered shrine to Ares, god of war. Blood-stained offerings cover the altar.",
        "category": "shrine",
        "choices": [
            {
                "id": "pray",
                "text": "Offer prayers for victory",
                "outcomes": [
                    {
                        "weight": 70,
                        "effects": [
                            {"type": "blessing", "stat": "morale", "value": 10, "duration": 3}
                        ],
                        "message": "Your soldiers feel Ares' presence. Their morale rises! (+10 morale for 3 battles)",
                    },
                    {
                        "weight": 30,
                        "effects": [],
                        "message": "The god is silent. Your prayers go unanswered.",
                    },
                ],
            },
            {
                "id": "donate",
                "text": "Make a blood sacrifice (-100 gold)",
                "cost": {"gold": 100},
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "blessing", "stat": "attack", "value": 2, "duration": 3},
                            {"type": "blessing", "stat": "morale", "value": 15, "duration": 3},
                        ],
                        "message": "Ares accepts your offering! Your warriors gain his fury! (+2 attack, +15 morale for 3 battles)",
                    }
                ],
            },
            {
                "id": "leave",
                "text": "Leave the shrine undisturbed",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "You continue on your way.",
                    }
                ],
            },
        ],
    },

    "temple_of_athena": {
        "name": "Temple of Athena",
        "description": "A beautiful temple to Athena, goddess of wisdom and strategy, stands before you.",
        "category": "shrine",
        "choices": [
            {
                "id": "pray",
                "text": "Pray for tactical wisdom",
                "outcomes": [
                    {
                        "weight": 80,
                        "effects": [
                            {"type": "blessing", "stat": "defense", "value": 2, "duration": 3}
                        ],
                        "message": "Athena grants you tactical insight. (+2 defense for 3 battles)",
                    },
                    {
                        "weight": 20,
                        "effects": [],
                        "message": "The goddess remains silent.",
                    },
                ],
            },
            {
                "id": "donate",
                "text": "Donate gold to the temple (-150 gold)",
                "cost": {"gold": 150},
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "blessing", "stat": "defense", "value": 3, "duration": 3},
                            {"type": "item_reward", "min_rarity": "rare"},
                        ],
                        "message": "The priestess blesses you and gifts you a sacred artifact!",
                    }
                ],
            },
            {
                "id": "leave",
                "text": "Continue your march",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "You depart peacefully.",
                    }
                ],
            },
        ],
    },

    # Merchant and Trade Events
    "traveling_merchant": {
        "name": "Traveling Merchant",
        "description": "A merchant's caravan crosses your path. He offers to trade weapons and supplies.",
        "category": "merchant",
        "choices": [
            {
                "id": "browse",
                "text": "Browse his wares",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [{"type": "open_shop", "shop_level": 2}],
                        "message": "The merchant opens his packs...",
                    }
                ],
            },
            {
                "id": "trade",
                "text": "Trade food for gold (Trade 50 food for 100 gold)",
                "cost": {"food": 50},
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [{"type": "reward", "gold": 100}],
                        "message": "A fair trade. The merchant is pleased.",
                    }
                ],
            },
            {
                "id": "leave",
                "text": "Decline and move on",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "The merchant waves goodbye.",
                    }
                ],
            },
        ],
    },

    "mysterious_trader": {
        "name": "Mysterious Trader",
        "description": "A hooded figure approaches your camp, offering rare and powerful items from distant lands.",
        "category": "merchant",
        "choices": [
            {
                "id": "trade",
                "text": "Trade for a mysterious artifact (-200 gold)",
                "cost": {"gold": 200},
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [{"type": "item_reward", "force_rarity": "rare"}],
                        "message": "The trader produces an exquisite item wrapped in silk...",
                    }
                ],
            },
            {
                "id": "suspicious",
                "text": "This seems suspicious... decline",
                "outcomes": [
                    {
                        "weight": 70,
                        "effects": [],
                        "message": "The figure vanishes into the shadows.",
                    },
                    {
                        "weight": 30,
                        "effects": [
                            {"type": "reward", "gold": 50},
                        ],
                        "message": "You find a small coin purse where the figure stood. Wise to be cautious!",
                    },
                ],
            },
        ],
    },

    # Combat Events
    "bandit_ambush": {
        "name": "Bandit Ambush!",
        "description": "Bandits have set up an ambush on the road ahead! They demand tribute or your lives.",
        "category": "combat",
        "choices": [
            {
                "id": "fight",
                "text": "Prepare for battle!",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "battle", "enemy_type": "bandits", "difficulty_modifier": -1}
                        ],
                        "message": "Your army charges into battle!",
                    }
                ],
            },
            {
                "id": "pay",
                "text": "Pay tribute (-100 gold)",
                "cost": {"gold": 100},
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "The bandits take your gold and let you pass.",
                    }
                ],
            },
            {
                "id": "intimidate",
                "text": "Intimidate them with your army's might",
                "skill_check": {"type": "morale", "threshold": 70},
                "outcomes": [
                    {
                        "weight": 100,
                        "success_only": True,
                        "effects": [],
                        "message": "The bandits flee at the sight of your disciplined army!",
                    },
                    {
                        "weight": 100,
                        "failure_only": True,
                        "effects": [
                            {"type": "battle", "enemy_type": "bandits", "difficulty_modifier": 0}
                        ],
                        "message": "The bandits laugh at your display. They attack!",
                    },
                ],
            },
        ],
    },

    "enemy_patrol": {
        "name": "Enemy Patrol",
        "description": "You spot an enemy patrol ahead. They haven't seen you yet.",
        "category": "combat",
        "choices": [
            {
                "id": "ambush",
                "text": "Ambush them!",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "battle", "enemy_type": "patrol", "difficulty_modifier": -2, "ambush": True}
                        ],
                        "message": "Your forces strike first!",
                    }
                ],
            },
            {
                "id": "avoid",
                "text": "Take a detour to avoid them",
                "outcomes": [
                    {
                        "weight": 80,
                        "effects": [{"type": "consume_food", "value": 10}],
                        "message": "You successfully avoid the patrol, but the detour costs extra supplies. (-10 food)",
                    },
                    {
                        "weight": 20,
                        "effects": [
                            {"type": "battle", "enemy_type": "patrol", "difficulty_modifier": 0}
                        ],
                        "message": "They spotted you! Battle is unavoidable!",
                    },
                ],
            },
            {
                "id": "parley",
                "text": "Attempt to parley",
                "outcomes": [
                    {
                        "weight": 30,
                        "effects": [{"type": "reward", "gold": 50, "experience": 25}],
                        "message": "Surprisingly, they agree to peaceful passage. You exchange information.",
                    },
                    {
                        "weight": 70,
                        "effects": [
                            {"type": "battle", "enemy_type": "patrol", "difficulty_modifier": 0}
                        ],
                        "message": "They reject your offer and attack!",
                    },
                ],
            },
        ],
    },

    # Discovery Events
    "ancient_battlefield": {
        "name": "Ancient Battlefield",
        "description": "You come upon an ancient battlefield. Rusted weapons and broken shields litter the ground.",
        "category": "discovery",
        "choices": [
            {
                "id": "search",
                "text": "Search the battlefield thoroughly",
                "outcomes": [
                    {
                        "weight": 50,
                        "effects": [
                            {"type": "reward", "gold": 75},
                            {"type": "item_reward", "min_rarity": "common"},
                        ],
                        "message": "You find some salvageable equipment and coins from fallen soldiers.",
                    },
                    {
                        "weight": 30,
                        "effects": [{"type": "item_reward", "force_rarity": "rare"}],
                        "message": "You discover a well-preserved officer's weapon!",
                    },
                    {
                        "weight": 20,
                        "effects": [],
                        "message": "Nothing of value remains. Time has claimed it all.",
                    },
                ],
            },
            {
                "id": "honor",
                "text": "Hold a ceremony honoring the fallen",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "blessing", "stat": "morale", "value": 15, "duration": 2}
                        ],
                        "message": "Your soldiers are inspired by respect for fallen warriors. (+15 morale for 2 battles)",
                    }
                ],
            },
            {
                "id": "leave",
                "text": "This place feels cursed. Leave quickly.",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "You depart without disturbing the dead.",
                    }
                ],
            },
        ],
    },

    "treasure_map": {
        "name": "Treasure Map",
        "description": "A dying scout hands you a map marked with an X. 'Great treasure,' he gasps, 'but... beware...'",
        "category": "discovery",
        "choices": [
            {
                "id": "follow",
                "text": "Follow the map",
                "outcomes": [
                    {
                        "weight": 60,
                        "effects": [
                            {"type": "treasure", "level": 3, "hidden": True}
                        ],
                        "message": "The map leads you to a hidden cache! Treasure!",
                    },
                    {
                        "weight": 30,
                        "effects": [
                            {"type": "battle", "enemy_type": "treasure_guards", "difficulty_modifier": 1},
                            {"type": "treasure_after_battle", "level": 3, "hidden": True},
                        ],
                        "message": "The treasure is guarded! Defeat them to claim your prize!",
                    },
                    {
                        "weight": 10,
                        "effects": [{"type": "lose_health", "value": 10}],
                        "message": "It was a trap! Your forces trigger a pitfall. (-10 troops lost)",
                    },
                ],
            },
            {
                "id": "ignore",
                "text": "The dying man's warning gives you pause. Ignore the map.",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "Sometimes caution is the better part of valor.",
                    }
                ],
            },
        ],
    },

    # Social Events
    "deserters": {
        "name": "Deserters from Enemy Army",
        "description": "A group of enemy soldiers approaches with white flags. They wish to defect to your side.",
        "category": "social",
        "choices": [
            {
                "id": "accept",
                "text": "Welcome them into your ranks",
                "cost": {"food": 30},
                "outcomes": [
                    {
                        "weight": 70,
                        "effects": [
                            {"type": "recruit_units", "count": "1-2", "random": True}
                        ],
                        "message": "The deserters join your army! (-30 food for supplies)",
                    },
                    {
                        "weight": 30,
                        "effects": [
                            {"type": "lose_health", "value": 5},
                            {"type": "debuff", "stat": "morale", "value": -10, "duration": 1},
                        ],
                        "message": "They were spies! They attacked from within before fleeing! (-5 casualties, -10 morale)",
                    },
                ],
            },
            {
                "id": "refuse",
                "text": "Refuse them. They cannot be trusted.",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "The deserters leave disappointed.",
                    }
                ],
            },
            {
                "id": "interrogate",
                "text": "Interrogate them for information first",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "reward", "experience": 50},
                            {"type": "reveal_map", "radius": 2},
                        ],
                        "message": "They reveal valuable intelligence about enemy positions! (+50 XP)",
                    }
                ],
            },
        ],
    },

    "village_feast": {
        "name": "Village Feast",
        "description": "A grateful village invites your army to a feast after you saved them from bandits.",
        "category": "social",
        "choices": [
            {
                "id": "accept",
                "text": "Accept the invitation",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "reward", "food": 50},
                            {"type": "blessing", "stat": "morale", "value": 20, "duration": 2},
                            {"type": "heal", "percent": 10},
                        ],
                        "message": "Your soldiers feast and rest! (+50 food, +20 morale for 2 battles, heal 10%)",
                    }
                ],
            },
            {
                "id": "decline",
                "text": "Decline politely, you must move on",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [{"type": "reward", "gold": 75}],
                        "message": "The villagers give you gold for provisions instead. (+75 gold)",
                    }
                ],
            },
        ],
    },

    # Miscellaneous Events
    "oracle_vision": {
        "name": "Oracle's Vision",
        "description": "An oracle offers to read your fortune for a price.",
        "category": "mystical",
        "choices": [
            {
                "id": "pay",
                "text": "Pay for the vision (-50 gold)",
                "cost": {"gold": 50},
                "outcomes": [
                    {
                        "weight": 40,
                        "effects": [
                            {"type": "reveal_map", "radius": 3},
                            {"type": "item_reward", "artifact": "oracle_pendant"},
                        ],
                        "message": "The oracle reveals hidden paths and gifts you a blessed pendant!",
                    },
                    {
                        "weight": 40,
                        "effects": [
                            {"type": "blessing", "stat": "critical_chance", "value": 5, "duration": 3}
                        ],
                        "message": "The vision sharpens your instincts. (+5% critical chance for 3 battles)",
                    },
                    {
                        "weight": 20,
                        "effects": [],
                        "message": "The oracle speaks in riddles you cannot understand.",
                    },
                ],
            },
            {
                "id": "refuse",
                "text": "Refuse the offer",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [],
                        "message": "The oracle vanishes in a cloud of incense.",
                    }
                ],
            },
        ],
    },

    "army_rivalry": {
        "name": "Internal Rivalry",
        "description": "Two of your officers are feuding, threatening unit cohesion.",
        "category": "challenge",
        "choices": [
            {
                "id": "mediate",
                "text": "Mediate the dispute",
                "skill_check": {"type": "leadership", "threshold": 5},
                "outcomes": [
                    {
                        "weight": 100,
                        "success_only": True,
                        "effects": [
                            {"type": "blessing", "stat": "morale", "value": 10, "duration": 2}
                        ],
                        "message": "Your wisdom resolves the conflict. Unit cohesion is restored! (+10 morale)",
                    },
                    {
                        "weight": 100,
                        "failure_only": True,
                        "effects": [
                            {"type": "debuff", "stat": "morale", "value": -15, "duration": 2}
                        ],
                        "message": "Your attempt fails. The feud intensifies! (-15 morale for 2 battles)",
                    },
                ],
            },
            {
                "id": "duel",
                "text": "Let them settle it with a duel",
                "outcomes": [
                    {
                        "weight": 60,
                        "effects": [
                            {"type": "lose_health", "value": 5}
                        ],
                        "message": "The duel is bloody but honor is satisfied. (-5 casualties)",
                    },
                    {
                        "weight": 40,
                        "effects": [
                            {"type": "blessing", "stat": "morale", "value": 15, "duration": 2}
                        ],
                        "message": "A clean duel restores honor and boosts morale! (+15 morale)",
                    },
                ],
            },
            {
                "id": "punish",
                "text": "Punish both officers for insubordination",
                "outcomes": [
                    {
                        "weight": 100,
                        "effects": [
                            {"type": "debuff", "stat": "morale", "value": -10, "duration": 1},
                            {"type": "blessing", "stat": "discipline", "value": 5, "duration": 3},
                        ],
                        "message": "Harsh but effective. The army respects your authority. (-10 morale this battle, +5 discipline)",
                    }
                ],
            },
        ],
    },
}


def get_event_by_id(event_id: str) -> Dict:
    """Get event template by ID."""
    return EVENT_TEMPLATES.get(event_id, {})


def get_events_by_category(category: str) -> List[str]:
    """
    Get all event IDs of a specific category.

    Categories: shrine, merchant, combat, discovery, social, mystical, challenge
    """
    return [
        event_id
        for event_id, event_data in EVENT_TEMPLATES.items()
        if event_data.get("category") == category
    ]


def get_all_event_ids() -> List[str]:
    """Get all event IDs."""
    return list(EVENT_TEMPLATES.keys())
