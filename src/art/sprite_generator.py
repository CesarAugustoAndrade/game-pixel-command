"""
Sprite Generator for Classical Army Roguelike

Generates 16x16 pixel art sprites for units, terrain, and UI elements
using procedural generation techniques with the Pillow library.
"""

from PIL import Image, ImageDraw
from typing import List, Tuple, Optional, Dict
import random
from .palettes import ClassicalPalette, FactionPalettes, TerrainPalette

class SpriteGenerator:
    """Main sprite generation class for creating pixel art assets."""

    SPRITE_SIZE = 16  # Standard sprite size

    def __init__(self):
        """Initialize the sprite generator."""
        self.palette = ClassicalPalette()
        self.faction_palettes = FactionPalettes()

    @staticmethod
    def create_blank_sprite(size: int = 16, background: Tuple[int, int, int] = None) -> Image.Image:
        """Create a blank sprite with transparent or colored background."""
        img = Image.new('RGBA', (size, size), background or (0, 0, 0, 0))
        return img

    def generate_hoplite_sprite(self, faction: str = 'greek') -> Image.Image:
        """
        Generate a Greek Hoplite sprite (heavy infantry).
        Features: Round shield (hoplon), spear, helmet with plume.
        """
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)
        colors = FactionPalettes.get_faction(faction)

        # Body (bronze armor)
        draw.rectangle([5, 7, 10, 13], fill=self.palette.BRONZE_MID)
        draw.rectangle([6, 8, 9, 12], fill=self.palette.BRONZE_LIGHT)

        # Head/Helmet
        draw.rectangle([6, 4, 9, 7], fill=self.palette.BRONZE_DARK)
        draw.rectangle([7, 5, 8, 6], fill=self.palette.SKIN_LIGHT)  # Face

        # Plume on helmet
        draw.rectangle([7, 2, 8, 4], fill=colors['plume'])

        # Arms
        draw.line([(4, 8), (4, 10)], fill=self.palette.SKIN_DARK, width=1)  # Left arm
        draw.line([(11, 8), (11, 10)], fill=self.palette.BRONZE_MID, width=1)  # Right arm (shield)

        # Legs
        draw.line([(6, 13), (6, 15)], fill=self.palette.BRONZE_DARK, width=1)
        draw.line([(9, 13), (9, 15)], fill=self.palette.BRONZE_DARK, width=1)

        # Round shield (hoplon) - characteristic Greek shield
        draw.ellipse([1, 7, 5, 11], fill=colors['shield'], outline=self.palette.BRONZE_DARK)
        # Shield pattern (lambda for Sparta or other symbol)
        draw.line([(2, 8), (3, 10)], fill=self.palette.WHITE, width=1)
        draw.line([(4, 8), (3, 10)], fill=self.palette.WHITE, width=1)

        # Spear (dory) - vertical
        draw.line([(12, 3), (12, 14)], fill=self.palette.WOOD_BROWN, width=1)
        draw.point((12, 2), fill=self.palette.BRONZE_LIGHT)  # Spear tip

        return img

    def generate_legionary_sprite(self, faction: str = 'roman') -> Image.Image:
        """
        Generate a Roman Legionary sprite.
        Features: Rectangular shield (scutum), short sword (gladius), segmented armor.
        """
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)
        colors = FactionPalettes.get_faction(faction)

        # Body (segmented armor - lorica segmentata)
        draw.rectangle([5, 7, 10, 13], fill=self.palette.BRONZE_DARK)
        # Armor segments
        for y in [8, 10, 12]:
            draw.line([(5, y), (10, y)], fill=self.palette.BRONZE_LIGHT, width=1)

        # Head/Helmet (galea)
        draw.rectangle([6, 4, 9, 7], fill=self.palette.BRONZE_MID)
        draw.rectangle([7, 5, 8, 6], fill=self.palette.SKIN_LIGHT)  # Face

        # Helmet crest
        draw.rectangle([7, 2, 8, 4], fill=colors['plume'])

        # Arms
        draw.line([(4, 8), (4, 10)], fill=self.palette.SKIN_DARK, width=1)
        draw.line([(11, 8), (11, 10)], fill=self.palette.SKIN_DARK, width=1)

        # Legs with pteruges (leather strips)
        draw.line([(6, 13), (6, 15)], fill=self.palette.BRONZE_DARK, width=1)
        draw.line([(9, 13), (9, 15)], fill=self.palette.BRONZE_DARK, width=1)

        # Rectangular shield (scutum) - characteristic Roman shield
        draw.rectangle([1, 6, 4, 12], fill=colors['shield'], outline=self.palette.BRONZE_DARK)
        # Shield boss and pattern
        draw.point((2, 9), fill=self.palette.BRONZE_LIGHT)
        draw.line([(2, 7), (2, 11)], fill=self.palette.GOLD, width=1)

        # Gladius (short sword) - diagonal
        draw.line([(11, 9), (13, 7)], fill=self.palette.BRONZE_LIGHT, width=1)
        draw.point((13, 6), fill=self.palette.BRONZE_LIGHT)  # Sword tip

        return img

    def generate_immortal_sprite(self, faction: str = 'persian') -> Image.Image:
        """
        Generate a Persian Immortal sprite.
        Features: Scale armor, bow/spear combo, distinctive headgear.
        """
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)
        colors = FactionPalettes.get_faction(faction)

        # Body (scale armor)
        draw.rectangle([5, 7, 10, 13], fill=colors['primary'])
        # Scale pattern
        for y in range(8, 13, 2):
            for x in range(6, 10):
                draw.point((x, y), fill=self.palette.BRONZE_LIGHT)

        # Head with Persian cap/turban
        draw.ellipse([6, 3, 9, 7], fill=colors['secondary'])
        draw.rectangle([7, 5, 8, 6], fill=self.palette.SKIN_DARK)  # Face

        # Arms
        draw.line([(4, 8), (4, 10)], fill=self.palette.SKIN_DARK, width=1)
        draw.line([(11, 8), (11, 10)], fill=colors['primary'], width=1)

        # Legs with Persian trousers
        draw.line([(6, 13), (6, 15)], fill=colors['secondary'], width=1)
        draw.line([(9, 13), (9, 15)], fill=colors['secondary'], width=1)

        # Bow (composite bow)
        draw.line([(2, 6), (2, 10)], fill=self.palette.WOOD_BROWN, width=1)
        draw.line([(2, 6), (3, 7)], fill=self.palette.WOOD_BROWN, width=1)
        draw.line([(2, 10), (3, 9)], fill=self.palette.WOOD_BROWN, width=1)
        # Bow string
        draw.line([(3, 7), (3, 9)], fill=self.palette.WHITE, width=1)

        # Spear
        draw.line([(12, 4), (12, 14)], fill=self.palette.WOOD_BROWN, width=1)
        draw.point((12, 3), fill=self.palette.BRONZE_LIGHT)

        # Wicker shield (small)
        draw.ellipse([10, 8, 12, 10], fill=colors['accent'], outline=self.palette.WOOD_BROWN)

        return img

    def generate_sacred_band_sprite(self, faction: str = 'carthage') -> Image.Image:
        """
        Generate a Carthaginian Sacred Band sprite (elite heavy infantry).
        Features: Heavy armor, large shield, spear.
        """
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)
        colors = FactionPalettes.get_faction(faction)

        # Body (heavy armor with Tyrian purple)
        draw.rectangle([5, 7, 10, 13], fill=colors['primary'])
        draw.rectangle([6, 8, 9, 12], fill=self.palette.BRONZE_LIGHT)  # Breastplate

        # Head/Helmet (Hellenistic style)
        draw.rectangle([6, 4, 9, 7], fill=self.palette.BRONZE_MID)
        draw.rectangle([7, 5, 8, 6], fill=self.palette.SKIN_DARK)  # Face

        # Helmet plume (distinctive purple)
        draw.rectangle([6, 2, 9, 4], fill=colors['primary'])

        # Arms
        draw.line([(4, 8), (4, 10)], fill=self.palette.BRONZE_MID, width=1)
        draw.line([(11, 8), (11, 10)], fill=self.palette.BRONZE_MID, width=1)

        # Legs with greaves
        draw.line([(6, 13), (6, 15)], fill=self.palette.BRONZE_MID, width=1)
        draw.line([(9, 13), (9, 15)], fill=self.palette.BRONZE_MID, width=1)

        # Large round shield (aspis)
        draw.ellipse([1, 6, 5, 11], fill=colors['shield'], outline=self.palette.BRONZE_DARK)
        # Carthaginian symbol (simplified)
        draw.point((3, 8), fill=colors['primary'])
        draw.point((3, 9), fill=colors['primary'])

        # Long spear
        draw.line([(12, 2), (12, 14)], fill=self.palette.WOOD_BROWN, width=1)
        draw.rectangle([11, 1, 13, 2], fill=self.palette.BRONZE_LIGHT)  # Spear tip

        return img

    def generate_archer_sprite(self, faction: str) -> Image.Image:
        """Generate a basic archer sprite for any faction."""
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)
        colors = FactionPalettes.get_faction(faction)

        # Light armor body
        draw.rectangle([5, 7, 10, 13], fill=colors['secondary'])

        # Head with simple cap
        draw.rectangle([6, 4, 9, 7], fill=self.palette.SKIN_LIGHT)
        draw.rectangle([6, 4, 9, 5], fill=colors['primary'])  # Cap

        # Arms positioned for bow
        draw.line([(4, 8), (3, 9)], fill=self.palette.SKIN_DARK, width=1)
        draw.line([(11, 8), (12, 9)], fill=self.palette.SKIN_DARK, width=1)

        # Legs
        draw.line([(6, 13), (6, 15)], fill=colors['secondary'], width=1)
        draw.line([(9, 13), (9, 15)], fill=colors['secondary'], width=1)

        # Large bow
        draw.line([(2, 5), (2, 11)], fill=self.palette.WOOD_BROWN, width=1)
        draw.line([(2, 5), (4, 6)], fill=self.palette.WOOD_BROWN, width=1)
        draw.line([(2, 11), (4, 10)], fill=self.palette.WOOD_BROWN, width=1)
        # Arrow
        draw.line([(3, 8), (6, 8)], fill=self.palette.WOOD_BROWN, width=1)

        # Quiver on back
        draw.rectangle([10, 5, 11, 9], fill=self.palette.WOOD_BROWN)

        return img

    def generate_cavalry_sprite(self, faction: str) -> Image.Image:
        """Generate a basic cavalry sprite for any faction."""
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)
        colors = FactionPalettes.get_faction(faction)

        # Horse body (simplified)
        draw.ellipse([3, 9, 10, 14], fill=self.palette.WOOD_BROWN)
        draw.rectangle([8, 10, 10, 15], fill=self.palette.WOOD_BROWN)  # Horse legs

        # Horse head
        draw.rectangle([1, 8, 4, 11], fill=self.palette.WOOD_BROWN)

        # Rider body
        draw.rectangle([5, 5, 8, 9], fill=colors['primary'])

        # Rider head
        draw.rectangle([5, 3, 7, 5], fill=self.palette.BRONZE_MID)
        draw.point((6, 4), fill=self.palette.SKIN_LIGHT)

        # Shield
        draw.ellipse([3, 5, 5, 8], fill=colors['shield'], outline=self.palette.BLACK)

        # Spear
        draw.line([(9, 2), (12, 8)], fill=self.palette.WOOD_BROWN, width=1)
        draw.point((12, 8), fill=self.palette.BRONZE_LIGHT)

        return img

    def generate_unit_sprite(self, unit_type: str, faction: str) -> Image.Image:
        """
        Generate a sprite for a specific unit type and faction.

        Args:
            unit_type: Type of unit (hoplite, legionary, archer, etc.)
            faction: Faction name (greek, roman, persian, carthage)

        Returns:
            Generated sprite image
        """
        generators = {
            'hoplite': self.generate_hoplite_sprite,
            'legionary': self.generate_legionary_sprite,
            'immortal': self.generate_immortal_sprite,
            'sacred_band': self.generate_sacred_band_sprite,
            'archer': self.generate_archer_sprite,
            'cavalry': self.generate_cavalry_sprite,
        }

        generator = generators.get(unit_type.lower())
        if generator:
            if unit_type in ['archer', 'cavalry']:
                return generator(faction)
            else:
                return generator(faction)
        else:
            # Default to a basic soldier if type not found
            return self.generate_hoplite_sprite(faction)

    def generate_grass_tile(self) -> Image.Image:
        """Generate a grass terrain tile with variation."""
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)

        # Base grass color
        draw.rectangle([0, 0, 15, 15], fill=TerrainPalette.GRASS_VARIATIONS[0])

        # Add grass texture
        for _ in range(20):
            x = random.randint(0, 15)
            y = random.randint(0, 15)
            color = random.choice(TerrainPalette.GRASS_VARIATIONS[1:])
            draw.point((x, y), fill=color)

        # Add occasional grass blades
        for _ in range(3):
            x = random.randint(1, 14)
            y = random.randint(1, 14)
            draw.line([(x, y), (x, y-2)], fill=TerrainPalette.GRASS_VARIATIONS[2], width=1)

        return img

    def generate_water_tile(self) -> Image.Image:
        """Generate a water terrain tile with wave pattern."""
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)

        # Base water
        draw.rectangle([0, 0, 15, 15], fill=TerrainPalette.WATER_VARIATIONS[0])

        # Wave pattern
        for y in range(0, 16, 4):
            for x in range(0, 16, 2):
                offset = 1 if (y // 4) % 2 == 0 else 0
                draw.point((x + offset, y), fill=TerrainPalette.WATER_VARIATIONS[2])
                draw.point((x + offset, y + 1), fill=TerrainPalette.WATER_VARIATIONS[1])

        return img

    def generate_sand_tile(self) -> Image.Image:
        """Generate a sand/desert terrain tile."""
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)

        # Base sand
        draw.rectangle([0, 0, 15, 15], fill=TerrainPalette.SAND_VARIATIONS[0])

        # Sand texture
        for _ in range(25):
            x = random.randint(0, 15)
            y = random.randint(0, 15)
            color = random.choice(TerrainPalette.SAND_VARIATIONS[1:])
            draw.point((x, y), fill=color)

        # Occasional dune lines
        if random.random() > 0.5:
            y = random.randint(4, 12)
            draw.line([(2, y), (13, y+1)], fill=TerrainPalette.SAND_VARIATIONS[3], width=1)

        return img

    def generate_mountain_tile(self) -> Image.Image:
        """Generate a mountain terrain tile."""
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)

        # Base rocky ground
        draw.rectangle([0, 0, 15, 15], fill=TerrainPalette.MOUNTAIN_COLORS[0])

        # Mountain peak shape
        points = [(7, 2), (3, 10), (11, 10)]
        draw.polygon(points, fill=TerrainPalette.MOUNTAIN_COLORS[1])

        # Lighter face
        points2 = [(7, 2), (7, 10), (11, 10)]
        draw.polygon(points2, fill=TerrainPalette.MOUNTAIN_COLORS[2])

        # Snow cap
        draw.line([(6, 3), (8, 3)], fill=TerrainPalette.MOUNTAIN_COLORS[3], width=1)
        draw.point((7, 2), fill=TerrainPalette.MOUNTAIN_COLORS[3])

        # Rock texture at base
        for _ in range(8):
            x = random.randint(0, 15)
            y = random.randint(11, 15)
            draw.point((x, y), fill=TerrainPalette.MOUNTAIN_COLORS[1])

        return img

    def generate_forest_tile(self) -> Image.Image:
        """Generate a forest terrain tile."""
        img = self.create_blank_sprite()
        draw = ImageDraw.Draw(img)

        # Grass base
        draw.rectangle([0, 0, 15, 15], fill=TerrainPalette.GRASS_VARIATIONS[0])

        # Tree trunks
        draw.rectangle([3, 8, 4, 12], fill=TerrainPalette.FOREST_COLORS[3])
        draw.rectangle([10, 9, 11, 13], fill=TerrainPalette.FOREST_COLORS[3])

        # Tree foliage (circular)
        draw.ellipse([1, 3, 6, 8], fill=TerrainPalette.FOREST_COLORS[1])
        draw.ellipse([8, 4, 13, 9], fill=TerrainPalette.FOREST_COLORS[0])

        # Add texture to trees
        for _ in range(6):
            x = random.randint(1, 6)
            y = random.randint(3, 8)
            draw.point((x, y), fill=TerrainPalette.FOREST_COLORS[2])

        for _ in range(6):
            x = random.randint(8, 13)
            y = random.randint(4, 9)
            draw.point((x, y), fill=TerrainPalette.FOREST_COLORS[2])

        return img

    def generate_terrain_tile(self, terrain_type: str) -> Image.Image:
        """
        Generate a terrain tile of the specified type.

        Args:
            terrain_type: Type of terrain (grass, water, sand, mountain, forest)

        Returns:
            Generated terrain tile image
        """
        generators = {
            'grass': self.generate_grass_tile,
            'water': self.generate_water_tile,
            'sand': self.generate_sand_tile,
            'mountain': self.generate_mountain_tile,
            'forest': self.generate_forest_tile,
        }

        generator = generators.get(terrain_type.lower(), self.generate_grass_tile)
        return generator()

    def create_sprite_sheet(self, sprites: List[Image.Image], columns: int = 8) -> Image.Image:
        """
        Create a sprite sheet from a list of sprites.

        Args:
            sprites: List of sprite images
            columns: Number of columns in the sprite sheet

        Returns:
            Combined sprite sheet image
        """
        if not sprites:
            return self.create_blank_sprite()

        sprite_size = sprites[0].size[0]
        rows = (len(sprites) + columns - 1) // columns

        sheet_width = columns * sprite_size
        sheet_height = rows * sprite_size

        sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))

        for i, sprite in enumerate(sprites):
            col = i % columns
            row = i // columns
            x = col * sprite_size
            y = row * sprite_size
            sheet.paste(sprite, (x, y))

        return sheet