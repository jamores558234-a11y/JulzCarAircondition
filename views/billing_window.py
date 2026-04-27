"""Billing management window - FIXED"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QTableWidget, QTableWidgetItem, QMessageBox, QDoubleSpinBox,
                             QComboBox, QFrame, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from controllers.billing_controller import BillingController
from controllers.service_controller import ServiceController
from database.connection import DatabaseConnection
from utils.helpers import format_currency


class BillingWindow(QWidget):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.billing_controller = BillingController()
        self.service_controller = ServiceController()
        self.db = DatabaseConnection()
        self.init_ui()
        try:
            self.load_billing()
        except Exception as e:
            print(f"Error loading billing: {e}")

    def init_ui(self):
        """Initialize billing UI"""
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

        title = QLabel("💰 Billing Management")
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

        form_layout.addWidget(QLabel("Service:"))
        self.service_combo = QComboBox()
        self.service_combo.setStyleSheet(self.get_input_style())
        self.service_combo.setMinimumHeight(42)
        try:
            self.load_services_combo()
        except:
            pass
        form_layout.addWidget(self.service_combo)

        form_layout.addWidget(QLabel("Labor Fee:"))
        self.labor_fee_spin = QDoubleSpinBox()
        self.labor_fee_spin.setMinimum(0)
        self.labor_fee_spin.setValue(500)
        self.labor_fee_spin.setStyleSheet(self.get_input_style())
        self.labor_fee_spin.setMinimumHeight(42)
        form_layout.addWidget(self.labor_fee_spin)

        form_layout.addStretch()
        layout.addWidget(form_frame)

        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        create_billing_btn = QPushButton("➕ Create Billing")
        create_billing_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
        create_billing_btn.setMinimumHeight(44)
        create_billing_btn.clicked.connect(self.create_billing)
        button_layout.addWidget(create_billing_btn)

        view_details_btn = QPushButton("👁️ View Details")
        view_details_btn.setStyleSheet(self.get_button_style("#3b82f6", "#2563eb"))
        view_details_btn.setMinimumHeight(44)
        view_details_btn.clicked.connect(self.view_billing_details)
        button_layout.addWidget(view_details_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style("#8b5cf6", "#7c3aed"))
        refresh_btn.setMinimumHeight(44)
        refresh_btn.clicked.connect(self.load_billing)
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
            ['ID', 'Service', 'Vehicle', 'Parts Cost', 'Labor Fee', 'Total', 'Status', 'Service ID'])
        self.table.setColumnHidden(7, True)
        self.table.clicked.connect(self.on_row_clicked)
        self.table.setStyleSheet(self.get_table_style())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        layout.addWidget(table_frame)
        self.setLayout(layout)

    def load_services_combo(self):
        """Load services in combo"""
        try:
            services = self.service_controller.get_all_services()
            if services:
                for service in services:
                    self.service_combo.addItem(
                        f"Service #{service.get('service_id', '')} - {service.get('plate_number', '')}",
                        service.get('service_id')
                    )
        except Exception as e:
            print(f"Error loading services: {e}")

    def load_billing(self):
        """Load billing records"""
        try:
            billings = self.billing_controller.get_all_billing()
            if billings is None:
                billings = []

            self.table.setRowCount(len(billings))

            for row, billing in enumerate(billings):
                try:
                    self.table.setItem(row, 0, QTableWidgetItem(str(billing.get('billing_id', ''))))
                    self.table.setItem(row, 1, QTableWidgetItem(str(billing.get('service_id', ''))))
                    self.table.setItem(row, 2, QTableWidgetItem(billing.get('plate_number', '')))
                    self.table.setItem(row, 3, QTableWidgetItem(format_currency(billing.get('parts_cost', 0))))
                    self.table.setItem(row, 4, QTableWidgetItem(format_currency(billing.get('labor_fee', 0))))
                    self.table.setItem(row, 5, QTableWidgetItem(format_currency(billing.get('total_amount', 0))))
                    self.table.setItem(row, 6, QTableWidgetItem(billing.get('status', '')))
                    self.table.setItem(row, 7, QTableWidgetItem(str(billing.get('service_id', ''))))
                except Exception as e:
                    print(f"Error loading billing row {row}: {e}")
        except Exception as e:
            print(f"Error loading billing: {e}")

    def create_billing(self):
        """Create billing"""
        try:
            service_id = self.service_combo.currentData()
            if not service_id:
                QMessageBox.warning(self, "Error", "Please select a service")
                return

            labor_fee = self.labor_fee_spin.value()

            query = "SELECT SUM(total_price) as total FROM service_parts WHERE service_id = %s"
            result = self.db.execute_query(query, (service_id,))
            parts_cost = float(result[0]['total']) if result and result[0]['total'] else 0.0

            if self.billing_controller.create_billing(service_id, parts_cost, labor_fee):
                QMessageBox.information(self, "Success", "Billing created successfully")
                self.load_billing()
                self.data_changed.emit()
            else:
                QMessageBox.warning(self, "Error", "Failed to create billing or billing already exists")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def on_row_clicked(self):
        """Load selected billing"""
        pass

    def view_billing_details(self):
        """View billing details"""
        try:
            row = self.table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Error", "Please select a billing")
                return

            billing_id = int(self.table.item(row, 0).text())
            billing = self.billing_controller.get_billing(billing_id)

            if billing:
                details = f"""
Billing ID: {billing.get('billing_id', 'N/A')}
Service ID: {billing.get('service_id', 'N/A')}
Parts Cost: {format_currency(billing.get('parts_cost', 0))}
Labor Fee: {format_currency(billing.get('labor_fee', 0))}
Total Amount: {format_currency(billing.get('total_amount', 0))}
Status: {billing.get('status', 'N/A')}
Created: {billing.get('created_at', 'N/A')}
                """
                QMessageBox.information(self, "Billing Details", details)
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