from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QFrame,
                              QMessageBox, QCheckBox)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal, QThread
import requests
import json
import re
from config import Configuration


class RegisterWorker(QThread):
    register_success = Signal(str)
    register_error = Signal(str)
    
    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        config = Configuration()
        self.base_url = config.BACKEND_URL
    
    def run(self):
        try:
            data = {
                "username": self.username,
                "email": self.email,
                "password": self.password
            }
            response = requests.post(f"{self.base_url}/register", json=data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                token = result.get("access_token")
                self.register_success.emit(token)
            else:
                error_msg = "Registration failed"
                if response.status_code == 400:
                    error_data = response.json()
                    error_msg = error_data.get("detail", "Username already exists")
                elif response.status_code >= 500:
                    error_msg = "Server error. Please try again later."
                self.register_error.emit(error_msg)
                
        except requests.exceptions.ConnectionError:
            self.register_error.emit("Cannot connect to server. Please ensure the backend is running on port 8000.")
        except requests.exceptions.Timeout:
            self.register_error.emit("Registration request timed out. Please try again.")
        except Exception as e:
            self.register_error.emit(f"Registration failed: {str(e)}")


class RegisterWidget(QWidget):
    registration_successful = Signal(str)
    switch_to_login = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.register_worker = None
    
    def setup_ui(self):
        self.setStyleSheet("""
            RegisterWidget {
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
        subtitle = QLabel("Create your account")
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
        
        main_layout.addWidget(header_widget, 2)
        
        # Form container with glassmorphism effect
        form_frame = QFrame()
        form_frame.setFixedSize(400, 520)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 12px;
                border: 1px solid #333333;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(14)
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
        self.username_input.setPlaceholderText("Choose a username")
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
        
        # Email field
        email_container = QVBoxLayout()
        email_container.setSpacing(5)
        email_label = QLabel("Email")
        email_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        email_label.setStyleSheet("color: #ffffff; margin-bottom: 2px; border: none;")
        email_label.setAlignment(Qt.AlignLeft)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        self.email_input.setStyleSheet("""
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
        email_container.addWidget(email_label)
        email_container.addWidget(self.email_input)
        form_layout.addLayout(email_container)
        
        # Password field
        password_container = QVBoxLayout()
        password_container.setSpacing(5)
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        password_label.setStyleSheet("color: #ffffff; margin-bottom: 2px; border: none;")
        password_label.setAlignment(Qt.AlignLeft)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Choose a secure password")
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
        
        # Confirm password field
        confirm_password_container = QVBoxLayout()
        confirm_password_container.setSpacing(5)
        confirm_password_label = QLabel("Confirm Password")
        confirm_password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        confirm_password_label.setStyleSheet("color: #ffffff; margin-bottom: 2px; border: none;")
        confirm_password_label.setAlignment(Qt.AlignLeft)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Re-enter your password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet("""
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
        confirm_password_container.addWidget(confirm_password_label)
        confirm_password_container.addWidget(self.confirm_password_input)
        form_layout.addLayout(confirm_password_container)
        
        # GDPR Consent checkbox
        consent_container = QVBoxLayout()
        consent_container.setSpacing(8)
        
        self.consent_checkbox = QCheckBox()
        self.consent_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                font-size: 11px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #404040;
                border-radius: 3px;
                background-color: #2a2a2a;
            }
            QCheckBox::indicator:checked {
                background-color: #666666;
                border: 2px solid #666666;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #777777;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #555555;
            }
        """)
        
        consent_text = QLabel("I agree to the collection and processing of my data as described in the privacy policy. I understand I can delete my account and data at any time.")
        consent_text.setWordWrap(True)
        consent_text.setFont(QFont("Segoe UI", 9))
        consent_text.setStyleSheet("color: #cccccc; margin-left: 8px; margin-top: 0px; border:none;")
        
        consent_layout = QHBoxLayout()
        consent_layout.setSpacing(8)
        consent_layout.addWidget(self.consent_checkbox)
        consent_layout.addWidget(consent_text, 1)
        
        form_layout.addLayout(consent_layout)
        
        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.clicked.connect(self.handle_register)
        self.register_button.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.register_button.setStyleSheet("""
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
        form_layout.addWidget(self.register_button)
        
        form_widget = QWidget()
        form_widget.setLayout(form_container)
        main_layout.addWidget(form_widget, 4)
        
        # Login link with scaling margins
        footer_container = QVBoxLayout()
        footer_container.setContentsMargins(0, 0, 0, 0)
        footer_widget = QWidget()
        footer_widget.setLayout(footer_container)
        footer_container.addStretch(1)
        login_link = QPushButton("Already have an account? Sign in")
        login_link.clicked.connect(self.switch_to_login.emit)
        login_link.setFont(QFont("Segoe UI", 11))
        login_link.setStyleSheet("""
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
        footer_container.addWidget(login_link)
        footer_container.addStretch(2)
        
        main_layout.addWidget(footer_widget, 1)
    
    def handle_register(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not all([username, email, password, confirm_password]):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Registration Error")
            msg.setText("Please fill in all fields")
            msg.exec()
            return
        
        if len(username) < 3:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Registration Error")
            msg.setText("Username must be at least 3 characters long")
            msg.exec()
            return
        
        if not self.is_valid_email(email):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Registration Error")
            msg.setText("Please enter a valid email address")
            msg.exec()
            return
        
        if len(password) < 6:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Registration Error")
            msg.setText("Password must be at least 6 characters long")
            msg.exec()
            return
        
        if password != confirm_password:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Registration Error")
            msg.setText("Passwords do not match")
            msg.exec()
            return
        
        if not self.consent_checkbox.isChecked():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Consent Required")
            msg.setText("You must agree to data processing to create an account")
            msg.setInformativeText("Please check the consent checkbox to proceed with registration.")
            msg.exec()
            return
        
        self.register_button.setText("Creating Account...")
        self.register_button.setEnabled(False)
        
        self.register_worker = RegisterWorker(username, email, password)
        self.register_worker.register_success.connect(self.on_register_success)
        self.register_worker.register_error.connect(self.on_register_error)
        self.register_worker.finished.connect(self.on_register_finished)
        self.register_worker.start()
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def on_register_success(self, token):
        self.registration_successful.emit(token)
    
    def on_register_error(self, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Registration Error")
        msg.setText(error_message)
        msg.exec()
    
    def on_register_finished(self):
        self.register_button.setText("Create Account")
        self.register_button.setEnabled(True)