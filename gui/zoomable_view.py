import logging

from PyQt6.QtGui import QPainter, QWheelEvent
from PyQt6.QtWidgets import QGraphicsView


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Allows panning
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)
        self.zoom_factor = 1.15
        self.current_scale = 1.0
        self.min_scale = 0.05
        self.max_scale = 100.0

    def wheelEvent(self, event: QWheelEvent):
        """ Zoom in/out centered around mouse position. """
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

        # COULD JUST DO THIS. But apparently less flexible and less precise. Not good for CAD type.
        # self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        # self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        #
        # if self.min_scale <= new_scale <= self.max_scale:
        #     self.scale(factor, factor)
        #     self.current_scale = new_scale
        #     logging.debug(f"current_scale: {self.current_scale}\n")


