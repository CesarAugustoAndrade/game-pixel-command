"""
Advance Wars-style deterministic combat calculator.
No RNG - all damage is predictable based on unit matchups, HP, and terrain.
"""

from typing import Dict, Any, Optional, Tuple
from src.core.constants import UNIT_MATCHUPS, TERRAIN_DEFENSE_STARS, MORALE_STATES


class CombatCalculator:
    """
    Handles deterministic combat calculations with unit matchups and counter-attacks.
    """

    def __init__(self):
        """Initialize combat calculator with matchup tables."""
        self.matchup_table = UNIT_MATCHUPS
        self.terrain_defense = TERRAIN_DEFENSE_STARS
        self.morale_states = MORALE_STATES

    def get_matchup_bonus(self, attacker_type: str, defender_type: str) -> int:
        """
        Get the base damage percentage for a unit matchup.

        Args:
            attacker_type: Type of attacking unit
            defender_type: Type of defending unit

        Returns:
            Damage percentage (100 = normal, 120 = advantage, 80 = disadvantage)
        """
        # Normalize unit types
        attacker_type = attacker_type.lower()
        defender_type = defender_type.lower()

        # Handle generic types
        if attacker_type not in self.matchup_table:
            # Default to infantry if unknown type
            attacker_type = "infantry"

        if defender_type not in self.matchup_table[attacker_type]:
            # Default to 100% if defender type unknown
            return 100

        return self.matchup_table[attacker_type][defender_type]

    def calculate_damage(
        self,
        attacker: Dict[str, Any],
        defender: Dict[str, Any],
        terrain_type: str = "plains"
    ) -> int:
        """
        Calculate deterministic damage from attacker to defender.

        Formula:
        1. Base damage% = unit matchup percentage
        2. HP-scaled damage% = base × (attacker_hp / max_hp)
        3. Apply terrain defense = damage × (1 - terrain_stars × 0.1)
        4. Convert to casualties

        Args:
            attacker: Attacker unit data with 'attack', 'count', 'unit_type'
            defender: Defender unit data with 'defense', 'count', 'unit_type'
            terrain_type: Terrain the defender is on

        Returns:
            Number of casualties inflicted
        """
        # Get unit types (default to infantry if not specified)
        attacker_type = attacker.get("unit_type", "infantry").lower()
        defender_type = defender.get("unit_type", "infantry").lower()

        # 1. Get base matchup percentage
        base_damage_percent = self.get_matchup_bonus(attacker_type, defender_type)

        # 2. Scale by attacker's HP percentage
        attacker_current_hp = attacker.get("count", 100)
        attacker_max_hp = attacker.get("max_count", attacker_current_hp)
        hp_percentage = attacker_current_hp / attacker_max_hp if attacker_max_hp > 0 else 1.0

        # Apply HP scaling to damage
        hp_scaled_damage = base_damage_percent * hp_percentage

        # 3. Apply terrain defense
        terrain_stars = self.terrain_defense.get(terrain_type, 0)
        terrain_reduction = 1.0 - (terrain_stars * 0.1)
        final_damage_percent = hp_scaled_damage * terrain_reduction

        # 4. Calculate actual casualties
        defender_count = defender.get("count", 100)
        casualties = int(defender_count * (final_damage_percent / 100))

        # Minimum 1 casualty if any damage was dealt
        if final_damage_percent > 0:
            casualties = max(1, casualties)

        return casualties

    def preview_combat(
        self,
        attacker: Dict[str, Any],
        defender: Dict[str, Any],
        attacker_terrain: str = "plains",
        defender_terrain: str = "plains",
        can_counter: bool = True
    ) -> Dict[str, Any]:
        """
        Preview the outcome of combat before it happens.

        Args:
            attacker: Attacker unit data
            defender: Defender unit data
            attacker_terrain: Terrain attacker is on (for counter-attack)
            defender_terrain: Terrain defender is on
            can_counter: Whether defender can counter-attack

        Returns:
            Dict with predicted damage for both sides
        """
        # Calculate attacker damage to defender
        attacker_damage = self.calculate_damage(attacker, defender, defender_terrain)

        # Calculate counter damage if applicable
        counter_damage = 0
        if can_counter and defender.get("count", 0) > attacker_damage:
            # Defender survives and can counter
            # Create defender state after taking damage
            defender_after = defender.copy()
            defender_after["count"] = defender.get("count", 100) - attacker_damage

            # Calculate counter damage with reduced HP
            counter_damage = self.calculate_damage(defender_after, attacker, attacker_terrain)

        # Determine matchup advantage
        attacker_type = attacker.get("unit_type", "infantry").lower()
        defender_type = defender.get("unit_type", "infantry").lower()
        matchup_bonus = self.get_matchup_bonus(attacker_type, defender_type)

        if matchup_bonus > 110:
            matchup_desc = "Strong Advantage"
            matchup_symbol = "⚔️✓"
        elif matchup_bonus > 100:
            matchup_desc = "Slight Advantage"
            matchup_symbol = "✓"
        elif matchup_bonus == 100:
            matchup_desc = "Even Match"
            matchup_symbol = "="
        elif matchup_bonus > 80:
            matchup_desc = "Slight Disadvantage"
            matchup_symbol = "⚠"
        else:
            matchup_desc = "Strong Disadvantage"
            matchup_symbol = "✗"

        return {
            "attacker_damage_dealt": attacker_damage,
            "defender_damage_dealt": counter_damage,
            "attacker_remaining": max(0, attacker.get("count", 100) - counter_damage),
            "defender_remaining": max(0, defender.get("count", 100) - attacker_damage),
            "defender_eliminated": attacker_damage >= defender.get("count", 100),
            "attacker_eliminated": counter_damage >= attacker.get("count", 100),
            "can_counter": can_counter,
            "matchup_bonus": matchup_bonus,
            "matchup_description": matchup_desc,
            "matchup_symbol": matchup_symbol,
            "attacker_terrain_stars": self.terrain_defense.get(attacker_terrain, 0),
            "defender_terrain_stars": self.terrain_defense.get(defender_terrain, 0),
        }

    def resolve_combat_with_counter(
        self,
        attacker: Dict[str, Any],
        defender: Dict[str, Any],
        attacker_terrain: str = "plains",
        defender_terrain: str = "plains",
        can_counter: bool = True
    ) -> Dict[str, Any]:
        """
        Resolve combat including counter-attack.

        Args:
            attacker: Attacker unit data
            defender: Defender unit data
            attacker_terrain: Terrain attacker is on
            defender_terrain: Terrain defender is on
            can_counter: Whether defender can counter

        Returns:
            Combat result with casualties for both sides
        """
        # Get preview (which calculates everything)
        result = self.preview_combat(
            attacker, defender,
            attacker_terrain, defender_terrain,
            can_counter
        )

        # Apply casualties (this would be done by the calling function)
        result["combat_resolved"] = True

        return result

    def get_morale_state(
        self,
        unit: Dict[str, Any],
        nearby_allies: int = 0
    ) -> str:
        """
        Determine unit's morale state based on HP and nearby allies.

        Args:
            unit: Unit data with current/max HP
            nearby_allies: Number of allied units within 2 hexes

        Returns:
            Morale state key ("high_morale", "normal", "shaken", "broken")
        """
        current_hp = unit.get("count", 100)
        max_hp = unit.get("max_count", current_hp)
        hp_percent = current_hp / max_hp if max_hp > 0 else 1.0

        # Determine morale state
        if hp_percent < 0.25 or (hp_percent < 0.5 and nearby_allies == 0):
            return "broken"
        elif hp_percent < 0.5:
            return "shaken"
        elif nearby_allies >= 3 and hp_percent > 0.8:
            return "high_morale"
        else:
            return "normal"

    def apply_morale_modifiers(
        self,
        base_damage: int,
        attacker_morale: str,
        defender_morale: str
    ) -> int:
        """
        Apply morale modifiers to damage.

        Args:
            base_damage: Base damage before morale
            attacker_morale: Attacker's morale state
            defender_morale: Defender's morale state

        Returns:
            Modified damage
        """
        # Get morale modifiers
        attacker_bonus = self.morale_states.get(attacker_morale, {}).get("damage_bonus", 1.0)
        defender_bonus = self.morale_states.get(defender_morale, {}).get("defense_bonus", 1.0)

        # Apply modifiers
        modified_damage = base_damage * attacker_bonus / defender_bonus

        return max(1, int(modified_damage))

    def get_matchup_description(
        self,
        attacker_type: str,
        defender_type: str
    ) -> str:
        """
        Get a text description of the matchup.

        Args:
            attacker_type: Attacking unit type
            defender_type: Defending unit type

        Returns:
            Description of the matchup advantage
        """
        bonus = self.get_matchup_bonus(attacker_type, defender_type)

        if bonus >= 120:
            return f"{attacker_type.title()} dominates {defender_type.title()}!"
        elif bonus >= 110:
            return f"{attacker_type.title()} has advantage vs {defender_type.title()}"
        elif bonus > 100:
            return f"{attacker_type.title()} slightly favored"
        elif bonus == 100:
            return "Even matchup"
        elif bonus >= 80:
            return f"{defender_type.title()} resists {attacker_type.title()}"
        elif bonus >= 60:
            return f"{defender_type.title()} has advantage"
        else:
            return f"{defender_type.title()} dominates {attacker_type.title()}!"