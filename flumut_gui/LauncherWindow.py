import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QCheckBox, QMessageBox, QApplication
from PyQt5.QtCore import Qt

from flumut_gui.ProgressWindow import ProgressWindow
import flumut


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
        layout.setContentsMargins(0,0,0,0)

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


class LauncherWindow(QWidget):
    def __init__(self) -> None:
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
        self.setFixedHeight(450)

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
        input_fasta = self.fasta_row.get_opened_file()
        output_excel = self.excel_row.get_file_path()
        output_markers = self.markers_row.get_opened_file()
        output_mutations = self.mutations_row.get_opened_file()
        output_literature = self.literature_row.get_opened_file()

        def launch_error(msg):
            QMessageBox.warning(self, 'Missing parameter', msg)

        if not input_fasta:
            return launch_error("No input FASTA file selected")
        if not output_excel and not output_markers and not output_mutations and not output_literature:
            return launch_error("At least one output type must be selected")
        if self.excel_row.is_enabled_row() and not output_excel:
            return launch_error("No output Excel file selected")
        if self.markers_row.is_enabled_row() and not output_markers:
            return launch_error("No output Markers file selected")
        if self.mutations_row.is_enabled_row() and not output_mutations:
            return launch_error("No output Mutations file selected")
        if self.literature_row.is_enabled_row() and not output_literature:
            return launch_error("No output Literature file selected")

        QApplication.setOverrideCursor(Qt.WaitCursor)
        flumut.analyze(None, input_fasta , None,
                output_markers, output_mutations, output_literature, output_excel)
        
        input_fasta.close()
        if output_markers:
            output_markers.close()
        if output_mutations: 
            output_mutations.close()
        if output_literature:
            output_literature.close()
        QApplication.restoreOverrideCursor()

        QMessageBox.information(self, 'Analysis complete', f'Completed analysis without errors')


    def update_database(self):
        if self.is_pyinstaller():
            flumut.update_db_file()
        else:
            flumut.update()
        QMessageBox.information(self, 'Updated FluMutDB', f'Updated FluMutDB to version {flumut.versions()["FluMutDB"]}')

    def is_pyinstaller(self):
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
