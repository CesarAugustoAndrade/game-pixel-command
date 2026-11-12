"""
Classical-themed color palettes for pixel art generation.

This module defines the 16-color palettes used throughout the game,
inspired by ancient civilizations and classical art.
"""

from typing import Tuple, Dict, List

# Color type alias for RGB tuples
Color = Tuple[int, int, int]

class ClassicalPalette:
    """
    Main 16-color palette for the classical strategy game.
    Based on ancient Greek pottery, Roman frescoes, and classical art.
    """

    # Base colors
    BLACK = (0, 0, 0)           # Pure black for outlines
    WHITE = (255, 255, 255)     # Pure white for highlights

    # Stone and marble colors
    STONE_DARK = (73, 65, 58)   # Dark stone/granite
    STONE_MID = (120, 108, 96)  # Medium stone
    STONE_LIGHT = (168, 152, 136) # Light stone/marble

    # Bronze and metal colors
    BRONZE_DARK = (92, 51, 23)   # Dark bronze/rust
    BRONZE_MID = (140, 89, 43)   # Bronze metal
    BRONZE_LIGHT = (196, 145, 79) # Polished bronze
    GOLD = (255, 215, 0)         # Gold accents

    # Organic colors
    SKIN_DARK = (139, 90, 43)    # Darker skin tone
    SKIN_LIGHT = (210, 180, 140)  # Lighter skin tone
    WOOD_BROWN = (101, 67, 33)   # Wood/leather

    # Terrain colors
    GRASS_GREEN = (52, 140, 49)  # Mediterranean grass
    WATER_BLUE = (64, 124, 172)  # Mediterranean sea
    SAND_YELLOW = (238, 203, 173) # Desert sand

    # UI accent color
    WINE_RED = (128, 0, 32)      # Roman wine red

    @classmethod
    def get_palette(cls) -> List[Color]:
        """Return the complete 16-color palette as a list."""
        return [
            cls.BLACK, cls.WHITE,
            cls.STONE_DARK, cls.STONE_MID, cls.STONE_LIGHT,
            cls.BRONZE_DARK, cls.BRONZE_MID, cls.BRONZE_LIGHT, cls.GOLD,
            cls.SKIN_DARK, cls.SKIN_LIGHT, cls.WOOD_BROWN,
            cls.GRASS_GREEN, cls.WATER_BLUE, cls.SAND_YELLOW,
            cls.WINE_RED
        ]


class FactionPalettes:
    """
    Faction-specific color palettes for unit differentiation.
    Each faction has primary, secondary, and accent colors.
    """

    GREEK = {
        'primary': (0, 48, 143),      # Deep blue
        'secondary': (255, 255, 255),  # White
        'accent': (255, 215, 0),       # Gold
        'shield': (0, 48, 143),        # Blue hoplon shield
        'plume': (255, 0, 0),          # Red plume
        'name': 'Greek City-States'
    }

    ROMAN = {
        'primary': (153, 0, 0),        # Deep red
        'secondary': (255, 215, 0),    # Gold
        'accent': (192, 192, 192),     # Silver
        'shield': (153, 0, 0),         # Red scutum
        'plume': (153, 0, 0),          # Red plume
        'name': 'Roman Republic'
    }

    PERSIAN = {
        'primary': (255, 215, 0),      # Gold
        'secondary': (128, 0, 128),    # Purple
        'accent': (0, 128, 128),       # Turquoise
        'shield': (255, 215, 0),       # Golden shields
        'plume': (128, 0, 128),        # Purple plume
        'name': 'Persian Empire'
    }

    CARTHAGE = {
        'primary': (128, 0, 128),      # Purple (Tyrian purple)
        'secondary': (255, 255, 255),  # White
        'accent': (255, 215, 0),       # Gold
        'shield': (255, 255, 255),     # White shield
        'plume': (128, 0, 128),        # Purple plume
        'name': 'Carthaginian Empire'
    }

    @classmethod
    def get_faction(cls, faction_name: str) -> Dict:
        """Get faction colors by name."""
        factions = {
            'greek': cls.GREEK,
            'roman': cls.ROMAN,
            'persian': cls.PERSIAN,
            'carthage': cls.CARTHAGE
        }
        return factions.get(faction_name.lower(), cls.GREEK)


class TerrainPalette:
    """
    Specialized palette for terrain tile generation.
    Includes variations for each terrain type.
    """

    GRASS_VARIATIONS = [
        (52, 140, 49),   # Base grass
        (45, 125, 42),   # Darker grass
        (60, 155, 56),   # Lighter grass
        (38, 110, 35),   # Shadow grass
    ]

    WATER_VARIATIONS = [
        (64, 124, 172),  # Base water
        (54, 114, 162),  # Darker water
        (74, 134, 182),  # Lighter water
        (44, 104, 152),  # Deep water
    ]

    SAND_VARIATIONS = [
        (238, 203, 173), # Base sand
        (228, 193, 163), # Darker sand
        (248, 213, 183), # Lighter sand
        (218, 183, 153), # Shadow sand
    ]

    MOUNTAIN_COLORS = [
        (73, 65, 58),    # Base rock
        (120, 108, 96),  # Mid rock
        (168, 152, 136), # Light rock
        (255, 255, 255), # Snow cap
    ]

    FOREST_COLORS = [
        (34, 87, 32),    # Dark tree
        (52, 140, 49),   # Mid tree
        (60, 155, 56),   # Light leaves
        (101, 67, 33),   # Tree trunk
    ]


def apply_faction_colors(base_colors: List[Color], faction: str) -> List[Color]:
    """
    Apply faction-specific color modifications to a base sprite.

    Args:
        base_colors: Original colors of the sprite
        faction: Name of the faction

    Returns:
        Modified colors with faction theming
    """
    faction_data = FactionPalettes.get_faction(faction)
    modified = base_colors.copy()

    # Replace specific colors with faction colors
    # This is a simple example - could be more sophisticated
    for i, color in enumerate(modified):
        # Replace reds with faction primary
        if color[0] > 150 and color[1] < 100 and color[2] < 100:
            modified[i] = faction_data['primary']
        # Replace blues with faction secondary
        elif color[2] > 150 and color[0] < 100 and color[1] < 100:
            modified[i] = faction_data['secondary']

    return modified