from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        button = QPushButton("Press Me")
        button.setCheckable(True)
        button.clicked.connect(self.button_clicked)
        button.clicked.connect(self.button_toggled)

        self.setWindowTitle("Sound Map")
        # self.setFixedSize(QSize(400, 300))
        # self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(400, 300))
        self.setCentralWidget(button)

    def button_clicked(self):
        print("clicked")
    def button_toggled(self, checked):
        print("checked?", checked)


# You need one (and only one) QApplication instance per application.
app = QApplication([])

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.
