from typing import Optional, NoReturn, List, Tuple
from multiprocessing import Pool, Queue
import multiprocessing as mp

from PyQt5.QtCore import QPointF, QRect, QMetaObject, QCoreApplication, QPoint, pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, \
    QHBoxLayout, QPushButton, QMenuBar, QMenu, QStatusBar, QAction, QApplication, QMainWindow, QGraphicsPixmapItem, \
    QFileDialog, QErrorMessage, QMessageBox, QProgressBar, QDialog, QInputDialog
from PyQt5.QtGui import QTransform

from gui.create_new_world_dialog import NewWorldDialog
from gui.MainwindowUI import MainWindow
from base.world import World
from base.region import Region
from settings import DEFAULT_WRLD_SZ_X, DEFAULT_WRLD_SZ_Y, _REGION_IMAGE_HEIGHT, _REGION_IMAGE_WIDTH
from utils.log import get_logger
from gui.progressbar_widget import ProgressBar
from gui.signal_slots import SignalSlot


# !TODO:check sprite logic on; coastal adjacency, river types
# !TODO:make override checks on worldmap edit
# !TODO:Make before save final check and highlight wrongly constructed tiles.
# !TODO:Create sprite difference for plains and flat
# !TODO:Set climate AND additional brush, (maybe change mouse icon)


