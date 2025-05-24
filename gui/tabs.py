import logging

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTabWidget, QDialog, \
    QLineEdit, QComboBox, QDialogButtonBox

from gui.custom_scene import CustomScene
from gui.zoomable_view import ZoomableGraphicsView


class DefaultTabContent(QWidget):
    def __init__(self, title, based_on=None):
        super().__init__()
        self.title = title
        self.template_tab_title = based_on

        self.scene = CustomScene(self)
        self.view = ZoomableGraphicsView(self.scene, self)

        self.label_title = QLabel(self.title)

        # Image Scale Label
        self.label_zoom_scale = QLabel()
        self.label_zoom_scale.setStyleSheet(
            """
            background-color: rgba(128, 128, 128, 180);
            color: white; 
            font-size: 14px;
            font-wight: bold;
            padding: 3px; 
            border: rgba(0, 0, 0, 256);
            border-radius: 4px;
            """
                                       )
        self.label_zoom_scale.setParent(self)
        self.label_zoom_scale.move(10, 10)  # Top-left corner
        self.label_zoom_scale.raise_()  # Stay on top
        self.update_zoom_scale_label()

        # Mouse Position Label
        self.label_mouse_pos = QLabel()
        self.label_mouse_pos.setStyleSheet(
            """
            background-color: rgba(128, 128, 128, 180);
            color: white;
            font-size: 14px;
            font-wight: bold;
            padding: 3px;
            border: rgba(0, 0, 0, 256);
            border-radius: 4px;
            """
        )
        self.label_mouse_pos.setParent(self)
        self.label_mouse_pos.move(10, 40)  # Top-left corner
        self.label_mouse_pos.raise_()  # Stay on top
        self.update_mouse_pos_label()

        # World Scale Label
        self.label_world_scale = QLabel()
        self.label_world_scale.setStyleSheet(
            """
            background-color: rgba(128, 128, 128, 180);
            color: white;
            font-size: 14px;
            font-wight: bold;
            padding: 3px;
            border: rgba(0, 0, 0, 256);
            border-radius: 4px;
            """
        )
        self.label_world_scale.setParent(self)
        self.label_world_scale.move(10, 70)  # Top-left corner
        self.label_world_scale.raise_()  # Stay on top
        self.update_world_scale_label()

        # Add a label to display the tab title as default content
        if self.template_tab_title is None:
            self.label_title.setText(f"Default content for '{self.title}' tab")
        else:
            self.label_title.setText(f"Default content for '{self.title}' tab, based on '{self.template_tab_title}' tab")

        # Any additional default widgets can be added here
        # Example: layout.addWidget(QPushButton("Example Button"))

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.label_title)
        # layout.addWidget(self.label_scale)
        self.setLayout(layout)

    def update_zoom_scale_label(self):
        """ Update the scale label with the current scale from view object """
        logging.debug("updating zoom scale label")
        self.label_zoom_scale.setText(f"Zoom: {self.view.current_zoom_scale:.0%}")
        self.label_zoom_scale.adjustSize()

    def update_mouse_pos_label(self):
        """ Update the mouse position label with the current mouse position from view object """
        logging.debug("updating mouse position label")
        pos = self.view.mouse_position
        self.label_mouse_pos.setText(f"x: {pos.x():.2f}, y: {pos.y():.2f}")
        self.label_mouse_pos.adjustSize()

    def update_world_scale_label(self):
        """ Update the world scale label/shape with info from view object """
        logging.debug("updating world scale label")

        if self.scene.world_scale is None:
            self.label_world_scale.setText("World Scale: Not Set")
        else:
            pixels = self.scene.world_scale[0]
            feet = self.scene.world_scale[1]
            self.label_world_scale.setText(f"World Scale: {pixels}px : {feet:.2f}ft")

        self.label_world_scale.adjustSize()


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
