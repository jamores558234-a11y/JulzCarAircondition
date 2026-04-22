"""Inventory management window"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QSpinBox, QDoubleSpinBox, QComboBox)
from PyQt6.QtCore import Qt
from controllers.inventory_controller import InventoryController
from utils.validators import validate_not_empty, validate_numeric


class InventoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.inventory_controller = InventoryController()
        self.init_ui()
        self.load_inventory()

    def init_ui(self):
        """Initialize inventory UI"""
        layout = QVBoxLayout()

        title = QLabel("Inventory Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

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
        layout.addWidget(QLabel("Inventory Status:"))
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Item Name', 'Available', 'Threshold', 'Status'])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def create_stock_in_section(self):
        """Create stock-in section"""
        from PyQt6.QtWidgets import QGroupBox

        group = QGroupBox("Stock-In")
        layout = QVBoxLayout()

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Item:"))
        self.stockin_item_combo = QComboBox()
        self.load_items_combo(self.stockin_item_combo)
        form_layout.addWidget(self.stockin_item_combo)

        form_layout.addWidget(QLabel("Quantity:"))
        self.stockin_qty_spin = QSpinBox()
        self.stockin_qty_spin.setMinimum(1)
        form_layout.addWidget(self.stockin_qty_spin)

        form_layout.addWidget(QLabel("Supplier:"))
        self.supplier_input = QLineEdit()
        form_layout.addWidget(self.supplier_input)

        form_layout.addWidget(QLabel("Total Cost:"))
        self.stockin_cost_spin = QDoubleSpinBox()
        self.stockin_cost_spin.setMinimum(0)
        form_layout.addWidget(self.stockin_cost_spin)

        layout.addLayout(form_layout)

        # Button
        stockin_btn = QPushButton("Stock-In")
        stockin_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px;")
        stockin_btn.clicked.connect(self.stock_in)
        layout.addWidget(stockin_btn)

        group.setLayout(layout)
        return group

    def create_stock_out_section(self):
        """Create stock-out section"""
        from PyQt6.QtWidgets import QGroupBox

        group = QGroupBox("Stock-Out")
        layout = QVBoxLayout()

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Item:"))
        self.stockout_item_combo = QComboBox()
        self.load_items_combo(self.stockout_item_combo)
        form_layout.addWidget(self.stockout_item_combo)

        form_layout.addWidget(QLabel("Quantity:"))
        self.stockout_qty_spin = QSpinBox()
        self.stockout_qty_spin.setMinimum(1)
        form_layout.addWidget(self.stockout_qty_spin)

        form_layout.addWidget(QLabel("Reason:"))
        self.reason_input = QLineEdit()
        form_layout.addWidget(self.reason_input)

        layout.addLayout(form_layout)

        # Button
        stockout_btn = QPushButton("Stock-Out")
        stockout_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 8px; border-radius: 4px;")
        stockout_btn.clicked.connect(self.stock_out)
        layout.addWidget(stockout_btn)

        group.setLayout(layout)
        return group

    def load_items_combo(self, combo):
        """Load items in combo"""
        items = self.inventory_controller.get_all_items()
        for item in items:
            combo.addItem(item['item_name'], item['item_id'])

    def load_inventory(self):
        """Load inventory from database"""
        items = self.inventory_controller.get_all_items()
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(str(item['item_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(item['item_name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['quantity_available'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item['minimum_threshold'])))

            # Status
            status = "Low Stock" if item['quantity_available'] < item['minimum_threshold'] else "OK"
            status_item = QTableWidgetItem(status)
            if status == "Low Stock":
                status_item.setBackground(__import__('PyQt6.QtGui', fromlist=['QColor']).QColor(255, 200, 200))
            self.table.setItem(row, 4, status_item)

    def stock_in(self):
        """Add stock"""
        item_id = self.stockin_item_combo.currentData()
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
            self.load_inventory()
        else:
            QMessageBox.warning(self, "Error", "Failed to add stock")

    def stock_out(self):
        """Remove stock"""
        item_id = self.stockout_item_combo.currentData()
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
        else:
            QMessageBox.warning(self, "Error", message)