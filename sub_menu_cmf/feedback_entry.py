import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QFormLayout, QFrame,
                             QScrollArea, QComboBox, QTextEdit)
from PyQt6.QtCore import Qt
from css.styles import AppStyles


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
        header = QLabel("CMF Feedback & Monitoring")
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
        card_layout = QVBoxLayout(form_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)

        # --- TOP ROW: Two Column Split for Basic Info ---
        top_row_layout = QHBoxLayout()
        top_row_layout.setSpacing(40)

        # LEFT COLUMN
        left_col = QFormLayout()
        left_col.setVerticalSpacing(15)
        self.txt_cm_no = QLineEdit()
        self.txt_cm_no.setReadOnly(True)
        self.cmb_status = QComboBox()
        self.cmb_status.addItems(["Pending", "Passed", "Failed"])

        left_col.addRow("Matching No:", self.txt_cm_no)
        left_col.addRow("Current Status:", self.cmb_status)

        # RIGHT COLUMN
        right_col = QFormLayout()
        right_col.setVerticalSpacing(15)
        self.txt_comments = QLineEdit()
        self.txt_comments.setPlaceholderText("Enter feedback or observations...")

        right_col.addRow("Feedback Comments:", self.txt_comments)

        top_row_layout.addLayout(left_col, 1)
        top_row_layout.addLayout(right_col, 1)

        # --- BOTTOM ROW: STORAGE DETAILS (BIG TEXT BOX) ---
        storage_layout = QVBoxLayout()
        storage_layout.setSpacing(10)

        lbl_storage = QLabel("<b>Storage Details (Box / Plastic / Tracking):</b>")
        self.txt_storage_details = QTextEdit()
        self.txt_storage_details.setPlaceholderText(
            "Provide detailed tracking info (e.g., Box #, Plastic Bin location, inventory notes)...")
        self.txt_storage_details.setMinimumHeight(250)  # Big text box as requested

        storage_layout.addWidget(lbl_storage)
        storage_layout.addWidget(self.txt_storage_details)

        # Assemble Card
        card_layout.addLayout(top_row_layout)
        card_layout.addLayout(storage_layout)

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
        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))

        for btn in [self.btn_upload, self.btn_print, self.btn_new, self.btn_save]:
            btn.setFixedSize(140, 45)

        button_layout.addWidget(self.btn_upload)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(button_layout)

    def load_cmf_data(self, cmf_no):
        """Method to trigger database fetch and fill the form"""
        self.txt_cm_no.setText(cmf_no)