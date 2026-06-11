# util/field_format.py
import math
import re

from PyQt6.QtWidgets import QMessageBox, QLineEdit, QTableWidgetItem, QCompleter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from db.read import get_all_completer_data, get_lot_no


def format_to_float(self, event, number, ):
    """Format the input to a float with 6 decimal places when focus is lost."""
    text = number.text().strip()
    try:
        if text:
            value = float(text)
            number.setText(f"{value:.6f}")
    except ValueError:
        QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
        number.setFocus()
        number.selectAll()
        return
    QLineEdit.focusOutEvent(number, event)


def production_mixing_time(event, line_edit):
    text = line_edit.text().strip()

    # Remove any existing MIN/MINS/MIN./MINS. (case-insensitive)
    text = re.sub(r'\s*MIN\.?S?\s*$', '', text, flags=re.IGNORECASE).strip()

    # Match valid number (integer or float)
    match = re.match(r'^(\d*\.?\d+)', text)
    if match:
        number_str = match.group(1)
        try:
            value = float(number_str)
            # Determine singular/plural
            unit = "MIN." if value == 1.0 else "MINS."
            line_edit.setText(f"{number_str} {unit}")
        except ValueError:
            line_edit.setText("5 MINS.")  # fallback
    else:
        # Optional: revert to default if invalid
        line_edit.setText("5 MINS.")


def add_batch_text(required, per_batch, notes_field):
    """
    Reusable function to calculate and display batch information.

    Parameters:
        required:    Quantity required (can be float, int, or str)
        per_batch:   Quantity per batch (can be float, int, or str)
        notes_field: The QLineEdit / QLabel / widget where the text will be shown
    """
    try:
        # Convert inputs to float safely
        req = float(required) if required is not None else 0.0
        per = float(per_batch) if per_batch is not None else 0.0

        if per <= 0:
            raise ValueError("Per batch quantity must be greater than zero")

        # Use math.ceil to round UP (important for batching)
        n = math.ceil(req / per)

        text = f"{n} batch{'es' if n != 1 else ''} by {per:.3f} KG."
        notes_field.setText(text)

    except Exception:
        notes_field.setText("1 batch by 0.000 KG.")


def expand_lot_list(raw_list):
    expanded = set()  # Use a set to automatically handle duplicates

    for item in raw_list:
        item = item.strip().upper()
        if not item: continue

        if '-' in item:
            try:
                # Split "1801I-1805I" into "1801I" and "1805I"
                parts = item.split('-')
                start_str = parts[0].strip()
                end_str = parts[1].strip()

                # Use Regex to separate numbers from letters (e.g., '1801', 'I')
                start_match = re.match(r"(\d+)([A-Z]+)", start_str)
                end_match = re.match(r"(\d+)([A-Z]+)", end_str)

                if start_match and end_match:
                    start_num = int(start_match.group(1))
                    end_num = int(end_match.group(1))
                    suffix = start_match.group(2)  # Assume suffix is the same (e.g., 'I')

                    # Generate the range
                    for i in range(start_num, end_num + 1):
                        # zfill(4) ensures 905 becomes 0905
                        expanded.add(f"{str(i).zfill(4)}{suffix}")
                else:
                    # Fallback if regex fails: just add the raw parts
                    expanded.add(start_str)
                    expanded.add(end_str)
            except Exception:
                expanded.add(item)  # If something goes wrong, just keep the original
        else:
            # No dash, just a single lot like "0905R"
            expanded.add(item)

    return sorted(list(expanded))


def setup_auto_completers(customer_widget=None,
                          product_widget=None,
                          order_widget=None,
                          lot_list=None):  # New parameter
    if not hasattr(setup_auto_completers, "_cached_expanded_lots"):
        # Fetch raw data from DB
        raw_data = get_lot_no()
        setup_auto_completers._cached_expanded_lots = expand_lot_list(raw_data)

    lot_list_db = setup_auto_completers._cached_expanded_lots
    data = get_all_completer_data()

    def setup_comp(widget, items):
        if not widget or not items:
            return
        str_items = [str(i) for i in items if i]
        if not str_items:
            return

        completer = QCompleter(str_items)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        widget.setCompleter(completer)

    # Setup completers
    if customer_widget:
        setup_comp(customer_widget, data.get('customers', []))

    if product_widget:
        setup_comp(product_widget, data.get('prod_codes', []))

    if order_widget:
        setup_comp(order_widget, data.get('orders', []))

    # Handle lot list - fetch fresh from database
    lot_list_from_db = lot_list_db  # This calls the database

    # If user passed a list (by reference), update it
    if lot_list is not None and isinstance(lot_list, list):
        lot_list.clear()  # Clear old content
        lot_list.extend(lot_list_from_db)  # Fill with new data
        return lot_list  # Return for convenience

    # If no list was passed, just return the fresh list
    return lot_list_from_db


