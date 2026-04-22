"""Reports window"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QTableWidget, QTableWidgetItem, QComboBox)
from PyQt6.QtCore import Qt
from database.connection import DatabaseConnection
from utils.helpers import format_currency


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.init_ui()

    def init_ui(self):
        """Initialize reports UI"""
        layout = QVBoxLayout()

        title = QLabel("Reports")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Report selection
        report_layout = QHBoxLayout()

        report_layout.addWidget(QLabel("Select Report:"))
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            'Service History',
            'Inventory Status',
            'Payment Transactions',
            'Low Stock Items'
        ])
        self.report_combo.currentTextChanged.connect(self.generate_report)
        report_layout.addWidget(self.report_combo)

        report_layout.addStretch()
        layout.addLayout(report_layout)

        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Generate initial report
        self.generate_report()

    def generate_report(self):
        """Generate selected report"""
        report_type = self.report_combo.currentText()

        if report_type == 'Service History':
            self.service_history_report()
        elif report_type == 'Inventory Status':
            self.inventory_status_report()
        elif report_type == 'Payment Transactions':
            self.payment_transactions_report()
        elif report_type == 'Low Stock Items':
            self.low_stock_report()

    def service_history_report(self):
        """Service history report"""
        query = """
        SELECT s.service_id, v.plate_number, c.name, s.issue_complaint, 
               s.status, s.created_at
        FROM services s
        JOIN vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN customers c ON v.customer_id = c.customer_id
        ORDER BY s.created_at DESC
        """
        results = self.db.execute_query(query)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Service ID', 'Vehicle', 'Customer', 'Issue', 'Status', 'Date'])
        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(result['service_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(result['plate_number']))
            self.table.setItem(row, 2, QTableWidgetItem(result['name']))
            self.table.setItem(row, 3, QTableWidgetItem(result['issue_complaint']))
            self.table.setItem(row, 4, QTableWidgetItem(result['status']))
            self.table.setItem(row, 5, QTableWidgetItem(str(result['created_at'])))

    def inventory_status_report(self):
        """Inventory status report"""
        query = """
        SELECT item_id, item_name, quantity_available, unit_price,
               quantity_available * unit_price as total_value,
               minimum_threshold
        FROM inventory
        ORDER BY item_name
        """
        results = self.db.execute_query(query)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Item', 'Quantity', 'Unit Price', 'Total Value', 'Threshold'])
        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(result['item_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(result['item_name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(result['quantity_available'])))
            self.table.setItem(row, 3, QTableWidgetItem(format_currency(result['unit_price'])))
            self.table.setItem(row, 4, QTableWidgetItem(format_currency(result['total_value'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(result['minimum_threshold'])))

    def payment_transactions_report(self):
        """Payment transactions report"""
        query = """
        SELECT p.payment_id, b.billing_id, p.amount_paid, p.payment_method,
               p.payment_date, b.total_amount, b.status
        FROM payments p
        JOIN billing b ON p.billing_id = b.billing_id
        ORDER BY p.payment_date DESC
        """
        results = self.db.execute_query(query)

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['Payment ID', 'Billing ID', 'Amount Paid', 'Method', 'Date', 'Total Amount', 'Status'])
        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(result['payment_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(result['billing_id'])))
            self.table.setItem(row, 2, QTableWidgetItem(format_currency(result['amount_paid'])))
            self.table.setItem(row, 3, QTableWidgetItem(result['payment_method']))
            self.table.setItem(row, 4, QTableWidgetItem(str(result['payment_date'])))
            self.table.setItem(row, 5, QTableWidgetItem(format_currency(result['total_amount'])))
            self.table.setItem(row, 6, QTableWidgetItem(result['status']))

    def low_stock_report(self):
        """Low stock items report"""
        query = """
        SELECT item_id, item_name, quantity_available, minimum_threshold, unit_price
        FROM inventory
        WHERE quantity_available < minimum_threshold
        ORDER BY quantity_available ASC
        """
        results = self.db.execute_query(query)

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Item', 'Available', 'Threshold', 'Unit Price'])
        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(result['item_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(result['item_name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(result['quantity_available'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(result['minimum_threshold'])))
            self.table.setItem(row, 4, QTableWidgetItem(format_currency(result['unit_price'])))