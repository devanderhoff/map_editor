from typing import Any, List, NoReturn, Optional, Tuple

import numpy as np
from PIL import Image
from PyQt5.QtCore import QObject, pyqtSignal

from base.image import WorldmapSprites
from base.region import Region
from game_objects.object_types import UtilityType, ClimateType, ReliefType, VegetationType, WaterType, WorldObjectType
from utils.log import get_logger


class World(QObject):

    def __init__(self, region_info_signal):
        super().__init__()

        self.worldname = 'insert name here'
        self.pixmap_flag = True  # Use pixmaps instead of PIL images.
        self.region_check_queue = []  # Queue of regions that have to rebuild their sprite.

        self.x_width: Optional[int] = None  # Width of the base.
        self.y_height: Optional[int] = None  # Height of the base.

        self.nr_regions: Optional[int] = None  # nr of regions in the base.
        self.region_names: Optional[List[str]] = None  # region names
        self.xy_regions: Optional[Tuple[int, int]] = None  # x and y coordinates of the region. (0,0) is top left.
        self.region_info_lst: Optional[
            List[Any]] = None  # List containing region information, climate_id, water_id etc.
        self.region_info_slice: Optional[List[int]] = None  # Start location to splice region information list.
        self.regions: Optional[List[Region]] = None  # Contains region objects which hold region info.
        self.region_signal_lst: Optional[List[pyqtSignal]] = \
            None  # list containing copies of the PyQt signal_flag to be send to region during init

        # Sprite related stuff
        self.sprite_generator: WorldmapSprites = WorldmapSprites()  # Initialize sprite builder
        self.scale = (1, 1,)
        self.worldmap_image: Optional[type(Image)] = None  # Hold created full worldmap image.

        self.region_info_signal = region_info_signal
        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

    def create_new_world(self, name: str, width: int, height: int, random_climate: bool,
                         scale: Tuple[int, int] = (1, 1)):
        """Create new world functionality"""

        # !TODO scale parameter unused?
        self.worldname = name
        self.x_width: int = width
        self.y_height: int = height

        # Create region base information.
        self.nr_regions, self.region_names, self.xy_regions, self.region_info_lst, self.region_info_slice = \
            self.create_region_base(random_climate=random_climate, loaded_file=False)

        # Populate base regions
        self.regions = self.create_regions()

        # Create initial sprites
        self.create_all_region_sprites()

    def load_world(self, filename) -> NoReturn:
        """Load world from .ybin file"""
        with open(filename, mode='rb') as file:
            self.region_info_lst = list(file.read())

        self.x_width = self.region_info_lst[0]
        self.y_height = self.region_info_lst[2]

        region_params = self.create_region_base(loaded_file=True)
        self.nr_regions, self.region_names, self.xy_regions, self.region_info_lst, self.region_info_slice = region_params

        self.regions = self.create_regions()
        self.create_all_region_sprites()

    def rebuild_region_list(self):
        """Rebuild region information before saving world. Placeholder for later"""
        region_list_base = [self.x_width, 0, self.y_height, 0]
        [region_list_base.extend(region.region_list) for region in self.regions]
        self.region_info_lst = region_list_base

    def create_all_region_sprites(self) -> NoReturn:
        """Create sprites for all region, by looping over and calling create_region_sprite for all."""
        self.logger.debug(f'{self.regions}')
        if self.regions:
            for region in self.regions:
                self.logger.debug("region.region_id: %d", region.region_id)
                self.create_region_sprite(region.region_id)

    def create_region_base(self, loaded_file: bool, random_climate: bool = False) -> NoReturn:
        """Create base information each region needs"""
        if self.x_width != 0 or self.y_height != 0:
            nr_regions = self.x_width * self.y_height
        else:
            raise ValueError('Width and height have to be > 0')
        region_names = [f'region_{x}_{y}' for y in range(self.y_height) for x in range(self.x_width)]
        xy_regions = [[x, y] for y in range(self.y_height) for x in range(self.x_width)]

        if loaded_file:
            region_information_list = self.region_info_lst
        elif random_climate:
            region_information_list = [self.x_width, 0, self.y_height, 0]

            for i in range(nr_regions):
                n = np.random.randint(0, 8)
                region_information_list.extend([n, 0, 0, 0, 0])
        else:
            region_information_list = [self.x_width, 0, self.y_height, 0] + ([-1, 0, 0, 0, 0] * nr_regions)

        region_information_slice = [*range(4, len(region_information_list), 5)]

        return nr_regions, region_names, xy_regions, region_information_list, region_information_slice

    def create_regions(self) -> List[Region]:
        """Populate the regions by creating Region() in the region list"""
        climate_id_list = [self.region_info_lst[idx] for idx in self.region_info_slice]
        relief_id_list = [self.region_info_lst[idx + 1] for idx in self.region_info_slice]
        vegetation_id_list = [self.region_info_lst[idx + 2] for idx in self.region_info_slice]
        water_id_list = [self.region_info_lst[idx + 3] for idx in self.region_info_slice]
        worldobject_id_list = [self.region_info_lst[idx + 4] for idx in self.region_info_slice]
        region_bytes_list = [self.region_info_lst[idx:idx + 5] for idx in self.region_info_slice]

        self.logger.debug('Creating regions..')
        # region_list = [
        #     Region(x, y, region_bytes, name, region_id, climate_id, relief_id, vegetation_id, water_id, worldobject_id,
        #            signal)
        #     for region_id, (
        #         [x, y], region_bytes, name, climate_id, relief_id, vegetation_id, water_id, worldobject_id, signal)
        #     in enumerate(
        #         zip(self.xy_regions, region_bytes, self.region_names, climate_id_list, relief_id_list,
        #             vegetation_id_list,
        #             water_id_list, worldobject_id_list, self.region_signal_lst))]
        # self.logger.debug("func create_regions: region list = %s", str(region_list))

        region_list = []
        for region_id, region_name in enumerate(self.region_names):
            [x, y] = self.xy_regions[region_id]
            region_bytes = region_bytes_list[region_id]
            name = self.region_names[region_id]
            climate_id = climate_id_list[region_id]
            relief_id = relief_id_list[region_id]
            vegetation_id = vegetation_id_list[region_id]
            water_id = water_id_list[region_id]
            worldobject_id = worldobject_id_list[region_id]

            region_list.append(
                Region(x=x, y=y,
                       region_bytes=region_bytes,
                       name=name,
                       region_id=region_id,
                       climate_id=climate_id,
                       relief_id=relief_id,
                       vegetation_id=vegetation_id,
                       water_id=water_id,
                       worldobject_id=worldobject_id,
                       region_info_signal=self.region_info_signal))
        self.logger.debug("func create_regions: region list = %s", str(region_list))
        return region_list

    def create_region_sprite(self, region_id, scale=(1, 1,), signal_flag: bool = False) -> NoReturn:
        self.logger.debug("func create_region_sprite(argument region_id = %d)", region_id)
        region = self.regions[region_id]
        self.generate_coastal_adjacency(region_id, signal_flag)
        self.generate_river_adjacency(region_id, signal_flag)
        sprite = self.sprite_generator.create_required_sprite(region.climate_id, region.relief_id,
                                                              region.vegetation_id, region.water_id,
                                                              region.world_object_id,
                                                              region.coastal_adjacency,
                                                              region.river_adjacency,
                                                              self.pixmap_flag,
                                                              scale)

        if self.pixmap_flag:
            region.setPixmap(sprite)
        else:
            region.region_sprite(sprite)
        region.region_changed = True

        if signal_flag:
            # self.logger.debug('Region_id_queue length: ', len(self.region_check_queue))
            for region_id_queue in self.region_check_queue:
                region = self.regions[region_id_queue]
                self.generate_river_adjacency(region_id_queue, not signal_flag)
                self.generate_coastal_adjacency(region_id_queue, not signal_flag)
                sprite = self.sprite_generator.create_required_sprite(region.climate_id, region.relief_id,
                                                                      region.vegetation_id, region.water_id,
                                                                      region.world_object_id,
                                                                      region.coastal_adjacency,
                                                                      region.river_adjacency,
                                                                      self.pixmap_flag,
                                                                      scale)
                if self.pixmap_flag:
                    region.setPixmap(sprite)
                else:
                    region.region_sprite(sprite)
            self.region_check_queue = []

    def generate_coastal_adjacency(self, region_id: int, signal: bool = False) -> NoReturn:
        # region = self.regions[region_id]
        n = region_id

        coastal_adjacency_temp = [0, 0, 0, 0, 0, 0, 0, 0]
        top_id = n - self.x_width
        top_left_id = n - self.x_width - 1
        left_id = n - 1
        bottom_left_id = n + self.x_width - 1
        bottom_id = n + self.x_width
        bottom_right_id = n + self.x_width + 1
        right_id = n + 1
        top_right_id = n - self.x_width + 1

        if 0 <= top_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[top_id].region_id)
            if self.regions[top_id].climate_id == 0:
                coastal_adjacency_temp[0] = 1

        if 0 <= top_left_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[top_left_id].region_id)
            if self.regions[top_left_id].climate_id == 0:
                coastal_adjacency_temp[1] = 1

        if 0 <= left_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[left_id].region_id)
            if self.regions[left_id].climate_id == 0:
                coastal_adjacency_temp[2] = 1

        if 0 <= bottom_left_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[bottom_left_id].region_id)
            if self.regions[bottom_left_id].climate_id == 0:
                coastal_adjacency_temp[3] = 1

        if 0 <= bottom_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[bottom_id].region_id)
            if self.regions[bottom_id].climate_id == 0:
                coastal_adjacency_temp[4] = 1

        if 0 <= bottom_right_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[bottom_right_id].region_id)
            if self.regions[bottom_right_id].climate_id == 0:
                coastal_adjacency_temp[5] = 1

        if 0 <= right_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[right_id].region_id)
            if self.regions[right_id].climate_id == 0:
                coastal_adjacency_temp[6] = 1

        if 0 <= top_right_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[top_right_id].region_id)
            if self.regions[top_right_id].climate_id == 0:
                coastal_adjacency_temp[7] = 1

        self.regions[n].coastal_adjacency = coastal_adjacency_temp

    def generate_river_adjacency(self, region_id, signal=False) -> NoReturn:
        # self.coastalAdjacency = self.createAdjacencyList()
        n = region_id
        river_adjacency_temp = [0, 0, 0, 0, 0, 0, 0, 0]
        top_id = n - self.x_width
        top_left_id = n - self.x_width - 1
        left_id = n - 1
        bottom_left_id = n + self.x_width - 1
        bottom_id = n + self.x_width
        bottom_right_id = n + self.x_width + 1
        right_id = n + 1
        top_right_id = n - self.x_width + 1
        check_list = [1, 2, 3]

        if 0 <= top_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[top_id].region_id)
            if self.regions[top_id].water_id in check_list:
                river_adjacency_temp[0] = 1
        if 0 <= top_left_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[top_left_id].region_id)
            if self.regions[top_left_id].water_id in check_list:
                river_adjacency_temp[1] = 1
        if 0 <= left_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[left_id].region_id)
            if self.regions[left_id].water_id in check_list:
                river_adjacency_temp[2] = 1
        if 0 <= bottom_left_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[bottom_left_id].region_id)
            if self.regions[bottom_left_id].water_id in check_list:
                river_adjacency_temp[3] = 1
        if 0 <= bottom_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[bottom_id].region_id)
            if self.regions[bottom_id].water_id in check_list:
                river_adjacency_temp[4] = 1
        if 0 <= bottom_right_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[bottom_right_id].region_id)
            if self.regions[bottom_right_id].water_id in check_list:
                river_adjacency_temp[5] = 1
        if 0 <= right_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[right_id].region_id)
            if self.regions[right_id].water_id in check_list:
                river_adjacency_temp[6] = 1
        if 0 <= top_right_id < self.nr_regions:
            if signal:
                self.region_check_queue.append(self.regions[top_right_id].region_id)
            if self.regions[top_right_id].water_id in check_list:
                river_adjacency_temp[7] = 1

        self.regions[n].river_adjacency = river_adjacency_temp

    def paint_region(self, region_id: int, brush_id: int, paint_id: int, scale: Tuple[int, int], signal_flag: bool = True):

        if type(brush) == UtilityType:
            if paint_id == 0:
                self.regions[region_id].climate = ClimateType(0)
                self.regions[region_id].relief = ReliefType(0)
                self.regions[region_id].vegetation = VegetationType(0)
                self.regions[region_id].water = WaterType(0)
                self.regions[region_id].world_object = WorldObjectType(0)
            elif paint_id == 1:
                self.regions[region_id].climate = ClimateType(1)
                self.regions[region_id].relief = ReliefType(1)
                self.regions[region_id].vegetation = VegetationType(0)
                self.regions[region_id].water = WaterType(0)
                self.regions[region_id].world_object = WorldObjectType(0)

        else:
            setattr(self.regions[region_id], brush, paint_id)

        # Recreate sprite with adjusted region values, include signal_flag = True to rebuild adjacent tiles.
        self.create_region_sprite(region_id, scale, signal_flag=signal_flag)

    def create_world_image(self) -> NoReturn:
        """Unused"""
        # !TODO method World.create_world_image() is not used.
        total_image_width = self._REGION_IMAGE_WIDTH * self.x_width
        total_image_height = self._REGION_IMAGE_HEIGHT * self.y_height
        self.worldmap_image = Image.new('RGB', (total_image_width, total_image_height))

        for region in self.regions:
            self.worldmap_image.paste(region.region_sprite, region.region_xy_to_img_coords(self._REGION_IMAGE_WIDTH,
                                                                                           self._REGION_IMAGE_HEIGHT))


