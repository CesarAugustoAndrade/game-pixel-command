"""
Generate all UI assets for the Classical Army Roguelike.

This script creates pixel art UI components including:
- Stone panels with 9-slice borders
- Bronze buttons in various states
- Health bars and status indicators
- Icons for actions and resources
- Decorative elements
"""

import os
from src.art.ui_components import UIComponentGenerator
from PIL import Image

def ensure_ui_directories():
    """Ensure UI asset directories exist."""
    directories = [
        'assets/sprites/ui/panels',
        'assets/sprites/ui/buttons',
        'assets/sprites/ui/bars',
        'assets/sprites/ui/icons',
        'assets/sprites/ui/decorative',
        'assets/sprites/ui/tooltips',
    ]

    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Ensured directory: {dir_path}")

def generate_panels(generator):
    """Generate various panel types."""
    print("\nGenerating panels...")

    # Stone panels of different sizes
    panel_sizes = [
        (32, 32, 'small'),
        (64, 64, 'medium'),
        (128, 64, 'wide'),
        (256, 128, 'large'),
        (320, 240, 'dialog'),
    ]

    for width, height, name in panel_sizes:
        print(f"  - Generating {name} stone panel ({width}x{height})")
        panel_slices = generator.generate_stone_panel(width, height)

        # Save the full panel
        panel_slices['full'].save(f'assets/sprites/ui/panels/stone_panel_{name}.png', 'PNG')

        # Save 9-slice components for the medium one (reusable)
        if name == 'medium':
            for slice_name, slice_img in panel_slices.items():
                if slice_name != 'full':
                    slice_img.save(f'assets/sprites/ui/panels/stone_panel_9slice_{slice_name}.png', 'PNG')

    # Generate parchment backgrounds
    parchment_sizes = [
        (128, 64, 'tooltip'),
        (256, 128, 'dialog'),
        (320, 48, 'banner'),
    ]

    for width, height, name in parchment_sizes:
        print(f"  - Generating {name} parchment ({width}x{height})")
        parchment = generator.generate_parchment_background(width, height)
        parchment.save(f'assets/sprites/ui/panels/parchment_{name}.png', 'PNG')

def generate_buttons(generator):
    """Generate button sprites in different states."""
    print("\nGenerating buttons...")

    button_sizes = [
        (48, 16, 'small'),
        (96, 24, 'medium'),
        (128, 32, 'large'),
    ]

    states = ['normal', 'hover', 'pressed', 'disabled']

    for width, height, size_name in button_sizes:
        for state in states:
            print(f"  - Generating {size_name} button ({state})")
            button = generator.generate_bronze_button(width, height, state)
            button.save(f'assets/sprites/ui/buttons/bronze_button_{size_name}_{state}.png', 'PNG')

    # Generate icon buttons
    icon_types = ['sword', 'shield', 'bow', 'move', 'end_turn']

    for icon_type in icon_types:
        print(f"  - Generating {icon_type} icon button")
        icon_button = generator.generate_icon_button(24, icon_type)
        icon_button.save(f'assets/sprites/ui/buttons/icon_button_{icon_type}.png', 'PNG')

def generate_bars(generator):
    """Generate health bars and other status bars."""
    print("\nGenerating bars...")

    # Health bars at different fill levels
    fill_levels = [
        (1.0, 'full'),
        (0.75, '75'),
        (0.5, '50'),
        (0.25, '25'),
        (0.0, 'empty'),
    ]

    bar_sizes = [
        (32, 4, 'small', 8),
        (48, 6, 'medium', 10),
        (64, 8, 'large', 12),
    ]

    for width, height, size_name, segments in bar_sizes:
        for fill_percent, fill_name in fill_levels:
            print(f"  - Generating {size_name} health bar ({fill_name})")
            health_bar = generator.generate_health_bar(width, height, segments, fill_percent)
            health_bar.save(f'assets/sprites/ui/bars/health_bar_{size_name}_{fill_name}.png', 'PNG')

    # Also create a single template bar that can be dynamically filled
    print("  - Generating health bar template")
    template_bar = generator.generate_health_bar(48, 6, 10, 0.0)
    template_bar.save('assets/sprites/ui/bars/health_bar_template.png', 'PNG')

