from region import Region
from image import WorldmapSprites
from PIL import Image, ImageQt
import numpy as np
from joblib import Parallel, delayed
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QGraphicsScene
from multiprocessing import Pool
import multiprocessing as mp


class World(QObject):
    world_trigger = pyqtSignal(int)

    def __init__(self, scale):
        super().__init__()
        self.pixmap_flag = True #Use pixmaps instead of PIL images.
        self.region_check_queue = []

        self.x_width = None  # Width of the world.
        self.y_height = None  # Height of the world.
        self.nr_regions = None  # nr of regions in the world.
        self.region_names = None  # region names
        self.xy_regions = None  # x and y coordinates of the region. (0,0) is top left.
        self.region_information_list = None  # List containing region information, climate, water etc.
        self.region_information_slice = None  # Start location to splice region information list into region info.
        self.regions = None  # Contains region objects which hold region info.
        self.region_signal_list = None  # list containing copies of the PyQt signal to be send to region during init

        # Sprite related stuff
        self.sprite_generator = WorldmapSprites()
        self._REGION_IMAGE_WIDTH = 300
        self._REGION_IMAGE_HEIGHT = 225
        self.scale = scale
        self.worldmap_image = None  # Hold created full worldmap image.

        # self.world_trigger.connect(self.create_region_sprite_signal)
        self.world_trigger.connect(self.create_region_sprite_signal)


    def create_new_world(self, width, height, random_climate):
        self.x_width = width
        self.y_height = height

        # Create region base information.
        self.nr_regions, self.region_names, self.xy_regions, self.region_information_list, \
        self.region_information_splice, self.region_signal_list = self.create_region_base(random_climate=random_climate, loaded_file=False)

        # Populate world regions
        self.regions = self.create_regions()

        # Determine sprite related coastal and river adjacencies.
        # self.generate_coastal_adjacency()
        # self.generate_river_adjacency()

        # Create initial sprites
        self.create_all_region_sprites()

    def load_world(self, filename):
        with open(filename, mode='rb') as file:
            self.region_information_list = list(file.read())
            self.x_width = self.region_information_list[0]
            self.y_height = self.region_information_list[2]
            self.nr_regions, self.region_names, self.xy_regions, self.region_information_list, \
            self.region_information_splice, self.region_signal_list = self.create_region_base(loaded_file=True)
            self.regions = self.create_regions()
            # self.generate_coastal_adjacency()
            # self.generate_river_adjacency()
            self.create_all_region_sprites()


    def create_all_region_sprites(self):
        # pool = Pool(processes=int(mp.cpu_count()/2))
        print(self.regions)
        for region in self.regions:
            print(region.region_id)
            # pool.apply(self.create_region_sprite, args=(region.region_id,))
            self.create_region_sprite(region.region_id, False)

    def create_world_image(self):
        total_image_width = self._REGION_IMAGE_WIDTH * self.x_width
        total_image_height = self._REGION_IMAGE_HEIGHT * self.y_height
        self.worldmap_image = Image.new('RGB', (total_image_width, total_image_height))

        for region in self.regions:
            self.worldmap_image.paste(region.region_sprite, region.region_xy_to_img_coords(self._REGION_IMAGE_WIDTH,
                                                                                           self._REGION_IMAGE_HEIGHT))

    def create_region_base(self, loaded_file, random_climate=False):
        if self.x_width != 0 or self.y_height != 0:
            nr_regions = self.x_width * self.y_height
        else:
            raise ValueError('Width and height have to be > 0')
        region_names = [f'region_{x}_{y}' for y in range(self.y_height) for x in range(self.x_width)]
        xy_regions = [[x, y] for y in range(self.y_height) for x in range(self.x_width)]
        if loaded_file:
            region_information_list = self.region_information_list
        elif random_climate:
            region_information_list = [self.x_width, 0, self.y_height, 0]
            for i in range(nr_regions):
                n = np.random.randint(0, 8)
                region_information_list.extend([n, -1, -1, -1, -1])
        else:
            region_information_list = [self.x_width, 0, self.y_height, 0] + ([-1, -1, -1, -1, -1] * nr_regions)
        region_information_slice = [*range(4, len(region_information_list), 5)]
        region_signal_list = [self.world_trigger] * nr_regions
        return nr_regions, region_names, xy_regions, region_information_list, region_information_slice, region_signal_list

    def create_regions(self):
        climate_id_list = [self.region_information_list[idx] for idx in self.region_information_splice]
        relief_id_list = [self.region_information_list[idx + 1] for idx in (self.region_information_splice)]
        vegetation_id_list = [self.region_information_list[idx + 2] for idx in (self.region_information_splice)]
        water_id_list = [self.region_information_list[idx + 3] for idx in (self.region_information_splice)]
        worldobject_id_list = [self.region_information_list[idx + 4] for idx in (self.region_information_splice)]
        region_bytes = [self.region_information_list[idx:idx+5] for idx in (self.region_information_splice)]

        print('test')
        region_list = [Region(x, y, region_bytes, name, region_id, climate_id, relief_id, vegetation_id, water_id, worldobject_id, signal)
                       for region_id, ([x, y], region_bytes, name, climate_id, relief_id, vegetation_id, water_id, worldobject_id, signal)
                       in enumerate(
                zip(self.xy_regions, region_bytes, self.region_names, climate_id_list, relief_id_list, vegetation_id_list,
                    water_id_list, worldobject_id_list, self.region_signal_list))]
        print(region_list)
        return region_list

    def create_region_sprite_signal(self, region_id):
        self.create_region_sprite(region_id, signal=True)


    def create_region_sprite(self, region_id, signal=False):
        print(region_id)
        region = self.regions[region_id]
        self.generate_coastal_adjacency(region_id, signal)
        self.generate_river_adjacency(region_id, signal)

        sprite = self.sprite_generator.create_required_sprite(region.climate_id, region.relief_id,
                                                                  region.vegetation_id, region.water_id,
                                                                  region.world_object_id,
                                                                  region.coastal_adjacency,
                                                                  region.river_adjacency,
                                                                  self.pixmap_flag,
                                                                  self.scale)
        if self.pixmap_flag:
            region.region_sprite.setPixmap(sprite)
        else:
            region.region_sprite(sprite)
        region.region_changed = True
        print(len(self.region_check_queue))

        if signal:
            for region_id_queue in self.region_check_queue:
                print(np.random.randint(100))
                region = self.regions[region_id_queue]
                self.generate_river_adjacency(region_id_queue, not signal)
                self.generate_coastal_adjacency(region_id_queue, not signal)
                sprite = self.sprite_generator.create_required_sprite(region.climate_id, region.relief_id,
                                                                      region.vegetation_id, region.water_id,
                                                                      region.world_object_id,
                                                                      region.coastal_adjacency,
                                                                      region.river_adjacency,
                                                                      self.pixmap_flag,
                                                                      self.scale)
                if self.pixmap_flag:
                    region.region_sprite.setPixmap(sprite)
                else:
                    region.region_sprite(sprite)

            self.region_check_queue = []

    def generate_coastal_adjacency(self, region_id, signal=False):
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


    def generate_river_adjacency(self, region_id, signal = False):
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
