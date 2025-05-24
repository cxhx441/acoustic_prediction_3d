import logging

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QWheelEvent, QMouseEvent, QDragMoveEvent
from PyQt6.QtWidgets import QGraphicsView, QLabel, QVBoxLayout


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.scene = scene
        self.parent = parent
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)  # Selection Tool?
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)
        self.zoom_factor = 1.15
        self.current_zoom_scale = 1.0
        self.min_zoom_scale = 0.05
        self.max_zoom_scale = 100.0
        self.mouse_position = QPointF()

        self.line_tool_enabled = False
        self.dragging = False
        self.p0 = None
        self.p1 = None
        self.temp_line = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self.line_tool_enabled:
            self.dragging = True
            pos_viewport = event.position()  # Gives position w/in viewport.
            self.p0 = self.mapToScene(pos_viewport.toPoint())

    def mouseMoveEvent(self, event):
        """ Track when the mouse moves with the scene. """
        logging.debug("Moving mouse in Scene")

        super().mouseMoveEvent(event)  # Need so inherited class mouseEvent gets triggered (dragging, in this case).
        pos_viewport = event.position()  # Gives position w/in viewport.
        self.mouse_position = self.mapToScene(pos_viewport.toPoint())
        self.parent.update_mouse_pos_label()

        logging.debug("BEFORE: left Button + line tool enabled")
        if self.dragging and self.line_tool_enabled:
            logging.debug("AFTER: left Button + line tool enabled")
            if self.temp_line is not None:
                self.scene.removeItem(self.temp_line)
            self.p1 = self.mapToScene(pos_viewport.toPoint())
            self.temp_line = self.scene.draw_line(self.p0.x(), self.p0.y(), self.p1.x(), self.p1.y())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self.line_tool_enabled:
            self.dragging = False
            pos_viewport = event.position()  # Gives position w/in viewport.
            self.p1 = self.mapToScene(pos_viewport.toPoint())
            self.scene.draw_line(self.p0.x(), self.p0.y(), self.p1.x(), self.p1.y())
            self.temp_line = None

    def wheelEvent(self, event: QWheelEvent):
        """ Zoom in/out centered around mouse position. """
        super().wheelEvent(event)  # Inherited class wheelEvent gets triggered. Not used here. Seems like good practice.
        logging.debug("Zooming in/out")

        # Zoom in or out
        zoom_in = event.angleDelta().y() > 0
        factor = self.zoom_factor if zoom_in else 1 / self.zoom_factor
        new_zoom_scale = self.current_zoom_scale * factor

        # Zoom around the mouse position
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

        if self.min_zoom_scale <= new_zoom_scale <= self.max_zoom_scale:
            pos_viewport = event.position()  # Gives position w/in viewport.

            old_center = self.mapToScene(pos_viewport.toPoint())
            self.scale(factor, factor)
            new_center = self.mapToScene(pos_viewport.toPoint())
            d = new_center - old_center
            self.translate(d.x(), d.y())
            self.current_zoom_scale = new_zoom_scale
            logging.debug(f"center: x, y: {old_center.x():.2f}, {old_center.y():.2f}")
            logging.debug(f"current_scale: {self.current_zoom_scale}\n")

        # Update scale label
        self.parent.update_zoom_scale_label()