class MainApplication(QApplication, SignalSlot):
    rebuild_sprite_signal = pyqtSignal(int)

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

        # Initialize both open and save file GUI elements
        self.open_file_dialog = QFileDialog()
        self.open_file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.save_file_dialog = QFileDialog()
        self.save_file_dialog.setAcceptMode(QFileDialog.AcceptSave)

        # Initialize progress bar for loading etc
        self.progress_bar = ProgressBar(parent=self)

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

        # Connect new, load and save world buttons to logic
        self.main_window.ui.actionLoad_world.triggered.connect(self.load_world)
        self.main_window.ui.actionNew_world.triggered.connect(self.new_world)
        self.main_window.ui.actionSave_world.triggered.connect(self.save_world)

        # Connect sprite rebuild signal
        self.rebuild_sprite_signal.connect(self.recreate_sprite_slot)

        # Create worldmap logic
        self.worldmap = World()

        # Open application
        self.main_window.show()

    def recreate_sprite_slot(self, region_id: int):
        if self.brush_id == 0:
            self.worldmap.regions[region_id].climate_id = self.paint_id
        elif self.brush_id == 1:
            self.worldmap.regions[region_id].relief_id = self.paint_id
        elif self.brush_id == 2:
            self.worldmap.regions[region_id].vegetation_id = self.paint_id
        elif self.brush_id == 3:
            self.worldmap.regions[region_id].water_id = self.paint_id

        self.worldmap.create_region_sprite(region_id, self.scale, True)

    def save_world(self):

        self.save_file_dialog.exec_()
        filename = self.save_file_dialog.selectedFiles()
        filename = filename[0]

        if self.save_file_dialog.result() == 1:
            self.worldmap.rebuild_region_list()
            if '.ybin' in filename and self.worldmap.region_info_lst:
                with open(filename, mode='wb') as file:

                    file.write(bytearray(self.worldmap.region_info_lst))
            elif self.worldmap.region_info_lst:
                filename = filename + '.ybin'
                with open(filename, mode='wb') as file:
                    file.write(bytes(self.worldmap.region_info_lst))
            else:
                self.message_box.setText('Something went wrong')
                self.message_box.setIcon(QMessageBox.Critical)
                self.message_box.show()

        else:
            return

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

            turbo_hyper_mega_processing_mode_3950x = False
            multiproc_nregions_threshold = 64
            if len(self.worldmap.regions) >= multiproc_nregions_threshold:
                turbo_hyper_mega_processing_mode_3950x = True

            if turbo_hyper_mega_processing_mode_3950x:
                if mp.cpu_count() < 32:
                    raise ValueError("Your system does not conform to the minimum requirements. (requires at least "
                                     "16 physical cores or more e-p33n-equivalent).")

                self.logger.debug("Multiprocessing not yet implemented; falling back to single process")
                # self.generate_world_regions_multiprocessing(scale=scale)
                self.generate_world_regions_single_process(scale=self.scale)
            else:
                self.generate_world_regions_single_process(scale=self.scale)

            # for region in self.worldmap.regions:
            #     x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * scale[0], _REGION_IMAGE_HEIGHT * scale[1])
            #     pos = QPoint(x, y)
            #     self.graphics_scene_map.create_scene_items_from_world(region, pos)

        # width, _ = self.new_world_width.getInt(self.MainWindow.centralwidget, 'new world width', 'test')
        # height, _ = self.new_world_width.getInt(self.MainWindow.centralwidget, 'new world width', 'test')
        # print(width)
        # print(height)
        #

    def generate_world_regions_single_process(self, scale: Tuple[int, ...]):

        # Kon niet slapen dus heb even wat gekloot maar het is niet af; zal volgende x ff verder kijken.
        self.logger.info(f"Generating new world w/ %s region tiles in single threaded mode...",
                         len(self.worldmap.regions))

        for region in self.worldmap.regions:
            x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * scale[0],
                                                    _REGION_IMAGE_HEIGHT * scale[1])
            pos = QPointF(x, y)
            self.graphics_scene_map.create_scene_items_from_world(region, pos)

    def generate_world_regions_multiprocessing(self, scale: Tuple[int, ...]):
        # Kon niet slapen dus heb even wat gekloot maar het is niet af; zal volgende x ff verder kijken.

        # Later? Volgens mij kost het vooral tijd om die pyqt gui elementen te maken, dus heeft multiprocessing hier niet
        #  veel zin denk ik. Gui shit intern laten werken met multiprocessing maakt de complexiteit ongeveer 182342x zo leip
        raise NotImplementedError
        nprocs = mp.cpu_count() - 1
        self.logger.info(f"Generating new world w/ %s region tiles in multiprocessing mode (%d processes)",
                         nprocs)

        self.logger.debug("Starting multiprocessing pool...")
        noesten_arbeiders = Pool(nprocs)
        self.logger.debug("Multiprocessing pool init succesful...")

        self.graphics_scene_map.init_newworld_queue()
        new_world_queue = self.graphics_scene_map.newworld_queue

        for region in self.worldmap.regions:
            x_input, y_input = region.x, region.y

            noesten_arbeiders.apply(self.scene_creation_func, args=(new_world_queue, region, x_input, y_input,
                                                                    region.standalone_region_xy_to_scene_coords,
                                                                    _REGION_IMAGE_WIDTH, _REGION_IMAGE_HEIGHT, scale,))
        noesten_arbeiders.join()
        new_world_queue.put("ReAdY")

    @staticmethod
    def scene_creation_func(queue: mp.Queue, region, x: int, y: int, regionfunc,
                            region_image_width, region_image_height, scale):
        raise NotImplementedError
        # Later? Volgens mij kost het vooral tijd om die pyqt gui elementen te maken, dus heeft multiprocessing hier niet
        #  veel zin denk ik. Gui shit intern laten werken met multiprocessing maakt de complexiteit ongeveer 182342x zo leip
        x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * scale[0], _REGION_IMAGE_HEIGHT * scale[1])
        pos = QPointF(x, y)
        queue.put((region.region_sprite, pos,))


# class GraphicsWorldmapView(QGraphicsView):
#     def __init__(self, widget):
#         super().__init__(widget)
#
#         # Add logger to this class (if it doesn't have one already)
#         if not hasattr(self, 'logger'):
#             self.logger = get_logger(__class__.__name__)
#
#         self._zoom = 0
#         self.scale(0.3, 0.3)
#
#     def wheelEvent(self, event) -> NoReturn:
#         if event.angleDelta().y() > 0:
#             factor = 1.25
#             self._zoom += 1
#         else:
#             factor = 0.8
#             self._zoom -= 1
#         if self._zoom > 0:
#             self.scale(factor, factor)
#         elif self._zoom < 0:
#             self.scale(factor, factor)
#         else:
#             self._zoom = 0

class GraphicsWorldmapScene(QGraphicsScene):
    def __init__(self, signal):
        super().__init__()

        self.recreate_sprite = signal
        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

    def init_newworld_queue(self):
        self.gen_world_queue = mp.Queue

    def create_scene_items_from_world(self, item: QGraphicsPixmapItem, pos: QPoint):
        self.addItem(item)
        item.setPos(pos)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        item = self.itemAt(event.scenePos(), QTransform())
        if isinstance(item, Region):
            self.recreate_sprite.emit(item.region_id)

    # item.clicked_signal()

