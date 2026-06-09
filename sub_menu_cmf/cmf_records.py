import qtawesome as fa
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableView, QHeaderView, QFrame,
                             QAbstractItemView, QCheckBox)
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from table_model.model import TableModel


# ─────────────────────────────────────────────────────────────────────────────
# Column index map (internal / full data row layout)
# ─────────────────────────────────────────────────────────────────────────────
# 0  CMF No.
# 1  Customer
# 2  Primary Color
# 3  Color Description
# 4  Finished Product
# 5  Required Date
# 6  Target Date
# 7  Matching Type
# 8  Product Code
# 9  Status
# 10 Submitted Date
# 11 AR No.
# 12 Reason

ALL_HEADERS = [
    "CMF No.", "Customer", "Primary Color", "Color Description",
    "Finished Product", "Required Date", "Target Date", "Matching Type",
    "Product Code", "Status", "Submitted Date", "AR No.", "Reason"
]

# Columns shown when BOTH checkboxes are checked (your current default view)
COLS_BOTH = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Columns shown when ONLY Completed is checked
COLS_COMPLETED = [0, 1, 2, 3, 4, 7, 8, 10, 11]

# Columns shown when ONLY Pending is checked
COLS_PENDING = [0, 1, 2, 3, 4, 5, 6, 7, 12]


class CMFRecords(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role

        self.setStyleSheet(AppStyles.MAIN_WINDOW_STYLESHEET)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- TOP SECTION: HEADER & SEARCH ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Color Matching Records")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0f172a;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText(" Search records...")
        self.txt_search.setFixedWidth(350)
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
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setFrameShape(QFrame.Shape.NoFrame)

        # Model is initialized with full headers; columns are hidden/shown via header
        self.model = TableModel([], ALL_HEADERS)
        self.table_view.setModel(self.model)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        table_layout.addWidget(self.table_view)
        self.main_layout.addWidget(self.table_container)

        # --- BOTTOM SECTION: FILTERS & EXPORT ---
        bottom_bar = QHBoxLayout()

        bottom_bar.addWidget(QLabel("<b>Filter Status:</b>"))

        self.chk_completed = QCheckBox("Completed")
        self.chk_pending = QCheckBox("Pending")
        self.chk_completed.setChecked(True)
        self.chk_pending.setChecked(True)

        self.chk_completed.stateChanged.connect(self.apply_filters)
        self.chk_pending.stateChanged.connect(self.apply_filters)

        bottom_bar.addWidget(self.chk_completed)
        bottom_bar.addWidget(self.chk_pending)

        bottom_bar.addSpacing(20)
        self.lbl_count = QLabel("Showing 0 records")
        bottom_bar.addWidget(self.lbl_count)
        bottom_bar.addStretch()

        self.btn_export = QPushButton(" Export to Excel")
        self.btn_export.setObjectName("SecondaryButton")
        self.btn_export.setIcon(fa.icon('fa5s.file-excel', color='white'))
        self.btn_export.setFixedWidth(160)
        self.btn_export.clicked.connect(self.handle_export)
        bottom_bar.addWidget(self.btn_export)

        self.main_layout.addLayout(bottom_bar)

    def _apply_column_visibility(self):
        """Show only the columns relevant to the current checkbox state."""
        show_completed = self.chk_completed.isChecked()
        show_pending = self.chk_pending.isChecked()

        if show_completed and show_pending:
            visible_cols = COLS_BOTH
        elif show_completed:
            visible_cols = COLS_COMPLETED
        elif show_pending:
            visible_cols = COLS_PENDING
        else:
            # Both unchecked — keep the default layout visible but table will be empty
            visible_cols = COLS_BOTH

        header = self.table_view.horizontalHeader()
        for col in range(len(ALL_HEADERS)):
            if col in visible_cols:
                header.showSection(col)
            else:
                header.hideSection(col)

    def load_data(self):
        """Fetch all data from DB initially."""
        # Full row must have a value for every column in ALL_HEADERS (13 cols)
        # Index:          0             1               2        3        4          5           6           7        8         9            10               11         12
        self.all_data = [
            ["CMF-24-001", "Masterbatch PH", "Red",   "Gloss", "Cap",   "10/25/24", "10/30/24", "New",    "PC-001", "Completed", "10/31/24",  "AR-001",   ""],
            ["CMF-24-002", "Generic Co.",    "Blue",  "Matte", "Tray",  "11/01/24", "11/05/24", "Re-Match","PC-002", "Pending",  "",          "",         "Awaiting approval"],
            ["CMF-24-003", "Example Corp",   "Black", "Jet",   "Case",  "10/20/24", "10/22/24", "New",    "PC-003", "Completed", "10/23/24",  "AR-003",   ""],
            ["CMF-24-004", "Tech Solutions", "White", "Snow",  "Panel", "11/10/24", "11/15/24", "New",    "PC-004", "Pending",  "",          "",         "Sample not yet received"],
        ]
        self.model.set_data(self.all_data)
        self.apply_filters()

    def apply_filters(self):
        """Filters rows by status + search keyword, then updates column visibility."""
        search_kw = self.txt_search.text().lower().strip()
        show_completed = self.chk_completed.isChecked()
        show_pending = self.chk_pending.isChecked()

        filtered_list = []
        for row in self.all_data:
            status = row[9]
            status_match = (show_completed and status == "Completed") or \
                           (show_pending and status == "Pending")
            if not status_match:
                continue
            if not search_kw or any(search_kw in str(cell).lower() for cell in row):
                filtered_list.append(row)

        self.model.beginResetModel()
        self.model._data = filtered_list
        self.model.endResetModel()

        self.lbl_count.setText(f"Showing {len(filtered_list)} records")

        # Update which columns are visible after the data is refreshed
        self._apply_column_visibility()

    def handle_export(self):
        print("Exporting currently visible records...")