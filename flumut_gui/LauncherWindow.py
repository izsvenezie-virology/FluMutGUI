import sys
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QCheckBox, QMessageBox, QApplication
from PyQt5.QtCore import Qt

from flumut_gui.ProgressWindow import ProgressWindow
import flumut


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
        layout.setContentsMargins(0,0,0,0)
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

        fasta = open(launch_options["input_fasta"], 'r', encoding="utf-8")
        if not launch_options["create_excel"]:
            launch_options["output_excel"] = None
        if launch_options["create_markers"]:
            markers = open(launch_options["output_markers"], 'w', encoding="utf-8")
        else:
            markers = None
        if launch_options["create_mutations"]:
            mutations = open(launch_options["output_mutations"], 'w', encoding="utf-8")
        else:
            mutations = None
        if launch_options["create_literature"]:
            literature = open(launch_options["output_literature"], 'w', encoding="utf-8")
        else:
            literature = None

        QApplication.setOverrideCursor(Qt.WaitCursor)
        flumut.analyze(None, fasta , None,
                markers, mutations, literature, launch_options["output_excel"],
                launch_options["relaxed_mode"])
        QApplication.restoreOverrideCursor()

        fasta.close()
        if markers:
            markers.close()
        if mutations:
            mutations.close()
        if literature:
            literature.close()

        QMessageBox.information(self, 'Analysis complete', f'Completed analysis without errors')


    def update_database(self):
        if self.is_pyinstaller():
            flumut.update_db_file()
        else:
            flumut.update()
        QMessageBox.information(self, 'Updated FluMutDB', f'Updated FluMutDB to version {flumut.versions()["FluMutDB"]}')

    def is_pyinstaller(self):
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
