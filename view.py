#from encodings.punycode import selective_find
import sys
import logging

from PyQt6.QtCore import QSize, Qt, QEvent
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QPalette, QColor, QPixmap, QPainter, QWheelEvent
# from PyQt6.QtGui import QScreen, QGuiApplication, QIcon
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
    QToolBar,
    QTabWidget,
    QLineEdit,
    QComboBox,
    QDialogButtonBox, QStatusBar, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QAbstractScrollArea,
    QGestureEvent, QPinchGesture,
)
from PyQt6.QtGui import QScreen, QGuiApplication, QIcon

logging.basicConfig(level=logging.DEBUG)

class NewTabDialog(QDialog):
    def __init__(self, parent=None, existing_tabs=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Tab")
        self.setFixedSize(300, 150)

        # Input for new tab name
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter new tab name")

        # Dropdown to select an existing tab as a template
        self.template_combo = QComboBox(self)
        self.template_combo.addItems(existing_tabs)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(QLabel("New Tab Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Base On Existing Tab:"))
        layout.addWidget(self.template_combo)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_tab_info(self):
        """Return the new tab name and selected template."""
        return self.name_input.text(), self.template_combo.currentText()


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Optional: allows panning
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.zoom_factor = 1.15
        self.current_scale = 1.0
        self.min_scale = 0.05
        self.max_scale = 100.0

    def wheelEvent(self, event):
        # Zoom in/out

        zoom_in = event.angleDelta().y() > 0
        factor = self.zoom_factor if zoom_in else 1 / self.zoom_factor

        new_scale = self.current_scale * factor
        if self.min_scale <= new_scale <= self.max_scale:
            self.scale(factor, factor)
            self.current_scale = new_scale


class DefaultTabContent(QWidget):
    def __init__(self, title, based_on=None):
        super().__init__()
        self.title = title
        self.template_tab_title = based_on
        self.label = QLabel(self.title)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add a label to display the tab title as default content
        if self.template_tab_title is None:
            self.label.setText(f"Default content for '{self.title}' tab")
        else:
            self.label.setText(f"Default content for '{self.title}' tab, based on '{self.template_tab_title}' tab")

        layout.addWidget(self.label)

        # Any additional default widgets can be added here
        # Example: layout.addWidget(QPushButton("Example Button"))

        # SET UP CANVAS
        # setup canvas
        self.scene = QGraphicsScene()

        # load image, and load into canvas
        pixmap = QPixmap("old/bed_image.png")
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        # create the view to show the canvas
        # self.view = QGraphicsView(self.scene, self)
        self.view = ZoomableGraphicsView(self.scene, self)

        layout.addWidget(self.view)

        layout.addWidget(self.label)
        self.setLayout(layout)


class CustomTabWidget(QTabWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setDocumentMode(True)
        self.setTabPosition(QTabWidget.TabPosition.South)
        self.setMovable(True)

        # Initial tabs and the "+" tab
        self.addTab(QWidget(), "+")  # Add the "+" tab
        self.add_default_tab("Map1")
        # initial_tab_titles = ["red", "green", "blue", "yellow"]
        # for title in initial_tab_titles:
        #     self.add_default_tab(title)
        self.setCurrentIndex(0)
        self.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        logging.debug(f"Tab index: {index}")
        # Check if the "+" tab was selected
        if self.tabText(index) == "+":
            existing_tabs = [self.tabText(i) for i in range(self.count() - 1)]
            dialog = NewTabDialog(self, existing_tabs)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                tab_name, template_name = dialog.get_tab_info()
                if tab_name:
                    new_tab_index = self.count() - 1
                    self.add_default_tab(tab_name, template_name)
                    self.setCurrentIndex(new_tab_index)
        else:
            # TODO reload other content in window?
            pass

    def add_default_tab(self, title, template_tab_title=None):
        insert_index = self.count() - 1  # Insert before the '+' tab.
        tab_content = DefaultTabContent(title, template_tab_title)
        self.insertTab(insert_index, tab_content, title)

    def print_tab_info(self):
        current_tab_title = self.tabText(self.currentIndex())
        logging.debug(f'Current Tab: {current_tab_title}')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_file_name = None

        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("./icons/new-text.png"))
        self.resize(1000, 1000)
        self.center()

        # add toolbar w buttons
        toolbar = QToolBar("My MainWindow Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_new_file_action = self._make_button_action(
            toolbar=toolbar,
            icon_png="icons/application--plus.png",
            menu_str="&New",
            status_str="Open a new file",
            triggered_func=self.new_project,
            set_checkable=False,
            add_separator=True
        )

        button_open_action = self._make_button_action(
            toolbar=toolbar,
            icon_png="icons/folder-horizontal-open.png",
            menu_str="&Open...",
            status_str="Open an existing .ax file",
            triggered_func=self.open_project,
            set_checkable=False,
            add_separator=True
        )

        button_close_action = self._make_button_action(
            toolbar=None,
            icon_png="Close",
            menu_str="&Close",
            status_str="Close the current file",
            triggered_func=self.close_project,
            set_checkable=False,
            add_separator=True
        )

        button_template_action = QAction(QIcon("wafer.png"), "&Your template Button", self)
        button_template_action.setStatusTip("this is my template button")
        button_template_action.triggered.connect(self.onMyToolBarButtonClick)
        button_template_action.setCheckable(True)
        toolbar.addAction(button_template_action)

        toolbar.addSeparator()

        # add statusbar
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        # add menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_new_file_action)
        file_menu.addAction(button_open_action)
        file_menu.addAction(button_close_action)
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("&Submenu")
        file_submenu.addAction(button_template_action)

        # add tabs
        self.tabs = CustomTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Ask user to either open an existing file, or start a new one.
        self.welcome_dialog = WelcomeDialog(self)
        self.welcome_dialog.exec()

    def _make_button_action(self, toolbar, icon_png, menu_str, status_str, triggered_func, set_checkable, add_separator=False):

        button_action = QAction(QIcon(icon_png), menu_str, self)
        button_action.setStatusTip(status_str)
        button_action.triggered.connect(triggered_func)
        button_action.setCheckable(set_checkable)

        if toolbar is not None:
            toolbar.addAction(button_action)
            if add_separator == True:
                toolbar.addSeparator()

        return button_action


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


class WelcomeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("./icons/new-text.png"))

        button_open_prj = QPushButton(QIcon("./icons/folder-horizontal-open.png"), "Open Project")
        # button_open_prj = QToolButton(parent.action_open_prj)
        button_new_prj = QPushButton(QIcon("./icons/application--plus.png"), "New Project")
        button_open_prj.clicked.connect(parent.open_project)
        button_new_prj.clicked.connect(parent.new_project)

        layout_h = QHBoxLayout()
        layout_h.addWidget(button_new_prj)
        layout_h.addWidget(button_open_prj)

        self.setFixedSize(QSize(500, 50))
        self.setLayout(layout_h)


qt_app = QApplication([])
screen = qt_app.primaryScreen()
main_window = MainWindow()
# main_window.show()
sys.exit(qt_app.exec())  # Good practice.

