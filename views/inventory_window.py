"""Inventory management window - FIXED"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox, QFrame,
                             QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from controllers.inventory_controller import InventoryController
from utils.validators import validate_not_empty, validate_numeric


class InventoryWindow(QWidget):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.inventory_controller = InventoryController()
        self.init_ui()
        try:
            self.load_inventory()
        except Exception as e:
            print(f"Error loading inventory: {e}")

    def init_ui(self):
        """Initialize inventory UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        self.setStyleSheet("background-color: #f8fafc;")

        # Title section
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-bottom: 2px solid #e2e8f0;
                padding: 15px 0px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(15, 10, 15, 10)

        title = QLabel("📦 Inventory Management")
        title.setStyleSheet("color: #1f2937; font-size: 26px; font-weight: 700;")
        title_layout.addWidget(title)

        layout.addWidget(title_frame)

        # Tabs for Stock-In and Stock-Out
        tab_layout = QHBoxLayout()

        # Stock In Section
        stock_in_group = self.create_stock_in_section()
        tab_layout.addWidget(stock_in_group)

        # Stock Out Section
        stock_out_group = self.create_stock_out_section()
        tab_layout.addWidget(stock_out_group)

        layout.addLayout(tab_layout)

        # Inventory Table
        table_label = QLabel("📊 Inventory Status:")
        table_label.setStyleSheet("color: #1f2937; font-weight: 600; font-size: 14px;")
        layout.addWidget(table_label)

        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Item Name', 'Available', 'Threshold', 'Status'])
        self.table.setStyleSheet(self.get_table_style())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_frame)
        self.setLayout(layout)

    def create_stock_in_section(self):
        """Create stock-in section"""
        group = QGroupBox("Stock-In")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 15px;
                font-weight: 600;
                color: #1f2937;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        layout = QVBoxLayout()

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Item:"))
        self.stockin_item_combo = QComboBox()
        self.stockin_item_combo.setStyleSheet(self.get_input_style())
        self.stockin_item_combo.setMinimumHeight(42)
        try:
            self.load_items_combo(self.stockin_item_combo)
        except:
            pass
        form_layout.addWidget(self.stockin_item_combo)

        form_layout.addWidget(QLabel("Qty:"))
        self.stockin_qty_spin = QSpinBox()
        self.stockin_qty_spin.setMinimum(1)
        self.stockin_qty_spin.setStyleSheet(self.get_input_style())
        self.stockin_qty_spin.setMinimumHeight(42)
        form_layout.addWidget(self.stockin_qty_spin)

        form_layout.addWidget(QLabel("Supplier:"))
        self.supplier_input = QLineEdit()
        self.supplier_input.setStyleSheet(self.get_input_style())
        self.supplier_input.setMinimumHeight(42)
        form_layout.addWidget(self.supplier_input)

        form_layout.addWidget(QLabel("Cost:"))
        self.stockin_cost_spin = QDoubleSpinBox()
        self.stockin_cost_spin.setMinimum(0)
        self.stockin_cost_spin.setStyleSheet(self.get_input_style())
        self.stockin_cost_spin.setMinimumHeight(42)
        form_layout.addWidget(self.stockin_cost_spin)

        layout.addLayout(form_layout)

        # Button
        stockin_btn = QPushButton("➕ Stock-In")
        stockin_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
        stockin_btn.setMinimumHeight(44)
        stockin_btn.clicked.connect(self.stock_in)
        layout.addWidget(stockin_btn)

        group.setLayout(layout)
        return group

    def create_stock_out_section(self):
        """Create stock-out section"""
        group = QGroupBox("Stock-Out")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 15px;
                font-weight: 600;
                color: #1f2937;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        layout = QVBoxLayout()

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Item:"))
        self.stockout_item_combo = QComboBox()
        self.stockout_item_combo.setStyleSheet(self.get_input_style())
        self.stockout_item_combo.setMinimumHeight(42)
        try:
            self.load_items_combo(self.stockout_item_combo)
        except:
            pass
        form_layout.addWidget(self.stockout_item_combo)

        form_layout.addWidget(QLabel("Qty:"))
        self.stockout_qty_spin = QSpinBox()
        self.stockout_qty_spin.setMinimum(1)
        self.stockout_qty_spin.setStyleSheet(self.get_input_style())
        self.stockout_qty_spin.setMinimumHeight(42)
        form_layout.addWidget(self.stockout_qty_spin)

        form_layout.addWidget(QLabel("Reason:"))
        self.reason_input = QLineEdit()
        self.reason_input.setStyleSheet(self.get_input_style())
        self.reason_input.setMinimumHeight(42)
        form_layout.addWidget(self.reason_input)

        form_layout.addStretch()
        layout.addLayout(form_layout)

        # Button
        stockout_btn = QPushButton("➖ Stock-Out")
        stockout_btn.setStyleSheet(self.get_button_style("#ef4444", "#dc2626"))
        stockout_btn.setMinimumHeight(44)
        stockout_btn.clicked.connect(self.stock_out)
        layout.addWidget(stockout_btn)

        group.setLayout(layout)
        return group

    def load_items_combo(self, combo):
        """Load items in combo"""
        try:
            items = self.inventory_controller.get_all_items()
            if items:
                for item in items:
                    combo.addItem(item.get('item_name', ''), item.get('item_id'))
        except Exception as e:
            print(f"Error loading items: {e}")

    def load_inventory(self):
        """Load inventory from database"""
        try:
            items = self.inventory_controller.get_all_items()
            if items is None:
                items = []

            self.table.setRowCount(len(items))

            for row, item in enumerate(items):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(item.get('item_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(item.get('item_name', '')))
                    self.table.setItem(row, 2, QTableWidgetItem(str(item.get('quantity_available', ''))))
                    self.table.setItem(row, 3, QTableWidgetItem(str(item.get('minimum_threshold', ''))))

                    # Status without QColor - use stylesheet instead
                    qty_available = item.get('quantity_available', 0)
                    threshold = item.get('minimum_threshold', 0)
                    status = "⚠️ Low Stock" if qty_available < threshold else "✓ OK"
                    status_item = QTableWidgetItem(status)

                    if qty_available < threshold:
                        status_item.setBackground(__import__('PyQt6.QtGui', fromlist=['QBrush']).QBrush(
                            __import__('PyQt6.QtCore', fromlist=['Qt']).Qt.GlobalColor.red
                        ))

                    self.table.setItem(row, 4, status_item)
                except Exception as e:
                    print(f"Error loading inventory row {row}: {e}")
        except Exception as e:
            print(f"Error loading inventory: {e}")

    def stock_in(self):
        """Add stock"""
        try:
            item_id = self.stockin_item_combo.currentData()
            if not item_id:
                QMessageBox.warning(self, "Error", "Please select an item")
                return

            quantity = self.stockin_qty_spin.value()
            supplier = self.supplier_input.text().strip()
            total_cost = self.stockin_cost_spin.value()

            if not supplier:
                QMessageBox.warning(self, "Error", "Please enter supplier name")
                return

            if self.inventory_controller.stock_in(item_id, quantity, supplier, total_cost):
                QMessageBox.information(self, "Success", "Stock added successfully")
                self.supplier_input.clear()
                self.stockin_qty_spin.setValue(1)
                self.stockin_cost_spin.setValue(0)
                self.data_changed.emit()
                self.load_inventory()
            else:
                QMessageBox.warning(self, "Error", "Failed to add stock")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def stock_out(self):
        """Remove stock"""
        try:
            item_id = self.stockout_item_combo.currentData()
            if not item_id:
                QMessageBox.warning(self, "Error", "Please select an item")
                return

            quantity = self.stockout_qty_spin.value()
            reason = self.reason_input.text().strip()

            if not reason:
                QMessageBox.warning(self, "Error", "Please enter reason")
                return

            success, message = self.inventory_controller.stock_out(item_id, quantity, reason)

            if success:
                QMessageBox.information(self, "Success", message)
                self.reason_input.clear()
                self.stockout_qty_spin.setValue(1)
                self.load_inventory()
                self.data_changed.emit()
            else:
                QMessageBox.warning(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 8px 10px;
                border: 2px solid #d1d5db;
                border-radius: 4px;
                font-size: 13px;
                background-color: #ffffff;
                color: #1f2937;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #3b82f6;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #1f2937;
                selection-background-color: #dbeafe;
                selection-color: #1e40af;
                border: 1px solid #d1d5db;
            }
        """

    @staticmethod
    def get_button_style(bg_color, hover_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    @staticmethod
    def get_table_style():
        return """
            QTableWidget {
                border: none;
                background-color: #ffffff;
                gridline-color: #e5e7eb;
            }
            QTableWidget::item {
                padding: 14px;
                color: #1f2937;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                color: #374151;
                padding: 14px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: 600;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1f2937;
            }
        """