import io
import flumut
import contextlib

from PyQt5.QtWidgets import QLabel, QDialog, QProgressBar, QTextEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class FluMutWorker(QThread):
    started = pyqtSignal()
    stdout = pyqtSignal(io.StringIO)
    stderr = pyqtSignal(io.StringIO)
    error = pyqtSignal(Exception)
    ended = pyqtSignal()

    def __init__(self, args_dict):
        QThread.__init__(self)
        self.args_dict = args_dict
        self._stderr = io.StringIO()

    def __del__(self):
        print('del')
        self.wait()

    def run(self):
        # total_sequences = len(re.findall(r'^>.+', self.args_dict['fasta_file'].read(), re.M))
        # self.args_dict['fasta_file'].seek(0)
        # self.args_dict['verbose'] = True

        # self.started.emit(total_sequences)

        try:
            with contextlib.redirect_stderr(io.StringIO()) as stderr, contextlib.redirect_stdout(io.StringIO()) as stdout:
                flumut.analyze(**self.args_dict)
        except Exception as e:
            self.error.emit(e)
            return

        stdout.seek(0)
        stderr.seek(0)
        self.stdout.emit(stdout)
        self.stderr.emit(stderr)
        self.ended.emit()


class ProgressWindow(QDialog):
    def __init__(self, args_dict) -> None:
        super().__init__()
        self.init_ui()
        self.setModal(True)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.flumut_arguments = args_dict
        self.log_txt.append("Executing FluMut...")
        self.start_flumut()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setLayout(layout)
        self.setWindowTitle('Executing FluMut')
        self.setMinimumWidth(450)
        self.setMinimumHeight(300)


        self.progress_lbl = QLabel("Executing FluMut command...")
        layout.addWidget(self.progress_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        self.log_lbl = QLabel("Log:")
        layout.addWidget(self.log_lbl)

        self.log_txt = QTextEdit()
        self.log_txt.setReadOnly(True)
        layout.addWidget(self.log_txt)

        self.cancel_btn = QPushButton("Cancel")
        layout.addWidget(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.cancel_flumut)

    def start_flumut(self):
        def handle_start(total_sequences):
            self.progress_bar.setRange(0, total_sequences + 1)
            self.progress_bar.setValue(0)
            self.log_txt.append(f'Detected {total_sequences} sequences.')

        def handle_end():
            self.log_txt.setTextColor(Qt.black)
            self.log_txt.append("Analysis ended without errors.")
            self.progress_bar.setValue(self.progress_bar.maximum())
            self.cancel_btn.setText("Close")

        def handle_error(error):
            self.progress_bar.setValue(self.progress_bar.maximum())
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red;}")
            self.log_txt.setTextColor(Qt.red)
            self.log_txt.append(f'{error.__class__.__name__}: {str(error)}')
            self.cancel_btn.setText("Close")
            QMessageBox.warning(self, error.__class__.__name__, str(error))

        def log_stdout(stdout):
            self.log_txt.setTextColor(Qt.black)
            self.log_txt.append(stdout.read())

        def log_stderr(stderr):
            self.log_txt.setTextColor(Qt.red)
            self.log_txt.append(stderr.read())

        self.flumut_thread = FluMutWorker(self.flumut_arguments)
        self.flumut_thread.started.connect(handle_start)
        self.flumut_thread.ended.connect(handle_end)
        self.flumut_thread.error.connect(handle_error)
        self.flumut_thread.stdout.connect(log_stdout)
        self.flumut_thread.stderr.connect(log_stderr)

        self.flumut_thread.start()

    def cancel_flumut(self):
        if self.cancel_btn.text() == "Close":
            self.close()
        else:
            self.log_txt.setTextColor(Qt.black)
            self.log_txt.append("Stopping FluMut analysis...")
            self.flumut_thread.terminate()
            self.log_txt.append("Process terminated.")
            self.progress_bar.setValue(self.progress_bar.maximum())
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red;}")
            self.cancel_btn.setText("Close")
