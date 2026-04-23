"""Dashboard window - Enhanced formal design with content - FIXED"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QMessageBox,
                             QFrame, QGridLayout, QScrollArea)
from PyQt6.QtGui import QFont, QIcon
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
        self.setGeometry(0, 0, 1600, 900)

    def init_ui(self):
        """Initialize dashboard UI"""
        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Content area
        self.stacked_widget = QStackedWidget()
        self.init_pages()
        main_layout.addWidget(self.stacked_widget, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = QWidget()
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
            }
            QPushButton {
                background-color: #1e293b;
                color: #e2e8f0;
                border: none;
                padding: 14px 16px;
                text-align: left;
                font-weight: 600;
                border-left: 4px solid transparent;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-left: 4px solid #3b82f6;
            }
            QPushButton:pressed {
                background-color: #0f172a;
                border-left: 4px solid #2563eb;
            }
            QLabel {
                color: #e2e8f0;
                padding: 15px;
                font-weight: 700;
                font-size: 12px;
            }
        """)
        sidebar.setMaximumWidth(220)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header with logo/title
        header = QLabel("JULZ CAR AC")
        header_font = QFont("Segoe UI", 11)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            background-color: #0f172a;
            color: #3b82f6;
            padding: 20px 15px;
            font-weight: 700;
            font-size: 12px;
            border-bottom: 1px solid #334155;
        """)
        layout.addWidget(header)

        # User info section
        user_section = QFrame()
        user_section.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border-bottom: 1px solid #334155;
            }
        """)
        user_layout = QVBoxLayout(user_section)
        user_layout.setContentsMargins(15, 15, 15, 15)
        user_layout.setSpacing(8)

        user_label = QLabel(f"👤 {self.user['full_name']}")
        user_label.setStyleSheet("color: #e2e8f0; font-weight: 600; font-size: 12px;")
        user_layout.addWidget(user_label)

        role_label = QLabel(f"📋 {self.user['role']}")
        role_label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        user_layout.addWidget(role_label)

        layout.addWidget(user_section)

        # Menu divider
        divider = QLabel("━" * 20)
        divider.setAlignment(Qt.AlignmentFlag.AlignCenter)
        divider.setStyleSheet("color: #334155; padding: 10px;")
        layout.addWidget(divider)

        # Menu buttons
        menu_items = [
            ("📊 Dashboard", 0),
            ("👥 Customers", 1),
            ("🚗 Vehicles", 2),
            ("🔧 Services", 3),
            ("📦 Inventory", 4),
            ("💰 Billing", 5),
            ("💳 Payments", 6),
            ("📈 Reports", 7),
        ]

        for label, page_idx in menu_items:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, idx=page_idx: self.stacked_widget.setCurrentIndex(idx))
            layout.addWidget(btn)

        layout.addStretch()

        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f1d1d;
                color: white;
                padding: 14px;
                border: none;
                font-weight: 600;
                border-left: 4px solid #7f1d1d;
            }
            QPushButton:hover {
                background-color: #b91c1c;
                border-left: 4px solid #dc2626;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)

        sidebar.setLayout(layout)
        return sidebar

    def init_pages(self):
        """Initialize all pages"""
        # Dashboard page with content
        dashboard = self.create_dashboard_page()
        self.stacked_widget.addWidget(dashboard)

        # Other pages
        self.stacked_widget.addWidget(CustomerWindow())
        self.stacked_widget.addWidget(VehicleWindow())
        self.stacked_widget.addWidget(ServiceWindow())
        self.stacked_widget.addWidget(InventoryWindow())
        self.stacked_widget.addWidget(BillingWindow())
        self.stacked_widget.addWidget(PaymentWindow())
        self.stacked_widget.addWidget(ReportsWindow())

    def create_dashboard_page(self):
        """Create the dashboard page with statistics"""
        dashboard = QWidget()
        dashboard.setStyleSheet("background-color: #f8fafc;")

        # Use scroll area for safety
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background-color: #f8fafc; border: none; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #f8fafc;")
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Welcome section
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2563eb, stop:1 #1e40af);
                border-radius: 12px;
            }
        """)
        welcome_frame.setMinimumHeight(120)
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setContentsMargins(30, 20, 30, 20)

        welcome_title = QLabel(f"Welcome back, {self.user.get('full_name', 'User')}! 👋")
        welcome_title.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: 700;
        """)
        welcome_layout.addWidget(welcome_title)

        welcome_subtitle = QLabel(f"Role: {self.user.get('role', 'Staff')} | Access Level: Full")
        welcome_subtitle.setStyleSheet("""
            color: #dbeafe;
            font-size: 14px;
        """)
        welcome_layout.addWidget(welcome_subtitle)

        main_layout.addWidget(welcome_frame)

        # Statistics section
        stats_label = QLabel("Quick Statistics")
        stats_label.setStyleSheet("""
            color: #1f2937;
            font-size: 18px;
            font-weight: 700;
            margin-top: 20px;
        """)
        main_layout.addWidget(stats_label)

        # Stats grid with safe defaults
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)

        stats = [
            ("👥 Total Customers", "0", "#dbeafe", "#1e40af"),
            ("🔧 Active Services", "0", "#dcfce7", "#15803d"),
            ("✅ Completed Services", "0", "#fce7f3", "#be185d"),
            ("📋 Total Services", "0", "#fef3c7", "#92400e"),
        ]

        for idx, (title, value, bg_color, text_color) in enumerate(stats):
            stat_card = self.create_stat_card(title, value, bg_color, text_color)
            stats_grid.addWidget(stat_card, idx // 2, idx % 2)

        main_layout.addLayout(stats_grid)

        # Quick actions section
        actions_label = QLabel("Quick Actions")
        actions_label.setStyleSheet("""
            color: #1f2937;
            font-size: 18px;
            font-weight: 700;
            margin-top: 20px;
        """)
        main_layout.addWidget(actions_label)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)

        action_buttons = [
            ("👤 Add New Customer", "#3b82f6"),
            ("🔧 Create Service", "#10b981"),
            ("💰 Process Billing", "#f59e0b"),
            ("📊 View Reports", "#8b5cf6"),
        ]

        for action_title, color in action_buttons:
            action_btn = QPushButton(action_title)
            action_btn.setMinimumHeight(50)
            action_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    opacity: 0.9;
                }}
            """)
            actions_layout.addWidget(action_btn)

        main_layout.addLayout(actions_layout)

        # Info section
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f3f4f6;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
        """)
        info_frame.setMinimumHeight(150)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 20, 20, 20)

        info_title = QLabel("System Features")
        info_title.setStyleSheet("color: #1f2937; font-weight: 700; font-size: 14px;")
        info_layout.addWidget(info_title)

        info_text = QLabel(
            "✓ Manage customer information and vehicle records\n"
            "✓ Track service requests and repairs\n"
            "✓ Manage inventory and spare parts\n"
            "✓ Generate invoices and billing\n"
            "✓ Process payments and generate reports"
        )
        info_text.setStyleSheet("color: #4b5563; font-size: 12px; line-height: 25px;")
        info_layout.addWidget(info_text)

        main_layout.addWidget(info_frame)
        main_layout.addStretch()

        scroll.setWidget(content_widget)

        # Add scroll to main dashboard layout
        dashboard_layout = QVBoxLayout(dashboard)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        dashboard_layout.addWidget(scroll)

        return dashboard

    def create_stat_card(self, title, value, bg_color, text_color):
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 12px;
                border: 1px solid {text_color}33;
            }}
        """)
        card.setMinimumHeight(120)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {text_color};
            font-size: 13px;
            font-weight: 600;
        """)
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {text_color};
            font-size: 36px;
            font-weight: 700;
        """)
        layout.addWidget(value_label)

        return card

    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()
            self.close()