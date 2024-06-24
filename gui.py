
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        """ pass main window as parent to open directly above it"""
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel  # | Ok | Open | Save

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        dlg = CustomDialog()
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

app = QApplication([])
w = MainWindow()
w.show()
app.exec()