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

        # Local Stylesheet for a modern "Card" look
        self.setStyleSheet("""
            QWidget { font-size: 14px; }
            /* Main containers (Cards) - White background to contrast with main window */
            #FormCard { 
                background-color: #ffffff; 
                border: 1px solid #e2e8f0; 
                border-radius: 8px; 
            }
            /* GroupBoxes - Subtle styling for labels */
            QGroupBox { 
                font-weight: bold; 
                color: #1e293b; 
                margin-top: 15px;
                border: 1px solid #f1f5f9;
                border-radius: 5px;
                padding-top: 10px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }

            /* Input styling */
            QLineEdit { 
                min-height: 32px; 
                border: 1px solid #cbd5e1; 
                border-radius: 4px; 
                padding-left: 8px; 
                background-color: #fcfcfc;
            }
            QLineEdit:focus { border: 1px solid #3b82f6; background-color: #ffffff; }

            /* Table styling */
            QTableWidget { 
                background-color: #ffffff;
                gridline-color: #e2e8f0; /* The grid color */
                border: 1px solid #cbd5e1;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 5px;
                border: 1px solid #e2e8f0;
                font-weight: bold;
            }
        """)

        self.init_ui()

    def init_ui(self):
        # 1. Main Vertical Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(15)

        # --- TITLE HEADER ---
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)

        header_label = QLabel("EXTRUDER COLOR MATCHING FORM (MB)")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;")
        title_layout.addWidget(header_label)

        title_layout.addStretch()
        form_code = QLabel("<b>FM00006D</b>")
        form_code.setStyleSheet("color: #64748b;")
        title_layout.addWidget(form_code)

        self.main_layout.addWidget(title_frame)

        # =========================================================================
        # BODY SECTION
        # =========================================================================
        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        # --- LEFT SIDE: FIELDS CARD ---
        left_card = QFrame(objectName="FormCard")
        left_card_layout = QVBoxLayout(left_card)
        left_card_layout.setContentsMargins(15, 10, 15, 15)

        # Group 1: General Info
        gen_group = QGroupBox("General Information")
        gen_form = QFormLayout(gen_group)
        self.txt_date = QLineEdit()
        self.txt_cm_form_no = QLineEdit()
        gen_form.addRow("Date:", self.txt_date)
        gen_form.addRow("CM Form #:", self.txt_cm_form_no)

        # Group 2: Formulation Details (New Group)
        form_group = QGroupBox("Formulation Details")
        form_details = QFormLayout(form_group)
        self.txt_prod_code = QLineEdit()
        self.txt_resin_used = QLineEdit()
        self.txt_customer = QLineEdit()
        self.txt_dosage = QLineEdit()
        self.txt_lot_no = QLineEdit()
        self.txt_mixing_time = QLineEdit()
        self.txt_color = QLineEdit()
        self.txt_application = QLineEdit()

        form_details.addRow("Product Code:", self.txt_prod_code)
        form_details.addRow("Resin Used:", self.txt_resin_used)
        form_details.addRow("Customer:", self.txt_customer)
        form_details.addRow("Dosage:", self.txt_dosage)
        form_details.addRow("Lot Number:", self.txt_lot_no)
        form_details.addRow("Mixing Time:", self.txt_mixing_time)
        form_details.addRow("Color:", self.txt_color)
        form_details.addRow("Application:", self.txt_application)

        # Group 3: Personnel
        person_group = QGroupBox("Personnel Responsibility")
        person_form = QFormLayout(person_group)
        self.txt_matched_by = QLineEdit()
        self.txt_weighed_by = QLineEdit()
        self.txt_encoded_by = QLineEdit()
        person_form.addRow("Matched by:", self.txt_matched_by)
        person_form.addRow("Weighed by:", self.txt_weighed_by)
        person_form.addRow("Encoded by:", self.txt_encoded_by)

        left_card_layout.addWidget(gen_group)
        left_card_layout.addWidget(form_group)
        left_card_layout.addWidget(person_group)
        left_card_layout.addStretch()

        # --- RIGHT SIDE: TABLE CARD ---
        right_card = QFrame(objectName="FormCard")
        right_card_layout = QVBoxLayout(right_card)
        right_card_layout.setContentsMargins(15, 15, 15, 15)

        right_card_layout.addWidget(QLabel("<b>FORMULA COMPOSITION</b>"))

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(12)  # Increased rows slightly
        self.table.setHorizontalHeaderLabels(["Material", "Final %", "Total Weight"])

        # Table Configuration
        self.table.setShowGrid(True)  # ENABLE GRID
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(38)  # Row height

        right_card_layout.addWidget(self.table)

        # Total Weight Section
        total_layout = QHBoxLayout()
        self.txt_total_weight = QLineEdit()
        self.txt_total_weight.setPlaceholderText("0.00")
        self.txt_total_weight.setFixedWidth(180)
        self.txt_total_weight.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txt_total_weight.setStyleSheet(
            "font-weight: bold; font-size: 16px; color: #1e293b; background-color: #f8fafc;")

        total_layout.addStretch()
        total_layout.addWidget(QLabel("<b>TOTAL WEIGHT:</b>"))
        total_layout.addWidget(self.txt_total_weight)
        right_card_layout.addLayout(total_layout)

        # Assemble body parts
        body_layout.addWidget(left_card, 2)
        body_layout.addWidget(right_card, 3)
        self.main_layout.addLayout(body_layout)

        # =========================================================================
        # ACTION BUTTONS
        # =========================================================================
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)

        self.btn_cancel = QPushButton(" Cancel", objectName="DangerButton")
        self.btn_cancel.setIcon(fa.icon('mdi6.text-box-remove', color='white'))
        self.btn_cancel.setMinimumSize(120, 42)

        self.btn_print = QPushButton(" Print", objectName="SecondaryButton")
        self.btn_print.setIcon(fa.icon('fa5s.print', color='white'))
        self.btn_print.setMinimumSize(120, 42)

        self.btn_new = QPushButton(" New", objectName="InfoButton")
        self.btn_new.setIcon(fa.icon('fa5s.file', color='white'))
        self.btn_new.setMinimumSize(120, 42)

        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))
        self.btn_save.setMinimumSize(120, 42)

        button_layout.addWidget(self.btn_cancel)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(button_layout)