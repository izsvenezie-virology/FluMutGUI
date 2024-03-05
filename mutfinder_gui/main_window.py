import sys
from PyQt5.QtWidgets import QApplication, QWidget


def launch_gui():
    app = QApplication(sys.argv)

    win = QWidget()
    win.setWindowTitle('Hello World')
    win.resize(250, 250)
    win.show()

    sys.exit(app.exec_())
