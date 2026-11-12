"""
Save/load system for game state serialization.
"""

import json
import os
from typing import Any, Dict
from pathlib import Path


class SaveSystem:
    """
    Handles saving and loading game state.
    """

    def __init__(self, save_directory: str = "saves"):
        """
        Initialize save system.

        Args:
            save_directory: Directory to store save files
        """
        self.save_directory = save_directory
        self._ensure_save_directory()

    def _ensure_save_directory(self) -> None:
        """Create save directory if it doesn't exist."""
        Path(self.save_directory).mkdir(parents=True, exist_ok=True)

    def save_game(self, save_name: str, game_data: Dict[str, Any]) -> bool:
        """
        Save game state to file.

        Args:
            save_name: Name of the save file
            game_data: Dictionary containing all game state

        Returns:
            True if save successful
        """
        try:
            file_path = os.path.join(self.save_directory, f"{save_name}.json")

            with open(file_path, 'w') as f:
                json.dump(game_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, save_name: str) -> Dict[str, Any]:
        """
        Load game state from file.

        Args:
            save_name: Name of the save file

        Returns:
            Dictionary containing game state, or None if load failed
        """
        try:
            file_path = os.path.join(self.save_directory, f"{save_name}.json")

            if not os.path.exists(file_path):
                print(f"Save file not found: {file_path}")
                return None

            with open(file_path, 'r') as f:
                game_data = json.load(f)

            return game_data

        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def list_saves(self) -> list:
        """
        List all available save files.

        Returns:
            List of save file names (without extension)
        """
        try:
            saves = []
            for file in os.listdir(self.save_directory):
                if file.endswith('.json'):
                    saves.append(file[:-5])  # Remove .json extension
            return saves

        except Exception as e:
            print(f"Error listing saves: {e}")
            return []

    def delete_save(self, save_name: str) -> bool:
        """
        Delete a save file.

        Args:
            save_name: Name of the save to delete

        Returns:
            True if deletion successful
        """
        try:
            file_path = os.path.join(self.save_directory, f"{save_name}.json")

            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                print(f"Save file not found: {file_path}")
                return False

        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
