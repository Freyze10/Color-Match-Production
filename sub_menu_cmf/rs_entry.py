import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QRadioButton, QCheckBox, QPushButton, QScrollArea,
                             QFrame, QGroupBox, QFormLayout, QTextEdit,
                             QButtonGroup, QGridLayout, QComboBox)
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from util.field_format import SmartDateEdit


class RSEntry(QWidget):
    def __init__(self, mac_department, user_department):
        super().__init__()
        self.mac_department = mac_department
        self.user_department = user_department

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
        # TOP PART: TWO COLUMNS
        # =========================================================================
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(25)

        # --- LEFT COLUMN: RS Tracking & Personnel ---
        left_col = QVBoxLayout()

        tracking_group = QGroupBox("RS Tracking Information")
        track_form = QFormLayout(tracking_group)
        track_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        track_form.setSpacing(12)

        self.txt_rs_no = QLineEdit()
        self.txt_rs_no.setPlaceholderText("Enter RS Number...")
        self.txt_customer = QLineEdit()
        self.txt_sales_person = QLineEdit()

        # Matching Type
        type_lay = QHBoxLayout()
        self.rad_new = QRadioButton("New Matching")
        self.rad_rematch = QRadioButton("Re-Match")
        self.rad_new.setChecked(True)
        type_lay.addWidget(self.rad_new)
        type_lay.addWidget(self.rad_rematch)
        type_lay.addStretch()

        # Date Row 1: Submitted & Required
        date_row_1 = QHBoxLayout()
        self.date_submitted = SmartDateEdit()
        self.txt_date_required = QLineEdit()
        self.txt_date_required.setPlaceholderText("MM/DD/YYYY")
        date_row_1.addWidget(self.date_submitted, 1)
        date_row_1.addWidget(QLabel("Required:"), 0)
        date_row_1.addWidget(self.txt_date_required, 1)

        # Date Row 2: Received & Due
        date_row_2 = QHBoxLayout()
        self.txt_date_received = SmartDateEdit(allow_multiple=True)
        self.date_due = SmartDateEdit()
        date_row_2.addWidget(self.txt_date_received, 1)
        date_row_2.addWidget(QLabel("Due Date:"), 0)
        date_row_2.addWidget(self.date_due, 1)

        track_form.addRow("RS Number:", self.txt_rs_no)
        track_form.addRow("Customer:", self.txt_customer)
        track_form.addRow("Sales Person:", self.txt_sales_person)
        track_form.addRow("Matching Type:", type_lay)
        track_form.addRow("Date Sub/Req:", date_row_1)
        track_form.addRow("Date Rec/Due:", date_row_2)

        # Product Codes
        self.txt_product_codes = QLineEdit()
        self.txt_product_codes.setPlaceholderText("Enter related product codes...")
        track_form.addRow("Product Code(s):", self.txt_product_codes)

        left_col.addWidget(tracking_group)
        left_col.addStretch()

        # --- RIGHT COLUMN: Technical Requirements ---
        right_col = QVBoxLayout()

        tech_group = QGroupBox("RS Technical Specifications")
        tech_form = QFormLayout(tech_group)
        tech_form.setSpacing(10)

        self.txt_finished_product = QLineEdit()
        self.txt_resin = QLineEdit()

        # Process Selection
        proc_grid = QGridLayout()
        self.chk_inj = QCheckBox("Injection");
        self.chk_blow = QCheckBox("Blow-Molding")
        self.chk_film = QCheckBox("Film");
        self.chk_pipe = QCheckBox("Pipe Extrusion")
        self.chk_proc_others = QCheckBox("Others:")
        self.txt_proc_others = QLineEdit()
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

        tech_form.addRow("Finished Product:", self.txt_finished_product)
        tech_form.addRow("Resin:", self.txt_resin)
        tech_form.addRow("Process:", proc_grid)
        tech_form.addRow("Colorant Type:", colorant_lay)

        # Color Requirement Grid (2 Rows x 4 Cols)
        color_req_group = QGroupBox("Color Requirement")
        color_grid = QGridLayout(color_req_group)
        self.color_bg = QButtonGroup(self)
        requirements = ["Transparent", "Opaque", "Translucent", "Metallic", "Fluorescent", "Pearlescent"]
        for i, name in enumerate(requirements):
            rad = QRadioButton(name)
            self.color_bg.addButton(rad)
            color_grid.addWidget(rad, i // 3, i % 3)

        self.rad_req_others = QRadioButton("Others:")
        self.txt_req_others = QLineEdit()
        self.color_bg.addButton(self.rad_req_others)
        color_grid.addWidget(self.rad_req_others, 2, 0)
        color_grid.addWidget(self.txt_req_others, 2, 1, 1, 2)

        right_col.addWidget(tech_group)
        right_col.addWidget(color_req_group)
        right_col.addStretch()

        columns_layout.addLayout(left_col, 1)
        columns_layout.addLayout(right_col, 1)

        # =========================================================================
        # BOTTOM PART: COLOR DESCRIPTION
        # =========================================================================
        desc_group = QGroupBox("Color Description")
        desc_layout = QVBoxLayout(desc_group)
        self.txt_color_desc = QTextEdit()
        self.txt_color_desc.setPlaceholderText("Enter detailed color requirements and observations here...")
        self.txt_color_desc.setMinimumHeight(120)
        desc_layout.addWidget(self.txt_color_desc)

        self.container_layout.addLayout(columns_layout)
        self.container_layout.addWidget(desc_group)

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
            btn.setMinimumHeight(40)
            btn.setFixedWidth(120)

        button_layout.addWidget(self.btn_upload);
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print);
        button_layout.addWidget(self.btn_new);
        button_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(button_layout)

    def load_rs_data(self, rs_no):
        """Pre-fill data if linked to an existing RS"""
        self.txt_rs_no.setText(rs_no)