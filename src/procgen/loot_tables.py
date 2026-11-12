"""
Loot tables and reward systems for battles and events.
Defines drop chances, gold rewards, and experience.
"""

import random
from typing import Dict, List, Optional, Tuple
from src.procgen.item_generator import ItemGenerator


class LootTable:
    """Manages loot drops and rewards."""

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize loot table.

        Args:
            seed: Random seed for reproducibility
        """
        self.random = random.Random(seed)
        self.item_generator = ItemGenerator(seed)

    def calculate_battle_rewards(
        self,
        enemy_faction: str,
        enemy_units: List[Dict],
        difficulty: int,
        is_elite: bool = False,
        is_boss: bool = False,
        victory_type: str = "normal",
    ) -> Dict:
        """
        Calculate all rewards from a battle.

        Args:
            enemy_faction: Enemy faction name
            enemy_units: List of enemy unit data
            difficulty: Battle difficulty level
            is_elite: Elite encounter flag
            is_boss: Boss encounter flag
            victory_type: "normal", "flawless", or "pyrrhic"

        Returns:
            Dictionary of rewards
        """
        # Calculate enemy strength
        enemy_strength = sum(unit.get("count", 100) for unit in enemy_units)

        # Base rewards
        gold = self._calculate_gold_reward(
            enemy_strength, difficulty, is_elite, is_boss
        )
        experience = self._calculate_experience_reward(
            enemy_strength, difficulty, is_elite, is_boss
        )

        # Item drops
        items = self.item_generator.generate_loot_drop(
            enemy_strength, enemy_faction, difficulty, is_elite, is_boss
        )

        # Victory type bonus
        if victory_type == "flawless":
            gold = int(gold * 1.5)
            experience = int(experience * 1.3)
            # Extra item chance
            if self.random.random() < 0.3:
                bonus_item = self.item_generator.generate_random_item(
                    difficulty=difficulty + 2
                )
                items.append(bonus_item)
        elif victory_type == "pyrrhic":
            gold = int(gold * 0.7)
            experience = int(experience * 0.8)

        # Resources (food, supplies)
        food = self._calculate_resource_reward(enemy_strength, "food")
        supplies = self._calculate_resource_reward(enemy_strength, "supplies")

        # Prisoners/recruits chance
        recruits = self._calculate_recruit_chance(
            enemy_units, victory_type, enemy_faction
        )

        return {
            "gold": gold,
            "experience": experience,
            "items": items,
            "food": food,
            "supplies": supplies,
            "recruits": recruits,
            "victory_type": victory_type,
        }

    def _calculate_gold_reward(
        self, enemy_strength: int, difficulty: int, is_elite: bool, is_boss: bool
    ) -> int:
        """Calculate gold reward from battle."""
        base_gold = 50 + (enemy_strength * 0.5)

        # Difficulty multiplier
        difficulty_mult = 1.0 + (difficulty * 0.1)

        # Encounter type multiplier
        if is_boss:
            base_gold *= 3.0
        elif is_elite:
            base_gold *= 2.0

        # Random variance
        variance = self.random.uniform(0.85, 1.15)

        return int(base_gold * difficulty_mult * variance)

    def _calculate_experience_reward(
        self, enemy_strength: int, difficulty: int, is_elite: bool, is_boss: bool
    ) -> int:
        """Calculate experience reward from battle."""
        base_xp = 100 + (enemy_strength * 0.3)

        # Difficulty multiplier
        difficulty_mult = 1.0 + (difficulty * 0.15)

        # Encounter type multiplier
        if is_boss:
            base_xp *= 2.5
        elif is_elite:
            base_xp *= 1.75

        return int(base_xp * difficulty_mult)

    def _calculate_resource_reward(self, enemy_strength: int, resource_type: str) -> int:
        """Calculate resource rewards (food, supplies)."""
        base_amount = 10 + (enemy_strength * 0.2)

        if resource_type == "food":
            multiplier = 1.2
        elif resource_type == "supplies":
            multiplier = 0.8
        else:
            multiplier = 1.0

        variance = self.random.uniform(0.8, 1.2)
        return int(base_amount * multiplier * variance)

    def _calculate_recruit_chance(
        self, enemy_units: List[Dict], victory_type: str, enemy_faction: str
    ) -> List[Dict]:
        """Calculate chance to recruit defeated units."""
        recruits = []

        # Base recruit chance
        if victory_type == "flawless":
            base_chance = 0.4
        elif victory_type == "normal":
            base_chance = 0.2
        else:  # pyrrhic
            base_chance = 0.05

        for unit in enemy_units:
            if self.random.random() < base_chance:
                # Calculate how many soldiers join
                max_count = unit.get("count", 100)
                recruit_count = self.random.randint(
                    int(max_count * 0.1), int(max_count * 0.3)
                )

                if recruit_count > 0:
                    recruits.append(
                        {
                            "unit_type": unit.get("unit_type", "infantry"),
                            "count": recruit_count,
                            "faction": enemy_faction,
                        }
                    )

        return recruits

    def get_merchant_shop_inventory(
        self, shop_level: int = 1, faction: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate merchant shop inventory.

        Args:
            shop_level: Level of the shop (affects quality and quantity)
            faction: Optional faction theme for items

        Returns:
            List of items for sale with prices
        """
        inventory = []

        # Number of items based on shop level
        num_items = 3 + shop_level

        for _ in range(num_items):
            # Shop level affects rarity chances
            if shop_level >= 5:
                difficulty = self.random.randint(5, 8)
            elif shop_level >= 3:
                difficulty = self.random.randint(3, 6)
            else:
                difficulty = self.random.randint(1, 4)

            # Generate item
            if faction and self.random.random() < 0.5:
                item = self.item_generator._generate_faction_themed_item(
                    faction, difficulty, "common"
                )
            else:
                item = self.item_generator.generate_random_item(difficulty=difficulty)

            # Calculate price
            price = self._calculate_item_price(item)

            inventory.append({"item": item, "price": price})

        return inventory

    def _calculate_item_price(self, item: Dict) -> int:
        """Calculate the purchase price of an item."""
        # Base price by rarity
        rarity_prices = {
            "common": 100,
            "rare": 300,
            "epic": 800,
            "legendary": 2000,
        }

        base_price = rarity_prices.get(item["rarity"], 100)

        # Add stat bonuses to price
        stats = item.get("stats", {})
        stat_value = sum(
            abs(v) for v in stats.values() if isinstance(v, (int, float))
        )

        total_price = base_price + (stat_value * 20)

        # Special effects increase price
        if "special_effect" in item:
            total_price = int(total_price * 1.5)

        return int(total_price)

    def get_treasure_loot(
        self, treasure_level: int = 1, is_hidden: bool = False
    ) -> Dict:
        """
        Generate loot from treasure chests or hidden caches.

        Args:
            treasure_level: Level/quality of treasure
            is_hidden: Whether this is a hidden treasure (better loot)

        Returns:
            Treasure contents dictionary
        """
        loot = {"gold": 0, "items": []}

        # Gold amount
        base_gold = 100 * treasure_level
        if is_hidden:
            base_gold *= 2

        loot["gold"] = int(base_gold * self.random.uniform(0.8, 1.3))

        # Items
        num_items = 1 if not is_hidden else self.random.randint(2, 3)
        min_rarity = "rare" if is_hidden else "common"

        for _ in range(num_items):
            difficulty = treasure_level + (2 if is_hidden else 0)
            item = self.item_generator.generate_random_item(
                difficulty=difficulty, force_rarity=None
            )

            # Ensure minimum rarity for hidden treasures
            if (
                is_hidden
                and self.item_generator._rarity_level(item["rarity"])
                < self.item_generator._rarity_level(min_rarity)
            ):
                item = self.item_generator.generate_item_from_template(
                    item["id"], min_rarity
                )

            loot["items"].append(item)

        return loot

    def get_event_rewards(self, event_type: str, player_choice: str) -> Dict:
        """
        Get rewards from event outcomes.

        Args:
            event_type: Type of event (shrine, merchant, etc.)
            player_choice: Player's choice in the event

        Returns:
            Event rewards
        """
        rewards = {"gold": 0, "items": [], "effects": []}

        if event_type == "shrine":
            if player_choice == "pray":
                # Blessing effect
                rewards["effects"] = [
                    {"type": "blessing", "stat": "morale", "bonus": 10, "duration": 3}
                ]
            elif player_choice == "donate":
                # Gold cost but better blessing
                rewards["gold"] = -100
                rewards["effects"] = [
                    {"type": "blessing", "stat": "attack", "bonus": 2, "duration": 3},
                    {"type": "blessing", "stat": "defense", "bonus": 2, "duration": 3},
                ]

        elif event_type == "ambush":
            if player_choice == "fight":
                # Battle rewards (handled separately)
                pass
            elif player_choice == "flee":
                # Lose some gold
                rewards["gold"] = -50

        elif event_type == "treasure_map":
            if player_choice == "follow":
                # Treasure!
                treasure = self.get_treasure_loot(
                    treasure_level=self.random.randint(2, 4), is_hidden=True
                )
                rewards["gold"] = treasure["gold"]
                rewards["items"] = treasure["items"]

        elif event_type == "mysterious_trader":
            if player_choice == "trade":
                # Random powerful item
                item = self.item_generator.generate_random_item(
                    difficulty=5, force_rarity="rare"
                )
                rewards["items"] = [item]
                rewards["gold"] = -200

        return rewards


# Convenience functions
def calculate_battle_rewards(
    enemy_faction: str,
    enemy_units: List[Dict],
    difficulty: int,
    is_elite: bool = False,
    is_boss: bool = False,
    victory_type: str = "normal",
    seed: Optional[int] = None,
) -> Dict:
    """
    Calculate rewards from a battle victory.

    Args:
        enemy_faction: Enemy faction
        enemy_units: List of enemy units
        difficulty: Battle difficulty
        is_elite: Elite encounter flag
        is_boss: Boss encounter flag
        victory_type: Type of victory
        seed: Random seed

    Returns:
        Rewards dictionary
    """
    loot_table = LootTable(seed)
    return loot_table.calculate_battle_rewards(
        enemy_faction, enemy_units, difficulty, is_elite, is_boss, victory_type
    )


def generate_merchant_shop(
    shop_level: int = 1, faction: Optional[str] = None, seed: Optional[int] = None
) -> List[Dict]:
    """
    Generate merchant inventory.

    Args:
        shop_level: Shop quality level
        faction: Optional faction theme
        seed: Random seed

    Returns:
        Shop inventory with prices
    """
    loot_table = LootTable(seed)
    return loot_table.get_merchant_shop_inventory(shop_level, faction)
