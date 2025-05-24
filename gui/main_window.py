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
    QStatusBar, QGraphicsView
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
        self._center_window()

        # add toolbar w buttons
        self.toolbar = QToolBar("My MainWindow Toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        # add statusbar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # add menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.edit_menu = self.menu.addMenu("&Edit")
        self.tools_menu = self.menu.addMenu("&Tools")

        # Add Tabs
        self.tabs = CustomTabWidget(self)
        self.setCentralWidget(self.tabs)


        # add all actions
        self.action_new_file = self._make_action(
            triggered_func=self.new_project,
            icon_png="application--plus.png",
            menu_str="&New",
            status_str="Open a new file",
            key_sequence="Ctrl+N",
        )

        self.action_open = self._make_action(
            triggered_func=self.open_project,
            icon_png="folder-horizontal-open.png",
            menu_str="&Open...",
            status_str="Open an existing .ax file",
            key_sequence="Ctrl+O"
        )

        self.action_close = self._make_action(
            triggered_func=self.close_project,
            menu_str="&Close",
            key_sequence="Ctrl+Q",
        )

        self.action_template = self._make_action(
            triggered_func=self.onMyToolBarButtonClick,
            icon_png="wafer.png",
            menu_str="&Your template button",
            status_str="this is my template button",
            set_checkable=True,
            key_sequence="Ctrl+K",
        )

        self.action_enable_line_tool = self._make_action(
            triggered_func=self.enable_line_tool,
            icon_png="line.png",
            status_str="Line Tool",
            set_checkable=True,
            key_sequence="Ctrl+2"
        )

        self.action_enable_hand_tool = self._make_action(
            triggered_func=self.enable_hand_tool,
            icon_png="hand.png",
            status_str="Hand Tool",
            set_checkable=True,
            key_sequence="Ctrl+H"
        )

        # Add buttons to toolbars
        self.toolbar.addAction(self.action_new_file)
        self.toolbar.addAction(self.action_open)
        self.toolbar.addAction(self.action_template)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_enable_hand_tool)
        self.toolbar.addAction(self.action_enable_line_tool)

        # Add buttons to menus
        self.file_menu.addAction(self.action_new_file)
        self.file_menu.addAction(self.action_open)
        self.file_menu.addAction(self.action_close)
        self.file_menu.addSeparator()
        self.file_submenu = self.file_menu.addMenu("&Submenu")
        self.file_submenu.addAction(self.action_template)

        # edit menu
        self.edit_menu.addAction(self.action_template)

        # Ask user to either open an existing file, or start a new one.
        self.welcome_dialog = WelcomeDialog(self)
        self.welcome_dialog.exec()

    def _make_action(self, triggered_func, icon_png=None, menu_str=None, status_str=None, set_checkable=False, key_sequence=None):
        """ Template for adding a button action. """
        icon = QIcon(f"resources/icons/{icon_png}")
        action = QAction(icon, menu_str, self)
        action.triggered.connect(triggered_func)
        action.setStatusTip(status_str)
        action.setCheckable(set_checkable)
        action.setShortcut(QKeySequence(key_sequence))
        return action

    def disable_all_scene_tools(self):
        """ disable all scene tools """
        self.action_enable_line_tool.setChecked(False)
        cur_tab = self.tabs.currentWidget()
        cur_tab.view.setDragMode(QGraphicsView.DragMode.NoDrag)  # No Panning
        cur_tab.view.line_tool_enabled = False
        self.action_enable_hand_tool.setChecked(False)

    def enable_line_tool(self):
        """ activate line tool """
        logging.debug("activate line tool")
        self.disable_all_scene_tools()
        self.action_enable_line_tool.setChecked(True)
        cur_tab = self.tabs.currentWidget()
        cur_tab.view.line_tool_enabled = True

    def enable_hand_tool(self):
        """ activate line tool """
        logging.debug("activate hand tool")
        self.disable_all_scene_tools()
        self.action_enable_hand_tool.setChecked(True)
        cur_tab = self.tabs.currentWidget()
        cur_tab.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Allows panning

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

    def _center_window(self):
        """ Thanks, ChatGPT. """
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

