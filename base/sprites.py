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

    plains = Image.open(WMAP_DIR / 'world_grassland.png')
    flat = plains
    rocky = Image.open(WMAP_DIR / 'world_rocky.png')
    hills = Image.open(WMAP_DIR / 'world_hills.png')
    mountains = Image.open(WMAP_DIR / 'world_mountains.png')

    RELIEF: Optional[Tuple[Union[type(Image), ndarray], ...]] = None

    # Vegetation
    grass = Image.open(WMAP_DIR / 'world_grass_1.png')
    cont_forest = Image.open(WMAP_DIR / 'world_continental_forest.png')
    cont_trees = Image.open(WMAP_DIR / 'world_continental_trees.png')
    oceanic_forest = Image.open(WMAP_DIR / 'world_oceanic_forest.png')
    oceanic_trees = Image.open(WMAP_DIR / 'world_oceanic_trees.png')
    medi_forest = Image.open(WMAP_DIR / 'world_mediterran_forest.png')
    medi_trees = Image.open(WMAP_DIR / 'world_mediterran_trees.png')
    tropical_forest = Image.open(WMAP_DIR / 'world_tropical_forest.png')
    tropical_trees = Image.open(WMAP_DIR / 'world_tropical_trees.png')
    arid_forest = Image.open(WMAP_DIR / 'world_arid_forest.png')
    arid_trees = Image.open(WMAP_DIR / 'world_arid_trees.png')
    nordic_forest = Image.open(WMAP_DIR / 'world_nordic_forest.png')
    nordic_trees = Image.open(WMAP_DIR / 'world_nordic_trees.png')

    # Water
    lake = Image.open(WMAP_DIR / 'world_lake.png')
    swamp = Image.open(WMAP_DIR / 'world_swamp.png')

    # Straight
    river_horizontal = Image.open(WMAP_PP_DIR / 'world_river_horizontal.png')
    river_vertical = Image.open(WMAP_PP_DIR / 'world_river_vertical.png')

    # Corners
    river_bottom_left = Image.open(WMAP_PP_DIR / 'world_river_leftbottom.png')
    river_bottom_right = Image.open(WMAP_PP_DIR / 'world_river_rightbottom.png')
    river_top_left = Image.open(WMAP_PP_DIR / 'world_river_leftTop.png')
    river_top_right = Image.open(WMAP_PP_DIR / 'world_river_topright.png')

    # Crossings
    river_crossing_left = Image.open(WMAP_PP_DIR / 'world_river_crossing_left.png')
    river_crossing_top = Image.open(WMAP_PP_DIR / 'world_river_crossing_up.png')
    river_crossing_right = Image.open(WMAP_PP_DIR / 'world_river_crossing_right.png')
    river_crossing_bottom = Image.open(WMAP_PP_DIR / 'world_river_crossing_bottom.png')

    # Mouths
    river_mouth_left = Image.open(WMAP_PP_DIR / 'world_river_mouth_west.png')
    river_mouth_top = Image.open(WMAP_PP_DIR / 'world_river_mouth_north.png')
    river_mouth_right = Image.open(WMAP_PP_DIR / 'world_river_mouth_east.png')
    river_mouth_bottom = Image.open(WMAP_PP_DIR / 'world_river_mouth_south.png')

    # Starts
    river_start_left = Image.open(WMAP_PP_DIR / 'world_river_start_left.png')
    river_start_top = Image.open(WMAP_PP_DIR / 'world_river_start_up.png')
    river_start_right = Image.open(WMAP_PP_DIR / 'world_river_start_right.png')
    river_start_bottom = Image.open(WMAP_PP_DIR / 'world_river_start_bottom.png')
    crop_river = [(0, 0, river_start_left.size[0] / 3, river_start_left.size[1]),
                       (river_start_left.size[0] / 3, 0, 2 * river_start_left.size[0] / 3,
                        river_start_left.size[1]),
                       (2 * river_start_left.size[0] / 3, 0, 3 * river_start_left.size[0] / 3,
                        river_start_left.size[1])]
    # primitive = Image.open('./prim.png')

    # Coast
    coast_left = Image.open(WMAP_PP_DIR / 'world_coast_left.png')
    coast_bottom = Image.open(WMAP_PP_DIR / 'world_coast_bottom.png')
    coast_right = Image.open(WMAP_PP_DIR / 'world_coast_right.png')
    coast_top = Image.open(WMAP_PP_DIR / 'world_coast_top.png')

    coast_top_left = Image.open(WMAP_PP_DIR / 'world_coast_topleft.png')
    coast_top_right = Image.open(WMAP_PP_DIR / 'world_coast_topright.png')
    coast_bottom_right = Image.open(WMAP_PP_DIR / 'world_coast_bottomright.png')
    coast_bottom_left = Image.open(WMAP_PP_DIR / 'world_coast_bottomleft.png')

    coast_3top = Image.open(WMAP_PP_DIR / 'world_coast_3top.png')
    coast_3right = Image.open(WMAP_PP_DIR / 'world_coast_3right.png')
    coast_3bottom = Image.open(WMAP_PP_DIR / 'world_coast_3bottom.png')
    coast_3left = Image.open(WMAP_PP_DIR / 'world_coast_3left.png')

    coast4 = Image.open(WMAP_PP_DIR / 'world_coast_4surround.png')

    coast_corner_bottom_left = Image.open(WMAP_PP_DIR / 'world_coast_corner_bottomleft.png')
    coast_corner_bottom_right = Image.open(WMAP_PP_DIR / 'world_coast_corner_bottomright.png')
    coast_corner_top_left = Image.open(WMAP_PP_DIR / 'world_coast_corner_topleft.png')
    coast_corner_top_right = Image.open(WMAP_PP_DIR / 'world_coast_corner_toprigh.png')

    def __post_init__(self):
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

        self.RELIEF = (self.plains, self.flat, self.rocky, self.hills, self.mountains, self.empty,)

    # def get_color_attributes(self) -> List[Tuple[str,Any]]:
    #     """Returns list of tuples with attribute names related to SPRITES and their corresponding values"""
    #     return [(attr, self.__getattribute__(attr),) for attr in self.__dict__ if self.sprt_keyw in attr]
