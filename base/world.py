from typing import Optional, List, Tuple, Any, NoReturn

import numpy as np
from PIL import Image
from PyQt5.QtCore import pyqtSignal, QObject

from base.image import WorldmapSprites
from base.region import Region
from utils.log import get_logger
from pympler import asizeof


class World(QObject):

    def __init__(self, region_info_signal):
        super().__init__()

        self.worldname = 'insert name here'
        self.pixmap_flag = True  # Use pixmaps instead of PIL images.
        self.region_check_queue = []

        self.x_width: Optional[int] = None  # Width of the base.
        self.y_height: Optional[int] = None  # Height of the base.
        self.nr_regions: Optional[int] = None  # nr of regions in the base.
        self.region_names: Optional[List[str]] = None  # region names
        self.xy_regions: Optional[Tuple[int, int]] = None  # x and y coordinates of the region. (0,0) is top left.
        self.region_info_lst: Optional[
            List[Any]] = None  # List containing region information, climate_id, water_id etc.
        self.region_info_slice: Optional[List[int]] = None  # Start location to splice region information list.
        self.regions = None  # Contains region objects which hold region info.
        self.region_signal_lst: Optional[
            List[pyqtSignal]] = None  # list containing copies of the PyQt signal_flag to be send to region during init

        # Sprite related stuff
        self.sprite_generator: WorldmapSprites = WorldmapSprites()
        self.scale = (1, 1,)
        self.worldmap_image: Optional[type(Image)] = None  # Hold created full worldmap image.

        self.region_info_signal = region_info_signal
        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

    def create_new_world(self, name, width, height, random_climate, scale):
        self.name = name
        self.x_width: int = width
        self.y_height: int = height

        # Create region base information.
        self.nr_regions, self.region_names, self.xy_regions, self.region_info_lst, \
        self.region_info_slice = self.create_region_base(random_climate=random_climate,
                                                                                 loaded_file=False)
        # Populate base regions
        self.regions = self.create_regions()

        # Create initial sprites
        self.create_all_region_sprites()

    def load_world(self, filename) -> NoReturn:
        with open(filename, mode='rb') as file:
            self.region_info_lst = list(file.read())

        self.x_width = self.region_info_lst[0]
        self.y_height = self.region_info_lst[2]
        self.nr_regions, self.region_names, self.xy_regions, self.region_info_lst, \
        self.region_info_slice = self.create_region_base(loaded_file=True)
        self.regions = self.create_regions()
        # self.generate_coastal_adjacency()
        # self.generate_river_adjacency()
        self.create_all_region_sprites()

    def rebuild_region_list(self):
        region_list_base = [self.x_width, 0, self.y_height, 0]
        [region_list_base.extend(region.region_list) for region in self.regions]
        self.region_info_lst = region_list_base

    def create_all_region_sprites(self) -> NoReturn:
        self.logger.debug(f'{self.regions}')
        for region in self.regions:
            self.logger.debug("region.region_id: %d", region.region_id)
            # pool.apply(self.create_region_sprite, args=(region.region_id,))
            self.create_region_sprite(region.region_id)

    def create_world_image(self) -> NoReturn:
        total_image_width = self._REGION_IMAGE_WIDTH * self.x_width
        total_image_height = self._REGION_IMAGE_HEIGHT * self.y_height
        self.worldmap_image = Image.new('RGB', (total_image_width, total_image_height))

        for region in self.regions:
            self.worldmap_image.paste(region.region_sprite, region.region_xy_to_img_coords(self._REGION_IMAGE_WIDTH,
                                                                                           self._REGION_IMAGE_HEIGHT))

    def create_region_base(self, loaded_file: bool, random_climate: bool = False) -> NoReturn:
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

    def create_regions(self) -> NoReturn:
        climate_id_list = [self.region_info_lst[idx] for idx in self.region_info_slice]
        relief_id_list = [self.region_info_lst[idx + 1] for idx in self.region_info_slice]
        vegetation_id_list = [self.region_info_lst[idx + 2] for idx in self.region_info_slice]
        water_id_list = [self.region_info_lst[idx + 3] for idx in self.region_info_slice]
        worldobject_id_list = [self.region_info_lst[idx + 4] for idx in self.region_info_slice]
        region_bytes_list = [self.region_info_lst[idx:idx + 5] for idx in self.region_info_slice]

        self.logger.debug('create_regions says: test')
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
                Region(x, y, region_bytes, name, region_id, climate_id, relief_id, vegetation_id, water_id,
                       worldobject_id, self.region_info_signal))
        self.logger.debug("func create_regions: region list = %s", str(region_list))
        return region_list

    def create_region_sprite(self, region_id, scale=(1, 1,), signal_flag: bool = False) -> NoReturn:
        self.logger.debug("func create_region_sprite(argument region_id = %d)", region_id)
        region = self.regions[region_id]
        self.generate_coastal_adjacency(region_id, signal_flag)
        self.generate_river_adjacency(region_id, signal_flag)
        # self.sprite_generator.scale_sprites(scale)
        # print(f'sprite generator size {asizeof.asized(self.sprite_generator, detail=2).format()}')
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

        # if self.pixmap_flag:
        #     region.region_sprite.setPixmap(sprite)
        # else:
        #     region.region_sprite(sprite)
        # region.region_changed = True

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
                # if self.pixmap_flag:
                #     region.region_sprite.setPixmap(sprite)
                # else:
                #     region.region_sprite(sprite)
                if self.pixmap_flag:
                    region.setPixmap(sprite)
                else:
                    region.region_sprite(sprite)
            self.region_check_queue = []

    def generate_coastal_adjacency(self, region_id: int, signal: bool = False) -> NoReturn:
        # region = self.regions[region_id]
        n = region_id

        coastal_adjacency_temp = [0, 0, 0, 0, 0, 0, 0, 0]  # 3x3 numpy array van maken?
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
            if self.regions[top_id].water_id in check_list:
                river_adjacency_temp[0] = 1
        if 0 <= top_left_id < self.nr_regions:
            if self.regions[top_left_id].water_id in check_list:
                river_adjacency_temp[1] = 1
        if 0 <= left_id < self.nr_regions:
            if self.regions[left_id].water_id in check_list:
                river_adjacency_temp[2] = 1
        if 0 <= bottom_left_id < self.nr_regions:
            if self.regions[bottom_left_id].water_id in check_list:
                river_adjacency_temp[3] = 1
        if 0 <= bottom_id < self.nr_regions:
            if self.regions[bottom_id].water_id in check_list:
                river_adjacency_temp[4] = 1
        if 0 <= bottom_right_id < self.nr_regions:
            if self.regions[bottom_right_id].water_id in check_list:
                river_adjacency_temp[5] = 1
        if 0 <= right_id < self.nr_regions:
            if self.regions[right_id].water_id in check_list:
                river_adjacency_temp[6] = 1
        if 0 <= top_right_id < self.nr_regions:
            if self.regions[top_right_id].water_id in check_list:
                river_adjacency_temp[7] = 1

        self.regions[n].river_adjacency = river_adjacency_temp
