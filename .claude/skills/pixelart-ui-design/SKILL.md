---
name: pixelart-ui-design
description: Specialized UI/UX design for pixel art games, especially classical era strategy games. Use when designing pixel-perfect interfaces, creating retro-style HUDs, implementing 8/16-bit UI elements, designing menus with limited color palettes, or creating authentic retro game interfaces with modern usability.
---

# Pixel Art UI Design Skill

## Overview

Complete guide for designing user interfaces in pixel art style for classical strategy games. Combines retro aesthetic authenticity with modern UX principles, using pygame-gui themed for pixel art and custom rendering techniques.

## Core Principles for Pixel Art UI

### 1. Pixel-Perfect Alignment

Every UI element must align to the pixel grid:

```python
# pixel_perfect.py

class PixelPerfectUI:
    """Ensure all UI elements are pixel-aligned"""
    
    @staticmethod
    def snap_to_grid(position, grid_size=8):
        """Snap position to nearest grid point"""
        x = (position[0] // grid_size) * grid_size
        y = (position[1] // grid_size) * grid_size
        return (x, y)
    
    @staticmethod
    def create_9slice_border(size, border_width=8):
        """
        Create 9-slice scalable border for UI panels
        9-slice allows scaling without distorting corners
        
        Layout:
        [TL][T][TR]
        [L ][C][R ]
        [BL][B][BR]
        """
        surface = pygame.Surface(size)
        
        # Draw corners (never scaled)
        # Top-left corner
        pygame.draw.rect(surface, BORDER_DARK, (0, 0, border_width, border_width))
        
        # Top-right corner
        pygame.draw.rect(surface, BORDER_DARK, 
                        (size[0]-border_width, 0, border_width, border_width))
        
        # Bottom-left corner
        pygame.draw.rect(surface, BORDER_DARK,
                        (0, size[1]-border_width, border_width, border_width))
        
        # Bottom-right corner
        pygame.draw.rect(surface, BORDER_DARK,
                        (size[0]-border_width, size[1]-border_width, 
                         border_width, border_width))
        
        # Draw edges (tiled)
        # Top edge
        for x in range(border_width, size[0]-border_width, border_width):
            pygame.draw.rect(surface, BORDER_MED, (x, 0, border_width, border_width))
        
        # Similar for other edges...
        
        return surface
```

### 2. Limited Color Palette for UI

Stick to complementary colors from your game palette:

```python
# classical_ui_palette.py

class ClassicalUIPalette:
    """16-color palette optimized for classical era UI"""
    
    # Base colors (8 colors)
    BLACK = (0, 0, 0)
    WHITE = (248, 248, 248)
    
    # Stone/Architecture colors (neutral UI backgrounds)
    STONE_DARK = (88, 88, 88)
    STONE = (168, 168, 168)
    STONE_LIGHT = (208, 208, 208)
    
    # Bronze/Metal (buttons, borders)
    BRONZE_DARK = (139, 90, 43)
    BRONZE = (205, 127, 50)
    BRONZE_LIGHT = (238, 180, 34)
    
    # Accent colors (highlights, selection)
    RED = (212, 24, 108)      # Enemy/danger
    BLUE = (41, 173, 255)     # Player/friendly
    GREEN = (112, 198, 169)   # Success/positive
    YELLOW = (233, 195, 91)   # Warning/gold
    
    # Parchment (text backgrounds)
    PARCHMENT_DARK = (194, 178, 128)
    PARCHMENT = (230, 220, 170)
    PARCHMENT_LIGHT = (248, 243, 214)
    
    # Transparency key
    TRANSPARENT = (255, 0, 255)  # Magenta key color
    
    @classmethod
    def get_palette_surface(cls):
        """Create palette swatch for reference"""
        swatch = pygame.Surface((16*16, 16))
        colors = [
            cls.BLACK, cls.STONE_DARK, cls.STONE, cls.STONE_LIGHT,
            cls.BRONZE_DARK, cls.BRONZE, cls.BRONZE_LIGHT,
            cls.RED, cls.BLUE, cls.GREEN, cls.YELLOW,
            cls.PARCHMENT_DARK, cls.PARCHMENT, cls.PARCHMENT_LIGHT,
            cls.WHITE, cls.TRANSPARENT
        ]
        
        for i, color in enumerate(colors):
            pygame.draw.rect(swatch, color, (i*16, 0, 16, 16))
        
        return swatch
```

