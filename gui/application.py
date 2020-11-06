from typing import Optional, NoReturn, List, Tuple

from PyQt5.QtCore import QPointF, QRect, QMetaObject, QCoreApplication, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, \
    QHBoxLayout, QPushButton, QMenuBar, QMenu, QStatusBar, QAction, QApplication, QMainWindow, QGraphicsPixmapItem


from base.world import World
from settings import DEFAULT_WRLD_SZ_X, DEFAULT_WRLD_SZ_Y, _REGION_IMAGE_HEIGHT, _REGION_IMAGE_WIDTH
from utils.log import get_logger


class MainApplication(QApplication):
    def __init__(self, argv: List[str]):
        super().__init__(argv)

        self.MainWindow = MainWindow()
        self.MainWindow.setupUi()

        self.graphics_view_map = GraphicView(self.MainWindow.centralwidget)
        self.graphics_view_map.setObjectName("graphicsView")
        self.MainWindow.horizontalLayout.addWidget(self.graphics_view_map)
        self.graphics_scene_map = GraphicScene()

        self.graphics_view_map.setScene(self.graphics_scene_map)

        scale = (1, 1,)
        self.worldmap = World(scale)
        self.worldmap.create_new_world(20, 20, True)
        #         # self.worldmap.load_world('./tiny_world.ybin')

        for region in self.worldmap.regions:
            x, y = region.region_xy_to_scene_coords(_REGION_IMAGE_WIDTH * scale[0], _REGION_IMAGE_HEIGHT * scale[1])
            pos = QPoint(x, y)
            self.graphics_scene_map.create_scene_items_from_world(region.region_sprite, pos)





        self.MainWindow.show()









class GraphicView(QGraphicsView):
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

class GraphicScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)

    def create_scene_items_from_world(self, item: QGraphicsPixmapItem, pos: QPoint):
        self.addItem(item)
        item.setPos(pos)


class MainWindow(QMainWindow):
    def setupUi(self) -> NoReturn:
        self.setObjectName("MainWindow")
        self.resize(927, 716)
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

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
        self.actionLoad_world.setText(_translate("MainWindow", "Load base"))
        self.actionSave_world.setText(_translate("MainWindow", "Save base"))
