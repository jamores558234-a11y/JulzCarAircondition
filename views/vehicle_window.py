"""Vehicle management window"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from controllers.vehicle_controller import VehicleController
from controllers.customer_controller import CustomerController
from utils.validators import validate_not_empty


class VehicleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.vehicle_controller = VehicleController()
        self.customer_controller = CustomerController()
        self.init_ui()
        self.load_vehicles()

    def init_ui(self):
        """Initialize vehicle UI"""
        layout = QVBoxLayout()

        title = QLabel("Vehicle Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Customer:"))
        self.customer_combo = QComboBox()
        self.customer_combo.setMaximumWidth(150)
        self.load_customers_combo()
        form_layout.addWidget(self.customer_combo)

        form_layout.addWidget(QLabel("Plate:"))
        self.plate_input = QLineEdit()
        self.plate_input.setMaximumWidth(120)
        self.plate_input.setPlaceholderText("ABC-1234")
        form_layout.addWidget(self.plate_input)

        form_layout.addWidget(QLabel("Model:"))
        self.model_input = QLineEdit()
        self.model_input.setMaximumWidth(150)
        form_layout.addWidget(self.model_input)

        form_layout.addWidget(QLabel("Type:"))
        self.type_input = QLineEdit()
        self.type_input.setMaximumWidth(100)
        form_layout.addWidget(self.type_input)

        form_layout.addWidget(QLabel("Year:"))
        self.year_input = QLineEdit()
        self.year_input.setMaximumWidth(80)
        form_layout.addWidget(self.year_input)

        form_layout.addWidget(QLabel("Color:"))
        self.color_input = QLineEdit()
        self.color_input.setMaximumWidth(100)
        form_layout.addWidget(self.color_input)

        form_layout.addStretch()
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        add_btn = QPushButton("Add Vehicle")
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px;")
        add_btn.clicked.connect(self.add_vehicle)
        button_layout.addWidget(add_btn)

        update_btn = QPushButton("Update Vehicle")
        update_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px; border-radius: 4px;")
        update_btn.clicked.connect(self.update_vehicle)
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("Delete Vehicle")
        delete_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 8px; border-radius: 4px;")
        delete_btn.clicked.connect(self.delete_vehicle)
        button_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_vehicles)
        button_layout.addWidget(refresh_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Customer', 'Plate', 'Model', 'Type', 'Year', 'Color', 'Customer ID'])
        self.table.setColumnHidden(7, True)  # Hide customer_id column
        self.table.clicked.connect(self.on_row_clicked)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_customers_combo(self):
        """Load customers in combo box"""
        customers = self.customer_controller.get_all_customers()
        for customer in customers:
            self.customer_combo.addItem(customer['name'], customer['customer_id'])

    def load_vehicles(self):
        """Load vehicles from database"""
        vehicles = self.vehicle_controller.get_all_vehicles()
        self.table.setRowCount(len(vehicles))

        for row, vehicle in enumerate(vehicles):
            self.table.setItem(row, 0, QTableWidgetItem(str(vehicle['vehicle_id'])))
            self.table.setItem(row, 1, QTableWidgetItem(vehicle['customer_name']))
            self.table.setItem(row, 2, QTableWidgetItem(vehicle['plate_number']))
            self.table.setItem(row, 3, QTableWidgetItem(vehicle['model']))
            self.table.setItem(row, 4, QTableWidgetItem(vehicle['type']))
            self.table.setItem(row, 5, QTableWidgetItem(str(vehicle['year'] or '')))
            self.table.setItem(row, 6, QTableWidgetItem(vehicle['color'] or ''))
            self.table.setItem(row, 7, QTableWidgetItem(str(vehicle['customer_id'])))

    def add_vehicle(self):
        """Add new vehicle"""
        customer_id = self.customer_combo.currentData()
        plate = self.plate_input.text().strip()
        model = self.model_input.text().strip()
        type_val = self.type_input.text().strip()
        year = self.year_input.text().strip()
        color = self.color_input.text().strip()

        if not validate_not_empty(plate, model, type_val):
            QMessageBox.warning(self, "Error", "Please fill in required fields")
            return

        try:
            year = int(year) if year else None
        except:
            QMessageBox.warning(self, "Error", "Invalid year")
            return

        if self.vehicle_controller.add_vehicle(customer_id, plate, model, type_val, year, color):
            QMessageBox.information(self, "Success", "Vehicle added successfully")
            self.clear_inputs()
            self.load_vehicles()
        else:
            QMessageBox.warning(self, "Error", "Failed to add vehicle")

    def on_row_clicked(self):
        """Load selected vehicle to form"""
        row = self.table.currentRow()
        if row >= 0:
            customer_id = int(self.table.item(row, 7).text())
            self.customer_combo.setCurrentIndex(self.customer_combo.findData(customer_id))
            self.plate_input.setText(self.table.item(row, 2).text())
            self.model_input.setText(self.table.item(row, 3).text())
            self.type_input.setText(self.table.item(row, 4).text())
            self.year_input.setText(self.table.item(row, 5).text())
            self.color_input.setText(self.table.item(row, 6).text())

    def update_vehicle(self):
        """Update selected vehicle"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a vehicle")
            return

        vehicle_id = int(self.table.item(row, 0).text())
        customer_id = self.customer_combo.currentData()
        plate = self.plate_input.text().strip()
        model = self.model_input.text().strip()
        type_val = self.type_input.text().strip()
        year = self.year_input.text().strip()
        color = self.color_input.text().strip()

        if not validate_not_empty(plate, model, type_val):
            QMessageBox.warning(self, "Error", "Please fill in required fields")
            return

        try:
            year = int(year) if year else None
        except:
            QMessageBox.warning(self, "Error", "Invalid year")
            return

        if self.vehicle_controller.update_vehicle(vehicle_id, customer_id, plate, model, type_val, year, color):
            QMessageBox.information(self, "Success", "Vehicle updated successfully")
            self.clear_inputs()
            self.load_vehicles()
        else:
            QMessageBox.warning(self, "Error", "Failed to update vehicle")

    def delete_vehicle(self):
        """Delete selected vehicle"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a vehicle")
            return

        vehicle_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "Confirm", "Delete this vehicle?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if self.vehicle_controller.delete_vehicle(vehicle_id):
                QMessageBox.information(self, "Success", "Vehicle deleted successfully")
                self.clear_inputs()
                self.load_vehicles()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete vehicle")

    def clear_inputs(self):
        """Clear input fields"""
        self.plate_input.clear()
        self.model_input.clear()
        self.type_input.clear()
        self.year_input.clear()
        self.color_input.clear()