### 3. Pixel Font Rendering

Use bitmap fonts for authentic pixel look:

```python
# pixel_font.py

class PixelFont:
    """Bitmap font renderer for pixel-perfect text"""
    
    def __init__(self, font_image_path, char_width=8, char_height=8):
        """
        Load bitmap font from image
        Font should be arranged in ASCII order
        """
        self.font_sheet = pygame.image.load(font_image_path).convert_alpha()
        self.char_width = char_width
        self.char_height = char_height
        
        # ASCII printable range
        self.first_char = 32  # Space
        self.last_char = 126  # ~
        
        # Cache character surfaces
        self.char_cache = {}
        self._load_characters()
    
    def _load_characters(self):
        """Extract individual characters from font sheet"""
        chars_per_row = self.font_sheet.get_width() // self.char_width
        
        for i in range(self.first_char, self.last_char + 1):
            char_index = i - self.first_char
            row = char_index // chars_per_row
            col = char_index % chars_per_row
            
            x = col * self.char_width
            y = row * self.char_height
            
            char_surface = self.font_sheet.subsurface(
                pygame.Rect(x, y, self.char_width, self.char_height)
            )
            
            self.char_cache[chr(i)] = char_surface
    
    def render(self, text, color=None):
        """
        Render text to surface
        If color provided, recolor the font
        """
        width = len(text) * self.char_width
        height = self.char_height
        
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        for i, char in enumerate(text):
            if char in self.char_cache:
                char_surf = self.char_cache[char].copy()
                
                # Recolor if needed
                if color:
                    char_surf = self._recolor_surface(char_surf, color)
                
                surface.blit(char_surf, (i * self.char_width, 0))
        
        return surface
    
    def _recolor_surface(self, surface, color):
        """Replace non-transparent pixels with color"""
        colored = surface.copy()
        arr = pygame.surfarray.pixels3d(colored)
        alpha = pygame.surfarray.pixels_alpha(colored)
        
        # Replace all non-transparent pixels with new color
        mask = alpha > 0
        arr[mask] = color
        
        del arr, alpha  # Release array locks
        return colored
    
    def get_text_width(self, text):
        """Calculate pixel width of text"""
        return len(text) * self.char_width
    
    def get_text_height(self):
        """Get font height"""
        return self.char_height
```

## Classical UI Components

### 1. Stone Panel

```python
# stone_panel.py

class StonePanel:
    """Decorative stone panel with chisel effect"""
    
    def __init__(self, rect, depth=4):
        self.rect = rect
        self.depth = depth
        self.surface = self._create_panel()
    
    def _create_panel(self):
        """Create stone panel with depth effect"""
        surface = pygame.Surface(self.rect.size)
        w, h = self.rect.size
        
        # Base stone color
        surface.fill(STONE)
        
        # Draw highlight (top-left)
        for i in range(self.depth):
            # Top edge
            pygame.draw.line(surface, STONE_LIGHT,
                           (i, i), (w-i-1, i))
            # Left edge
            pygame.draw.line(surface, STONE_LIGHT,
                           (i, i), (i, h-i-1))
        
        # Draw shadow (bottom-right)
        for i in range(self.depth):
            # Bottom edge
            pygame.draw.line(surface, STONE_DARK,
                           (i, h-i-1), (w-i-1, h-i-1))
            # Right edge
            pygame.draw.line(surface, STONE_DARK,
                           (w-i-1, i), (w-i-1, h-i-1))
        
        return surface
    
    def draw(self, screen, position):
        """Draw panel at position"""
        screen.blit(self.surface, position)


class ChiseledBorder:
    """Decorative border with carved stone effect"""
    
    @staticmethod
    def draw_frame(surface, rect, border_width=8):
        """Draw ornate stone frame"""
        # Outer dark border
        pygame.draw.rect(surface, STONE_DARK, rect, border_width)
        
        # Inner light border
        inner_rect = rect.inflate(-border_width*2, -border_width*2)
        pygame.draw.rect(surface, STONE_LIGHT, inner_rect, 2)
        
        # Add corner decorations
        ChiseledBorder._draw_corner_decoration(
            surface, rect.topleft, 'top-left', border_width
        )
        ChiseledBorder._draw_corner_decoration(
            surface, (rect.right, rect.top), 'top-right', border_width
        )
        ChiseledBorder._draw_corner_decoration(
            surface, (rect.left, rect.bottom), 'bottom-left', border_width
        )
        ChiseledBorder._draw_corner_decoration(
            surface, rect.bottomright, 'bottom-right', border_width
        )
    
    @staticmethod
    def _draw_corner_decoration(surface, pos, corner, size):
        """Draw small decorative element in corner"""
        # Simple diamond pattern
        if corner == 'top-left':
            points = [
                (pos[0] + size//2, pos[1]),
                (pos[0] + size, pos[1] + size//2),
                (pos[0] + size//2, pos[1] + size),
                (pos[0], pos[1] + size//2)
            ]
        # Similar for other corners...
        
        pygame.draw.polygon(surface, BRONZE_LIGHT, points)
        pygame.draw.polygon(surface, BRONZE_DARK, points, 1)
```

