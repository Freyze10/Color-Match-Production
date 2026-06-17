import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QGroupBox, QFormLayout, QFrame,
                             QScrollArea, QComboBox, QTextEdit)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from util.field_format import SmartDateEdit


class FeedbackEntry(QWidget):
    def __init__(self, mac_department, user_department):
        super().__init__()
        self.mac_department = mac_department
        self.user_department = user_department
        self.setStyleSheet(AppStyles.MAIN_WINDOW_STYLESHEET)
        self.init_ui()

    def init_ui(self):
        # 1. Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        # Title
        header = QLabel("CMF Feedback & Status Management")
        header.setStyleSheet("font-size: 22px; font-weight: bold; color: #0f172a;")
        self.main_layout.addWidget(header)

        # 2. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        cont_layout = QVBoxLayout(container)
        cont_layout.setContentsMargins(0, 0, 10, 0)

        # 3. Form Card
        form_card = QFrame(objectName="FormCard")
        card_main_layout = QVBoxLayout(form_card)
        card_main_layout.setContentsMargins(25, 25, 25, 25)
        card_main_layout.setSpacing(20)

        # --- TWO COLUMN SPLIT ---
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(40)

        # ==========================================
        # LEFT COLUMN: Tracking & Timelines
        # ==========================================
        left_col = QFormLayout()
        left_col.setVerticalSpacing(15)

        self.txt_cmf_no = QLineEdit()
        self.txt_cmf_no.setReadOnly(True)

        # Overall Status (from Pending/Completed)
        self.cmb_overall_status = QComboBox()
        self.cmb_overall_status.addItems(["Pending", "Completed"])

        self.txt_customer = QLineEdit()

        # ─── DATE ROW 1: Date Created & Required ───
        date_row_1 = QHBoxLayout()
        self.date_submitted_left = SmartDateEdit()
        self.txt_date_required = QLineEdit()
        self.txt_date_required.setPlaceholderText("MM/DD/YYYY")
        date_row_1.addWidget(self.date_submitted_left, 1)
        date_row_1.addWidget(QLabel("<b>Required:</b>"), 0)
        date_row_1.addWidget(self.txt_date_required, 1)

        # ─── DATE ROW 2: Date Received & Due ───
        date_row_2 = QHBoxLayout()
        self.date_received = SmartDateEdit(allow_multiple=True)
        self.date_due = SmartDateEdit()
        date_row_2.addWidget(self.date_received, 1)
        date_row_2.addWidget(QLabel("<b>Due Date:</b>"), 0)
        date_row_2.addWidget(self.date_due, 1)

        self.txt_finished_prod = QLineEdit()
        self.txt_color_desc = QLineEdit()
        self.txt_match_type = QLineEdit()
        self.txt_salesperson = QLineEdit()

        left_col.addRow("Matching No:", self.txt_cmf_no)
        left_col.addRow("Current Status:", self.cmb_overall_status)
        left_col.addRow("Customer:", self.txt_customer)
        left_col.addRow("Date Created:", date_row_1)
        left_col.addRow("Date Received:", date_row_2)
        left_col.addRow("Finished Product:", self.txt_finished_prod)
        left_col.addRow("Color Description:", self.txt_color_desc)
        left_col.addRow("Matching Type:", self.txt_match_type)
        left_col.addRow("Sales Person:", self.txt_salesperson)

        # ==========================================
        # RIGHT COLUMN: Feedback & Results
        # ==========================================
        right_col = QFormLayout()
        right_col.setVerticalSpacing(15)

        # Feedback Status (Passed/Failed)
        self.cmb_feedback_status = QComboBox()
        self.cmb_feedback_status.addItems(["Passed", "Failed"])

        self.txt_feedback_comments = QLineEdit()
        self.txt_feedback_comments.setPlaceholderText("Enter feedback details...")

        self.txt_reason = QLineEdit()
        self.txt_prod_code = QLineEdit()
        self.txt_prod_code_desc = QLineEdit()

        # ─── SAMPLE ROW: Set/Pc & Qty ───
        sample_row = QHBoxLayout()
        self.txt_set_pc = QLineEdit()
        self.txt_set_pc.setPlaceholderText("Qty")
        self.txt_set_pc.setValidator(QIntValidator(0, 999999))
        self.txt_qty_given = QLineEdit()
        self.txt_qty_given.setPlaceholderText("KG")
        qty_validator = QDoubleValidator(0.0, 999999.999, 3)
        qty_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.txt_qty_given.setValidator(qty_validator)

        sample_row.addWidget(self.txt_set_pc, 1)
        sample_row.addWidget(QLabel("<b>KG:</b>"), 0)
        sample_row.addWidget(self.txt_qty_given, 1)

        self.date_submitted_right = SmartDateEdit()
        self.txt_lot_no = QLineEdit()
        self.txt_ar_no = QLineEdit()
        self.date_ar = SmartDateEdit()

        right_col.addRow("Feedback Status:", self.cmb_feedback_status)
        right_col.addRow("Feedback Comments:", self.txt_feedback_comments)
        right_col.addRow("Pending Reason:", self.txt_reason)
        right_col.addRow("Product Code:", self.txt_prod_code)
        right_col.addRow("Code Description:", self.txt_prod_code_desc)
        right_col.addRow("Set-Pc / Qty:", sample_row)
        right_col.addRow("Date Submitted:", self.date_submitted_right)
        right_col.addRow("Lot No.:", self.txt_lot_no)
        right_col.addRow("AR No.:", self.txt_ar_no)
        right_col.addRow("AR Date:", self.date_ar)

        columns_layout.addLayout(left_col, 1)
        columns_layout.addLayout(right_col, 1)

        # --- STORAGE DETAILS SECTION ---
        storage_layout = QVBoxLayout()
        storage_layout.setSpacing(10)
        storage_layout.addWidget(QLabel("<b>Storage Details (Box / Plastic / Tracking):</b>"))
        self.txt_storage_details = QTextEdit()
        self.txt_storage_details.setPlaceholderText("Enter tracking info, bin locations, or inventory notes...")
        self.txt_storage_details.setMinimumHeight(180)
        storage_layout.addWidget(self.txt_storage_details)

        # Assemble Form Card
        card_main_layout.addLayout(columns_layout)
        card_main_layout.addLayout(storage_layout)

        cont_layout.addWidget(form_card)
        cont_layout.addStretch()
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
        self.btn_save = QPushButton(" Save Feedback", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))

        for btn in [self.btn_upload, self.btn_print, self.btn_new, self.btn_save]:
            btn.setFixedSize(145, 45)

        button_layout.addWidget(self.btn_upload)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(button_layout)

    def load_cmf_data(self, cmf_no):
        """Method to trigger database fetch and fill the form"""
        self.txt_cmf_no.setText(cmf_no)
        # Add your database select logic here