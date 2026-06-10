import qtawesome as fa
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFormLayout, QFrame, QAbstractItemView, QScrollArea,
                             QStyledItemDelegate, QComboBox, QCompleter)
from PyQt6.QtCore import Qt
from css.styles import AppStyles
from util.formula_table_delegate import MaterialDelegate, NumericDelegate


class PendingCompleted(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        self.mac_role = mac_role
        self.user_role = user_role
        self.init_ui()

    def init_ui(self):
        pass