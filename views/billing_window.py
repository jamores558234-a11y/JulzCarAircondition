"""Billing management window"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QTableWidget, QTableWidgetItem, QMessageBox, QDoubleSpinBox,
                             QComboBox, QDialog, QTextEdit)
from PyQt6.QtCore import Qt
from controllers.billing_controller import BillingController
from controllers.service_controller import ServiceController
from database.connection import DatabaseConnection
from utils.helpers import format_currency


class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.billing_controller = BillingController()
        self.service_controller = ServiceController()
        self.db = DatabaseConnection()
        self.init_ui()
        self.load_billing()

    def init_ui(self):
        """Initialize billing UI"""
        layout = QVBoxLayout()

        title = QLabel("Billing Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Service:"))
        self.service_combo = QComboBox()
        self.service_combo.setMaximumWidth(150)
        self.load_services_combo()
        form_layout.addWidget(self.service_combo)

        form_layout.addWidget(QLabel("Labor Fee:"))
        self.labor_fee_spin = QDoubleSpinBox()
        self.labor_fee_spin.setMinimum(0)
        self.labor_fee_spin.setValue(500)
        form_layout.addWidget(self.labor_fee_spin)

        form_layout.addStretch()
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        create_billing_btn = QPushButton("Create Billing")
        create_billing_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px;")
        create_billing_btn.clicked.connect(self.create_billing)
        button_layout.addWidget(create_billing_btn)

        view_details_btn = QPushButton("View Details")
        view_details_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px; border-radius: 4px;")
        view_details_btn.clicked.connect(self.view_billing_details)
        button_layout.addWidget(view_details_btn)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_billing)
        button_layout.addWidget(refresh_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Service', 'Vehicle', 'Parts Cost', 'Labor Fee', 'Total', 'Status', 'Service ID'])
        self.table.setColumnHidden(7, True)
        self.table.clicked.connect(self.on_row_clicked)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_services_combo(self):
        """Load services in combo"""
        services = self.service_controller.get_all_services()
        for service in services:
            self.service_combo.addItem(f"Service #{service['service_id']} - {service['plate_number']}",
                                       service['service_id'])

    def load_billing(self):
        """Load billing records"""
        billings = self.billing_controller.get_all_billing()
        self.table.setRowCount(len(billings))

        for row, billing in enumerate(billings):
            self.table.setItem(row, 0, QTableWidgetItem(str(billing['billing_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(billing['service_id'])))
            self.table.setItem(row, 2, QTableWidgetItem(billing['plate_number']))
            self.table.setItem(row, 3, QTableWidgetItem(format_currency(billing['parts_cost'])))
            self.table.setItem(row, 4, QTableWidgetItem(format_currency(billing['labor_fee'])))
            self.table.setItem(row, 5, QTableWidgetItem(format_currency(billing['total_amount'])))

            status_item = QTableWidgetItem(billing['status'])
            self.table.setItem(row, 6, status_item)
            self.table.setItem(row, 7, QTableWidgetItem(str(billing['service_id'])))

    def create_billing(self):
        """Create billing"""
        service_id = self.service_combo.currentData()
        labor_fee = self.labor_fee_spin.value()

        # Calculate parts cost
        query = """SELECT SUM(total_price) as total FROM service_parts WHERE service_id = %s"""
        result = self.db.execute_query(query, (service_id,))
        parts_cost = result[0]['total'] if result and result[0]['total'] else 0

        if self.billing_controller.create_billing(service_id, parts_cost, labor_fee):
            QMessageBox.information(self, "Success", "Billing created successfully")
            self.load_billing()
        else:
            QMessageBox.warning(self, "Error", "Failed to create billing or billing already exists")

    def on_row_clicked(self):
        """Load selected billing"""
        pass

    def view_billing_details(self):
        """View billing details"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a billing")
            return

        billing_id = int(self.table.item(row, 0).text())
        billing = self.billing_controller.get_billing(billing_id)

        if billing:
            details = f"""
Billing ID: {billing['billing_id']}
Service ID: {billing['service_id']}
Parts Cost: {format_currency(billing['parts_cost'])}
Labor Fee: {format_currency(billing['labor_fee'])}
Total Amount: {format_currency(billing['total_amount'])}
Status: {billing['status']}
Created: {billing['created_at']}
            """
            QMessageBox.information(self, "Billing Details", details)