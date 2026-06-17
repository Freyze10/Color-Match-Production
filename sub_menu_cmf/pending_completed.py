import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QGroupBox, QFormLayout, QFrame,
                             QScrollArea, QComboBox)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from util.field_format import SmartDateEdit


class PendingCompleted(QWidget):
    def __init__(self, mac_department, user_department):
        super().__init__()
        self.mac_department = mac_department
        self.user_department = user_department
        self.setStyleSheet(AppStyles.MAIN_WINDOW_STYLESHEET)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        # Title
        header = QLabel("Update CMF Status & Tracking")
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
        grid_layout.setSpacing(40)

        # ==========================================
        # LEFT COLUMN: Timelines & Specs
        # ==========================================
        left_col = QFormLayout()
        left_col.setVerticalSpacing(15)

        self.txt_cmf_no = QLineEdit();
        self.txt_cmf_no.setReadOnly(True)
        self.txt_customer = QLineEdit()

        # ─── DATE ROW 1: Date Submitted & Required ───
        date_row_1 = QHBoxLayout()
        date_row_1.setSpacing(10)
        self.date_submitted_left = SmartDateEdit()  # Renamed from Form Made
        self.txt_date_required = QLineEdit()
        self.txt_date_required.setPlaceholderText("MM/DD/YYYY")
        date_row_1.addWidget(self.date_submitted_left, 1)
        date_row_1.addWidget(QLabel("Required:"), 0)
        date_row_1.addWidget(self.txt_date_required, 1)

        # ─── DATE ROW 2: Date Received & Due ───
        date_row_2 = QHBoxLayout()
        date_row_2.setSpacing(10)
        self.date_received = SmartDateEdit(allow_multiple=True)
        self.date_due = SmartDateEdit()
        date_row_2.addWidget(self.date_received, 1)
        date_row_2.addWidget(QLabel("Due Date:"), 0)
        date_row_2.addWidget(self.date_due, 1)

        self.txt_finished_prod = QLineEdit()
        self.txt_color_desc = QLineEdit()
        self.txt_match_type = QLineEdit()
        self.txt_salesperson = QLineEdit()

        left_col.addRow("Matching No:", self.txt_cmf_no)
        left_col.addRow("Customer:", self.txt_customer)
        left_col.addRow("Date Created:", date_row_1)
        left_col.addRow("Date Received:", date_row_2)
        left_col.addRow("Finished Product:", self.txt_finished_prod)
        left_col.addRow("Color Description:", self.txt_color_desc)
        left_col.addRow("Matching Type:", self.txt_match_type)
        left_col.addRow("Sales Person:", self.txt_salesperson)

        # ==========================================
        # RIGHT COLUMN: Results & Submission
        # ==========================================
        right_col = QFormLayout()
        right_col.setVerticalSpacing(15)

        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Pending", "Completed"])

        self.txt_reason = QLineEdit()
        self.txt_prod_code = QLineEdit()
        self.txt_prod_code_desc = QLineEdit()

        # ─── SAMPLE ROW: Set/Pc & Qty ───
        sample_row = QHBoxLayout()
        sample_row.setSpacing(10)
        self.txt_set_pc = QLineEdit()
        self.txt_set_pc.setPlaceholderText("Qty")
        self.txt_set_pc.setValidator(QIntValidator(0, 999999))
        self.txt_qty_given = QLineEdit()
        self.txt_qty_given.setPlaceholderText("KG")
        qty_validator = QDoubleValidator(0.0, 999999.999, 3)
        qty_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.txt_qty_given.setValidator(qty_validator)

        sample_row.addWidget(self.txt_set_pc, 1)
        sample_row.addWidget(QLabel("Quantity Given (KG):"), 0)
        sample_row.addWidget(self.txt_qty_given, 1)

        self.date_submitted_right = SmartDateEdit()  # Date sample was submitted
        self.txt_lot_no = QLineEdit()
        self.txt_ar_no = QLineEdit()
        self.date_ar = SmartDateEdit()

        right_col.addRow("Current Status:", self.cmb_status)
        right_col.addRow("Pending Reason:", self.txt_reason)
        right_col.addRow("Product Code:", self.txt_prod_code)
        right_col.addRow("Code Description:", self.txt_prod_code_desc)
        right_col.addRow("Set-Pc:", sample_row)
        right_col.addRow("Date Submitted:", self.date_submitted_right)
        right_col.addRow("Lot No.:", self.txt_lot_no)
        right_col.addRow("AR No.:", self.txt_ar_no)
        right_col.addRow("AR Date:", self.date_ar)

        grid_layout.addLayout(left_col, 1)
        grid_layout.addLayout(right_col, 1)

        cont_layout.addWidget(form_card)
        cont_layout.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # Footer Buttons
        footer = QHBoxLayout()
        self.btn_save = QPushButton(" Update Record")
        self.btn_save.setObjectName("SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))
        self.btn_save.setFixedSize(180, 45)
        footer.addStretch()
        footer.addWidget(self.btn_save)
        self.main_layout.addLayout(footer)

    def load_cmf_data(self, cmf_no):
        self.txt_cmf_no.setText(cmf_no)