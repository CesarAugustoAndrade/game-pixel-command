"""
Procedural item generation system.
Generates items with randomized stats based on rarity and templates.
"""

import random
from typing import Dict, Optional, List
from src.data.item_definitions import (
    ITEM_RARITIES,
    WEAPON_TEMPLATES,
    ARMOR_TEMPLATES,
    ARTIFACT_TEMPLATES,
    get_item_template,
    get_items_for_unit_type,
)


class ItemGenerator:
    """Generates procedurally created items with varying stats."""

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize item generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.random = random.Random(seed)

    def generate_random_item(
        self,
        difficulty: int = 1,
        unit_type: Optional[str] = None,
        force_rarity: Optional[str] = None,
        item_category: Optional[str] = None,
    ) -> Dict:
        """
        Generate a random item.

        Args:
            difficulty: Affects chance of better rarity
            unit_type: Filter to compatible items for this unit type
            force_rarity: Force specific rarity (common, rare, epic, legendary)
            item_category: Filter by category ("weapon", "armor", "artifact")

        Returns:
            Generated item dictionary
        """
        # Select item template
        if item_category:
            if item_category == "weapon":
                templates = WEAPON_TEMPLATES
            elif item_category == "armor":
                templates = ARMOR_TEMPLATES
            elif item_category == "artifact":
                templates = ARTIFACT_TEMPLATES
            else:
                templates = {**WEAPON_TEMPLATES, **ARMOR_TEMPLATES, **ARTIFACT_TEMPLATES}
        else:
            templates = {**WEAPON_TEMPLATES, **ARMOR_TEMPLATES, **ARTIFACT_TEMPLATES}

        # Filter by unit type
        if unit_type:
            compatible_ids = get_items_for_unit_type(unit_type)
            templates = {k: v for k, v in templates.items() if k in compatible_ids}

        if not templates:
            # Fallback: any item
            templates = {**WEAPON_TEMPLATES, **ARMOR_TEMPLATES}

        template_id = self.random.choice(list(templates.keys()))
        template = templates[template_id]

        # Determine rarity
        if force_rarity:
            rarity = force_rarity
        else:
            rarity = self._roll_rarity(difficulty, template.get("min_rarity"))

        # Generate item from template
        return self.generate_item_from_template(template_id, rarity)

    def generate_item_from_template(
        self, template_id: str, rarity: str = "common"
    ) -> Dict:
        """
        Generate an item from a specific template.

        Args:
            template_id: Item template identifier
            rarity: Item rarity

        Returns:
            Generated item dictionary
        """
        template = get_item_template(template_id)
        if not template:
            raise ValueError(f"Unknown item template: {template_id}")

        # Check minimum rarity
        min_rarity = template.get("min_rarity", "common")
        if self._rarity_level(rarity) < self._rarity_level(min_rarity):
            rarity = min_rarity

        # Base stats from template
        item = {
            "id": template_id,
            "name": template["name"],
            "type": template["type"],
            "description": template["description"],
            "rarity": rarity,
            "stats": {},
        }

        # Copy optional fields
        if "required_unit_types" in template:
            item["required_unit_types"] = template["required_unit_types"]
        if "historical_note" in template:
            item["historical_note"] = template["historical_note"]
        if "special_effect" in template:
            item["special_effect"] = template["special_effect"]
        if "single_use" in template:
            item["single_use"] = template["single_use"]

        # Apply rarity multiplier to stats
        multiplier = ITEM_RARITIES[rarity]["stat_multiplier"]
        variance = 0.1  # +/- 10% variance

        # Process all stat bonuses
        stat_keys = [
            "attack_bonus",
            "defense_bonus",
            "armor_bonus",
            "damage_bonus",
            "morale_bonus",
            "movement_penalty",
            "formation_bonus",
            "range_bonus",
            "accuracy_bonus",
            "critical_chance",
            "armor_penetration",
            "leadership_bonus",
            "experience_bonus",
            "vision_penalty",
            "defense_penalty",
        ]

        for stat_key in stat_keys:
            if stat_key in template:
                base_value = template[stat_key]
                # Apply multiplier with variance
                if isinstance(base_value, (int, float)):
                    varied_multiplier = multiplier * (
                        1.0 + self.random.uniform(-variance, variance)
                    )
                    final_value = base_value * varied_multiplier

                    # Round to int for discrete stats
                    if stat_key.endswith("_bonus") or stat_key.endswith("_penalty"):
                        final_value = max(1, round(final_value))
                    elif stat_key in ["critical_chance", "accuracy_bonus"]:
                        final_value = round(final_value, 1)

                    item["stats"][stat_key] = final_value
                else:
                    item["stats"][stat_key] = base_value

        # Add flavor text based on rarity
        item["name"] = self._add_rarity_prefix(item["name"], rarity)

        return item

    def generate_loot_drop(
        self,
        enemy_strength: int,
        enemy_faction: str,
        battle_difficulty: int,
        is_elite: bool = False,
        is_boss: bool = False,
    ) -> List[Dict]:
        """
        Generate loot drops from an enemy.

        Args:
            enemy_strength: Total strength of enemy army
            enemy_faction: Enemy faction
            battle_difficulty: Battle difficulty level
            is_elite: Whether this is an elite encounter
            is_boss: Whether this is a boss encounter

        Returns:
            List of generated items
        """
        loot = []

        # Determine number of items
        if is_boss:
            num_items = self.random.randint(3, 5)
            min_rarity = "epic"
        elif is_elite:
            num_items = self.random.randint(2, 3)
            min_rarity = "rare"
        else:
            # Base drop chance
            drop_chance = min(0.8, 0.3 + (battle_difficulty * 0.05))
            if self.random.random() > drop_chance:
                return []  # No drop
            num_items = self.random.randint(1, 2)
            min_rarity = "common"

        # Generate items
        for _ in range(num_items):
            # Adjust difficulty for rarity calculation
            adjusted_difficulty = battle_difficulty
            if is_elite:
                adjusted_difficulty += 3
            if is_boss:
                adjusted_difficulty += 5

            # Faction-themed items (higher chance)
            if self.random.random() < 0.4:
                item = self._generate_faction_themed_item(
                    enemy_faction, adjusted_difficulty, min_rarity
                )
            else:
                item = self.generate_random_item(
                    difficulty=adjusted_difficulty, force_rarity=None
                )

            # Ensure minimum rarity
            if self._rarity_level(item["rarity"]) < self._rarity_level(min_rarity):
                item = self.generate_item_from_template(item["id"], min_rarity)

            loot.append(item)

        return loot

    def _generate_faction_themed_item(
        self, faction: str, difficulty: int, min_rarity: str
    ) -> Dict:
        """Generate an item themed to a specific faction."""
        faction_items = {
            "rome": ["gladius", "pilum", "scutum", "lorica_segmentata", "galea"],
            "greece": [
                "xiphos",
                "kopis",
                "dory",
                "sarissa",
                "aspis",
                "corinthian_helmet",
                "linothorax",
            ],
            "persia": ["composite_bow", "phrygian_helmet"],
            "carthage": ["sling", "falcata"],
        }

        themed_items = faction_items.get(faction, [])
        if themed_items:
            template_id = self.random.choice(themed_items)
            rarity = self._roll_rarity(difficulty, min_rarity)
            return self.generate_item_from_template(template_id, rarity)
        else:
            return self.generate_random_item(difficulty=difficulty)

    def _roll_rarity(
        self, difficulty: int, min_rarity: Optional[str] = None
    ) -> str:
        """
        Roll for item rarity based on difficulty.

        Args:
            difficulty: Difficulty level (higher = better loot)
            min_rarity: Minimum rarity to roll

        Returns:
            Rarity string
        """
        # Build weighted pool
        weights = []
        rarities = []

        for rarity, data in ITEM_RARITIES.items():
            # Skip if below minimum
            if min_rarity and self._rarity_level(rarity) < self._rarity_level(
                min_rarity
            ):
                continue

            # Adjust weight by difficulty
            base_weight = data["drop_weight"]
            if rarity == "rare":
                adjusted_weight = base_weight * (1 + difficulty * 0.1)
            elif rarity == "epic":
                adjusted_weight = base_weight * (1 + difficulty * 0.15)
            elif rarity == "legendary":
                adjusted_weight = base_weight * (1 + difficulty * 0.2)
            else:
                adjusted_weight = base_weight

            weights.append(adjusted_weight)
            rarities.append(rarity)

        # Roll
        return self.random.choices(rarities, weights=weights)[0]

    def _rarity_level(self, rarity: str) -> int:
        """Convert rarity to numeric level for comparison."""
        levels = {"common": 0, "rare": 1, "epic": 2, "legendary": 3}
        return levels.get(rarity, 0)

    def _add_rarity_prefix(self, name: str, rarity: str) -> str:
        """Add a prefix to item name based on rarity."""
        if rarity == "rare":
            prefixes = ["Fine", "Superior", "Quality", "Masterwork"]
            return f"{self.random.choice(prefixes)} {name}"
        elif rarity == "epic":
            prefixes = ["Exquisite", "Heroic", "Legendary", "Mythic"]
            return f"{self.random.choice(prefixes)} {name}"
        elif rarity == "legendary":
            prefixes = ["Divine", "Godly", "Ancient", "Blessed"]
            return f"{self.random.choice(prefixes)} {name}"
        else:
            return name


