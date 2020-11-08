from PyQt5.QtWidgets import QMainWindow, QApplication

from gui.application import MainApplication
from pympler import asizeof

if __name__ == "__main__":
    import sys

    app = MainApplication(sys.argv)
    sys.exit(app.exec_())