### 2. Bronze Button

```python
# bronze_button.py

class BronzeButton:
    """3D bronze button with press animation"""
    
    def __init__(self, rect, text, font):
        self.rect = rect
        self.text = text
        self.font = font
        
        self.pressed = False
        self.hovered = False
        self.enabled = True
        
        # Pre-render states
        self.surface_normal = self._render_state('normal')
        self.surface_hover = self._render_state('hover')
        self.surface_pressed = self._render_state('pressed')
        self.surface_disabled = self._render_state('disabled')
    
    def _render_state(self, state):
        """Render button in specific state"""
        surface = pygame.Surface(self.rect.size)
        w, h = self.rect.size
        
        # Choose colors based on state
        if state == 'disabled':
            base_color = STONE
            highlight = STONE_LIGHT
            shadow = STONE_DARK
        else:
            base_color = BRONZE
            highlight = BRONZE_LIGHT if state == 'hover' else BRONZE
            shadow = BRONZE_DARK
        
        # Draw base
        surface.fill(base_color)
        
        # Draw depth based on state
        depth = 2 if state == 'pressed' else 4
        
        if state != 'pressed':
            # Raised button - highlight top/left
            for i in range(depth):
                pygame.draw.line(surface, highlight, (i, i), (w-i-1, i))
                pygame.draw.line(surface, highlight, (i, i), (i, h-i-1))
                pygame.draw.line(surface, shadow, (i, h-i-1), (w-i-1, h-i-1))
                pygame.draw.line(surface, shadow, (w-i-1, i), (w-i-1, h-i-1))
        else:
            # Pressed button - inverted
            for i in range(depth):
                pygame.draw.line(surface, shadow, (i, i), (w-i-1, i))
                pygame.draw.line(surface, shadow, (i, i), (i, h-i-1))
                pygame.draw.line(surface, highlight, (i, h-i-1), (w-i-1, h-i-1))
                pygame.draw.line(surface, highlight, (w-i-1, i), (w-i-1, h-i-1))
        
        # Render text
        text_color = STONE_DARK if state == 'disabled' else WHITE
        text_surf = self.font.render(self.text, text_color)
        
        # Center text (with offset if pressed)
        text_rect = text_surf.get_rect(center=(w//2, h//2))
        if state == 'pressed':
            text_rect.move_ip(1, 1)  # Shift down when pressed
        
        surface.blit(text_surf, text_rect)
        
        return surface
    
    def update(self, mouse_pos, mouse_pressed):
        """Update button state"""
        if not self.enabled:
            return
        
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pressed = self.hovered and mouse_pressed
    
    def draw(self, screen):
        """Draw button in current state"""
        if not self.enabled:
            surface = self.surface_disabled
        elif self.pressed:
            surface = self.surface_pressed
        elif self.hovered:
            surface = self.surface_hover
        else:
            surface = self.surface_normal
        
        screen.blit(surface, self.rect)
    
    def is_clicked(self, event):
        """Check if button was clicked"""
        if not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
```

### 3. Parchment Scroll

