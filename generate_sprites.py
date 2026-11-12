"""
Sprite Generation Script for Classical Army Roguelike

This script generates all pixel art sprites for units and terrain tiles
and saves them to the appropriate asset directories.
"""

import os
from src.art.sprite_generator import SpriteGenerator
from PIL import Image

def ensure_directories():
    """Ensure all required asset directories exist."""
    directories = [
        'assets/sprites/units',
        'assets/sprites/units/greek',
        'assets/sprites/units/roman',
        'assets/sprites/units/persian',
        'assets/sprites/units/carthage',
        'assets/sprites/terrain',
        'assets/sprites/ui',
    ]

    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Ensured directory: {dir_path}")

def generate_faction_units(generator, faction_name):
    """Generate all unit sprites for a specific faction."""
    print(f"\nGenerating {faction_name.capitalize()} faction units...")

    # Define unit types for each faction
    faction_units = {
        'greek': [
            ('hoplite', 'Greek heavy infantry with round shield and spear'),
            ('archer', 'Greek light archer'),
            ('cavalry', 'Greek cavalry unit'),
        ],
        'roman': [
            ('legionary', 'Roman heavy infantry with rectangular shield'),
            ('archer', 'Roman auxiliary archer'),
            ('cavalry', 'Roman cavalry (equites)'),
        ],
        'persian': [
            ('immortal', 'Elite Persian guard with scale armor'),
            ('archer', 'Persian archer with composite bow'),
            ('cavalry', 'Persian heavy cavalry'),
        ],
        'carthage': [
            ('sacred_band', 'Elite Carthaginian heavy infantry'),
            ('archer', 'Carthaginian archer'),
            ('cavalry', 'Carthaginian cavalry'),
        ],
    }

    sprites = []
    units = faction_units.get(faction_name, [])

    for unit_type, description in units:
        print(f"  - Generating {unit_type}: {description}")
        sprite = generator.generate_unit_sprite(unit_type, faction_name)

        # Save individual sprite
        filename = f"assets/sprites/units/{faction_name}/{unit_type}.png"
        sprite.save(filename, 'PNG')
        sprites.append(sprite)

    # Create faction sprite sheet
    if sprites:
        sheet = generator.create_sprite_sheet(sprites, columns=3)
        sheet_filename = f"assets/sprites/units/{faction_name}_units.png"
        sheet.save(sheet_filename, 'PNG')
        print(f"  Saved sprite sheet: {sheet_filename}")

    return sprites

def generate_terrain_tiles(generator):
    """Generate all terrain tile sprites."""
    print("\nGenerating terrain tiles...")

    terrain_types = [
        ('grass', 'Grassland terrain'),
        ('water', 'Water terrain with waves'),
        ('sand', 'Desert sand terrain'),
        ('mountain', 'Mountain terrain'),
        ('forest', 'Forest terrain with trees'),
    ]

    sprites = []

    for terrain_type, description in terrain_types:
        print(f"  - Generating {terrain_type}: {description}")

        # Generate 3 variations of each terrain type for variety
        for i in range(3):
            sprite = generator.generate_terrain_tile(terrain_type)
            filename = f"assets/sprites/terrain/{terrain_type}_{i}.png"
            sprite.save(filename, 'PNG')
            sprites.append(sprite)

    # Create terrain sprite sheet
    sheet = generator.create_sprite_sheet(sprites, columns=5)
    sheet_filename = "assets/sprites/terrain/terrain_tiles.png"
    sheet.save(sheet_filename, 'PNG')
    print(f"  Saved terrain sprite sheet: {sheet_filename}")

    return sprites

def generate_ui_elements(generator):
    """Generate UI element sprites."""
    print("\nGenerating UI elements...")

    # Create some basic UI elements
    ui_sprites = []

    # Create a simple button background (stone style)
    button_bg = Image.new('RGBA', (32, 16), (120, 108, 96, 255))  # Stone color
    button_bg.save("assets/sprites/ui/button_stone.png", 'PNG')
    print("  - Generated stone button background")

    # Create a panel background
    panel_bg = Image.new('RGBA', (64, 64), (73, 65, 58, 255))  # Dark stone
    panel_bg.save("assets/sprites/ui/panel_stone.png", 'PNG')
    print("  - Generated stone panel background")

    return ui_sprites

def create_master_sprite_sheet(generator):
    """Create a master sprite sheet with all sprites."""
    print("\nCreating master sprite sheet...")

    all_sprites = []

    # Collect all faction units
    for faction in ['greek', 'roman', 'persian', 'carthage']:
        for unit_type in ['hoplite', 'legionary', 'immortal', 'sacred_band', 'archer', 'cavalry']:
            try:
                sprite = generator.generate_unit_sprite(unit_type, faction)
                all_sprites.append(sprite)
            except:
                pass  # Skip if unit type doesn't exist for faction

    # Add terrain tiles
    for terrain_type in ['grass', 'water', 'sand', 'mountain', 'forest']:
        sprite = generator.generate_terrain_tile(terrain_type)
        all_sprites.append(sprite)

    # Create and save master sheet
    if all_sprites:
        master_sheet = generator.create_sprite_sheet(all_sprites, columns=8)
        master_sheet.save("assets/sprites/master_spritesheet.png", 'PNG')
        print(f"  Created master sprite sheet with {len(all_sprites)} sprites")

    return all_sprites

def main():
    """Main sprite generation function."""
    print("="*50)
    print("Classical Army Roguelike - Sprite Generation")
    print("="*50)

    # Ensure directories exist
    ensure_directories()

    # Initialize sprite generator
    generator = SpriteGenerator()

    # Generate all faction units
    factions = ['greek', 'roman', 'persian', 'carthage']
    for faction in factions:
        generate_faction_units(generator, faction)

    # Generate terrain tiles
    generate_terrain_tiles(generator)

    # Generate UI elements
    generate_ui_elements(generator)

    # Create master sprite sheet
    create_master_sprite_sheet(generator)

    print("\n" + "="*50)
    print("Sprite generation complete!")
    print("All sprites have been saved to the assets/sprites/ directory")
    print("="*50)

    # Print summary
    print("\nGenerated assets summary:")
    print("  - 4 faction sprite sets (Greek, Roman, Persian, Carthage)")
    print("  - 3 unit types per faction (infantry, archer, cavalry)")
    print("  - 5 terrain types with 3 variations each")
    print("  - Basic UI elements")
    print("  - Master sprite sheet with all sprites")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\nYou can now run 'python main.py' to see the sprites in action!")
    else:
        print("\nSprite generation encountered errors. Please check the output above.")