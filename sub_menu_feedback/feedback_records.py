import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableView, QHeaderView, QFrame,
                             QAbstractItemView, QMenu)
from PyQt6.QtCore import Qt, pyqtSignal
from css.styles import AppStyles
from table_model.model import TableModel

# ─────────────────────────────────────────────────────────────────────────────
# Updated Header List (11 Columns Total)
# ─────────────────────────────────────────────────────────────────────────────
FEEDBACK_HEADERS = [
    "Matching No.", "Customer", "Product Code", "Color Description",
    "Finished Product", "Date Required", "Due Date",
    "Matching Type", "Status", "Status Details", "Package Details"
]


class FeedbackRecords(QWidget):
    request_edit = pyqtSignal(str)

    def __init__(self, mac_department, user_department):
        super().__init__()
        self.mac_department = mac_department
        self.user_department = user_department
        self.setStyleSheet(AppStyles.MAIN_WINDOW_STYLESHEET)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- TOP SECTION: HEADER & SEARCH ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Feedback & Monitoring Records")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0f172a;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText(" Search feedback records...")
        self.txt_search.setFixedWidth(400)
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.textChanged.connect(self.apply_filters)

        self.btn_refresh = QPushButton(" Refresh")
        self.btn_refresh.setIcon(fa.icon('fa5s.sync-alt', color=AppStyles.TEAL_600))
        self.btn_refresh.clicked.connect(self.load_data)

        header_layout.addWidget(self.txt_search)
        header_layout.addWidget(self.btn_refresh)
        self.main_layout.addLayout(header_layout)

        # --- MIDDLE SECTION: TABLE ---
        self.table_container = QFrame(objectName="FormCard")
        table_layout = QVBoxLayout(self.table_container)

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setFrameShape(QFrame.Shape.NoFrame)

        # Context Menu
        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)

        self.model = TableModel([], FEEDBACK_HEADERS)
        self.table_view.setModel(self.model)

        # ─── COLUMN SIZING & RESIZABILITY ───
        header = self.table_view.horizontalHeader()

        # 1. Allow all columns to be manually resized by the user
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # 2. Set initial widths to fit contents so the user has a good starting point
        self.table_view.resizeColumnsToContents()

        # 3. Ensure the Customer column (Index 1) stretches to fill remaining empty space
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        table_layout.addWidget(self.table_view)
        self.main_layout.addWidget(self.table_container)

        # --- BOTTOM SECTION ---
        bottom_bar = QHBoxLayout()
        self.lbl_count = QLabel("Showing 0 records")
        self.lbl_count.setStyleSheet(f"color: {AppStyles.SLATE_500};")
        bottom_bar.addWidget(self.lbl_count)
        bottom_bar.addStretch()

        self.btn_export = QPushButton(" Export to Excel")
        self.btn_export.setObjectName("SecondaryButton")
        self.btn_export.setIcon(fa.icon('fa5s.file-excel', color='white'))
        self.btn_export.setFixedWidth(160)
        bottom_bar.addWidget(self.btn_export)
        self.main_layout.addLayout(bottom_bar)

    def show_context_menu(self, pos):
        index = self.table_view.indexAt(pos)
        if not index.isValid(): return

        cmf_no = str(self.model._data[index.row()][0])
        menu = QMenu(self)
        edit_action = menu.addAction(fa.icon('fa5s.comment-medical', color=AppStyles.TEAL_600),
                                     "Update Feedback")

        action = menu.exec(self.table_view.mapToGlobal(pos))
        if action == edit_action:
            self.request_edit.emit(cmf_no)

    def load_data(self):
        """Fetch data from DB matching the 11 columns in FEEDBACK_HEADERS."""
        # Row format: [Matching No, Customer, P-Code, Desc, Product, ReqDate, DueDate, MatchType, Status, Details, Package]
        self.all_data = [
            ["CMF-24-001", "Masterbatch PH", "PC-RED-01", "Gloss Red", "Cap", "10/25/24", "10/25/24", "New", "Passed",
             "Passed QC testing", "Box 104"],
            ["CMF-24-002", "Generic Co.", "PC-BLU-99", "Matte Blue", "Tray", "11/05/24", "11/06/24", "Re-Match",
             "Pending", "Waiting for final check", "Bin A-2"],
            ["CMF-24-003", "Example Corp", "PC-BLK-05", "Jet Black", "Case", "10/22/24", "10/22/24", "New", "Failed",
             "Color too dark", "Shelf 4"],
        ]
        self.model.set_data(self.all_data)
        self.apply_filters()

    def apply_filters(self):
        search_kw = self.txt_search.text().lower().strip()
        if not search_kw:
            filtered_list = self.all_data[:]
        else:
            filtered_list = [
                row for row in self.all_data
                if any(search_kw in str(cell).lower() for cell in row)
            ]

        self.model.beginResetModel()
        self.model._data = filtered_list
        self.model.endResetModel()
        self.lbl_count.setText(f"Showing {len(filtered_list)} records")