"""
Tactical Combat Rendering and UI System
Handles visualization of the battlefield, units, UI elements, and effects
"""

import pygame
from typing import Dict, List, Tuple, Optional
from combat_game_state import *

# Color palette matching the pixel-art aesthetic
COLORS = {
    # Terrain
    'grass_light': (167, 181, 80),
    'grass_medium': (147, 161, 70),
    'grass_dark': (127, 141, 60),
    'tree_green': (80, 100, 40),
    'tree_trunk': (90, 70, 50),
    
    # UI
    'grid_line': (140, 150, 60, 100),
    'ui_background': (40, 35, 30),
    'ui_border': (180, 160, 120),
    'health_green': (60, 180, 80),
    'health_yellow': (220, 200, 60),
    'health_red': (200, 60, 60),
    'morale_blue': (80, 140, 220),
    
    # Units - Attacker (Blue)
    'attacker_primary': (60, 120, 200),
    'attacker_secondary': (80, 150, 220),
    'attacker_accent': (180, 200, 230),
    
    # Units - Defender (Red/Gold)
    'defender_primary': (180, 60, 50),
    'defender_secondary': (220, 180, 60),
    'defender_accent': (240, 220, 180),
    
    # Effects
    'arrow_shaft': (120, 90, 60),
    'arrow_head': (150, 150, 150),
    'dust': (180, 160, 120, 150),
    'sparks': (255, 220, 100),
    'impact': (200, 200, 200),
    
    # Selection
    'selection': (255, 255, 100),
    'target_marker': (255, 100, 100)
}


class Camera:
    """Camera system for panning and zooming"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom = 1.0
    
    def world_to_screen(self, world_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = int((world_pos[0] - self.x) * self.zoom)
        screen_y = int((world_pos[1] - self.y) * self.zoom)
        return (screen_x, screen_y)
    
    def screen_to_world(self, screen_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert screen coordinates to world coordinates"""
        world_x = int(screen_pos[0] / self.zoom + self.x)
        world_y = int(screen_pos[1] / self.zoom + self.y)
        return (world_x, world_y)


