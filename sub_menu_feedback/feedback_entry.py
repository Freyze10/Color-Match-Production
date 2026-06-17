import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QGroupBox, QFormLayout, QFrame,
                             QScrollArea, QComboBox)
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
        header = QLabel("CMF Feedback & Status Tracking")
        header.setStyleSheet("font-size: 22px; font-weight: bold; color: #0f172a;")
        self.main_layout.addWidget(header)

        # 2. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        cont_layout = QVBoxLayout(container)
        cont_layout.setContentsMargins(0, 0, 10, 0)

        # 3. Main Form Card
        form_card = QFrame(objectName="FormCard")
        grid_layout = QHBoxLayout(form_card)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(40)

        # ==========================================
        # LEFT COLUMN: CMF Details + FEEDBACK
        # ==========================================
        left_col = QFormLayout()
        left_col.setVerticalSpacing(15)

        self.txt_cm_no = QLineEdit();
        self.txt_cm_no.setReadOnly(True)
        self.txt_customer = QLineEdit()

        # Date Row 1: Created & Required
        date_row_1 = QHBoxLayout()
        self.date_created = SmartDateEdit()
        self.txt_date_required = QLineEdit();
        self.txt_date_required.setPlaceholderText("MM/DD/YYYY")
        date_row_1.addWidget(self.date_created, 1)
        date_row_1.addWidget(QLabel("Required:"), 0)
        date_row_1.addWidget(self.txt_date_required, 1)

        # Date Row 2: Received & Due
        date_row_2 = QHBoxLayout()
        self.date_received = SmartDateEdit(allow_multiple=True)
        self.date_due = SmartDateEdit()
        date_row_2.addWidget(self.date_received, 1)
        date_row_2.addWidget(QLabel("Due Date:"), 0)
        date_row_2.addWidget(self.date_due, 1)

        self.txt_finished_prod = QLineEdit()
        self.txt_color_desc = QLineEdit()
        self.txt_match_type = QLineEdit()
        self.txt_salesperson = QLineEdit()

        # --- FEEDBACK FIELDS (Moved to Left) ---
        self.cmb_feedback_status = QComboBox()
        self.cmb_feedback_status.addItems(["Pending", "Passed", "Failed"])
        self.txt_feedback_comments = QLineEdit()
        self.txt_feedback_comments.setPlaceholderText("Enter feedback observations...")
        self.txt_storage_details = QLineEdit()
        self.txt_storage_details.setPlaceholderText("Box #, Plastic Bin location...")

        # Add to left layout
        left_col.addRow("Matching No:", self.txt_cm_no)
        left_col.addRow("Customer:", self.txt_customer)
        left_col.addRow("Date Created:", date_row_1)
        left_col.addRow("Date Received:", date_row_2)
        left_col.addRow("Finished Product:", self.txt_finished_prod)
        left_col.addRow("Color Description:", self.txt_color_desc)
        left_col.addRow("Matching Type:", self.txt_match_type)
        left_col.addRow("Sales Person:", self.txt_salesperson)

        # Feedback Separator and Fields
        left_col.addRow(QLabel("<br><b>FEEDBACK & MONITORING</b>"))
        left_col.addRow("Feedback Status:", self.cmb_feedback_status)
        left_col.addRow("Comments:", self.txt_feedback_comments)
        left_col.addRow("Storage Details:", self.txt_storage_details)

        # ==========================================
        # RIGHT COLUMN: Results & Submission
        # ==========================================
        right_col = QFormLayout()
        right_col.setVerticalSpacing(15)

        self.cmb_current_status = QComboBox()
        self.cmb_current_status.addItems(["Pending", "Completed"])
        self.txt_reason = QLineEdit()
        self.txt_prod_code = QLineEdit()
        self.txt_prod_code_desc = QLineEdit()

        # Sample Row: Set/Pc & Qty
        sample_row = QHBoxLayout()
        self.txt_set_pc = QLineEdit();
        self.txt_set_pc.setPlaceholderText("Qty")
        self.txt_set_pc.setValidator(QIntValidator(0, 999999))
        self.txt_qty_given = QLineEdit();
        self.txt_qty_given.setPlaceholderText("KG")
        qty_val = QDoubleValidator(0.0, 999999.999, 3);
        qty_val.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.txt_qty_given.setValidator(qty_val)
        sample_row.addWidget(self.txt_set_pc, 1);
        sample_row.addWidget(QLabel("KG:"), 0);
        sample_row.addWidget(self.txt_qty_given, 1)

        self.date_submitted = SmartDateEdit()
        self.txt_lot_no = QLineEdit()
        self.txt_ar_no = QLineEdit()
        self.date_ar = SmartDateEdit()

        right_col.addRow("Current Status:", self.cmb_current_status)
        right_col.addRow("Pending Reason:", self.txt_reason)
        right_col.addRow("Product Code:", self.txt_prod_code)
        right_col.addRow("Code Description:", self.txt_prod_code_desc)
        right_col.addRow("Set-Pc:", sample_row)
        right_col.addRow("Date Submitted:", self.date_submitted)
        right_col.addRow("Lot No.:", self.txt_lot_no)
        right_col.addRow("AR Number:", self.txt_ar_no)
        right_col.addRow("AR Date:", self.date_ar)

        # Assemble Grid
        grid_layout.addLayout(left_col, 1)
        grid_layout.addLayout(right_col, 1)

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
        self.btn_save = QPushButton(" Save Update", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))

        for btn in [self.btn_upload, self.btn_print, self.btn_new, self.btn_save]:
            btn.setFixedSize(140, 45)

        button_layout.addWidget(self.btn_upload);
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print);
        button_layout.addWidget(self.btn_new);
        button_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(button_layout)

    def load_cmf_data(self, cmf_no):
        self.txt_cm_no.setText(cmf_no)