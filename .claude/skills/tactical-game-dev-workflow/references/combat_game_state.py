"""
Tactical Combat Game State System
A pixel-art real-time tactical battle system with morale-based victory conditions

REFERENCE IMPLEMENTATION for tactical-game-dev-workflow skill
This file demonstrates complete game state management for a tactical combat system.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import random


class UnitType(Enum):
    """Types of military units available"""
    INFANTRY = "infantry"
    CAVALRY = "cavalry"
    SKIRMISHER = "skirmisher"  # Ranged units (archers, javelin throwers)
    SIEGE = "siege"  # Catapults, ballistae


class UnitStance(Enum):
    """Combat stances for units"""
    ATTACKING = "attacking"
    HOLDING = "holding"
    ROUTING = "routing"  # Unit has broken and is fleeing
    DESTROYED = "destroyed"


class ProjectileType(Enum):
    """Types of ranged projectiles"""
    ARROW = "arrow"
    JAVELIN = "javelin"
    STONE = "stone"  # From catapults
    BOLT = "bolt"  # From crossbows/ballistae


class ArmySide(Enum):
    """Which side of the battlefield"""
    ATTACKER = "attacker"  # Left side (blue)
    DEFENDER = "defender"  # Right side (red)


class BattlePhase(Enum):
    """Current phase of the battle"""
    DEPLOYMENT = "deployment"
    SKIRMISH = "skirmish"  # Automatic ranged combat
    ENGAGEMENT = "engagement"  # Main battle
    MORALE_BREAK = "morale_break"  # One side's morale has broken
    VICTORY = "victory"


@dataclass
class GridPosition:
    """Position on the tactical grid"""
    x: int
    y: int

    def distance_to(self, other: 'GridPosition') -> float:
        """Calculate grid distance to another position"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Projectile:
    """A projectile in flight"""
    projectile_type: ProjectileType
    start_pos: GridPosition
    target_pos: GridPosition
    current_progress: float = 0.0  # 0.0 to 1.0
    damage: int = 5
    source_unit_id: Optional[str] = None

    def update(self, delta_time: float) -> bool:
        """Update projectile position. Returns True if reached target."""
        self.current_progress += delta_time * 2.0  # Speed factor
        return self.current_progress >= 1.0


@dataclass
class ParticleEffect:
    """Visual effect particle"""
    effect_type: str  # "dust", "sparks", "blood", "impact"
    position: GridPosition
    lifetime: float = 1.0
    elapsed: float = 0.0

    def is_alive(self) -> bool:
        return self.elapsed < self.lifetime

    def update(self, delta_time: float):
        self.elapsed += delta_time