```python
# parchment_scroll.py

class ParchmentScroll:
    """Text display on parchment background"""
    
    def __init__(self, rect, text, font):
        self.rect = rect
        self.text = text
        self.font = font
        self.scroll_offset = 0
        
        self.surface = self._create_scroll()
    
    def _create_scroll(self):
        """Create parchment background"""
        surface = pygame.Surface(self.rect.size)
        w, h = self.rect.size
        
        # Parchment base
        surface.fill(PARCHMENT)
        
        # Add texture (random darker pixels)
        for _ in range(w * h // 50):  # 2% pixels
            x = random.randint(0, w-1)
            y = random.randint(0, h-1)
            surface.set_at((x, y), PARCHMENT_DARK)
        
        # Worn edges effect
        for x in range(w):
            # Top edge
            if random.random() < 0.3:
                surface.set_at((x, 0), PARCHMENT_DARK)
            # Bottom edge
            if random.random() < 0.3:
                surface.set_at((x, h-1), PARCHMENT_DARK)
        
        for y in range(h):
            # Left edge
            if random.random() < 0.3:
                surface.set_at((0, y), PARCHMENT_DARK)
            # Right edge
            if random.random() < 0.3:
                surface.set_at((w-1, y), PARCHMENT_DARK)
        
        return surface
    
    def draw_text(self, screen, position):
        """Draw scroll with text"""
        # Draw parchment background
        screen.blit(self.surface, position)
        
        # Draw text with word wrap
        lines = self._wrap_text(self.text, self.rect.width - 16)
        
        y_offset = 8 - self.scroll_offset
        for line in lines:
            if y_offset > self.rect.height:
                break
            
            if y_offset >= 0:
                text_surf = self.font.render(line, STONE_DARK)
                screen.blit(text_surf, (position[0] + 8, position[1] + y_offset))
            
            y_offset += self.font.get_text_height() + 2
    
    def _wrap_text(self, text, max_width):
        """Word wrap text to fit width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font.get_text_width(test_line) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def scroll(self, delta):
        """Scroll text up/down"""
        self.scroll_offset += delta
        self.scroll_offset = max(0, self.scroll_offset)
```

### 4. Icon-Based UI Elements

```python
# icon_ui.py

class IconButton:
    """Button with pixel art icon"""
    
    def __init__(self, position, icon_surface, tooltip_text=""):
        self.rect = pygame.Rect(position[0], position[1], 32, 32)
        self.icon = icon_surface
        self.tooltip = tooltip_text
        
        self.hovered = False
        self.pressed = False
        
        # Create button frames
        self.frame_normal = self._create_frame(STONE)
        self.frame_hover = self._create_frame(STONE_LIGHT)
        self.frame_pressed = self._create_frame(STONE_DARK)
    
    def _create_frame(self, color):
        """Create button frame"""
        frame = pygame.Surface((32, 32))
        frame.fill(color)
        
        # Border
        pygame.draw.rect(frame, BRONZE_DARK, (0, 0, 32, 32), 2)
        
        # Icon in center
        icon_rect = self.icon.get_rect(center=(16, 16))
        frame.blit(self.icon, icon_rect)
        
        return frame
    
    def draw(self, screen):
        """Draw icon button"""
        if self.pressed:
            screen.blit(self.frame_pressed, self.rect)
        elif self.hovered:
            screen.blit(self.frame_hover, self.rect)
        else:
            screen.blit(self.frame_normal, self.rect)


class ResourceDisplay:
    """Display resource with icon"""
    
    def __init__(self, position, icon, value, font):
        self.position = position
        self.icon = icon
        self.value = value
        self.font = font
    
    def draw(self, screen):
        """Draw icon + value"""
        # Draw icon
        screen.blit(self.icon, self.position)
        
        # Draw value next to icon
        text_surf = self.font.render(str(self.value), WHITE)
        text_pos = (self.position[0] + self.icon.get_width() + 4,
                   self.position[1])
        screen.blit(text_surf, text_pos)
    
    def update_value(self, new_value):
        """Update displayed value"""
        self.value = new_value
```

## HUD Design Patterns

### 1. Minimalist Battle HUD

