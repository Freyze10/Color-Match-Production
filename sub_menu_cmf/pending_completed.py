import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QGroupBox, QFormLayout, QFrame,
                             QScrollArea, QDateEdit, QComboBox)
from PyQt6.QtCore import Qt, QDate
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

        # --- LEFT COLUMN ---
        left_col = QFormLayout()
        left_col.setVerticalSpacing(15)
        self.txt_cmf_no = QLineEdit()
        self.txt_cmf_no.setReadOnly(True)
        self.txt_customer = QLineEdit()
        self.date_made = SmartDateEdit()
        self.date_received = SmartDateEdit(allow_multiple=True)
        self.date_required = QLineEdit()
        self.date_required.setPlaceholderText("MM/DD/YYYY")
        self.date_due = SmartDateEdit()
        self.txt_finished_prod = QLineEdit()
        self.txt_color_desc = QLineEdit()

        left_col.addRow("Matching No:", self.txt_cmf_no)
        left_col.addRow("Customer:", self.txt_customer)
        left_col.addRow("Form Made Date:", self.date_made)
        left_col.addRow("Received by Lab:", self.date_received)
        left_col.addRow("Date Required:", self.date_required)
        left_col.addRow("Due Date:", self.date_due)
        left_col.addRow("Finished Product:", self.txt_finished_prod)
        left_col.addRow("Color Description:", self.txt_color_desc)

        # --- RIGHT COLUMN ---
        right_col = QFormLayout()
        right_col.setVerticalSpacing(15)

        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Pending", "Completed"])

        self.txt_match_type = QLineEdit()
        self.txt_salesperson = QLineEdit()
        self.txt_reason = QLineEdit()
        self.txt_prod_code = QLineEdit()
        self.txt_prod_code_desc = QLineEdit()  # NEW FIELD
        self.date_submitted = SmartDateEdit()
        self.txt_ar_no = QLineEdit()
        self.date_ar = SmartDateEdit()

        right_col.addRow("Current Status:", self.cmb_status)
        right_col.addRow("Matching Type:", self.txt_match_type)
        right_col.addRow("Sales Person:", self.txt_salesperson)
        right_col.addRow("Pending Reason:", self.txt_reason)
        right_col.addRow("Product Code:", self.txt_prod_code)
        right_col.addRow("Code Description:", self.txt_prod_code_desc)  # Added here
        right_col.addRow("Date Submitted:", self.date_submitted)
        right_col.addRow("AR Number:", self.txt_ar_no)
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
        """Method to trigger database fetch and fill the form"""
        self.txt_cmf_no.setText(cmf_no)
        # Here you would perform your DB query to fill all the QLineEdits and QDateEdits