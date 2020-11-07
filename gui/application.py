from typing import Optional, NoReturn, List, Tuple

from PyQt5.QtCore import QPointF, QRect, QMetaObject, QCoreApplication, QPoint, pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, \
    QHBoxLayout, QPushButton, QMenuBar, QMenu, QStatusBar, QAction, QApplication, QMainWindow, QGraphicsPixmapItem, \
    QFileDialog, QErrorMessage, QMessageBox, QProgressBar, QDialog, QInputDialog
from PyQt5.QtGui import QTransform

from gui.create_new_world_dialog import NewWorldDialog
from base.world import World
from base.region import Region
from settings import DEFAULT_WRLD_SZ_X, DEFAULT_WRLD_SZ_Y, _REGION_IMAGE_HEIGHT, _REGION_IMAGE_WIDTH
from utils.log import get_logger
from gui.signal_slots import SignalSlot


class MainApplication(QApplication, SignalSlot):
    recreate_sprite = pyqtSignal(int)

    def __init__(self, argv: List[str]):
        super().__init__(argv)
        # self.signalslots = SignalSlot()

        self.paint_climate = 0
        self.paint_relief = 0

        self.world_loaded = False

        self.MainWindow = MainWindow()
        self.MainWindow.setupUi()

        self.graphics_view_map = GraphicsWorldmapView(self.MainWindow.centralwidget)
        self.graphics_view_map.setObjectName("graphicsView")
        self.MainWindow.horizontalLayout.addWidget(self.graphics_view_map)
        self.graphics_scene_map = GraphicsWorldmapScene(self.recreate_sprite)
        self.graphics_view_map.setScene(self.graphics_scene_map)

        ## Init gui elements temp ##
        self.open_file_dialog = QFileDialog()
        self.open_file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        self.save_file_dialog = QFileDialog()
        self.save_file_dialog.setAcceptMode(QFileDialog.AcceptSave)

        self.MainWindow.pushButton.pressed.connect(self.press_climate_button)
        self.MainWindow.pushButton_2.pressed.connect(self.press_climate_button_2)
        self.MainWindow.pushButton_3.pressed.connect(self.press_climate_button_3)
        self.MainWindow.pushButton_4.pressed.connect(self.press_climate_button_4)
        self.MainWindow.pushButton_5.pressed.connect(self.press_climate_button_5)
        self.MainWindow.pushButton_6.pressed.connect(self.press_climate_button_6)
        self.MainWindow.pushButton_7.pressed.connect(self.press_climate_button_7)
        self.MainWindow.pushButton_8.pressed.connect(self.press_climate_button_8)
        self.MainWindow.pushButton_9.pressed.connect(self.press_climate_button_9)
        # self.save_file_dialog = self.save_file_dialog.getSaveFileName()
        # self.error = QErrorMessage()
        self.message_box = QMessageBox()

        self.new_world_ui = NewWorldDialog()
        self.new_world_ui.ui.spinBox.setMinimum(1)
        self.new_world_ui.ui.spinBox_2.setMinimum(1)

        ## INITIALIZE ALL SIGNAL CONNECTIONS HERE ##
        self.MainWindow.actionLoad_world.triggered.connect(self.load_world)
        self.MainWindow.actionNew_world.triggered.connect(self.new_world)
        self.MainWindow.actionSave_world.triggered.connect(self.save_world)
        self.recreate_sprite.connect(self.recreate_sprite_slot)
        # self.graphics_scene_map.

        ## From here world logic ##
        # Create world
        # scale = (1, 1,)
        self.worldmap = World()
        # self.worldmap.create_new_world(5, 5, random_climate=True)
        #         # self.worldmap.load_world('./tiny_world.ybin')

        # for region in self.worldmap.regions:
        #     x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * scale[0], _REGION_IMAGE_HEIGHT * scale[1])
        #     pos = QPoint(x, y)
        #     self.graphics_scene_map.create_scene_items_from_world(region.region_sprite, pos)

        self.MainWindow.show()

    def recreate_sprite_slot(self, region_id):
        self.worldmap.regions[region_id].climate_id = self.paint_climate
        self.worldmap.create_region_sprite(region_id, True)

    def save_world(self):
        self.save_file_dialog.exec_()
        filename = self.save_file_dialog.selectedFiles()
        filename = filename[0]

        if self.save_file_dialog.result() == 1:
            # self.worldmap.regions[3].world_object_id = 1
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
        # self.file_dialog.show()
        self.open_file_dialog.exec_()
        filename = self.open_file_dialog.selectedFiles()
        filename = filename[0]

        if self.open_file_dialog.result() == 1:
            # self.file_dialog.close()
            if '.ybin' in filename:
                self.graphics_scene_map.clear()
                self.worldmap.regions = []
                self.worldmap.load_world(filename)
                scale = (1, 1,)
                for region in self.worldmap.regions:
                    x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * scale[0],
                                                            _REGION_IMAGE_HEIGHT * scale[1])
                    pos = QPoint(x, y)
                    self.graphics_scene_map.create_scene_items_from_world(region, pos)
            else:
                # self.error.showMessage('You have to load an .ybin world file')
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
            self.worldmap.create_new_world(name, width, height, random_climate=random_climate)
            scale = (1, 1,)
            for region in self.worldmap.regions:
                x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * scale[0], _REGION_IMAGE_HEIGHT * scale[1])
                pos = QPoint(x, y)
                self.graphics_scene_map.create_scene_items_from_world(region, pos)

        # width, _ = self.new_world_width.getInt(self.MainWindow.centralwidget, 'new world width', 'test')
        # height, _ = self.new_world_width.getInt(self.MainWindow.centralwidget, 'new world width', 'test')
        # print(width)
        # print(height)
        #


class GraphicsWorldmapView(QGraphicsView):
    def __init__(self, widget):
        super().__init__(widget)

        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

        self._zoom = 0
        self.scale(0.3, 0.3)

    def wheelEvent(self, event) -> NoReturn:
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        if self._zoom > 0:
            self.scale(factor, factor)
        elif self._zoom < 0:
            self.scale(factor, factor)
        else:
            self._zoom = 0


class GraphicsWorldmapScene(QGraphicsScene):
    def __init__(self, signal):
        super().__init__()

        self.recreate_sprite = signal
        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

    def create_scene_items_from_world(self, item: QGraphicsPixmapItem, pos: QPoint):
        self.addItem(item)
        item.setPos(pos)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        item = self.itemAt(event.scenePos(), QTransform())
        if isinstance(item, Region):
            self.recreate_sprite.emit(item.region_id)

    # item.clicked_signal()


class MainWindow(QMainWindow):
    def setupUi(self) -> NoReturn:
        self.setObjectName("MainWindow")
        self.resize(927, 716)
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout.addWidget(self.pushButton_9)




        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 927, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.actionLoad_world = QAction(self)
        self.actionLoad_world.setObjectName("actionLoad_world")
        self.actionSave_world = QAction(self)
        self.actionSave_world.setObjectName("actionSave_world")
        self.actionNew_world = QAction(self)
        self.actionNew_world.setObjectName("actionNew_world")

        self.menuFile.addAction(self.actionNew_world)
        self.menuFile.addAction(self.actionLoad_world)
        self.menuFile.addAction(self.actionSave_world)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi()
        # QMetaObject.connectSlotsByName(self)

    def retranslateUi(self) -> NoReturn:
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionLoad_world.setText(_translate("MainWindow", "Load world"))
        self.actionSave_world.setText(_translate("MainWindow", "Save world"))
        self.actionNew_world.setText(_translate("MainWindow", "New world"))
