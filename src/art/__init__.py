"""
Pixel Art and Sprite Generation Module

This module contains all functionality for generating pixel art sprites,
including unit sprites, terrain tiles, and UI elements for the classical
army roguelike game.
"""

from .palettes import ClassicalPalette, FactionPalettes
from .sprite_generator import SpriteGenerator

__all__ = ['ClassicalPalette', 'FactionPalettes', 'SpriteGenerator']