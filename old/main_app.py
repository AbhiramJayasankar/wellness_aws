import sys
import json
import logging
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QFrame, QStackedWidget,
                              QMessageBox, QSystemTrayIcon, QMenu)
import requests
import os
from datetime import datetime
from typing import Optional

from PySide6.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QBrush, QPainterPath, QIcon, QAction
from PySide6.QtCore import Qt, QTimer, Signal

# Import eye tracker components
from config import Configuration
from eye_tracker import EyeTracker
from system_monitor import SystemMonitor
from video_capture import VideoCapture
from ui_widgets import VideoDisplayWidget, SystemStatsWidget
from login import LoginWidget
from register import RegisterWidget
from notification_manager import NotificationManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EyeTrackerWidget(QWidget):
    def __init__(self, config: Optional[Configuration] = None, username: str = "User", auth_token: str = None):
        super().__init__()
        
        try:
            # Initialize configuration with validation
            self.config = config or Configuration()
            self.username = username
            self.auth_token = auth_token
            
            # Session tracking variables
            self.session_start_time = datetime.now().isoformat()
            self.current_blink_count = 0
            
            logger.info("Configuration initialized successfully")
            
            # Initialize components with error handling
            self.video_capture = VideoCapture(self.config)
            if not self.video_capture.is_initialized:
                self._show_camera_error()
                return
            
            self.eye_tracker = EyeTracker(self.config)
            self.eye_tracker.add_observer(self)
            
            self.notification_manager = NotificationManager(self.config)
            
            self.system_monitor = SystemMonitor(self.config.STATS_UPDATE_INTERVAL)
            
            # Setup UI
            self.setup_ui()
            
            # Setup timers
            self.video_timer = QTimer()
            self.video_timer.timeout.connect(self.update_frame)
            self.video_timer.start(self.config.VIDEO_UPDATE_INTERVAL)
            
            # Start system monitoring
            self.system_monitor.stats_updated.connect(self.stats_widget.update_stats)
            self.system_monitor.start_monitoring()
            
            logger.info("Eye tracker initialized successfully")
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            self._show_initialization_error(str(e))
    
    def _show_camera_error(self) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Camera Error")
        msg.setText("Failed to initialize camera")
        msg.setInformativeText(
            f"Could not access camera {self.config.CAMERA_INDEX}.\n"
            "Please check if the camera is connected and not used by another application."
        )
        msg.exec()
    
    def _show_initialization_error(self, error_msg: str) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Initialization Error")
        msg.setText("Failed to initialize eye tracker")
        msg.setInformativeText(f"Error: {error_msg}")
        msg.exec()
    
    def setup_ui(self) -> None:
        # Create horizontal main layout (sidebar + camera)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)
        
        # Create sidebar with profile and stats
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-right: 2px solid #555;
                border-radius: 12px;
            }
        """)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        sidebar_layout.setSpacing(20)
        sidebar.setLayout(sidebar_layout)
        
        # Profile section
        profile_frame = QFrame()
        profile_frame.setStyleSheet("""
            QFrame {
                background-color: #404040;
                border: 1px solid #666;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        profile_layout = QVBoxLayout()
        profile_layout.setContentsMargins(10, 10, 10, 10)
        profile_layout.setSpacing(10)
        profile_frame.setLayout(profile_layout)
        
        # Profile icon
        profile_icon = QLabel()
        profile_icon.setText("👤")
        profile_icon.setFont(QFont("Arial", 24))
        profile_icon.setAlignment(Qt.AlignCenter)
        profile_icon.setStyleSheet("background: transparent; border: none;")
        profile_layout.addWidget(profile_icon)
        
        # Username display
        name_label = QLabel(self.username)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: white; background: transparent; border: none;")
        profile_layout.addWidget(name_label)
        
        # App version
        version_label = QLabel("WaW Eyetracker v0.1")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Arial", 10))
        version_label.setStyleSheet("color: #ccc; background: transparent; border: none;")
        profile_layout.addWidget(version_label)
        
        sidebar_layout.addWidget(profile_frame)
        
        # System stats section
        self.stats_widget = SystemStatsWidget(self.config)
        # Override styling for sidebar integration
        self.stats_widget.setStyleSheet("""
            SystemStatsWidget {
                background-color: #404040;
                border: 1px solid #666;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: white;
                background-color: transparent;
                border: none;
                padding: 3px;
                margin: 1px;
            }
            QFrame {
                background-color: #555;
                border: none;
            }
        """)
        sidebar_layout.addWidget(self.stats_widget)
        
        # Add stretch to push everything to top
        sidebar_layout.addStretch()
        
        # Add sidebar to main layout
        main_layout.addWidget(sidebar)
        
        # Create video display widget that fills the main area
        self.video_display = VideoDisplayWidget(self.config)
        main_layout.addWidget(self.video_display)
    
    
    def on_blink_detected(self, blink_count: int) -> None:
        # Update current session blink count
        self.current_blink_count = blink_count
        # Check blink rate and send notification if needed
        self.notification_manager.check_blink_rate_and_notify(blink_count)
        # Output JSON for external consumption
        print(json.dumps({"blink_count": blink_count}), flush=True)
    
    def on_eye_data_updated(self, left_ear: float, right_ear: float, avg_ear: float) -> None:
        # Could be used for additional real-time processing or logging
        pass
    
    def send_session_data_to_backend(self) -> None:
        """Send current session data to backend"""
        if not self.auth_token:
            logger.warning("No auth token available, cannot send session data")
            return
            
        try:
            session_end_time = datetime.now().isoformat()
            session_data = {
                "session_start_time": self.session_start_time,
                "session_end_time": session_end_time,
                "total_blinks": self.current_blink_count
            }
            
            headers = {
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json"
            }
            
            # Try to send to backend
            response = requests.post(
                f"{self.config.BACKEND_URL}/sessions",
                json=session_data,
                headers=headers,
                timeout=5  # 5 second timeout
            )
            
            if response.status_code == 200:
                logger.info("Session data sent successfully to backend")
            else:
                logger.error(f"Failed to send session data: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error sending session data: {e}")
        except Exception as e:
            logger.error(f"Error sending session data: {e}")

    def update_frame(self) -> None:
        try:
            ret, frame = self.video_capture.read_frame()
            if ret and frame is not None:
                # Process frame with eye tracker
                processed_frame, eye_data = self.eye_tracker.process_frame(frame)
                
                # Display the processed frame
                self.video_display.display_frame(processed_frame)
            else:
                logger.warning("Failed to read frame from camera")
        except Exception as e:
            logger.error(f"Frame update error: {e}")

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        # The video display will automatically rescale on the next frame update
    
    def closeEvent(self, event) -> None:
        # Send session data to backend before closing
        try:
            self.send_session_data_to_backend()
        except Exception as e:
            logger.error(f"Error sending session data on close: {e}")
            
        # Clean shutdown of all components
        try:
            if hasattr(self, 'video_timer'):
                self.video_timer.stop()
            if hasattr(self, 'system_monitor'):
                self.system_monitor.stop_monitoring()
            if hasattr(self, 'video_capture'):
                self.video_capture.release()
            if hasattr(self, 'eye_tracker'):
                self.eye_tracker.close()
            logger.info("Application shutdown completed")
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
        finally:
            super().closeEvent(event)


class MainApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_system_tray()
        
    def setup_ui(self):
        self.setWindowTitle("Eye Tracker Application")
        self.setMinimumSize(600, 720)
        self.resize(1000, 550)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        
        # Create pages
        self.login_page = LoginWidget()
        self.register_page = RegisterWidget()
        
        # Add pages to stack
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        
        # Connect signals
        self.login_page.login_successful.connect(self.on_login_successful)
        self.login_page.switch_to_register.connect(self.show_register_page)
        self.register_page.registration_successful.connect(self.on_registration_successful)
        self.register_page.switch_to_login.connect(self.show_login_page)
        
        # Store authentication token and username
        self.auth_token = None
        self.username = None
        
        # Start with login page
        self.show_login_page()
    
    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)
    
    def show_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)
    
    def on_login_successful(self, token):
        self.auth_token = token
        # Get username from login page
        self.username = self.login_page.username_input.text().strip()
        self.show_main_page()
    
    def on_registration_successful(self, token):
        self.auth_token = token
        # Get username from register page
        self.username = self.register_page.username_input.text().strip()
        self.show_main_page()
    
    def show_main_page(self):
        try:
            config = Configuration()
            self.eye_tracker_page = EyeTrackerWidget(config, self.username, self.auth_token)
            
            if hasattr(self.eye_tracker_page, 'video_capture') and self.eye_tracker_page.video_capture.is_initialized:
                self.stacked_widget.addWidget(self.eye_tracker_page)
                self.stacked_widget.setCurrentWidget(self.eye_tracker_page)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Error")
                msg.setText("Failed to initialize eye tracker")
                msg.exec()
        except Exception as e:
            logger.error(f"Failed to create eye tracker page: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to initialize eye tracker: {str(e)}")
            msg.exec()
    
    def setup_system_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("System tray is not available on this system")
            return

        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        
        # Load icon (use existing icon.ico or create a default one)
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Use a default icon if icon.ico doesn't exist
            self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        
        # Create context menu
        tray_menu = QMenu()
        
        # Show/Hide action
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide_window)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        
        # Handle tray icon activation (double-click to show/hide)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        # Show system tray icon
        self.tray_icon.show()
        
        # Set tooltip
        self.tray_icon.setToolTip("Eye Tracker Application")
        
        logger.info("System tray icon initialized successfully")
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide_window()
            else:
                self.show_window()
    
    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()
    
    def hide_window(self):
        self.hide()
    
    def quit_application(self):
        # Send session data before quitting
        try:
            if hasattr(self, 'eye_tracker_page') and self.eye_tracker_page:
                self.eye_tracker_page.send_session_data_to_backend()
                logger.info("Session data sent before quitting from tray")
        except Exception as e:
            logger.error(f"Error sending session data on tray quit: {e}")
        
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        QApplication.quit()
    
    def closeEvent(self, event) -> None:
        """Handle main window close event (X button) - hide to tray instead of quitting"""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            # Hide to system tray instead of closing
            self.hide()
            self.tray_icon.showMessage(
                "Eye Tracker",
                "Application is still running in the system tray. Use the context menu to quit.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            event.ignore()
        else:
            # If no system tray, actually quit
            try:
                if hasattr(self, 'eye_tracker_page'):
                    self.eye_tracker_page.closeEvent(event)
                logger.info("Main application shutdown completed")
            except Exception as e:
                logger.error(f"Main application shutdown error: {e}")
            finally:
                super().closeEvent(event)


def main() -> None:
    try:
        app = QApplication(sys.argv)
        
        logger.info("Starting Eye Tracker Application")
        
        # Create and show the main application
        main_app = MainApplication()
        main_app.show()
        
        # Start the application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()