"""
Asset Loader - Preloads game assets at startup.
"""

from typing import List, Tuple, Optional
from src.core.engine import ResourceManager


class AssetLoader:
    """
    Handles preloading of game assets for better performance.
    """

    # Common UI sprites to preload
    UI_SPRITES = [
        ("ui", "menu -image.png"),
    ]

    # Common fonts to preload (size)
    COMMON_FONTS = [16, 24, 32, 40, 48, 72]

    def __init__(self, resource_manager: ResourceManager):
        """
        Initialize asset loader.

        Args:
            resource_manager: ResourceManager instance to use
        """
        self.resource_manager = resource_manager
        self.total_assets = 0
        self.loaded_assets = 0

    def preload_all(self, callback: Optional[callable] = None) -> None:
        """
        Preload all common assets.

        Args:
            callback: Optional callback function(progress) called during loading
        """
        # Calculate total assets to load
        self.total_assets = (
            len(self.UI_SPRITES) +
            len(self.COMMON_FONTS)
        )
        self.loaded_assets = 0

        # Preload UI sprites
        self._preload_ui_sprites(callback)

        # Preload common fonts
        self._preload_fonts(callback)

        print(f"Asset preloading complete: {self.loaded_assets}/{self.total_assets} assets loaded")

    def _preload_ui_sprites(self, callback: Optional[callable] = None) -> None:
        """Preload UI sprites."""
        for category, filename in self.UI_SPRITES:
            try:
                path = self.resource_manager.get_sprite_path(category, filename)
                self.resource_manager.load_sprite(path)
                self.loaded_assets += 1

                if callback:
                    callback(self.loaded_assets / self.total_assets)
            except Exception as e:
                print(f"Failed to preload sprite {category}/{filename}: {e}")

    def _preload_fonts(self, callback: Optional[callable] = None) -> None:
        """Preload common font sizes."""
        for size in self.COMMON_FONTS:
            try:
                self.resource_manager.get_font(size)
                self.loaded_assets += 1

                if callback:
                    callback(self.loaded_assets / self.total_assets)
            except Exception as e:
                print(f"Failed to preload font size {size}: {e}")

    def get_progress(self) -> float:
        """
        Get loading progress.

        Returns:
            Progress as float 0.0 to 1.0
        """
        if self.total_assets == 0:
            return 1.0
        return self.loaded_assets / self.total_assets


def preload_game_assets(resource_manager: ResourceManager) -> None:
    """
    Helper function to preload all game assets.

    Args:
        resource_manager: ResourceManager instance
    """
    loader = AssetLoader(resource_manager)
    loader.preload_all()