import qtawesome as fa
from PyQt6.QtWidgets import QLineEdit, QCalendarWidget, QDialog, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QKeyEvent


class SmartDateEdit(QLineEdit):
    def __init__(self, parent=None, allow_multiple=False):
        super().__init__(parent)
        self.allow_multiple = allow_multiple
        self._segments = [""]

        # Setup Styling & Placeholder
        self.setPlaceholderText("MM/DD/YYYY" + (", ..." if allow_multiple else ""))
        if not allow_multiple:
            self.setMaxLength(10)

        # ─── ADD CALENDAR ICON ───
        # Uses your existing qtawesome (fa) setup
        self.calendar_action = self.addAction(
            fa.icon('fa5s.calendar-alt', color='#64748B'),
            QLineEdit.ActionPosition.TrailingPosition
        )
        self.calendar_action.triggered.connect(self.show_calendar_popup)

    # ── Internal formatting logic (same as before) ────────────────────────────

    def _format_segment(self, digits: str) -> str:
        d = digits[:8]
        result = ""
        if len(d) >= 1: result += d[:2]
        if len(d) >= 3: result += "/" + d[2:4]
        if len(d) >= 5:
            result += "/" + d[4:8]
        elif len(d) == 3 or len(d) == 4:
            result += "/"
        return result

    def _apply(self):
        self.blockSignals(True)
        formatted_segments = [self._format_segment(s) for s in self._segments if s or len(self._segments) == 1]
        self.setText(", ".join(formatted_segments))
        self.setCursorPosition(len(self.text()))
        self.blockSignals(False)

    # ── Calendar Logic ────────────────────────────────────────────────────────

    def show_calendar_popup(self):
        # Create a frameless popup dialog
        popup = QDialog(self)
        popup.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        layout = QVBoxLayout(popup)
        layout.setContentsMargins(0, 0, 0, 0)

        cal = QCalendarWidget()
        cal.setGridVisible(True)
        # Select the date currently in the last segment if possible
        layout.addWidget(cal)

        # When a date is clicked
        cal.clicked.connect(lambda qdate: self.handle_calendar_selection(qdate, popup))

        # Position the popup below the line edit
        pos = self.mapToGlobal(QPoint(0, self.height()))
        popup.move(pos)
        popup.exec()

    def handle_calendar_selection(self, qdate, popup):
        # Format the selected date into 8 digits: MMDDYYYY
        date_digits = qdate.toString("MMddyyyy")

        if self.allow_multiple:
            # If the current last segment is empty, fill it
            if not self._segments[-1]:
                self._segments[-1] = date_digits
            # If the last segment is already full, add a new one
            elif len(self._segments[-1]) == 8:
                self._segments.append(date_digits)
            # If the last segment is partially typed, overwrite it
            else:
                self._segments[-1] = date_digits
        else:
            # Single mode: overwrite everything
            self._segments = [date_digits]

        self._apply()
        popup.accept()

    # ── Key Events (Manual Typing) ────────────────────────────────────────────

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()

        if key == Qt.Key.Key_Backspace:
            if self._segments:
                if self._segments[-1] == "" and len(self._segments) > 1:
                    self._segments.pop()
                elif self._segments[-1] != "":
                    self._segments[-1] = self._segments[-1][:-1]
                self._apply()
            return

        if self.allow_multiple and text == ",":
            if len(self._segments[-1]) == 8:
                self._segments.append("")
                self._apply()
            return

        if text.isdigit():
            if len(self._segments[-1]) < 8:
                self._segments[-1] += text
                self._apply()
            return

        # Allow basic navigation
        if key in (Qt.Key.Key_Tab, Qt.Key.Key_Backtab, Qt.Key.Key_Return,
                   Qt.Key.Key_Enter, Qt.Key.Key_Left, Qt.Key.Key_Right):
            super().keyPressEvent(event)

    # ── Public Helpers ────────────────────────────────────────────────────────

    def get_dates_list(self):
        return [self._format_segment(s) for s in self._segments if len(s) == 8]

    def set_date_text(self, date_str: str):
        if not date_str:
            self._segments = [""]
        else:
            if self.allow_multiple:
                parts = date_str.split(",")
                self._segments = ["".join(filter(str.isdigit, p))[:8] for p in parts]
            else:
                self._segments = ["".join(filter(str.isdigit, date_str))[:8]]
        self._apply()


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value, display_text=None, is_float=False):
        self.value = value
        self.is_float = is_float
        if display_text is None:
            if is_float:
                display_text = f"{value:.6f}" if value is not None else ""
            else:
                display_text = str(value) if value is not None else ""
        super().__init__(display_text)

    def __lt__(self, other):
        if isinstance(other, NumericTableWidgetItem):
            if self.is_float:
                return float(self.value) < float(other.value)
            else:
                return int(self.value) < int(other.value)
        return super().__lt__(other)