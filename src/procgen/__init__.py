"""
Procedural generation module.
"""

from src.procgen.campaign_generator import CampaignGenerator
# from src.procgen.battle_map_generator import BattleMapGenerator  # Disabled (hex-based, not used in 4v4 formation battles)
from src.procgen.encounter_generator import EncounterGenerator
from src.procgen.tile_map_generator import TileMapGenerator, TileType

__all__ = [
    'CampaignGenerator',
    # 'BattleMapGenerator',  # Disabled
    'EncounterGenerator',
    'TileMapGenerator',
    'TileType',
]
