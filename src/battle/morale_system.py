"""
Morale system for units and armies in combat.
Supports both unit-level and army-level morale for morale-driven warfare.
"""

from typing import Dict, Any, Optional
from src.core.constants import *
from src.core.morale_constants import *
from src.core.event_system import EventSystem, EVENT_MORALE_CHANGED


class MoraleSystem:
    """
    Manages unit morale and morale-based effects (fleeing, routing, etc.).
    """

    def __init__(self, event_system: EventSystem):
        """
        Initialize morale system.

        Args:
            event_system: Event system for broadcasting morale events
        """
        self.event_system = event_system

    def initialize_unit_morale(self, unit: Dict[str, Any]) -> None:
        """
        Initialize morale for a unit.

        Args:
            unit: Unit data dict
        """
        if "morale" not in unit:
            unit["morale"] = MORALE_MAX
        unit["is_broken"] = False
        unit["is_routed"] = False

    def modify_morale(self, unit: Dict[str, Any], change: int, reason: str = "") -> None:
        """
        Modify a unit's morale value.

        Args:
            unit: Unit data
            change: Morale change (positive or negative)
            reason: Reason for morale change
        """
        old_morale = unit.get("morale", MORALE_MAX)
        new_morale = max(0, min(MORALE_MAX, old_morale + change))

        unit["morale"] = new_morale

        # Check for morale state changes
        self._check_morale_state(unit)

        # Broadcast morale change event
        self.event_system.emit(EVENT_MORALE_CHANGED, {
            "unit_id": unit.get("id"),
            "old_morale": old_morale,
            "new_morale": new_morale,
            "change": change,
            "reason": reason,
        })

    def _check_morale_state(self, unit: Dict[str, Any]) -> None:
        """
        Check and update morale state (broken, routed, etc.).

        Args:
            unit: Unit data
        """
        morale = unit.get("morale", MORALE_MAX)

        # Check for routing
        if morale <= MORALE_ROUT_THRESHOLD and not unit.get("is_routed", False):
            unit["is_routed"] = True
            unit["is_broken"] = True
            self._handle_unit_rout(unit)

        # Check for morale break
        elif morale <= MORALE_BREAK_THRESHOLD and not unit.get("is_broken", False):
            unit["is_broken"] = True
            self._handle_unit_break(unit)

        # Check for morale recovery
        elif morale > MORALE_BREAK_THRESHOLD and unit.get("is_broken", False):
            unit["is_broken"] = False
            unit["is_routed"] = False

    def _handle_unit_break(self, unit: Dict[str, Any]) -> None:
        """
        Handle a unit breaking (morale < threshold but not routed).

        Args:
            unit: Unit data
        """
        # Broken units have reduced effectiveness
        # TODO: Apply combat penalties
        pass

    def _handle_unit_rout(self, unit: Dict[str, Any]) -> None:
        """
        Handle a unit routing (fleeing the battlefield).

        Args:
            unit: Unit data
        """
        # Routed units try to flee
        # TODO: Implement fleeing behavior
        pass

    def apply_combat_morale_effects(
        self,
        attacker: Dict[str, Any],
        defender: Dict[str, Any],
        combat_result: Dict[str, Any],
    ) -> None:
        """
        Apply morale effects from combat.

        Args:
            attacker: Attacking unit
            defender: Defending unit
            combat_result: Result dict from CombatCalculator
        """
        # Attacker gains morale for casualties inflicted
        if combat_result.get("casualties", 0) > 0:
            morale_gain = min(5, combat_result["casualties"] // 10)
            self.modify_morale(attacker, morale_gain, "successful_attack")

        # Defender loses morale for casualties taken
        casualties = combat_result.get("casualties", 0)
        if casualties > 0:
            morale_loss = -max(3, casualties // 5)
            self.modify_morale(defender, morale_loss, "casualties_taken")

        # Extra morale loss if critical hit
        if combat_result.get("critical", False):
            self.modify_morale(defender, -5, "critical_hit_taken")

    def apply_flanking_morale_penalty(self, unit: Dict[str, Any]) -> None:
        """
        Apply morale penalty for being flanked.

        Args:
            unit: Unit being flanked
        """
        self.modify_morale(unit, -10, "flanked")

    def apply_ally_rout_penalty(self, unit: Dict[str, Any]) -> None:
        """
        Apply morale penalty when a nearby ally routs.

        Args:
            unit: Unit affected by ally routing
        """
        self.modify_morale(unit, -8, "ally_routed")

    def apply_victory_morale(self, unit: Dict[str, Any]) -> None:
        """
        Apply morale bonus for victory.

        Args:
            unit: Victorious unit
        """
        self.modify_morale(unit, 20, "victory")

    def get_morale_modifier(self, unit: Dict[str, Any]) -> float:
        """
        Get combat modifier based on current morale.

        Args:
            unit: Unit data

        Returns:
            Combat effectiveness modifier (0.5 to 1.2)
        """
        morale = unit.get("morale", MORALE_MAX)

        if morale >= 80:
            return 1.2  # High morale bonus
        elif morale >= 60:
            return 1.0  # Normal effectiveness
        elif morale >= 40:
            return 0.9  # Slightly reduced
        elif morale >= MORALE_BREAK_THRESHOLD:
            return 0.7  # Reduced effectiveness
        else:
            return 0.5  # Severely reduced (broken/routing)

    # ========================================================================
    # ARMY-LEVEL MORALE (For Morale-Driven Warfare)
    # ========================================================================

    def initialize_army_morale(self, army: Any) -> None:
        """
        Initialize army-level morale pool.

        Args:
            army: Army entity
        """
        army.morale = MORALE_MAX
        army.morale_state = "normal"  # normal, critical, routing
        army.is_routed = False
        army.momentum = 0  # Tracks battle momentum (-100 to +100)

    def get_army_morale(self, army: Any) -> int:
        """
        Get current army morale.

        Args:
            army: Army entity

        Returns:
            Current morale value
        """
        return getattr(army, "morale", MORALE_MAX)

    def modify_army_morale(
        self,
        army: Any,
        change: int,
        reason: str = "",
        apply_cascade: bool = True
    ) -> None:
        """
        Modify army morale with cascading effects.

        Args:
            army: Army entity
            change: Morale change (positive or negative)
            reason: Reason for change
            apply_cascade: Whether to apply cascading multipliers
        """
        old_morale = self.get_army_morale(army)

        # Apply cascading effect (morale losses increase when already low)
        if apply_cascade and change < 0 and old_morale < MORALE_CASCADE_THRESHOLD:
            change = int(change * MORALE_CASCADE_MULTIPLIER)

        # Apply global multiplier
        if change < 0:
            change = int(change * GLOBAL_MORALE_DAMAGE_MULTIPLIER)
        else:
            change = int(change * GLOBAL_MORALE_RECOVERY_MULTIPLIER)

        new_morale = max(MORALE_ZERO, min(MORALE_MAX, old_morale + change))
        army.morale = new_morale

        # Update morale state
        self._update_army_morale_state(army)

        # Broadcast event
        self.event_system.emit(EVENT_MORALE_CHANGED, {
            "entity": "army",
            "army_id": id(army),
            "old_morale": old_morale,
            "new_morale": new_morale,
            "change": change,
            "reason": reason,
            "cascaded": apply_cascade and old_morale < MORALE_CASCADE_THRESHOLD,
        })

        if DEBUG_MORALE_SYSTEM:
            print(f"Army morale: {old_morale} → {new_morale} ({change:+d}) [{reason}]")

    def _update_army_morale_state(self, army: Any) -> None:
        """
        Update army morale state based on current morale.

        Args:
            army: Army entity
        """
        morale = self.get_army_morale(army)

        old_state = getattr(army, "morale_state", "normal")

        if morale <= MORALE_ZERO:
            army.morale_state = "defeated"
            army.is_routed = True
        elif morale <= ROUT_CHECK_THRESHOLD:
            army.morale_state = "routing"
        elif morale <= MORALE_CRITICAL_THRESHOLD:
            army.morale_state = "critical"
        elif morale <= MORALE_BREAK_THRESHOLD:
            army.morale_state = "shaken"
        else:
            army.morale_state = "normal"
            army.is_routed = False

        # Trigger state change effects
        if old_state != army.morale_state:
            self._handle_army_morale_state_change(army, old_state, army.morale_state)

    def _handle_army_morale_state_change(
        self,
        army: Any,
        old_state: str,
        new_state: str
    ) -> None:
        """
        Handle army morale state transitions.

        Args:
            army: Army entity
            old_state: Previous morale state
            new_state: New morale state
        """
        if DEBUG_MORALE_SYSTEM:
            print(f"Army morale state: {old_state} → {new_state}")

        # Apply state-specific effects
        if new_state == "critical":
            # Units move slower, miss more, reduced effectiveness
            self._apply_critical_morale_penalties(army)
        elif new_state == "routing":
            # Units attempt to flee
            self._trigger_rout_checks(army)
        elif new_state == "defeated":
            # Army retreats from battlefield
            self._handle_army_defeat(army)

    def _apply_critical_morale_penalties(self, army: Any) -> None:
        """
        Apply penalties when army morale is critical.

        Args:
            army: Army entity
        """
        # Units suffer effectiveness penalty
        for unit in army.units:
            if hasattr(unit, "morale_component"):
                unit.morale_component.effectiveness_modifier = DEMORALIZED_EFFECTIVENESS_PENALTY

    def _trigger_rout_checks(self, army: Any) -> None:
        """
        Trigger rout checks for units when army morale is very low.

        Args:
            army: Army entity
        """
        import random
        for unit in army.units:
            if random.random() < ROUT_CHANCE_PERCENT:
                if hasattr(unit, "morale_component"):
                    unit.morale_component.is_routing = True

    def _handle_army_defeat(self, army: Any) -> None:
        """
        Handle army defeat (morale reached zero).

        Args:
            army: Army entity
        """
        army.is_defeated = True
        army.is_routed = True
        # Army will retreat in next update

    def apply_morale_damage_source(
        self,
        army: Any,
        source: str,
        multiplier: float = 1.0,
        **kwargs
    ) -> None:
        """
        Apply morale damage from a specific source.

        Args:
            army: Army entity
            source: Damage source type
            multiplier: Damage multiplier (for unit tier, etc.)
            **kwargs: Additional source-specific parameters
        """
        damage_map = {
            "unit_lost": -BASE_UNIT_MORALE_LOSS * multiplier,
            "skirmish_loss": -SKIRMISH_LOSS_MORALE_DAMAGE,
            "charge_hit": -CHARGE_MORALE_DAMAGE,
            "failed_defense": -FAILED_DEFENSE_MORALE_DAMAGE,
            "commander_defeated": -COMMANDER_DEFEAT_MORALE_DAMAGE,
            "flank_success": -FLANK_SUCCESS_MORALE_DAMAGE,
            "ambush": -AMBUSH_MORALE_DAMAGE,
            "surrounded": -SURROUNDED_MORALE_PENALTY,
            "counter_commit_loss": -COUNTERCOMMIT_LOSS_MORALE_PENALTY,
            "selective_loss": -SELECTIVE_LOSS_MORALE_HIT,
        }

        gain_map = {
            "skirmish_win": SKIRMISH_WIN_MORALE_BONUS,
            "counter_commit_win": COUNTERCOMMIT_WIN_MORALE_SWING,
            "selective_win": SELECTIVE_WIN_MORALE_GAIN,
            "commander_duel_win": COMMANDER_DUEL_WIN_MORALE_SWING,
        }

        if source in damage_map:
            self.modify_army_morale(army, damage_map[source], reason=source)
        elif source in gain_map:
            self.modify_army_morale(army, gain_map[source], reason=source)

    def get_army_effectiveness_modifier(self, army: Any) -> float:
        """
        Get army-wide effectiveness modifier based on morale.

        Uses MORALE_EFFECTIVENESS_CURVE for granular scaling.

        Args:
            army: Army entity

        Returns:
            Effectiveness multiplier (0.1 to 1.0)
        """
        morale = self.get_army_morale(army)

        # Find closest morale value in curve
        for threshold in sorted(MORALE_EFFECTIVENESS_CURVE.keys(), reverse=True):
            if morale >= threshold:
                return MORALE_EFFECTIVENESS_CURVE[threshold]

        return MORALE_EFFECTIVENESS_CURVE[0]  # Minimum effectiveness

    def apply_momentum_effects(
        self,
        winning_army: Any,
        losing_army: Any
    ) -> None:
        """
        Apply momentum morale effects per turn.

        Args:
            winning_army: Army with momentum advantage
            losing_army: Army losing momentum
        """
        # Winning side gains morale
        self.modify_army_morale(
            winning_army,
            MOMENTUM_MORALE_GAIN_PER_TURN,
            reason="momentum_gain",
            apply_cascade=False
        )

        # Losing side loses morale
        self.modify_army_morale(
            losing_army,
            -MOMENTUM_MORALE_LOSS_PER_TURN,
            reason="momentum_loss",
            apply_cascade=True  # Cascades when already low
        )

        # Update momentum tracking
        winning_army.momentum = min(100, winning_army.momentum + 10)
        losing_army.momentum = max(-100, losing_army.momentum - 10)

    def check_morale_gap_dominance(
        self,
        army1: Any,
        army2: Any
    ) -> Optional[Any]:
        """
        Check if morale gap creates dominance situation.

        Args:
            army1: First army
            army2: Second army

        Returns:
            Dominant army if gap exceeds threshold, None otherwise
        """
        morale1 = self.get_army_morale(army1)
        morale2 = self.get_army_morale(army2)

        gap = abs(morale1 - morale2)

        if gap >= MORALE_GAP_DOMINANCE_THRESHOLD:
            return army1 if morale1 > morale2 else army2

        return None

    def is_army_defeated(self, army: Any) -> bool:
        """
        Check if army is defeated (morale reached zero).

        Args:
            army: Army entity

        Returns:
            True if army morale is zero
        """
        return self.get_army_morale(army) <= MORALE_ZERO

    # ========================================================================
    # COMMANDER STATS EFFECTS
    # ========================================================================

    def get_leadership_mitigation(self, leadership_stat: int) -> float:
        """
        Get morale loss mitigation from Leadership stat.

        Leadership reduces morale damage taken.
        At 100 leadership: 25% reduction
        At 0 leadership: 0% reduction

        Args:
            leadership_stat: Leadership value (0-100)

        Returns:
            Reduction multiplier (0.0 to 0.25)
        """
        return (leadership_stat * COMMANDER_STAT_SCALING_FACTOR) * LEADERSHIP_MITIGATION_PERCENT

    def get_tactics_flank_bonus(self, tactics_stat: int) -> float:
        """
        Get flanking damage bonus from Tactics stat.

        Tactics increases damage when flanking enemies.
        At 100 tactics: +50% damage
        At 0 tactics: 0% bonus

        Args:
            tactics_stat: Tactics value (0-100)

        Returns:
            Damage bonus multiplier (0.0 to 0.5)
        """
        return (tactics_stat * COMMANDER_STAT_SCALING_FACTOR) * TACTICS_FLANK_MULTIPLIER

    def get_martial_prowess_bonus(self, martial_stat: int) -> float:
        """
        Get personal combat damage bonus from Martial Prowess stat.

        Martial Prowess increases personal damage output.
        At 100 martial: +100% damage
        At 0 martial: 0% bonus

        Args:
            martial_stat: Martial Prowess value (0-100)

        Returns:
            Damage bonus multiplier (0.0 to 1.0)
        """
        return (martial_stat * COMMANDER_STAT_SCALING_FACTOR) * MARTIAL_DAMAGE_MULTIPLIER

    def get_presence_buff(self, presence_stat: int) -> float:
        """
        Get unit effectiveness buff from Presence stat.

        Presence buffs nearby units' effectiveness.
        At 100 presence: +20% effectiveness
        At 0 presence: 0% bonus

        Args:
            presence_stat: Presence value (0-100)

        Returns:
            Effectiveness buff multiplier (0.0 to 0.2)
        """
        return (presence_stat * COMMANDER_STAT_SCALING_FACTOR) * PRESENCE_BUFF_PERCENT

    def apply_leadership_mitigation(
        self,
        army: Any,
        base_morale_loss: int,
        leadership_stat: int
    ) -> int:
        """
        Apply Leadership stat to reduce morale loss.

        Args:
            army: Army entity
            base_morale_loss: Base morale loss before mitigation
            leadership_stat: Commander's Leadership value

        Returns:
            Mitigated morale loss (negative value)
        """
        mitigation = self.get_leadership_mitigation(leadership_stat)
        reduced_loss = int(base_morale_loss * (1 - mitigation))
        return -reduced_loss