# Convenience function
def generate_item(
    template_id: Optional[str] = None,
    rarity: str = "common",
    difficulty: int = 1,
    unit_type: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict:
    """
    Generate an item.

    Args:
        template_id: Specific template to use (None for random)
        rarity: Item rarity
        difficulty: Difficulty level for random generation
        unit_type: Filter by compatible unit type
        seed: Random seed

    Returns:
        Generated item dictionary
    """
    generator = ItemGenerator(seed)

    if template_id:
        return generator.generate_item_from_template(template_id, rarity)
    else:
        return generator.generate_random_item(difficulty, unit_type)


def generate_battle_loot(
    enemy_strength: int,
    enemy_faction: str,
    difficulty: int,
    is_elite: bool = False,
    is_boss: bool = False,
    seed: Optional[int] = None,
) -> List[Dict]:
    """
    Generate loot from a battle.

    Args:
        enemy_strength: Enemy army strength
        enemy_faction: Enemy faction
        difficulty: Battle difficulty
        is_elite: Elite encounter flag
        is_boss: Boss encounter flag
        seed: Random seed

    Returns:
        List of item dictionaries
    """
    generator = ItemGenerator(seed)
    return generator.generate_loot_drop(
        enemy_strength, enemy_faction, difficulty, is_elite, is_boss
    )
