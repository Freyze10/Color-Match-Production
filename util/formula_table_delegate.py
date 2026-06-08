# --- DELEGATE FOR NUMBERS (Cols 1 & 2) ---
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox, QCompleter


class NumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QDoubleValidator(0.0, 999999999.99, 7, editor)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        editor.setValidator(validator)
        return editor


# --- DELEGATE FOR MATERIAL AUTOFILL (Col 0) ---
class MaterialDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, materials=None):
        super().__init__(parent)
        self.materials = materials or []

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.setEditable(True)
        editor.addItems(self.materials)

        completer = editor.completer()
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)

        editor.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        return editor

    def setModelData(self, editor, model, index):
        val = editor.currentText()
        if val in self.materials:
            model.setData(index, val, Qt.ItemDataRole.EditRole)
        else:
            model.setData(index, "", Qt.ItemDataRole.EditRole)