import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QAction, QStyle, QTabWidget, QFileDialog
from PyQt5 import QtCore

from flumut_gui.SampleTreeTab import SampleTreeTab
from flumut_gui.LauncherWindow import LauncherWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('FluMut GUI')
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        
        def open_report():
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(None, "Open FluMut Results", "","JSON files (*.json);;All Files (*)", options=options)
            if fileName:
                print(fileName)

        def launch_flumut():
            print("Launch FluMut")


        launch_icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        launch_action = QAction(launch_icon, "Launch FluMut", self)
        launch_action.triggered.connect(launch_flumut)

        open_icon = self.style().standardIcon(QStyle.SP_DialogOpenButton)
        open_action = QAction(open_icon, "Open FluMut report", self)
        open_action.triggered.connect(open_report)

        toolbar = QToolBar('main_toolbar')
        toolbar.addAction(launch_action)
        toolbar.addAction(open_action)
        self.addToolBar(toolbar)

        tabs = QTabWidget()
        tab1 = SampleTreeTab()
        tab2 = QWidget()
        tabs.addTab(tab1, "View #1")
        tabs.addTab(tab2, "View #2")
        self.setCentralWidget(tabs)


def launch_gui():
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    
    # win = MainWindow()
    # win.showMaximized()

    win = LauncherWindow()
    win.show()

    sys.exit(app.exec())
