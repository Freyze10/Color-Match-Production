import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QGroupBox, QFormLayout, QFrame,
                             QScrollArea, QComboBox, QRadioButton, QCheckBox,
                             QButtonGroup, QGridLayout)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from util.field_format import SmartDateEdit


class RSEntry(QWidget):
    def __init__(self, mac_department, user_department):
        super().__init__()
        self.mac_department = mac_department
        self.user_department = user_department
        self.setStyleSheet(AppStyles.MAIN_WINDOW_STYLESHEET)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25) # Matched Spacing
        self.main_layout.setSpacing(20)

        # Title
        header = QLabel("RS Entry & Specifications")
        header.setStyleSheet("font-size: 22px; font-weight: bold; color: #0f172a;")
        self.main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        cont_layout = QVBoxLayout(container)
        cont_layout.setContentsMargins(0, 0, 10, 0)

        form_card = QFrame(objectName="FormCard")
        grid_layout = QHBoxLayout(form_card)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(40) # Matched Spacing

        # ==========================================
        # LEFT COLUMN: RS Tracking
        # ==========================================
        left_col = QFormLayout()
        left_col.setVerticalSpacing(15) # Matched Spacing

        self.txt_rs_no = QLineEdit()
        self.txt_rs_no.setPlaceholderText("Enter RS Number")
        self.txt_customer = QLineEdit()

        # ─── DATE ROW 1: Submitted & Required ───
        date_row_1 = QHBoxLayout()
        date_row_1.setSpacing(10)
        self.date_submitted = SmartDateEdit()
        self.txt_date_required = QLineEdit()
        self.txt_date_required.setPlaceholderText("MM/DD/YYYY")
        date_row_1.addWidget(self.date_submitted, 1)
        date_row_1.addWidget(QLabel("Required:"), 0)
        date_row_1.addWidget(self.txt_date_required, 1)

        # ─── DATE ROW 2: Received & Due ───
        date_row_2 = QHBoxLayout()
        date_row_2.setSpacing(10)
        self.date_received = SmartDateEdit(allow_multiple=True)
        self.date_due = SmartDateEdit()
        date_row_2.addWidget(self.date_received, 1)
        date_row_2.addWidget(QLabel("Due Date:"), 0)
        date_row_2.addWidget(self.date_due, 1)

        self.txt_product_codes = QLineEdit()
        self.txt_color_desc = QLineEdit()
        self.txt_finished_prod = QLineEdit()
        self.txt_match_type = QLineEdit()
        self.txt_salesperson = QLineEdit()

        left_col.addRow("RS Number:", self.txt_rs_no)
        left_col.addRow("Customer:", self.txt_customer)
        left_col.addRow("Date Created:", date_row_1)
        left_col.addRow("Date Received:", date_row_2)
        left_col.addRow("Product Code(s):", self.txt_product_codes)
        left_col.addRow("Color Description:", self.txt_color_desc)
        left_col.addRow("Finished Product:", self.txt_finished_prod)
        left_col.addRow("Matching Type:", self.txt_match_type)
        left_col.addRow("Sales Person:", self.txt_salesperson)

        # ==========================================
        # RIGHT COLUMN: RS Technical Specs
        # ==========================================
        right_col = QFormLayout()
        right_col.setVerticalSpacing(15)

        self.txt_resin = QLineEdit()

        # Dosage (Float only)
        self.txt_dosage = QLineEdit()
        self.txt_dosage.setPlaceholderText("0.000000")
        dosage_val = QDoubleValidator(0.0, 100.0, 6)
        dosage_val.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.txt_dosage.setValidator(dosage_val)

        # Process Selection
        proc_grid = QGridLayout()
        self.chk_inj = QCheckBox("Injection"); self.chk_blow = QCheckBox("Blow-Molding"); self.chk_film = QCheckBox("Film")
        self.chk_pipe = QCheckBox("Pipe Extrusion"); self.chk_proc_others = QCheckBox("Others:")
        self.txt_proc_others = QLineEdit(); self.txt_proc_others.setPlaceholderText("Specify...")
        proc_grid.addWidget(self.chk_inj, 0, 0); proc_grid.addWidget(self.chk_blow, 0, 1); proc_grid.addWidget(self.chk_film, 0, 2)
        proc_grid.addWidget(self.chk_pipe, 1, 0); proc_grid.addWidget(self.chk_proc_others, 1, 1); proc_grid.addWidget(self.txt_proc_others, 1, 2)

        # Colorant Type
        colorant_lay = QHBoxLayout()
        self.colorant_bg = QButtonGroup(self)
        self.rad_mb = QRadioButton("MB"); self.rad_dc = QRadioButton("DC"); self.rad_colant_others = QRadioButton("Others:")
        for r in [self.rad_mb, self.rad_dc, self.rad_colant_others]:
            self.colorant_bg.addButton(r); colorant_lay.addWidget(r)
        self.txt_colorant_others = QLineEdit()
        colorant_lay.addWidget(self.txt_colorant_others)

        # Color Requirement (Manual Positioning Grid)
        color_req_grid = QGridLayout()
        self.color_req_bg = QButtonGroup(self)
        req_list = ["Transparent", "Opaque", "Translucent", "Metallic", "Fluorescent"]
        for i, name in enumerate(req_list):
            rad = QRadioButton(name)
            self.color_req_bg.addButton(rad)
            color_req_grid.addWidget(rad, 0, i) # Row 0: 5 items

        self.rad_pearlescent = QRadioButton("Pearlescent")
        self.rad_req_others = QRadioButton("Others:")
        self.txt_req_others = QLineEdit(); self.txt_req_others.setPlaceholderText("Specify...")
        self.color_req_bg.addButton(self.rad_pearlescent); self.color_req_bg.addButton(self.rad_req_others)

        color_req_grid.addWidget(self.rad_pearlescent, 1, 0)
        color_req_grid.addWidget(self.rad_req_others, 1, 1)
        color_req_grid.addWidget(self.txt_req_others, 1, 2, 1, 3) # Spans remaining width

        right_col.addRow("Resin:", self.txt_resin)
        right_col.addRow("Dosage (%):", self.txt_dosage)
        right_col.addRow("Process:", proc_grid)
        right_col.addRow("Colorant Type:", colorant_lay)
        right_col.addRow("Color Requirement:", color_req_grid)

        grid_layout.addLayout(left_col, 1)
        grid_layout.addLayout(right_col, 1)

        cont_layout.addWidget(form_card)
        cont_layout.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # Footer Buttons (Upload on Left, rest on Right)
        footer = QHBoxLayout()
        self.btn_upload = QPushButton(" Upload", objectName="PrimaryButton")
        self.btn_upload.setIcon(fa.icon('mdi6.text-box-remove', color='white'))
        self.btn_print = QPushButton(" Print", objectName="SecondaryButton")
        self.btn_print.setIcon(fa.icon('fa5s.print', color='white'))
        self.btn_new = QPushButton(" New", objectName="InfoButton")
        self.btn_new.setIcon(fa.icon('fa5s.file', color='white'))
        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))

        for btn in [self.btn_upload, self.btn_print, self.btn_new, self.btn_save]:
            btn.setFixedSize(140, 45)

        footer.addWidget(self.btn_upload)
        footer.addStretch()
        footer.addWidget(self.btn_print)
        footer.addWidget(self.btn_new)
        footer.addWidget(self.btn_save)
        self.main_layout.addLayout(footer)

    def load_rs_data(self, rs_no):
        self.txt_rs_no.setText(rs_no)