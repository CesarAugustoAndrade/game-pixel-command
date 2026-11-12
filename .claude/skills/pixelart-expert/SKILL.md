---
name: pixelart-expert
description: Comprehensive pixel art creation system for retro games using Python. Use when creating pixel art sprites, animations, tilesets, generating procedural pixel art, working with limited color palettes, implementing dithering, pixel-perfect scaling, creating retro game graphics with Pyxel or Pillow, or any pixel art tasks for game development.
---

# Pixel Art Expert Skill

## Overview

Complete pixel art creation and manipulation system for retro-style games. Uses **Pyxel** for integrated retro game engine with built-in pixel art editor, and **Pillow** for programmatic pixel art generation and advanced manipulation.

## Installation

```bash
# Pyxel - Retro game engine with pixel art tools
pip install pyxel

# Pillow - Image manipulation
pip install Pillow

# Optional: For advanced color quantization
pip install scikit-image numpy
```

## Pyxel - Retro Game Engine Approach

### Pyxel Features for Pixel Art

Pyxel is a retro game engine inspired by PICO-8 and TIC-80, designed specifically for pixel art games with simple specifications like displaying only 16 colors and supporting 4 sound channels.

**Key Features:**
- Fixed 16-color palette
- Built-in sprite editor (Pyxel Editor)
- Built-in tilemap editor
- Built-in sound and music editor
- 256x256 sprite bank
- 8 tilemap banks
- Perfect for retro aesthetic

### Basic Pyxel Setup

```python
# basic_pyxel_game.py
import pyxel

class PixelArtGame:
    def __init__(self):
        # Initialize 160x120 window with 16-color palette
        pyxel.init(160, 120, title="Pixel Art Game", fps=60)
        
        # Load resource file (.pyxres)
        # Create with: pyxeleditor
        pyxel.load("assets.pyxres")
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        """Update game logic"""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def draw(self):
        """Draw sprites and graphics"""
        pyxel.cls(0)  # Clear screen with color 0
        
        # Draw sprite from image bank 0
        # blt(x, y, img_bank, u, v, w, h, [colkey])
        pyxel.blt(
            x=50, y=50,           # Position on screen
            img=0,                # Image bank
            u=0, v=0,             # Source position in image bank
            w=16, h=16,           # Size
            colkey=0              # Transparent color
        )

if __name__ == "__main__":
    PixelArtGame()
```

### Creating Assets with Pyxel Editor

```bash
# Launch Pyxel Editor to create sprites
pyxeleditor my_game.pyxres

# Editor controls:
# - Click "Image" tab to draw sprites
# - Click "Tilemap" tab to create levels
# - Click "Sound" tab for sound effects
# - Click "Music" tab for music
```

### Advanced Pyxel Drawing

```python
# advanced_pyxel.py
import pyxel

class PixelArtDemo:
    def __init__(self):
        pyxel.init(256, 256, title="Pixel Art Techniques")
        self.frame = 0
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.frame += 1
    
    def draw(self):
        pyxel.cls(0)
        
        # 1. Pixel-perfect lines
        pyxel.line(10, 10, 100, 10, 7)  # Horizontal white line
        pyxel.line(10, 20, 10, 80, 8)   # Vertical red line
        
        # 2. Rectangles (outline and filled)
        pyxel.rect(20, 30, 40, 40, 9)      # Filled orange rectangle
        pyxel.rectb(70, 30, 40, 40, 10)    # Outlined yellow rectangle
        
        # 3. Circles (outline and filled)
        pyxel.circ(140, 50, 20, 11)        # Filled lime circle
        pyxel.circb(200, 50, 20, 12)       # Outlined cyan circle
        
        # 4. Animated sprite with flip
        # Flip sprite horizontally/vertically for walking animation
        flip_h = (self.frame // 15) % 2
        pyxel.blt(120, 100, 0, 0, 0, 16, 16, colkey=0)
        
        # 5. Tilemap rendering
        # Draw portion of tilemap
        pyxel.bltm(
            x=0, y=150,           # Screen position
            tm=0,                 # Tilemap bank
            u=0, v=0,             # Source position in tilemap
            w=256, h=100,         # Size to draw
            colkey=0              # Transparent color
        )
        
        # 6. Text rendering
        pyxel.text(10, 10, "PIXEL ART!", 7)
        
        # 7. Dithering pattern (manual)
        self.draw_dithered_rect(150, 150, 50, 50)
    
    def draw_dithered_rect(self, x, y, w, h):
        """Draw dithered rectangle for shading effect"""
        for dy in range(h):
            for dx in range(w):
                # Checkerboard dithering pattern
                if (dx + dy) % 2 == 0:
                    pyxel.pset(x + dx, y + dy, 5)  # Dark gray
                else:
                    pyxel.pset(x + dx, y + dy, 6)  # Light gray

if __name__ == "__main__":
    PixelArtDemo()
```

