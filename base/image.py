from pathlib import Path
from typing import List, NoReturn, Tuple, Union

import numpy as np
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from numpy import ndarray

from base.colours import Colours
from base.sprite_mappings import SpriteMapperContainer, SpriteMapperVegetation
from base.sprites import Sprites
from settings import RESOURCES_DIR
from utils.log import get_logger


class WorldmapSprites:
    # Image size is 300x225 pixels

    WMAP_DIR: Path = Path(RESOURCES_DIR / 'worldmap').resolve()
    WMAP_PP_DIR: Path = WMAP_DIR / 'resources'

    DEFAULT_CANVAS_SIZE: Tuple[int, int, int] = (225, 300, 4,)
    DEFAULT_FALLBACK_SPRITE: Image = Image.fromarray(np.zeros(DEFAULT_CANVAS_SIZE).astype(np.uint8))

    def __init__(self, canvas_size: Tuple[int, int, int] = DEFAULT_CANVAS_SIZE):
        """Class containing worldmap sprites and base adjustment logic"""

        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

        self.blank_canvas: ndarray = np.ones(canvas_size)
        self.empty_array: ndarray = np.zeros(canvas_size)
        self.empty: Image = Image.fromarray(self.empty_array.astype(np.uint8))

        self.COLRS: Colours = Colours(blank_canvas=self.blank_canvas, empty_array=self.empty_array)
        self.SPRITES: Sprites = Sprites(empty=self.empty)

        self.sprite_mappers = SpriteMapperContainer(
            sprite_mappers=[
                SpriteMapperVegetation(fallback_sprite=self.empty)
            ]
        )

        # Crop values
        # self.crop = [(0,0,300,225), (300,0,600,225), (600,0,900,225)]

    def create_required_sprite(self, climate_id: int, relief_id: int, vegetation_id: int, water_id: int,
                               world_object_id: int, coastal_adjacency: List[int], river_adjacency: List[int],
                               pixmap_flag: bool = True, scale: Union[int, float] = 1) -> type(Image):
        # Background first
        # scale = (0.5, 0.5,)
        background, flag_ground = self.select_background(climate_id)

        if climate_id != 0:
            relief, flag_relief = self.select_relief_sprite(relief_id)
        else:
            flag_relief = False

        grass, flag_grass = self.add_grass_sprite(climate_id, relief_id)
        vegatation, flag_veg = self.select_vegetation_sprite(vegetation_id, climate_id, relief_id)

        if climate_id != 0:
            coast, flag_coast, second_coast, second_flagcoast = self.select_coast_sprite(coastal_adjacency)
            corner, flag_corner, second_corner, second_flagcorner = self.select_corner_sprite(coastal_adjacency)
        else:
            flag_coast, flag_corner, second_flagcorner = False, False, False

        if water_id != 0:
            water, flag_water = self.select_water_sprite(water_id, river_adjacency, coastal_adjacency)
        else:
            flag_water = False

        if water_id not in (0, 4, 5):
            river_size, flag_river = self.select_river_size_sprite(water_id)
        else:
            flag_river = False

        prim, flagPrim = self.check_prim(world_object_id)

        if not flag_ground:
            self.logger.warning('NO BACKGROUND FOUND')

        background_image = Image.fromarray(background.astype(np.uint8))
        # background_image = background

        if flag_relief:
            background_image.alpha_composite(relief)

        if flag_grass:
            background_image.alpha_composite(grass)

        if flag_coast:
            background_image.alpha_composite(coast)
            if second_flagcoast:
                background_image.alpha_composite(second_coast)

        if flag_corner:
            background_image.alpha_composite(corner)
            if second_flagcorner:
                background_image.alpha_composite(second_corner)

        if flag_veg:
            background_image.alpha_composite(vegatation)

        if flag_water:
            background_image.alpha_composite(water)

        if flag_river:
            background_image.alpha_composite(river_size)

        if flagPrim:
            background_image.alpha_composite(prim)

        if pixmap_flag:
            background_image = ImageQt.ImageQt(background_image)
            background_image = QPixmap.fromImage(background_image)

        return background_image

    def select_river_size_sprite(self, water_id):

        river_sprite_dict = {1: self.SPRITES.sprite_river_small,
                             2: self.SPRITES.sprite_river_medium,
                             3: self.SPRITES.sprite_river_large}
        try:
            return river_sprite_dict[water_id], True
        except KeyError:
            return self.empty, False

    def select_background(self, climate_id: int) -> Tuple[ndarray, bool]:
        return self.COLRS.BACKGROUND[climate_id], True

    def select_relief_sprite(self, relief_id: int) -> Tuple[type(Image), bool]:
        n = np.random.randint(0, 3)
        return self.SPRITES.RELIEF[relief_id].crop(self.create_crop(self.SPRITES.RELIEF[relief_id])[n]), True

    def select_vegetation_sprite(self, vegetation_id: int, climate_id: int, relief_id: int) -> Tuple[type(Image), bool]:

        vegetation_sprite, flag_found = \
            self.sprite_mappers['VEGETATION'].get_sprite(
                climate_id=climate_id,
                vegetation_id=vegetation_id,
                relief_id=relief_id)

        n: int = np.random.randint(0, 3)
        vegetation_sprite.crop(self.create_crop(vegetation_sprite)[n])
        return vegetation_sprite, flag_found

    def select_water_sprite(self, water_id: int, river_adjacency: List[int],
                            coastal_adjacency: List[int]) -> Tuple[type(Image), bool]:
        """Method contains logic for generating world map rivers.
         River ID's are the following;
        WATER = ("NONE", "RIVER_SMALL", "RIVER_MED", "RIVER_LARGE", "LAKE", "SWAMP",)
        Note, if water_id is 0 (so no water) this function is NOT called.
         """
        # ! TODO: EVERYTHING AGAIN THIS IS GARBAGE
        # set constants etc.
        n = np.random.randint(0, 3)
        found_flag = False
        water_sprite = self.empty
        river_adjacency = np.asarray(river_adjacency)
        coastal_adjacency = np.asarray(coastal_adjacency)

        # When water_id is a lake, return lake sprite.
        if water_id == 4:
            water_sprite = self.SPRITES.sprite_lake
            water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
            found_flag = True

        # When water_id is a swamp, return swamp sprite.
        elif water_id == 5:
            water_sprite = self.SPRITES.sprite_swamp
            water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
            found_flag = True

        # water_id is a river type.
        else:
            # First determine if it's a crossing
            nr_river = sum(river_adjacency[[0, 2, 4, 6]])
            nr_coast = sum(coastal_adjacency[[0, 2, 4, 6]])

            # Detect when a crossing should be used, total of 2 cases;
            # First case: 3 adjacent rivers
            # Second case: 2 adjacent rivers and an adjacent coast.
            crossing = nr_river >= 3 or (nr_coast == 1 and nr_river == 2)

            # Check for coastal rivers, either solo, or should be next to coast.
            solo_river = (nr_river == 0 and nr_coast == 1)
            next_to_coast = nr_coast >= 1

            # River starts only have 1 river next to them, and never a coast.
            river_start = (nr_river == 1 and nr_coast == 0)

            # First put in river mouths.
            # cases;
            # Mouth has to be nextToCoast. Then it can be normal mouth, or river crossing, or soloRiver.
            if next_to_coast:
                # !TODO revisit logic and make more readable
                if solo_river:
                    if coastal_adjacency[0] == 1:
                        water_sprite = self.SPRITES.sprite_river_start_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[2] == 1:
                        water_sprite = self.SPRITES.sprite_river_start_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[4] == 1:
                        water_sprite = self.SPRITES.sprite_river_start_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[6] == 1:
                        water_sprite = self.SPRITES.sprite_river_start_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                elif crossing:
                    adjacencySum = coastal_adjacency + river_adjacency
                    if adjacencySum[0] >= 1 and adjacencySum[2] >= 1 and adjacencySum[4] >= 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif adjacencySum[2] >= 1 and adjacencySum[4] >= 1 and adjacencySum[6] >= 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif adjacencySum[4] >= 1 and adjacencySum[6] >= 1 and adjacencySum[0] >= 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif adjacencySum[6] >= 1 and adjacencySum[0] >= 1 and adjacencySum[2] >= 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                else:
                    if coastal_adjacency[0] == 1 and river_adjacency[4] == 1:
                        water_sprite = self.SPRITES.sprite_river_mouth_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[2] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.SPRITES.sprite_river_mouth_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[4] == 1 and river_adjacency[0] == 1:
                        water_sprite = self.SPRITES.sprite_river_mouth_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif coastal_adjacency[6] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.SPRITES.sprite_river_mouth_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[0] == 1 and river_adjacency[2] == 1) or (
                            coastal_adjacency[2] == 1 and river_adjacency[0] == 1):
                        water_sprite = self.SPRITES.sprite_river_top_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[0] == 1 and river_adjacency[6] == 1) or (
                            coastal_adjacency[6] == 1 and river_adjacency[0] == 1):
                        water_sprite = self.SPRITES.sprite_river_top_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[2] == 1 and river_adjacency[4] == 1) or (
                            coastal_adjacency[4] == 1 and river_adjacency[2] == 1):
                        water_sprite = self.SPRITES.sprite_river_bottom_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif (coastal_adjacency[4] == 1 and river_adjacency[6] == 1) or (
                            coastal_adjacency[6] == 1 and river_adjacency[4] == 1):
                        water_sprite = self.SPRITES.sprite_river_bottom_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
            elif river_start:
                if river_adjacency[0] == 1:
                    water_sprite = self.SPRITES.sprite_river_start_top
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
                elif river_adjacency[2] == 1:
                    water_sprite = self.SPRITES.sprite_river_start_left
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
                elif river_adjacency[4] == 1:
                    water_sprite = self.SPRITES.sprite_river_start_bottom
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
                elif river_adjacency[6] == 1:
                    water_sprite = self.SPRITES.sprite_river_start_right
                    water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                    found_flag = True
            elif not next_to_coast:
                if not crossing:
                    if river_adjacency[0] == 1 and river_adjacency[4] == 1:
                        water_sprite = self.SPRITES.sprite_river_vertical
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[2] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.SPRITES.sprite_river_horizontal
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[0] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.SPRITES.sprite_river_top_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[0] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.SPRITES.sprite_river_top_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[4] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.SPRITES.sprite_river_bottom_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[4] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.SPRITES.sprite_river_bottom_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                if crossing:
                    if river_adjacency[0] == 1 and river_adjacency[2] == 1 and river_adjacency[4] == 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_left
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[2] == 1 and river_adjacency[4] == 1 and river_adjacency[6] == 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_bottom
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[4] == 1 and river_adjacency[6] == 1 and river_adjacency[0] == 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_right
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True
                    elif river_adjacency[6] == 1 and river_adjacency[0] == 1 and river_adjacency[2] == 1:
                        water_sprite = self.SPRITES.sprite_river_crossing_top
                        water_sprite = water_sprite.crop(self.create_crop(water_sprite)[n])
                        found_flag = True

            # If nothing is found return something
        if water_id in [1,2,3] and not found_flag:
            n = np.random.randint(4)
            temp = [self.SPRITES.sprite_river_start_bottom, self.SPRITES.sprite_river_start_left,
             self.SPRITES.sprite_river_start_top, self.SPRITES.sprite_river_start_right]
            water_sprite = temp[n]
            found_flag = True
        return water_sprite, found_flag

    def add_grass_sprite(self, climate_id: int, relief_id: int) -> Tuple[type(Image), bool]:
        n = np.random.randint(0, 3)

        grass_sprite = self.empty
        grass_flag = False

        climdict = {1: self.COLRS.COLOUR_CONTINENTAL,
                    2: self.COLRS.COLOUR_OCEANIC,
                    3: self.COLRS.COLOUR_MEDITERRANEAN,
                    4: self.COLRS.COLOUR_TROPICAL,
                    5: self.COLRS.COLOUR_ARID,
                    7: self.COLRS.COLOUR_NORDIC}
        if climate_id != 0 and climate_id != 6 and climate_id != 8 and climate_id != -1 and relief_id != 4:
            grass_sprite = self.SPRITES.sprite_grass
            grass_sprite = grass_sprite.crop(self.create_crop(grass_sprite)[n])

            try:
                colour = climdict[climate_id] / 255
            except KeyError:
                self.logger.debug("Keyerror grass_sprite for climate_id %d (this may be intended behaviour; EAFP)")
                self.logger.debug('Unknown climate_id, debug...')
                colour = np.array([1, 1, 1, 1])

            grass_sprite = np.array(grass_sprite) * colour
            grass_sprite = Image.fromarray(grass_sprite.astype(np.uint8))
            grass_flag = True

        return grass_sprite, grass_flag

    def check_prim(self, world_object_id: int) -> Tuple[type(Image), bool]:
        prim_flag = False
        prim_sprite = self.empty
        if world_object_id == 1:
            prim_flag = True
            prim_sprite = self.SPRITES.sprite_primitive
        return prim_sprite, prim_flag

    def select_coast_sprite(self, coastal_adjacency: List[int]) -> Tuple[type(Image), bool, type(Image), bool]:
        #     topID = n - self.xWidth
        #     topLeftID = n - self.xWidth - 1
        #     leftID = n - 1
        #     bottomLeftID = n + self.xWidth - 1
        #     bottomID = n + self.xWidth
        #     bottomRightID = n + self.xWidth + 1
        #     rightID = n + 1
        #     topRightID = n - self.xWidth + 1
        coast_id: List[int] = [0, 2, 4, 6]
        n: int = np.random.randint(0, 3)
        coast_sprite: type(Image) = self.empty
        coast_flag: bool = False
        second_coast_sprite: type(Image) = self.empty
        second_coast_flag: bool = False

        coastal_adjacency = np.asarray(coastal_adjacency)
        if coastal_adjacency[coast_id].sum() == 1:
            if coastal_adjacency[0] == 1:
                coast_sprite = self.SPRITES.sprite_coast_top
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
            if coastal_adjacency[2] == 1:
                coast_sprite = self.SPRITES.sprite_coast_left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
            if coastal_adjacency[4] == 1:
                coast_sprite = self.SPRITES.sprite_coast_bottom
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
            if coastal_adjacency[6] == 1:
                coast_sprite = self.SPRITES.sprite_coast_right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True
        if coastal_adjacency[coast_id].sum() == 2:
            if coastal_adjacency[0] == 1 and coastal_adjacency[2] == 1:
                coast_sprite = self.SPRITES.sprite_coast_top_left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[2] == 1 and coastal_adjacency[4] == 1:
                coast_sprite = self.SPRITES.sprite_coast_bottom_left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[4] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.SPRITES.sprite_coast_bottom_right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[0] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.SPRITES.sprite_coast_top_right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[0] == 1 and coastal_adjacency[4] == 1:
                coast_sprite = self.SPRITES.sprite_coast_top
                second_coast_sprite = self.SPRITES.sprite_coast_bottom
                coast_flag = True
                second_coast_flag = True

            if coastal_adjacency[2] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.SPRITES.sprite_coast_left
                second_coast_sprite = self.SPRITES.sprite_coast_right
                coast_flag = True
                second_coast_flag = True

        if coastal_adjacency[coast_id].sum() == 3:
            if coastal_adjacency[0] == 1 and coastal_adjacency[2] == 1 and coastal_adjacency[4] == 1:
                coast_sprite = self.SPRITES.sprite_coast_3left
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[2] == 1 and coastal_adjacency[4] == 1 and coastal_adjacency[6] == 1:
                coast_sprite = self.SPRITES.sprite_coast_3bottom
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[4] == 1 and coastal_adjacency[6] == 1 and coastal_adjacency[0] == 1:
                coast_sprite = self.SPRITES.sprite_coast_3right
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

            if coastal_adjacency[6] == 1 and coastal_adjacency[0] == 1 and coastal_adjacency[2] == 1:
                coast_sprite = self.SPRITES.sprite_coast_3top
                coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
                coast_flag = True

        if coastal_adjacency[coast_id].sum() == 4:
            coast_sprite = self.SPRITES.sprite_coast4
            coast_sprite = coast_sprite.crop(self.create_crop(coast_sprite)[n])
            coast_flag = True

        return coast_sprite, coast_flag, second_coast_sprite, second_coast_flag

    def select_corner_sprite(self, coastal_adjacency: List[int]) -> Tuple[type(Image), bool, type(Image), bool]:
        # bottomleft, bottomright, topright, topleft
        corner_sprite = self.empty
        corner_flag = False
        corner_sprite_secondary = self.empty
        corner_flag_secondary = False
        coastal_adjacency = np.asarray(coastal_adjacency)

        if (coastal_adjacency[0] == 0) and (coastal_adjacency[1] == 1) and (coastal_adjacency[2] == 0):
            corner_sprite = self.SPRITES.sprite_coast_corner_top_left
            corner_flag = True

        if coastal_adjacency[2] == 0 and coastal_adjacency[3] == 1 and coastal_adjacency[4] == 0:
            if corner_flag:
                corner_sprite_secondary = self.SPRITES.sprite_coast_corner_bottom_left
                corner_flag_secondary = True
                return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary
            corner_sprite = self.SPRITES.sprite_coast_corner_bottom_left
            corner_flag = True

        if coastal_adjacency[4] == 0 and coastal_adjacency[5] == 1 and coastal_adjacency[6] == 0:
            if corner_flag:
                corner_sprite_secondary = self.SPRITES.sprite_coast_corner_bottom_right
                corner_flag_secondary = True
                return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary
            corner_sprite = self.SPRITES.sprite_coast_corner_bottom_right
            corner_flag = True

        if coastal_adjacency[6] == 0 and coastal_adjacency[7] == 1 and coastal_adjacency[0] == 0:
            if corner_flag:
                corner_sprite_secondary = self.SPRITES.sprite_coast_corner_top_right
                corner_flag_secondary = True
                return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary
            corner_sprite = self.SPRITES.sprite_coast_corner_top_right
            corner_flag = True

        return corner_sprite, corner_flag, corner_sprite_secondary, corner_flag_secondary

    @staticmethod
    def create_crop(image: type(Image)) -> NoReturn:
        return [(0, 0, image.size[0] / 3, image.size[1]), (image.size[0] / 3, 0, 2 * image.size[0] / 3, image.size[1]),
                (2 * image.size[0] / 3, 0, 3 * image.size[0] / 3, image.size[1])]

    def scale_sprites(self, scale):
        self.COLRS = Colours(self.blank_canvas, self.empty_array)

        for sprite in self.SPRITES.__dict__:
            if self.SPRITES.sprt_keyw in sprite:
                temp = self.SPRITES.__getattribute__(sprite)
                temp.thumbnail(temp.size[0] * scale[0], temp.size[1] * scale[1], Image.ANTIALIAS)

        x = self.SPRITES.sprite_plains.size[0]
        y = self.SPRITES.sprite_plains.size[1]
        self.blank_canvas: ndarray = np.ones((y, x, 4))
        self.empty_array: ndarray = np.zeros((y, x, 4))
