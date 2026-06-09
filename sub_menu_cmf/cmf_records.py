import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableView, QHeaderView, QFrame,
                             QAbstractItemView)
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from table_model.model import TableModel


# Mock import for your database read function
# from db.read import get_cmf_list

class CMFRecords(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        # Centralized styling
        self.setStyleSheet(AppStyles.MAIN_WINDOW_STYLESHEET)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        # 1. Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- TOP SECTION: HEADER & SEARCH ---
        header_layout = QHBoxLayout()

        # Title
        title_label = QLabel("Color Matching Records")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0f172a;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Search Bar
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText(" Search records (CMF#, Customer, Product...)")
        self.txt_search.setFixedWidth(350)
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.textChanged.connect(self.handle_filter)

        # Refresh Button
        self.btn_refresh = QPushButton(" Refresh")
        self.btn_refresh.setIcon(fa.icon('fa5s.sync-alt', color=AppStyles.TEAL_600))
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_refresh.setFixedWidth(110)

        header_layout.addWidget(self.txt_search)
        header_layout.addWidget(self.btn_refresh)
        self.main_layout.addLayout(header_layout)

        # --- MIDDLE SECTION: THE TABLE CARD ---
        self.table_container = QFrame(objectName="FormCard")
        table_layout = QVBoxLayout(self.table_container)
        table_layout.setContentsMargins(10, 10, 10, 10)

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setSortingEnabled(True)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setFrameShape(QFrame.Shape.NoFrame)

        # Initialize Table Model
        self.headers = [
            "CMF No.", "Customer", "Primary Color", "Color Description",
            "Finished Product", "Required Date", "Target Date", "Matching Type"
        ]
        self.model = TableModel([], self.headers)
        self.table_view.setModel(self.model)

        # Configure Header sizing
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        # Make specific columns wider by default
        header.resizeSection(0, 120)  # CMF No
        header.resizeSection(1, 180)  # Customer
        header.resizeSection(3, 200)  # Description

        table_layout.addWidget(self.table_view)
        self.main_layout.addWidget(self.table_container)

        # --- BOTTOM SECTION: FOOTER ---
        self.lbl_count = QLabel("Showing 0 records")
        self.lbl_count.setStyleSheet(f"color: {AppStyles.SLATE_500}; font-size: 13px;")
        self.main_layout.addWidget(self.lbl_count)

    def load_data(self):
        """
        Fetch data from the database and populate the table.
        Replace 'dummy_data' with your actual database call.
        """
        # Example data format matching the headers
        dummy_data = [
            ["CMF-2024-001", "Customer A", "Red", "Glossy Red Finish", "Plastic Toy", "10/25/2024", "10/30/2024",
             "New"],
            ["CMF-2024-002", "Customer B", "Blue", "Matte Blue", "Car Part", "11/01/2024", "11/05/2024", "Re-Match"],
            ["CMF-2024-003", "Customer C", "Black", "Jet Black", "Phone Case", "10/20/2024", "10/22/2024", "New"],
        ]

        # Actual Implementation:
        # data = get_cmf_list()
        # self.model.set_data(data)

        self.model.set_data(dummy_data)
        self.update_count()

    def handle_filter(self):
        """Filters the table based on the search bar text."""
        search_text = self.txt_search.text()
        self.model.filter_data(search_text)
        self.update_count()

    def update_count(self):
        count = self.model.rowCount()
        self.lbl_count.setText(f"Showing {count} records")

    def get_selected_cmf_no(self):
        """Returns the CMF Number of the selected row."""
        index = self.table_view.currentIndex()
        if index.isValid():
            # Returns the value from the first column (index 0)
            return self.model._data[index.row()][0]
        return None