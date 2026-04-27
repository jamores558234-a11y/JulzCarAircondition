"""Customer management window - Enhanced formal design"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QFrame, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from controllers.customer_controller import CustomerController
from utils.validators import validate_not_empty, validate_email, validate_phone


class CustomerWindow(QWidget):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.controller = CustomerController()
        self.init_ui()
        self.load_customers()

    def init_ui(self):
        """Initialize customer UI with formal design"""
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
                border-radius: 0px;
                padding: 15px 0px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(15, 10, 15, 10)

        title = QLabel("👥 Customer Management")
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
        form_layout = QVBoxLayout(form_frame)

        # Form title
        form_title = QLabel("Customer Details")
        form_title.setStyleSheet("color: #374151; font-size: 15px; font-weight: 600; margin-bottom: 10px;")
        form_layout.addWidget(form_title)

        # Input fields in grid
        input_layout = QVBoxLayout()

        # Name
        name_label = QLabel("Full Name")
        name_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px;")
        input_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter customer name")
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(42)
        input_layout.addWidget(self.name_input)

        # Row 2: Contact and Email
        row2_layout = QHBoxLayout()

        contact_label = QLabel("Contact Number")
        contact_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px; margin-top: 5px;")
        row2_layout.addWidget(contact_label)
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Enter contact number")
        self.contact_input.setStyleSheet(self.get_input_style())
        self.contact_input.setMinimumHeight(42)
        row2_layout.addWidget(self.contact_input)

        email_label = QLabel("Email Address")
        email_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px; margin-top: 5px;")
        row2_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setMinimumHeight(42)
        row2_layout.addWidget(self.email_input)

        input_layout.addLayout(row2_layout)

        # Address
        address_label = QLabel("Address")
        address_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px; margin-top: 5px;")
        input_layout.addWidget(address_label)
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter customer address")
        self.address_input.setStyleSheet(self.get_input_style())
        self.address_input.setMinimumHeight(42)
        input_layout.addWidget(self.address_input)

        form_layout.addLayout(input_layout)
        layout.addWidget(form_frame)

        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        add_btn = QPushButton("➕ Add Customer")
        add_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
        add_btn.setMinimumHeight(44)
        add_btn.clicked.connect(self.add_customer)
        button_layout.addWidget(add_btn)

        update_btn = QPushButton("✏️ Update")
        update_btn.setStyleSheet(self.get_button_style("#3b82f6", "#2563eb"))
        update_btn.setMinimumHeight(44)
        update_btn.clicked.connect(self.update_customer)
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet(self.get_button_style("#ef4444", "#dc2626"))
        delete_btn.setMinimumHeight(44)
        delete_btn.clicked.connect(self.delete_customer)
        button_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style("#8b5cf6", "#7c3aed"))
        refresh_btn.setMinimumHeight(44)
        refresh_btn.clicked.connect(self.load_customers)
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

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Contact', 'Email', 'Address'])
        self.table.clicked.connect(self.on_row_clicked)
        self.table.setStyleSheet(self.get_table_style())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_frame)
        self.setLayout(layout)

    def load_customers(self):
        """Load customers from database"""
        try:
            customers = self.controller.get_all_customers()
            self.table.setRowCount(len(customers))

            for row, customer in enumerate(customers):
                self.table.setItem(row, 0, QTableWidgetItem(str(customer['customer_id'])))
                self.table.setItem(row, 1, QTableWidgetItem(customer['name']))
                self.table.setItem(row, 2, QTableWidgetItem(customer['contact']))
                self.table.setItem(row, 3, QTableWidgetItem(customer['email'] or ''))
                self.table.setItem(row, 4, QTableWidgetItem(customer['address'] or ''))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load customers: {e}")

    def add_customer(self):
        """Add new customer"""
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not validate_not_empty(name, contact):
            QMessageBox.warning(self, "Validation Error", "Please fill in name and contact")
            return

        if email and not validate_email(email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format")
            return

        if not validate_phone(contact):
            QMessageBox.warning(self, "Validation Error", "Invalid contact number")
            return

        if self.controller.add_customer(name, contact, email, address):
            QMessageBox.information(self, "Success", "Customer added successfully")
            self.clear_inputs()
            self.load_customers()
            self.data_changed.emit()
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
            QMessageBox.warning(self, "Selection Error", "Please select a customer to update")
            return

        customer_id = int(self.table.item(row, 0).text())
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not validate_not_empty(name, contact):
            QMessageBox.warning(self, "Validation Error", "Please fill in name and contact")
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
            QMessageBox.warning(self, "Selection Error", "Please select a customer to delete")
            return

        customer_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this customer?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.delete_customer(customer_id):
                QMessageBox.information(self, "Success", "Customer deleted successfully")
                self.clear_inputs()
                self.load_customers()
                self.data_changed.emit()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete customer")

    def clear_inputs(self):
        """Clear input fields"""
        self.name_input.clear()
        self.contact_input.clear()
        self.email_input.clear()
        self.address_input.clear()

    @staticmethod
    def get_input_style():
        return """
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                font-size: 13px;
                background-color: #ffffff;
                color: #1f2937;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                background-color: #ffffff;
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