```python
# minimalist_hud.py

class MinimalistBattleHUD:
    """Clean, unobtrusive battle interface"""
    
    def __init__(self, screen_size, font):
        self.screen_size = screen_size
        self.font = font
        
        # HUD elements only in corners
        self.top_left = TopLeftPanel(font)
        self.top_right = TopRightPanel(font)
        self.bottom_left = UnitPanel(font)
        self.bottom_right = ActionsPanel(font)
    
    def draw(self, screen, game_state):
        """Draw minimal HUD elements"""
        # Top-left: Turn + Faction
        self.top_left.draw(screen, (8, 8), 
                          f"Turn {game_state.turn} - {game_state.faction}")
        
        # Top-right: Resources
        self.top_right.draw(screen, (self.screen_size[0] - 100, 8),
                           game_state.gold)
        
        # Bottom-left: Selected unit
        if game_state.selected_unit:
            self.bottom_left.draw(screen, (8, self.screen_size[1] - 80),
                                 game_state.selected_unit)
        
        # Bottom-right: Available actions
        if game_state.selected_unit:
            self.bottom_right.draw(screen, 
                                  (self.screen_size[0] - 120, 
                                   self.screen_size[1] - 120),
                                  game_state.selected_unit.actions)


class TopLeftPanel:
    """Small info panel - turn indicator"""
    
    def __init__(self, font):
        self.font = font
        self.panel = StonePanel(pygame.Rect(0, 0, 150, 32), depth=2)
    
    def draw(self, screen, position, text):
        """Draw panel with text"""
        self.panel.draw(screen, position)
        
        text_surf = self.font.render(text, WHITE)
        text_pos = (position[0] + 8, position[1] + 8)
        screen.blit(text_surf, text_pos)
```

### 2. Contextual Tooltips

```python
# pixel_tooltips.py

class PixelTooltip:
    """Pixel art styled tooltip"""
    
    def __init__(self, font, max_width=200):
        self.font = font
        self.max_width = max_width
        self.visible = False
        self.position = (0, 0)
        self.text = ""
        self.surface = None
    
    def show(self, text, position):
        """Show tooltip at position"""
        self.text = text
        self.position = position
        self.visible = True
        self.surface = self._create_tooltip()
    
    def _create_tooltip(self):
        """Create tooltip surface"""
        # Wrap text
        lines = self._wrap_text(self.text)
        
        # Calculate size
        width = min(self.max_width, 
                   max(self.font.get_text_width(line) for line in lines) + 16)
        height = len(lines) * (self.font.get_text_height() + 2) + 12
        
        # Create surface
        surface = pygame.Surface((width, height))
        
        # Parchment background
        surface.fill(PARCHMENT_LIGHT)
        
        # Dark border
        pygame.draw.rect(surface, STONE_DARK, (0, 0, width, height), 2)
        
        # Inner light border
        pygame.draw.rect(surface, WHITE, (2, 2, width-4, height-4), 1)
        
        # Render text
        y = 6
        for line in lines:
            text_surf = self.font.render(line, STONE_DARK)
            surface.blit(text_surf, (8, y))
            y += self.font.get_text_height() + 2
        
        return surface
    
    def draw(self, screen):
        """Draw tooltip if visible"""
        if self.visible and self.surface:
            # Ensure tooltip stays on screen
            x, y = self.position
            w, h = self.surface.get_size()
            
            if x + w > screen.get_width():
                x = screen.get_width() - w
            if y + h > screen.get_height():
                y = screen.get_height() - h
            
            screen.blit(self.surface, (x, y))
    
    def hide(self):
        """Hide tooltip"""
        self.visible = False
    
    def _wrap_text(self, text):
        """Word wrap for tooltip"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font.get_text_width(test_line) <= self.max_width - 16:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
```

### 3. Health Bars (Pixel Style)

```python
# pixel_health_bar.py

class PixelHealthBar:
    """Retro-style health bar"""
    
    def __init__(self, max_value, width=64, height=8):
        self.max_value = max_value
        self.current_value = max_value
        self.width = width
        self.height = height
    
    def draw(self, screen, position):
        """Draw health bar at position"""
        x, y = position
        
        # Background (empty bar)
        pygame.draw.rect(screen, STONE_DARK, (x, y, self.width, self.height))
        
        # Border
        pygame.draw.rect(screen, BLACK, (x, y, self.width, self.height), 1)
        
        # Fill (current health)
        fill_width = int((self.current_value / self.max_value) * (self.width - 2))
        
        # Color based on percentage
        if self.current_value / self.max_value > 0.6:
            fill_color = GREEN
        elif self.current_value / self.max_value > 0.3:
            fill_color = YELLOW
        else:
            fill_color = RED
        
        if fill_width > 0:
            pygame.draw.rect(screen, fill_color, 
                           (x + 1, y + 1, fill_width, self.height - 2))
        
        # Segments (optional - adds pixel art style)
        segment_width = 4
        for i in range(0, self.width, segment_width):
            pygame.draw.line(screen, STONE_DARK,
                           (x + i, y), (x + i, y + self.height - 1))
    
    def set_value(self, value):
        """Update current value"""
        self.current_value = max(0, min(self.max_value, value))
    
    def damage(self, amount):
        """Take damage"""
        self.current_value = max(0, self.current_value - amount)
    
    def heal(self, amount):
        """Restore health"""
        self.current_value = min(self.max_value, self.current_value + amount)
```

