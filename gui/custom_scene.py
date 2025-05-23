from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from utils.path_utils import bed_image_path


class CustomScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        # load image, and load into canvas
        pixmap = QPixmap(bed_image_path("bed_image.jpg"))
        # pixmap = QPixmap(bed_image_path("bed_image.png"))
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.addItem(self.pixmap_item)

