from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem
from utils.path_utils import bed_image_path


class CustomScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.world_scale = None  # Pixels to feet

        # load image, and load into canvas
        pixmap = QPixmap(bed_image_path("bed_image.jpg"))
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.addItem(self.pixmap_item)

    def draw_line(self, x0, y0, x1, y1):
        line = QGraphicsLineItem(x0, y0, x1, y1)
        self.addItem(line)
        return line

