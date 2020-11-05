from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsObject, QGraphicsItem
from PyQt5.QtGui import QPixmap


class Foo(QGraphicsPixmapItem, QGraphicsObject):
    # Define a new signal called 'trigger' that has no arguments.
    trigger = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.setPixmap()

    def connect_and_emit_trigger(self):
        # Connect the trigger signal to a slot.
        self.trigger.connect(self.handle_trigger)

        # Emit the signal.
        self.trigger.emit()
        # self.setPixmap()

    def handle_trigger(self):
        # Show that the slot has been called.

        print("trigger signal received")




if __name__ == "__main__":
    test = Foo()
    print(test)
    test.connect_and_emit_trigger()
    # import sys
    #
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