### Pyxel Color Palette

```python
# Pyxel's fixed 16-color palette (default)
PYXEL_PALETTE = {
    0:  (0, 0, 0),         # Black
    1:  (43, 51, 95),      # Navy
    2:  (126, 32, 114),    # Purple
    3:  (25, 149, 156),    # Teal
    4:  (139, 72, 82),     # Maroon
    5:  (57, 92, 152),     # Dark Blue
    6:  (169, 193, 255),   # Light Blue
    7:  (238, 238, 238),   # White
    8:  (212, 24, 108),    # Red
    9:  (211, 132, 65),    # Orange
    10: (233, 195, 91),    # Yellow
    11: (112, 198, 169),   # Lime
    12: (118, 150, 222),   # Cyan
    13: (163, 163, 163),   # Gray
    14: (255, 151, 152),   # Pink
    15: (237, 199, 176),   # Peach
}

# You can customize the palette
def set_custom_palette():
    """Set custom 16-color palette"""
    # NES-style palette
    nes_palette = [
        0x000000, 0x1c1c1c, 0x373737, 0x545454,
        0x707070, 0x8c8c8c, 0xa8a8a8, 0xc4c4c4,
        0xe0e0e0, 0xfcfcfc, 0x2078fc, 0x3c9cfc,
        0x58b8fc, 0x74d4fc, 0x90f0fc, 0xacfcfc
    ]
    
    for i, color in enumerate(nes_palette):
        pyxel.colors[i] = color
```

## Pillow - Programmatic Pixel Art Generation

### Creating Pixel Art from Scratch

```python
# pixel_art_generator.py
from PIL import Image, ImageDraw
import random

class PixelArtGenerator:
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.image = Image.new('RGB', (width, height), color='black')
        self.pixels = self.image.load()
    
    def set_pixel(self, x, y, color):
        """Set individual pixel color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[x, y] = color
    
    def get_pixel(self, x, y):
        """Get individual pixel color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[x, y]
        return None
    
    def scale_nearest_neighbor(self, scale_factor):
        """Pixel-perfect scaling (no blur)"""
        new_size = (self.width * scale_factor, self.height * scale_factor)
        return self.image.resize(new_size, Image.NEAREST)
    
    def save(self, filename, scale=1):
        """Save pixel art (optionally scaled)"""
        if scale > 1:
            scaled = self.scale_nearest_neighbor(scale)
            scaled.save(filename)
        else:
            self.image.save(filename)
    
    def quantize_colors(self, num_colors=16):
        """Reduce to limited color palette"""
        return self.image.quantize(colors=num_colors, method=2)

# Example: Generate random sprite
def generate_random_sprite(size=16, symmetry=True):
    """Generate random symmetric sprite (like Space Invaders)"""
    gen = PixelArtGenerator(size, size)
    
    # Define limited palette
    palette = [
        (0, 0, 0),         # Black (transparent)
        (255, 255, 255),   # White
        (255, 0, 0),       # Red
        (0, 255, 0),       # Green
        (0, 0, 255),       # Blue
    ]
    
    # Generate half, then mirror for symmetry
    half_width = size // 2
    
    for y in range(size):
        for x in range(half_width):
            if random.random() > 0.5:
                color = random.choice(palette[1:])  # Skip black
                gen.set_pixel(x, y, color)
                
                if symmetry:
                    # Mirror to other side
                    gen.set_pixel(size - 1 - x, y, color)
    
    return gen

# Usage
sprite = generate_random_sprite(16, symmetry=True)
sprite.save("random_sprite.png", scale=10)  # Save at 10x size
```

### Dithering Algorithms

