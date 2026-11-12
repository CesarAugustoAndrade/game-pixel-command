"""
Bitmap Font System for Classical Army Roguelike

Provides pixel-perfect text rendering using bitmap fonts.
Supports both generated and loaded bitmap fonts.
"""

import pygame
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Tuple, Optional, List

class BitmapFont:
    """
    Bitmap font renderer for pixel-perfect text.
    """

    # Character sets
    CHARSET_BASIC = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?.,:-+*/=()[]{}\"'<>_| "
    CHARSET_NUMBERS = "0123456789"
    CHARSET_ROMAN = "IVXLCDM"  # Roman numerals

    def __init__(self, char_width: int = 8, char_height: int = 8):
        """
        Initialize bitmap font.

        Args:
            char_width: Width of each character
            char_height: Height of each character
        """
        self.char_width = char_width
        self.char_height = char_height
        self.characters = {}  # Dictionary of character surfaces
        self.spacing = 1  # Pixel spacing between characters

    def generate_pixel_font(self, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Generate a simple pixel font programmatically.
        Creates basic 5x7 characters within the specified char size.
        """
        # Define pixel patterns for each character (5x7 within 8x8 grid)
        font_data = {
            'A': [
                "  XXX  ",
                " X   X ",
                "X     X",
                "XXXXXXX",
                "X     X",
                "X     X",
                "X     X",
            ],
            'B': [
                "XXXXXX ",
                "X     X",
                "X     X",
                "XXXXXX ",
                "X     X",
                "X     X",
                "XXXXXX ",
            ],
            'C': [
                " XXXXX ",
                "X     X",
                "X      ",
                "X      ",
                "X      ",
                "X     X",
                " XXXXX ",
            ],
            'D': [
                "XXXXX  ",
                "X    X ",
                "X     X",
                "X     X",
                "X     X",
                "X    X ",
                "XXXXX  ",
            ],
            'E': [
                "XXXXXXX",
                "X      ",
                "X      ",
                "XXXXX  ",
                "X      ",
                "X      ",
                "XXXXXXX",
            ],
            'H': [
                "X     X",
                "X     X",
                "X     X",
                "XXXXXXX",
                "X     X",
                "X     X",
                "X     X",
            ],
            'I': [
                " XXXXX ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                " XXXXX ",
            ],
            'L': [
                "X      ",
                "X      ",
                "X      ",
                "X      ",
                "X      ",
                "X      ",
                "XXXXXXX",
            ],
            'O': [
                " XXXXX ",
                "X     X",
                "X     X",
                "X     X",
                "X     X",
                "X     X",
                " XXXXX ",
            ],
            'R': [
                "XXXXXX ",
                "X     X",
                "X     X",
                "XXXXXX ",
                "X   X  ",
                "X    X ",
                "X     X",
            ],
            'T': [
                "XXXXXXX",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
            ],
            '0': [
                " XXXXX ",
                "X     X",
                "X   X X",
                "X  X  X",
                "X X   X",
                "X     X",
                " XXXXX ",
            ],
            '1': [
                "   X   ",
                "  XX   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                " XXXXX ",
            ],
            '2': [
                " XXXXX ",
                "X     X",
                "      X",
                " XXXXX ",
                "X      ",
                "X      ",
                "XXXXXXX",
            ],
            '3': [
                " XXXXX ",
                "X     X",
                "      X",
                "  XXXX ",
                "      X",
                "X     X",
                " XXXXX ",
            ],
            '4': [
                "    XX ",
                "   X X ",
                "  X  X ",
                " X   X ",
                "XXXXXXX",
                "     X ",
                "     X ",
            ],
            '5': [
                "XXXXXXX",
                "X      ",
                "X      ",
                "XXXXXX ",
                "      X",
                "X     X",
                " XXXXX ",
            ],
            ':': [
                "       ",
                "   XX  ",
                "   XX  ",
                "       ",
                "   XX  ",
                "   XX  ",
                "       ",
            ],
            '/': [
                "      X",
                "     X ",
                "    X  ",
                "   X   ",
                "  X    ",
                " X     ",
                "X      ",
            ],
            ' ': [
                "       ",
                "       ",
                "       ",
                "       ",
                "       ",
                "       ",
                "       ",
            ],
            '.': [
                "       ",
                "       ",
                "       ",
                "       ",
                "       ",
                "   XX  ",
                "   XX  ",
            ],
            '!': [
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "       ",
                "   X   ",
            ],
            '?': [
                " XXXXX ",
                "X     X",
                "      X",
                "   XXX ",
                "   X   ",
                "       ",
                "   X   ",
            ],
        }

        # Generate lowercase as smaller versions
        lowercase_map = {
            'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E',
            'h': 'H', 'i': 'I', 'l': 'L', 'o': 'O', 'r': 'R', 't': 'T'
        }

        # Create surfaces for defined characters
        for char, pattern in font_data.items():
            surface = pygame.Surface((self.char_width, self.char_height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))  # Transparent background

            for y, row in enumerate(pattern):
                if y >= self.char_height:
                    break
                for x, pixel in enumerate(row):
                    if x >= self.char_width:
                        break
                    if pixel == 'X':
                        surface.set_at((x, y), color)

            self.characters[char] = surface

        # Generate lowercase (offset by 1 pixel down and slightly smaller)
        for lower, upper in lowercase_map.items():
            if upper in font_data:
                surface = pygame.Surface((self.char_width, self.char_height), pygame.SRCALPHA)
                surface.fill((0, 0, 0, 0))

                pattern = font_data[upper]
                for y in range(1, len(pattern)):  # Start from row 1, making it smaller
                    if y >= self.char_height - 1:
                        break
                    row = pattern[y]
                    for x, pixel in enumerate(row[1:]):  # Skip first column
                        if x >= self.char_width - 2:
                            break
                        if pixel == 'X':
                            surface.set_at((x, y + 1), color)

                self.characters[lower] = surface

        # Generate remaining numbers and letters not explicitly defined
        for i in range(6, 10):
            if str(i) not in self.characters:
                # Copy pattern from '5' and modify slightly
                self.characters[str(i)] = self._generate_default_char(str(i), color)

        # Generate other missing uppercase letters
        for c in "FGJKMNPQSUVWXYZ":
            if c not in self.characters:
                self.characters[c] = self._generate_default_char(c, color)

        # Generate remaining lowercase
        for c in "fgjkmnpqsuvwxyz":
            if c not in self.characters:
                self.characters[c] = self._generate_default_char(c.upper(), color, True)

        # Special characters
        special_chars = {
            '-': [(0, 3, 5, 1)],  # Horizontal line
            '+': [(2, 1, 1, 5), (0, 3, 5, 1)],  # Cross
            '=': [(0, 2, 5, 1), (0, 4, 5, 1)],  # Two horizontal lines
            '(': [(3, 1, 1, 1), (2, 2, 1, 3), (3, 5, 1, 1)],  # Left parenthesis
            ')': [(1, 1, 1, 1), (2, 2, 1, 3), (1, 5, 1, 1)],  # Right parenthesis
        }

        for char, rects in special_chars.items():
            surface = pygame.Surface((self.char_width, self.char_height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))
            for x, y, w, h in rects:
                pygame.draw.rect(surface, color, (x, y, w, h))
            self.characters[char] = surface

    def _generate_default_char(self, char: str, color: Tuple[int, int, int],
                              lowercase: bool = False) -> pygame.Surface:
        """Generate a default character pattern."""
        surface = pygame.Surface((self.char_width, self.char_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        # Simple box with character indicator
        offset = 1 if lowercase else 0
        size_reduce = 2 if lowercase else 0

        # Draw a simple rectangular pattern as placeholder
        pygame.draw.rect(surface, color,
                        (offset, offset + 1,
                         self.char_width - 2 - size_reduce,
                         self.char_height - 3 - size_reduce), 1)

        return surface

    def render_text(self, text: str, color: Optional[Tuple[int, int, int]] = None) -> pygame.Surface:
        """
        Render text using the bitmap font.

        Args:
            text: Text to render
            color: Optional color override (if None, uses original font color)

        Returns:
            Surface containing the rendered text
        """
        if not self.characters:
            self.generate_pixel_font()

        # Calculate total width
        total_width = len(text) * (self.char_width + self.spacing) - self.spacing
        surface = pygame.Surface((total_width, self.char_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        # Render each character
        x_pos = 0
        for char in text:
            if char in self.characters:
                char_surface = self.characters[char]

                # Apply color if specified
                if color:
                    colored_surface = char_surface.copy()
                    # Replace all non-transparent pixels with the new color
                    for x in range(colored_surface.get_width()):
                        for y in range(colored_surface.get_height()):
                            if colored_surface.get_at((x, y))[3] > 0:  # If not transparent
                                colored_surface.set_at((x, y), color)
                    surface.blit(colored_surface, (x_pos, 0))
                else:
                    surface.blit(char_surface, (x_pos, 0))

            x_pos += self.char_width + self.spacing

        return surface

    def render_number(self, number: int, color: Optional[Tuple[int, int, int]] = None,
                     use_roman: bool = False) -> pygame.Surface:
        """
        Render a number, optionally as Roman numerals.

        Args:
            number: Number to render
            color: Optional color override
            use_roman: Whether to use Roman numerals

        Returns:
            Surface containing the rendered number
        """
        if use_roman:
            text = self._to_roman(number)
        else:
            text = str(number)

        return self.render_text(text, color)

    def _to_roman(self, number: int) -> str:
        """Convert number to Roman numerals."""
        if number <= 0 or number > 3999:
            return str(number)  # Fallback to Arabic

        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syms = [
            'M', 'CM', 'D', 'CD',
            'C', 'XC', 'L', 'XL',
            'X', 'IX', 'V', 'IV',
            'I'
        ]
        roman_num = ''
        i = 0
        while number > 0:
            for _ in range(number // val[i]):
                roman_num += syms[i]
                number -= val[i]
            i += 1
        return roman_num

    def get_text_size(self, text: str) -> Tuple[int, int]:
        """Get the size of rendered text."""
        width = len(text) * (self.char_width + self.spacing) - self.spacing
        return (width, self.char_height)

class BitmapFontManager:
    """
    Manager for multiple bitmap fonts.
    """

    def __init__(self):
        """Initialize font manager."""
        self.fonts = {}
        self._create_default_fonts()

    def _create_default_fonts(self):
        """Create default fonts of different sizes."""
        # Small font (8x8)
        small_font = BitmapFont(8, 8)
        small_font.generate_pixel_font((255, 255, 255))
        self.fonts['small'] = small_font

        # Medium font (12x12)
        medium_font = BitmapFont(12, 12)
        medium_font.generate_pixel_font((255, 255, 255))
        self.fonts['medium'] = medium_font

        # Large font (16x16)
        large_font = BitmapFont(16, 16)
        large_font.generate_pixel_font((255, 255, 255))
        self.fonts['large'] = large_font

    def get_font(self, size: str = 'small') -> BitmapFont:
        """Get a font by size name."""
        return self.fonts.get(size, self.fonts['small'])

    def render(self, text: str, size: str = 'small',
              color: Optional[Tuple[int, int, int]] = None) -> pygame.Surface:
        """Convenience method to render text."""
        font = self.get_font(size)
        return font.render_text(text, color)