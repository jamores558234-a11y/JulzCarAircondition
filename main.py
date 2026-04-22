"""Main application entry point"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from views.login_window import LoginWindow
from views.dashboard_window import DashboardWindow


class ApplicationManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.dashboard_window = None
        self.show_login()

    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow()
        self.login_window.login_success = self.show_dashboard
        self.login_window.show()

    def show_dashboard(self, user):
        """Show dashboard window"""
        self.dashboard_window = DashboardWindow(user)
        self.dashboard_window.logout_signal.connect(self.on_logout)
        self.dashboard_window.show()
        if self.login_window:
            self.login_window.close()

    def on_logout(self):
        """Handle logout"""
        if self.dashboard_window:
            self.dashboard_window.close()
        self.show_login()

    def run(self):
        """Run application"""
        sys.exit(self.app.exec())


if __name__ == "__main__":
    manager = ApplicationManager()
    manager.run()
    manager.run()