# class MainWindow(QMainWindow):
#     def setupUi(self) -> NoReturn:
#         self.setObjectName("MainWindow")
#         self.resize(927, 716)
#         self.centralwidget = QWidget()
#         self.centralwidget.setObjectName("centralwidget")
#
#         self.horizontalLayout = QHBoxLayout(self.centralwidget)
#         self.horizontalLayout.setObjectName("horizontalLayout")
#
#         self.pushButton = QPushButton(self.centralwidget)
#         self.pushButton.setObjectName("pushButton")
#         self.horizontalLayout.addWidget(self.pushButton)
#
#         self.pushButton_2 = QPushButton(self.centralwidget)
#         self.pushButton_2.setObjectName("pushButton_2")
#         self.horizontalLayout.addWidget(self.pushButton_2)
#
#         self.pushButton_3 = QPushButton(self.centralwidget)
#         self.pushButton_3.setObjectName("pushButton_3")
#         self.horizontalLayout.addWidget(self.pushButton_3)
#
#         self.pushButton_4 = QPushButton(self.centralwidget)
#         self.pushButton_4.setObjectName("pushButton_4")
#         self.horizontalLayout.addWidget(self.pushButton_4)
#
#         self.pushButton_5 = QPushButton(self.centralwidget)
#         self.pushButton_5.setObjectName("pushButton_5")
#         self.horizontalLayout.addWidget(self.pushButton_5)
#
#         self.pushButton_6 = QPushButton(self.centralwidget)
#         self.pushButton_6.setObjectName("pushButton_6")
#         self.horizontalLayout.addWidget(self.pushButton_6)
#
#         self.pushButton_7 = QPushButton(self.centralwidget)
#         self.pushButton_7.setObjectName("pushButton_7")
#         self.horizontalLayout.addWidget(self.pushButton_7)
#
#         self.pushButton_8 = QPushButton(self.centralwidget)
#         self.pushButton_8.setObjectName("pushButton_8")
#         self.horizontalLayout.addWidget(self.pushButton_8)
#
#         self.pushButton_9 = QPushButton(self.centralwidget)
#         self.pushButton_9.setObjectName("pushButton_9")
#         self.horizontalLayout.addWidget(self.pushButton_9)
#
#
#
#
#         self.setCentralWidget(self.centralwidget)
#
#         self.menubar = QMenuBar(self)
#         self.menubar.setGeometry(QRect(0, 0, 927, 21))
#         self.menubar.setObjectName("menubar")
#         self.menuFile = QMenu(self.menubar)
#         self.menuFile.setObjectName("menuFile")
#         self.setMenuBar(self.menubar)
#
#         self.statusbar = QStatusBar(self)
#         self.statusbar.setObjectName("statusbar")
#         self.setStatusBar(self.statusbar)
#
#         self.actionLoad_world = QAction(self)
#         self.actionLoad_world.setObjectName("actionLoad_world")
#         self.actionSave_world = QAction(self)
#         self.actionSave_world.setObjectName("actionSave_world")
#         self.actionNew_world = QAction(self)
#         self.actionNew_world.setObjectName("actionNew_world")
#
#         self.menuFile.addAction(self.actionNew_world)
#         self.menuFile.addAction(self.actionLoad_world)
#         self.menuFile.addAction(self.actionSave_world)
#
#         self.menubar.addAction(self.menuFile.menuAction())
#
#         self.retranslateUi()
#         # QMetaObject.connectSlotsByName(self)
#
#     def retranslateUi(self) -> NoReturn:
#         _translate = QCoreApplication.translate
#         self.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
#         self.pushButton.setText(_translate("MainWindow", "PushButton"))
#         self.menuFile.setTitle(_translate("MainWindow", "File"))
#         self.actionLoad_world.setText(_translate("MainWindow", "Load world"))
#         self.actionSave_world.setText(_translate("MainWindow", "Save world"))
#         self.actionNew_world.setText(_translate("MainWindow", "New world"))