@dataclass
class Unit:
    """A military unit on the battlefield"""
    unit_id: str
    unit_type: UnitType
    side: ArmySide
    position: GridPosition

    # Combat stats
    health: int = 100
    max_health: int = 100
    attack_power: int = 10
    defense: int = 5
    range: int = 1  # Grid cells, skirmishers have higher range

    # Morale and state
    morale: int = 100
    max_morale: int = 100
    stance: UnitStance = UnitStance.HOLDING

    # Unit composition
    soldier_count: int = 20
    max_soldiers: int = 20

    # Combat timers
    attack_cooldown: float = 0.0
    attack_speed: float = 2.0  # Seconds between attacks

    # Target
    target_unit_id: Optional[str] = None

    def take_damage(self, damage: int) -> bool:
        """Apply damage to unit. Returns True if unit is destroyed."""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage

        # Calculate soldier losses
        health_percentage = self.health / self.max_health
        self.soldier_count = max(0, int(self.max_soldiers * health_percentage))

        # Morale loss from damage
        self.morale -= actual_damage // 2

        if self.health <= 0:
            self.stance = UnitStance.DESTROYED
            self.soldier_count = 0
            return True

        # Check for morale break
        if self.morale <= 20:
            self.stance = UnitStance.ROUTING

        return False

    def can_attack(self) -> bool:
        """Check if unit can perform an attack"""
        return (self.stance in [UnitStance.ATTACKING, UnitStance.HOLDING] and
                self.attack_cooldown <= 0 and
                self.health > 0)

    def reset_attack_cooldown(self):
        """Reset the attack timer"""
        self.attack_cooldown = self.attack_speed

    def update(self, delta_time: float):
        """Update unit state"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time


@dataclass
class Commander:
    """Army commander with special abilities"""
    name: str
    side: ArmySide
    health: int = 100
    max_health: int = 100
    leadership_bonus: int = 10  # Morale bonus to nearby units
    portrait_index: int = 0

    def is_alive(self) -> bool:
        return self.health > 0


@dataclass
class Army:
    """An army consisting of multiple units"""
    side: ArmySide
    commander: Commander
    units: List[Unit] = field(default_factory=list)

    # Army-wide stats
    total_morale: int = 100
    max_morale: int = 100

    def calculate_morale(self) -> int:
        """Calculate current army morale based on units"""
        if not self.units:
            return 0

        alive_units = [u for u in self.units if u.stance != UnitStance.DESTROYED]
        if not alive_units:
            return 0

        # Average morale of alive units
        avg_morale = sum(u.morale for u in alive_units) / len(alive_units)

        # Commander bonus
        if self.commander.is_alive():
            avg_morale += self.commander.leadership_bonus

        self.total_morale = int(min(self.max_morale, avg_morale))
        return self.total_morale

    def is_broken(self) -> bool:
        """Check if army morale is broken"""
        return self.total_morale <= 30

    def get_unit_by_id(self, unit_id: str) -> Optional[Unit]:
        """Find unit by ID"""
        for unit in self.units:
            if unit.unit_id == unit_id:
                return unit
        return None

    def get_alive_units(self) -> List[Unit]:
        """Get all units that are still fighting"""
        return [u for u in self.units if u.stance not in [UnitStance.DESTROYED, UnitStance.ROUTING]]


@dataclass
class BattleMap:
    """The battlefield grid"""
    width: int = 24  # Grid cells
    height: int = 14

    # Terrain features
    castle_position: Optional[GridPosition] = None
    trees: List[GridPosition] = field(default_factory=list)

    def is_valid_position(self, pos: GridPosition) -> bool:
        """Check if position is within map bounds"""
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def get_deployment_zone(self, side: ArmySide) -> List[GridPosition]:
        """Get valid deployment positions for a side"""
        positions = []
        if side == ArmySide.ATTACKER:
            # Left side of map
            for y in range(self.height):
                for x in range(4):
                    positions.append(GridPosition(x, y))
        else:
            # Right side of map
            for y in range(self.height):
                for x in range(self.width - 4, self.width):
                    positions.append(GridPosition(x, y))
        return positions


@dataclass
class CombatLog:
    """Log of combat events"""
    message: str
    timestamp: float
    event_type: str  # "attack", "damage", "morale", "victory"


class BattleState:
    """Main game state for the tactical combat"""

    def __init__(self):
        self.phase = BattlePhase.DEPLOYMENT
        self.battle_time = 0.0

        # Map and armies
        self.battle_map = BattleMap()
        self.attacker = None
        self.defender = None

        # Active projectiles and effects
        self.projectiles: List[Projectile] = []
        self.particle_effects: List[ParticleEffect] = []

        # Combat log
        self.combat_log: List[CombatLog] = []

        # UI state
        self.selected_unit_id: Optional[str] = None
        self.camera_position = GridPosition(12, 7)  # Center of map

    def initialize_battle(self):
        """Set up the initial battle state"""
        # Create commanders
        attacker_commander = Commander(
            name="General Maximus",
            side=ArmySide.ATTACKER,
            portrait_index=0
        )

        defender_commander = Commander(
            name="Tribune Aurelius",
            side=ArmySide.DEFENDER,
            portrait_index=1
        )

        # Create armies
        self.attacker = Army(ArmySide.ATTACKER, attacker_commander)
        self.defender = Army(ArmySide.DEFENDER, defender_commander)

        # Deploy units
        self._deploy_sample_armies()

        self.log_event("Battle begins!", "start")
        self.phase = BattlePhase.SKIRMISH

    def _deploy_sample_armies(self):
        """Deploy sample armies for demonstration"""
        # Attacker infantry
        for i in range(10):
            unit = Unit(
                unit_id=f"attacker_inf_{i}",
                unit_type=UnitType.INFANTRY,
                side=ArmySide.ATTACKER,
                position=GridPosition(2, 2 + i),
                stance=UnitStance.ATTACKING
            )
            self.attacker.units.append(unit)

        # Defender infantry
        for i in range(10):
            unit = Unit(
                unit_id=f"defender_inf_{i}",
                unit_type=UnitType.INFANTRY,
                side=ArmySide.DEFENDER,
                position=GridPosition(21, 2 + i),
                stance=UnitStance.ATTACKING
            )
            self.defender.units.append(unit)

    def update(self, delta_time: float):
        """Main update loop for the battle"""
        self.battle_time += delta_time

        # Update all units
        for army in [self.attacker, self.defender]:
            if army:
                for unit in army.units:
                    unit.update(delta_time)

        # Update projectiles
        self._update_projectiles(delta_time)

        # Update particle effects
        self.particle_effects = [p for p in self.particle_effects if p.is_alive()]
        for particle in self.particle_effects:
            particle.update(delta_time)

        # Phase-specific logic
        if self.phase == BattlePhase.SKIRMISH:
            self._process_skirmish_phase()
        elif self.phase == BattlePhase.ENGAGEMENT:
            self._process_engagement_phase()

        # Check victory conditions
        self._check_victory_conditions()

    def _update_projectiles(self, delta_time: float):
        """Update all projectiles in flight"""
        completed = []
        for projectile in self.projectiles:
            if projectile.update(delta_time):
                completed.append(projectile)
                self._handle_projectile_impact(projectile)

        for proj in completed:
            self.projectiles.remove(proj)

    def _handle_projectile_impact(self, projectile: Projectile):
        """Handle a projectile hitting its target"""
        for army in [self.attacker, self.defender]:
            if not army:
                continue
            for unit in army.units:
                if (unit.position.x == projectile.target_pos.x and
                    unit.position.y == projectile.target_pos.y and
                    unit.stance != UnitStance.DESTROYED):

                    was_destroyed = unit.take_damage(projectile.damage)
                    self.particle_effects.append(
                        ParticleEffect("impact", projectile.target_pos, lifetime=0.5)
                    )

                    if was_destroyed:
                        self.log_event(f"{unit.unit_id} destroyed!", "damage")
                    break

    def _process_skirmish_phase(self):
        """Process automatic ranged combat"""
        # Process attacks from both sides
        for army, enemy_army in [(self.attacker, self.defender), (self.defender, self.attacker)]:
            if not army or not enemy_army:
                continue

            for unit in army.units:
                if unit.stance == UnitStance.ATTACKING and unit.can_attack():
                    target = self._find_nearest_enemy(unit, enemy_army)
                    if target and unit.position.distance_to(target.position) <= unit.range:
                        self._execute_attack(unit, target)

        # Transition after 10 seconds
        if self.battle_time > 10.0:
            self.phase = BattlePhase.ENGAGEMENT
            self.log_event("Armies engage!", "phase")

    def _process_engagement_phase(self):
        """Process main battle engagement"""
        self._process_skirmish_phase()  # Continue combat

    def _find_nearest_enemy(self, unit: Unit, enemy_army: Army) -> Optional[Unit]:
        """Find the nearest enemy unit"""
        alive_enemies = enemy_army.get_alive_units()
        if not alive_enemies:
            return None

        nearest = None
        min_distance = float('inf')

        for enemy in alive_enemies:
            distance = unit.position.distance_to(enemy.position)
            if distance < min_distance:
                min_distance = distance
                nearest = enemy

        return nearest

    def _execute_attack(self, attacker: Unit, target: Unit):
        """Execute an attack from one unit to another"""
        if attacker.range > 1:
            # Ranged attack
            projectile = Projectile(
                projectile_type=ProjectileType.ARROW,
                start_pos=attacker.position,
                target_pos=target.position,
                damage=attacker.attack_power,
                source_unit_id=attacker.unit_id
            )
            self.projectiles.append(projectile)
        else:
            # Melee attack
            was_destroyed = target.take_damage(attacker.attack_power)
            self.particle_effects.append(
                ParticleEffect("sparks", target.position, lifetime=0.4)
            )

        attacker.reset_attack_cooldown()

    def _check_victory_conditions(self):
        """Check if battle should end"""
        if self.phase == BattlePhase.VICTORY:
            return

        # Update morale
        if self.attacker:
            self.attacker.calculate_morale()
        if self.defender:
            self.defender.calculate_morale()

        # Check for victory
        attacker_alive = len(self.attacker.get_alive_units()) if self.attacker else 0
        defender_alive = len(self.defender.get_alive_units()) if self.defender else 0

        if attacker_alive == 0 or (self.attacker and self.attacker.is_broken()):
            self.phase = BattlePhase.VICTORY
            self.log_event("Defender wins!", "victory")

        if defender_alive == 0 or (self.defender and self.defender.is_broken()):
            self.phase = BattlePhase.VICTORY
            self.log_event("Attacker wins!", "victory")

    def log_event(self, message: str, event_type: str):
        """Add an event to the combat log"""
        self.combat_log.append(
            CombatLog(
                message=message,
                timestamp=self.battle_time,
                event_type=event_type
            )
        )
        if len(self.combat_log) > 50:
            self.combat_log.pop(0)

    def get_state_summary(self) -> dict:
        """Get a summary of the current battle state"""
        return {
            "phase": self.phase.value,
            "battle_time": self.battle_time,
            "attacker_morale": self.attacker.total_morale if self.attacker else 0,
            "defender_morale": self.defender.total_morale if self.defender else 0,
            "attacker_units_alive": len(self.attacker.get_alive_units()) if self.attacker else 0,
            "defender_units_alive": len(self.defender.get_alive_units()) if self.defender else 0,
            "active_projectiles": len(self.projectiles),
            "recent_events": [log.message for log in self.combat_log[-5:]]
        }


def create_sample_battle() -> BattleState:
    """Create a sample battle for demonstration"""
    battle = BattleState()
    battle.initialize_battle()
    return battle


if __name__ == "__main__":
    # Example usage
    battle = create_sample_battle()

    print("=== TACTICAL COMBAT INITIALIZED ===")
    print(f"Phase: {battle.phase.value}")
    print(f"Map Size: {battle.battle_map.width}x{battle.battle_map.height}")
    print(f"\nAttacker: {battle.attacker.commander.name}")
    print(f"  Units: {len(battle.attacker.units)}")
    print(f"  Morale: {battle.attacker.calculate_morale()}/100")
    print(f"\nDefender: {battle.defender.commander.name}")
    print(f"  Units: {len(battle.defender.units)}")
    print(f"  Morale: {battle.defender.calculate_morale()}/100")

    # Simulate battle
    print("\n--- Simulating 5 seconds of combat ---")
    for i in range(50):
        battle.update(0.1)

    summary = battle.get_state_summary()
    print(f"\nPhase: {summary['phase']}")
    print(f"Battle Time: {summary['battle_time']:.1f}s")
    print(f"Attacker Morale: {summary['attacker_morale']}/100")
    print(f"Defender Morale: {summary['defender_morale']}/100")
    print(f"Active Projectiles: {summary['active_projectiles']}")
    print("\nRecent Events:")
    for event in summary['recent_events']:
        print(f"  - {event}")