
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QDialog)
from PyQt6.QtCore import Qt
from controllers.customer_controller import CustomerController
from utils.validators import validate_not_empty, validate_email, validate_phone


class CustomerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = CustomerController()
        self.init_ui()
        self.load_customers()

    def init_ui(self):
        """Initialize customer UI"""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Customer Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form layout
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setMaximumWidth(150)
        form_layout.addWidget(self.name_input)

        form_layout.addWidget(QLabel("Contact:"))
        self.contact_input = QLineEdit()
        self.contact_input.setMaximumWidth(150)
        form_layout.addWidget(self.contact_input)

        form_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setMaximumWidth(150)
        form_layout.addWidget(self.email_input)

        form_layout.addWidget(QLabel("Address:"))
        self.address_input = QLineEdit()
        self.address_input.setMaximumWidth(150)
        form_layout.addWidget(self.address_input)

        form_layout.addStretch()

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        add_btn = QPushButton("Add Customer")
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px;")
        add_btn.clicked.connect(self.add_customer)
        button_layout.addWidget(add_btn)

        update_btn = QPushButton("Update Customer")
        update_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px; border-radius: 4px;")
        update_btn.clicked.connect(self.update_customer)
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("Delete Customer")
        delete_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 8px; border-radius: 4px;")
        delete_btn.clicked.connect(self.delete_customer)
        button_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_customers)
        button_layout.addWidget(refresh_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Contact', 'Email', 'Address'])
        self.table.clicked.connect(self.on_row_clicked)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_customers(self):
        """Load customers from database"""
        customers = self.controller.get_all_customers()
        self.table.setRowCount(len(customers))

        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(str(customer['customer_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(customer['name']))
            self.table.setItem(row, 2, QTableWidgetItem(customer['contact']))
            self.table.setItem(row, 3, QTableWidgetItem(customer['email'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(customer['address'] or ''))

    def add_customer(self):
        """Add new customer"""
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not validate_not_empty(name, contact):
            QMessageBox.warning(self, "Error", "Please fill in name and contact")
            return

        if email and not validate_email(email):
            QMessageBox.warning(self, "Error", "Invalid email format")
            return

        if not validate_phone(contact):
            QMessageBox.warning(self, "Error", "Invalid contact number")
            return

        if self.controller.add_customer(name, contact, email, address):
            QMessageBox.information(self, "Success", "Customer added successfully")
            self.clear_inputs()
            self.load_customers()
        else:
            QMessageBox.warning(self, "Error", "Failed to add customer")

    def on_row_clicked(self):
        """Load selected customer data to form"""
        row = self.table.currentRow()
        if row >= 0:
            self.name_input.setText(self.table.item(row, 1).text())
            self.contact_input.setText(self.table.item(row, 2).text())
            self.email_input.setText(self.table.item(row, 3).text())
            self.address_input.setText(self.table.item(row, 4).text())

    def update_customer(self):
        """Update selected customer"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a customer")
            return

        customer_id = int(self.table.item(row, 0).text())
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not validate_not_empty(name, contact):
            QMessageBox.warning(self, "Error", "Please fill in name and contact")
            return

        if self.controller.update_customer(customer_id, name, contact, email, address):
            QMessageBox.information(self, "Success", "Customer updated successfully")
            self.clear_inputs()
            self.load_customers()
        else:
            QMessageBox.warning(self, "Error", "Failed to update customer")

    def delete_customer(self):
        """Delete selected customer"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a customer")
            return

        customer_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "Confirm", "Delete this customer?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.delete_customer(customer_id):
                QMessageBox.information(self, "Success", "Customer deleted successfully")
                self.clear_inputs()
                self.load_customers()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete customer")

    def clear_inputs(self):
        """Clear input fields"""
        self.name_input.clear()
        self.contact_input.clear()
        self.email_input.clear()
        self.address_input.clear()