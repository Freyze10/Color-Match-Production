import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QRadioButton, QCheckBox, QPushButton, QScrollArea,
                             QFrame, QGroupBox, QFormLayout, QButtonGroup,
                             QGridLayout, QComboBox)
from PyQt6.QtGui import QDoubleValidator
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
        # 1. Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 0)
        self.main_layout.setSpacing(10)

        # 2. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setSpacing(15)

        # =========================================================================
        # MAIN FORM CARD
        # =========================================================================
        form_card = QFrame(objectName="FormCard")
        columns_layout = QHBoxLayout(form_card)
        columns_layout.setContentsMargins(20, 20, 20, 20)
        columns_layout.setSpacing(30)

        # --- LEFT COLUMN: Tracking & Personal ---
        left_col_form = QFormLayout()
        left_col_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        left_col_form.setVerticalSpacing(12)

        self.txt_rs_no = QLineEdit()
        self.txt_customer = QLineEdit()
        self.txt_sales_person = QLineEdit()

        # Matching Type
        type_lay = QHBoxLayout()
        self.rad_new = QRadioButton("New")
        self.rad_rematch = QRadioButton("Re-Match")
        self.rad_new.setChecked(True)
        type_lay.addWidget(self.rad_new);
        type_lay.addWidget(self.rad_rematch);
        type_lay.addStretch()

        # Dates
        date_row_1 = QHBoxLayout()
        self.date_submitted = SmartDateEdit()
        self.txt_date_required = QLineEdit();
        self.txt_date_required.setPlaceholderText("MM/DD/YYYY")
        date_row_1.addWidget(self.date_submitted, 1);
        date_row_1.addWidget(QLabel("Req:"), 0);
        date_row_1.addWidget(self.txt_date_required, 1)

        date_row_2 = QHBoxLayout()
        self.date_received = SmartDateEdit(allow_multiple=True)
        self.date_due = SmartDateEdit()
        date_row_2.addWidget(self.date_received, 1);
        date_row_2.addWidget(QLabel("Due:"), 0);
        date_row_2.addWidget(self.date_due, 1)

        self.txt_product_codes = QLineEdit()
        self.txt_color_desc = QLineEdit()  # Now a regular field, not a big box

        left_col_form.addRow("RS Number:", self.txt_rs_no)
        left_col_form.addRow("Customer:", self.txt_customer)
        left_col_form.addRow("Sales Person:", self.txt_sales_person)
        left_col_form.addRow("Matching Type:", type_lay)
        left_col_form.addRow("Date Sub/Req:", date_row_1)
        left_col_form.addRow("Date Rec/Due:", date_row_2)
        left_col_form.addRow("Product Code(s):", self.txt_product_codes)
        left_col_form.addRow("Color Description:", self.txt_color_desc)

        # --- RIGHT COLUMN: Technical ---
        right_col_form = QFormLayout()
        right_col_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        right_col_form.setVerticalSpacing(12)

        self.txt_finished_product = QLineEdit()
        self.txt_resin = QLineEdit()

        # Dosage Field (Float Validator)
        self.txt_dosage = QLineEdit()
        self.txt_dosage.setPlaceholderText("0.000000")
        dosage_val = QDoubleValidator(0.0, 100.0, 6)
        dosage_val.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.txt_dosage.setValidator(dosage_val)

        # Process Selection
        proc_grid = QGridLayout()
        self.chk_inj = QCheckBox("Injection");
        self.chk_blow = QCheckBox("Blow-Molding")
        self.chk_film = QCheckBox("Film");
        self.chk_pipe = QCheckBox("Pipe Extrusion")
        self.chk_proc_others = QCheckBox("Others:")
        self.txt_proc_others = QLineEdit();
        self.txt_proc_others.setPlaceholderText("Specify...")
        proc_grid.addWidget(self.chk_inj, 0, 0);
        proc_grid.addWidget(self.chk_blow, 0, 1)
        proc_grid.addWidget(self.chk_film, 1, 0);
        proc_grid.addWidget(self.chk_pipe, 1, 1)
        proc_grid.addWidget(self.chk_proc_others, 2, 0);
        proc_grid.addWidget(self.txt_proc_others, 2, 1)

        # Colorant Type
        colorant_lay = QHBoxLayout()
        self.rad_mb = QRadioButton("MB");
        self.rad_dc = QRadioButton("DC");
        self.rad_col_others = QRadioButton("Others:")
        self.colorant_bg = QButtonGroup(self)
        for r in [self.rad_mb, self.rad_dc, self.rad_col_others]: self.colorant_bg.addButton(r); colorant_lay.addWidget(
            r)
        self.txt_col_others = QLineEdit()
        colorant_lay.addWidget(self.txt_col_others)

        # Color Requirement Grid
        color_req_lay = QGridLayout()
        self.color_bg = QButtonGroup(self)
        reqs = ["Transparent", "Opaque", "Translucent", "Metallic", "Fluorescent", "Pearlescent"]
        for i, name in enumerate(reqs):
            rad = QRadioButton(name)
            self.color_bg.addButton(rad)
            color_req_lay.addWidget(rad, i // 3, i % 3)

        right_col_form.addRow("Finished Product:", self.txt_finished_product)
        right_col_form.addRow("Resin:", self.txt_resin)
        right_col_form.addRow("Dosage (%):", self.txt_dosage)
        right_col_form.addRow("Process:", proc_grid)
        right_col_form.addRow("Colorant Type:", colorant_lay)
        right_col_form.addRow("Color Req:", color_req_lay)

        columns_layout.addLayout(left_col_form, 1)
        columns_layout.addLayout(right_col_form, 1)

        self.container_layout.addWidget(form_card)
        self.container_layout.addStretch()

        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # =========================================================================
        # BUTTON BAR
        # =========================================================================
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 10)

        self.btn_upload = QPushButton(" Upload", objectName="PrimaryButton")
        self.btn_upload.setIcon(fa.icon('mdi6.text-box-remove', color='white'))
        self.btn_print = QPushButton(" Print", objectName="SecondaryButton")
        self.btn_print.setIcon(fa.icon('fa5s.print', color='white'))
        self.btn_new = QPushButton(" New", objectName="InfoButton")
        self.btn_new.setIcon(fa.icon('fa5s.file', color='white'))
        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))

        for btn in [self.btn_upload, self.btn_print, self.btn_new, self.btn_save]:
            btn.setMinimumHeight(42)
            btn.setFixedWidth(130)

        button_layout.addWidget(self.btn_upload);
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print);
        button_layout.addWidget(self.btn_new);
        button_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(button_layout)

    def load_rs_data(self, rs_no):
        self.txt_rs_no.setText(rs_no)