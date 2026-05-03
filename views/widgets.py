"""Shared reusable UI widgets"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QListWidget, QListWidgetItem, QFrame, QLabel,
                             QApplication)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


# ── Shared style helpers ───────────────────────────────────────────────────────

SHARED_INPUT_STYLE = """
    QLineEdit {
        padding: 10px 14px;
        border: 1.5px solid #d1d5db;
        border-radius: 8px;
        font-size: 13px;
        background-color: #f9fafb;
        color: #111827;
        font-family: 'Segoe UI', sans-serif;
    }
    QLineEdit:focus {
        border: 1.5px solid #2563eb;
        background-color: #ffffff;
    }
"""

SHARED_BTN_STYLE = """
    QPushButton {{
        background-color: {bg};
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        padding: 10px 22px;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.2px;
    }}
    QPushButton:hover {{
        background-color: {hover};
    }}
    QPushButton:pressed {{
        background-color: {pressed};
    }}
    QPushButton:disabled {{
        background-color: #d1d5db;
        color: #9ca3af;
    }}
"""

SHARED_TABLE_STYLE = """
    QTableWidget {
        border: none;
        background-color: #ffffff;
        gridline-color: #f3f4f6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        selection-background-color: #eff6ff;
    }
    QTableWidget::item {
        padding: 12px 16px;
        color: #1f2937;
        border-bottom: 1px solid #f3f4f6;
    }
    QTableWidget::item:selected {
        background-color: #dbeafe;
        color: #1e3a8a;
    }
    QTableWidget::item:hover {
        background-color: #f0f9ff;
    }
    QHeaderView::section {
        background-color: #f8fafc;
        color: #374151;
        padding: 13px 16px;
        border: none;
        border-bottom: 2px solid #e5e7eb;
        font-weight: 700;
        font-size: 12px;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
"""

def btn_style(bg, hover, pressed=None):
    return SHARED_BTN_STYLE.format(bg=bg, hover=hover, pressed=pressed or hover)

def section_label(text):
    """Returns a styled section/form label"""
    lbl = QLabel(text)
    lbl.setStyleSheet("""
        font-size: 12px;
        font-weight: 600;
        color: #374151;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 4px;
    """)
    return lbl


# ── Searchable Combo Box ───────────────────────────────────────────────────────

class SearchableComboBox(QWidget):
    """
    Drop-in replacement for QComboBox with built-in search/filter.
    Popup is a separate top-level window — safe to create at any time.
    Emits selection_changed(data_id: int, display_text: str).
    """
    selection_changed = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_items = []   # list of (label_str, data_id)
        self._selected_id = None
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedHeight(46)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Visible search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search customer…")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 14px;
                border: 1.5px solid #d1d5db;
                border-radius: 8px;
                font-size: 13px;
                background-color: #f9fafb;
                color: #111827;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit:focus {
                border: 1.5px solid #2563eb;
                background-color: #ffffff;
            }
        """)
        self.search_input.textChanged.connect(self._on_text_changed)
        self.search_input.installEventFilter(self)
        outer.addWidget(self.search_input)

        # Popup — created as a true top-level popup window (no parent)
        self._popup = QFrame(None, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self._popup.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border: 1.5px solid #2563eb;
                border-radius: 8px;
            }
        """)
        pop_layout = QVBoxLayout(self._popup)
        pop_layout.setContentsMargins(4, 4, 4, 4)
        pop_layout.setSpacing(0)

        self._list = QListWidget()
        self._list.setStyleSheet("""
            QListWidget {
                border: none;
                background: #ffffff;
                font-size: 13px;
                font-family: 'Segoe UI', sans-serif;
                outline: none;
            }
            QListWidget::item {
                padding: 9px 12px;
                color: #111827;
                border-radius: 5px;
                margin: 1px 2px;
            }
            QListWidget::item:hover {
                background-color: #eff6ff;
                color: #1d4ed8;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
                font-weight: 600;
            }
        """)
        self._list.itemClicked.connect(self._on_item_selected)
        pop_layout.addWidget(self._list)
        self._popup.hide()

    # ── Event filter: open popup on click or arrow key ─────────────────────────

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj is self.search_input:
            if event.type() == QEvent.Type.MouseButtonPress:
                self._show_popup()
                return False
        return super().eventFilter(obj, event)

    # ── Popup logic ────────────────────────────────────────────────────────────

    def _on_text_changed(self, text):
        self._selected_id = None
        self._filter_list(text)
        if not self._popup.isVisible():
            self._show_popup()
        else:
            self._resize_popup()

    def _show_popup(self):
        self._filter_list(self.search_input.text())
        if self._list.count() == 0:
            return
        self._resize_popup()
        self._popup.show()
        self._popup.raise_()

    def _resize_popup(self):
        pos = self.search_input.mapToGlobal(self.search_input.rect().bottomLeft())
        width = self.search_input.width()
        height = min(240, self._list.count() * 38 + 12)
        self._popup.setGeometry(pos.x(), pos.y() + 2, width, height)

    def _filter_list(self, text):
        self._list.clear()
        kw = text.lower().strip()
        for label, data_id in self._all_items:
            if not kw or kw in label.lower():
                item = QListWidgetItem(label)
                item.setData(Qt.ItemDataRole.UserRole, data_id)
                self._list.addItem(item)

    def _on_item_selected(self, item):
        self._selected_id = item.data(Qt.ItemDataRole.UserRole)
        self.search_input.setText(item.text())
        self._popup.hide()
        self.selection_changed.emit(self._selected_id, item.text())

    # ── Public API ─────────────────────────────────────────────────────────────

    def populate(self, items):
        """items: list of (label_str, data_id)"""
        self._all_items = items
        self._filter_list('')

    def set_selection_by_id(self, data_id):
        for label, did in self._all_items:
            if did == data_id:
                self._selected_id = data_id
                self.search_input.setText(label)
                return

    def current_data(self):
        return self._selected_id

    def clear_selection(self):
        self._selected_id = None
        self.search_input.clear()
