from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QFrame,
                              QMessageBox)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal, QThread
import requests
import json
from config import Configuration


class LoginWorker(QThread):
    login_success = Signal(str)
    login_error = Signal(str)
    
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        config = Configuration()
        self.base_url = config.BACKEND_URL
    
    def run(self):
        try:
            data = {
                "username": self.username,
                "password": self.password
            }
            response = requests.post(f"{self.base_url}/login", json=data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                token = result.get("access_token")
                self.login_success.emit(token)
            else:
                error_msg = "Invalid credentials"
                if response.status_code == 401:
                    error_msg = "Invalid username or password"
                elif response.status_code >= 500:
                    error_msg = "Server error. Please try again later."
                self.login_error.emit(error_msg)
                
        except requests.exceptions.ConnectionError:
            self.login_error.emit("Cannot connect to server. Please ensure the backend is running on port 8000.")
        except requests.exceptions.Timeout:
            self.login_error.emit("Login request timed out. Please try again.")
        except Exception as e:
            self.login_error.emit(f"Login failed: {str(e)}")


class LoginWidget(QWidget):
    login_successful = Signal(str)
    switch_to_register = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.login_worker = None
    
    def setup_ui(self):
        self.setStyleSheet("""
            LoginWidget {
                background-color: #000000;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        # App logo/title section
        header_frame = QFrame()
        header_frame.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout()
        header_frame.setLayout(header_layout)
        
        
        # App title
        title = QLabel("Eye Tracker")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; margin-bottom: 5px;")
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Welcome back")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #cccccc; margin-bottom: 20px;")
        header_layout.addWidget(subtitle)
        
        # Add header with scaling margins
        header_container = QVBoxLayout()
        header_container.setContentsMargins(0, 0, 0, 0)
        header_widget = QWidget()
        header_widget.setLayout(header_container)
        header_container.addStretch(2)
        header_container.addWidget(header_frame)
        header_container.addStretch(1)
        
        main_layout.addWidget(header_widget, 3)
        
        # Form container with glassmorphism effect
        form_frame = QFrame()
        form_frame.setFixedSize(400, 280)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 12px;
                border: 1px solid #333333;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(16)
        form_frame.setLayout(form_layout)
        
        # Center the form frame horizontally with scaling margins
        form_container = QHBoxLayout()
        form_container.setContentsMargins(0, 0, 0, 0)
        form_container.addStretch(2)
        form_container.addWidget(form_frame)
        form_container.addStretch(2)
        
        # Username field
        username_container = QVBoxLayout()
        username_container.setSpacing(5)
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        username_label.setStyleSheet("color: #ffffff; margin-bottom: 2px; border: none;")
        username_label.setAlignment(Qt.AlignLeft)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 14px;
                border: 1px solid #404040;
                border-radius: 6px;
                font-size: 13px;
                background-color: #2a2a2a;
                color: #ffffff;
                selection-background-color: #555555;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #666666;
                background-color: #333333;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
        """)
        username_container.addWidget(username_label)
        username_container.addWidget(self.username_input)
        form_layout.addLayout(username_container)
        
        # Password field
        password_container = QVBoxLayout()
        password_container.setSpacing(5)
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        password_label.setStyleSheet("color: #ffffff; margin-bottom: 2px; border: none;")
        password_label.setAlignment(Qt.AlignLeft)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 14px;
                border: 1px solid #404040;
                border-radius: 6px;
                font-size: 13px;
                background-color: #2a2a2a;
                color: #ffffff;
                selection-background-color: #555555;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #666666;
                background-color: #333333;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
        """)
        password_container.addWidget(password_label)
        password_container.addWidget(self.password_input)
        form_layout.addLayout(password_container)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                padding: 14px 20px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                background-color: #666666;
                color: #ffffff;
                margin-top: 8px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #cccccc;
            }
        """)
        form_layout.addWidget(self.login_button)
        
        form_widget = QWidget()
        form_widget.setLayout(form_container)
        main_layout.addWidget(form_widget, 2)
        
        # Register link with scaling margins
        footer_container = QVBoxLayout()
        footer_container.setContentsMargins(0, 0, 0, 0)
        footer_widget = QWidget()
        footer_widget.setLayout(footer_container)
        footer_container.addStretch(1)
        register_link = QPushButton("Don't have an account? Create one")
        register_link.clicked.connect(self.switch_to_register.emit)
        register_link.setFont(QFont("Segoe UI", 11))
        register_link.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #cccccc;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        footer_container.addWidget(register_link)
        footer_container.addStretch(2)
        
        main_layout.addWidget(footer_widget, 1)
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Login Error")
            msg.setText("Please enter both username and password")
            msg.exec()
            return
        
        self.login_button.setText("Signing In...")
        self.login_button.setEnabled(False)
        
        self.login_worker = LoginWorker(username, password)
        self.login_worker.login_success.connect(self.on_login_success)
        self.login_worker.login_error.connect(self.on_login_error)
        self.login_worker.finished.connect(self.on_login_finished)
        self.login_worker.start()
    
    def on_login_success(self, token):
        self.login_successful.emit(token)
    
    def on_login_error(self, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Login Error")
        msg.setText(error_message)
        msg.exec()
    
    def on_login_finished(self):
        self.login_button.setText("Sign In")
        self.login_button.setEnabled(True)