class BattleRenderer:
    """Renders the tactical battle scene"""
    
    def __init__(self, screen_width: int = 1200, screen_height: int = 800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = 40  # Pixels per grid cell
        self.camera = Camera(screen_width, screen_height)
        
        # Sprite cache (in a real implementation, load actual sprites)
        self.sprites: Dict[str, pygame.Surface] = {}
        
        # UI dimensions
        self.ui_panel_height = 120
        self.battle_view_height = screen_height - self.ui_panel_height
    
    def initialize_pygame(self):
        """Initialize pygame and create the display"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tactical Combat")
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)
    
    def render_frame(self, battle_state: BattleState):
        """Render a complete frame"""
        # Clear screen
        self.screen.fill(COLORS['grass_medium'])
        
        # Render layers
        self._render_terrain(battle_state.battle_map)
        self._render_grid(battle_state.battle_map)
        self._render_units(battle_state)
        self._render_projectiles(battle_state.projectiles)
        self._render_effects(battle_state.particle_effects)
        self._render_selection(battle_state)
        
        # Render UI
        self._render_ui_panel(battle_state)
        self._render_commander_portraits(battle_state)
        self._render_phase_indicator(battle_state)
        
        pygame.display.flip()
    
    def _render_terrain(self, battle_map: BattleMap):
        """Render the battlefield terrain"""
        # Draw grass with variation
        for y in range(battle_map.height):
            for x in range(battle_map.width):
                screen_pos = self._grid_to_screen(x, y)
                
                # Vary grass color slightly for texture
                color_variant = (x + y) % 3
                if color_variant == 0:
                    color = COLORS['grass_light']
                elif color_variant == 1:
                    color = COLORS['grass_medium']
                else:
                    color = COLORS['grass_dark']
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (screen_pos[0], screen_pos[1], self.cell_size, self.cell_size)
                )
        
        # Draw trees
        for tree_pos in battle_map.trees:
            self._render_tree(tree_pos)
        
        # Draw castle
        if battle_map.castle_position:
            self._render_castle(battle_map.castle_position)
    
    def _render_tree(self, pos: GridPosition):
        """Render a tree"""
        screen_pos = self._grid_to_screen(pos.x, pos.y)
        
        # Tree crown (simplified circle)
        crown_center = (screen_pos[0] + self.cell_size // 2, 
                       screen_pos[1] + self.cell_size // 3)
        pygame.draw.circle(
            self.screen,
            COLORS['tree_green'],
            crown_center,
            int(self.cell_size * 0.6)
        )
        
        # Tree trunk
        trunk_rect = pygame.Rect(
            screen_pos[0] + self.cell_size // 2 - 3,
            screen_pos[1] + self.cell_size // 2,
            6,
            self.cell_size // 2
        )
        pygame.draw.rect(self.screen, COLORS['tree_trunk'], trunk_rect)
    
    def _render_castle(self, pos: GridPosition):
        """Render castle fortifications"""
        screen_pos = self._grid_to_screen(pos.x, pos.y)
        
        # Castle walls (simplified)
        wall_rect = pygame.Rect(
            screen_pos[0] - self.cell_size,
            screen_pos[1] - self.cell_size,
            self.cell_size * 3,
            self.cell_size * 3
        )
        pygame.draw.rect(self.screen, (150, 140, 130), wall_rect)
        pygame.draw.rect(self.screen, (100, 90, 80), wall_rect, 3)
        
        # Towers
        tower_positions = [
            (screen_pos[0] - self.cell_size, screen_pos[1] - self.cell_size),
            (screen_pos[0] + self.cell_size * 2 - 15, screen_pos[1] - self.cell_size)
        ]
        
        for tower_pos in tower_positions:
            tower_rect = pygame.Rect(tower_pos[0], tower_pos[1], 15, 25)
            pygame.draw.rect(self.screen, (140, 130, 120), tower_rect)
            pygame.draw.rect(self.screen, (90, 80, 70), tower_rect, 2)
    
    def _render_grid(self, battle_map: BattleMap):
        """Render the tactical grid overlay"""
        # Vertical lines
        for x in range(battle_map.width + 1):
            screen_x = x * self.cell_size
            pygame.draw.line(
                self.screen,
                COLORS['grid_line'],
                (screen_x, 0),
                (screen_x, self.battle_view_height),
                1
            )
        
        # Horizontal lines
        for y in range(battle_map.height + 1):
            screen_y = y * self.cell_size
            pygame.draw.line(
                self.screen,
                COLORS['grid_line'],
                (0, screen_y),
                (self.screen_width, screen_y),
                1
            )
    
    def _render_units(self, battle_state: BattleState):
        """Render all units on the battlefield"""
        for army in [battle_state.attacker, battle_state.defender]:
            if not army:
                continue
            
            for unit in army.units:
                if unit.stance == UnitStance.DESTROYED:
                    continue
                
                self._render_unit(unit, battle_state.selected_unit_id == unit.unit_id)
    
    def _render_unit(self, unit: Unit, is_selected: bool):
        """Render a single unit"""
        screen_pos = self._grid_to_screen(unit.position.x, unit.position.y)
        
        # Determine colors based on side
        if unit.side == ArmySide.ATTACKER:
            primary_color = COLORS['attacker_primary']
            secondary_color = COLORS['attacker_secondary']
        else:
            primary_color = COLORS['defender_primary']
            secondary_color = COLORS['defender_secondary']
        
        # Unit size based on type and soldier count
        if unit.unit_type == UnitType.CAVALRY:
            unit_width = int(self.cell_size * 0.7)
            unit_height = int(self.cell_size * 0.8)
        else:
            unit_width = int(self.cell_size * 0.6)
            unit_height = int(self.cell_size * 0.6)
        
        # Center unit in cell
        unit_rect = pygame.Rect(
            screen_pos[0] + (self.cell_size - unit_width) // 2,
            screen_pos[1] + (self.cell_size - unit_height) // 2,
            unit_width,
            unit_height
        )
        
        # Draw unit representation
        if unit.soldier_count > 1:
            # Draw multiple small figures for formations
            figures_per_row = min(4, int(unit.soldier_count ** 0.5))
            figure_size = max(3, unit_width // figures_per_row - 1)
            
            for i in range(min(unit.soldier_count, 16)):  # Cap visual soldiers
                row = i // figures_per_row
                col = i % figures_per_row
                figure_x = unit_rect.x + col * (figure_size + 1)
                figure_y = unit_rect.y + row * (figure_size + 1)
                
                pygame.draw.circle(
                    self.screen,
                    primary_color,
                    (figure_x + figure_size // 2, figure_y + figure_size // 2),
                    figure_size // 2
                )
        else:
            # Single unit representation
            pygame.draw.ellipse(self.screen, primary_color, unit_rect)
        
        # Draw unit border
        pygame.draw.rect(self.screen, secondary_color, unit_rect, 2)
        
        # Selection highlight
        if is_selected:
            selection_rect = unit_rect.inflate(8, 8)
            pygame.draw.rect(self.screen, COLORS['selection'], selection_rect, 3)
        
        # Health bar
        self._render_health_bar(unit, screen_pos)
        
        # Stance indicator
        if unit.stance == UnitStance.ATTACKING:
            indicator_pos = (screen_pos[0] + self.cell_size - 10, screen_pos[1] + 5)
            pygame.draw.polygon(
                self.screen,
                (255, 100, 100),
                [
                    indicator_pos,
                    (indicator_pos[0] - 6, indicator_pos[1] + 3),
                    (indicator_pos[0] - 6, indicator_pos[1] - 3)
                ]
            )
        elif unit.stance == UnitStance.ROUTING:
            # Draw routing indicator (white flag)
            flag_pos = (screen_pos[0] + self.cell_size - 10, screen_pos[1] + 5)
            pygame.draw.rect(
                self.screen,
                (240, 240, 240),
                (flag_pos[0] - 6, flag_pos[1], 6, 4)
            )
    
    def _render_health_bar(self, unit: Unit, screen_pos: Tuple[int, int]):
        """Render unit health bar"""
        bar_width = self.cell_size - 8
        bar_height = 4
        bar_x = screen_pos[0] + 4
        bar_y = screen_pos[1] + self.cell_size - 8
        
        # Background
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            (bar_x, bar_y, bar_width, bar_height)
        )
        
        # Health fill
        health_percentage = unit.health / unit.max_health
        fill_width = int(bar_width * health_percentage)
        
        if health_percentage > 0.6:
            health_color = COLORS['health_green']
        elif health_percentage > 0.3:
            health_color = COLORS['health_yellow']
        else:
            health_color = COLORS['health_red']
        
        if fill_width > 0:
            pygame.draw.rect(
                self.screen,
                health_color,
                (bar_x, bar_y, fill_width, bar_height)
            )
    
    def _render_projectiles(self, projectiles: List[Projectile]):
        """Render all active projectiles"""
        for projectile in projectiles:
            # Interpolate position
            start_screen = self._grid_to_screen(
                projectile.start_pos.x,
                projectile.start_pos.y
            )
            end_screen = self._grid_to_screen(
                projectile.target_pos.x,
                projectile.target_pos.y
            )
            
            # Calculate current position
            current_x = start_screen[0] + (end_screen[0] - start_screen[0]) * projectile.current_progress
            current_y = start_screen[1] + (end_screen[1] - start_screen[1]) * projectile.current_progress
            
            # Add arc to projectile path
            arc_height = 20
            arc_offset = arc_height * (1 - (2 * projectile.current_progress - 1) ** 2)
            current_y -= arc_offset
            
            # Draw projectile based on type
            if projectile.projectile_type == ProjectileType.ARROW:
                # Arrow
                pygame.draw.line(
                    self.screen,
                    COLORS['arrow_shaft'],
                    (int(current_x), int(current_y)),
                    (int(current_x - 5), int(current_y + 5)),
                    2
                )
                pygame.draw.circle(
                    self.screen,
                    COLORS['arrow_head'],
                    (int(current_x), int(current_y)),
                    2
                )
            elif projectile.projectile_type == ProjectileType.STONE:
                # Stone
                pygame.draw.circle(
                    self.screen,
                    (120, 120, 120),
                    (int(current_x), int(current_y)),
                    4
                )
            else:
                # Default projectile
                pygame.draw.circle(
                    self.screen,
                    (200, 180, 160),
                    (int(current_x), int(current_y)),
                    3
                )
    
    def _render_effects(self, effects: List[ParticleEffect]):
        """Render particle effects"""
        for effect in effects:
            screen_pos = self._grid_to_screen(effect.position.x, effect.position.y)
            alpha = int(255 * (1 - effect.elapsed / effect.lifetime))
            
            if effect.effect_type == "dust":
                # Dust cloud
                for i in range(5):
                    offset_x = (i - 2) * 3
                    offset_y = (i - 2) * 2
                    color = (*COLORS['dust'][:3], alpha // 2)
                    pygame.draw.circle(
                        self.screen,
                        color[:3],  # pygame doesn't support alpha in draw
                        (screen_pos[0] + self.cell_size // 2 + offset_x,
                         screen_pos[1] + self.cell_size // 2 + offset_y),
                        4
                    )
            
            elif effect.effect_type == "sparks":
                # Combat sparks
                for i in range(4):
                    angle = i * 90
                    offset_x = int(8 * (1 - effect.elapsed / effect.lifetime) * (i % 2 * 2 - 1))
                    offset_y = int(8 * (1 - effect.elapsed / effect.lifetime) * (i // 2 * 2 - 1))
                    pygame.draw.circle(
                        self.screen,
                        COLORS['sparks'],
                        (screen_pos[0] + self.cell_size // 2 + offset_x,
                         screen_pos[1] + self.cell_size // 2 + offset_y),
                        2
                    )
            
            elif effect.effect_type == "impact":
                # Impact effect
                radius = int(10 * (1 - effect.elapsed / effect.lifetime))
                pygame.draw.circle(
                    self.screen,
                    COLORS['impact'],
                    (screen_pos[0] + self.cell_size // 2,
                     screen_pos[1] + self.cell_size // 2),
                    radius,
                    2
                )
    
    def _render_selection(self, battle_state: BattleState):
        """Render selection indicators and target markers"""
        if not battle_state.selected_unit_id:
            return
        
        selected_unit = battle_state._find_unit_by_id(battle_state.selected_unit_id)
        if not selected_unit or not selected_unit.target_unit_id:
            return
        
        target_unit = battle_state._find_unit_by_id(selected_unit.target_unit_id)
        if not target_unit:
            return
        
        # Draw line from selected to target
        start_pos = self._grid_to_screen(selected_unit.position.x, selected_unit.position.y)
        end_pos = self._grid_to_screen(target_unit.position.x, target_unit.position.y)
        
        pygame.draw.line(
            self.screen,
            COLORS['target_marker'],
            (start_pos[0] + self.cell_size // 2, start_pos[1] + self.cell_size // 2),
            (end_pos[0] + self.cell_size // 2, end_pos[1] + self.cell_size // 2),
            2
        )
    
    def _render_ui_panel(self, battle_state: BattleState):
        """Render the bottom UI panel"""
        panel_rect = pygame.Rect(
            0,
            self.battle_view_height,
            self.screen_width,
            self.ui_panel_height
        )
        
        # Panel background
        pygame.draw.rect(self.screen, COLORS['ui_background'], panel_rect)
        pygame.draw.line(
            self.screen,
            COLORS['ui_border'],
            (0, self.battle_view_height),
            (self.screen_width, self.battle_view_height),
            3
        )
    
    def _render_commander_portraits(self, battle_state: BattleState):
        """Render commander portraits with health/morale bars"""
        portrait_size = 80
        portrait_y = self.battle_view_height + 20
        
        # Attacker portrait (left)
        if battle_state.attacker:
            self._render_commander_panel(
                battle_state.attacker,
                40,
                portrait_y,
                portrait_size
            )
        
        # Defender portrait (right)
        if battle_state.defender:
            self._render_commander_panel(
                battle_state.defender,
                self.screen_width - 240,
                portrait_y,
                portrait_size
            )
    
    def _render_commander_panel(self, army: Army, x: int, y: int, size: int):
        """Render a single commander panel"""
        # Portrait frame
        frame_color = COLORS['attacker_primary'] if army.side == ArmySide.ATTACKER else COLORS['defender_primary']
        portrait_rect = pygame.Rect(x, y, size, size)
        
        pygame.draw.rect(self.screen, frame_color, portrait_rect)
        pygame.draw.rect(self.screen, COLORS['ui_border'], portrait_rect, 3)
        
        # Commander name
        name_text = self.font_small.render(army.commander.name, True, COLORS['ui_border'])
        self.screen.blit(name_text, (x + size + 10, y + 5))
        
        # Health bar
        bar_x = x + size + 10
        bar_y = y + 30
        bar_width = 150
        bar_height = 12
        
        pygame.draw.rect(self.screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
        
        health_pct = army.commander.health / army.commander.max_health
        health_fill = int(bar_width * health_pct)
        pygame.draw.rect(self.screen, COLORS['health_green'], (bar_x, bar_y, health_fill, bar_height))
        
        health_label = self.font_small.render(
            f"Health: {army.commander.health}/{army.commander.max_health}",
            True,
            (200, 200, 200)
        )
        self.screen.blit(health_label, (bar_x, bar_y - 15))
        
        # Morale bar
        morale_y = bar_y + 20
        pygame.draw.rect(self.screen, (40, 40, 40), (bar_x, morale_y, bar_width, bar_height))
        
        morale_pct = army.total_morale / army.max_morale
        morale_fill = int(bar_width * morale_pct)
        pygame.draw.rect(self.screen, COLORS['morale_blue'], (bar_x, morale_y, morale_fill, bar_height))
        
        morale_label = self.font_small.render(
            f"Morale: {army.total_morale}/{army.max_morale}",
            True,
            (200, 200, 200)
        )
        self.screen.blit(morale_label, (bar_x, morale_y - 15))
        
        # Unit count
        alive_units = len(army.get_alive_units())
        total_units = len(army.units)
        units_text = self.font_small.render(
            f"Units: {alive_units}/{total_units}",
            True,
            (200, 200, 200)
        )
        self.screen.blit(units_text, (bar_x, morale_y + 20))
    
    def _render_phase_indicator(self, battle_state: BattleState):
        """Render the current battle phase"""
        phase_text = battle_state.phase.value.upper().replace('_', ' ')
        text_surface = self.font_large.render(phase_text, True, (255, 255, 200))
        
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen_width // 2
        text_rect.y = self.battle_view_height + 10
        
        # Background
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
        pygame.draw.rect(self.screen, COLORS['ui_border'], bg_rect, 2)
        
        self.screen.blit(text_surface, text_rect)
        
        # Battle timer
        time_text = self.font_medium.render(
            f"Time: {int(battle_state.battle_time)}s",
            True,
            (180, 180, 180)
        )
        time_rect = time_text.get_rect()
        time_rect.centerx = self.screen_width // 2
        time_rect.y = text_rect.bottom + 5
        self.screen.blit(time_text, time_rect)
    
    def _grid_to_screen(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """Convert grid coordinates to screen coordinates"""
        return (grid_x * self.cell_size, grid_y * self.cell_size)
    
    def screen_to_grid(self, screen_x: int, screen_y: int) -> GridPosition:
        """Convert screen coordinates to grid position"""
        grid_x = screen_x // self.cell_size
        grid_y = screen_y // self.cell_size
        return GridPosition(grid_x, grid_y)


def main():
    """Main game loop example"""
    renderer = BattleRenderer()
    renderer.initialize_pygame()
    
    battle = create_sample_battle()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0  # 60 FPS, delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    grid_pos = renderer.screen_to_grid(*event.pos)
                    # Find unit at position
                    for army in [battle.attacker, battle.defender]:
                        if army:
                            for unit in army.units:
                                if (unit.position.x == grid_pos.x and 
                                    unit.position.y == grid_pos.y):
                                    battle.select_unit(unit.unit_id)
                                    print(f"Selected: {unit.unit_id}")
                                    break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Toggle pause (simplified)
                    print("Space pressed")
                elif event.key == pygame.K_a:
                    # Order selected unit to attack
                    if battle.selected_unit_id:
                        print(f"Attack command for {battle.selected_unit_id}")
        
        # Update battle state
        if battle.phase != BattlePhase.VICTORY:
            battle.update(dt)
        
        # Render
        renderer.render_frame(battle)
    
    pygame.quit()


if __name__ == "__main__":
    main()