class WorldSummary:
    string: str
    summary_lines: List[str]

    def __init__(self, regions: List[Region], init_only: bool = False):
        """
        Class for summarizing world properties; currently just provides a text world summary.

        :param regions: a list of regions used to build the summary
        :param init_only: (Optional) flag to set if the instance shouldn't immediately update the summary
            upon instantiation. (Default = False).
        """
        self.summary_lines = []
        self.string = ''
        if not init_only:
            self.update(regions)

    def update(self, regions: List[Region], linesep: str = ' \n'):

        climate_count: List[int] = [0] * 10
        climate_count_spawns: List[int] = [0] * 10
        relief_count: List[int] = [0] * 5
        forest_count: List[int] = [0]
        water_count: List[int] = [0] * 6

        if regions:
            for region in regions:
                climate_count[region.climate_id] += 1

                if region.world_object_id == 1:
                    climate_count_spawns[region.climate_id] += 1

                relief_count[region.relief_id] += 1

                if region.vegetation_id == 1:
                    forest_count += 1

                water_count[region.water_id] += 1

        self.summary_lines = \
            ['Climate count',
             '-------------------',
             f'Sea = {climate_count[0]}',
             f'Continental = {climate_count[1]}',
             f'Oceanic = {climate_count[2]}',
             f'Mediterranean = {climate_count[3]},'
             f'Tropical = {climate_count[4]}',
             f'Arid = {climate_count[5]}',
             f'Desert = {climate_count[6]}',
             f'Nordic = {climate_count[7]}',
             f'Polar = {climate_count[8]}',
             f'Unknown = {climate_count[9]}',
             f'\nRelief count',
             '-------------------',
             f'Flat = {relief_count[0]}',
             f'Plains = {relief_count[1]}',
             f'Rocky = {relief_count[2]}',
             f'Hills = {relief_count[3]}',
             f'Mountains = {relief_count[4]}'
             f'Forrest count = {forest_count}',
             f'Water counts\n-------------------\n',
             f'River small = {water_count[1]}',
             f'River medium = {water_count[2]}',
             f'River large = {water_count[3]}',
             f'Lakes = {water_count[4]}',
             f'Swamps = {water_count[5]}',
             f'\nPrimitives per climate',
             f'-------------------',
             f'Sea primitives = {climate_count_spawns[0]}',
             f'Continental primitives = {climate_count_spawns[1]}',
             f'Oceanic primitives = {climate_count_spawns[2]}',
             f'Mediterranean primitives = {climate_count_spawns[3]}',
             f'Tropical primitives = {climate_count_spawns[4]}',
             f'Arid primitives = {climate_count_spawns[5]}',
             f'Desert primitives = {climate_count_spawns[6]}',
             f'Nordic primitives = {climate_count_spawns[7]}',
             f'Polar primitives = {climate_count_spawns[8]}',
             f'Unknown primitives = {climate_count_spawns[9]}']

        self.string = linesep.join(self.summary_lines)

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"{type(self).__name__}(text={self.summary_lines[0]} ... {self.summary_lines[-1]})"
