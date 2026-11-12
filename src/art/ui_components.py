"""
UI Component Generator for Classical Army Roguelike

Generates pixel art UI components with classical theming:
- Stone panels with 9-slice borders
- Bronze buttons with 3D effects
- Parchment backgrounds
- Health bars and status indicators
- Classical decorative elements
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Dict, List, Optional
from .palettes import ClassicalPalette

class UIComponentGenerator:
    """Generate pixel art UI components with classical theming."""

    def __init__(self):
        """Initialize UI component generator."""
        self.palette = ClassicalPalette()

    def generate_stone_panel(self, width: int = 64, height: int = 64) -> Dict[str, Image.Image]:
        """
        Generate a stone panel with 9-slice border system.
        Returns a dictionary with all 9 slices for flexible scaling.
        """
        slices = {}
        corner_size = 8  # Size of corner pieces

        # Create the full panel first
        panel = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel)

        # Base stone color with gradient effect
        base_color = self.palette.STONE_MID
        dark_color = self.palette.STONE_DARK
        light_color = self.palette.STONE_LIGHT

        # Draw base panel
        draw.rectangle([2, 2, width-3, height-3], fill=base_color)

        # Add depth with borders
        # Top and left borders (lighter - catching light)
        draw.line([(2, 2), (width-3, 2)], fill=light_color, width=2)  # Top
        draw.line([(2, 2), (2, height-3)], fill=light_color, width=2)  # Left

        # Bottom and right borders (darker - in shadow)
        draw.line([(3, height-3), (width-2, height-3)], fill=dark_color, width=2)  # Bottom
        draw.line([(width-3, 3), (width-3, height-3)], fill=dark_color, width=2)  # Right

        # Add corner accents (chiseled effect)
        draw.rectangle([0, 0, 4, 4], fill=dark_color)  # Top-left
        draw.rectangle([width-4, 0, width, 4], fill=dark_color)  # Top-right
        draw.rectangle([0, height-4, 4, height], fill=dark_color)  # Bottom-left
        draw.rectangle([width-4, height-4, width, height], fill=dark_color)  # Bottom-right

        # Add texture (stone speckles)
        import random
        for _ in range(width * height // 100):
            x = random.randint(4, width-5)
            y = random.randint(4, height-5)
            shade = random.choice([dark_color, light_color])
            draw.point((x, y), fill=shade)

        # Create 9-slice pieces
        # Corners
        slices['top_left'] = panel.crop((0, 0, corner_size, corner_size))
        slices['top_right'] = panel.crop((width-corner_size, 0, width, corner_size))
        slices['bottom_left'] = panel.crop((0, height-corner_size, corner_size, height))
        slices['bottom_right'] = panel.crop((width-corner_size, height-corner_size, width, height))

        # Edges
        slices['top'] = panel.crop((corner_size, 0, width-corner_size, corner_size))
        slices['bottom'] = panel.crop((corner_size, height-corner_size, width-corner_size, height))
        slices['left'] = panel.crop((0, corner_size, corner_size, height-corner_size))
        slices['right'] = panel.crop((width-corner_size, corner_size, width, height-corner_size))

        # Center
        slices['center'] = panel.crop((corner_size, corner_size, width-corner_size, height-corner_size))

        # Also return the full panel
        slices['full'] = panel

        return slices

    def generate_bronze_button(self, width: int = 48, height: int = 16,
                              state: str = 'normal') -> Image.Image:
        """
        Generate a bronze button with classical 3D effect.

        Args:
            width: Button width
            height: Button height
            state: 'normal', 'hover', 'pressed', or 'disabled'
        """
        button = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(button)

        # Define colors for different states
        if state == 'normal':
            base = self.palette.BRONZE_MID
            light = self.palette.BRONZE_LIGHT
            dark = self.palette.BRONZE_DARK
        elif state == 'hover':
            base = self.palette.BRONZE_LIGHT
            light = self.palette.GOLD
            dark = self.palette.BRONZE_MID
        elif state == 'pressed':
            base = self.palette.BRONZE_DARK
            light = self.palette.BRONZE_MID
            dark = (46, 25, 11)  # Even darker bronze
        else:  # disabled
            base = self.palette.STONE_MID
            light = self.palette.STONE_LIGHT
            dark = self.palette.STONE_DARK

        # Draw main button body
        if state == 'pressed':
            # Pressed state - inset effect
            draw.rectangle([1, 1, width-2, height-2], fill=base)
            # Inverted borders for pressed look
            draw.line([(1, 1), (width-2, 1)], fill=dark, width=1)  # Top (dark)
            draw.line([(1, 1), (1, height-2)], fill=dark, width=1)  # Left (dark)
            draw.line([(2, height-2), (width-2, height-2)], fill=light, width=1)  # Bottom (light)
            draw.line([(width-2, 2), (width-2, height-2)], fill=light, width=1)  # Right (light)
        else:
            # Normal raised effect
            draw.rectangle([1, 1, width-2, height-2], fill=base)
            # 3D borders
            draw.line([(1, 1), (width-2, 1)], fill=light, width=1)  # Top highlight
            draw.line([(1, 1), (1, height-2)], fill=light, width=1)  # Left highlight
            draw.line([(2, height-2), (width-2, height-2)], fill=dark, width=1)  # Bottom shadow
            draw.line([(width-2, 2), (width-2, height-2)], fill=dark, width=1)  # Right shadow

        # Add metallic shine effect (except when pressed)
        if state != 'pressed':
            for x in range(2, width-2, 3):
                draw.point((x, 2), fill=light)

        # Corner rivets for decoration
        rivet_color = dark if state != 'pressed' else light
        draw.point((2, 2), fill=rivet_color)
        draw.point((width-3, 2), fill=rivet_color)
        draw.point((2, height-3), fill=rivet_color)
        draw.point((width-3, height-3), fill=rivet_color)

        return button

    def generate_health_bar(self, width: int = 32, height: int = 4,
                           segments: int = 10, fill_percent: float = 1.0) -> Image.Image:
        """
        Generate a segmented pixel art health bar.

        Args:
            width: Total width of health bar
            height: Height of health bar
            segments: Number of segments
            fill_percent: How full the bar is (0.0 to 1.0)
        """
        bar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bar)

        # Background (empty bar)
        draw.rectangle([0, 0, width-1, height-1], fill=(40, 20, 20), outline=(0, 0, 0))

        # Calculate filled segments
        segment_width = (width - 2) // segments
        filled_segments = int(segments * fill_percent)

        # Determine color based on health percentage
        if fill_percent > 0.66:
            bar_color = (0, 200, 0)  # Green
            highlight = (0, 255, 0)
        elif fill_percent > 0.33:
            bar_color = (200, 200, 0)  # Yellow
            highlight = (255, 255, 0)
        else:
            bar_color = (200, 0, 0)  # Red
            highlight = (255, 0, 0)

        # Draw filled segments
        for i in range(filled_segments):
            x = 1 + i * segment_width
            # Main segment
            draw.rectangle([x, 1, x + segment_width - 2, height-2], fill=bar_color)
            # Highlight on top
            draw.line([(x, 1), (x + segment_width - 2, 1)], fill=highlight, width=1)

        # Add segment dividers
        for i in range(1, segments):
            x = i * segment_width
            draw.line([(x, 0), (x, height-1)], fill=(0, 0, 0), width=1)

        return bar

    def generate_parchment_background(self, width: int = 128, height: int = 64) -> Image.Image:
        """
        Generate a parchment texture background for text displays.
        """
        parchment = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(parchment)

        # Base parchment color
        base_color = (238, 223, 204)  # Light tan
        edge_color = (210, 190, 160)  # Darker edges
        stain_color = (225, 210, 185)  # Age stains

        # Fill with base color
        draw.rectangle([0, 0, width-1, height-1], fill=base_color)

        # Add aged edges
        # Top edge
        for y in range(3):
            alpha = 1.0 - (y / 3.0)
            for x in range(width):
                if (x + y) % 2 == 0:
                    draw.point((x, y), fill=edge_color)

        # Bottom edge
        for y in range(height-3, height):
            for x in range(width):
                if (x + y) % 2 == 0:
                    draw.point((x, y), fill=edge_color)

        # Side edges with torn effect
        import random
        for y in range(height):
            # Left edge
            edge_width = random.randint(2, 4)
            for x in range(edge_width):
                if random.random() > 0.3:
                    draw.point((x, y), fill=edge_color)

            # Right edge
            edge_width = random.randint(2, 4)
            for x in range(width - edge_width, width):
                if random.random() > 0.3:
                    draw.point((x, y), fill=edge_color)

        # Add age stains/texture
        for _ in range(width * height // 200):
            x = random.randint(5, width-6)
            y = random.randint(5, height-6)
            radius = random.randint(2, 4)
            for dx in range(-radius, radius+1):
                for dy in range(-radius, radius+1):
                    if dx*dx + dy*dy <= radius*radius:
                        if 0 <= x+dx < width and 0 <= y+dy < height:
                            if random.random() > 0.5:
                                draw.point((x+dx, y+dy), fill=stain_color)

        return parchment

    def generate_icon_button(self, size: int = 24, icon_type: str = 'sword') -> Image.Image:
        """
        Generate an icon button for actions.

        Args:
            size: Size of the button (square)
            icon_type: Type of icon ('sword', 'shield', 'bow', 'move', 'end_turn')
        """
        button = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(button)

        # Bronze button background
        draw.rectangle([1, 1, size-2, size-2], fill=self.palette.BRONZE_MID)
        # Borders
        draw.line([(1, 1), (size-2, 1)], fill=self.palette.BRONZE_LIGHT, width=1)
        draw.line([(1, 1), (1, size-2)], fill=self.palette.BRONZE_LIGHT, width=1)
        draw.line([(2, size-2), (size-2, size-2)], fill=self.palette.BRONZE_DARK, width=1)
        draw.line([(size-2, 2), (size-2, size-2)], fill=self.palette.BRONZE_DARK, width=1)

        # Draw icon based on type
        icon_color = self.palette.GOLD
        center_x = size // 2
        center_y = size // 2

        if icon_type == 'sword':
            # Simple sword icon
            draw.line([(center_x, 4), (center_x, size-4)], fill=icon_color, width=1)  # Blade
            draw.line([(center_x-2, center_y+2), (center_x+2, center_y+2)], fill=icon_color, width=1)  # Guard
            draw.point((center_x, size-4), fill=self.palette.WHITE)  # Tip highlight

        elif icon_type == 'shield':
            # Shield shape
            points = [
                (center_x, 5),
                (center_x-3, 8),
                (center_x-3, size-7),
                (center_x, size-5),
                (center_x+3, size-7),
                (center_x+3, 8)
            ]
            draw.polygon(points, fill=icon_color, outline=self.palette.BRONZE_DARK)

        elif icon_type == 'bow':
            # Bow icon
            draw.arc([(center_x-4, 5), (center_x+4, size-5)],
                    start=120, end=240, fill=icon_color, width=1)
            draw.line([(center_x-2, 7), (center_x-2, size-7)], fill=self.palette.WHITE, width=1)  # String

        elif icon_type == 'move':
            # Movement arrows
            # Up arrow
            draw.line([(center_x, 5), (center_x, 8)], fill=icon_color, width=1)
            draw.line([(center_x-1, 6), (center_x, 5), (center_x+1, 6)], fill=icon_color)
            # Down arrow
            draw.line([(center_x, size-8), (center_x, size-5)], fill=icon_color, width=1)
            draw.line([(center_x-1, size-6), (center_x, size-5), (center_x+1, size-6)], fill=icon_color)

        elif icon_type == 'end_turn':
            # Hourglass or check mark
            # Check mark
            draw.line([(center_x-3, center_y), (center_x-1, center_y+2)], fill=icon_color, width=2)
            draw.line([(center_x-1, center_y+2), (center_x+3, center_y-2)], fill=icon_color, width=2)

        return button

    def generate_tooltip_background(self, width: int = 96, height: int = 48) -> Image.Image:
        """
        Generate a tooltip background with parchment style and pointer.
        """
        # Add extra height for the pointer
        full_height = height + 6
        tooltip = Image.new('RGBA', (width, full_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(tooltip)

        # Parchment colors
        bg_color = (238, 223, 204, 240)  # Slightly transparent
        border_color = (101, 67, 33)  # Dark brown border

        # Main tooltip body
        draw.rectangle([1, 1, width-2, height-2], fill=bg_color, outline=border_color)

        # Pointer triangle at bottom center
        pointer_x = width // 2
        points = [
            (pointer_x - 4, height - 1),
            (pointer_x + 4, height - 1),
            (pointer_x, height + 5)
        ]
        draw.polygon(points, fill=bg_color, outline=border_color)

        # Inner shadow for depth
        draw.rectangle([2, 2, width-3, height-3], outline=(210, 190, 160))

        return tooltip

    def generate_decorative_corner(self, size: int = 16, style: str = 'greek') -> Image.Image:
        """
        Generate decorative corner elements for panels.

        Args:
            size: Size of the corner piece
            style: 'greek', 'roman', 'celtic'
        """
        corner = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(corner)

        color = self.palette.BRONZE_LIGHT
        accent = self.palette.GOLD

        if style == 'greek':
            # Greek key pattern (simplified)
            # Outer L shape
            draw.line([(2, size-3), (2, 2), (size-3, 2)], fill=color, width=2)
            # Inner L shape
            draw.line([(5, size-6), (5, 5), (size-6, 5)], fill=accent, width=1)
            # Connecting lines
            draw.line([(2, size-3), (5, size-6)], fill=color, width=1)
            draw.line([(size-3, 2), (size-6, 5)], fill=color, width=1)

        elif style == 'roman':
            # Laurel leaf pattern
            for i in range(3):
                x = 3 + i * 4
                y = 3 + i * 4
                # Leaf shape
                draw.ellipse([x, y, x+3, y+5], fill=color)
                draw.line([(x+1, y+2), (x+1, y+4)], fill=accent, width=1)

        elif style == 'celtic':
            # Simple knot pattern
            draw.arc([(2, 2), (size-3, size-3)], start=180, end=270, fill=color, width=2)
            draw.arc([(4, 4), (size-5, size-5)], start=180, end=270, fill=accent, width=1)

        return corner

    def generate_resource_icon(self, resource_type: str = 'gold', size: int = 16) -> Image.Image:
        """
        Generate resource icons for UI displays.

        Args:
            resource_type: 'gold', 'food', 'supplies', 'xp'
            size: Icon size
        """
        icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)

        if resource_type == 'gold':
            # Gold coin
            draw.ellipse([2, 2, size-3, size-3], fill=self.palette.GOLD, outline=self.palette.BRONZE_DARK)
            # Embossed face/symbol
            draw.ellipse([5, 5, size-6, size-6], outline=self.palette.BRONZE_MID)

        elif resource_type == 'food':
            # Wheat/grain
            wheat_color = (218, 165, 32)  # Goldenrod
            # Stalk
            draw.line([(size//2, 3), (size//2, size-3)], fill=wheat_color, width=1)
            # Grains
            for i in range(4):
                y = 4 + i * 2
                draw.ellipse([size//2-2, y, size//2+2, y+1], fill=wheat_color)

        elif resource_type == 'supplies':
            # Crate/box
            box_color = self.palette.WOOD_BROWN
            draw.rectangle([3, 5, size-4, size-3], fill=box_color)
            # Wood grain
            draw.line([(4, 7), (size-5, 7)], fill=self.palette.BRONZE_DARK, width=1)
            draw.line([(4, 10), (size-5, 10)], fill=self.palette.BRONZE_DARK, width=1)

        elif resource_type == 'xp':
            # Star or laurel
            star_color = (255, 255, 0)  # Yellow
            cx, cy = size//2, size//2
            # Simple 4-point star
            draw.polygon([
                (cx, 3), (cx-2, cy), (cx, size-4), (cx+2, cy)
            ], fill=star_color, outline=self.palette.GOLD)

        return icon