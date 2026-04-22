"""Service management window"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QTextEdit)
from PyQt6.QtCore import Qt
from controllers.service_controller import ServiceController
from controllers.vehicle_controller import VehicleController
from database.connection import DatabaseConnection


class ServiceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.service_controller = ServiceController()
        self.vehicle_controller = VehicleController()
        self.db = DatabaseConnection()
        self.init_ui()
        self.load_services()

    def init_ui(self):
        """Initialize service UI"""
        layout = QVBoxLayout()

        title = QLabel("Service Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Vehicle:"))
        self.vehicle_combo = QComboBox()
        self.vehicle_combo.setMaximumWidth(150)
        self.load_vehicles_combo()
        form_layout.addWidget(self.vehicle_combo)

        form_layout.addWidget(QLabel("Mechanic:"))
        self.mechanic_combo = QComboBox()
        self.mechanic_combo.setMaximumWidth(150)
        self.load_mechanics_combo()
        form_layout.addWidget(self.mechanic_combo)

        form_layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(['Pending', 'Ongoing', 'Completed'])
        self.status_combo.setMaximumWidth(120)
        form_layout.addWidget(self.status_combo)

        form_layout.addStretch()
        layout.addLayout(form_layout)

        # Issue complaint
        layout.addWidget(QLabel("Issue/Complaint:"))
        self.issue_input = QTextEdit()
        self.issue_input.setMaximumHeight(80)
        layout.addWidget(self.issue_input)

        # Buttons
        button_layout = QHBoxLayout()

        create_btn = QPushButton("Create Service")
        create_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px;")
        create_btn.clicked.connect(self.create_service)
        button_layout.addWidget(create_btn)

        update_status_btn = QPushButton("Update Status")
        update_status_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px; border-radius: 4px;")
        update_status_btn.clicked.connect(self.update_status)
        button_layout.addWidget(update_status_btn)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_services)
        button_layout.addWidget(refresh_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Vehicle', 'Customer', 'Mechanic', 'Issue', 'Status', 'Created', 'Vehicle ID'])
        self.table.setColumnHidden(7, True)
        self.table.clicked.connect(self.on_row_clicked)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_vehicles_combo(self):
        """Load vehicles in combo"""
        vehicles = self.vehicle_controller.get_all_vehicles()
        for vehicle in vehicles:
            self.vehicle_combo.addItem(f"{vehicle['plate_number']} - {vehicle['model']}", vehicle['vehicle_id'])

    def load_mechanics_combo(self):
        """Load mechanics in combo"""
        query = "SELECT user_id, full_name FROM users WHERE role = 'Mechanic'"
        mechanics = self.db.execute_query(query)
        if mechanics:
            for mechanic in mechanics:
                self.mechanic_combo.addItem(mechanic['full_name'], mechanic['user_id'])

    def load_services(self):
        """Load services from database"""
        services = self.service_controller.get_all_services()
        self.table.setRowCount(len(services))

        for row, service in enumerate(services):
            self.table.setItem(row, 0, QTableWidgetItem(str(service['service_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(f"{service['plate_number']} - {service['model']}"))
            self.table.setItem(row, 2, QTableWidgetItem(service['customer_name']))
            self.table.setItem(row, 3, QTableWidgetItem(service['mechanic_name'] or 'Unassigned'))
            self.table.setItem(row, 4, QTableWidgetItem(service['issue_complaint'][:50]))

            status_item = QTableWidgetItem(service['status'])
            self.table.setItem(row, 5, status_item)

            self.table.setItem(row, 6, QTableWidgetItem(str(service['created_at'])))
            self.table.setItem(row, 7, QTableWidgetItem(str(service['vehicle_id'])))

    def create_service(self):
        """Create new service"""
        vehicle_id = self.vehicle_combo.currentData()
        mechanic_id = self.mechanic_combo.currentData()
        issue = self.issue_input.toPlainText().strip()

        if not issue:
            QMessageBox.warning(self, "Error", "Please enter issue complaint")
            return

        if self.service_controller.create_service(vehicle_id, mechanic_id, issue):
            QMessageBox.information(self, "Success", "Service created successfully")
            self.issue_input.clear()
            self.load_services()
        else:
            QMessageBox.warning(self, "Error", "Failed to create service")

    def on_row_clicked(self):
        """Load selected service to form"""
        row = self.table.currentRow()
        if row >= 0:
            vehicle_id = int(self.table.item(row, 7).text())
            status = self.table.item(row, 5).text()

            self.vehicle_combo.setCurrentIndex(self.vehicle_combo.findData(vehicle_id))
            self.status_combo.setCurrentText(status)

    def update_status(self):
        """Update service status"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a service")
            return

        service_id = int(self.table.item(row, 0).text())
        new_status = self.status_combo.currentText()

        if self.service_controller.update_service_status(service_id, new_status):
            QMessageBox.information(self, "Success", "Service status updated successfully")
            self.load_services()
        else:
            QMessageBox.warning(self, "Error", "Cannot update status. Ensure proper workflow order.")