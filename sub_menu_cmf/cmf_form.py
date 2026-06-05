import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QDateEdit, QRadioButton, QCheckBox, QPushButton,
                             QScrollArea, QFrame, QGridLayout, QGroupBox,
                             QFormLayout, QTextEdit, QButtonGroup)
from PyQt6.QtCore import Qt, QDate
from css.styles import AppStyles


class CMFForm(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 1. Scroll Area for the long form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        self.form_layout = QVBoxLayout(container)
        self.form_layout.setSpacing(15)

        # --- SECTION 1: BASIC INFORMATION ---
        basic_group = QGroupBox("General Information")
        basic_form = QFormLayout(basic_group)

        self.txt_cm_no = QLineEdit()
        self.txt_customer = QLineEdit()
        self.date_submitted = QDateEdit(calendarPopup=True)
        self.date_submitted.setDate(QDate.currentDate())
        self.date_required = QDateEdit(calendarPopup=True)
        self.date_required.setDate(QDate.currentDate().addDays(7))

        # Matching Type (Radio)
        type_layout = QHBoxLayout()
        self.radio_new = QRadioButton("New Matching")
        self.radio_rematch = QRadioButton("Re-Match")
        self.radio_new.setChecked(True)
        type_layout.addWidget(self.radio_new)
        type_layout.addWidget(self.radio_rematch)
        type_layout.addStretch()

        self.txt_sales_person = QLineEdit()
        self.txt_color_desc = QLineEdit()
        self.txt_finished_product = QLineEdit()

        basic_form.addRow("Color Matching No:", self.txt_cm_no)
        basic_form.addRow("Customer:", self.txt_customer)
        basic_form.addRow("Date Submitted:", self.date_submitted)
        basic_form.addRow("Date Required:", self.date_required)
        basic_form.addRow("Matching Type:", type_layout)
        basic_form.addRow("Sales Person:", self.txt_sales_person)
        basic_form.addRow("Color Description:", self.txt_color_desc)
        basic_form.addRow("Finished Product:", self.txt_finished_product)

        # --- SECTION 2: COLOR REQUIREMENTS ---
        color_group = QGroupBox("Color Requirement")
        color_grid = QGridLayout(color_group)

        self.chk_transparent = QCheckBox("Transparent")
        self.chk_opaque = QCheckBox("Opaque")
        self.chk_translucent = QCheckBox("Translucent")
        self.chk_metallic = QCheckBox("Metallic")
        self.chk_fluorescent = QCheckBox("Fluorescent")
        self.chk_pearlescent = QCheckBox("Pearlescent")
        self.chk_color_others = QCheckBox("Others:")
        self.txt_color_others = QLineEdit()

        color_grid.addWidget(self.chk_transparent, 0, 0)
        color_grid.addWidget(self.chk_opaque, 0, 1)
        color_grid.addWidget(self.chk_translucent, 0, 2)
        color_grid.addWidget(self.chk_metallic, 1, 0)
        color_grid.addWidget(self.chk_fluorescent, 1, 1)
        color_grid.addWidget(self.chk_pearlescent, 1, 2)
        color_grid.addWidget(self.chk_color_others, 2, 0)
        color_grid.addWidget(self.txt_color_others, 2, 1, 1, 2)

        # --- SECTION 3: RESIN & PROCESS ---
        process_group = QGroupBox("Material & Process")
        process_form = QFormLayout(process_group)

        self.txt_resin = QLineEdit()

        process_grid = QGridLayout()
        self.chk_injection = QCheckBox("Injection")
        self.chk_blow_molding = QCheckBox("Blow-Molding")
        self.chk_film = QCheckBox("Film")
        self.chk_pipe = QCheckBox("Pipe Extrusion")
        self.chk_proc_others = QCheckBox("Others:")
        self.txt_proc_others = QLineEdit()

        process_grid.addWidget(self.chk_injection, 0, 0)
        process_grid.addWidget(self.chk_blow_molding, 0, 1)
        process_grid.addWidget(self.chk_film, 0, 2)
        process_grid.addWidget(self.chk_pipe, 1, 0)
        process_grid.addWidget(self.chk_proc_others, 1, 1)
        process_grid.addWidget(self.txt_proc_others, 1, 2)

        process_form.addRow("Resin:", self.txt_resin)
        process_form.addRow("Process:", process_grid)

        # --- SECTION 4: TECHNICAL SPECS ---
        tech_group = QGroupBox("Technical Specifications")
        tech_form = QFormLayout(tech_group)

        self.txt_qty_resin = QLineEdit()

        # Yes/No groupings
        def create_yes_no():
            layout = QHBoxLayout()
            group = QButtonGroup(self)
            y = QRadioButton("Yes")
            n = QRadioButton("No")
            group.addButton(y)
            group.addButton(n)
            layout.addWidget(y)
            layout.addWidget(n)
            layout.addStretch()
            return layout, y, n

        resin_prov_lay, self.res_y, self.res_n = create_yes_no()
        self.txt_mi_resin = QLineEdit()

        sample_avail_lay, self.samp_y, self.samp_n = create_yes_no()

        colorant_lay = QHBoxLayout()
        self.chk_mb = QCheckBox("MB")
        self.chk_dc = QCheckBox("DC")
        self.chk_col_others = QCheckBox("Others:")
        self.txt_col_others = QLineEdit()
        colorant_lay.addWidget(self.chk_mb)
        colorant_lay.addWidget(self.chk_dc)
        colorant_lay.addWidget(self.chk_col_others)
        colorant_lay.addWidget(self.txt_col_others)

        self.txt_dosage = QLineEdit()
        guide_ret_lay, self.guide_y, self.guide_n = create_yes_no()

        other_spec_lay = QHBoxLayout()
        self.chk_food = QCheckBox("Food Contact")
        self.chk_sun = QCheckBox("Sunlight Exposure")
        other_spec_lay.addWidget(self.chk_food)
        other_spec_lay.addWidget(self.chk_sun)

        self.txt_temp = QLineEdit()
        low_cost_lay, self.low_y, self.low_n = create_yes_no()
        self.txt_remarks = QTextEdit()
        self.txt_remarks.setMaximumHeight(80)

        tech_form.addRow("Qty of Resin for Testing:", self.txt_qty_resin)
        tech_form.addRow("Customer Provided Resin:", resin_prov_lay)
        tech_form.addRow("MI Customer's Resin:", self.txt_mi_resin)
        tech_form.addRow("Is Sample Colorant Avail:", sample_avail_lay)
        tech_form.addRow("Type of Colorant:", colorant_lay)
        tech_form.addRow("Dosage:", self.txt_dosage)
        tech_form.addRow("Is Color Guide to be Returned:", guide_ret_lay)
        tech_form.addRow("Other Specifications:", other_spec_lay)
        tech_form.addRow("Processing Temp:", self.txt_temp)
        tech_form.addRow("Low Cost Requirement:", low_cost_lay)
        tech_form.addRow("Remarks:", self.txt_remarks)

        # Add groups to the scrollable layout
        self.form_layout.addWidget(basic_group)
        self.form_layout.addWidget(color_group)
        self.form_layout.addWidget(process_group)
        self.form_layout.addWidget(tech_group)

        # Product Code Footer
        footer_layout = QHBoxLayout()
        self.txt_prod_code = QLineEdit()
        self.txt_prod_code.setPlaceholderText("To be filled by Color Matching Dept")
        footer_layout.addWidget(QLabel("<b>PRODUCT CODE:</b>"))
        footer_layout.addWidget(self.txt_prod_code)
        self.form_layout.addLayout(footer_layout)

        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # --- BUTTON LAYOUT (AS REQUESTED) ---
        button_layout = QHBoxLayout()

        self.btn_cancel = QPushButton("Cancel", objectName="DangerButton")  # Changed text to Cancel as per Icon logic
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