import qtawesome as fa
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from sub_menu_cmf.cmf_form import CMFForm
from sub_menu_cmf.cmf_records import CMFRecords
from sub_menu_cmf.dc_formula import DCFormula
from sub_menu_cmf.mb_formula import MBFormula
from sub_menu_cmf.pending_completed import PendingCompleted

class CMFModule(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.cmf_records_tab = CMFRecords(self.mac_role, self.user_role)
        self.cmf_form_tab = CMFForm(self.mac_role, self.user_role)
        self.mb_formula_tab = MBFormula(self.mac_role, self.user_role)
        self.dc_formula_tab = DCFormula(self.mac_role, self.user_role)
        self.pending_completed_tab = PendingCompleted(self.mac_role, self.user_role)

        # Connect the bridge signal
        self.cmf_records_tab.request_update.connect(self.go_to_update_tab)
        self.cmf_records_tab.request_edit.connect(self.go_to_edit_tab)

        self.tabs.addTab(self.cmf_records_tab, fa.icon('msc.checklist', color=AppStyles.SLATE_600), " CMF Records")
        self.tabs.addTab(self.cmf_form_tab, fa.icon('fa5s.file-alt', color=AppStyles.SLATE_600), " CMF Form")
        self.tabs.addTab(self.mb_formula_tab, fa.icon('mdi.flask-outline', color=AppStyles.SLATE_600), " MB Formula")
        self.tabs.addTab(self.dc_formula_tab, fa.icon('mdi.flask-empty-outline', color=AppStyles.SLATE_600), " DC Formula")
        self.tabs.addTab(self.pending_completed_tab, fa.icon('ri.file-edit-line', color=AppStyles.SLATE_600), " Pending/Completed")

        self.tabs.setCurrentIndex(0)
        layout.addWidget(self.tabs)

    def go_to_update_tab(self, cmf_no):
        """Slot to handle jumping to tab 5 (index 4)"""
        self.pending_completed_tab.load_cmf_data(cmf_no)
        self.tabs.setCurrentIndex(4)

    def go_to_edit_tab(self, cmf_no):
        """Slot to handle jumping to tab 2 (index 1)"""
        # self.cmf_form_tab.load_data(cmf_no) # Assuming CMFForm has a load method
        self.tabs.setCurrentIndex(1)