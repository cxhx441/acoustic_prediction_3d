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
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
)
from PyQt6.QtGui import QScreen, QGuiApplication, QIcon

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
        initial_tab_titles = ["red", "green", "blue", "yellow"]
        for title in initial_tab_titles:
            self.add_default_tab(title)
        self.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
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
        print(f'Current Tab: {current_tab_title}')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_file_name = None

        # Ask user to either open an existing file, or start a new one.
        self.welcome_dialog = WelcomeDialog(self)
        self.welcome_dialog.exec()

        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("./icons/new-text.png"))
        self.resize(1000, 1000)
        self.center()

        # self.action_open_prj = QAction(QIcon("./icons/folder-horizontal-open.png"), "Load Project")
        # self.action_open_prj.setStatusTip("Open a project")
        # self.action_open_prj.triggered.connect(self.load_project)
        # self.action_open_prj.setShortcut(QKeySequence("Ctrl+o"))

        # Main Window Components
        # button_print_project = QPushButton("print project")
        # button_close_project = QPushButton("close project")
        # button_print_project.clicked.connect(self.print_project)
        # button_close_project.clicked.connect(self.close_project)
        #
        # layout_h = QHBoxLayout()
        # layout_h.addWidget(button_print_project)
        # layout_h.addWidget(button_close_project)

        self.tabs = CustomTabWidget(self)
        self.setCentralWidget(self.tabs)
        # widget = QWidget()
        # widget.setLayout(layout_h)
        # self.setCentralWidget(widget)

    def print_project(self):
        current_tab_title = self.tabs.tabText(self.tabs.currentIndex())
        print(f"project is: {self.project_file_name}, configuration is: {current_tab_title}")

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

