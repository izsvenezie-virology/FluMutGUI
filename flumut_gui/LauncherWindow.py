import sys
import traceback
from PyQt5.QtWidgets import QWidget, QFileDialog, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QCheckBox, QMessageBox, QApplication, QLabel
from PyQt5.QtCore import Qt

from flumut_gui.ProgressWindow import ProgressWindow
from flumut_gui import __version__
import flumut


def excepthook(exc_type, exc_value, exc_tb):
    tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    QMessageBox.warning(None, exc_type.__name__, tb)
    QApplication.quit()


class SelectFileRow(QWidget):
    def __init__(self, parent: QWidget, is_input: bool) -> None:
        super().__init__(parent)
        self._is_enabled_row = True
        self._init_ui(is_input)

    def set_enabled_row(self, enable: bool):
        self._chk_enable.setChecked(enable)

    def is_enabled_row(self):
        return self._is_enabled_row

    def set_switchable(self, switchable: bool):
        self._chk_enable.setVisible(switchable)

    def set_default_value(self, source, suffix):
        def set_default_name():
            source_path = source.get_file_path()
            if not self._is_enabled_row:
                return
            if self.get_file_path():
                return
            if not source_path:
                return
            basename = source_path.rsplit('.', 1)[0]
            self._txt_path.setText(basename + suffix)
        self._chk_enable.toggled.connect(set_default_name)

    def set_browse_parameters(self, title, filter):
        self._browse_title = title
        self._browse_filter = filter

    def get_file_path(self):
        return self._txt_path.text().strip()

    def get_opened_file(self):
        if not self.get_file_path():
            return None
        return open(self.get_file_path(), self._open_mode, encoding="utf-8")

    def _init_ui(self, is_input: bool):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self._chk_enable = QCheckBox()
        self._txt_path = QLineEdit()
        self._btn_browse = QPushButton("Browse...")

        def switch_enable():
            self._is_enabled_row = self._chk_enable.isChecked()
            self._txt_path.setEnabled(self._is_enabled_row)
            self._btn_browse.setEnabled(self._is_enabled_row)
            if not self._is_enabled_row:
                self._txt_path.setText(None)

        def browse_input():
            fname, _ = QFileDialog().getOpenFileName(None, self._browse_title, '', self._browse_filter)
            self._txt_path.setText(fname)

        def browse_output():
            fname, _ = QFileDialog().getSaveFileName(None, self._browse_title, '', self._browse_filter)
            self._txt_path.setText(fname)

        self._chk_enable.toggled.connect(switch_enable)
        self._chk_enable.setChecked(True)
        self._btn_browse.clicked.connect(browse_input if is_input else browse_output)
        self._open_mode = 'r' if is_input else 'w'

        layout.addWidget(self._chk_enable)
        layout.addWidget(self._txt_path)
        layout.addWidget(self._btn_browse)


class VersionRow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 20)

        self._lbl_versions = QLabel()
        self._lbl_versions.setAlignment(Qt.AlignRight)
        self._lbl_versions.setStyleSheet("QLabel {color : grey}")
        self._lbl_versions.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.update_text()
        layout.addWidget(self._lbl_versions)

    def update_text(self):
        versions = flumut.versions()
        self._lbl_versions.setText(f'FluMutGUI {__version__}; FluMut {versions["FluMut"]}; FluMutDB {versions  ["FluMutDB"]}')


