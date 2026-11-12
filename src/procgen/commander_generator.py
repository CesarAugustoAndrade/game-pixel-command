"""
Procedural enemy commander generation.
Creates commanders with randomized stats and abilities.
"""

import random
from typing import Dict, List, Optional
from src.data.commander_data import get_commanders_by_faction, get_commander_data


class CommanderGenerator:
    """Generates enemy commanders for battles."""

    # Commander name components for procedural generation
    GREEK_NAMES = [
        "Theron", "Philippos", "Demetrios", "Nikandros", "Aristides",
        "Kleitos", "Perikles", "Xenophon", "Lysander", "Brasidas"
    ]

    ROMAN_NAMES = [
        "Marcus", "Gaius", "Lucius", "Titus", "Quintus",
        "Publius", "Decimus", "Gnaeus", "Sextus", "Aulus"
    ]

    PERSIAN_NAMES = [
        "Artaxerxes", "Darius", "Xerxes", "Cyrus", "Tigranes",
        "Mithridates", "Pharnabazus", "Tissaphernes", "Megabyzus", "Orontes"
    ]

    CARTHAGINIAN_NAMES = [
        "Hanno", "Hamilcar", "Hasdrubal", "Mago", "Gisco",
        "Adherbal", "Bomilcar", "Himilco", "Maharbal", "Hannibal"
    ]

    TITLES = [
        "General", "Commander", "Strategos", "Legate", "Satrap",
        "Captain", "Tribune", "Polemarch", "Hipparch", "Navarch"
    ]

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize commander generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.random = random.Random(seed)

    def generate_commander(
        self,
        faction: str,
        difficulty: int = 1,
        is_elite: bool = False,
        is_boss: bool = False,
        use_historical: bool = False,
    ) -> Dict:
        """
        Generate a commander for an enemy army.

        Args:
            faction: Faction name
            difficulty: Commander power level (1-10)
            is_elite: Generate elite commander
            is_boss: Generate boss-level commander
            use_historical: Use historical commanders if True

        Returns:
            Commander data dictionary
        """
        # Use historical commander if requested and available
        if use_historical or is_boss:
            historical_commanders = get_commanders_by_faction(faction)
            if historical_commanders:
                # Pick a random historical commander
                commander_id = self.random.choice(historical_commanders)
                commander = get_commander_data(commander_id).copy()
                commander["id"] = commander_id
                commander["is_historical"] = True
                return commander

        # Generate procedural commander
        name = self._generate_name(faction)
        title = self._generate_title(faction, is_elite, is_boss)

        # Base stats scaled by difficulty
        stats = self._generate_stats(difficulty, is_elite, is_boss)

        # Generate bonuses
        bonuses = self._generate_bonuses(difficulty, faction, is_elite, is_boss)

        # Generate abilities
        abilities = self._generate_abilities(difficulty, faction, is_elite, is_boss)

        commander = {
            "id": f"generated_{faction}_{self.random.randint(1000, 9999)}",
            "name": name,
            "title": title,
            "faction": faction,
            "description": f"A {title.lower()} of {faction.capitalize()}",
            "is_historical": False,
            "stats": stats,
            "bonuses": bonuses,
            "abilities": abilities,
            "traits": self._generate_traits(difficulty),
            "color": self._get_faction_color(faction),
        }

        return commander

    def _generate_name(self, faction: str) -> str:
        """Generate a commander name based on faction."""
        name_pools = {
            "greece": self.GREEK_NAMES,
            "rome": self.ROMAN_NAMES,
            "persia": self.PERSIAN_NAMES,
            "carthage": self.CARTHAGINIAN_NAMES,
        }

        names = name_pools.get(faction, self.GREEK_NAMES)
        return self.random.choice(names)

    def _generate_title(self, faction: str, is_elite: bool, is_boss: bool) -> str:
        """Generate appropriate title."""
        if is_boss:
            return "Supreme Commander" if self.random.random() < 0.5 else "War Master"
        elif is_elite:
            return "Elite " + self.random.choice(self.TITLES)
        else:
            return self.random.choice(self.TITLES)

    def _generate_stats(
        self, difficulty: int, is_elite: bool, is_boss: bool
    ) -> Dict[str, int]:
        """Generate commander stats."""
        base_stat = 30 + (difficulty * 5)

        if is_boss:
            base_stat += 20
        elif is_elite:
            base_stat += 10

        # Add variance
        stats = {}
        for stat_name in ["leadership", "tactics", "cavalry_command", "infantry_command", "siege", "bravery"]:
            variance = self.random.randint(-10, 15)
            stat_value = min(100, max(20, base_stat + variance))
            stats[stat_name] = stat_value

        return stats

    def _generate_bonuses(
        self, difficulty: int, faction: str, is_elite: bool, is_boss: bool
    ) -> Dict:
        """Generate commander bonuses."""
        bonuses = {}

        # Morale bonus (all commanders provide some morale)
        morale_bonus = 5 + (difficulty * 2)
        if is_boss:
            morale_bonus += 15
        elif is_elite:
            morale_bonus += 10
        bonuses["morale"] = morale_bonus

        # Number of additional bonuses based on difficulty
        num_bonuses = 1 + (difficulty // 3)
        if is_elite:
            num_bonuses += 1
        if is_boss:
            num_bonuses += 2

        # Available bonus types
        bonus_pool = [
            ("movement", 1),
            ("cavalry_flanking", 0.10),
            ("formation_bonus", 0.10),
            ("experience_gain", 0.25),
            ("archer_damage", 0.10),
            ("infantry_defense", 0.10),
            ("spearman_defense", 0.10),
            ("first_turn_movement", 1),
        ]

        # Select random bonuses
        selected_bonuses = self.random.sample(
            bonus_pool, min(num_bonuses, len(bonus_pool))
        )

        for bonus_name, base_value in selected_bonuses:
            # Scale by difficulty
            if isinstance(base_value, float):
                bonuses[bonus_name] = round(
                    base_value * (1 + difficulty * 0.1), 2
                )
            else:
                bonuses[bonus_name] = base_value + (difficulty // 4)

        return bonuses

    def _generate_abilities(
        self, difficulty: int, faction: str, is_elite: bool, is_boss: bool
    ) -> List[Dict]:
        """Generate commander abilities."""
        abilities = []

        # Number of abilities
        num_abilities = 1
        if is_elite:
            num_abilities = 2
        if is_boss:
            num_abilities = 3 + self.random.randint(0, 1)

        # Always include a passive aura
        abilities.append(self._generate_passive_aura(difficulty))

        # Add active abilities
        for _ in range(num_abilities - 1):
            ability = self._generate_active_ability(difficulty, faction)
            abilities.append(ability)

        return abilities

    def _generate_passive_aura(self, difficulty: int) -> Dict:
        """Generate a passive aura ability."""
        aura_range = 3 + (difficulty // 2)
        morale_bonus = 5 + (difficulty * 1)
        attack_bonus = round(0.05 + (difficulty * 0.01), 2)

        return {
            "id": "commander_aura",
            "name": "Commander's Presence",
            "type": "passive",
            "description": f"Inspires nearby troops within {aura_range} hexes.",
            "effects": {
                "aura_range": aura_range,
                "morale_bonus": morale_bonus,
                "attack_bonus": attack_bonus,
            },
        }

    def _generate_active_ability(self, difficulty: int, faction: str) -> Dict:
        """Generate an active ability."""
        ability_types = [
            {
                "id": "rally_troops",
                "name": "Rally the Troops",
                "uses_per_battle": 2,
                "cooldown": 3,
                "description": "Restore morale to nearby units.",
                "effects": {
                    "morale_restore": 20 + (difficulty * 2),
                    "range": 5,
                    "duration": 2,
                },
            },
            {
                "id": "tactical_insight",
                "name": "Tactical Insight",
                "uses_per_battle": 1,
                "cooldown": 5,
                "description": "Grant attack and defense bonuses to all units.",
                "effects": {
                    "attack_bonus": 0.15 + (difficulty * 0.02),
                    "defense_bonus": 0.15 + (difficulty * 0.02),
                    "duration": 3,
                },
            },
            {
                "id": "forced_march",
                "name": "Forced March",
                "uses_per_battle": 2,
                "cooldown": 4,
                "description": "Increase movement speed temporarily.",
                "effects": {
                    "movement_bonus": 2 + (difficulty // 3),
                    "range": 0,  # All units
                    "duration": 2,
                },
            },
            {
                "id": "desperate_assault",
                "name": "Desperate Assault",
                "uses_per_battle": 1,
                "cooldown": 6,
                "description": "Sacrifice defense for massive attack boost.",
                "effects": {
                    "attack_bonus": 0.30 + (difficulty * 0.05),
                    "defense_penalty": -0.20,
                    "morale_bonus": 15,
                    "duration": 2,
                },
            },
            {
                "id": "defensive_stance",
                "name": "Defensive Stance",
                "uses_per_battle": 2,
                "cooldown": 4,
                "description": "Significantly boost defense at cost of mobility.",
                "effects": {
                    "defense_bonus": 0.40 + (difficulty * 0.05),
                    "movement_penalty": -2,
                    "duration": 3,
                },
            },
        ]

        ability = self.random.choice(ability_types).copy()
        ability["type"] = "active"

        return ability

    def _generate_traits(self, difficulty: int) -> Dict[str, List[str]]:
        """Generate personality traits."""
        positive_traits = [
            "disciplined", "strategic", "brave", "charismatic", "experienced"
        ]
        negative_traits = [
            "reckless", "cautious", "arrogant", "inexperienced", "brutal"
        ]

        num_traits = 2 + (difficulty // 4)

        return {
            "positive": self.random.sample(positive_traits, min(num_traits, 3)),
            "negative": self.random.sample(negative_traits, min(2, len(negative_traits))),
        }

    def _get_faction_color(self, faction: str) -> List[int]:
        """Get color for faction."""
        colors = {
            "rome": [200, 50, 50],
            "greece": [50, 100, 200],
            "persia": [150, 100, 200],
            "carthage": [100, 200, 100],
        }
        return colors.get(faction, [150, 150, 150])


# Convenience function
def generate_enemy_commander(
    faction: str,
    difficulty: int = 1,
    is_elite: bool = False,
    is_boss: bool = False,
    seed: Optional[int] = None,
) -> Dict:
    """
    Generate an enemy commander.

    Args:
        faction: Faction name
        difficulty: Commander power level
        is_elite: Elite commander flag
        is_boss: Boss commander flag
        seed: Random seed

    Returns:
        Commander data dictionary
    """
    generator = CommanderGenerator(seed)
    return generator.generate_commander(faction, difficulty, is_elite, is_boss)
