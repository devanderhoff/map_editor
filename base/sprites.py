from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Any, Union, Optional

from PIL import Image
from numpy import ndarray

from settings import RESOURCES_DIR
from utils.log import get_logger


@dataclass
class Sprites:

    empty: ndarray

    WMAP_DIR = Path(RESOURCES_DIR / 'worldmap').resolve()
    WMAP_PP_DIR = WMAP_DIR / 'postprocess'
    sprt_keyw = 'sprite'

    sprite_plains = Image.open(WMAP_DIR / 'world_grassland.png')
    sprite_flat = sprite_plains
    sprite_rocky = Image.open(WMAP_DIR / 'world_rocky.png')
    sprite_hills = Image.open(WMAP_DIR / 'world_hills.png')
    sprite_mountains = Image.open(WMAP_DIR / 'world_mountains.png')

    RELIEF: Optional[Tuple[Union[type(Image), ndarray], ...]] = None

    # Vegetation
    sprite_grass = Image.open(WMAP_DIR / 'world_grass_1.png')
    sprite_cont_forest = Image.open(WMAP_DIR / 'world_continental_forest.png')
    sprite_cont_trees = Image.open(WMAP_DIR / 'world_continental_trees.png')
    sprite_oceanic_forest = Image.open(WMAP_DIR / 'world_oceanic_forest.png')
    sprite_oceanic_trees = Image.open(WMAP_DIR / 'world_oceanic_trees.png')
    sprite_medi_forest = Image.open(WMAP_DIR / 'world_mediterran_forest.png')
    sprite_medi_trees = Image.open(WMAP_DIR / 'world_mediterran_trees.png')
    sprite_tropical_forest = Image.open(WMAP_DIR / 'world_tropical_forest.png')
    sprite_tropical_trees = Image.open(WMAP_DIR / 'world_tropical_trees.png')
    sprite_arid_forest = Image.open(WMAP_DIR / 'world_arid_forest.png')
    sprite_arid_trees = Image.open(WMAP_DIR / 'world_arid_trees.png')
    sprite_nordic_forest = Image.open(WMAP_DIR / 'world_nordic_forest.png')
    sprite_nordic_trees = Image.open(WMAP_DIR / 'world_nordic_trees.png')

    # Water
    sprite_lake = Image.open(WMAP_DIR / 'world_lake.png')
    sprite_swamp = Image.open(WMAP_DIR / 'world_swamp.png')

    # Straight
    sprite_river_horizontal = Image.open(WMAP_PP_DIR / 'world_river_horizontal.png')
    sprite_river_vertical = Image.open(WMAP_PP_DIR / 'world_river_vertical.png')

    # Corners
    sprite_river_bottom_left = Image.open(WMAP_PP_DIR / 'world_river_leftbottom.png')
    sprite_river_bottom_right = Image.open(WMAP_PP_DIR / 'world_river_rightbottom.png')
    sprite_river_top_left = Image.open(WMAP_PP_DIR / 'world_river_leftTop.png')
    sprite_river_top_right = Image.open(WMAP_PP_DIR / 'world_river_topright.png')

    # Crossings
    sprite_river_crossing_left = Image.open(WMAP_PP_DIR / 'world_river_crossing_left.png')
    sprite_river_crossing_top = Image.open(WMAP_PP_DIR / 'world_river_crossing_up.png')
    sprite_river_crossing_right = Image.open(WMAP_PP_DIR / 'world_river_crossing_right.png')
    sprite_river_crossing_bottom = Image.open(WMAP_PP_DIR / 'world_river_crossing_bottom.png')

    # Mouths
    sprite_river_mouth_left = Image.open(WMAP_PP_DIR / 'world_river_mouth_west.png')
    sprite_river_mouth_top = Image.open(WMAP_PP_DIR / 'world_river_mouth_north.png')
    sprite_river_mouth_right = Image.open(WMAP_PP_DIR / 'world_river_mouth_east.png')
    sprite_river_mouth_bottom = Image.open(WMAP_PP_DIR / 'world_river_mouth_south.png')

    # Starts
    sprite_river_start_left = Image.open(WMAP_PP_DIR / 'world_river_start_left.png')
    sprite_river_start_top = Image.open(WMAP_PP_DIR / 'world_river_start_up.png')
    sprite_river_start_right = Image.open(WMAP_PP_DIR / 'world_river_start_right.png')
    sprite_river_start_bottom = Image.open(WMAP_PP_DIR / 'world_river_start_bottom.png')
    # crop_river = [(0, 0, river_start_left.size[0] / 3, river_start_left.size[1]),
    #                    (river_start_left.size[0] / 3, 0, 2 * river_start_left.size[0] / 3,
    #                     river_start_left.size[1]),
    #                    (2 * river_start_left.size[0] / 3, 0, 3 * river_start_left.size[0] / 3,
    #                     river_start_left.size[1])]
    # primitive = Image.open('./prim.png')

    # Coast
    sprite_coast_left = Image.open(WMAP_PP_DIR / 'world_coast_left.png')
    sprite_coast_bottom = Image.open(WMAP_PP_DIR / 'world_coast_bottom.png')
    sprite_coast_right = Image.open(WMAP_PP_DIR / 'world_coast_right.png')
    sprite_coast_top = Image.open(WMAP_PP_DIR / 'world_coast_top.png')

    sprite_coast_top_left = Image.open(WMAP_PP_DIR / 'world_coast_topleft.png')
    sprite_coast_top_right = Image.open(WMAP_PP_DIR / 'world_coast_topright.png')
    sprite_coast_bottom_right = Image.open(WMAP_PP_DIR / 'world_coast_bottomright.png')
    sprite_coast_bottom_left = Image.open(WMAP_PP_DIR / 'world_coast_bottomleft.png')

    sprite_coast_3top = Image.open(WMAP_PP_DIR / 'world_coast_3top.png')
    sprite_coast_3right = Image.open(WMAP_PP_DIR / 'world_coast_3right.png')
    sprite_coast_3bottom = Image.open(WMAP_PP_DIR / 'world_coast_3bottom.png')
    sprite_coast_3left = Image.open(WMAP_PP_DIR / 'world_coast_3left.png')

    sprite_coast4 = Image.open(WMAP_PP_DIR / 'world_coast_4surround.png')

    sprite_coast_corner_bottom_left = Image.open(WMAP_PP_DIR / 'world_coast_corner_bottomleft.png')
    sprite_coast_corner_bottom_right = Image.open(WMAP_PP_DIR / 'world_coast_corner_bottomright.png')
    sprite_coast_corner_top_left = Image.open(WMAP_PP_DIR / 'world_coast_corner_topleft.png')
    sprite_coast_corner_top_right = Image.open(WMAP_PP_DIR / 'world_coast_corner_toprigh.png')

    def __post_init__(self):
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

        self.RELIEF = (self.sprite_plains, self.sprite_flat, self.sprite_rocky, self.sprite_hills,
                       self.sprite_mountains, self.empty,)

    def get_sprite_attributes(self) -> List[Tuple[str,Any]]:
        """Returns list of tuples with attribute names related to SPRITES and their corresponding values"""
        return [(attr, self.__getattribute__(attr),) for attr in self.__dict__ if self.sprt_keyw in attr]

