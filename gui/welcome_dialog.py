from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QPushButton, QHBoxLayout

from utils.path_utils import resource_path


class WelcomeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon(resource_path("icons/new-text.png")))

        button_open_prj = QPushButton(QIcon(resource_path("icons/folder-horizontal-open.png")), "Open Project")
        # button_open_prj = QToolButton(parent.action_open_prj)
        button_new_prj = QPushButton(QIcon(resource_path("icons/application--plus.png")), "New Project")
        button_open_prj.clicked.connect(parent.open_project)
        button_new_prj.clicked.connect(parent.new_project)

        layout_h = QHBoxLayout()
        layout_h.addWidget(button_new_prj)
        layout_h.addWidget(button_open_prj)

        self.setFixedSize(QSize(500, 50))
        self.setLayout(layout_h)

