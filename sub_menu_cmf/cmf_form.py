import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QDateEdit, QRadioButton, QCheckBox, QPushButton,
                             QScrollArea, QFrame, QGroupBox, QFormLayout, QTextEdit,
                             QButtonGroup, QGridLayout)
from PyQt6.QtCore import Qt, QDate
from css.styles import AppStyles


class CMFForm(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        self.init_ui()

    def init_ui(self):
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # Scroll area for safety, though 2-column should fit most screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        # The split: Left Column and Right Column
        self.columns_layout = QHBoxLayout(container)
        self.columns_layout.setSpacing(20)
        self.columns_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ==========================================
        # LEFT COLUMN: General & Color Specs
        # ==========================================
        left_col = QVBoxLayout()

        # Section: Basic Info
        gen_group = QGroupBox("General Information")
        gen_form = QFormLayout(gen_group)
        gen_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.txt_cm_no = QLineEdit()
        self.txt_customer = QLineEdit()
        self.date_submitted = QDateEdit(calendarPopup=True, date=QDate.currentDate())
        self.date_required = QDateEdit(calendarPopup=True, date=QDate.currentDate().addDays(7))

        type_lay = QHBoxLayout()
        self.rad_new = QRadioButton("New Matching")
        self.rad_rematch = QRadioButton("Re-Match")
        self.rad_new.setChecked(True)
        type_lay.addWidget(self.rad_new)
        type_lay.addWidget(self.rad_rematch)

        self.txt_sales_person = QLineEdit()
        self.txt_finished_product = QLineEdit()
        self.txt_color_desc = QLineEdit()

        gen_form.addRow("Color Matching No:", self.txt_cm_no)
        gen_form.addRow("Customer:", self.txt_customer)
        gen_form.addRow("Date Submitted:", self.date_submitted)
        gen_form.addRow("Date Required:", self.date_required)
        gen_form.addRow("Matching Type:", type_lay)
        gen_form.addRow("Sales Person:", self.txt_sales_person)
        gen_form.addRow("Finished Product:", self.txt_finished_product)
        gen_form.addRow("Color Description:", self.txt_color_desc)

        # Section: Color Requirement (Radio Buttons as requested)
        color_group = QGroupBox("Color Requirement")
        color_grid = QGridLayout(color_group)
        self.color_bg = QButtonGroup(self)

        requirements = ["Transparent", "Opaque", "Translucent", "Metallic", "Fluorescent", "Pearlescent"]
        for i, name in enumerate(requirements):
            rad = QRadioButton(name)
            self.color_bg.addButton(rad)
            color_grid.addWidget(rad, i // 2, i % 2)  # 2 columns inside the groupbox

        self.rad_col_others = QRadioButton("Others:")
        self.color_bg.addButton(self.rad_col_others)
        self.txt_col_req_others = QLineEdit()
        color_grid.addWidget(self.rad_col_others, 3, 0)
        color_grid.addWidget(self.txt_col_req_others, 3, 1)

        left_col.addWidget(gen_group)
        left_col.addWidget(color_group)
        left_col.addStretch()

        # ==========================================
        # RIGHT COLUMN: Process & Technical
        # ==========================================
        right_col = QVBoxLayout()

        tech_group = QGroupBox("Process & Technical Specifications")
        tech_form = QFormLayout(tech_group)

        self.txt_resin = QLineEdit()

        # Process Selection
        proc_grid = QGridLayout()
        self.chk_inj = QCheckBox("Injection")
        self.chk_blow = QCheckBox("Blow-Molding")
        self.chk_film = QCheckBox("Film")
        self.chk_pipe = QCheckBox("Pipe Extrusion")
        proc_grid.addWidget(self.chk_inj, 0, 0);
        proc_grid.addWidget(self.chk_blow, 0, 1)
        proc_grid.addWidget(self.chk_film, 1, 0);
        proc_grid.addWidget(self.chk_pipe, 1, 1)

        self.txt_qty_resin = QLineEdit()

        # Yes/No Helper
        def yes_no_layout():
            lay = QHBoxLayout()
            bg = QButtonGroup(self)
            y, n = QRadioButton("Yes"), QRadioButton("No")
            bg.addButton(y);
            bg.addButton(n)
            lay.addWidget(y);
            lay.addWidget(n);
            lay.addStretch()
            return lay, y, n

        res_lay, self.res_y, self.res_n = yes_no_layout()
        samp_lay, self.samp_y, self.samp_n = yes_no_layout()
        guide_lay, self.guide_y, self.guide_n = yes_no_layout()
        low_lay, self.low_y, self.low_n = yes_no_layout()

        self.txt_mi = QLineEdit()
        self.txt_dosage = QLineEdit()
        self.txt_temp = QLineEdit()

        tech_form.addRow("Resin:", self.txt_resin)
        tech_form.addRow("Process:", proc_grid)
        tech_form.addRow("Qty Resin for Testing:", self.txt_qty_resin)
        tech_form.addRow("Customer Provided Resin:", res_lay)
        tech_form.addRow("MI Customer's Resin:", self.txt_mi)
        tech_form.addRow("Sample Colorant Avail:", samp_lay)
        tech_form.addRow("Dosage:", self.txt_dosage)
        tech_form.addRow("Return Color Guide:", guide_lay)
        tech_form.addRow("Processing Temp:", self.txt_temp)
        tech_form.addRow("Low Cost Requirement:", low_lay)

        right_col.addWidget(tech_group)
        right_col.addStretch()

        # Add columns to main split
        self.columns_layout.addLayout(left_col, 1)
        self.columns_layout.addLayout(right_col, 1)

        # ==========================================
        # BOTTOM: Remarks & Additional Information
        # ==========================================
        bottom_info_layout = QVBoxLayout()

        self.txt_remarks = QTextEdit()
        self.txt_remarks.setPlaceholderText("Enter remarks here...")
        self.txt_remarks.setMaximumHeight(60)

        self.txt_additional_info = QTextEdit()
        self.txt_additional_info.setPlaceholderText("Enter any additional information beyond what's stated above...")
        self.txt_additional_info.setMinimumHeight(100)  # Big text box as requested

        bottom_info_layout.addWidget(QLabel("<b>Remarks:</b>"))
        bottom_info_layout.addWidget(self.txt_remarks)
        bottom_info_layout.addWidget(QLabel("<b>Additional Information:</b>"))
        bottom_info_layout.addWidget(self.txt_additional_info)

        # Product Code Footer
        footer_lay = QHBoxLayout()
        self.txt_prod_code = QLineEdit()
        self.txt_prod_code.setFixedWidth(250)
        footer_lay.addStretch()
        footer_lay.addWidget(QLabel("<b>PRODUCT CODE:</b>"))
        footer_lay.addWidget(self.txt_prod_code)

        # Add everything to the scrollable container
        self.form_layout = QVBoxLayout(container)  # Redefining form_layout to hold columns + bottom
        self.form_layout.addLayout(self.columns_layout)
        self.form_layout.addLayout(bottom_info_layout)
        self.form_layout.addLayout(footer_lay)

        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # --- BUTTONS ---
        button_layout = QHBoxLayout()

        self.btn_cancel = QPushButton("Cancel", objectName="DangerButton")
        self.btn_cancel.setIcon(fa.icon('mdi6.text-box-remove', color='white'))
        button_layout.addWidget(self.btn_cancel)

        button_layout.addStretch()

        print_btn = QPushButton("Print", objectName="SecondaryButton")
        print_btn.setIcon(fa.icon('fa5s.print', color='white'))
        button_layout.addWidget(print_btn)

        self.new_btn = QPushButton("New", objectName="InfoButton")
        self.new_btn.setIcon(fa.icon('fa5s.file', color='white'))
        button_layout.addWidget(self.new_btn)

        self.save_btn = QPushButton("Save", objectName="SuccessButton")
        self.save_btn.setIcon(fa.icon('fa5s.save', color='white'))
        button_layout.addWidget(self.save_btn)

        self.main_layout.addLayout(button_layout)