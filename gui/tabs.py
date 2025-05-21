import logging

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsScene, QGraphicsPixmapItem, QTabWidget, QDialog, \
    QLineEdit, QComboBox, QDialogButtonBox

from gui.zoomable_view import ZoomableGraphicsView
from utils.path_utils import bed_image_path


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

        # Any additional default widgets can be added here
        # Example: layout.addWidget(QPushButton("Example Button"))

        # SET UP CANVAS
        # setup canvas
        self.scene = QGraphicsScene()

        # load image, and load into canvas
        pixmap = QPixmap(bed_image_path("bed_image.jpg"))
        # pixmap = QPixmap(bed_image_path("bed_image.png"))

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