```python
# dithering.py
from PIL import Image
import numpy as np

class DitheringEngine:
    """Implement various dithering algorithms for pixel art"""
    
    @staticmethod
    def floyd_steinberg(image, palette):
        """
        Floyd-Steinberg dithering - diffuses quantization error to neighbors
        Produces smooth gradients with limited colors
        """
        img_array = np.array(image, dtype=float)
        height, width = img_array.shape[:2]
        
        for y in range(height):
            for x in range(width):
                old_pixel = img_array[y, x].copy()
                
                # Find nearest color in palette
                new_pixel = DitheringEngine._find_nearest_color(old_pixel, palette)
                img_array[y, x] = new_pixel
                
                # Calculate error
                error = old_pixel - new_pixel
                
                # Distribute error to neighbors (Floyd-Steinberg matrix)
                if x + 1 < width:
                    img_array[y, x + 1] += error * 7/16
                if y + 1 < height:
                    if x > 0:
                        img_array[y + 1, x - 1] += error * 3/16
                    img_array[y + 1, x] += error * 5/16
                    if x + 1 < width:
                        img_array[y + 1, x + 1] += error * 1/16
        
        return Image.fromarray(np.uint8(img_array))
    
    @staticmethod
    def ordered_dithering(image, palette, matrix_size=4):
        """
        Ordered (Bayer) dithering - uses threshold matrix
        Produces characteristic crosshatch pattern
        """
        # Bayer matrix 4x4
        bayer_matrix = np.array([
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]) / 16
        
        img_array = np.array(image, dtype=float) / 255.0
        height, width = img_array.shape[:2]
        
        for y in range(height):
            for x in range(width):
                threshold = bayer_matrix[y % matrix_size, x % matrix_size]
                old_pixel = img_array[y, x]
                
                # Apply threshold
                dithered = old_pixel + (threshold - 0.5) / len(palette)
                new_pixel = DitheringEngine._find_nearest_color(
                    dithered * 255, palette
                )
                img_array[y, x] = new_pixel / 255.0
        
        return Image.fromarray(np.uint8(img_array * 255))
    
    @staticmethod
    def _find_nearest_color(pixel, palette):
        """Find closest color in palette to given pixel"""
        min_distance = float('inf')
        nearest = palette[0]
        
        for color in palette:
            distance = np.sum((pixel - np.array(color)) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest = color
        
        return np.array(nearest)

# Usage
def apply_retro_dithering(input_image, output_image):
    """Convert image to retro pixel art with dithering"""
    img = Image.open(input_image)
    
    # Resize to pixel art size
    small = img.resize((64, 64), Image.NEAREST)
    
    # Define retro palette (e.g., Game Boy palette)
    gameboy_palette = [
        (15, 56, 15),      # Dark green
        (48, 98, 48),      # Medium-dark green
        (139, 172, 15),    # Light green
        (155, 188, 15),    # Lightest green
    ]
    
    # Apply Floyd-Steinberg dithering
    dithered = DitheringEngine.floyd_steinberg(small, gameboy_palette)
    
    # Scale up with nearest neighbor (pixel-perfect)
    final = dithered.resize((640, 640), Image.NEAREST)
    final.save(output_image)

# Example usage
apply_retro_dithering("photo.jpg", "pixel_art.png")
```

### Sprite Sheet Generation

