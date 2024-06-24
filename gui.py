from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout_h = QHBoxLayout()
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()

        layout_v1.addWidget(Color('red'))
        layout_v1.addWidget(Color('yellow'))
        layout_v1.addWidget(Color('purple'))

        layout_v2.addWidget(Color('orange'))
        layout_v2.addWidget(Color('blue'))
        layout_v2.addWidget(Color('green'))

        layout_h.addLayout(layout_v1)
        layout_h.addLayout(layout_v2)

        widget = QWidget()
        widget.setLayout(layout_h)
        self.setCentralWidget(widget)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()