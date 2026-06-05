import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFormLayout, QFrame, QSizePolicy, QAbstractItemView)
from PyQt6.QtCore import Qt
from css.styles import AppStyles


class MBFormula(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        # Increase base font size for this specific widget to make it "Big"
        self.setStyleSheet("""
            QWidget { font-size: 14px; }
            QLineEdit { min-height: 35px; border: 1px solid #cbd5e1; border-radius: 4px; padding-left: 8px; }
            QTableWidget { border: 1px solid #cbd5e1; border-radius: 6px; background-color: white; }
            QGroupBox { font-weight: bold; color: #334155; margin-top: 20px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }
            QLabel { color: #475569; font-weight: 500; }
            #FormCard { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; }
        """)

        self.init_ui()

    def init_ui(self):
        # 1. Main Vertical Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Title Section
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        header_label = QLabel("EXTRUDER COLOR MATCHING FORM (MB)")
        header_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #1e293b;")
        title_layout.addWidget(header_label)
        title_layout.addStretch()
        title_layout.addWidget(QLabel("<b>FM00006D</b>"))
        self.main_layout.addWidget(title_frame)

        # =========================================================================
        # MIDDLE SECTION: LEFT (FIELDS) & RIGHT (TABLE)
        # =========================================================================
        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        # --- LEFT SIDE: FORM FIELDS IN A CONTAINER ---
        left_card = QFrame(objectName="FormCard")
        left_card_layout = QVBoxLayout(left_card)
        left_card_layout.setContentsMargins(20, 20, 20, 20)

        info_form = QFormLayout()
        info_form.setSpacing(15)
        info_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Fields
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

        left_card_layout.addLayout(info_form)

        # Personnel Section
        person_group = QGroupBox("Personnel Responsibility")
        person_form = QFormLayout(person_group)
        self.txt_matched_by = QLineEdit()
        self.txt_weighed_by = QLineEdit()
        self.txt_encoded_by = QLineEdit()

        person_form.addRow("Matched by:", self.txt_matched_by)
        person_form.addRow("Weighed by:", self.txt_weighed_by)
        person_form.addRow("Encoded by:", self.txt_encoded_by)
        left_card_layout.addWidget(person_group)

        # --- RIGHT SIDE: TABLE IN A CONTAINER ---
        right_card = QFrame(objectName="FormCard")
        right_card_layout = QVBoxLayout(right_card)
        right_card_layout.setContentsMargins(15, 15, 15, 15)

        table_header_layout = QHBoxLayout()
        table_header_layout.addWidget(QLabel("<b>FORMULA COMPOSITION</b>"))
        right_card_layout.addLayout(table_header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(10)
        self.table.setHorizontalHeaderLabels(["Material", "Final %", "Total Weight"])

        # Table Configuration
        self.table.verticalHeader().setVisible(False)  # Hide vertical header
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(40)  # Make rows taller

        right_card_layout.addWidget(self.table)

        # Total Weight Section (Editable)
        total_layout = QHBoxLayout()
        self.txt_total_weight = QLineEdit()
        self.txt_total_weight.setPlaceholderText("0.00")
        self.txt_total_weight.setFixedWidth(200)
        self.txt_total_weight.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_total_weight.setStyleSheet("font-weight: bold; font-size: 16px; color: #0f172a;")

        total_layout.addStretch()
        total_layout.addWidget(QLabel("<b>TOTAL WEIGHT:</b>"))
        total_layout.addWidget(self.txt_total_weight)
        right_card_layout.addLayout(total_layout)

        # Assemble body
        body_layout.addWidget(left_card, 2)  # Left card takes slightly less space
        body_layout.addWidget(right_card, 3)  # Table card takes more space
        self.main_layout.addLayout(body_layout)

        # =========================================================================
        # BOTTOM: ACTION BUTTONS
        # =========================================================================
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)

        self.btn_cancel = QPushButton(" Cancel", objectName="DangerButton")
        self.btn_cancel.setIcon(fa.icon('mdi6.text-box-remove', color='white'))
        self.btn_cancel.setMinimumSize(130, 45)

        self.btn_print = QPushButton(" Print", objectName="SecondaryButton")
        self.btn_print.setIcon(fa.icon('fa5s.print', color='white'))
        self.btn_print.setMinimumSize(130, 45)

        self.btn_new = QPushButton(" New", objectName="InfoButton")
        self.btn_new.setIcon(fa.icon('fa5s.file', color='white'))
        self.btn_new.setMinimumSize(130, 45)

        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))
        self.btn_save.setMinimumSize(130, 45)

        button_layout.addWidget(self.btn_cancel)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(button_layout)