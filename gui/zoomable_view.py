import logging

from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QWheelEvent, QMouseEvent
from PyQt6.QtWidgets import QGraphicsView, QLabel, QVBoxLayout


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.parent = parent
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Allows panning
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)
        self.zoom_factor = 1.15
        self.current_scale = 1.0
        self.min_scale = 0.05
        self.max_scale = 100.0
        self.mouse_position = QPointF()
        # layout = QVBoxLayout()
        # self.setLayout(layout)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Track when the mouse moves with the scene. """
        logging.debug("Moving mouse in Scene")
        super().mouseMoveEvent(event)  # Need so inherited class mouseEvent gets triggered (dragging, in this case).
        pos_viewport = event.position()  # Gives position w/in viewport.
        self.mouse_position = self.mapToScene(pos_viewport.toPoint())
        self.parent.update_mouse_pos_label()

    def wheelEvent(self, event: QWheelEvent):
        """ Zoom in/out centered around mouse position. """
        super().wheelEvent(event)  # Inherited class wheelEvent gets triggered. Not used here. Seems like good practice.
        logging.debug("Zooming in/out")

        # Zoom in or out
        zoom_in = event.angleDelta().y() > 0
        factor = self.zoom_factor if zoom_in else 1 / self.zoom_factor
        new_scale = self.current_scale * factor

        # Zoom around the mouse position
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

        if self.min_scale <= new_scale <= self.max_scale:
            pos_viewport = event.position()  # Gives position w/in viewport.

            old_center = self.mapToScene(pos_viewport.toPoint())
            self.scale(factor, factor)
            new_center = self.mapToScene(pos_viewport.toPoint())
            d = new_center - old_center
            self.translate(d.x(), d.y())
            self.current_scale = new_scale
            logging.debug(f"center: x, y: {old_center.x():.2f}, {old_center.y():.2f}")
            logging.debug(f"current_scale: {self.current_scale}\n")

        # Update scale label
        self.parent.update_scale_label()
