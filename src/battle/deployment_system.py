"""
Deployment system for large-scale battles.
Auto-deploys 8-12 units in tactical formations based on unit types.
"""

from typing import List, Dict
from src.entities.unit import Unit
from src.battle.battlefield_grid import BattlefieldGrid, BattlePosition


class DeploymentSystem:
    """
    Manages tactical deployment of armies on the battlefield.

    Deployment logic:
    - Heavy infantry: Front center
    - Spearmen: Front flanks (anti-cavalry)
    - Light infantry: Second line
    - Cavalry: Wide flanks (for flanking maneuvers)
    - Archers: Rear center
    - Skirmishers: Front skirmish line
    """

    def __init__(self, battlefield: BattlefieldGrid):
        """
        Initialize deployment system.

        Args:
            battlefield: Battlefield grid
        """
        self.battlefield = battlefield

        # Formation spacing
        self.unit_spacing_x = 80  # Horizontal space between formations
        self.unit_spacing_y = 90  # Vertical space between formations

    def deploy_army(self, units: List[Unit], side: str) -> Dict[int, BattlePosition]:
        """
        Deploy an army in tactical formation.

        Args:
            units: List of units to deploy (up to 12)
            side: "player" or "enemy"

        Returns:
            Dict mapping unit id to BattlePosition
        """
        # Limit to 12 units
        units = units[:12]

        # Categorize units by type
        categorized = self._categorize_units(units)

        # Generate positions based on side
        if side == "player":
            return self._deploy_player_side(categorized)
        else:
            return self._deploy_enemy_side(categorized)

    def _categorize_units(self, units: List[Unit]) -> Dict[str, List[Unit]]:
        """
        Categorize units by tactical role.

        Args:
            units: List of units

        Returns:
            Dict of category -> list of units
        """
        categories = {
            "heavy_infantry": [],
            "light_infantry": [],
            "spearmen": [],
            "cavalry": [],
            "archers": [],
            "skirmishers": [],
            "special": []
        }

        for unit in units:
            unit_type = unit.unit_component.unit_type.lower()

            if "infantry" in unit_type and "light" not in unit_type:
                categories["heavy_infantry"].append(unit)
            elif "light" in unit_type or "peltast" in unit_type:
                categories["light_infantry"].append(unit)
            elif "spear" in unit_type or "hoplite" in unit_type or "phalanx" in unit_type:
                categories["spearmen"].append(unit)
            elif "cavalry" in unit_type or "horse" in unit_type:
                categories["cavalry"].append(unit)
            elif "archer" in unit_type or "bowman" in unit_type:
                categories["archers"].append(unit)
            elif "skirmisher" in unit_type or "jav" in unit_type:
                categories["skirmishers"].append(unit)
            else:
                categories["special"].append(unit)

        return categories

    def _deploy_player_side(self, categorized: Dict[str, List[Unit]]) -> Dict[int, BattlePosition]:
        """
        Deploy player army on left side of battlefield.

        Formation layout (viewed from above):
                    ARCHERS
                      ▼▼▼

        CAVALRY   SPEAR INFANTRY SPEAR   CAVALRY
          ◉       ████  ██████  ████      ◉

                  SKIRMISHERS
                     ...
        """
        positions = {}

        # Base positions
        front_line_x = 150  # Front line position
        second_line_x = 80  # Second line
        rear_line_x = 30    # Rear line (archers)

        center_y = self.battlefield.HEIGHT // 2  # Vertical center

        # Track vertical positions
        front_positions = []
        second_positions = []
        rear_positions = []
        flank_positions = []

        # 1. Deploy heavy infantry in front center
        for i, unit in enumerate(categorized["heavy_infantry"]):
            y = center_y + (i - len(categorized["heavy_infantry"]) // 2) * self.unit_spacing_y
            front_positions.append((unit, BattlePosition(front_line_x, y, 0.0)))

        # 2. Deploy spearmen on front flanks
        spearmen = categorized["spearmen"]
        if len(spearmen) > 0:
            # Top flank
            y_top = center_y - 120
            front_positions.append((spearmen[0], BattlePosition(front_line_x, y_top, 0.0)))

        if len(spearmen) > 1:
            # Bottom flank
            y_bottom = center_y + 120
            front_positions.append((spearmen[1], BattlePosition(front_line_x, y_bottom, 0.0)))

        # Additional spearmen in second line
        for i, unit in enumerate(spearmen[2:]):
            y = center_y + (i - len(spearmen[2:]) // 2) * self.unit_spacing_y
            second_positions.append((unit, BattlePosition(second_line_x, y, 0.0)))

        # 3. Deploy light infantry in second line
        for i, unit in enumerate(categorized["light_infantry"]):
            y = center_y + (i - len(categorized["light_infantry"]) // 2) * self.unit_spacing_y
            second_positions.append((unit, BattlePosition(second_line_x, y, 0.0)))

        # 4. Deploy archers in rear
        for i, unit in enumerate(categorized["archers"]):
            y = center_y + (i - len(categorized["archers"]) // 2) * self.unit_spacing_y
            rear_positions.append((unit, BattlePosition(rear_line_x, y, 0.0)))

        # 5. Deploy cavalry on wide flanks
        cavalry = categorized["cavalry"]
        if len(cavalry) > 0:
            # Top flank (wide)
            y_top = center_y - 180
            flank_positions.append((cavalry[0], BattlePosition(second_line_x, y_top, 0.0)))

        if len(cavalry) > 1:
            # Bottom flank (wide)
            y_bottom = center_y + 180
            flank_positions.append((cavalry[1], BattlePosition(second_line_x, y_bottom, 0.0)))

        # Additional cavalry
        for i, unit in enumerate(cavalry[2:]):
            y = center_y - 180 + i * self.unit_spacing_y
            flank_positions.append((unit, BattlePosition(second_line_x, y, 0.0)))

        # 6. Deploy skirmishers in front skirmish line
        for i, unit in enumerate(categorized["skirmishers"]):
            y = center_y + (i - len(categorized["skirmishers"]) // 2) * self.unit_spacing_y
            front_positions.append((unit, BattlePosition(front_line_x + 50, y, 0.0)))

        # 7. Deploy special units in second line
        for i, unit in enumerate(categorized["special"]):
            y = center_y + (i - len(categorized["special"]) // 2) * self.unit_spacing_y
            second_positions.append((unit, BattlePosition(second_line_x, y, 0.0)))

        # Collect all positions
        all_positions = front_positions + second_positions + rear_positions + flank_positions

        # Build position dict
        for unit, position in all_positions:
            positions[unit.id] = position
            # Update unit's position component
            unit.position_component.row = int(position.y // 100)  # Approximate
            unit.position_component.col = int(position.x // 100)
            unit.position_component.side = "player"

        return positions

    def _deploy_enemy_side(self, categorized: Dict[str, List[Unit]]) -> Dict[int, BattlePosition]:
        """
        Deploy enemy army on right side of battlefield.

        Formation is mirrored from player side.
        """
        positions = {}

        # Base positions (mirrored)
        front_line_x = 850  # Enemy front line
        second_line_x = 920  # Enemy second line
        rear_line_x = 970   # Enemy rear line

        center_y = self.battlefield.HEIGHT // 2

        # Track vertical positions
        front_positions = []
        second_positions = []
        rear_positions = []
        flank_positions = []

        # 1. Deploy heavy infantry in front center
        for i, unit in enumerate(categorized["heavy_infantry"]):
            y = center_y + (i - len(categorized["heavy_infantry"]) // 2) * self.unit_spacing_y
            front_positions.append((unit, BattlePosition(front_line_x, y, 180.0)))  # Face left

        # 2. Deploy spearmen on front flanks
        spearmen = categorized["spearmen"]
        if len(spearmen) > 0:
            y_top = center_y - 120
            front_positions.append((spearmen[0], BattlePosition(front_line_x, y_top, 180.0)))

        if len(spearmen) > 1:
            y_bottom = center_y + 120
            front_positions.append((spearmen[1], BattlePosition(front_line_x, y_bottom, 180.0)))

        # Additional spearmen
        for i, unit in enumerate(spearmen[2:]):
            y = center_y + (i - len(spearmen[2:]) // 2) * self.unit_spacing_y
            second_positions.append((unit, BattlePosition(second_line_x, y, 180.0)))

        # 3. Deploy light infantry in second line
        for i, unit in enumerate(categorized["light_infantry"]):
            y = center_y + (i - len(categorized["light_infantry"]) // 2) * self.unit_spacing_y
            second_positions.append((unit, BattlePosition(second_line_x, y, 180.0)))

        # 4. Deploy archers in rear
        for i, unit in enumerate(categorized["archers"]):
            y = center_y + (i - len(categorized["archers"]) // 2) * self.unit_spacing_y
            rear_positions.append((unit, BattlePosition(rear_line_x, y, 180.0)))

        # 5. Deploy cavalry on wide flanks
        cavalry = categorized["cavalry"]
        if len(cavalry) > 0:
            y_top = center_y - 180
            flank_positions.append((cavalry[0], BattlePosition(second_line_x, y_top, 180.0)))

        if len(cavalry) > 1:
            y_bottom = center_y + 180
            flank_positions.append((cavalry[1], BattlePosition(second_line_x, y_bottom, 180.0)))

        for i, unit in enumerate(cavalry[2:]):
            y = center_y - 180 + i * self.unit_spacing_y
            flank_positions.append((unit, BattlePosition(second_line_x, y, 180.0)))

        # 6. Deploy skirmishers
        for i, unit in enumerate(categorized["skirmishers"]):
            y = center_y + (i - len(categorized["skirmishers"]) // 2) * self.unit_spacing_y
            front_positions.append((unit, BattlePosition(front_line_x - 50, y, 180.0)))

        # 7. Deploy special units
        for i, unit in enumerate(categorized["special"]):
            y = center_y + (i - len(categorized["special"]) // 2) * self.unit_spacing_y
            second_positions.append((unit, BattlePosition(second_line_x, y, 180.0)))

        # Collect all positions
        all_positions = front_positions + second_positions + rear_positions + flank_positions

        # Build position dict
        for unit, position in all_positions:
            positions[unit.id] = position
            # Update unit's position component
            unit.position_component.row = int(position.y // 100)
            unit.position_component.col = int(position.x // 100)
            unit.position_component.side = "enemy"

        return positions
