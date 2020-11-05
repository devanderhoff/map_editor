from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsObject, QGraphicsSceneMouseEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent


class Region(QGraphicsObject):
    """
    Region class that holds all region (tile) data.
    """
    # Initialize region information.
    CLIMATES = ("SEA", "CONTINENTAL", "OCEANIC", "MEDITERRANEAN", "TROPICAL", "ARID", "DESERT", "NORDIC",
                "POLAR", "UNKNOWN",)
    RELIEF = ("NONE", "PLAIN", "ROCKY", "HILLS", "MOUNTAINS", "UNKNOWN",)
    VEGETATION = ("NONE", "FOREST", "UNKNOWN",)
    WATER = ("NONE", "RIVER_SMALL", "RIVER_MED", "RIVER_LARGE", "LAKE", "SWAMP", "UNKNOWN",)
    WORLD_OBJECT = ("NONE", "SPAWN", "UNKNOWN",)

    trigger = pyqtSignal()

    def __init__(self, x, y, region_list, name, region_id, climate, relief, vegetation, water, worldobject, signal):
        # X and Y coordinates start top-left corner.
        super().__init__()
        self.x = x          # world x
        self.y = y          # world y

        self.region_list = region_list

        self.image_coords = None

        # Region name.
        self.name = name
        self.region_id = region_id

        self.climate_id = climate
        self.climate_str = self.CLIMATES[climate]

        self.relief_id = relief
        self.relief_str = self.RELIEF[relief]

        self.vegetation_id = vegetation
        self.vegetation_str = self.VEGETATION[vegetation]

        self.water_id = water
        self.water_str = self.WATER[water]

        self.world_object_id = worldobject
        self.world_object_str = self.WORLD_OBJECT[worldobject]

        # contains information about coast and river adjacency
        self.coastal_adjacency = None
        self.river_adjacency = None

        # Holds region sprite
        self.region_sprite = RegionPixmap(self.trigger)
        self.region_sprite_loaded = False

        self.region_changed = False
        self.world_trigger = signal

        self.trigger.connect(self.signal_to_climate)


    def signal_to_climate(self):
        print('i am in signal to climate')
        self.climate_id = 0
        self.world_trigger.emit(self.region_id)

    def region_xy_to_img_coords(self, image_width, image_height):
        return int(self.x * image_width), int(self.y * image_height)

    def region_xy_to_scene_coords(self, image_width, image_height):
        return (self.x + 0.5) * image_width, (self.y + 0.5) * image_height

    @property
    def region_sprite(self):
        return self._region_sprite

    @region_sprite.setter
    def region_sprite(self, image):
        self._region_sprite = image

    @property
    def climate_id(self):
        return self._climate_id

    @climate_id.setter
    def climate_id(self, value):
        self._climate_id = value
        self.region_list[0] = value
        self.climate_str = self.CLIMATES[value]

    @property
    def relief_id(self):
        return self._relief_id

    @relief_id.setter
    def relief_id(self, value):
        self._relief_id = value
        self.region_list[1] = value
        self.relief_str = self.RELIEF[value]
        # self.world_trigger.emit(self.region_id)

    @property
    def vegetation_id(self):
        return self._vegetation_id

    @vegetation_id.setter
    def vegetation_id(self, value):
        self._vegetation_id = value
        self.region_list[2] = value
        self.vegetation_str = self.VEGETATION[value]
        # self.world_trigger.emit(self.region_id)

    @property
    def water_id(self):
        return self._water_id

    @water_id.setter
    def water_id(self, value):
        self._water_id = value
        self.region_list[3] = value
        self.water_str = self.WATER[value]
        # self.world_trigger.emit(self.region_id)

    @property
    def world_object_id(self):
        return self._world_object_id

    @world_object_id.setter
    def world_object_id(self, value):
        self._world_object_id = value
        self.region_list[4] = value
        self.world_object_str = self.WORLD_OBJECT[value]

        # self.world_trigger.emit(self.region_id)

class RegionPixmap(QGraphicsPixmapItem):
    def __init__(self, trigger):
        super().__init__()
        self.trigger = trigger


    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        # self.climate_id = 0
        self.trigger.emit()
        print(self.pos().x(), self.pos().y())