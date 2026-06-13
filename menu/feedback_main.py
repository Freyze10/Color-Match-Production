import qtawesome as fa
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from css.styles import AppStyles

# Assuming your folder structure is sub_menu_feedback
from sub_menu_feedback.feedback_entry import FeedbackEntry
from sub_menu_feedback.feedback_records import FeedbackRecords

class FeedbackModule(QWidget):
    def __init__(self, mac_department, user_department):
        super().__init__()
        self.mac_department = mac_department
        self.user_department = user_department
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # 1. Initialize Tabs
        self.records_tab = FeedbackRecords(self.mac_department, self.user_department)
        self.form_tab = FeedbackEntry(self.mac_department, self.user_department)

        # 2. Connect the Signal (When user clicks 'Edit' in the list)
        self.records_tab.request_edit.connect(self.go_to_edit_tab)

        # 3. Add to Tab Widget
        self.tabs.addTab(self.records_tab, fa.icon('msc.checklist', color=AppStyles.SLATE_600), " Feedback Records")
        self.tabs.addTab(self.form_tab, fa.icon('fa5s.comment-dots', color=AppStyles.SLATE_600), " Feedback Entry")

        self.tabs.setCurrentIndex(0)
        layout.addWidget(self.tabs)

    def go_to_edit_tab(self, cmf_no):
        """Slot to receive CMF No, load the form, and switch tabs"""
        # Populate the Entry Form with the selected CMF No
        self.form_tab.load_cmf_data(cmf_no)
        # Switch to the Entry Tab (Index 1)
        self.tabs.setCurrentIndex(1)