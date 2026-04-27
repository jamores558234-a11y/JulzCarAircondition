"""Service management window - Updated for role-based access"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QTextEdit, QFrame, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from controllers.service_controller import ServiceController
from controllers.vehicle_controller import VehicleController
from database.connection import DatabaseConnection


class ServiceWindow(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, user=None):
        super().__init__()
        self.user = user or {}
        self.user_role = self.user.get('role', 'Staff')
        self.user_id = self.user.get('user_id')
        self.service_controller = ServiceController()
        self.vehicle_controller = VehicleController()
        self.db = DatabaseConnection()
        self.init_ui()
        try:
            self.load_services()
        except Exception as e:
            print(f"Error loading services: {e}")

    def init_ui(self):
        """Initialize service UI"""
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

        title_text = "🔧 My Services" if self.user_role == 'Mechanic' else "🔧 Service Management"
        title = QLabel(title_text)
        title.setStyleSheet("color: #1f2937; font-size: 26px; font-weight: 700;")
        title_layout.addWidget(title)

        layout.addWidget(title_frame)

        # Form section - Only show for non-mechanics
        if self.user_role != 'Mechanic':
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

            form_title = QLabel("Service Details")
            form_title.setStyleSheet("color: #374151; font-size: 15px; font-weight: 600; margin-bottom: 10px;")
            form_layout.addWidget(form_title)

            # Form Row 1
            form_row1 = QHBoxLayout()

            form_row1.addWidget(QLabel("Vehicle:"))
            self.vehicle_combo = QComboBox()
            self.vehicle_combo.setStyleSheet(self.get_input_style())
            self.vehicle_combo.setMinimumHeight(42)
            try:
                self.load_vehicles_combo()
            except:
                pass
            form_row1.addWidget(self.vehicle_combo)

            form_row1.addWidget(QLabel("Mechanic:"))
            self.mechanic_combo = QComboBox()
            self.mechanic_combo.setStyleSheet(self.get_input_style())
            self.mechanic_combo.setMinimumHeight(42)
            try:
                self.load_mechanics_combo()
            except:
                pass
            form_row1.addWidget(self.mechanic_combo)

            form_row1.addWidget(QLabel("Status:"))
            self.status_combo = QComboBox()
            self.status_combo.addItems(['Pending', 'Ongoing', 'Completed'])
            self.status_combo.setStyleSheet(self.get_input_style())
            self.status_combo.setMinimumHeight(42)
            form_row1.addWidget(self.status_combo)

            form_row1.addStretch()
            form_layout.addLayout(form_row1)

            # Issue complaint
            issue_label = QLabel("Issue/Complaint:")
            issue_label.setStyleSheet("color: #374151; font-weight: 600; font-size: 12px; margin-top: 10px;")
            form_layout.addWidget(issue_label)
            self.issue_input = QTextEdit()
            self.issue_input.setMaximumHeight(80)
            self.issue_input.setStyleSheet(self.get_input_style())
            form_layout.addWidget(self.issue_input)

            layout.addWidget(form_frame)

        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        if self.user_role != 'Mechanic':
            create_btn = QPushButton("➕ Create Service")
            create_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
            create_btn.setMinimumHeight(44)
            create_btn.clicked.connect(self.create_service)
            button_layout.addWidget(create_btn)

        update_status_btn = QPushButton("✏️ Update Status")
        update_status_btn.setStyleSheet(self.get_button_style("#3b82f6", "#2563eb"))
        update_status_btn.setMinimumHeight(44)
        update_status_btn.clicked.connect(self.update_status)
        button_layout.addWidget(update_status_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style("#8b5cf6", "#7c3aed"))
        refresh_btn.setMinimumHeight(44)
        refresh_btn.clicked.connect(self.load_services)
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
            ['ID', 'Vehicle', 'Customer', 'Mechanic', 'Issue', 'Status', 'Created', 'Vehicle ID'])
        self.table.setColumnHidden(7, True)
        self.table.clicked.connect(self.on_row_clicked)
        self.table.setStyleSheet(self.get_table_style())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_frame)
        self.setLayout(layout)

    def load_vehicles_combo(self):
        """Load vehicles in combo"""
        try:
            vehicles = self.vehicle_controller.get_all_vehicles()
            if vehicles:
                for vehicle in vehicles:
                    self.vehicle_combo.addItem(
                        f"{vehicle.get('plate_number', '')} - {vehicle.get('model', '')}",
                        vehicle.get('vehicle_id')
                    )
        except Exception as e:
            print(f"Error loading vehicles: {e}")

    def load_mechanics_combo(self):
        """Load mechanics in combo"""
        try:
            query = "SELECT user_id, full_name FROM users WHERE role = 'Mechanic'"
            mechanics = self.db.execute_query(query)
            if mechanics:
                for mechanic in mechanics:
                    self.mechanic_combo.addItem(mechanic.get('full_name', ''), mechanic.get('user_id'))
        except Exception as e:
            print(f"Error loading mechanics: {e}")

    def load_services(self):
        """Load services from database"""
        try:
            if self.user_role == 'Mechanic':
                # Mechanics only see their own services
                query = """
                SELECT s.*, v.plate_number, v.model, c.name as customer_name, u.full_name as mechanic_name 
                FROM services s
                JOIN vehicles v ON s.vehicle_id = v.vehicle_id
                JOIN customers c ON v.customer_id = c.customer_id
                LEFT JOIN users u ON s.mechanic_id = u.user_id
                WHERE s.mechanic_id = %s
                ORDER BY s.created_at DESC
                """
                services = self.db.execute_query(query, (self.user_id,))
            else:
                # Admins and staff see all services
                services = self.service_controller.get_all_services()

            if services is None:
                services = []

            self.table.setRowCount(len(services))

            for row, service in enumerate(services):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(service.get('service_id', ''))))
                    plate = service.get('plate_number', 'N/A')
                    model = service.get('model', 'N/A')
                    self.table.setItem(row, 1, QTableWidgetItem(f"{plate} - {model}"))
                    self.table.setItem(row, 2, QTableWidgetItem(service.get('customer_name', '')))
                    self.table.setItem(row, 3, QTableWidgetItem(service.get('mechanic_name', 'Unassigned')))
                    issue = service.get('issue_complaint', '')[:50]
                    self.table.setItem(row, 4, QTableWidgetItem(issue))
                    self.table.setItem(row, 5, QTableWidgetItem(service.get('status', '')))
                    self.table.setItem(row, 6, QTableWidgetItem(str(service.get('created_at', ''))))
                    self.table.setItem(row, 7, QTableWidgetItem(str(service.get('vehicle_id', ''))))
                except Exception as e:
                    print(f"Error loading row {row}: {e}")
        except Exception as e:
            print(f"Error loading services: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load services: {str(e)}")

    def create_service(self):
        """Create new service"""
        try:
            vehicle_id = self.vehicle_combo.currentData()
            if not vehicle_id:
                QMessageBox.warning(self, "Error", "Please select a vehicle")
                return

            mechanic_id = self.mechanic_combo.currentData()
            issue = self.issue_input.toPlainText().strip()

            if not issue:
                QMessageBox.warning(self, "Error", "Please enter issue complaint")
                return

            if self.service_controller.create_service(vehicle_id, mechanic_id, issue):
                QMessageBox.information(self, "Success", "Service created successfully")
                self.issue_input.clear()
                self.load_services()
                self.data_changed.emit()
            else:
                QMessageBox.warning(self, "Error", "Failed to create service")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def on_row_clicked(self):
        """Load selected service to form"""
        try:
            row = self.table.currentRow()
            if row >= 0 and self.user_role != 'Mechanic':
                vehicle_id = int(self.table.item(row, 7).text())
                status = self.table.item(row, 5).text()

                self.vehicle_combo.setCurrentIndex(self.vehicle_combo.findData(vehicle_id))
                self.status_combo.setCurrentText(status)
        except Exception as e:
            print(f"Error on row clicked: {e}")

    def update_status(self):
        """Update service status"""
        try:
            row = self.table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Selection Error", "Please select a service")
                return

            service_id = int(self.table.item(row, 0).text())

            # For mechanics, limit status changes
            if self.user_role == 'Mechanic':
                current_status = self.table.item(row, 5).text()
                if current_status == 'Pending':
                    new_status = 'Ongoing'
                elif current_status == 'Ongoing':
                    new_status = 'Completed'
                else:
                    QMessageBox.warning(self, "Error", "Service is already completed")
                    return
            else:
                new_status = self.status_combo.currentText()

            if self.service_controller.update_service_status(service_id, new_status):
                QMessageBox.information(self, "Success", "Service status updated successfully")
                self.load_services()
                self.data_changed.emit()
            else:
                QMessageBox.warning(self, "Error", "Cannot update status. Check workflow order.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QComboBox, QTextEdit {
                padding: 10px 12px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                font-size: 13px;
                background-color: #ffffff;
                color: #1f2937;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
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