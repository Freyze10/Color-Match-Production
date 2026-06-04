from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CMFForm(QWidget):
    def __init__(self, mac_role, user_role):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This is the CMF Entry Form"))
        # Add your form logic here...