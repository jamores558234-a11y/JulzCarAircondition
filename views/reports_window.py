"""Reports window - FIXED"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QTableWidget, QTableWidgetItem, QComboBox, QFrame,
                             QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database.connection import DatabaseConnection
from utils.helpers import format_currency


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.init_ui()
        try:
            self.generate_report()
        except Exception as e:
            print(f"Error generating initial report: {e}")

    def init_ui(self):
        """Initialize reports UI"""
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

        title = QLabel("📈 Reports")
        title.setStyleSheet("color: #1f2937; font-size: 26px; font-weight: 700;")
        title_layout.addWidget(title)

        layout.addWidget(title_frame)

        # Report selection
        report_frame = QFrame()
        report_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        report_layout = QHBoxLayout(report_frame)

        report_layout.addWidget(QLabel("Select Report:"))
        self.report_combo = QComboBox()
        self.report_combo.setStyleSheet(self.get_input_style())
        self.report_combo.setMinimumHeight(42)
        self.report_combo.addItems([
            'Service History',
            'Inventory Status',
            'Payment Transactions',
            'Low Stock Items'
        ])
        self.report_combo.currentTextChanged.connect(self.generate_report)
        report_layout.addWidget(self.report_combo)

        report_layout.addStretch()
        layout.addWidget(report_frame)

        # Table section
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
        self.table.setStyleSheet(self.get_table_style())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_frame)
        self.setLayout(layout)

    def generate_report(self):
        """Generate selected report"""
        try:
            report_type = self.report_combo.currentText()

            if report_type == 'Service History':
                self.service_history_report()
            elif report_type == 'Inventory Status':
                self.inventory_status_report()
            elif report_type == 'Payment Transactions':
                self.payment_transactions_report()
            elif report_type == 'Low Stock Items':
                self.low_stock_report()
        except Exception as e:
            print(f"Error generating report: {e}")

    def service_history_report(self):
        """Service history report"""
        try:
            query = """
            SELECT s.service_id, v.plate_number, c.name, s.issue_complaint, 
                   s.status, s.created_at
            FROM services s
            JOIN vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN customers c ON v.customer_id = c.customer_id
            ORDER BY s.created_at DESC
            LIMIT 100
            """
            results = self.db.execute_query(query)

            if results is None:
                results = []

            self.table.setColumnCount(6)
            self.table.setHorizontalHeaderLabels(['Service ID', 'Vehicle', 'Customer', 'Issue', 'Status', 'Date'])
            self.table.setRowCount(len(results))

            for row, result in enumerate(results):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(result.get('service_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(result.get('plate_number', '')))
                    self.table.setItem(row, 2, QTableWidgetItem(result.get('name', '')))
                    self.table.setItem(row, 3, QTableWidgetItem(result.get('issue_complaint', '')[:50]))
                    self.table.setItem(row, 4, QTableWidgetItem(result.get('status', '')))
                    self.table.setItem(row, 5, QTableWidgetItem(str(result.get('created_at', ''))))
                except Exception as e:
                    print(f"Error loading row {row}: {e}")
        except Exception as e:
            print(f"Error generating service history report: {e}")

    def inventory_status_report(self):
        """Inventory status report"""
        try:
            query = """
            SELECT item_id, item_name, quantity_available, unit_price,
                   quantity_available * unit_price as total_value,
                   minimum_threshold
            FROM inventory
            ORDER BY item_name
            """
            results = self.db.execute_query(query)

            if results is None:
                results = []

            self.table.setColumnCount(6)
            self.table.setHorizontalHeaderLabels(['ID', 'Item', 'Quantity', 'Unit Price', 'Total Value', 'Threshold'])
            self.table.setRowCount(len(results))

            for row, result in enumerate(results):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(result.get('item_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(result.get('item_name', '')))
                    self.table.setItem(row, 2, QTableWidgetItem(str(result.get('quantity_available', ''))))
                    self.table.setItem(row, 3, QTableWidgetItem(format_currency(result.get('unit_price', 0))))
                    self.table.setItem(row, 4, QTableWidgetItem(format_currency(result.get('total_value', 0))))
                    self.table.setItem(row, 5, QTableWidgetItem(str(result.get('minimum_threshold', ''))))
                except Exception as e:
                    print(f"Error loading row {row}: {e}")
        except Exception as e:
            print(f"Error generating inventory report: {e}")

    def payment_transactions_report(self):
        """Payment transactions report"""
        try:
            query = """
            SELECT p.payment_id, b.billing_id, p.amount_paid, p.payment_method,
                   p.payment_date, b.total_amount, b.status
            FROM payments p
            JOIN billing b ON p.billing_id = b.billing_id
            ORDER BY p.payment_date DESC
            LIMIT 100
            """
            results = self.db.execute_query(query)

            if results is None:
                results = []

            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(
                ['Payment ID', 'Billing ID', 'Amount Paid', 'Method', 'Date', 'Total Amount', 'Status'])
            self.table.setRowCount(len(results))

            for row, result in enumerate(results):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(result.get('payment_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(str(result.get('billing_id', ''))))
                    self.table.setItem(row, 2, QTableWidgetItem(format_currency(result.get('amount_paid', 0))))
                    self.table.setItem(row, 3, QTableWidgetItem(result.get('payment_method', '')))
                    self.table.setItem(row, 4, QTableWidgetItem(str(result.get('payment_date', ''))))
                    self.table.setItem(row, 5, QTableWidgetItem(format_currency(result.get('total_amount', 0))))
                    self.table.setItem(row, 6, QTableWidgetItem(result.get('status', '')))
                except Exception as e:
                    print(f"Error loading row {row}: {e}")
        except Exception as e:
            print(f"Error generating payment report: {e}")

    def low_stock_report(self):
        """Low stock items report"""
        try:
            query = """
            SELECT item_id, item_name, quantity_available, minimum_threshold, unit_price
            FROM inventory
            WHERE quantity_available < minimum_threshold
            ORDER BY quantity_available ASC
            """
            results = self.db.execute_query(query)

            if results is None:
                results = []

            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(['ID', 'Item', 'Available', 'Threshold', 'Unit Price'])
            self.table.setRowCount(len(results))

            for row, result in enumerate(results):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(result.get('item_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(result.get('item_name', '')))
                    self.table.setItem(row, 2, QTableWidgetItem(str(result.get('quantity_available', ''))))
                    self.table.setItem(row, 3, QTableWidgetItem(str(result.get('minimum_threshold', ''))))
                    self.table.setItem(row, 4, QTableWidgetItem(format_currency(result.get('unit_price', 0))))
                except Exception as e:
                    print(f"Error loading row {row}: {e}")
        except Exception as e:
            print(f"Error generating low stock report: {e}")

    @staticmethod
    def get_input_style():
        return """
            QComboBox {
                padding: 10px 12px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                font-size: 13px;
                background-color: #ffffff;
                color: #1f2937;
            }
            QComboBox:focus {
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