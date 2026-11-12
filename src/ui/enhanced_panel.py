"""
Enhanced panel widget with sprite support and 9-slice scaling.
"""

import pygame
from typing import Optional, List
from src.ui.widgets.widget import Widget


class EnhancedPanel(Widget):
    """
    Enhanced panel with sprite support for classical stone/parchment textures.
    Supports 9-slice scaling for proper corners and edges.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        sprite: Optional[pygame.Surface] = None,
        nine_slice_sprites: Optional[dict] = None,
        border_color: Optional[tuple] = None,
        border_width: int = 0,
        corner_decorations: Optional[List[pygame.Surface]] = None,
    ):
        """
        Initialize enhanced panel.

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
            sprite: Simple sprite to scale to panel size
            nine_slice_sprites: Dict with keys: 'corners', 'edges', 'center' for 9-slice
            border_color: Border color (None for no border)
            border_width: Border width
            corner_decorations: List of corner decoration sprites [TL, TR, BL, BR]
        """
        super().__init__(x, y, width, height)

        self.sprite = sprite
        self.nine_slice_sprites = nine_slice_sprites
        self.border_color = border_color
        self.border_width = border_width
        self.corner_decorations = corner_decorations or []

        # Fallback colors
        self.background_color = (90, 75, 60)  # Stone color

        # Pre-render panel if using 9-slice
        self.rendered_panel = None
        if self.nine_slice_sprites:
            self._render_nine_slice()
        elif self.sprite:
            self.rendered_panel = pygame.transform.scale(self.sprite, (width, height))

    def _render_nine_slice(self):
        """Pre-render panel using 9-slice sprites."""
        if not self.nine_slice_sprites:
            return

        # Create surface for the panel
        self.rendered_panel = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Get 9-slice components
        corners = self.nine_slice_sprites.get('corners', {})
        edges = self.nine_slice_sprites.get('edges', {})
        center = self.nine_slice_sprites.get('center')

        # Get corner sprites
        tl = corners.get('top_left')
        tr = corners.get('top_right')
        bl = corners.get('bottom_left')
        br = corners.get('bottom_right')

        # Get edge sprites
        top = edges.get('top')
        bottom = edges.get('bottom')
        left = edges.get('left')
        right = edges.get('right')

        # Calculate dimensions
        corner_size = tl.get_width() if tl else 0
        edge_width = self.rect.width - (2 * corner_size)
        edge_height = self.rect.height - (2 * corner_size)

        # Draw center (tiled or stretched)
        if center:
            scaled_center = pygame.transform.scale(center, (edge_width, edge_height))
            self.rendered_panel.blit(scaled_center, (corner_size, corner_size))

        # Draw edges
        if top:
            scaled_top = pygame.transform.scale(top, (edge_width, top.get_height()))
            self.rendered_panel.blit(scaled_top, (corner_size, 0))

        if bottom:
            scaled_bottom = pygame.transform.scale(bottom, (edge_width, bottom.get_height()))
            self.rendered_panel.blit(scaled_bottom, (corner_size, self.rect.height - bottom.get_height()))

        if left:
            scaled_left = pygame.transform.scale(left, (left.get_width(), edge_height))
            self.rendered_panel.blit(scaled_left, (0, corner_size))

        if right:
            scaled_right = pygame.transform.scale(right, (right.get_width(), edge_height))
            self.rendered_panel.blit(scaled_right, (self.rect.width - right.get_width(), corner_size))

        # Draw corners
        if tl:
            self.rendered_panel.blit(tl, (0, 0))
        if tr:
            self.rendered_panel.blit(tr, (self.rect.width - tr.get_width(), 0))
        if bl:
            self.rendered_panel.blit(bl, (0, self.rect.height - bl.get_height()))
        if br:
            self.rendered_panel.blit(br, (self.rect.width - br.get_width(), self.rect.height - br.get_height()))

    def render(self, screen: pygame.Surface) -> None:
        """Render enhanced panel."""
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 50))
        screen.blit(shadow_surface, shadow_rect.topleft)

        # Draw panel background
        if self.rendered_panel:
            screen.blit(self.rendered_panel, self.rect.topleft)
        else:
            # Fallback: draw textured rectangle
            panel_surface = pygame.Surface((self.rect.width, self.rect.height))
            panel_surface.fill(self.background_color)

            # Add stone texture
            for i in range(200):
                x = (hash(f"{i}x{self.rect.x}") % self.rect.width)
                y = (hash(f"{i}y{self.rect.y}") % self.rect.height)
                color_var = (hash(f"{i}c") % 20) - 10
                pixel_color = tuple(max(0, min(255, c + color_var)) for c in self.background_color)
                pygame.draw.circle(panel_surface, pixel_color, (x, y), 1)

            screen.blit(panel_surface, self.rect.topleft)

        # Draw border
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)

        # Draw corner decorations
        if self.corner_decorations:
            positions = [
                (self.rect.left, self.rect.top),  # Top-left
                (self.rect.right, self.rect.top),  # Top-right
                (self.rect.left, self.rect.bottom),  # Bottom-left
                (self.rect.right, self.rect.bottom),  # Bottom-right
            ]

            for i, corner in enumerate(self.corner_decorations[:4]):
                if corner:
                    decorated = corner.copy()
                    # Flip corners as needed
                    if i == 1:  # Top-right
                        decorated = pygame.transform.flip(decorated, True, False)
                    elif i == 2:  # Bottom-left
                        decorated = pygame.transform.flip(decorated, False, True)
                    elif i == 3:  # Bottom-right
                        decorated = pygame.transform.flip(decorated, True, True)

                    # Adjust position based on corner
                    pos = list(positions[i])
                    if i % 2 == 1:  # Right side
                        pos[0] -= decorated.get_width()
                    if i >= 2:  # Bottom
                        pos[1] -= decorated.get_height()

                    screen.blit(decorated, pos)


def load_nine_slice_sprites(resource_manager, base_path: str) -> dict:
    """
    Helper function to load 9-slice sprites from a base path.

    Args:
        resource_manager: Game resource manager
        base_path: Base path for 9-slice sprites (e.g., "assets/sprites/ui/panels/stone_panel_9slice")

    Returns:
        Dict with 9-slice components
    """
    try:
        return {
            'corners': {
                'top_left': resource_manager.load_sprite(f"{base_path}_top_left.png"),
                'top_right': resource_manager.load_sprite(f"{base_path}_top_right.png"),
                'bottom_left': resource_manager.load_sprite(f"{base_path}_bottom_left.png"),
                'bottom_right': resource_manager.load_sprite(f"{base_path}_bottom_right.png"),
            },
            'edges': {
                'top': resource_manager.load_sprite(f"{base_path}_top.png"),
                'bottom': resource_manager.load_sprite(f"{base_path}_bottom.png"),
                'left': resource_manager.load_sprite(f"{base_path}_left.png"),
                'right': resource_manager.load_sprite(f"{base_path}_right.png"),
            },
            'center': resource_manager.load_sprite(f"{base_path}_center.png"),
        }
    except Exception as e:
        print(f"Failed to load 9-slice sprites: {e}")
        return None
