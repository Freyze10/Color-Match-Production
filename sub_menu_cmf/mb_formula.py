import qtawesome as fa
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFormLayout, QFrame, QAbstractItemView, QScrollArea,
                             QStyledItemDelegate, QComboBox, QCompleter)
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from util.field_format import SmartDateEdit
from util.formula_table_delegate import MaterialDelegate, NumericDelegate


class MBFormula(QWidget):
    def __init__(self, mac_department, user_department):
        super().__init__()
        self.mac_department = mac_department
        self.user_department = user_department
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- TOP HEADER ---
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        header_label = QLabel("EXTRUDER COLOR MATCHING FORM")
        header_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_layout.addWidget(header_label)
        title_layout.addStretch()
        title_layout.addWidget(QLabel("<b>FM00006D</b>"))
        self.main_layout.addWidget(title_frame)

        # =========================================================================
        # MAIN BODY
        # =========================================================================
        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        # --- LEFT PANEL: FIELDS ---
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll.setFixedWidth(380)

        left_container = QWidget()
        left_cont_layout = QVBoxLayout(left_container)
        left_cont_layout.setContentsMargins(0, 0, 0, 0)

        field_card = QFrame(objectName="FormCard")
        field_card_layout = QVBoxLayout(field_card)
        field_card_layout.setSpacing(10)

        # Groups
        gen_group = QGroupBox("General Information")
        gen_form = QFormLayout(gen_group)
        gen_form.setContentsMargins(10, 25, 10, 10)
        self.txt_date = SmartDateEdit()
        self.txt_cm_form_no = QLineEdit()
        gen_form.addRow("Date:", self.txt_date)
        gen_form.addRow("CM Form #:", self.txt_cm_form_no)

        form_group = QGroupBox("Formulation Details")
        f_details = QFormLayout(form_group)
        f_details.setContentsMargins(10, 25, 10, 10)
        self.txt_prod_code = QLineEdit()
        self.txt_resin_used = QLineEdit()
        self.txt_customer = QLineEdit()
        self.txt_dosage = QLineEdit()
        self.txt_lot_no = QLineEdit()
        self.txt_mixing_time = QLineEdit()
        self.txt_color = QLineEdit()
        self.txt_application = QLineEdit()
        self.txt_finished_prod = QLineEdit()

        f_details.addRow("Product Code:", self.txt_prod_code)
        f_details.addRow("Resin Used:", self.txt_resin_used)
        f_details.addRow("Customer:", self.txt_customer)
        f_details.addRow("Dosage:", self.txt_dosage)
        f_details.addRow("Lot Number:", self.txt_lot_no)
        f_details.addRow("Mixing Time:", self.txt_mixing_time)
        f_details.addRow("Color:", self.txt_color)
        f_details.addRow("Application:", self.txt_application)
        f_details.addRow("Finished Prod:", self.txt_finished_prod)

        person_group = QGroupBox("Personnel")
        p_form = QFormLayout(person_group)
        p_form.setContentsMargins(10, 25, 10, 10)
        self.txt_matched_by = QLineEdit()
        self.txt_weighed_by = QLineEdit()
        self.txt_encoded_by = QLineEdit()
        p_form.addRow("Matched by:", self.txt_matched_by)
        p_form.addRow("Weighed by:", self.txt_weighed_by)
        p_form.addRow("Encoded by:", self.txt_encoded_by)

        field_card_layout.addWidget(gen_group)
        field_card_layout.addWidget(form_group)
        field_card_layout.addWidget(person_group)

        left_cont_layout.addWidget(field_card)
        left_scroll.setWidget(left_container)

        # --- RIGHT PANEL: TABLE ---
        right_card = QFrame(objectName="FormCard")
        right_card_layout = QVBoxLayout(right_card)
        right_card_layout.addWidget(QLabel("<b>FORMULA COMPOSITION</b>"))

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(16)
        self.table.setHorizontalHeaderLabels(["Material", "Final %", "Total Weight"])

        # --- APPLY DELEGATES ---
        # 1. Autofill Material (Usually you would load this from the database)
        dummy_materials = ["PE Resin", "PP Resin", "Titanium Dioxide", "Carbon Black", "Iron Oxide Red"]
        self.material_delegate = MaterialDelegate(self, dummy_materials)
        self.table.setItemDelegateForColumn(0, self.material_delegate)

        # 2. Numeric Only Columns
        self.numeric_delegate = NumericDelegate()
        self.table.setItemDelegateForColumn(1, self.numeric_delegate)
        self.table.setItemDelegateForColumn(2, self.numeric_delegate)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        right_card_layout.addWidget(self.table)

        # Total Weight Section
        total_layout = QHBoxLayout()
        self.txt_total_weight = QLineEdit(objectName="TotalWeightField")
        self.txt_total_weight.setPlaceholderText("0.00")
        self.txt_total_weight.setFixedWidth(180)
        self.txt_total_weight.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_validator = QDoubleValidator(0.0, 999999999.9999999, 7, self)
        total_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.txt_total_weight.setValidator(total_validator)

        total_layout.addStretch()
        total_layout.addWidget(QLabel("<b>TOTAL WEIGHT:</b>"))
        total_layout.addWidget(self.txt_total_weight)
        right_card_layout.addLayout(total_layout)

        body_layout.addWidget(left_scroll)
        body_layout.addWidget(right_card, 1)
        self.main_layout.addLayout(body_layout)

        # --- BUTTON BAR ---
        button_layout = QHBoxLayout()
        self.btn_print = QPushButton(" Print", objectName="SecondaryButton")
        self.btn_print.setIcon(fa.icon('fa5s.print', color='white'))

        self.btn_new = QPushButton(" New", objectName="InfoButton")
        self.btn_new.setIcon(fa.icon('fa5s.file', color='white'))

        self.btn_save = QPushButton(" Save", objectName="SuccessButton")
        self.btn_save.setIcon(fa.icon('fa5s.save', color='white'))

        for btn in [self.btn_print, self.btn_new, self.btn_save]:
            btn.setMinimumHeight(40)

        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(button_layout)

    def load_formula_by_cmf(self, cmf_no):
        # Set the Header Field
        self.txt_cm_form_no.setText(cmf_no)