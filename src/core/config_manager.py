"""
Configuration Manager - handles loading and saving game configuration.
"""

import json
import os
from typing import Any, Dict


class ConfigManager:
    """
    Manages game configuration from config.json file.
    Provides methods to get/set config values and persist changes.
    """

    # Default configuration values
    DEFAULT_CONFIG = {
        "display": {
            "width": 1280,
            "height": 720,
            "fullscreen": False,
            "vsync": True,
            "fps": 60
        },
        "audio": {
            "master_volume": 0.8,
            "music_volume": 0.6,
            "sfx_volume": 0.7,
            "enabled": True
        },
        "gameplay": {
            "difficulty": "normal",
            "tutorial_enabled": True,
            "autosave": True,
            "autosave_interval": 300
        },
        "battle": {
            "grid_width": 20,
            "grid_height": 15,
            "hex_size": 32,
            "animation_speed": 1.0,
            "show_movement_range": True,
            "show_attack_range": True
        },
        "controls": {
            "mouse_edge_scroll": True,
            "keyboard_scroll_speed": 10,
            "camera_drag_button": 2
        },
        "debug": {
            "enabled": False,
            "show_fps": True,
            "show_grid": True,
            "show_pathfinding": False,
            "god_mode": False
        }
    }

    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to config.json file
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from JSON file or use defaults."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)

                # Merge with defaults to ensure all keys exist
                self.config = self._merge_with_defaults(loaded_config)
                print(f"Configuration loaded from {self.config_path}")
            else:
                print(f"Config file not found, using defaults")
                self.config = self.DEFAULT_CONFIG.copy()
                self.save_config()  # Create default config file
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            self.config = self.DEFAULT_CONFIG.copy()

    def save_config(self) -> bool:
        """
        Save current configuration to JSON file.

        Returns:
            True if save was successful, False otherwise
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            section: Configuration section (e.g., 'display', 'audio')
            key: Configuration key within section
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default

    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            section: Configuration section
            key: Configuration key within section
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.

        Args:
            section: Section name

        Returns:
            Dictionary of section values or empty dict
        """
        return self.config.get(section, {}).copy()

    def set_section(self, section: str, values: Dict[str, Any]) -> None:
        """
        Set entire configuration section.

        Args:
            section: Section name
            values: Dictionary of values to set
        """
        self.config[section] = values.copy()

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = self.DEFAULT_CONFIG.copy()
        print("Configuration reset to defaults")

    def reset_section(self, section: str) -> None:
        """
        Reset a specific section to default values.

        Args:
            section: Section name to reset
        """
        if section in self.DEFAULT_CONFIG:
            self.config[section] = self.DEFAULT_CONFIG[section].copy()
            print(f"Section '{section}' reset to defaults")

    def _merge_with_defaults(self, loaded_config: Dict) -> Dict:
        """
        Merge loaded config with defaults to ensure all keys exist.

        Args:
            loaded_config: Configuration loaded from file

        Returns:
            Merged configuration dictionary
        """
        merged = self.DEFAULT_CONFIG.copy()

        for section, values in loaded_config.items():
            if section in merged and isinstance(values, dict):
                merged[section].update(values)
            else:
                merged[section] = values

        return merged

    def validate_display_resolution(self, width: int, height: int) -> bool:
        """
        Validate display resolution.

        Args:
            width: Screen width
            height: Screen height

        Returns:
            True if resolution is valid
        """
        return width >= 800 and height >= 600 and width <= 7680 and height <= 4320

    def validate_volume(self, volume: float) -> bool:
        """
        Validate audio volume value.

        Args:
            volume: Volume value to validate

        Returns:
            True if volume is valid (0.0 to 1.0)
        """
        return 0.0 <= volume <= 1.0

    def validate_difficulty(self, difficulty: str) -> bool:
        """
        Validate difficulty setting.

        Args:
            difficulty: Difficulty string

        Returns:
            True if difficulty is valid
        """
        return difficulty in ["easy", "normal", "hard", "veteran"]

    def __str__(self) -> str:
        """String representation of config."""
        return json.dumps(self.config, indent=2)
