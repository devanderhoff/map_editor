from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsObject

from utils.log import get_logger


class Foo(QGraphicsPixmapItem, QGraphicsObject):
    # Define a new signal_flag called 'trigger' that has no arguments.
    trigger: pyqtSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.setPixmap()

        if not self.hasattr('logger'):
            self.logger = get_logger(__class__.__name__)

    def connect_and_emit_trigger(self):
        # Connect the trigger signal_flag to a slot.
        self.trigger.connect(self.handle_trigger)

        # Emit the signal_flag.
        self.trigger.emit()
        # self.setPixmap()

    def handle_trigger(self):
        # Show that the slot has been called.

        self.logger.debug("Trigger signal_flag received...")


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
