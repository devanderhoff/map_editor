import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QMainWindow, QWidget, \
    QHBoxLayout, QPushButton, QMenuBar, QMenu, QStatusBar, QAction, QGraphicsPixmapItem, QGraphicsSceneMouseEvent
from PyQt5.QtCore import Qt, QPointF, QRect, QMetaObject, QCoreApplication
from world import World
from PyQt5.QtGui import QPixmap
import numpy as np
from PIL import Image, ImageQt


class GraphicView(QGraphicsView):
    def __init__(self, widget):
        super().__init__(widget)

        self._zoom = 0
        self.setScene(GraphicScene())
        self.scale(0.3, 0.3)
        self.signal_down = None

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor=0.8
            self._zoom -= 1

        if self._zoom > 0:
            self.scale(factor, factor)
        elif self._zoom < 0:
            self.scale(factor, factor)
        else:
            self._zoom = 0

    # def signal_connect(self, handle):
        


class GraphicScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        scale = (1, 1,)
        self.worldmap = World(scale)
        self.worldmap.create_new_world(10, 10, True)
        #         # self.worldmap.load_world('./tiny_world.ybin')
        for n, region in enumerate(self.worldmap.regions):
            #
            # pixmap = QPixmap.fromImage(region.region_sprite)
            # region.setPixmap(pixmap)
            # # item = QGraphicsPixmapItem(pixmap)
            self.addItem(region.region_sprite)

            x, y = region.region_xy_to_scene_coords(self.worldmap._REGION_IMAGE_WIDTH * scale[0],
                                                    self.worldmap._REGION_IMAGE_HEIGHT * scale[1])
            pos = QPointF(x, y)
            region.region_sprite.setPos(region.mapToScene(pos))
    # def test:
    #     print('test')

    # def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     for region in self.worldmap.regions:
    #         if region.region_changed:
    #             self.worldmap.create_region_sprite(region)
    #             pixmap = QPixmap.fromImage(region.region_sprite)
    #             region.setPixmap(pixmap)
    #     n = np.random.randint(0, len(self.worldmap.regions))
    #     item = self.graphicsView.items()[n]
    #     image_array = np.ones((225, 300, 4)) * 155
    #     image = Image.fromarray(image_array.astype(np.uint8))
    #     image_pix = ImageQt.ImageQt(image)
    #
    #     pixmap = QPixmap.fromImage(image_pix)
    #     item.setPixmap(pixmap)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(927, 716)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = GraphicView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_2.pressed.connect(name='setbrush')

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 927, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_world = QAction(MainWindow)
        self.actionLoad_world.setObjectName("actionLoad_world")
        self.actionSave_world = QAction(MainWindow)
        self.actionSave_world.setObjectName("actionSave_world")
        self.menuFile.addAction(self.actionLoad_world)
        self.menuFile.addAction(self.actionSave_world)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionLoad_world.setText(_translate("MainWindow", "Load world"))
        self.actionSave_world.setText(_translate("MainWindow", "Save world"))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
