from typing import Optional, NoReturn, List, Tuple
from multiprocessing import Pool, Queue
import multiprocessing as mp
import copy

from PyQt5.QtCore import QPointF, QRect, QMetaObject, QCoreApplication, QPoint, pyqtSignal, pyqtBoundSignal, pyqtSlot, \
    QObject, QEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, \
    QHBoxLayout, QPushButton, QMenuBar, QMenu, QStatusBar, QAction, QApplication, QMainWindow, QGraphicsPixmapItem, \
    QFileDialog, QErrorMessage, QMessageBox, QProgressBar, QDialog, QInputDialog, QGraphicsSceneHoverEvent
from PyQt5.QtGui import QTransform, QMouseEvent
from pathlib import Path
from gui.create_new_world_dialog import NewWorldDialog
from gui.MainwindowUI import MainWindow
from base.world import World
from base.region import Region
from settings import DEFAULT_WRLD_SZ_X, DEFAULT_WRLD_SZ_Y, _REGION_IMAGE_HEIGHT, _REGION_IMAGE_WIDTH
from utils.log import get_logger
from gui.progressbar_widget import ProgressBar
from gui.signal_slots import SignalSlot
from pympler import asizeof
from PIL import Image
from settings import RESOURCES_DIR

# !TODO:check sprite logic on; coastal adjacency, river types
# !TODO:make override checks on worldmap edit
# !TODO:Make before save final check and highlight wrongly constructed tiles.
# !TODO:Create sprite difference for plains and flat
# !TODO:Set climate AND additional brush, (maybe change mouse icon)


