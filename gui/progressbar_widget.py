import sys
import time
from typing import Any

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)
import asyncio

TIME_LIMIT = 100


class BuildWorld(QThread):
    # Kon niet slapen dus heb even wat gekloot maar het is niet af; zal volgende x ff verder kijken.
    pbar_progress1 = pyqtSignal(int)

    def __init__(self):
        self.loop = asyncio.new_event_loop()

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run(self):
        count = 0
        while count < TIME_LIMIT:
            count += 1
            time.sleep(1)
            self.pbar_progress1.emit(count)

class ProgressBar(QDialog):
    # Kon niet slapen dus heb even wat gekloot maar het is niet af; zal volgende x ff verder kijken.
    def __init__(self, parent: Any, window_title: str = 'Please wait...'):
        super().__init__()

        self.parent = parent
        self.setWindowTitle(window_title)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 30)
        self.progress.setMaximum(100)

    async def summon(self):
        self.show()
        self.calc = BuildWorld()
        self.calc.valuechanged.connect(self.on_value_change())

    def on_value_change(self, value):
        self.progress.setValue(value)

