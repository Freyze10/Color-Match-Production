import qtawesome as fa
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt

# Import your sub-widgets from their respective files
from css.styles import AppStyles
from sub_menu_cmf.cmf_form import CMFForm
from sub_menu_cmf.cmf_records import CMFRecords
from sub_menu_cmf.dc_formula import DCFormula
from sub_menu_cmf.mb_formula import MBFormula


class CMFModule(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create the Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)  # Makes it look cleaner on some platforms

        # 1. Initialize the sub-widgets
        # We pass roles/permissions down to the children
        self.cmf_records_tab = CMFRecords(self.mac_role, self.user_role)
        self.cmf_form_tab = CMFForm(self.mac_role, self.user_role)
        self.mb_formula_tab = MBFormula(self.mac_role, self.user_role)
        self.dc_formula_tab = DCFormula(self.mac_role, self.user_role)

        # 2. Add widgets to tabs with icons
        self.tabs.addTab(self.cmf_records_tab, fa.icon('msc.checklist', color=AppStyles.SLATE_600), " CMF Records")
        self.tabs.addTab(self.cmf_form_tab, fa.icon('fa5s.file-alt', color=AppStyles.SLATE_600), " CMF Form")
        self.tabs.addTab(self.mb_formula_tab, fa.icon('mdi.flask-outline', color=AppStyles.SLATE_600), " MB Formula")
        self.tabs.addTab(self.dc_formula_tab, fa.icon('mdi.flask-empty-outline', color=AppStyles.SLATE_600),
                         " DC Formula")

        # 3. SET DEFAULT TAB
        # This ensures Tab 1 (Index 0) is always shown when the widget opens
        self.tabs.setCurrentIndex(0)

        layout.addWidget(self.tabs)

    def open_specific_tab(self, index):
        """Helper method if you want to jump to a tab from code later"""
        self.tabs.setCurrentIndex(index)