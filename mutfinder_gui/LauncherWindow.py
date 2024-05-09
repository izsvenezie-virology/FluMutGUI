from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


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
        self.setWindowTitle('Launch MutFinder')
        self.setFixedWidth(600)

        self.fasta_row = self.create_input_fasta_row()
        self.excel_row = self.create_output_excel_row()
        self.tabular_row = self.create_output_tabular_row()
        self.matrix_row = self.create_output_matrix_row()

        self.excel_lbl = QLabel("Output XLSM:")
        self.tabular_lbl = QLabel("Output TSV:")
        self.matrix_lbl = QLabel("Output TSV:")

        self.excel_row.setEnabled(False)
        self.excel_lbl.setEnabled(False)
        self.tabular_row.setEnabled(False)
        self.tabular_lbl.setEnabled(False)
        self.matrix_row.setEnabled(False)
        self.matrix_lbl.setEnabled(False)

        self.excel_chk = QCheckBox()
        self.excel_chk.toggled.connect(lambda: self.excel_row.setEnabled(self.excel_chk.isChecked()) or self.excel_lbl.setEnabled(self.excel_chk.isChecked()))
        
        self.tabular_chk = QCheckBox()
        self.tabular_chk.toggled.connect(lambda: self.tabular_row.setEnabled(self.tabular_chk.isChecked()) or self.tabular_lbl.setEnabled(self.tabular_chk.isChecked()))
        
        self.matrix_chk = QCheckBox()
        self.matrix_chk.toggled.connect(lambda: self.matrix_row.setEnabled(self.matrix_chk.isChecked()) or self.matrix_lbl.setEnabled(self.matrix_chk.isChecked()))

        self.launch_btn = QPushButton("Launch")
        self.launch_btn.clicked.connect(self.launch_mutfinder)
        
        layout.addRow("Input FASTA:", self.fasta_row)
        layout.addRow("Create Excel report:", self.excel_chk)
        layout.addRow(self.excel_lbl, self.excel_row)
        layout.addRow("Create Tabular report:", self.tabular_chk)
        layout.addRow(self.tabular_lbl, self.tabular_row)
        layout.addRow("Create Matrix report:", self.matrix_chk)
        layout.addRow(self.matrix_lbl, self.matrix_row)
        layout.addRow("", None)
        layout.addRow("", self.launch_btn)


    def create_input_fasta_row(self):
        layout = QHBoxLayout()
        row = QWidget()
        row.setLayout(layout)

        def browse_input_fasta():
            options = QFileDialog.Options()
            fname, _ = QFileDialog.getOpenFileName(None, "Open input FASTA", "", "FASTA files (*.fasta,*.fas,*.fa);;All Files (*)", options=options)
            if fname:
                line_edit.setText(fname)

        line_edit = QLineEdit()
        line_edit.setReadOnly(True)

        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_input_fasta)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row
    

    def create_output_excel_row(self):
        layout = QHBoxLayout()
        row = QWidget()
        row.setLayout(layout)

        def browse_output_excel():
            options = QFileDialog.Options()
            fname, _ = QFileDialog.getSaveFileName(None, "Save Excel output as...", "", "XLSM files (*.xlsm);;All Files (*)", options=options)
            if fname:
                line_edit.setText(fname)

        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_output_excel)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row


    def create_output_tabular_row(self):
        layout = QHBoxLayout()
        row = QWidget()
        row.setLayout(layout)

        def browse_output_tabular():
            options = QFileDialog.Options()
            fname, _ = QFileDialog.getSaveFileName(None, "Save Tabular output as...", "", "TSV files (*.tsv);;All Files (*)", options=options)
            if fname:
                line_edit.setText(fname)

        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_output_tabular)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row
    

    def create_output_matrix_row(self):
        layout = QHBoxLayout()
        row = QWidget()
        row.setLayout(layout)

        def browse_output_matrix():
            options = QFileDialog.Options()
            fname, _ = QFileDialog.getSaveFileName(None, "Save Matrix output as...", "", "TSV files (*.tsv);;All Files (*)", options=options)
            if fname:
                line_edit.setText(fname)

        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_output_matrix)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row


    def launch_mutfinder(self):
        launch_options = {
            "input_fasta": self.fasta_row.layout().itemAt(0).widget().text(),
            "create_excel": self.excel_chk.isChecked(),
            "output_excel": self.excel_row.layout().itemAt(0).widget().text(),
            "create_tabular": self.tabular_chk.isChecked(),
            "output_tabular": self.tabular_row.layout().itemAt(0).widget().text(),
            "create_matrix": self.matrix_chk.isChecked(),
            "output_matrix": self.matrix_row.layout().itemAt(0).widget().text()
        }

        print("Launching MutFinder with options:")
        for key, value in launch_options.items():
            print(f"\t{key}:\t{value}")

    
