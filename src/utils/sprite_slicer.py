"""
Sprite Slicer - Extract sprites from sprite sheets.
"""

import pygame
from typing import List, Tuple


class SpriteSlicer:
    """
    Utility for slicing sprites from sprite sheets.
    """

    @staticmethod
    def load_and_slice(
        image_path: str,
        slice_rects: List[Tuple[int, int, int, int]]
    ) -> List[pygame.Surface]:
        """
        Load an image and slice it into multiple sprites.

        Args:
            image_path: Path to the sprite sheet
            slice_rects: List of (x, y, width, height) rectangles to extract

        Returns:
            List of sliced pygame surfaces
        """
        # Load the sprite sheet
        sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Extract each sprite
        sprites = []
        for rect in slice_rects:
            x, y, width, height = rect
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), (x, y, width, height))
            sprites.append(sprite)

        return sprites

    @staticmethod
    def slice_vertical_strip(
        image_path: str,
        start_y: int,
        sprite_height: int,
        spacing: int,
        count: int,
        full_width: bool = True,
        x: int = 0,
        width: int = None
    ) -> List[pygame.Surface]:
        """
        Slice a vertical strip of evenly-spaced sprites.

        Args:
            image_path: Path to the sprite sheet
            start_y: Y position of first sprite
            sprite_height: Height of each sprite
            spacing: Vertical spacing between sprites
            count: Number of sprites to extract
            full_width: If True, use full image width (default True)
            x: X position if not full width
            width: Width if not full width

        Returns:
            List of sliced sprites
        """
        sprite_sheet = pygame.image.load(image_path).convert_alpha()
        sheet_width = sprite_sheet.get_width()

        sprites = []
        current_y = start_y

        for i in range(count):
            sprite_width = sheet_width if full_width else width
            sprite_x = 0 if full_width else x

            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), (sprite_x, current_y, sprite_width, sprite_height))
            sprites.append(sprite)

            current_y += sprite_height + spacing

        return sprites


def slice_menu_buttons(image_path: str) -> dict:
    """
    Slice menu button sprites from menu-buttons.png.

    Returns dictionary with:
    - 'title': Title banner sprite
    - 'new_campaign': New Campaign button
    - 'continue': Continue button
    - 'settings': Settings button
    - 'quit': Quit button

    Args:
        image_path: Path to menu-buttons.png

    Returns:
        Dictionary of button sprites
    """
    # Load the full sprite sheet to get dimensions
    sprite_sheet = pygame.image.load(image_path).convert_alpha()
    sheet_width = sprite_sheet.get_width()
    sheet_height = sprite_sheet.get_height()

    # Approximate measurements from the image
    # Title banner is at the top
    title_height = int(sheet_height * 0.25)  # ~25% of total height
    title_rect = (0, 0, sheet_width, title_height)

    # Buttons start after some spacing
    buttons_start_y = title_height + int(sheet_height * 0.08)  # Gap after title
    button_height = int(sheet_height * 0.13)  # Each button is ~13% of height
    button_spacing = int(sheet_height * 0.015)  # Small spacing between buttons

    # Calculate centered button region
    button_margin = int(sheet_width * 0.05)  # 5% margin on each side
    button_width = sheet_width - (button_margin * 2)
    button_x = button_margin

    # Extract title
    title = pygame.Surface((sheet_width, title_height), pygame.SRCALPHA)
    title.blit(sprite_sheet, (0, 0), title_rect)

    # Extract buttons
    buttons = []
    current_y = buttons_start_y
    for i in range(4):  # 4 buttons
        button = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        button.blit(sprite_sheet, (0, 0), (button_x, current_y, button_width, button_height))
        buttons.append(button)
        current_y += button_height + button_spacing

    return {
        'title': title,
        'new_campaign': buttons[0],
        'continue': buttons[1],
        'settings': buttons[2],
        'quit': buttons[3]
    }
