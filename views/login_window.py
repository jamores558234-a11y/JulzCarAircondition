"""Login window - Enhanced formal design"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox, QMessageBox, QFrame)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from controllers.auth_controller import AuthController


class LoginWindow(QWidget):
    login_success = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.init_ui()

    def init_ui(self):
        """Initialize login UI with formal design"""
        self.setWindowTitle("Julz Car AC Service - Login")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
            }
            QLineEdit, QComboBox {
                padding: 12px 15px;
                border: 2px solid #d1d5db;
                border-radius: 6px;
                font-size: 13px;
                background-color: #ffffff;
                color: #1f2937;
                font-weight: 500;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2563eb;
                background-color: #ffffff;
            }
            QLabel {
                color: #1f2937;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Header with title and subtitle
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)

        # Main title
        title = QLabel("Julz Car AC Service")
        title_font = QFont("Segoe UI", 24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1f2937; font-weight: 700;")
        header_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Management System")
        subtitle_font = QFont("Segoe UI", 14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #6b7280;")
        header_layout.addWidget(subtitle)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #e5e7eb;")
        header_layout.addWidget(divider)

        main_layout.addLayout(header_layout)

        # Login section
        login_label = QLabel("Sign In")
        login_label_font = QFont("Segoe UI", 16)
        login_label_font.setBold(True)
        login_label.setFont(login_label_font)
        login_label.setStyleSheet("color: #1f2937; margin-bottom: 15px;")
        main_layout.addWidget(login_label)

        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #374151; font-weight: 600; margin-top: 5px;")
        main_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(40)
        main_layout.addWidget(self.username_input)

        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #374151; font-weight: 600; margin-top: 10px;")
        main_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        main_layout.addWidget(self.password_input)

        # Role
        role_label = QLabel("User Role")
        role_label.setStyleSheet("color: #374151; font-weight: 600; margin-top: 10px;")
        main_layout.addWidget(role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Admin', 'Staff', 'Mechanic'])
        self.role_combo.setMinimumHeight(40)
        main_layout.addWidget(self.role_combo)

        # Login button
        login_btn = QPushButton("Sign In")
        login_btn.setMinimumHeight(45)
        login_btn.setFont(QFont("Segoe UI", 13))
        login_btn.clicked.connect(self.handle_login)
        main_layout.addWidget(login_btn, 0, Qt.AlignmentFlag.AlignTop)

        main_layout.addSpacing(20)

        # Demo credentials info
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #dbeafe;
                border: 1px solid #93c5fd;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 10, 15, 10)

        demo_title = QLabel("Demo Credentials")
        demo_title.setStyleSheet("color: #1e40af; font-weight: 600;")
        info_layout.addWidget(demo_title)

        demo_text = QLabel("Username: admin\nPassword: admin123\nRole: Admin")
        demo_text.setStyleSheet("color: #1e3a8a; font-size: 11px; line-height: 20px;")
        info_layout.addWidget(demo_text)

        main_layout.addWidget(info_frame)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def handle_login(self):
        """Handle login"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter username and password")
            return

        user = self.auth_controller.authenticate_user(username, password)

        if user:
            self.login_success.emit(user)
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Authentication Error", "Invalid username or password")

    def clear_inputs(self):
        """Clear input fields"""
        self.username_input.clear()
        self.password_input.clear()