```python
# spritesheet_generator.py
from PIL import Image
import math

class SpriteSheetGenerator:
    def __init__(self, sprite_width, sprite_height):
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprites = []
    
    def add_sprite(self, image):
        """Add sprite to sheet"""
        if image.size != (self.sprite_width, self.sprite_height):
            image = image.resize(
                (self.sprite_width, self.sprite_height),
                Image.NEAREST
            )
        self.sprites.append(image)
    
    def generate_sheet(self, sprites_per_row=8, padding=0):
        """Generate sprite sheet from collected sprites"""
        if not self.sprites:
            return None
        
        num_sprites = len(self.sprites)
        rows = math.ceil(num_sprites / sprites_per_row)
        
        # Calculate sheet dimensions
        sheet_width = (self.sprite_width + padding) * sprites_per_row
        sheet_height = (self.sprite_height + padding) * rows
        
        # Create blank sheet
        sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        
        # Paste sprites
        for i, sprite in enumerate(self.sprites):
            row = i // sprites_per_row
            col = i % sprites_per_row
            
            x = col * (self.sprite_width + padding)
            y = row * (self.sprite_height + padding)
            
            sheet.paste(sprite, (x, y))
        
        return sheet
    
    def save_sheet(self, filename, sprites_per_row=8, padding=0):
        """Generate and save sprite sheet"""
        sheet = self.generate_sheet(sprites_per_row, padding)
        if sheet:
            sheet.save(filename)
    
    def generate_animation_frames(self, num_frames, animation_func):
        """Generate animation frames using custom function"""
        for frame in range(num_frames):
            sprite = animation_func(frame, num_frames)
            self.add_sprite(sprite)

# Example: Create walking animation
def create_walk_cycle():
    """Generate simple walk cycle animation"""
    sheet = SpriteSheetGenerator(16, 16)
    
    def draw_walk_frame(frame, total_frames):
        """Draw a single walk frame"""
        img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Simple stick figure animation
        progress = frame / total_frames
        
        # Body
        draw.rectangle([6, 4, 9, 12], fill=(255, 255, 255))
        
        # Legs (animate)
        left_leg_y = 12 + int(2 * math.sin(progress * 2 * math.pi))
        right_leg_y = 12 - int(2 * math.sin(progress * 2 * math.pi))
        
        draw.rectangle([6, 12, 7, left_leg_y], fill=(255, 255, 255))
        draw.rectangle([8, 12, 9, right_leg_y], fill=(255, 255, 255))
        
        return img
    
    sheet.generate_animation_frames(8, draw_walk_frame)
    sheet.save_sheet("walk_cycle.png", sprites_per_row=8)

create_walk_cycle()
```

### Procedural Pixel Art Generation

```python
# procedural_pixelart.py
import random
from PIL import Image

class ProceduralPixelArt:
    """Generate pixel art procedurally"""
    
    @staticmethod
    def generate_weapon(size=16, weapon_type="sword"):
        """Generate pixel art weapon"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        pixels = img.load()
        
        if weapon_type == "sword":
            # Blade colors
            blade = (192, 192, 192)  # Silver
            edge = (255, 255, 255)   # White highlight
            handle = (139, 69, 19)   # Brown
            
            # Draw blade
            for y in range(2, 12):
                pixels[size//2, y] = blade
                pixels[size//2 - 1, y] = edge
            
            # Draw cross-guard
            for x in range(size//2 - 2, size//2 + 3):
                pixels[x, 12] = handle
            
            # Draw handle
            for y in range(13, size - 1):
                pixels[size//2, y] = handle
        
        elif weapon_type == "axe":
            # Implement axe generation
            pass
        
        return img
    
    @staticmethod
    def generate_character(size=16, style="human"):
        """Generate random character sprite"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        pixels = img.load()
        
        # Random skin tone
        skin_tones = [
            (255, 220, 177),  # Light
            (210, 180, 140),  # Medium
            (139, 90, 43),    # Dark
        ]
        skin = random.choice(skin_tones)
        
        # Random hair color
        hair_colors = [
            (0, 0, 0),        # Black
            (139, 69, 19),    # Brown
            (255, 255, 0),    # Blonde
            (255, 0, 0),      # Red
        ]
        hair = random.choice(hair_colors)
        
        # Draw head
        for y in range(3, 8):
            for x in range(5, 11):
                pixels[x, y] = skin
        
        # Draw hair
        for x in range(5, 11):
            pixels[x, 3] = hair
            pixels[x, 4] = hair
        
        # Draw eyes
        pixels[6, 5] = (0, 0, 0)
        pixels[9, 5] = (0, 0, 0)
        
        # Draw body (random shirt color)
        shirt_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        
        for y in range(8, 12):
            for x in range(6, 10):
                pixels[x, y] = shirt_color
        
        # Draw legs
        pants = (0, 0, 139)  # Blue
        for y in range(12, 16):
            pixels[6, y] = pants
            pixels[9, y] = pants
        
        return img
    
    @staticmethod
    def generate_tileset(tile_size=16, num_tiles=16):
        """Generate procedural tileset"""
        sheet = SpriteSheetGenerator(tile_size, tile_size)
        
        # Grass variations
        for i in range(4):
            grass = ProceduralPixelArt._generate_grass_tile(tile_size)
            sheet.add_sprite(grass)
        
        # Stone variations
        for i in range(4):
            stone = ProceduralPixelArt._generate_stone_tile(tile_size)
            sheet.add_sprite(stone)
        
        # Water variations
        for i in range(4):
            water = ProceduralPixelArt._generate_water_tile(tile_size)
            sheet.add_sprite(water)
        
        return sheet.generate_sheet(sprites_per_row=4)
    
    @staticmethod
    def _generate_grass_tile(size):
        """Generate grass tile with variation"""
        img = Image.new('RGB', (size, size), (34, 139, 34))  # Base green
        pixels = img.load()
        
        # Add random grass blades
        for _ in range(random.randint(5, 15)):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            pixels[x, y] = (0, 255, 0)  # Bright green
        
        return img
    
    @staticmethod
    def _generate_stone_tile(size):
        """Generate stone tile"""
        base_gray = random.randint(100, 140)
        img = Image.new('RGB', (size, size), (base_gray, base_gray, base_gray))
        pixels = img.load()
        
        # Add texture
        for _ in range(random.randint(10, 20)):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            variation = random.randint(-20, 20)
            color = max(0, min(255, base_gray + variation))
            pixels[x, y] = (color, color, color)
        
        return img
    
    @staticmethod
    def _generate_water_tile(size):
        """Generate water tile"""
        img = Image.new('RGB', (size, size), (0, 119, 190))  # Base blue
        pixels = img.load()
        
        # Add wave highlights
        for _ in range(random.randint(3, 8)):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            pixels[x, y] = (100, 149, 237)  # Light blue
        
        return img
```

