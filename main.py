
import sys
import logging

from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication

logging.basicConfig(level=logging.DEBUG)

qt_app = QApplication([])
screen = qt_app.primaryScreen()
main_window = MainWindow()
# main_window.show()
sys.exit(qt_app.exec())  # Good practice.
