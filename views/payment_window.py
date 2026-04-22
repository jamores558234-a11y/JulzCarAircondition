"""Payment management window"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QTableWidget, QTableWidgetItem, QMessageBox, QDoubleSpinBox,
                             QComboBox, QLineEdit)
from PyQt6.QtCore import Qt
from controllers.payment_controller import PaymentController
from controllers.billing_controller import BillingController
from utils.helpers import format_currency


class PaymentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.payment_controller = PaymentController()
        self.billing_controller = BillingController()
        self.init_ui()
        self.load_payments()

    def init_ui(self):
        """Initialize payment UI"""
        layout = QVBoxLayout()

        title = QLabel("Payment Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Billing:"))
        self.billing_combo = QComboBox()
        self.billing_combo.setMaximumWidth(150)
        self.load_billing_combo()
        form_layout.addWidget(self.billing_combo)

        form_layout.addWidget(QLabel("Amount:"))
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setMinimum(0)
        form_layout.addWidget(self.amount_spin)

        form_layout.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(['Cash', 'Check', 'Credit Card', 'Bank Transfer'])
        form_layout.addWidget(self.method_combo)

        form_layout.addWidget(QLabel("Notes:"))
        self.notes_input = QLineEdit()
        form_layout.addWidget(self.notes_input)

        form_layout.addStretch()
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        record_btn = QPushButton("Record Payment")
        record_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px;")
        record_btn.clicked.connect(self.record_payment)
        button_layout.addWidget(record_btn)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_payments)
        button_layout.addWidget(refresh_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Billing ID', 'Amount Paid', 'Method', 'Date', 'Notes'])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_billing_combo(self):
        """Load pending billings"""
        billings = self.billing_controller.get_all_billing()
        for billing in billings:
            if billing['status'] != 'Paid':
                self.billing_combo.addItem(
                    f"Billing #{billing['billing_id']} - {format_currency(billing['total_amount'])}",
                    billing['billing_id']
                )

    def load_payments(self):
        """Load payments"""
        query = "SELECT * FROM payments ORDER BY payment_date DESC"
        from database.connection import DatabaseConnection
        db = DatabaseConnection()
        payments = db.execute_query(query)

        self.table.setRowCount(len(payments))

        for row, payment in enumerate(payments):
            self.table.setItem(row, 0, QTableWidgetItem(str(payment['payment_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(payment['billing_id'])))
            self.table.setItem(row, 2, QTableWidgetItem(format_currency(payment['amount_paid'])))
            self.table.setItem(row, 3, QTableWidgetItem(payment['payment_method']))
            self.table.setItem(row, 4, QTableWidgetItem(str(payment['payment_date'])))
            self.table.setItem(row, 5, QTableWidgetItem(payment['notes'] or ''))

    def record_payment(self):
        """Record payment"""
        billing_id = self.billing_combo.currentData()
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
            self.load_billing_combo()
        else:
            QMessageBox.warning(self, "Error", "Failed to record payment")