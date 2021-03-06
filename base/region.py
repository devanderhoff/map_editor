from typing import Optional, List, Any, Union

from PIL.Image import Image
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneHoverEvent
from nptyping import NDArray

from utils.log import get_logger
# class SignalHolder(QObject):
#     signal = pyqtSignal(str, int, str, str, str, str, str)
#
#     def __init__(self):
#         super().__init__()


class Region(QGraphicsPixmapItem):
    """
    Region class that holds all region (tile) data.
    """
    # Initialize region information.
    CLIMATES = ("SEA", "CONTINENTAL", "OCEANIC",
                "MEDITERRANEAN", "TROPICAL", "ARID",
                "DESERT", "NORDIC", "POLAR", "UNKNOWN",)
    RELIEF = ("FLAT", "PLAIN", "ROCKY", "HILLS", "MOUNTAINS",)
    VEGETATION = ("NONE", "FOREST", )
    WATER = ("NONE", "RIVER_SMALL", "RIVER_MED", "RIVER_LARGE", "LAKE", "SWAMP",)
    WORLD_OBJECT = ("NONE", "SPAWN",)

    def __init__(self, x: int, y: int,
                 name: str,
                 region_id: int,
                 climate_id: int,
                 relief_id: int,
                 vegetation_id: int,
                 water_id: int,
                 worldobject_id: int,
                 region_bytes: int,
                 region_info_signal: pyqtSignal):
        # X and Y coordinates start top-left corner.
        super().__init__()

        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

        self.region_bytes = region_bytes
        #  !TODO: region_bytes attribute in Region class is passed but not used?

        self.init_flag = False
        self.x: int = x  # base x
        self.y: int = y  # base y

        self.region_list: List[Union[int, None]] = [None, None, None, None, None]

        self.image_coords: Optional[Any] = None

        # Region name.
        self.name: str = name
        self.region_id: int = region_id

        self.climate_id: int = climate_id
        self.climate_str = self.CLIMATES[climate_id]

        self.relief_id: int = relief_id
        self.relief_str = self.RELIEF[relief_id]

        self.vegetation_id: int = vegetation_id
        self.vegetation_str = self.VEGETATION[vegetation_id]

        self.water_id: int = water_id
        self.water_str = self.WATER[water_id]

        self.world_object_id: int = worldobject_id
        self.world_object_str = self.WORLD_OBJECT[worldobject_id]

        # contains information about coast and river adjacency
        self.coastal_adjacency: Optional[NDArray[3, 3, bool]] = None
        self.river_adjacency: Optional[NDArray[3, 3, bool]] = None

        # Holds region sprite
        # self.region_sprite: RegionPixmap = RegionPixmap(self.trigger)
        # self.region_sprite = QGraphicsPixmapItem()
        self.region_sprite_loaded: bool = False
        self.region_changed: bool = False
        self._region_sprite: Optional[Image] = None

        self.setAcceptHoverEvents(True)

        # self.signal_holder = SignalHolder()
        self.region_info_signal = region_info_signal

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.logger.debug(self.region_id)
        self.region_info_signal.emit(self.name, self.region_id,
                                     self.climate_str, self.relief_str,
                                     self.vegetation_str,
                                     self.water_str,
                                     self.world_object_str)

        # self.signal.emit(self.name, self.region_id, self.climate_str, self.relief_str,
        #                                self.vegetation_str,
        #                                self.water_str, self.world_object_str)

    def region_xy_to_img_coords(self, image_width, image_height):
        return int(self.x * image_width), int(self.y * image_height)

    def region_xy_to_scene_coords(self, image_width, image_height):
        return (self.x + 0.5) * image_width, (self.y + 0.5) * image_height

    @staticmethod
    def standalone_region_xy_to_scene_coords(x, y, image_width, image_height):
        return (x + 0.5) * image_width, (y + 0.5) * image_height

    @property
    def region_sprite(self):
        return self._region_sprite

    @region_sprite.setter
    def region_sprite(self, image: Image):
        self._region_sprite = image

    @property
    def climate_id(self):
        return self._climate_id

    @climate_id.setter
    def climate_id(self, value):
        if not self.init_flag:
            self._climate_id = value
            self.region_list[0] = value
            self.climate_str = self.CLIMATES[value]

    @property
    def relief_id(self):
        return self._relief_id

    @relief_id.setter
    def relief_id(self, value):
        if not self.init_flag:
            self._relief_id = value
            self.region_list[1] = value
            self.relief_str = self.RELIEF[value]
            # self.world_trigger.emit(self.region_id)

    @property
    def vegetation_id(self):
        return self._vegetation_id

    @vegetation_id.setter
    def vegetation_id(self, value):
        if not self.init_flag:
            self._vegetation_id = value
            self.region_list[2] = value
            self.vegetation_str = self.VEGETATION[value]
            # self.world_trigger.emit(self.region_id)

    @property
    def water_id(self):
        return self._water_id

    @water_id.setter
    def water_id(self, value):
        if not self.init_flag:
            self._water_id = value
            self.region_list[3] = value
            self.water_str = self.WATER[value]
            # self.world_trigger.emit(self.region_id)

    @property
    def world_object_id(self):
        return self._world_object_id

    @world_object_id.setter
    def world_object_id(self, value):
        if not self.init_flag:
            self._world_object_id = value
            self.region_list[4] = value
            self.world_object_str = self.WORLD_OBJECT[value]

        # self.world_trigger.emit(self.region_id)

    # def __repr__(self):
    #     return self.climate_str


class RegionPixmap(QGraphicsPixmapItem):
    def __init__(self, trigger):
        super().__init__()

        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

        self.trigger = trigger

    def clicked_signal(self):
        self.trigger.emit()

    # def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     # self.climate_id = 0
    #     self.trigger.emit()
    #     self.logger.debug("mousePressEvent: %d, %d", self.pos().x(), self.pos().y())
