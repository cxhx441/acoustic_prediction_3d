from random import random, randint
import sys

from PyQt6.QtCore import QSize
# from PyQt6.QtGui import QIcon, QAction, QKeySequence, QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QDialog,
    QToolButton,
    QTabWidget,
)
from PyQt6.QtGui import QScreen, QGuiApplication, QIcon


class TabWidget(QWidget):
    def __init__(self, configuration=None):
        super().__init__()
        self.configuration = configuration


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_file_name = None

        # self.action_open_prj = QAction(QIcon("./icons/folder-horizontal-open.png"), "Load Project")
        # self.action_open_prj.setStatusTip("Open a project")
        # self.action_open_prj.triggered.connect(self.load_project)
        # self.action_open_prj.setShortcut(QKeySequence("Ctrl+o"))

        # Ask user to either open an existing file, or start a new one.
        self.welcome_dialog = WelcomeDialog(self)
        self.welcome_dialog.exec()

        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("./icons/new-text.png"))
        self.resize(screen.availableSize())
        self.move(screen.availableGeometry().left(), screen.availableGeometry().top())

        # Main Window Components
        button_print_project = QPushButton("print project")
        button_close_project = QPushButton("close project")
        button_print_project.clicked.connect(self.print_project)
        button_close_project.clicked.connect(self.close_project)

        layout_h = QHBoxLayout()
        layout_h.addWidget(button_print_project)
        layout_h.addWidget(button_close_project)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True) # Only macOS affected
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)

        self.tab_titles = ["red", "green", "blue", "yellow"]
        for n, color in enumerate(self.tab_titles):
            self.tabs.addTab(QWidget(), color)
        self.tabs.setLayout(layout_h)
        self.setCentralWidget(self.tabs)
        # widget = QWidget()
        # widget.setLayout(layout_h)
        # self.setCentralWidget(widget)

    def print_project(self):
        print(f"project is: {self.project_file_name}, configuration is: {self.tab_titles[self.tabs.currentIndex()]}")

    def load_project(self):
        print("loading project...")
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "SoundMap files (*.ax *.acs)")
        self.project_file_name = fname[0]
        print(f'Opening file: {self.project_file_name}')

        self.show()
        self.welcome_dialog.close()

    def new_project(self):
        print("starting new project...")
        self.show()
        self.welcome_dialog.close()

    def close_project(self):
        self.hide()
        self.welcome_dialog.exec()


class WelcomeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("./icons/new-text.png"))

        button_load_prj = QPushButton(QIcon("./icons/folder-horizontal-open.png"), "Load Project")
        # button_load_prj = QToolButton(parent.action_open_prj)
        button_new_prj = QPushButton(QIcon("./icons/application--plus.png"), "New Project")
        button_load_prj.clicked.connect(parent.load_project)
        button_new_prj.clicked.connect(parent.new_project)

        layout_h = QHBoxLayout()
        layout_h.addWidget(button_new_prj)
        layout_h.addWidget(button_load_prj)

        self.setFixedSize(QSize(500, 50))
        self.setLayout(layout_h)


qt_app = QApplication([])
screen = qt_app.primaryScreen()
main_window = MainWindow()
# main_window.show()
sys.exit(qt_app.exec())  # Good practice.

