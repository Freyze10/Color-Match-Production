import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFormLayout, QFrame, QAbstractItemView, QScrollArea)
from PyQt6.QtCore import Qt
from css.styles import AppStyles


class DCFormula(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- TOP HEADER ---
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        header_label = QLabel("FORMULATION FORM (DC)")
        header_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_layout.addWidget(header_label)

        title_layout.addStretch()
        title_layout.addWidget(QLabel("<b>FM00006D</b>"))
        self.main_layout.addWidget(title_frame)

        # =========================================================================
        # MAIN BODY: LEFT (SCROLLABLE FIELDS) | RIGHT (TABLE)
        # =========================================================================
        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        # --- LEFT PANEL: FIELDS ---
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll.setFixedWidth(400)

        left_container = QWidget()
        left_cont_layout = QVBoxLayout(left_container)
        left_cont_layout.setContentsMargins(0, 0, 0, 0)

        field_card = QFrame(objectName="FormCard")
        field_card_layout = QVBoxLayout(field_card)
        field_card_layout.setSpacing(10)

        # Group 1: General Details (Mapped from Image)
        gen_group = QGroupBox("Formulation Details")
        gen_form = QFormLayout(gen_group)
        gen_form.setContentsMargins(10, 25, 10, 10)
        gen_form.setVerticalSpacing(10)

        self.txt_code = QLineEdit()
        self.txt_cmf_no = QLineEdit()
        self.txt_customer = QLineEdit()
        self.txt_resin = QLineEdit()
        self.txt_color = QLineEdit()
        self.txt_date_matched = QLineEdit()
        self.txt_dosage = QLineEdit()
        self.txt_sample_size = QLineEdit()
        self.txt_product_used = QLineEdit()
        self.txt_mixing_time = QLineEdit()
        self.txt_application = QLineEdit()

        gen_form.addRow("Code:", self.txt_code)
        gen_form.addRow("CMF #:", self.txt_cmf_no)
        gen_form.addRow("Customer:", self.txt_customer)
        gen_form.addRow("Resin:", self.txt_resin)
        gen_form.addRow("Color:", self.txt_color)
        gen_form.addRow("Date Matched:", self.txt_date_matched)
        gen_form.addRow("Dosage:", self.txt_dosage)
        gen_form.addRow("Sample Size:", self.txt_sample_size)
        gen_form.addRow("Product Used:", self.txt_product_used)
        gen_form.addRow("Mixing Time:", self.txt_mixing_time)
        gen_form.addRow("Application:", self.txt_application)

        # Group 2: Personnel
        person_group = QGroupBox("Personnel")
        p_form = QFormLayout(person_group)
        p_form.setContentsMargins(10, 25, 10, 10)
        p_form.setVerticalSpacing(10)

        self.txt_matched_by = QLineEdit()
        self.txt_weighed_by = QLineEdit()
        self.txt_encoded_by = QLineEdit()

        p_form.addRow("Matched by:", self.txt_matched_by)
        p_form.addRow("Weighed by:", self.txt_weighed_by)
        p_form.addRow("Encoded by:", self.txt_encoded_by)

        field_card_layout.addWidget(gen_group)
        field_card_layout.addWidget(person_group)

        left_cont_layout.addWidget(field_card)
        left_scroll.setWidget(left_container)

        # --- RIGHT PANEL: TABLE ---
        right_card = QFrame(objectName="FormCard")
        right_card_layout = QVBoxLayout(right_card)

        lbl_table = QLabel("<b>FORMULA COMPOSITION</b>")
        lbl_table.setStyleSheet("font-size: 14px; margin-bottom: 5px;")
        right_card_layout.addWidget(lbl_table)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(16)
        self.table.setHorizontalHeaderLabels(["Material", "Final %", "Total Weight"])

        # Table Configuration
        header = self.table.horizontalHeader()
        header.setMinimumHeight(50)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Rows stretch to fill height
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setShowGrid(True)

        right_card_layout.addWidget(self.table)

        # Total Weight Section
        total_layout = QHBoxLayout()
        self.txt_total_weight = QLineEdit(objectName="TotalWeightField")
        self.txt_total_weight.setPlaceholderText("0.00")
        self.txt_total_weight.setFixedWidth(200)
        self.txt_total_weight.setAlignment(Qt.AlignmentFlag.AlignRight)

        total_layout.addStretch()
        total_layout.addWidget(QLabel("<b>TOTAL WEIGHT:</b>"))
        total_layout.addWidget(self.txt_total_weight)
        right_card_layout.addLayout(total_layout)

        # Assemble Main Layout
        body_layout.addWidget(left_scroll)
        body_layout.addWidget(right_card, 1)  # Right side expands
        self.main_layout.addLayout(body_layout)

        # =========================================================================
        # BUTTON BAR
        # =========================================================================
        button_layout = QHBoxLayout()

        # self.btn_cancel = QPushButton(" Cancel", objectName="DangerButton")
        # self.btn_cancel.setIcon(fa.icon('mdi6.text-box-remove', color='white'))

        self.btn_print = QPushButton(" Print", objectName="SecondaryButton")
        self.btn_print.setIcon(fa.icon('fa5s.print', color='white'))

        self.btn_new = QPushButton(" New", objectName="InfoButton")
        self.btn_new.setIcon(fa.icon('fa5s.file', color='white'))

        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))

        for btn in [ self.btn_print, self.btn_new, self.btn_save]:
            btn.setMinimumHeight(40)

        # button_layout.addWidget(self.btn_cancel)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(button_layout)