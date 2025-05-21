import logging

from PyQt6.QtCore import QSize

from PyQt6.QtGui import (
    QIcon,
    QAction,
    QKeySequence,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QToolBar,
    QStatusBar
)

from gui.tabs import CustomTabWidget
from gui.welcome_dialog import WelcomeDialog

from utils.path_utils import resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_file_name = None

        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon(resource_path("icons/new-text.png")))
        self.resize(1000, 1000)
        self.center()

        # add toolbar w buttons
        toolbar = QToolBar("My MainWindow Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # add statusbar
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        # add menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        edit_menu = menu.addMenu("&Edit")
        tools_menu = menu.addMenu("&Tools")

        # Add Tabs
        self.tabs = CustomTabWidget(self)
        self.setCentralWidget(self.tabs)


        # add all actions
        action_new_file = self._make_action(
            triggered_func=self.new_project,
            icon_png=resource_path("icons/application--plus.png"),
            menu_str="&New",
            status_str="Open a new file",
            key_sequence="Ctrl+N",
        )

        action_open = self._make_action(
            triggered_func=self.open_project,
            icon_png=resource_path("icons/folder-horizontal-open.png"),
            menu_str="&Open...",
            status_str="Open an existing .ax file",
            key_sequence="Ctrl+O"
        )

        action_close = self._make_action(
            triggered_func=self.close_project,
            menu_str="&Close",
            key_sequence="Ctrl+Q",
        )

        action_template = self._make_action(
            triggered_func=self.onMyToolBarButtonClick,
            icon_png="wafer.png",
            menu_str="&Your template button",
            status_str="this is my template button",
            set_checkable=True,
            key_sequence="Ctrl+K",
        )

        # Add buttons to toolbars
        toolbar.addAction(action_new_file)
        toolbar.addAction(action_open)
        toolbar.addAction(action_template)
        toolbar.addSeparator()

        # Add buttons to menus
        file_menu.addAction(action_new_file)
        file_menu.addAction(action_open)
        file_menu.addAction(action_close)
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("&Submenu")
        file_submenu.addAction(action_template)

        # edit menu
        edit_menu.addAction(action_template)

        # Ask user to either open an existing file, or start a new one.
        self.welcome_dialog = WelcomeDialog(self)
        self.welcome_dialog.exec()

    def _make_action(self, triggered_func, icon_png=None, menu_str=None, status_str=None, set_checkable=False, key_sequence=None):
        """ Template for adding a button action. """
        action = QAction(QIcon(icon_png), menu_str, self)
        action.triggered.connect(triggered_func)
        action.setStatusTip(status_str)
        action.setCheckable(set_checkable)
        action.setShortcut(QKeySequence(key_sequence))

        return action


    def onMyToolBarButtonClick(self, s):
        logging.debug("clicked toolbar button")

    def print_project(self):
        current_tab_title = self.tabs.tabText(self.tabs.currentIndex())
        logging.debug(f"project is: {self.project_file_name}, configuration is: {current_tab_title}")

    def open_project(self):
        logging.debug("opening project...")
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "SoundMap files (*.ax *.acs)")
        self.project_file_name = fname[0]
        logging.debug(f'Opening file: {self.project_file_name}')
        self.show()
        self.welcome_dialog.close()

    def new_project(self):
        logging.debug("starting new project...")
        self.show()
        self.welcome_dialog.close()

    def close_project(self):
        self.hide()
        self.welcome_dialog.exec()

    def center(self):
        """ Thanks, ChatGPT. """
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

