
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel, \
    QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):

        button = QMessageBox.question(self, "Question dialog", "The longer message")
        # QMessageBox.about(parent, title, message)
        # QMessageBox.critical(parent, title, message)
        # QMessageBox.information(parent, title, message)
        # QMessageBox.question(parent, title, message)
        # QMessageBox.warning(parent, title, message)

        if button == QMessageBox.StandardButton.Yes:
            print("Yes!")
        else:
            print("No!")

app = QApplication([])
w = MainWindow()
w.show()
app.exec()