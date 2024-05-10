import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QAction, QStyle, QTabWidget, QFileDialog
from PyQt5 import QtCore

from mutfinder_gui.SampleTreeTab import SampleTreeTab
from mutfinder_gui.LauncherWindow import LauncherWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('MutFinder GUI')
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        
        def open_report():
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(None, "Open MutFinder Results", "","JSON files (*.json);;All Files (*)", options=options)
            if fileName:
                print(fileName)

        def launch_mutfinder():
            print("Launch MutFinder")


        launch_icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        launch_action = QAction(launch_icon, "Launch MutFinder", self)
        launch_action.triggered.connect(launch_mutfinder)

        open_icon = self.style().standardIcon(QStyle.SP_DialogOpenButton)
        open_action = QAction(open_icon, "Open MutFinder report", self)
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
    
    # win = MainWindow()
    # win.showMaximized()

    win = LauncherWindow()
    win.show()

    sys.exit(app.exec_())
