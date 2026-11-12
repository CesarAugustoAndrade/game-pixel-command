"""
Event processing system - handles event resolution and outcomes.
"""

import random
from typing import Dict, List, Optional, Tuple
from src.data.event_definitions import get_event_by_id, get_events_by_category
from src.procgen.item_generator import ItemGenerator
from src.procgen.loot_tables import LootTable


class EventProcessor:
    """Processes events, choices, and applies outcomes."""

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize event processor.

        Args:
            seed: Random seed for reproducibility
        """
        self.random = random.Random(seed)
        self.item_generator = ItemGenerator(seed)
        self.loot_table = LootTable(seed)

    def select_random_event(
        self,
        category: Optional[str] = None,
        exclude_events: Optional[List[str]] = None,
    ) -> Dict:
        """
        Select a random event.

        Args:
            category: Optional category filter
            exclude_events: List of event IDs to exclude

        Returns:
            Event template dictionary
        """
        if category:
            from src.data.event_definitions import get_events_by_category

            event_ids = get_events_by_category(category)
        else:
            from src.data.event_definitions import get_all_event_ids

            event_ids = get_all_event_ids()

        # Filter out excluded events
        if exclude_events:
            event_ids = [e for e in event_ids if e not in exclude_events]

        if not event_ids:
            return {}

        event_id = self.random.choice(event_ids)
        event = get_event_by_id(event_id)
        event["id"] = event_id  # Add ID to returned event
        return event

    def process_choice(
        self,
        event: Dict,
        choice_id: str,
        player_stats: Dict,
        player_resources: Dict,
    ) -> Dict:
        """
        Process a player's choice in an event.

        Args:
            event: Event data dictionary
            choice_id: Chosen option ID
            player_stats: Player/army stats for skill checks
            player_resources: Player resources (gold, food, etc.)

        Returns:
            Result dictionary with effects, message, and updated resources
        """
        # Find the chosen choice
        choice = None
        for c in event.get("choices", []):
            if c["id"] == choice_id:
                choice = c
                break

        if not choice:
            return {
                "success": False,
                "message": "Invalid choice",
                "effects": [],
                "resources_changed": {},
            }

        # Check costs
        cost = choice.get("cost", {})
        if not self._can_afford(player_resources, cost):
            return {
                "success": False,
                "message": "Insufficient resources for this choice",
                "effects": [],
                "resources_changed": {},
            }

        # Deduct costs
        resources_changed = {}
        for resource, amount in cost.items():
            resources_changed[resource] = -amount

        # Check skill check if required
        skill_check = choice.get("skill_check")
        skill_check_passed = None

        if skill_check:
            skill_check_passed = self._evaluate_skill_check(skill_check, player_stats)

        # Select outcome
        outcome = self._select_outcome(choice["outcomes"], skill_check_passed)

        # Apply outcome effects
        effects = self._process_effects(outcome["effects"], player_stats, event)

        return {
            "success": True,
            "message": outcome["message"],
            "effects": effects,
            "resources_changed": resources_changed,
            "skill_check_result": skill_check_passed,
        }

    def _can_afford(self, resources: Dict, cost: Dict) -> bool:
        """Check if player can afford the cost."""
        for resource, amount in cost.items():
            if resources.get(resource, 0) < amount:
                return False
        return True

    def _evaluate_skill_check(self, skill_check: Dict, player_stats: Dict) -> bool:
        """
        Evaluate a skill check.

        Args:
            skill_check: Skill check requirements
            player_stats: Player stats

        Returns:
            True if passed, False if failed
        """
        check_type = skill_check.get("type")
        threshold = skill_check.get("threshold", 0)

        # Get relevant stat
        stat_value = player_stats.get(check_type, 0)

        # Add some randomness (d20-style roll)
        roll = self.random.randint(1, 20)
        total = stat_value + roll

        return total >= threshold

    def _select_outcome(
        self, outcomes: List[Dict], skill_check_result: Optional[bool]
    ) -> Dict:
        """
        Select an outcome based on weights and skill check results.

        Args:
            outcomes: List of possible outcomes
            skill_check_result: Result of skill check (None if no check)

        Returns:
            Selected outcome
        """
        # Filter outcomes based on skill check
        valid_outcomes = []

        for outcome in outcomes:
            if skill_check_result is not None:
                if outcome.get("success_only") and not skill_check_result:
                    continue
                if outcome.get("failure_only") and skill_check_result:
                    continue

            valid_outcomes.append(outcome)

        if not valid_outcomes:
            # Fallback
            return {"weight": 100, "effects": [], "message": "Nothing happens."}

        # Weighted random selection
        weights = [o.get("weight", 100) for o in valid_outcomes]
        return self.random.choices(valid_outcomes, weights=weights)[0]

    def _process_effects(
        self, effects: List[Dict], player_stats: Dict, event: Dict
    ) -> List[Dict]:
        """
        Process and generate actual effect data from effect templates.

        Args:
            effects: List of effect templates
            player_stats: Player stats
            event: Event data

        Returns:
            List of processed effects with generated data
        """
        processed_effects = []

        for effect in effects:
            effect_type = effect.get("type")
            processed_effect = {"type": effect_type}

            if effect_type == "blessing" or effect_type == "debuff":
                processed_effect.update(
                    {
                        "stat": effect.get("stat"),
                        "value": effect.get("value"),
                        "duration": effect.get("duration", 1),
                    }
                )

            elif effect_type == "reward":
                processed_effect.update(
                    {
                        "gold": effect.get("gold", 0),
                        "experience": effect.get("experience", 0),
                        "food": effect.get("food", 0),
                        "supplies": effect.get("supplies", 0),
                    }
                )

            elif effect_type == "item_reward":
                # Generate item
                difficulty = player_stats.get("difficulty_level", 1)
                min_rarity = effect.get("min_rarity")
                force_rarity = effect.get("force_rarity")
                artifact_id = effect.get("artifact")

                if artifact_id:
                    # Specific artifact
                    item = self.item_generator.generate_item_from_template(
                        artifact_id, "legendary"
                    )
                else:
                    # Random item
                    item = self.item_generator.generate_random_item(
                        difficulty=difficulty,
                        force_rarity=force_rarity if force_rarity else None,
                    )

                    # Enforce minimum rarity
                    if min_rarity:
                        item_rarity_level = self.item_generator._rarity_level(
                            item["rarity"]
                        )
                        min_rarity_level = self.item_generator._rarity_level(min_rarity)
                        if item_rarity_level < min_rarity_level:
                            item = self.item_generator.generate_item_from_template(
                                item["id"], min_rarity
                            )

                processed_effect["item"] = item

            elif effect_type == "treasure":
                level = effect.get("level", 1)
                is_hidden = effect.get("hidden", False)
                treasure = self.loot_table.get_treasure_loot(level, is_hidden)
                processed_effect.update(treasure)

            elif effect_type == "open_shop":
                shop_level = effect.get("shop_level", 1)
                inventory = self.loot_table.get_merchant_shop_inventory(shop_level)
                processed_effect["shop_inventory"] = inventory

            elif effect_type == "battle":
                processed_effect.update(
                    {
                        "enemy_type": effect.get("enemy_type", "bandits"),
                        "difficulty_modifier": effect.get("difficulty_modifier", 0),
                        "ambush": effect.get("ambush", False),
                    }
                )

            elif effect_type == "lose_health":
                processed_effect["casualties"] = effect.get("value", 0)

            elif effect_type == "heal":
                processed_effect["heal_percent"] = effect.get("percent", 10)

            elif effect_type == "consume_food":
                processed_effect["food_cost"] = effect.get("value", 0)

            elif effect_type == "recruit_units":
                count_str = effect.get("count", "1")
                if "-" in count_str:
                    min_count, max_count = map(int, count_str.split("-"))
                    count = self.random.randint(min_count, max_count)
                else:
                    count = int(count_str)

                processed_effect["recruit_count"] = count
                processed_effect["random"] = effect.get("random", False)

            elif effect_type == "reveal_map":
                processed_effect["radius"] = effect.get("radius", 1)

            else:
                # Pass through any other effect data
                processed_effect.update(effect)

            processed_effects.append(processed_effect)

        return processed_effects

    def get_event_preview(self, event: Dict, player_resources: Dict) -> Dict:
        """
        Get a preview of an event including which choices are available.

        Args:
            event: Event data
            player_resources: Player resources

        Returns:
            Dictionary with event info and available choices
        """
        available_choices = []

        for choice in event.get("choices", []):
            cost = choice.get("cost", {})
            can_afford = self._can_afford(player_resources, cost)

            choice_info = {
                "id": choice["id"],
                "text": choice["text"],
                "can_afford": can_afford,
                "cost": cost,
                "has_skill_check": "skill_check" in choice,
            }

            if choice_info["has_skill_check"]:
                skill_check = choice["skill_check"]
                choice_info["skill_check_type"] = skill_check.get("type")
                choice_info["skill_check_threshold"] = skill_check.get("threshold")

            available_choices.append(choice_info)

        return {
            "id": event.get("id"),
            "name": event.get("name"),
            "description": event.get("description"),
            "category": event.get("category"),
            "choices": available_choices,
        }


# Convenience functions
def select_event(
    category: Optional[str] = None,
    exclude: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> Dict:
    """Select a random event."""
    processor = EventProcessor(seed)
    return processor.select_random_event(category, exclude)


def process_event_choice(
    event: Dict,
    choice_id: str,
    player_stats: Dict,
    player_resources: Dict,
    seed: Optional[int] = None,
) -> Dict:
    """Process an event choice and return the result."""
    processor = EventProcessor(seed)
    return processor.process_choice(event, choice_id, player_stats, player_resources)
