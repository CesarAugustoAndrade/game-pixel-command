"""
Data Loader - Loads game data from JSON files.
"""

import json
import os
from typing import Dict, List, Any, Optional
from src.core.constants import PATH_DATA


class DataLoader:
    """
    Handles loading game data from JSON files.
    """

    def __init__(self):
        """Initialize data loader."""
        self._units = None
        self._factions = None

    def load_units(self) -> Dict[str, Any]:
        """
        Load unit definitions from JSON.

        Returns:
            Dictionary of unit definitions
        """
        if self._units is None:
            units_path = os.path.join(PATH_DATA, "units.json")
            try:
                with open(units_path, 'r') as f:
                    self._units = json.load(f)
                print(f"Loaded {len(self._units)} unit definitions")
            except Exception as e:
                print(f"Error loading units.json: {e}")
                self._units = {}

        return self._units

    def load_factions(self) -> Dict[str, Any]:
        """
        Load faction data from JSON.

        Returns:
            Dictionary of faction data
        """
        if self._factions is None:
            factions_path = os.path.join(PATH_DATA, "factions.json")
            try:
                with open(factions_path, 'r') as f:
                    self._factions = json.load(f)
                print(f"Loaded {len(self._factions)} factions")
            except Exception as e:
                print(f"Error loading factions.json: {e}")
                self._factions = {}

        return self._factions

    def get_unit_definition(self, unit_id: str) -> Dict[str, Any]:
        """
        Get unit definition by ID.

        Args:
            unit_id: Unit type ID

        Returns:
            Unit definition dict
        """
        units = self.load_units()
        return units.get(unit_id, {})

    def get_faction_data(self, faction: str) -> Dict[str, Any]:
        """
        Get faction data by name.

        Args:
            faction: Faction name

        Returns:
            Faction data dict
        """
        factions = self.load_factions()
        return factions.get(faction, {})

    def get_units_by_faction(self, faction: str) -> List[str]:
        """
        Get available unit types for a faction.

        Args:
            faction: Faction name

        Returns:
            List of unit IDs
        """
        faction_data = self.get_faction_data(faction)
        return faction_data.get("available_units", [])

    def get_faction_bonus(self, faction: str, bonus_type: str) -> float:
        """
        Get a specific bonus for a faction.

        Args:
            faction: Faction name
            bonus_type: Type of bonus

        Returns:
            Bonus multiplier (1.0 = no bonus)
        """
        faction_data = self.get_faction_data(faction)
        bonuses = faction_data.get("bonuses", {})
        return bonuses.get(bonus_type, 1.0)

    def get_all_unit_ids(self) -> List[str]:
        """
        Get list of all unit IDs.

        Returns:
            List of unit IDs
        """
        units = self.load_units()
        return list(units.keys())

    def get_all_faction_ids(self) -> List[str]:
        """
        Get list of all faction IDs.

        Returns:
            List of faction IDs
        """
        factions = self.load_factions()
        return list(factions.keys())

    def reload_all(self) -> None:
        """Reload all data from files (useful for modding)."""
        self._units = None
        self._factions = None
        self.load_units()
        self.load_factions()
        print("Game data reloaded")


# Global data loader instance
_data_loader_instance: Optional[DataLoader] = None


def get_data_loader() -> DataLoader:
    """
    Get the global data loader instance (singleton pattern).

    Returns:
        DataLoader instance
    """
    global _data_loader_instance
    if _data_loader_instance is None:
        _data_loader_instance = DataLoader()
    return _data_loader_instance


# Convenience functions that match the old Python API
def get_unit_definition(unit_id: str) -> Dict[str, Any]:
    """Get unit definition by ID."""
    return get_data_loader().get_unit_definition(unit_id)


def get_faction_data(faction: str) -> Dict[str, Any]:
    """Get faction data by name."""
    return get_data_loader().get_faction_data(faction)


def get_units_by_faction(faction: str) -> List[str]:
    """Get available unit types for a faction."""
    return get_data_loader().get_units_by_faction(faction)


def get_faction_bonus(faction: str, bonus_type: str) -> float:
    """Get a specific bonus for a faction."""
    return get_data_loader().get_faction_bonus(faction, bonus_type)