## Integration with pygame-gui

### Custom Theme for Pixel Art

```python
# pygame_gui_pixel_theme.py

def create_pixel_art_theme():
    """Generate pygame-gui theme for pixel art style"""
    
    theme_dict = {
        "defaults": {
            "colours": {
                "normal_bg": "#A8A8A8",
                "hovered_bg": "#D0D0D0",
                "disabled_bg": "#585858",
                "selected_bg": "#6B5344",
                "dark_bg": "#2F1810",
                "normal_text": "#FFFFFF",
                "hovered_text": "#FFFFFF",
                "selected_text": "#FFD700",
                "disabled_text": "#888888",
                "link_text": "#2A9DFF",
                "link_hover": "#4DB8FF",
                "link_selected": "#1F7ACC",
                "text_shadow": "#000000",
                "normal_border": "#4A3728",
                "hovered_border": "#8B4513",
                "disabled_border": "#444444",
                "selected_border": "#CD7F32",
                "active_border": "#FFD700",
                "filled_bar": "#DC143C",
                "unfilled_bar": "#4A0000"
            },
            "font": {
                "name": "pixel_font",
                "size": 8,
                "bold": False,
                "italic": False
            },
            "misc": {
                "shape": "rectangle",
                "shape_corner_radius": 0,  # Square corners for pixel art
                "border_width": 2,
                "shadow_width": 0,  # No shadows in pixel art
                "tool_tip_delay": 0.5,
                "text_horiz_alignment": "center",
                "text_vert_alignment": "center",
                "text_horiz_alignment_padding": 4,
                "text_vert_alignment_padding": 4
            }
        },
        
        "button": {
            "colours": {
                "normal_bg": "#8B4513",
                "hovered_bg": "#CD7F32",
                "selected_bg": "#654321",
                "disabled_bg": "#585858",
                "active_bg": "#A0522D",
                "normal_border": "#4A3728",
                "hovered_border": "#8B4513"
            },
            "misc": {
                "border_width": 2
            }
        },
        
        "text_box": {
            "colours": {
                "dark_bg": "#E6DCA6",
                "normal_border": "#8B7355"
            }
        },
        
        "drop_down_menu": {
            "colours": {
                "dark_bg": "#8B7355"
            }
        }
    }
    
    return theme_dict


def apply_pixel_theme_to_manager(ui_manager):
    """Apply pixel art theme to pygame-gui manager"""
    theme = create_pixel_art_theme()
    
    # Save to temp file
    import json
    with open('temp_pixel_theme.json', 'w') as f:
        json.dump(theme, f, indent=2)
    
    # Load into manager
    ui_manager.get_theme().load_theme('temp_pixel_theme.json')
```

## Complete Example: Classical Battle UI