class MainApplication(QApplication, SignalSlot):
    rebuild_sprite_signal = pyqtSignal(int)
    region_info_signal = pyqtSignal(str, int, str, str, str, str, str)

    def __init__(self, argv: List[str]):
        super().__init__(argv)

        # Initialize "world editor tool" attribute
        self.paint_id = 0
        self.brush_id = 0
        self.brushes = ['climate', 'relief', 'vegetation', 'water', 'spawn']

        self.logger = get_logger(f'{__name__}: {self.__class__.__name__}')
        self.world_loaded = False

        # Initialize GUI
        self.main_window = MainWindow()
        self.graphics_scene_map = GraphicsWorldmapScene(self.rebuild_sprite_signal)
        self.main_window.ui.graphics_view_map.setScene(self.graphics_scene_map)
        self.message_box = QMessageBox()  # Common message box

        # Create new world dialog
        self.new_world_ui = NewWorldDialog()
        self.new_world_ui.ui.spinBox.setMinimum(1)
        self.new_world_ui.ui.spinBox_2.setMinimum(1)
        self.new_world_ui.ui.spinBox.setMaximum(150)
        self.new_world_ui.ui.spinBox_2.setMaximum(100)

        # Initialize both open and save file GUI elements
        self.open_file_dialog = QFileDialog()
        self.open_file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.save_file_dialog = QFileDialog()
        self.save_file_dialog.setAcceptMode(QFileDialog.AcceptSave)

        # Initialize progress bar for loading etc
        # self.progress_bar = QProgressBar(self.main_window)
        # self.progress_bar.setGeometry(200, 80, 250, 20)

        # Connect editor climate buttons to logic
        self.main_window.ui.pushButton.pressed.connect(self.press_climate_button_sea)
        self.main_window.ui.pushButton_2.pressed.connect(self.press_climate_button_cont)
        self.main_window.ui.pushButton_3.pressed.connect(self.press_climate_button_oceanic)
        self.main_window.ui.pushButton_8.pressed.connect(self.press_climate_button_medi)
        self.main_window.ui.pushButton_7.pressed.connect(self.press_climate_button_tropical)
        self.main_window.ui.pushButton_9.pressed.connect(self.press_climate_button_arid)
        self.main_window.ui.pushButton_11.pressed.connect(self.press_climate_button_desert)
        self.main_window.ui.pushButton_10.pressed.connect(self.press_climate_button_nordic)
        self.main_window.ui.pushButton_12.pressed.connect(self.press_climate_button_polar)

        # Connect editor relief buttons to logic
        self.main_window.ui.pushButton_13.pressed.connect(self.press_relief_button_none)
        self.main_window.ui.pushButton_16.pressed.connect(self.press_relief_button_plains)
        self.main_window.ui.pushButton_17.pressed.connect(self.press_relief_button_rocky)
        self.main_window.ui.pushButton_19.pressed.connect(self.press_relief_button_hills)
        self.main_window.ui.pushButton_20.pressed.connect(self.press_relief_button_mountains)

        # Connect editor vegetation buttons to logic
        self.main_window.ui.pushButton_32.pressed.connect(self.press_vegetation_button_none)
        self.main_window.ui.pushButton_35.pressed.connect(self.press_vegetation_button_forrest)

        # Connect editor river buttons to logic
        self.main_window.ui.pushButton_33.pressed.connect(self.press_river_button_none)
        self.main_window.ui.pushButton_37.pressed.connect(self.press_river_button_estuary)
        self.main_window.ui.pushButton_38.pressed.connect(self.press_river_button_river)
        self.main_window.ui.pushButton_39.pressed.connect(self.press_river_button_maw)
        self.main_window.ui.pushButton_40.pressed.connect(self.press_river_button_lake)
        self.main_window.ui.pushButton_41.pressed.connect(self.press_river_button_swamp)

        # Connect editor primitive buttons to logic
        self.main_window.ui.pushButton_34.pressed.connect(self.press_primitive_button_none)
        self.main_window.ui.pushButton_36.pressed.connect(self.press_primitive_button_prim)

        # Connect editor utility buttons to logic
        self.main_window.ui.pushButton_99.pressed.connect(self.press_utility_button_only_sea)
        self.main_window.ui.pushButton_97.pressed.connect(self.press_utility_button_cont_flatlands)

        # Connect new, load and save world buttons to logic
        self.main_window.ui.actionLoad_world.triggered.connect(self.load_world)
        self.main_window.ui.actionNew_world.triggered.connect(self.new_world)
        self.main_window.ui.actionSave_world.triggered.connect(self.save_world)
        self.main_window.ui.actionTiny_world.triggered.connect(self.load_tiny_world)

        # Connect world menu
        self.main_window.ui.actionRemovePrimitives.triggered.connect(self.remove_primitives)
        self.main_window.ui.actionWorldinfo.triggered.connect(self.show_world_summary)
        # self.main_window.ui.actionShiftone.triggered.connect(self.shift_region)

        # Connect sprite rebuild signal
        self.rebuild_sprite_signal.connect(self.recreate_sprite_slot)
        self.region_info_signal.connect(self.display_region_info)

        # Create worldmap logic and send signals "downstream"
        self.worldmap = World(self.region_info_signal)

        # Open application
        self.main_window.show()

    def display_region_info(self, name: str, region_id: int, climate_str: str, relief_str: str, vegetation_str: str,
                            water_str: str, world_object_str: str):
        """Slot that provides logic to populate the region information display"""
        self.logger.debug(f'Display region information of region {name}, with region ID {region_id}')
        text = f'Region name: {name} \nRegion ID: {region_id} \nClimate: {climate_str} \nRelief: {relief_str} \n' \
               f'Vegetation: {vegetation_str} \nWater: {water_str} \nPrimitive: {world_object_str} \n------------------'
        self.main_window.ui.textBrowser.setPlainText(text)

    def recreate_sprite_slot(self, region_id: int):
        """Slot that provides brush functionality"""
        if self.brush_id == 0:
            self.worldmap.regions[region_id].climate_id = self.paint_id
        elif self.brush_id == 1:
            self.worldmap.regions[region_id].relief_id = self.paint_id
        elif self.brush_id == 2:
            self.worldmap.regions[region_id].vegetation_id = self.paint_id
        elif self.brush_id == 3:
            self.worldmap.regions[region_id].water_id = self.paint_id
        elif self.brush_id == 4:
            self.worldmap.regions[region_id].world_object_id = self.paint_id
        elif self.brush_id == 5:
            # Utility brush;
            if self.paint_id == 0:
                self.worldmap.regions[region_id].climate_id = 0
                self.worldmap.regions[region_id].relief_id = 0
                self.worldmap.regions[region_id].vegetation_id = 0
                self.worldmap.regions[region_id].water_id = 0
                self.worldmap.regions[region_id].world_object_id = 0
            if self.paint_id == 1:
                self.worldmap.regions[region_id].climate_id = 1
                self.worldmap.regions[region_id].relief_id = 1
                self.worldmap.regions[region_id].vegetation_id = 0
                self.worldmap.regions[region_id].water_id = 0
                self.worldmap.regions[region_id].world_object_id = 0

        # Recreate sprite with adjusted region values, include signal_flag = True to rebuild adjacent tiles.
        self.worldmap.create_region_sprite(region_id, self.scale, signal_flag=True)

    def remove_primitives(self):
        """Menu function to remove all primitive spawns on the worldmap"""
        if self.worldmap.regions:
            for region in self.worldmap.regions:
                if region.world_object_id == 1:
                    region.world_object_id = 0
                    self.worldmap.create_region_sprite(region.region_id, self.scale, False)
            self.message_box.setText('Removed primitives')
            self.message_box.setIcon(QMessageBox.Information)
            self.message_box.show()
        else:
            self.message_box.setText('No region data present.')
            self.message_box.setIcon(QMessageBox.Critical)
            self.message_box.show()

    # def shift_region(self):
    #     for region in self.worldmap.regions:
    #         region.climate_id = 0
    #         region.relief_id = 0
    #         region.world_object_id = 0
    #         region.vegetation_id = 0
    #         region.water_id = 0
    #     for region in self.worldmap.regions:
    #         self.worldmap.create_region_sprite(region.region_id, self.scale, signal_flag=False)

    def shift_region(self):
        img_climate = Image.open('europe_ymir.png')
        img_relief = Image.open('europe_relief.png')
        img_rivers = Image.open('europe_rivers.png')
        width = img_climate.size[0]/100
        height = img_climate.size[1]/70
        templist = []
        templist_p = []
        templist_r = []
        for region in self.worldmap.regions:
            x = (region.x + 0.5) * width
            y = (region.y + 0.5) * height


            pixel_climate = img_climate.getpixel((x,y))
            pixel_relief = img_relief.getpixel((x,y))
            pixel_rivers = img_rivers.getpixel((x, y))
            templist.append(pixel_climate)
            templist_p.append(pixel_relief)
            templist_r.append(pixel_rivers)
            if pixel_climate == (0,0,0,0):
                region.climate_id = 0
            elif pixel_climate == (0, 77, 0, 255):
                region.climate_id = 1
            elif pixel_climate == (0, 118, 132, 255):
                region.climate_id = 2
            elif pixel_climate == (210, 0, 179, 255):
                region.climate_id = 3
            elif pixel_climate == (0, 255, 0, 255):
                region.climate_id = 4
            elif pixel_climate == (215, 129, 0, 255):
                region.climate_id = 5
            elif pixel_climate == (107, 107, 107, 255):
                region.climate_id = 6
            elif pixel_climate == (123, 0, 255, 255):
                region.climate_id = 7
            elif pixel_climate == (223, 223, 0, 255):
                region.climate_id = 8

            if pixel_relief == (255, 85, 0, 255):
                region.relief_id = 4
            elif pixel_relief == (0, 21, 255, 255):
                region.relief_id = 3

            if pixel_rivers == (0, 255, 251, 255):
                region.water_id = 3
            elif pixel_rivers == (11, 0, 255, 255):
                region.water_id = 1
            # self.worldmap.create_region_sprite(region.region_id, self.scale, False)

        self.worldmap.create_all_region_sprites()
        temp_sortlist = set(templist_r)
        # pixel_climate = img.getpixel((1,1))




    def show_world_summary(self):
        """Menu function that gives an summary of the created worldmap"""
        # CLIMATES = ("SEA", "CONTINENTAL", "OCEANIC", "MEDITERRANEAN", "TROPICAL", "ARID", "DESERT", "NORDIC",
        # "POLAR", "UNKNOWN",)
        # RELIEF = ("NONE", "PLAIN", "ROCKY", "HILLS", "MOUNTAINS",)
        # VEGETATION = ("NONE", "FOREST", )
        # WATER = ("NONE", "RIVER_SMALL", "RIVER_MED", "RIVER_LARGE", "LAKE", "SWAMP",)
        # WORLD_OBJECT = ("NONE", "SPAWN",)

        climate_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        climate_count_spawns = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        relief_count = [0, 0, 0, 0, 0]
        forrest_count = 0
        water_count = [0, 0, 0, 0, 0, 0]

        if self.worldmap.regions:
            for region in self.worldmap.regions:
                climate_count[region.climate_id] += 1
                if region.world_object_id == 1:
                    climate_count_spawns[region.climate_id] += 1
                relief_count[region.relief_id] += 1
                if region.vegetation_id == 1:
                    forrest_count += 1
                water_count[region.water_id] += 1

            # Create string
            text = f'Climate count \n-------------------\n Sea = {climate_count[0]} \nContinental = {climate_count[1]} \nOceanic = ' \
                   f'{climate_count[2]} \nMediterranean = {climate_count[3]} \nTropical = {climate_count[4]} \nArid = {climate_count[5]} ' \
                   f'\nDesert = {climate_count[6]} \nNordic = {climate_count[7]} \nPolar = {climate_count[8]}\nUnknown = {climate_count[9]} \n\nRelief count \n-------------------\n' \
                   f'Flat = {relief_count[0]}\nPlains = {relief_count[1]}\nRocky = {relief_count[2]}\nHills = {relief_count[3]}\n' \
                   f'Mountains = {relief_count[4]}\nForrest count = {forrest_count}\n\nWater counts\n-------------------\nRiver small = {water_count[1]}\nRiver medium = {water_count[2]}\n' \
                   f'River large = {water_count[3]}\nLakes = {water_count[4]}\nSwamps = {water_count[4]}\n\nPrimitives per climate\n-------------------\n' \
                   f'Sea primitives = {climate_count_spawns[0]}\nContinental primitives = {climate_count_spawns[1]}\nOceanic primitives = {climate_count_spawns[2]}\n' \
                   f'Mediterranean primitives = {climate_count_spawns[3]}\nTropical primitives = {climate_count_spawns[4]}\n' \
                   f'Arid primitives = {climate_count_spawns[5]}\nDesert primitives = {climate_count_spawns[6]}\nNordic primitives = {climate_count_spawns[7]}\nPolar primitives = {climate_count_spawns[8]}' \
                   f'\nUnknown primitives = {climate_count_spawns[9]}'

            self.message_box.setText(text)
            self.message_box.setIcon(QMessageBox.Information)
            self.message_box.show()
        else:
            self.message_box.setText('Something went wrong')
            self.message_box.setIcon(QMessageBox.Critical)
            self.message_box.show()

    def save_world(self):

        self.save_file_dialog.exec_()
        filename = self.save_file_dialog.selectedFiles()
        filename = filename[0]

        if self.save_file_dialog.result() == 1 and self.worldmap.regions:
            self.worldmap.rebuild_region_list()
            if min(self.worldmap.region_info_lst) == -1:
                self.message_box.setText('There are regions of type "Unknown" still present, abort')
                self.message_box.setIcon(QMessageBox.Critical)
                self.message_box.show()
                return
            if '.ybin' in filename and self.worldmap.region_info_lst:
                with open(filename, mode='wb') as file:
                    self.logger.debug('Saving worldmap to file, please wait..')
                    file.write(bytearray(self.worldmap.region_info_lst))
                    self.logger.debug('File saved!')
            elif self.worldmap.region_info_lst:
                filename = filename + '.ybin'
                with open(filename, mode='wb') as file:
                    file.write(bytes(self.worldmap.region_info_lst))
            else:
                self.message_box.setText('Something went wrong')
                self.message_box.setIcon(QMessageBox.Critical)
                self.message_box.show()

        else:
            self.message_box.setText('Something went wrong')
            self.message_box.setIcon(QMessageBox.Critical)
            self.message_box.show()
            return

    def load_tiny_world(self):
        """Convenience function to load in pre-build tiny world for quick editting."""
        DIR = Path(RESOURCES_DIR).resolve()
        filename = DIR / 'world.ybin'
        self.graphics_scene_map.clear()
        self.worldmap.regions = []
        self.worldmap.load_world(filename)
        self.scale = (1, 1,)
        for region in self.worldmap.regions:
            x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * self.scale[0],
                                                    _REGION_IMAGE_HEIGHT * self.scale[1])
            pos = QPointF(x, y)
            self.graphics_scene_map.create_scene_items_from_world(region, pos)

    def load_world(self):
        # !TODO: Reset view after creating a new scene.
        self.open_file_dialog.exec_()
        filename = self.open_file_dialog.selectedFiles()
        filename = filename[0] if filename else None
        if not filename:
            self.logger.debug("File loading dialog was cancelled; no world will be loaded")
            return

        if self.open_file_dialog.result() == 1:
            if '.ybin' in filename:
                self.graphics_scene_map.clear()
                self.worldmap.regions = []
                self.worldmap.load_world(filename)
                self.scale = (1, 1,)
                for region in self.worldmap.regions:
                    x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * self.scale[0],
                                                            _REGION_IMAGE_HEIGHT * self.scale[1])
                    pos = QPointF(x, y)
                    self.graphics_scene_map.create_scene_items_from_world(region, pos)

            else:
                self.message_box.setText('You have to load an .ybin world file')
                self.message_box.setIcon(QMessageBox.Critical)
                self.message_box.show()
        else:
            return

    def new_world(self):
        # !TODO: Reset view after creating a new scene.
        self.new_world_ui.exec_()
        if self.new_world_ui.result() == 0:
            return
        elif self.new_world_ui.result() == 1:
            width = self.new_world_ui.ui.spinBox.value()
            height = self.new_world_ui.ui.spinBox_2.value()
            name = self.new_world_ui.ui.lineEdit.text()
            random_climate = self.new_world_ui.ui.checkBox.isChecked()

            self.worldmap.regions = []
            self.graphics_scene_map.clear()
            self.scale = (1, 1,)
            self.worldmap.create_new_world(name, width, height, random_climate, self.scale)
            for region in self.worldmap.regions:
                x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * self.scale[0],
                                                        _REGION_IMAGE_HEIGHT * self.scale[1])
                pos = QPointF(x, y)
                self.graphics_scene_map.create_scene_items_from_world(region, pos)


class GraphicsWorldmapScene(QGraphicsScene):
    def __init__(self, rebuild_sprite_signal):
        super().__init__()

        self.rebuild_sprite_signal = rebuild_sprite_signal

        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

        self.current_item = None
        self.pressed = False

    def create_scene_items_from_world(self, item: QGraphicsPixmapItem, pos: QPoint):
        self.addItem(item)
        item.setPos(pos)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.pressed:
            item = self.itemAt(event.scenePos(), QTransform())
            same = item == self.current_item

            if isinstance(item, Region) and not same:
                self.rebuild_sprite_signal.emit(item.region_id)
                self.current_item = item

        return super(GraphicsWorldmapScene, self).mouseMoveEvent(event)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if event.button() == 1:
            item = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item, Region):
                self.rebuild_sprite_signal.emit(item.region_id)
                self.current_item = item
                self.pressed = True

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.pressed = False
