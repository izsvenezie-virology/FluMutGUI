from typing import List
import subprocess

from PyQt5.QtWidgets import QLabel, QDialog, QProgressBar, QTextEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class FluMutWorker(QThread):
    started = pyqtSignal(int)
    output = pyqtSignal(str)
    error = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, cmd: List[str]):
        QThread.__init__(self, None)
        self.cmd = cmd
    
    def __del__(self):
        print('del')
        self.wait()
    
    def run(self):
        try:
            flumut_process = subprocess.Popen(self.cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            self.error.emit("Error: the process failed to start!")
            self.error.emit("Details:")
            self.error.emit(str(e))
            self.finished.emit(-1)
            return
        
        self.started.emit(flumut_process.pid)
        
        while True:
            line = flumut_process.stdout.readline().strip()
            if not line:
                break
            self.output.emit(line)
        
        flumut_process.wait()
        self.error.emit(flumut_process.stderr.read())
        self.finished.emit(flumut_process.returncode)
        


class ProgressWindow(QDialog):
    def __init__(self, flumut_arguments: List[str]) -> None:
        super().__init__()
        self.init_ui()
        self.setModal(True)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.flumut_arguments = flumut_arguments

        self.log_txt.append("Executing FluMut...")
        self.start_flumut()
    

    def init_ui(self):
        layout = QVBoxLayout()

        self.setLayout(layout)
        self.setWindowTitle('Executing FluMut')
        self.setFixedWidth(400)

        self.progress_lbl = QLabel("Executing FluMut command...")
        layout.addWidget(self.progress_lbl)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")

        self.log_lbl = QLabel("Log:")
        layout.addWidget(self.log_lbl)

        self.log_txt = QTextEdit()
        self.log_txt.setReadOnly(True)
        layout.addWidget(self.log_txt)

        self.cancel_btn = QPushButton("Cancel")
        layout.addWidget(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.cancel_flumut)
    

    def start_flumut(self):
        def log_start(pid):
            self.log_txt.append(f"Process started with PID {pid}")
            self.log_txt.append("Program output:\n")
            self.log_txt.setTextColor(Qt.darkGreen)
        
        def log_end(returncode):
            self.log_txt.setTextColor(Qt.black)
            self.log_txt.append("Process finished with return code " + str(returncode))
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(100)
            self.cancel_btn.setText("Close")
        
        def log_stdout(line):
            self.log_txt.append(line)

        def log_stderr(line):
            self.log_txt.setTextColor(Qt.red)
            self.log_txt.append(line)
            self.log_txt.setTextColor(Qt.black)

        self.log_txt.append("Launching with arguments: " + " ".join(self.flumut_arguments))
        self.flumut_thread = FluMutWorker(self.flumut_arguments)
        self.flumut_thread.started.connect(log_start)
        self.flumut_thread.output.connect(log_stdout)
        self.flumut_thread.error.connect(log_stderr)
        self.flumut_thread.finished.connect(log_end)
        
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)
        self.flumut_thread.start()


    def cancel_flumut(self):
        if self.cancel_btn.text() == "Close":
            self.close()
            # quit()
        else:
            self.log_txt.setTextColor(Qt.black)
            self.log_txt.append("Killing FluMut process...\n")
            self.flumut_thread.terminate()
            self.log_txt.append("Process terminated.")
            self.cancel_btn.setText("Close")
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
