"""Vehicle management window - Enhanced design"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QFrame, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from controllers.vehicle_controller import VehicleController
from controllers.customer_controller import CustomerController
from utils.validators import validate_not_empty


class VehicleWindow(QWidget):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.vehicle_controller = VehicleController()
        self.customer_controller = CustomerController()
        self.init_ui()
        try:
            self.load_vehicles()
        except Exception as e:
            print(f"Error loading vehicles: {e}")

    def init_ui(self):
        """Initialize vehicle UI"""
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

        title = QLabel("🚗 Vehicle Management")
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

        form_title = QLabel("Vehicle Details")
        form_title.setStyleSheet("color: #374151; font-size: 15px; font-weight: 600; margin-bottom: 10px;")
        form_layout.addWidget(form_title)

        # Customer selection
        cust_layout = QHBoxLayout()
        cust_label = QLabel("Customer")
        cust_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px;")
        cust_layout.addWidget(cust_label)
        self.customer_combo = QComboBox()
        self.customer_combo.setStyleSheet(self.get_input_style())
        self.customer_combo.setMinimumHeight(42)
        try:
            self.load_customers_combo()
        except:
            pass
        cust_layout.addWidget(self.customer_combo)
        cust_layout.addStretch()
        form_layout.addLayout(cust_layout)

        # Plate, Model, Type in row
        row1_layout = QHBoxLayout()

        plate_label = QLabel("Plate Number")
        plate_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px;")
        row1_layout.addWidget(plate_label)
        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("ABC-1234")
        self.plate_input.setStyleSheet(self.get_input_style())
        self.plate_input.setMinimumHeight(42)
        row1_layout.addWidget(self.plate_input)

        model_label = QLabel("Model")
        model_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px;")
        row1_layout.addWidget(model_label)
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Toyota Camry")
        self.model_input.setStyleSheet(self.get_input_style())
        self.model_input.setMinimumHeight(42)
        row1_layout.addWidget(self.model_input)

        type_label = QLabel("Type")
        type_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px;")
        row1_layout.addWidget(type_label)
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Sedan")
        self.type_input.setStyleSheet(self.get_input_style())
        self.type_input.setMinimumHeight(42)
        row1_layout.addWidget(self.type_input)

        form_layout.addLayout(row1_layout)

        # Year and Color in row
        row2_layout = QHBoxLayout()

        year_label = QLabel("Year")
        year_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px;")
        row2_layout.addWidget(year_label)
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("2020")
        self.year_input.setStyleSheet(self.get_input_style())
        self.year_input.setMinimumHeight(42)
        row2_layout.addWidget(self.year_input)

        color_label = QLabel("Color")
        color_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px;")
        row2_layout.addWidget(color_label)
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Silver")
        self.color_input.setStyleSheet(self.get_input_style())
        self.color_input.setMinimumHeight(42)
        row2_layout.addWidget(self.color_input)

        row2_layout.addStretch()
        form_layout.addLayout(row2_layout)

        layout.addWidget(form_frame)

        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        add_btn = QPushButton("➕ Add Vehicle")
        add_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
        add_btn.setMinimumHeight(44)
        add_btn.clicked.connect(self.add_vehicle)
        button_layout.addWidget(add_btn)

        update_btn = QPushButton("✏️ Update")
        update_btn.setStyleSheet(self.get_button_style("#3b82f6", "#2563eb"))
        update_btn.setMinimumHeight(44)
        update_btn.clicked.connect(self.update_vehicle)
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet(self.get_button_style("#ef4444", "#dc2626"))
        delete_btn.setMinimumHeight(44)
        delete_btn.clicked.connect(self.delete_vehicle)
        button_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style("#8b5cf6", "#7c3aed"))
        refresh_btn.setMinimumHeight(44)
        refresh_btn.clicked.connect(self.load_vehicles)
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
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Customer', 'Plate', 'Model', 'Type', 'Year', 'Color', 'Cust ID'])
        self.table.setColumnHidden(7, True)
        self.table.clicked.connect(self.on_row_clicked)
        self.table.setStyleSheet(self.get_table_style())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_frame)
        self.setLayout(layout)

    def load_customers_combo(self):
        """Load customers in combo box"""
        try:
            customers = self.customer_controller.get_all_customers()
            if customers:
                for customer in customers:
                    self.customer_combo.addItem(customer['name'], customer['customer_id'])
        except Exception as e:
            print(f"Error loading customers: {e}")

    def load_vehicles(self):
        """Load vehicles from database"""
        try:
            vehicles = self.vehicle_controller.get_all_vehicles()
            if vehicles is None:
                vehicles = []

            self.table.setRowCount(len(vehicles))

            for row, vehicle in enumerate(vehicles):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(vehicle.get('vehicle_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(vehicle.get('customer_name', '')))
                    self.table.setItem(row, 2, QTableWidgetItem(vehicle.get('plate_number', '')))
                    self.table.setItem(row, 3, QTableWidgetItem(vehicle.get('model', '')))
                    self.table.setItem(row, 4, QTableWidgetItem(vehicle.get('type', '')))
                    self.table.setItem(row, 5, QTableWidgetItem(str(vehicle.get('year', ''))))
                    self.table.setItem(row, 6, QTableWidgetItem(vehicle.get('color', '')))
                    self.table.setItem(row, 7, QTableWidgetItem(str(vehicle.get('customer_id', ''))))
                except Exception as e:
                    print(f"Error loading row {row}: {e}")
        except Exception as e:
            print(f"Error loading vehicles: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load vehicles: {str(e)}")

    def add_vehicle(self):
        """Add new vehicle"""
        try:
            customer_id = self.customer_combo.currentData()
            if not customer_id:
                QMessageBox.warning(self, "Error", "Please select a customer")
                return

            plate = self.plate_input.text().strip()
            model = self.model_input.text().strip()
            type_val = self.type_input.text().strip()
            year = self.year_input.text().strip()
            color = self.color_input.text().strip()

            if not validate_not_empty(plate, model, type_val):
                QMessageBox.warning(self, "Validation Error", "Please fill in plate, model, and type")
                return

            try:
                year = int(year) if year else None
            except:
                QMessageBox.warning(self, "Error", "Invalid year format")
                return

            if self.vehicle_controller.add_vehicle(customer_id, plate, model, type_val, year, color):
                QMessageBox.information(self, "Success", "Vehicle added successfully")
                self.clear_inputs()
                self.load_vehicles()
            else:
                QMessageBox.warning(self, "Error", "Failed to add vehicle")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def on_row_clicked(self):
        """Load selected vehicle to form"""
        try:
            row = self.table.currentRow()
            if row >= 0:
                customer_id = int(self.table.item(row, 7).text())
                self.customer_combo.setCurrentIndex(self.customer_combo.findData(customer_id))
                self.plate_input.setText(self.table.item(row, 2).text())
                self.model_input.setText(self.table.item(row, 3).text())
                self.type_input.setText(self.table.item(row, 4).text())
                self.year_input.setText(self.table.item(row, 5).text())
                self.color_input.setText(self.table.item(row, 6).text())
        except Exception as e:
            print(f"Error on row clicked: {e}")

    def update_vehicle(self):
        """Update selected vehicle"""
        try:
            row = self.table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Selection Error", "Please select a vehicle")
                return

            vehicle_id = int(self.table.item(row, 0).text())
            customer_id = self.customer_combo.currentData()
            plate = self.plate_input.text().strip()
            model = self.model_input.text().strip()
            type_val = self.type_input.text().strip()
            year = self.year_input.text().strip()
            color = self.color_input.text().strip()

            if not validate_not_empty(plate, model, type_val):
                QMessageBox.warning(self, "Validation Error", "Please fill in required fields")
                return

            try:
                year = int(year) if year else None
            except:
                QMessageBox.warning(self, "Error", "Invalid year format")
                return

            if self.vehicle_controller.update_vehicle(vehicle_id, customer_id, plate, model, type_val, year, color):
                QMessageBox.information(self, "Success", "Vehicle updated successfully")
                self.clear_inputs()
                self.load_vehicles()
            else:
                QMessageBox.warning(self, "Error", "Failed to update vehicle")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_vehicle(self):
        """Delete selected vehicle"""
        try:
            row = self.table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Selection Error", "Please select a vehicle")
                return

            vehicle_id = int(self.table.item(row, 0).text())

            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                "Are you sure you want to delete this vehicle?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.vehicle_controller.delete_vehicle(vehicle_id):
                    QMessageBox.information(self, "Success", "Vehicle deleted successfully")
                    self.clear_inputs()
                    self.load_vehicles()
                    self.data_changed.emit()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete vehicle")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_inputs(self):
        """Clear input fields"""
        self.plate_input.clear()
        self.model_input.clear()
        self.type_input.clear()
        self.year_input.clear()
        self.color_input.clear()

    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QComboBox {
                padding: 10px 12px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                font-size: 13px;
                background-color: #ffffff;
                color: #1f2937;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3b82f6;
                background-color: #ffffff;
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