import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFormLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from css.styles import AppStyles


class MBFormula(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        self.init_ui()

    def init_ui(self):
        # 1. Main Vertical Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Title / Header (Optional based on your image)
        header_label = QLabel("EXTRUDER COLOR MATCHING FORM (MB)")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #334155;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(header_label)

        # =========================================================================
        # MIDDLE SECTION: LEFT (FIELDS) & RIGHT (TABLE)
        # =========================================================================
        body_layout = QHBoxLayout()
        body_layout.setSpacing(30)

        # --- LEFT SIDE: FORM FIELDS ---
        left_panel = QVBoxLayout()

        info_group = QGroupBox("Form Details")
        info_form = QFormLayout(info_group)
        info_form.setSpacing(12)
        info_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Fields from the image
        self.txt_date = QLineEdit()
        self.txt_cm_form_no = QLineEdit()
        self.txt_prod_code = QLineEdit()
        self.txt_resin_used = QLineEdit()
        self.txt_customer = QLineEdit()
        self.txt_dosage = QLineEdit()
        self.txt_lot_no = QLineEdit()
        self.txt_mixing_time = QLineEdit()
        self.txt_color = QLineEdit()
        self.txt_application = QLineEdit()

        info_form.addRow("Date:", self.txt_date)
        info_form.addRow("CM Form #:", self.txt_cm_form_no)
        info_form.addRow("Product Code:", self.txt_prod_code)
        info_form.addRow("Resin Used:", self.txt_resin_used)
        info_form.addRow("Customer:", self.txt_customer)
        info_form.addRow("Dosage:", self.txt_dosage)
        info_form.addRow("Lot Number:", self.txt_lot_no)
        info_form.addRow("Mixing Time:", self.txt_mixing_time)
        info_form.addRow("Color:", self.txt_color)
        info_form.addRow("Application:", self.txt_application)

        # Personnel Group
        person_group = QGroupBox("Personnel")
        person_form = QFormLayout(person_group)
        self.txt_matched_by = QLineEdit()
        self.txt_weighed_by = QLineEdit()
        self.txt_encoded_by = QLineEdit()

        person_form.addRow("Matched by:", self.txt_matched_by)
        person_form.addRow("Weighed by:", self.txt_weighed_by)
        person_form.addRow("Encoded by:", self.txt_encoded_by)

        left_panel.addWidget(info_group)
        left_panel.addWidget(person_group)
        left_panel.addStretch()  # Push everything to the top

        # --- RIGHT SIDE: TABLE ---
        right_panel = QVBoxLayout()

        table_label = QLabel("<b>Formula Composition</b>")
        right_panel.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(10)
        self.table.setHorizontalHeaderLabels(["Material", "Final %", "Total Weight"])

        # Table Styling
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("QTableWidget { border: 1px solid #cbd5e1; gridline-color: #e2e8f0; }")

        right_panel.addWidget(self.table)

        # Total Weight Field at the end of the table
        total_layout = QHBoxLayout()
        self.txt_grand_total = QLineEdit()
        self.txt_grand_total.setPlaceholderText("0.00")
        self.txt_grand_total.setFixedWidth(150)
        self.txt_grand_total.setReadOnly(True)  # Usually calculated
        self.txt_grand_total.setAlignment(Qt.AlignmentFlag.AlignRight)

        total_layout.addStretch()
        total_layout.addWidget(QLabel("<b>GRAND TOTAL:</b>"))
        total_layout.addWidget(self.txt_grand_total)
        right_panel.addLayout(total_layout)

        # Assemble body
        body_layout.addLayout(left_panel, 1)  # 1/3 of screen
        body_layout.addLayout(right_panel, 2)  # 2/3 of screen
        self.main_layout.addLayout(body_layout)

        # =========================================================================
        # BOTTOM: ACTION BUTTONS
        # =========================================================================
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)

        self.btn_cancel = QPushButton(" Cancel", objectName="DangerButton")
        self.btn_cancel.setIcon(fa.icon('mdi6.text-box-remove', color='white'))
        self.btn_cancel.setMinimumSize(120, 40)

        self.btn_print = QPushButton(" Print", objectName="SecondaryButton")
        self.btn_print.setIcon(fa.icon('fa5s.print', color='white'))
        self.btn_print.setMinimumSize(120, 40)

        self.btn_new = QPushButton(" New", objectName="InfoButton")
        self.btn_new.setIcon(fa.icon('fa5s.file', color='white'))
        self.btn_new.setMinimumSize(120, 40)

        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))
        self.btn_save.setMinimumSize(120, 40)

        button_layout.addWidget(self.btn_cancel)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(button_layout)