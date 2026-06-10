import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QDateEdit, QRadioButton, QCheckBox, QPushButton,
                             QScrollArea, QFrame, QGroupBox, QFormLayout, QTextEdit,
                             QButtonGroup, QGridLayout, QSizePolicy, QComboBox)
from PyQt6.QtCore import Qt, QDate
from css.styles import AppStyles


class CMFForm(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        self.init_ui()

    def init_ui(self):
        # 1. Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 0)
        self.main_layout.setSpacing(10)

        # 2. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setSpacing(10)

        # =========================================================================
        # TOP PART: TWO COLUMNS
        # =========================================================================
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(20)

        # --- LEFT COLUMN (Stretch 3) ---
        left_col = QVBoxLayout()

        gen_group = QGroupBox("General Information")
        gen_form = QFormLayout(gen_group)
        gen_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        gen_form.setSpacing(12)

        self.txt_cm_no = QLineEdit()
        self.txt_customer = QLineEdit()

        # ─── DATE ROW 1: Submitted (DateEdit) & Required (LineEdit) ───
        date_row_1 = QHBoxLayout()
        date_row_1.setSpacing(10)
        self.date_submitted = QDateEdit(calendarPopup=True, date=QDate.currentDate())
        self.date_submitted.setDisplayFormat("MM/dd/yyyy")  # Set Format

        self.txt_date_required = QLineEdit()
        self.txt_date_required.setPlaceholderText("MM/DD/YYYY")

        date_row_1.addWidget(self.date_submitted, 1)
        date_row_1.addWidget(QLabel("Required Date:"), 0)
        date_row_1.addWidget(self.txt_date_required, 1)

        # ─── DATE ROW 2: Received (LineEdit) & Due (DateEdit) ───
        date_row_2 = QHBoxLayout()
        date_row_2.setSpacing(10)
        self.txt_date_received = QLineEdit()
        self.txt_date_received.setPlaceholderText("MM/DD/YYYY")

        self.date_due = QDateEdit(calendarPopup=True, date=QDate.currentDate().addDays(5))
        self.date_due.setDisplayFormat("MM/dd/yyyy")  # Set Format

        date_row_2.addWidget(self.txt_date_received, 1)
        date_row_2.addWidget(QLabel("Due Date:"), 0)
        date_row_2.addWidget(self.date_due, 1)

        type_lay = QHBoxLayout()
        self.rad_new = QRadioButton("New Matching")
        self.rad_rematch = QRadioButton("Re-Match")
        self.rad_new.setChecked(True)
        type_lay.addWidget(self.rad_new)
        type_lay.addWidget(self.rad_rematch)
        type_lay.addStretch()

        self.txt_sales_person = QLineEdit()
        self.txt_finished_product = QLineEdit()

        # ─── COLOR ROW: Primary & Description ───
        color_row = QHBoxLayout()
        self.cmb_primary_color = QComboBox()
        self.cmb_primary_color.addItems(
            ["", "Red", "Blue", "Yellow", "Green", "Orange", "Purple", "Brown", "Black", "White", "Grey"])
        self.cmb_primary_color.setFixedWidth(120)

        self.txt_color_desc = QLineEdit()
        self.txt_color_desc.setPlaceholderText("Enter color description...")

        color_row.addWidget(self.cmb_primary_color)
        color_row.addWidget(QLabel("Description:"), 0)
        color_row.addWidget(self.txt_color_desc, 1)

        # Adding to Form
        gen_form.addRow("Color Matching No:", self.txt_cm_no)
        gen_form.addRow("Customer:", self.txt_customer)
        gen_form.addRow("Date Submitted:", date_row_1)
        gen_form.addRow("Date Received:", date_row_2)
        gen_form.addRow("Matching Type:", type_lay)
        gen_form.addRow("Sales Person:", self.txt_sales_person)
        gen_form.addRow("Finished Product:", self.txt_finished_product)
        gen_form.addRow("Primary Color:", color_row)

        color_group = QGroupBox("Color Requirement")
        color_grid = QGridLayout(color_group)
        self.color_bg = QButtonGroup(self)
        requirements = ["Transparent", "Opaque", "Translucent", "Metallic", "Fluorescent", "Pearlescent"]
        for i, name in enumerate(requirements):
            rad = QRadioButton(name)
            self.color_bg.addButton(rad)
            color_grid.addWidget(rad, i // 3, i % 3)

        self.rad_col_others = QRadioButton("Others:")
        self.color_bg.addButton(self.rad_col_others)
        self.txt_col_req_others = QLineEdit()
        color_grid.addWidget(self.rad_col_others, 2, 0)
        color_grid.addWidget(self.txt_col_req_others, 2, 1, 1, 2)

        left_col.addWidget(gen_group)
        left_col.addWidget(color_group)

        # --- RIGHT COLUMN ---
        right_col = QVBoxLayout()
        tech_group = QGroupBox("Process & Technical Specifications")
        tech_form = QFormLayout(tech_group)
        tech_form.setSpacing(10)

        self.txt_resin = QLineEdit()
        proc_grid = QGridLayout()
        self.chk_inj = QCheckBox("Injection");
        self.chk_blow = QCheckBox("Blow-Molding")
        self.chk_film = QCheckBox("Film");
        self.chk_pipe = QCheckBox("Pipe Extrusion")
        proc_grid.addWidget(self.chk_inj, 0, 0);
        proc_grid.addWidget(self.chk_blow, 0, 1)
        proc_grid.addWidget(self.chk_film, 1, 0);
        proc_grid.addWidget(self.chk_pipe, 1, 1)

        self.txt_qty_resin = QLineEdit()

        def yes_no_layout():
            lay = QHBoxLayout();
            bg = QButtonGroup(self)
            y, n = QRadioButton("Yes"), QRadioButton("No")
            bg.addButton(y);
            bg.addButton(n)
            lay.addWidget(y);
            lay.addWidget(n);
            lay.addStretch()
            return lay, y, n

        res_lay, self.res_y, self.res_n = yes_no_layout()
        self.txt_mi = QLineEdit()
        samp_lay, self.samp_y, self.samp_n = yes_no_layout()

        colorant_lay = QHBoxLayout()
        self.colorant_bg = QButtonGroup(self)
        self.rad_mb = QRadioButton("MB");
        self.rad_dc = QRadioButton("DC");
        self.rad_colorant_others = QRadioButton("Others:")
        self.colorant_bg.addButton(self.rad_mb);
        self.colorant_bg.addButton(self.rad_dc);
        self.colorant_bg.addButton(self.rad_colorant_others)
        self.txt_colorant_others = QLineEdit()
        colorant_lay.addWidget(self.rad_mb);
        colorant_lay.addWidget(self.rad_dc);
        colorant_lay.addWidget(self.rad_colorant_others);
        colorant_lay.addWidget(self.txt_colorant_others)

        self.txt_dosage = QLineEdit()

        spec_lay = QHBoxLayout()
        self.chk_food = QCheckBox("Food Contact");
        self.chk_sunlight = QCheckBox("Sunlight Exposure");
        self.chk_spec_others = QCheckBox("Others:")
        self.txt_spec_others = QLineEdit()
        spec_lay.addWidget(self.chk_food);
        spec_lay.addWidget(self.chk_sunlight);
        spec_lay.addWidget(self.chk_spec_others);
        spec_lay.addWidget(self.txt_spec_others)

        guide_lay, self.guide_y, self.guide_n = yes_no_layout()
        self.txt_temp = QLineEdit()
        low_lay, self.low_y, self.low_n = yes_no_layout()

        self.txt_remarks = QTextEdit()
        self.txt_remarks.setPlaceholderText("Remarks...")
        self.txt_remarks.setMaximumHeight(40)

        tech_form.addRow("Resin Type:", self.txt_resin)
        tech_form.addRow("Process:", proc_grid)
        tech_form.addRow("Qty Resin for Test:", self.txt_qty_resin)
        tech_form.addRow("Resin Provided:", res_lay)
        tech_form.addRow("MI Value:", self.txt_mi)
        tech_form.addRow("Sample Avail:", samp_lay)
        tech_form.addRow("Type of Colorant:", colorant_lay)
        tech_form.addRow("Target Dosage:", self.txt_dosage)
        tech_form.addRow("Other Specs:", spec_lay)
        tech_form.addRow("Return Guide:", guide_lay)
        tech_form.addRow("Operating Temp:", self.txt_temp)
        tech_form.addRow("Low Cost Req:", low_lay)
        tech_form.addRow("Remarks:", self.txt_remarks)

        right_col.addWidget(tech_group)

        columns_layout.addLayout(left_col, 3)
        columns_layout.addLayout(right_col, 2)

        # =========================================================================
        # BOTTOM PART: NOTES
        # =========================================================================
        notes_group = QGroupBox("Additional Information")
        notes_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        notes_layout = QVBoxLayout(notes_group)

        self.txt_additional_info = QTextEdit()
        self.txt_additional_info.setPlaceholderText("Detailed technical info, special instructions, etc...")
        self.txt_additional_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.txt_additional_info.setMinimumHeight(200)
        notes_layout.addWidget(self.txt_additional_info)

        self.container_layout.addLayout(columns_layout, 0)
        self.container_layout.addWidget(notes_group, 1)

        # Footer
        footer_info = QHBoxLayout()
        self.txt_prod_code = QLineEdit()
        footer_info.addWidget(QLabel("<b>PRODUCT CODE:</b>"))
        footer_info.addWidget(self.txt_prod_code)
        self.container_layout.addLayout(footer_info)

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
            btn.setMinimumHeight(40)

        button_layout.addWidget(self.btn_upload)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_print)
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(button_layout)