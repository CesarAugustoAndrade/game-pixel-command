"""
Engine initialization and resource management.
"""

import pygame
from typing import Dict, Optional
from pathlib import Path
from src.core.config_manager import ConfigManager
from src.core.constants import PATH_SPRITES, PATH_SOUNDS, PATH_MUSIC


class ResourceManager:
    """
    Manages loading and caching of game resources (sprites, sounds, etc.).
    """

    def __init__(self):
        self._sprites: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._fonts: Dict[tuple, pygame.font.Font] = {}

    def load_sprite(self, path: str, scale: Optional[tuple] = None) -> pygame.Surface:
        """
        Load a sprite from file. Caches the result.

        Args:
            path: Path to the sprite file
            scale: Optional (width, height) to scale the sprite

        Returns:
            The loaded pygame Surface
        """
        cache_key = f"{path}_{scale}" if scale else path

        if cache_key not in self._sprites:
            try:
                sprite = pygame.image.load(path).convert_alpha()
                if scale:
                    sprite = pygame.transform.scale(sprite, scale)
                self._sprites[cache_key] = sprite
            except pygame.error as e:
                print(f"Failed to load sprite {path}: {e}")
                # Return a placeholder surface
                sprite = pygame.Surface((32, 32))
                sprite.fill((255, 0, 255))  # Magenta for missing sprites
                self._sprites[cache_key] = sprite

        return self._sprites[cache_key]

    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound from file. Caches the result.

        Args:
            path: Path to the sound file

        Returns:
            The loaded pygame Sound or None if failed
        """
        if path not in self._sounds:
            try:
                sound = pygame.mixer.Sound(path)
                self._sounds[path] = sound
            except pygame.error as e:
                print(f"Failed to load sound {path}: {e}")
                return None

        return self._sounds[path]

    def get_font(self, size: int, font_name: Optional[str] = None) -> pygame.font.Font:
        """
        Get a font object. Caches the result.

        Args:
            size: Font size
            font_name: Optional font name (None for system default)

        Returns:
            pygame Font object
        """
        cache_key = (font_name, size)

        if cache_key not in self._fonts:
            self._fonts[cache_key] = pygame.font.Font(font_name, size)

        return self._fonts[cache_key]

    def clear_cache(self) -> None:
        """Clear all cached resources."""
        self._sprites.clear()
        self._sounds.clear()
        self._fonts.clear()

    def get_sprite_path(self, category: str, filename: str) -> str:
        """
        Build path for a sprite file.

        Args:
            category: Sprite category (e.g., 'ui', 'units', 'terrain')
            filename: Sprite filename

        Returns:
            Full path to sprite file
        """
        return str(Path(PATH_SPRITES) / category / filename)

    def get_sound_path(self, filename: str) -> str:
        """
        Build path for a sound file.

        Args:
            filename: Sound filename

        Returns:
            Full path to sound file
        """
        return str(Path(PATH_SOUNDS) / filename)

    def get_music_path(self, filename: str) -> str:
        """
        Build path for a music file.

        Args:
            filename: Music filename

        Returns:
            Full path to music file
        """
        return str(Path(PATH_MUSIC) / filename)

    def preload_sprites(self, sprite_list: list) -> None:
        """
        Preload a list of sprites into cache.

        Args:
            sprite_list: List of tuples (path, scale) to preload
        """
        for sprite_info in sprite_list:
            if isinstance(sprite_info, tuple):
                path, scale = sprite_info
                self.load_sprite(path, scale)
            else:
                self.load_sprite(sprite_info)


class GameEngine:
    """
    Main game engine responsible for initialization and resource management.
    """

    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the game engine.

        Args:
            config_path: Path to configuration file
        """
        # Initialize ConfigManager first
        self.config = ConfigManager(config_path)

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Get display settings from config
        width = self.config.get('display', 'width', 1280)
        height = self.config.get('display', 'height', 720)
        fullscreen = self.config.get('display', 'fullscreen', False)
        vsync = self.config.get('display', 'vsync', True)
        title = "Classical Army Roguelite"

        # Create display
        flags = pygame.FULLSCREEN if fullscreen else 0
        if vsync:
            flags |= pygame.SCALED
        self.screen = pygame.display.set_mode((width, height), flags, vsync=1 if vsync else 0)
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.resource_manager = ResourceManager()

        self.is_running = False

        # Set audio volumes from config
        self._apply_audio_settings()

    def get_delta_time(self, fps: int) -> float:
        """
        Get the delta time in seconds and tick the clock.

        Args:
            fps: Target frames per second

        Returns:
            Delta time in seconds
        """
        return self.clock.tick(fps) / 1000.0

    def _apply_audio_settings(self) -> None:
        """Apply audio settings from configuration."""
        master_volume = self.config.get('audio', 'master_volume', 0.8)
        music_volume = self.config.get('audio', 'music_volume', 0.6)

        # Set pygame mixer volumes
        pygame.mixer.music.set_volume(master_volume * music_volume)

    def apply_display_settings(self) -> None:
        """Apply display settings from config (for runtime changes)."""
        width = self.config.get('display', 'width', 1280)
        height = self.config.get('display', 'height', 720)
        fullscreen = self.config.get('display', 'fullscreen', False)

        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((width, height), flags)

    def get_fps_target(self) -> int:
        """Get target FPS from config."""
        return self.config.get('display', 'fps', 60)

    def quit(self) -> None:
        """Clean up and quit the engine."""
        self.is_running = False
        pygame.quit()