class LauncherWindow(QWidget):
    def __init__(self) -> None:
        sys.excepthook = excepthook
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(15)

        self.setLayout(layout)
        self.setWindowTitle('Launch FluMut')
        self.setMinimumWidth(600)
        self.setFixedHeight(320)

        self.versions_row = VersionRow(self)
        layout.addRow(None, self.versions_row)

        self.fasta_row = SelectFileRow(self, True)
        self.fasta_row.set_switchable(False)
        self.fasta_row.set_browse_parameters("Open input FASTA", "FASTA files (*.fasta *.fas *.fa);;All Files (*)")
        layout.addRow("Input FASTA:", self.fasta_row)

        self.excel_row = SelectFileRow(self, False)
        self.excel_row.set_enabled_row(False)
        self.excel_row.set_default_value(self.fasta_row, '.xlsm')
        self.excel_row.set_browse_parameters("Save Excel output as...", "Excel files (*.xlsm *.xlsx)")
        layout.addRow("Excel output:", self.excel_row)

        self.markers_row = SelectFileRow(self, False)
        self.markers_row.set_enabled_row(False)
        self.markers_row.set_default_value(self.fasta_row, '_markers.tsv')
        self.markers_row.set_browse_parameters("Save Markers output as...", "TSV files (*.tsv)")
        layout.addRow("Markers output:", self.markers_row)

        self.mutations_row = SelectFileRow(self, False)
        self.mutations_row.set_enabled_row(False)
        self.mutations_row.set_default_value(self.fasta_row, '_mutations.tsv')
        self.mutations_row.set_browse_parameters("Save Mutations output as...", "TSV files (*.tsv)")
        layout.addRow("Mutations output:", self.mutations_row)

        self.literature_row = SelectFileRow(self, False)
        self.literature_row.set_enabled_row(False)
        self.literature_row.set_default_value(self.fasta_row, '_literature.tsv')
        self.literature_row.set_browse_parameters("Save Literature output as...", "TSV files (*.tsv)")
        layout.addRow("Literature output:", self.literature_row)

        self.launch_btn = QPushButton("Launch")
        self.launch_btn.clicked.connect(self.launch_flumut)
        layout.addRow(None, self.launch_btn)

        self.update_btn = QPushButton('Update database')
        self.update_btn.clicked.connect(self.update_database)
        layout.addRow(None, self.update_btn)

    def launch_flumut(self):
        try:
            args_dict = {
                'name_regex': None,
                'fasta_file': self.fasta_row.get_opened_file(),
                'db_file': None,
                'markers_output': self.markers_row.get_opened_file(),
                'mutations_output': self.mutations_row.get_opened_file(),
                'literature_output': self.literature_row.get_opened_file(),
                'excel_output': self.excel_row.get_file_path(),
                'relaxed': False,
                'skip_unmatch_names': True,
                'skip_unknown_segments': True,
                'debug': True
            }
        except FileNotFoundError as e:
            return QMessageBox.warning(self, 'File not found', f'Unable to open file {e.filename}.')

        def launch_error(msg):
            QMessageBox.warning(self, 'Missing parameter', msg)

        if not args_dict['fasta_file']:
            return launch_error("No input FASTA file selected")
        if not args_dict['excel_output'] and not args_dict['markers_output'] and not args_dict['mutations_output'] and not args_dict['literature_output']:
            return launch_error("At least one output type must be selected")
        if self.excel_row.is_enabled_row() and not args_dict['excel_output']:
            return launch_error("No output Excel file selected")
        if self.markers_row.is_enabled_row() and not args_dict['markers_output']:
            return launch_error("No output Markers file selected")
        if self.mutations_row.is_enabled_row() and not args_dict['mutations_output']:
            return launch_error("No output Mutations file selected")
        if self.literature_row.is_enabled_row() and not args_dict['literature_output']:
            return launch_error("No output Literature file selected")

        ProgressWindow(args_dict).exec()

        args_dict['fasta_file'].close()
        if args_dict['markers_output']:
            args_dict['markers_output'].close()
        if args_dict['mutations_output']:
            args_dict['mutations_output'].close()
        if args_dict['literature_output']:
            args_dict['literature_output'].close()

    def update_database(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if self.is_pyinstaller():
            flumut.update_db_file()
        else:
            flumut.update()
        self.versions_row.update_text()
        QApplication.restoreOverrideCursor()
        QMessageBox.information(self, 'Updated FluMutDB',
                                f'Updated FluMutDB to version {flumut.versions()["FluMutDB"]}')

    def is_pyinstaller(self):
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
