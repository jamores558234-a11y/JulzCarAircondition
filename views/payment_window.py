"""Payment management window - FIXED"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QTableWidget, QTableWidgetItem, QMessageBox, QDoubleSpinBox,
                             QComboBox, QLineEdit, QFrame, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from controllers.payment_controller import PaymentController
from controllers.billing_controller import BillingController
from database.connection import DatabaseConnection
from utils.helpers import format_currency


class PaymentWindow(QWidget):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.payment_controller = PaymentController()
        self.billing_controller = BillingController()
        self.db = DatabaseConnection()
        self.init_ui()
        try:
            self.load_payments()
        except Exception as e:
            print(f"Error loading payments: {e}")

    def init_ui(self):
        """Initialize payment UI"""
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

        title = QLabel("💳 Payment Management")
        title.setStyleSheet("color: #1f2937; font-size: 26px; font-weight: 700;")
        title_layout.addWidget(title)

        layout.addWidget(title_frame)

        # Form section
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        form_layout = QHBoxLayout(form_frame)

        form_layout.addWidget(QLabel("Billing:"))
        self.billing_combo = QComboBox()
        self.billing_combo.setStyleSheet(self.get_input_style())
        self.billing_combo.setMinimumHeight(42)
        try:
            self.load_billing_combo()
        except:
            pass
        form_layout.addWidget(self.billing_combo)

        form_layout.addWidget(QLabel("Amount:"))
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setMinimum(0)
        self.amount_spin.setStyleSheet(self.get_input_style())
        self.amount_spin.setMinimumHeight(42)
        form_layout.addWidget(self.amount_spin)

        form_layout.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(['Cash', 'Check', 'Credit Card', 'Bank Transfer'])
        self.method_combo.setStyleSheet(self.get_input_style())
        self.method_combo.setMinimumHeight(42)
        form_layout.addWidget(self.method_combo)

        form_layout.addWidget(QLabel("Notes:"))
        self.notes_input = QLineEdit()
        self.notes_input.setStyleSheet(self.get_input_style())
        self.notes_input.setMinimumHeight(42)
        form_layout.addWidget(self.notes_input)

        form_layout.addStretch()
        layout.addWidget(form_frame)

        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        record_btn = QPushButton("💾 Record Payment")
        record_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
        record_btn.setMinimumHeight(44)
        record_btn.clicked.connect(self.record_payment)
        button_layout.addWidget(record_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style("#8b5cf6", "#7c3aed"))
        refresh_btn.setMinimumHeight(44)
        refresh_btn.clicked.connect(self.load_payments)
        button_layout.addWidget(refresh_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Billing ID', 'Amount Paid', 'Method', 'Date', 'Notes'])
        self.table.setStyleSheet(self.get_table_style())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_frame)
        self.setLayout(layout)

    def load_billing_combo(self):
        """Load pending billings"""
        try:
            billings = self.billing_controller.get_all_billing()
            if billings:
                for billing in billings:
                    if billing.get('status') != 'Paid':
                        self.billing_combo.addItem(
                            f"Billing #{billing.get('billing_id', '')} - {format_currency(billing.get('total_amount', 0))}",
                            billing.get('billing_id')
                        )
        except Exception as e:
            print(f"Error loading billing: {e}")

    def load_payments(self):
        """Load payments"""
        try:
            query = "SELECT * FROM payments ORDER BY payment_date DESC LIMIT 100"
            payments = self.db.execute_query(query)

            if payments is None:
                payments = []

            self.table.setRowCount(len(payments))

            for row, payment in enumerate(payments):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(payment.get('payment_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(str(payment.get('billing_id', ''))))
                    self.table.setItem(row, 2, QTableWidgetItem(format_currency(payment.get('amount_paid', 0))))
                    self.table.setItem(row, 3, QTableWidgetItem(payment.get('payment_method', '')))
                    self.table.setItem(row, 4, QTableWidgetItem(str(payment.get('payment_date', ''))))
                    self.table.setItem(row, 5, QTableWidgetItem(payment.get('notes', '') or ''))
                except Exception as e:
                    print(f"Error loading payment row {row}: {e}")
        except Exception as e:
            print(f"Error loading payments: {e}")

    def record_payment(self):
        """Record payment"""
        try:
            billing_id = self.billing_combo.currentData()
            if not billing_id:
                QMessageBox.warning(self, "Error", "Please select a billing")
                return

            amount = self.amount_spin.value()
            method = self.method_combo.currentText()
            notes = self.notes_input.text().strip()

            if amount <= 0:
                QMessageBox.warning(self, "Error", "Please enter valid amount")
                return

            if self.payment_controller.record_payment(billing_id, amount, method, notes):
                QMessageBox.information(self, "Success", "Payment recorded successfully")
                self.amount_spin.setValue(0)
                self.notes_input.clear()
                self.load_payments()
                self.data_changed.emit()
                self.load_billing_combo()
            else:
                QMessageBox.warning(self, "Error", "Failed to record payment")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QComboBox, QDoubleSpinBox {
                padding: 10px 12px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                font-size: 13px;
                background-color: #ffffff;
                color: #1f2937;
            }
            QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
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
                border-radius: 6px;
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