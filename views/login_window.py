"""Login window"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from controllers.auth_controller import AuthController


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.init_ui()

    def init_ui(self):
        """Initialize login UI"""
        self.setWindowTitle("Julz Car AC Service - Login")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #007bff;
                color: black;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Julz Car AC Service Management System")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Login to Your Account")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Role
        layout.addWidget(QLabel("Role:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Admin', 'Staff', 'Mechanic'])
        layout.addWidget(self.role_combo)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        layout.addStretch()

        # Demo credentials
        demo_label = QLabel("Demo: username=admin, password=admin123")
        demo_label.setStyleSheet("color: #666; font-size: 10px;")
        demo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(demo_label)

        self.setLayout(layout)

    def handle_login(self):
        """Handle login"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return

        user = self.auth_controller.authenticate_user(username, password)

        if user:
            self.login_success.emit(user)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def login_success(self, user):
        """Login successful - override in main app"""
        pass