def generate_icons(generator):
    """Generate resource and action icons."""
    print("\nGenerating icons...")

    # Resource icons
    resources = ['gold', 'food', 'supplies', 'xp']

    for resource in resources:
        print(f"  - Generating {resource} icon")
        icon = generator.generate_resource_icon(resource, 16)
        icon.save(f'assets/sprites/ui/icons/resource_{resource}.png', 'PNG')

        # Also create larger versions
        icon_large = generator.generate_resource_icon(resource, 32)
        icon_large.save(f'assets/sprites/ui/icons/resource_{resource}_large.png', 'PNG')

def generate_decorative(generator):
    """Generate decorative elements."""
    print("\nGenerating decorative elements...")

    # Corner decorations
    styles = ['greek', 'roman', 'celtic']
    sizes = [16, 24, 32]

    for style in styles:
        for size in sizes:
            print(f"  - Generating {style} corner (size {size})")
            corner = generator.generate_decorative_corner(size, style)
            corner.save(f'assets/sprites/ui/decorative/corner_{style}_{size}.png', 'PNG')

    # Tooltip backgrounds
    tooltip_sizes = [
        (96, 48, 'small'),
        (128, 64, 'medium'),
        (192, 96, 'large'),
    ]

    for width, height, name in tooltip_sizes:
        print(f"  - Generating {name} tooltip background")
        tooltip = generator.generate_tooltip_background(width, height)
        tooltip.save(f'assets/sprites/ui/tooltips/tooltip_{name}.png', 'PNG')

def create_ui_spritesheet(generator):
    """Create a master UI spritesheet."""
    print("\nCreating UI spritesheet...")

    sprites = []

    # Collect various UI elements
    # Small buttons
    for state in ['normal', 'hover', 'pressed', 'disabled']:
        button = generator.generate_bronze_button(48, 16, state)
        sprites.append(button)

    # Icon buttons
    for icon_type in ['sword', 'shield', 'bow', 'move', 'end_turn']:
        icon = generator.generate_icon_button(24, icon_type)
        sprites.append(icon)

    # Resource icons
    for resource in ['gold', 'food', 'supplies', 'xp']:
        icon = generator.generate_resource_icon(resource, 16)
        sprites.append(icon)

    # Health bars
    for fill in [1.0, 0.75, 0.5, 0.25, 0.0]:
        bar = generator.generate_health_bar(32, 4, 8, fill)
        sprites.append(bar)

    if sprites:
        # Arrange in a grid
        cols = 8
        rows = (len(sprites) + cols - 1) // cols

        # Find max dimensions
        max_width = max(s.width for s in sprites)
        max_height = max(s.height for s in sprites)

        # Add padding
        cell_width = max_width + 4
        cell_height = max_height + 4

        # Create spritesheet
        sheet_width = cols * cell_width
        sheet_height = rows * cell_height
        sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))

        # Place sprites
        for i, sprite in enumerate(sprites):
            col = i % cols
            row = i // cols
            x = col * cell_width + (cell_width - sprite.width) // 2
            y = row * cell_height + (cell_height - sprite.height) // 2
            sheet.paste(sprite, (x, y))

        sheet.save('assets/sprites/ui/ui_spritesheet.png', 'PNG')
        print(f"  Created UI spritesheet with {len(sprites)} elements")

def main():
    """Main UI asset generation function."""
    print("="*50)
    print("Classical Army Roguelike - UI Asset Generation")
    print("="*50)

    # Ensure directories exist
    ensure_ui_directories()

    # Initialize generator
    generator = UIComponentGenerator()

    # Generate all UI assets
    generate_panels(generator)
    generate_buttons(generator)
    generate_bars(generator)
    generate_icons(generator)
    generate_decorative(generator)
    create_ui_spritesheet(generator)

    print("\n" + "="*50)
    print("UI asset generation complete!")
    print("All UI components have been saved to assets/sprites/ui/")
    print("="*50)

    # Print summary
    print("\nGenerated assets summary:")
    print("  - Stone panels (5 sizes + 9-slice components)")
    print("  - Parchment backgrounds (3 types)")
    print("  - Bronze buttons (3 sizes × 4 states)")
    print("  - Icon buttons (5 action types)")
    print("  - Health bars (3 sizes × 5 fill levels)")
    print("  - Resource icons (4 types × 2 sizes)")
    print("  - Decorative corners (3 styles × 3 sizes)")
    print("  - Tooltip backgrounds (3 sizes)")
    print("  - Master UI spritesheet")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\nYou can now use these UI assets in the game!")
    else:
        print("\nUI asset generation encountered errors.")