```python
# complete_battle_ui.py
import pygame
import pygame_gui

class ClassicalBattleUI:
    """Complete pixel art battle interface"""
    
    def __init__(self, screen_size):
        self.screen_size = screen_size
        
        # Initialize pygame-gui
        self.ui_manager = pygame_gui.UIManager(screen_size)
        apply_pixel_theme_to_manager(self.ui_manager)
        
        # Load pixel font
        self.pixel_font = PixelFont('assets/fonts/ancient_8x8.png', 8, 8)
        
        # Create UI components
        self.hud = MinimalistBattleHUD(screen_size, self.pixel_font)
        self.tooltip = PixelTooltip(self.pixel_font)
        
        # Custom pixel art elements
        self.bronze_buttons = self._create_action_buttons()
        self.health_bars = {}
        
        # Selection
        self.selected_unit = None
    
    def _create_action_buttons(self):
        """Create pixel art action buttons"""
        buttons = {}
        
        # Load icons (16x16 pixel art)
        move_icon = pygame.image.load('assets/icons/move.png').convert_alpha()
        attack_icon = pygame.image.load('assets/icons/attack.png').convert_alpha()
        defend_icon = pygame.image.load('assets/icons/defend.png').convert_alpha()
        
        # Create icon buttons
        x = self.screen_size[0] - 120
        y = self.screen_size[1] - 120
        
        buttons['move'] = IconButton((x, y), move_icon, "Move Unit")
        buttons['attack'] = IconButton((x + 36, y), attack_icon, "Attack")
        buttons['defend'] = IconButton((x + 72, y), defend_icon, "Defend")
        
        return buttons
    
    def update(self, dt, game_state):
        """Update UI state"""
        self.ui_manager.update(dt)
        
        # Update unit health bars
        for unit in game_state.units:
            if unit.id not in self.health_bars:
                self.health_bars[unit.id] = PixelHealthBar(unit.max_health, 32, 4)
            self.health_bars[unit.id].set_value(unit.health)
        
        # Update button states
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for button in self.bronze_buttons.values():
            button.update(mouse_pos, mouse_pressed)
    
    def draw(self, screen, game_state):
        """Draw all UI elements"""
        # Draw pygame-gui elements
        self.ui_manager.draw_ui(screen)
        
        # Draw custom pixel art HUD
        self.hud.draw(screen, game_state)
        
        # Draw health bars above units
        for unit in game_state.units:
            if unit.id in self.health_bars:
                bar_pos = (unit.screen_x - 16, unit.screen_y - 8)
                self.health_bars[unit.id].draw(screen, bar_pos)
        
        # Draw action buttons (if unit selected)
        if self.selected_unit:
            for button in self.bronze_buttons.values():
                button.draw(screen)
        
        # Draw tooltip
        self.tooltip.draw(screen)
    
    def handle_event(self, event):
        """Handle UI events"""
        # pygame-gui events
        self.ui_manager.process_events(event)
        
        # Custom button events
        if self.selected_unit:
            for action, button in self.bronze_buttons.items():
                if button.is_clicked(event):
                    return ('action', action)
        
        # Hover tooltips
        if event.type == pygame.MOUSEMOTION:
            self._update_tooltip(event.pos)
        
        return None
    
    def _update_tooltip(self, mouse_pos):
        """Update tooltip based on mouse position"""
        # Check if hovering over buttons
        for action, button in self.bronze_buttons.items():
            if button.rect.collidepoint(mouse_pos):
                self.tooltip.show(button.tooltip, 
                                (mouse_pos[0] + 10, mouse_pos[1] + 10))
                return
        
        self.tooltip.hide()
```

## Best Practices Summary

1. **Pixel-Perfect Alignment**: Everything on grid (usually 8px)
2. **Limited Palette**: 8-16 colors maximum
3. **No Anti-Aliasing**: Crisp, clean edges
4. **Consistent Style**: All UI matches pixel art aesthetic
5. **Clear Hierarchy**: Important info is bigger/brighter
6. **Instant Feedback**: Every action has visual response
7. **Readable Text**: Use bitmap fonts, high contrast
8. **Minimize Clutter**: Show only essential information
9. **Authentic Feel**: Study NES/SNES/Genesis UI designs
10. **Modern UX**: Retro look, modern usability

## Tools & Resources

**Font Creation:**
- Pixelart font editors: Fontstruct, BitFontMaker
- Pre-made pixel fonts: DaFont (pixel category)

**Icon Creation:**
- Aseprite, Pyxel Editor for 16x16 icons
- Maintain consistent size (8x8, 16x16, 32x32)

**UI Mockups:**
- Sketch in pixel editor first
- Test at actual game resolution
- Prototype in Pyxel/Pygame before implementing

**Reference Games:**
- Advance Wars (GBA) - excellent strategy UI
- Fire Emblem (GBA/SNES) - information display
- HOMM3 - resource management UI
- Age of Empires (classic) - RTS pixel UI

This skill provides everything needed to create authentic pixel art UIs that look retro but feel modern!
