from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt

from flumut_gui.ProgressWindow import ProgressWindow


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

        self.fasta_row = self.create_input_fasta_row()

        self.excel_row = self.create_output_excel_row()
        self.excel_row.setEnabled(False)
        self.excel_lbl = QLabel("Output XLSM:")
        self.excel_lbl.setEnabled(False)
        
        self.markers_row = self.create_output_markers_row()
        self.markers_row.setEnabled(False)
        self.markers_lbl = QLabel("Output TSV:")
        self.markers_lbl.setEnabled(False)
        
        self.mutations_row = self.create_output_mutations_row()
        self.mutations_row.setEnabled(False)
        self.mutations_lbl = QLabel("Output TSV:")
        self.mutations_lbl.setEnabled(False)
        
        self.literature_row = self.create_output_literature_row()
        self.literature_row.setEnabled(False)
        self.literature_lbl = QLabel("Output TSV:")
        self.literature_lbl.setEnabled(False)

        self.relaxed_mode_chk = QCheckBox()

        self.excel_chk = QCheckBox()
        self.excel_chk.toggled.connect(lambda: self.checkbox_tooggled("excel"))
        
        self.markers_chk = QCheckBox()
        self.markers_chk.toggled.connect(lambda: self.checkbox_tooggled("markers"))
        
        self.mutations_chk = QCheckBox()
        self.mutations_chk.toggled.connect(lambda: self.checkbox_tooggled("mutations"))

        self.literature_chk = QCheckBox()
        self.literature_chk.toggled.connect(lambda: self.checkbox_tooggled("literature"))

        self.launch_btn = QPushButton("Launch")
        self.launch_btn.clicked.connect(self.launch_flumut)

        self.update_btn = QPushButton('Update database')
        self.update_btn.clicked.connect(self.update_database)
        
        layout.addRow("Input FASTA:", self.fasta_row)
        layout.addRow("Relaxed mode:", self.relaxed_mode_chk)
        layout.addRow("Create Excel report:", self.excel_chk)
        layout.addRow(self.excel_lbl, self.excel_row)
        
        layout.addRow("Create Markers report:", self.markers_chk)
        layout.addRow(self.markers_lbl, self.markers_row)
        layout.addRow("Create Mutations report:", self.mutations_chk)
        layout.addRow(self.mutations_lbl, self.mutations_row)
        layout.addRow("Create Literature report:", self.literature_chk)
        layout.addRow(self.literature_lbl, self.literature_row)
        layout.addRow("", None)
        layout.addRow("", self.launch_btn)
        layout.addRow('', None)
        layout.addRow('', self.update_btn)


    def checkbox_tooggled(self, target):
        checkbox =  {
            "excel": self.excel_chk,
            "markers": self.markers_chk,
            "mutations": self.mutations_chk,
            "literature": self.literature_chk
        }[target]
        
        row = {
            "excel": self.excel_row,
            "markers": self.markers_row,
            "mutations": self.mutations_row,
            "literature": self.literature_row
        }[target]

        label = {
            "excel": self.excel_lbl,
            "markers": self.markers_lbl,
            "mutations": self.mutations_lbl,
            "literature": self.literature_lbl
        }[target]
        
        file_suffix = {
            "excel": ".xlsm",
            "markers": "_markers.tsv",
            "mutations": "_mutations.tsv",
            "literature": "_literature.tsv"
        }[target]

        chk_state = checkbox.isChecked()
        row.setEnabled(chk_state)
        label.setEnabled(chk_state)

        # If a FASTA path exists, take the basename and use it as the default output filename
        fasta_text = self.fasta_row.layout().itemAt(0).widget().text()
        curr_text = row.layout().itemAt(0).widget().text()
        if chk_state and curr_text == "" and fasta_text != "":
            basename = fasta_text.rsplit('.', 1)[0]
            row.layout().itemAt(0).widget().setText(basename + file_suffix)
    

    def create_input_fasta_row(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
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
        layout.setContentsMargins(0,0,0,0)
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


    def create_output_markers_row(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        row = QWidget()
        row.setLayout(layout)

        def browse_output_markers():
            dialog = QFileDialog()
            dialog.setDefaultSuffix("tsv")
            fname, _ = dialog.getSaveFileName(None, "Save Markers output as...", "", "TSV files (*.tsv)")
            
            if fname:
                if not fname.endswith(".tsv"):
                    fname += ".tsv"
                line_edit.setText(fname)

        line_edit = QLineEdit()
        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_output_markers)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row
    

    def create_output_mutations_row(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        row = QWidget()
        row.setLayout(layout)

        def browse_output_mutations():
            dialog = QFileDialog()
            dialog.setDefaultSuffix("tsv")
            fname, _ = dialog.getSaveFileName(None, "Save Mutations output as...", "", "TSV files (*.tsv)")
            
            if fname:
                if not fname.endswith(".tsv"):
                    fname += ".tsv"
                line_edit.setText(fname)

        line_edit = QLineEdit()
        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_output_mutations)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row
    

    def create_output_literature_row(self):
        layout = QHBoxLayout()
        row = QWidget()
        row.setLayout(layout)

        def browse_output_literature():
            dialog = QFileDialog()
            dialog.setDefaultSuffix("tsv")
            fname, _ = dialog.getSaveFileName(None, "Save Literature output as...", "", "TSV files (*.tsv)")
            
            if fname:
                if not fname.endswith(".tsv"):
                    fname += ".tsv"
                line_edit.setText(fname)

        line_edit = QLineEdit()
        btn = QPushButton("Browse...")
        btn.clicked.connect(browse_output_literature)

        layout.addWidget(line_edit)
        layout.addWidget(btn)

        return row


    def launch_flumut(self):
        launch_options = {
            "input_fasta": self.fasta_row.layout().itemAt(0).widget().text().strip(),
            "relaxed_mode": self.relaxed_mode_chk.isChecked(),
            "create_excel": self.excel_chk.isChecked(),
            "output_excel": self.excel_row.layout().itemAt(0).widget().text().strip(),
            "create_markers": self.markers_chk.isChecked(),
            "output_markers": self.markers_row.layout().itemAt(0).widget().text().strip(),
            "create_mutations": self.mutations_chk.isChecked(),
            "output_mutations": self.mutations_row.layout().itemAt(0).widget().text().strip(),
            "create_literature": self.literature_chk.isChecked(),
            "output_literature": self.literature_row.layout().itemAt(0).widget().text().strip()
        }

        def launch_error(msg):
            print("Launch error:", msg)
            QMessageBox.warning(self, 'Missing parameter', msg)

        if launch_options['input_fasta'] == "":
            return launch_error("No input FASTA file selected")
        if not launch_options['create_excel'] and not launch_options['create_markers'] and not launch_options['create_mutations'] and not launch_options['create_literature']:
            return launch_error("At least one output type must be selected")
        if launch_options['create_excel'] and launch_options['output_excel'] == "":
            return launch_error("No output Excel file selected")
        if launch_options['create_markers'] and launch_options['output_markers'] == "":
            return launch_error("No output Markers file selected")
        if launch_options['create_mutations'] and launch_options['output_mutations'] == "":
            return launch_error("No output Mutations file selected")
        if launch_options['create_literature'] and launch_options['output_literature'] == "":
            return launch_error("No output Literature file selected")
        
        print("Launch options:")
        for key, value in launch_options.items():
            print(f"  {key:.<20}{value}")

        cmd = ["flumut"]

        if launch_options["relaxed_mode"]:
            cmd.append("-r")
        if launch_options["create_excel"]:
            cmd.extend(["-x", launch_options['output_excel']])
        if launch_options["create_markers"]:
            cmd.extend(["-m", launch_options['output_markers']])
        if launch_options["create_mutations"]:
            cmd.extend(["-M", launch_options['output_mutations']])
        if launch_options["create_literature"]:
            cmd.extend(["-l", launch_options['output_literature']])
        
        cmd.append(launch_options['input_fasta'])

        print("Launching:", cmd)
        ProgressWindow(cmd).exec()


    def update_database(self):
        progr_window = ProgressWindow(['flumut', '--update'])
        progr_window.setWindowTitle('Updating FluMut database...')
        progr_window.exec()
