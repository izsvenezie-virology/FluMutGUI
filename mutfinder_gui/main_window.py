import sys
from PyQt5.QtWidgets import QApplication, QWidget


def launch_gui():
    app = QApplication(sys.argv)

    win = QWidget()
    win.setWindowTitle('Hello World')
    win.showMaximized()

    sys.exit(app.exec_())
