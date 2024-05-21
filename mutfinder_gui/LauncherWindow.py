from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QCheckBox, QErrorMessage
from PyQt5.QtCore import Qt

from mutfinder_gui.ProgressWindow import ProgressWindow


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
        self.excel_row.setEnabled(False)
        self.excel_lbl = QLabel("Output XLSM:")
        self.excel_lbl.setEnabled(False)
        
        self.tabular_row = self.create_output_tabular_row()
        self.tabular_row.setEnabled(False)
        self.tabular_lbl = QLabel("Output TSV:")
        self.tabular_lbl.setEnabled(False)
        
        self.matrix_row = self.create_output_matrix_row()
        self.matrix_row.setEnabled(False)
        self.matrix_lbl = QLabel("Output TSV:")
        self.matrix_lbl.setEnabled(False)

        self.strict_mode_chk = QCheckBox()

        self.excel_chk = QCheckBox()
        self.excel_chk.toggled.connect(lambda: self.checkbox_tooggled(self.excel_chk, self.excel_lbl, self.excel_row))
        
        self.tabular_chk = QCheckBox()
        self.tabular_chk.toggled.connect(lambda: self.checkbox_tooggled(self.tabular_chk, self.tabular_lbl, self.tabular_row))
        
        self.matrix_chk = QCheckBox()
        self.matrix_chk.toggled.connect(lambda: self.checkbox_tooggled(self.matrix_chk, self.matrix_lbl, self.matrix_row))

        self.launch_btn = QPushButton("Launch")
        self.launch_btn.clicked.connect(self.launch_mutfinder)
        
        layout.addRow("Input FASTA:", self.fasta_row)
        layout.addRow("Strict mode:", self.strict_mode_chk)
        layout.addRow("Create Excel report:", self.excel_chk)
        layout.addRow(self.excel_lbl, self.excel_row)
        layout.addRow("Create Tabular report:", self.tabular_chk)
        layout.addRow(self.tabular_lbl, self.tabular_row)
        layout.addRow("Create Matrix report:", self.matrix_chk)
        layout.addRow(self.matrix_lbl, self.matrix_row)
        layout.addRow("", None)
        layout.addRow("", self.launch_btn)


    def checkbox_tooggled(self, checkbox, label, row):
        row.setEnabled(checkbox.isChecked())
        label.setEnabled(checkbox.isChecked())
    

    def create_input_fasta_row(self):
        layout = QHBoxLayout()
        row = QWidget()
        row.setLayout(layout)

        def browse_input_fasta():
            options = QFileDialog.Options()
            fname, _ = QFileDialog.getOpenFileName(None, "Open input FASTA", "", "FASTA files (*.fasta *.fas *.fa);;All Files (*)", options=options)
            if fname:
                line_edit.setText(fname)

        line_edit = QLineEdit()

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
            dialog = QFileDialog()
            dialog.setDefaultSuffix("xlsm")
            fname, _ = dialog.getSaveFileName(None, "Save Excel output as...", "", "XLSM files (*.xlsm)")
            
            if fname:
                if not fname.endswith(".xlsm"):
                    fname += ".xlsm"
                line_edit.setText(fname)

        line_edit = QLineEdit()
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
            dialog = QFileDialog()
            dialog.setDefaultSuffix("tsv")
            fname, _ = dialog.getSaveFileName(None, "Save Tabular output as...", "", "TSV files (*.tsv)")
            
            if fname:
                if not fname.endswith(".tsv"):
                    fname += ".tsv"
                line_edit.setText(fname)

        line_edit = QLineEdit()
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
            dialog = QFileDialog()
            dialog.setDefaultSuffix("tsv")
            fname, _ = dialog.getSaveFileName(None, "Save Matrix output as...", "", "TSV files (*.tsv)")
            
            if fname:
                if not fname.endswith(".tsv"):
                    fname += ".tsv"
                line_edit.setText(fname)

        line_edit = QLineEdit()
        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_output_matrix)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row


    def launch_mutfinder(self):
        launch_options = {
            "input_fasta": self.fasta_row.layout().itemAt(0).widget().text().strip(),
            "strict_mode": self.strict_mode_chk.isChecked(),
            "create_excel": self.excel_chk.isChecked(),
            "output_excel": self.excel_row.layout().itemAt(0).widget().text().strip(),
            "create_tabular": self.tabular_chk.isChecked(),
            "output_tabular": self.tabular_row.layout().itemAt(0).widget().text().strip(),
            "create_matrix": self.matrix_chk.isChecked(),
            "output_matrix": self.matrix_row.layout().itemAt(0).widget().text().strip()
        }

        def launch_error(msg):
            print("Launch error:", msg)
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(msg)

        if launch_options['input_fasta'] == "":
            return launch_error("No input FASTA file selected")
        if not launch_options['create_excel'] and not launch_options['create_tabular'] and not launch_options['create_matrix']:
            return launch_error("No output selected")
        if launch_options['create_excel'] and launch_options['output_excel'] == "":
            return launch_error("No output Excel file selected")
        if launch_options['create_tabular'] and launch_options['output_tabular'] == "":
            return launch_error("No output Tabular file selected")
        if launch_options['create_matrix'] and launch_options['output_matrix'] == "":
            return launch_error("No output Matrix file selected")
        
        print("Launch options:")
        for key, value in launch_options.items():
            print(f"  {key:.<20}{value}")

        cmd = ["mutfinder"]

        if launch_options["strict_mode"]:
            cmd.append("-s")
        if launch_options["create_excel"]:
            cmd.extend(["-x", launch_options['output_excel']])
        if launch_options["create_tabular"]:
            cmd.extend(["-t", launch_options['output_tabular']])
        if launch_options["create_matrix"]:
            cmd.extend(["-m", launch_options['output_matrix']])
        cmd.append(launch_options['input_fasta'])

        print("Launching:", cmd)
        ProgressWindow(cmd).exec_()

