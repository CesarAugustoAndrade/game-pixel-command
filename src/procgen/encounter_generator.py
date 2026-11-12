"""
Enemy encounter generation.
"""

import random
from typing import List, Dict, Any, Optional
from src.procgen.commander_generator import CommanderGenerator


class EncounterGenerator:
    """
    Generates enemy encounters based on difficulty and faction.
    """

    def __init__(self, seed: int = None):
        """
        Initialize encounter generator.

        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        self.commander_generator = CommanderGenerator(seed)

    def generate_encounter(
        self, difficulty: int, faction: str = None, player_strength: int = 100,
        include_commander: bool = False
    ) -> Dict[str, Any]:
        """
        Generate an enemy encounter.

        Args:
            difficulty: Difficulty level (1-10)
            faction: Enemy faction (None for random)
            player_strength: Player's total troop count for balancing
            include_commander: Whether to include a commander

        Returns:
            Dictionary with 'units' and optionally 'commander'
        """
        if faction is None:
            faction = random.choice(["rome", "greece", "persia", "carthage"])

        # Calculate target enemy strength based on difficulty
        strength_multiplier = 0.5 + (difficulty * 0.15)
        target_strength = int(player_strength * strength_multiplier)

        # Ensure minimum target strength
        target_strength = max(target_strength, 100)  # At least 100 troops

        # Generate units
        units = []
        current_strength = 0

        # Get faction unit pool
        unit_pool = self._get_faction_units(faction)

        while current_strength < target_strength:
            unit_type = random.choice(unit_pool)
            unit_size = random.randint(30, 100)

            units.append({
                "type": unit_type,
                "count": unit_size,
                "faction": faction,
            })

            current_strength += unit_size

        encounter = {"units": units, "faction": faction}

        # Add commander if requested
        if include_commander:
            commander = self.commander_generator.generate_commander(
                faction=faction,
                difficulty=difficulty,
                is_elite=False,
                is_boss=False
            )
            encounter["commander"] = commander

        return encounter

    def _get_faction_units(self, faction: str) -> List[str]:
        """
        Get available unit types for a faction.

        Args:
            faction: Faction name

        Returns:
            List of unit type strings
        """
        faction_units = {
            "rome": ["infantry", "infantry", "spearman", "cavalry"],
            "greece": ["spearman", "spearman", "infantry", "archer"],
            "persia": ["archer", "archer", "cavalry", "infantry"],
            "carthage": ["cavalry", "spearman", "archer", "infantry"],
        }

        return faction_units.get(faction, ["infantry", "archer", "spearman"])

    def generate_elite_encounter(
        self, difficulty: int, faction: str = None, player_strength: int = 100
    ) -> Dict[str, Any]:
        """
        Generate an elite encounter with higher quality units and commander.

        Args:
            difficulty: Difficulty level
            faction: Enemy faction
            player_strength: Player strength for balancing

        Returns:
            Dictionary with elite units and commander
        """
        if faction is None:
            faction = random.choice(["rome", "greece", "persia", "carthage"])

        encounter = self.generate_encounter(
            difficulty + 2, faction, player_strength, include_commander=False
        )
        units = encounter["units"]

        # Upgrade units to veterans
        for unit in units:
            unit["veterancy"] = random.randint(1, 3)
            unit["equipment_quality"] = "elite"

        # Generate elite commander
        commander = self.commander_generator.generate_commander(
            faction=faction,
            difficulty=difficulty + 2,
            is_elite=True,
            is_boss=False
        )

        return {
            "units": units,
            "faction": faction,
            "commander": commander,
            "is_elite": True
        }

    def generate_boss_encounter(
        self, faction: str = None, player_strength: int = 100
    ) -> Dict[str, Any]:
        """
        Generate a boss encounter with powerful commander.

        Args:
            faction: Enemy faction
            player_strength: Player strength for balancing

        Returns:
            Dictionary with boss units and legendary commander
        """
        if faction is None:
            faction = random.choice(["rome", "greece", "persia", "carthage"])

        encounter = self.generate_encounter(
            8, faction, player_strength, include_commander=False
        )
        units = encounter["units"]

        # Upgrade units to max veterancy
        for unit in units:
            unit["veterancy"] = 3
            unit["equipment_quality"] = "legendary"

        # Generate boss commander (may use historical figures)
        commander = self.commander_generator.generate_commander(
            faction=faction,
            difficulty=10,
            is_elite=False,
            is_boss=True,
            use_historical=True  # Prefer historical commanders for bosses
        )

        return {
            "units": units,
            "faction": faction,
            "commander": commander,
            "is_boss": True
        }