### Color Palette Management

```python
# palette_manager.py

class PaletteManager:
    """Manage and apply color palettes"""
    
    # Famous retro palettes
    PALETTES = {
        'gameboy': [
            (15, 56, 15),
            (48, 98, 48),
            (139, 172, 15),
            (155, 188, 15),
        ],
        'nes': [
            (0, 0, 0), (252, 252, 252), (168, 0, 32), (228, 92, 16),
            (172, 124, 0), (0, 184, 0), (0, 168, 68), (0, 136, 136),
            (0, 88, 248), (60, 0, 252), (168, 0, 252), (228, 0, 228),
            (248, 120, 248), (252, 160, 68), (252, 204, 168), (252, 224, 168),
        ],
        'cga': [
            (0, 0, 0), (0, 0, 170), (0, 170, 0), (0, 170, 170),
            (170, 0, 0), (170, 0, 170), (170, 85, 0), (170, 170, 170),
            (85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255),
            (255, 85, 85), (255, 85, 255), (255, 255, 85), (255, 255, 255),
        ],
        'pico8': [
            (0, 0, 0), (29, 43, 83), (126, 37, 83), (0, 135, 81),
            (171, 82, 54), (95, 87, 79), (194, 195, 199), (255, 241, 232),
            (255, 0, 77), (255, 163, 0), (255, 236, 39), (0, 228, 54),
            (41, 173, 255), (131, 118, 156), (255, 119, 168), (255, 204, 170),
        ],
    }
    
    @staticmethod
    def apply_palette(image, palette_name):
        """Convert image to use specific palette"""
        palette = PaletteManager.PALETTES.get(palette_name)
        if not palette:
            return image
        
        return DitheringEngine.floyd_steinberg(image, palette)
    
    @staticmethod
    def extract_palette(image, num_colors=16):
        """Extract dominant colors from image"""
        quantized = image.quantize(colors=num_colors, method=2)
        palette = quantized.getpalette()
        
        # Convert to list of RGB tuples
        colors = []
        for i in range(0, num_colors * 3, 3):
            colors.append(tuple(palette[i:i+3]))
        
        return colors
    
    @staticmethod
    def create_gradient_palette(color1, color2, steps=16):
        """Create smooth gradient palette between two colors"""
        palette = []
        for i in range(steps):
            t = i / (steps - 1)
            r = int(color1[0] * (1 - t) + color2[0] * t)
            g = int(color1[1] * (1 - t) + color2[1] * t)
            b = int(color1[2] * (1 - t) + color2[2] * t)
            palette.append((r, g, b))
        return palette
```

## Best Practices

### 1. Pixel Art Principles

