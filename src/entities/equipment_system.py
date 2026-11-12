"""
Equipment system - applies item bonuses to unit stats.
"""

from typing import Dict, List, Optional
from src.entities.components import (
    EquipmentComponent,
    StatsComponent,
    MoraleComponent,
    MovementComponent,
    CombatComponent,
    UnitComponent,
)


class EquipmentSystem:
    """Manages equipment and applies bonuses to units."""

    def __init__(self):
        """Initialize equipment system."""
        pass

    def apply_item_to_unit(self, unit, item: Dict) -> bool:
        """
        Equip an item to a unit.

        Args:
            unit: Unit entity
            item: Item data dictionary

        Returns:
            True if successfully equipped, False otherwise
        """
        equipment = unit.get_component(EquipmentComponent)
        if not equipment:
            return False

        # Check unit type compatibility
        required_types = item.get("required_unit_types", [])
        if required_types:
            unit_comp = unit.get_component(UnitComponent)
            if unit_comp and unit_comp.unit_type not in required_types:
                print(
                    f"Cannot equip {item['name']}: unit type {unit_comp.unit_type} not compatible"
                )
                return False

        # Determine equipment slot
        item_type = item.get("type", "")

        if "weapon" in item_type or item_type in [
            "sword",
            "spear",
            "javelin",
            "bow",
            "ranged",
        ]:
            # Unequip old weapon if exists
            if equipment.weapon:
                self._remove_item_bonuses(unit, equipment.weapon)
            equipment.weapon = item

        elif "armor" in item_type or item_type in [
            "heavy_armor",
            "medium_armor",
            "shield",
            "helmet",
        ]:
            # Unequip old armor if exists
            if equipment.armor:
                self._remove_item_bonuses(unit, equipment.armor)
            equipment.armor = item

        else:
            # Special equipment/artifact
            equipment.special_equipment.append(item)

        # Apply bonuses
        self._apply_item_bonuses(unit, item)

        print(f"Equipped {item['name']} to unit {unit.id}")
        return True

    def unequip_item(self, unit, slot: str) -> Optional[Dict]:
        """
        Unequip an item from a unit.

        Args:
            unit: Unit entity
            slot: "weapon", "armor", or item id for special equipment

        Returns:
            Unequipped item or None
        """
        equipment = unit.get_component(EquipmentComponent)
        if not equipment:
            return None

        item = None

        if slot == "weapon" and equipment.weapon:
            item = equipment.weapon
            self._remove_item_bonuses(unit, item)
            equipment.weapon = None

        elif slot == "armor" and equipment.armor:
            item = equipment.armor
            self._remove_item_bonuses(unit, item)
            equipment.armor = None

        else:
            # Search special equipment by id
            for i, special_item in enumerate(equipment.special_equipment):
                if special_item.get("id") == slot:
                    item = special_item
                    self._remove_item_bonuses(unit, item)
                    equipment.special_equipment.pop(i)
                    break

        if item:
            print(f"Unequipped {item['name']} from unit {unit.id}")

        return item

    def get_effective_stats(self, unit) -> Dict:
        """
        Calculate unit's effective stats including all equipment bonuses.

        Args:
            unit: Unit entity

        Returns:
            Dictionary of effective stat values
        """
        # Base stats
        stats_comp = unit.get_component(StatsComponent)
        morale_comp = unit.get_component(MoraleComponent)
        movement_comp = unit.get_component(MovementComponent)
        combat_comp = unit.get_component(CombatComponent)

        effective_stats = {
            "attack": stats_comp.attack if stats_comp else 10,
            "defense": stats_comp.defense if stats_comp else 10,
            "armor": stats_comp.armor if stats_comp else 0,
            "damage_min": stats_comp.damage_min if stats_comp else 1,
            "damage_max": stats_comp.damage_max if stats_comp else 6,
            "morale": morale_comp.current if morale_comp else 100,
            "movement": movement_comp.movement_points if movement_comp else 3,
            "range": combat_comp.range if combat_comp else 1,
            "accuracy": 0,  # Base accuracy bonus
            "critical_chance": 0,  # Base critical chance
            "armor_penetration": 0,  # Base armor penetration
            "leadership": 0,  # Base leadership
        }

        # Apply equipment bonuses
        equipment = unit.get_component(EquipmentComponent)
        if equipment:
            # Weapon
            if equipment.weapon:
                effective_stats = self._add_item_stats(
                    effective_stats, equipment.weapon
                )

            # Armor
            if equipment.armor:
                effective_stats = self._add_item_stats(effective_stats, equipment.armor)

            # Special equipment
            for item in equipment.special_equipment:
                effective_stats = self._add_item_stats(effective_stats, item)

        return effective_stats

    def _apply_item_bonuses(self, unit, item: Dict) -> None:
        """Apply item stat bonuses to unit components."""
        stats = item.get("stats", {})

        stats_comp = unit.get_component(StatsComponent)
        morale_comp = unit.get_component(MoraleComponent)
        movement_comp = unit.get_component(MovementComponent)
        combat_comp = unit.get_component(CombatComponent)

        # Apply stat bonuses
        if stats_comp:
            if "attack_bonus" in stats:
                stats_comp.attack += int(stats["attack_bonus"])
            if "defense_bonus" in stats:
                stats_comp.defense += int(stats["defense_bonus"])
            if "armor_bonus" in stats:
                stats_comp.armor += int(stats["armor_bonus"])
            if "damage_bonus" in stats:
                stats_comp.damage_min += int(stats["damage_bonus"])
                stats_comp.damage_max += int(stats["damage_bonus"])

        if morale_comp and "morale_bonus" in stats:
            morale_comp.max_morale += int(stats["morale_bonus"])
            morale_comp.current = min(
                morale_comp.current + int(stats["morale_bonus"]), morale_comp.max_morale
            )

        if movement_comp and "movement_penalty" in stats:
            movement_comp.max_movement -= int(stats["movement_penalty"])
            movement_comp.max_movement = max(1, movement_comp.max_movement)

        if combat_comp and "range_bonus" in stats:
            combat_comp.range += int(stats["range_bonus"])

        # Note: Some stats like accuracy, critical_chance, armor_penetration
        # don't have direct component storage, so they're only applied
        # through get_effective_stats() when needed

    def _remove_item_bonuses(self, unit, item: Dict) -> None:
        """Remove item stat bonuses from unit components."""
        stats = item.get("stats", {})

        stats_comp = unit.get_component(StatsComponent)
        morale_comp = unit.get_component(MoraleComponent)
        movement_comp = unit.get_component(MovementComponent)
        combat_comp = unit.get_component(CombatComponent)

        # Remove stat bonuses
        if stats_comp:
            if "attack_bonus" in stats:
                stats_comp.attack -= int(stats["attack_bonus"])
            if "defense_bonus" in stats:
                stats_comp.defense -= int(stats["defense_bonus"])
            if "armor_bonus" in stats:
                stats_comp.armor -= int(stats["armor_bonus"])
            if "damage_bonus" in stats:
                stats_comp.damage_min -= int(stats["damage_bonus"])
                stats_comp.damage_max -= int(stats["damage_bonus"])

        if morale_comp and "morale_bonus" in stats:
            morale_comp.max_morale -= int(stats["morale_bonus"])
            morale_comp.current = min(morale_comp.current, morale_comp.max_morale)

        if movement_comp and "movement_penalty" in stats:
            movement_comp.max_movement += int(stats["movement_penalty"])

        if combat_comp and "range_bonus" in stats:
            combat_comp.range -= int(stats["range_bonus"])
            combat_comp.range = max(1, combat_comp.range)

    def _add_item_stats(self, base_stats: Dict, item: Dict) -> Dict:
        """Add item stats to a base stats dictionary."""
        item_stats = item.get("stats", {})
        result = base_stats.copy()

        # Map item stats to effective stats
        stat_mappings = {
            "attack_bonus": "attack",
            "defense_bonus": "defense",
            "armor_bonus": "armor",
            "damage_bonus": lambda r: (
                r.update(
                    {
                        "damage_min": r["damage_min"] + int(item_stats["damage_bonus"]),
                        "damage_max": r["damage_max"] + int(item_stats["damage_bonus"]),
                    }
                )
                or r
            ),
            "morale_bonus": "morale",
            "range_bonus": "range",
            "accuracy_bonus": "accuracy",
            "critical_chance": "critical_chance",
            "armor_penetration": "armor_penetration",
            "leadership_bonus": "leadership",
        }

        for item_stat, target in stat_mappings.items():
            if item_stat in item_stats:
                if callable(target):
                    target(result)
                else:
                    if target in result:
                        result[target] += item_stats[item_stat]
                    else:
                        result[target] = item_stats[item_stat]

        # Handle penalties
        if "movement_penalty" in item_stats:
            result["movement"] = max(1, result["movement"] - int(item_stats["movement_penalty"]))

        if "defense_penalty" in item_stats:
            result["defense"] -= int(item_stats["defense_penalty"])

        return result

    def get_all_equipped_items(self, unit) -> List[Dict]:
        """
        Get all items equipped on a unit.

        Args:
            unit: Unit entity

        Returns:
            List of equipped items
        """
        equipment = unit.get_component(EquipmentComponent)
        if not equipment:
            return []

        items = []
        if equipment.weapon:
            items.append(equipment.weapon)
        if equipment.armor:
            items.append(equipment.armor)
        items.extend(equipment.special_equipment)

        return items
