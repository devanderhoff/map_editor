# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'worldmap_editor_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from typing import Optional, NoReturn, List, Tuple
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QGraphicsView
from utils.log import get_logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(694, 701)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(189, 360))
        self.frame.setMaximumSize(QtCore.QSize(189, 360)) #348
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QtWidgets.QToolBox(self.frame)
        self.toolBox.setMinimumSize(QtCore.QSize(169, 350)) #328
        self.toolBox.setMaximumSize(QtCore.QSize(169, 350)) #328
        self.toolBox.setAccessibleName("")
        self.toolBox.setObjectName("toolBox")

        self.climate_tab = QtWidgets.QWidget()
        self.climate_tab.setGeometry(QtCore.QRect(0, 0, 169, 168))
        self.climate_tab.setMinimumSize(QtCore.QSize(169, 168))
        self.climate_tab.setMaximumSize(QtCore.QSize(169, 168))
        self.climate_tab.setObjectName("climates")
        # self.climate_tab.set

        self.widget = QtWidgets.QWidget(self.climate_tab)
        self.widget.setGeometry(QtCore.QRect(0, 0, 167, 167))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton.setObjectName("pushButton")


        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_2.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)


        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_3.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_3.setObjectName("pushButton_3")

        self.gridLayout_2.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_8.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_2.addWidget(self.pushButton_8, 1, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.widget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_7.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 1, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.widget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_9.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_2.addWidget(self.pushButton_9, 1, 2, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.widget)
        self.pushButton_11.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_11.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_2.addWidget(self.pushButton_11, 2, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.widget)
        self.pushButton_10.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_10.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_2.addWidget(self.pushButton_10, 2, 1, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.widget)
        self.pushButton_12.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_12.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_2.addWidget(self.pushButton_12, 2, 2, 1, 1)
        self.toolBox.addItem(self.climate_tab, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 169, 193))
        self.page_2.setObjectName("page_2")
        self.layoutWidget = QtWidgets.QWidget(self.page_2)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 167, 167))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_17 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_17.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_17.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout_3.addWidget(self.pushButton_17, 1, 1, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_16.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_16.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout_3.addWidget(self.pushButton_16, 1, 0, 1, 1)
        self.pushButton_19 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_19.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_19.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_19.setObjectName("pushButton_19")
        self.gridLayout_3.addWidget(self.pushButton_19, 2, 0, 1, 1)
        self.pushButton_20 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_20.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_20.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_20.setObjectName("pushButton_20")
        self.gridLayout_3.addWidget(self.pushButton_20, 2, 1, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_13.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_13.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_3.addWidget(self.pushButton_13, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.layoutWidget_4 = QtWidgets.QWidget(self.page_3)
        self.layoutWidget_4.setGeometry(QtCore.QRect(0, 0, 167, 167))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.layoutWidget_4)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButton_32 = QtWidgets.QPushButton(self.layoutWidget_4)
        self.pushButton_32.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_32.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_32.setObjectName("pushButton_32")
        self.gridLayout_6.addWidget(self.pushButton_32, 0, 0, 1, 1)
        self.pushButton_35 = QtWidgets.QPushButton(self.layoutWidget_4)
        self.pushButton_35.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_35.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_35.setObjectName("pushButton_35")
        self.gridLayout_6.addWidget(self.pushButton_35, 1, 0, 1, 1)
        self.toolBox.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.layoutWidget_5 = QtWidgets.QWidget(self.page_4)
        self.layoutWidget_5.setGeometry(QtCore.QRect(0, 0, 167, 167))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.layoutWidget_5)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.pushButton_33 = QtWidgets.QPushButton(self.layoutWidget_5)
        self.pushButton_33.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_33.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_33.setObjectName("pushButton_33")
        self.gridLayout_7.addWidget(self.pushButton_33, 0, 0, 1, 1)
        self.pushButton_37 = QtWidgets.QPushButton(self.layoutWidget_5)
        self.pushButton_37.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_37.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_37.setObjectName("pushButton_37")
        self.gridLayout_7.addWidget(self.pushButton_37, 1, 0, 1, 1)
        self.pushButton_38 = QtWidgets.QPushButton(self.layoutWidget_5)
        self.pushButton_38.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_38.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_38.setObjectName("pushButton_38")
        self.gridLayout_7.addWidget(self.pushButton_38, 1, 1, 1, 1)
        self.pushButton_39 = QtWidgets.QPushButton(self.layoutWidget_5)
        self.pushButton_39.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_39.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_39.setObjectName("pushButton_39")
        self.gridLayout_7.addWidget(self.pushButton_39, 1, 2, 1, 1)
        self.pushButton_40 = QtWidgets.QPushButton(self.layoutWidget_5)
        self.pushButton_40.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_40.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_40.setObjectName("pushButton_40")
        self.gridLayout_7.addWidget(self.pushButton_40, 2, 0, 1, 1)
        self.pushButton_41 = QtWidgets.QPushButton(self.layoutWidget_5)
        self.pushButton_41.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_41.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_41.setObjectName("pushButton_41")
        self.gridLayout_7.addWidget(self.pushButton_41, 2, 1, 1, 1)
        self.toolBox.addItem(self.page_4, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.layoutWidget_6 = QtWidgets.QWidget(self.page_5)
        self.layoutWidget_6.setGeometry(QtCore.QRect(0, 0, 167, 167))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.layoutWidget_6)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pushButton_34 = QtWidgets.QPushButton(self.layoutWidget_6)
        self.pushButton_34.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_34.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_34.setObjectName("pushButton_34")
        self.gridLayout_8.addWidget(self.pushButton_34, 0, 0, 1, 1)
        self.pushButton_36 = QtWidgets.QPushButton(self.layoutWidget_6)
        self.pushButton_36.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_36.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_36.setObjectName("pushButton_36")
        self.gridLayout_8.addWidget(self.pushButton_36, 1, 0, 1, 1)
        self.toolBox.addItem(self.page_5, "")

        # Beun
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.layoutWidget_7 = QtWidgets.QWidget(self.page_6)
        self.layoutWidget_7.setGeometry(QtCore.QRect(0, 0, 167, 167))
        self.layoutWidget_7.setObjectName("layoutWidget_7")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.layoutWidget_7)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.pushButton_99 = QtWidgets.QPushButton(self.layoutWidget_7)
        self.pushButton_99.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_99.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_99.setObjectName("pushButton_99")
        self.gridLayout_9.addWidget(self.pushButton_99, 0, 0, 1, 1)
        self.pushButton_98 = QtWidgets.QPushButton(self.layoutWidget_7)
        self.pushButton_98.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_98.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_98.setObjectName("pushButton_98")
        self.gridLayout_9.addWidget(self.pushButton_98, 1, 0, 1, 1)
        self.pushButton_97 = QtWidgets.QPushButton(self.layoutWidget_7)
        self.pushButton_97.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_97.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_97.setObjectName("pushButton_97")
        self.gridLayout_9.addWidget(self.pushButton_97, 0, 1, 1, 1)
        self.pushButton_96 = QtWidgets.QPushButton(self.layoutWidget_7)
        self.pushButton_96.setMinimumSize(QtCore.QSize(51, 51))
        self.pushButton_96.setMaximumSize(QtCore.QSize(51, 51))
        self.pushButton_96.setObjectName("pushButton_96")
        self.gridLayout_9.addWidget(self.pushButton_96, 1, 1, 1, 1)
        self.toolBox.addItem(self.page_6, "")





        self.verticalLayout.addWidget(self.toolBox)
        self.frame_3 = QtWidgets.QFrame(self.splitter)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.formLayout = QtWidgets.QFormLayout(self.frame_3)
        self.formLayout.setObjectName("formLayout")
        self.textBrowser = QtWidgets.QPlainTextEdit(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(171, 171))
        self.textBrowser.setMaximumSize(QtCore.QSize(171, 171))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setReadOnly(True)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.textBrowser)
        self.checkBox = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_2.setObjectName("checkBox_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_3.setObjectName("checkBox_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.checkBox_3)
        self.pushButton_42 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_42.setObjectName("pushButton_42")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pushButton_42)
        self.frame_2 = QtWidgets.QFrame(self.splitter_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.graphics_view_map = GraphicsWorldmapView(self.frame_2)
        self.graphics_view_map.setObjectName("graphicsView")
        self.verticalLayout_3.addWidget(self.graphics_view_map)
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 694, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menutemp = QtWidgets.QMenu(self.menubar)
        self.menutemp.setObjectName("menutemp")
        self.actionWorldinfo = QtWidgets.QAction(MainWindow)
        self.actionWorldinfo.setObjectName("actionWorldinfo")
        self.actionRemovePrimitives = QtWidgets.QAction(MainWindow)
        self.actionRemovePrimitives.setObjectName("actionRemovePrimitives")
        self.actionShiftone = QtWidgets.QAction(MainWindow)
        self.actionShiftone.setObjectName("actionShiftone")
        self.menutemp.addAction(self.actionWorldinfo)
        self.menutemp.addAction(self.actionRemovePrimitives)
        self.menutemp.addAction(self.actionShiftone)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_world = QtWidgets.QAction(MainWindow)
        self.actionNew_world.setObjectName("actionNew_world")
        self.actionLoad_world = QtWidgets.QAction(MainWindow)
        self.actionLoad_world.setObjectName("actionLoad_world")
        self.actionSave_world = QtWidgets.QAction(MainWindow)
        self.actionSave_world.setObjectName("actionSave_world")
        self.actionTiny_world = QtWidgets.QAction(MainWindow)
        self.actionTiny_world.setObjectName("Tiny_world")
        self.menuFile.addAction(self.actionNew_world)
        self.menuFile.addAction(self.actionLoad_world)
        self.menuFile.addAction(self.actionSave_world)
        self.menuFile.addAction(self.actionTiny_world)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menutemp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Sea"))
        self.pushButton_2.setText(_translate("MainWindow", "Cont"))
        self.pushButton_3.setText(_translate("MainWindow", "Oceanic"))
        self.pushButton_8.setText(_translate("MainWindow", "Medi"))
        self.pushButton_7.setText(_translate("MainWindow", "Tropical"))
        self.pushButton_9.setText(_translate("MainWindow", "Arid"))
        self.pushButton_11.setText(_translate("MainWindow", "Desert"))
        self.pushButton_10.setText(_translate("MainWindow", "Nordic"))
        self.pushButton_12.setText(_translate("MainWindow", "Polar"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.climate_tab), _translate("MainWindow", "Climate brushes"))
        self.pushButton_17.setText(_translate("MainWindow", "Rocky"))
        self.pushButton_16.setText(_translate("MainWindow", "Plains"))
        self.pushButton_19.setText(_translate("MainWindow", "Hills"))
        self.pushButton_20.setText(_translate("MainWindow", "Mountain"))
        self.pushButton_13.setText(_translate("MainWindow", "None"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "Relief brushes"))
        self.pushButton_32.setText(_translate("MainWindow", "None"))
        self.pushButton_35.setText(_translate("MainWindow", "Forrest"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("MainWindow", "Vegetation brushes"))
        self.pushButton_33.setText(_translate("MainWindow", "None"))
        self.pushButton_37.setText(_translate("MainWindow", "River\n"
                                                            "Small"))
        self.pushButton_38.setText(_translate("MainWindow", "River\n"
                                                            "Medium"))
        self.pushButton_39.setText(_translate("MainWindow", "River\n"
                                                            "Large"))
        self.pushButton_40.setText(_translate("MainWindow", "Lake"))
        self.pushButton_41.setText(_translate("MainWindow", "Swamp"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("MainWindow", "Water brushes"))
        self.pushButton_34.setText(_translate("MainWindow", "None"))
        self.pushButton_36.setText(_translate("MainWindow", "Primitive"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), _translate("MainWindow", "Primitive brushes"))
        self.pushButton_99.setText(_translate("MainWindow", "Empty \nSea"))
        self.pushButton_98.setText(_translate("MainWindow", "Flatten"))
        self.pushButton_98.hide()
        self.pushButton_97.setText(_translate("MainWindow", 'Cont \nFlatlands'))
        self.pushButton_96.setText(_translate("MainWindow", 'Chop'))
        self.pushButton_96.hide()
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_6), _translate("MainWindow", "Utility brushes"))

        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox.hide()
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_2.hide()
        self.checkBox_3.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_3.hide()
        self.pushButton_42.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_42.hide()
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menutemp.setTitle(_translate("MainWindow", "World"))
        self.actionNew_world.setText(_translate("MainWindow", "New  world"))
        self.actionLoad_world.setText(_translate("MainWindow", "Load world"))
        self.actionSave_world.setText(_translate("MainWindow", "Save world"))
        self.actionTiny_world.setText(_translate("MainWindow", "Load pre-build tiny world"))
        self.actionWorldinfo.setText(_translate("MainWindow", "World Info"))
        self.actionRemovePrimitives.setText(_translate("MainWindow", "Remove Primitives"))
        self.actionShiftone.setText(_translate('MainWindow', "Shift all regions"))

class GraphicsWorldmapView(QGraphicsView):
    def __init__(self, widget):
        super().__init__(widget)

        # Add logger to this class (if it doesn't have one already)
        if not hasattr(self, 'logger'):
            self.logger = get_logger(__class__.__name__)
        # self.setAcceptHoverEvents(True)
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