- **Pixel-Perfect Scaling**: Always use nearest-neighbor scaling (never bilinear/bicubic)
- **Limited Palette**: Stick to 8-16 colors for authentic retro look
- **Dithering**: Use for shading with limited colors
- **Anti-Aliasing**: Avoid it! Embrace the crisp pixel edges
- **Readability**: Ensure sprites are clear at small sizes

### 2. Animation Tips

```python
# Good animation practice
class AnimatedSprite:
    def __init__(self, frames, fps=10):
        self.frames = frames
        self.fps = fps
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 1.0 / fps
    
    def update(self, dt):
        """Update animation"""
        self.frame_time += dt
        
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self):
        return self.frames[self.current_frame]
```

### 3. Performance Optimization

```python
# Cache scaled sprites
class SpriteCache:
    def __init__(self):
        self.cache = {}
    
    def get_scaled_sprite(self, sprite, scale):
        """Get cached scaled sprite or create new one"""
        key = (id(sprite), scale)
        
        if key not in self.cache:
            self.cache[key] = sprite.resize(
                (sprite.width * scale, sprite.height * scale),
                Image.NEAREST
            )
        
        return self.cache[key]
```

### 4. Tileset Organization

```
Standard tileset layout (16x16 tiles):
Row 0: Ground tiles (grass, dirt, stone)
Row 1: Wall tiles (all variations)
Row 2: Water tiles (animated frames)
Row 3: Decorative objects
Row 4-7: Character sprites (walk cycles)
```

## Common Workflows

### Workflow 1: Creating Game Assets with Pyxel

```bash
# 1. Create new resource file
pyxeleditor my_game.pyxres

# 2. Draw sprites in Image Bank
# 3. Create tilemap in Tilemap Bank
# 4. Add sounds/music
# 5. Save and load in game code
```

### Workflow 2: Converting Photos to Pixel Art

```python
def photo_to_pixelart(input_path, output_path, size=64, palette='gameboy'):
    """Complete pipeline: photo -> pixel art"""
    # 1. Load and resize
    img = Image.open(input_path)
    img = img.resize((size, size), Image.LANCZOS)
    
    # 2. Apply palette
    img = PaletteManager.apply_palette(img, palette)
    
    # 3. Scale up (pixel-perfect)
    final = img.resize((size * 8, size * 8), Image.NEAREST)
    
    # 4. Save
    final.save(output_path)
```

### Workflow 3: Procedural Asset Generation

```python
# Generate complete asset pack
def generate_asset_pack(output_dir):
    """Generate complete pixel art asset pack"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Characters
    for i in range(10):
        char = ProceduralPixelArt.generate_character(16)
        char.save(f"{output_dir}/character_{i}.png")
    
    # Weapons
    for weapon in ['sword', 'axe', 'bow']:
        weapon_img = ProceduralPixelArt.generate_weapon(16, weapon)
        weapon_img.save(f"{output_dir}/{weapon}.png")
    
    # Tileset
    tileset = ProceduralPixelArt.generate_tileset(16, 16)
    tileset.save(f"{output_dir}/tileset.png")

generate_asset_pack("assets/")
```

## Tools Integration

### Export for Game Engines

```python
def export_for_unity(spritesheet, output_path, sprite_size=16):
    """Export with metadata for Unity"""
    import json
    
    # Save spritesheet
    spritesheet.save(output_path)
    
    # Generate metadata
    width, height = spritesheet.size
    cols = width // sprite_size
    rows = height // sprite_size
    
    metadata = {
        'sprite_size': sprite_size,
        'columns': cols,
        'rows': rows,
        'sprites': []
    }
    
    for row in range(rows):
        for col in range(cols):
            metadata['sprites'].append({
                'name': f'sprite_{row}_{col}',
                'x': col * sprite_size,
                'y': row * sprite_size,
                'width': sprite_size,
                'height': sprite_size
            })
    
    # Save metadata
    with open(output_path.replace('.png', '.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
```

## Conclusion

This skill provides complete pixel art capabilities using Python. Pyxel excels for integrated retro game development with its built-in editor and 16-color palette restrictions perfect for authentic retro aesthetics, while Pillow enables programmatic generation and advanced manipulation. Combine both approaches for maximum flexibility in creating pixel art for games.
