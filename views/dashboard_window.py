"""Dashboard window"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

from views.customer_window import CustomerWindow
from views.vehicle_window import VehicleWindow
from views.service_window import ServiceWindow
from views.inventory_window import InventoryWindow
from views.billing_window import BillingWindow
from views.payment_window import PaymentWindow
from views.reports_window import ReportsWindow


class DashboardWindow(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()
        self.setWindowTitle("Julz Car AC Service Management System")
        self.setGeometry(0, 0, 1400, 800)

    def init_ui(self):
        """Initialize dashboard UI"""
        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Content area
        self.stacked_widget = QStackedWidget()
        self.init_pages()
        main_layout.addWidget(self.stacked_widget)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = QWidget()
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 12px;
                text-align: left;
                font-weight: bold;
                border-left: 4px solid #34495e;
            }
            QPushButton:hover {
                background-color: #1abc9c;
                border-left: 4px solid #1abc9c;
            }
            QLabel {
                color: white;
                padding: 15px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        sidebar.setMaximumWidth(200)

        layout = QVBoxLayout()

        # User info
        user_label = QLabel(f"User: {self.user['full_name']}\nRole: {self.user['role']}")
        user_label.setWordWrap(True)
        layout.addWidget(user_label)

        # Divider
        divider = QLabel("─" * 20)
        divider.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(divider)

        # Menu buttons
        menu_items = [
            ("Dashboard", 0),
            ("Customers", 1),
            ("Vehicles", 2),
            ("Services", 3),
            ("Inventory", 4),
            ("Billing", 5),
            ("Payments", 6),
            ("Reports", 7),
        ]

        for label, page_idx in menu_items:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, idx=page_idx: self.stacked_widget.setCurrentIndex(idx))
            layout.addWidget(btn)

        layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)

        sidebar.setLayout(layout)
        return sidebar

    def init_pages(self):
        """Initialize all pages"""
        # Dashboard page
        dashboard = QWidget()
        dashboard_layout = QVBoxLayout()
        welcome = QLabel(f"Welcome, {self.user['full_name']}!")
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        welcome_font.setBold(True)
        welcome.setFont(welcome_font)
        dashboard_layout.addWidget(welcome)
        dashboard_layout.addStretch()
        dashboard.setLayout(dashboard_layout)
        self.stacked_widget.addWidget(dashboard)

        # Other pages
        self.stacked_widget.addWidget(CustomerWindow())
        self.stacked_widget.addWidget(VehicleWindow())
        self.stacked_widget.addWidget(ServiceWindow())
        self.stacked_widget.addWidget(InventoryWindow())
        self.stacked_widget.addWidget(BillingWindow())
        self.stacked_widget.addWidget(PaymentWindow())
        self.stacked_widget.addWidget(ReportsWindow())

    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()
            self.close()