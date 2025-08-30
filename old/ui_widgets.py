import cv2
import numpy as np
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from PySide6.QtGui import QImage, QPixmap, QFont, QPainter, QPainterPath
from PySide6.QtCore import Qt

from config import Configuration
from system_monitor import SystemStats


class VideoDisplayWidget(QLabel):
    def __init__(self, config: Configuration):
        super().__init__()
        self.config = config
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(*config.VIDEO_MIN_SIZE)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("border: 0px solid #ccc; border-radius: 12px; background-color: black;")
        self.border_radius = 12
        self.current_pixmap = None
    
    def display_frame(self, frame: np.ndarray) -> None:
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale to fit while maintaining aspect ratio
        label_size = self.size()
        self.current_pixmap = QPixmap.fromImage(qt_image).scaled(
            label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.current_pixmap:
            # Create rounded rectangle path
            path = QPainterPath()
            rect = self.rect()
            path.addRoundedRect(rect, self.border_radius, self.border_radius)
            
            # Clip to rounded rectangle
            painter.setClipPath(path)
            
            # Calculate position to center the pixmap
            pixmap_rect = self.current_pixmap.rect()
            x = (rect.width() - pixmap_rect.width()) // 2
            y = (rect.height() - pixmap_rect.height()) // 2
            
            # Draw the pixmap
            painter.drawPixmap(x, y, self.current_pixmap)


class SystemStatsWidget(QWidget):
    def __init__(self, config: Configuration):
        super().__init__()
        self.config = config
        self.setup_ui()
    
    def setup_ui(self) -> None:
        self.setMinimumWidth(self.config.STATS_PANEL_MIN_WIDTH)
        self.setMaximumWidth(self.config.STATS_PANEL_MAX_WIDTH)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setStyleSheet("border-right: 2px solid #ccc; padding: 10px;")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("System Statistics")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        # Stats labels
        self.cpu_label = QLabel()
        self.ram_label = QLabel()
        self.power_label = QLabel()
        self.disk_label = QLabel()
        
        stats_font = QFont("Consolas", 9)
        for label in [self.cpu_label, self.ram_label, self.power_label, self.disk_label]:
            label.setFont(stats_font)
            label.setStyleSheet("padding: 5px; margin: 2px; color: white;")
            label.setWordWrap(True)
            layout.addWidget(label)
        
        layout.addStretch()
    
    def update_stats(self, stats: SystemStats) -> None:
        # Use more efficient string formatting
        self.cpu_label.setText(f"🖥️  CPU Usage: {stats.cpu_usage:5.1f}%")
        
        ram_text = (f"🧠  RAM Usage: {stats.ram_percent:5.1f}%\n"
                   f"({stats.ram_used_gb:.1f}/{stats.ram_total_gb:.1f} GB)")
        self.ram_label.setText(ram_text)
        
        if stats.battery_percent is not None:
            power_text = (f"🔋  Battery: {stats.battery_percent:5.1f}%\n"
                         f"({stats.power_status})")
        else:
            power_text = f"🔋  {stats.power_status}\n(No Battery)"
        self.power_label.setText(power_text)
        
        disk_text = (f"💾  Disk Usage: {stats.disk_percent:5.1f}%\n"
                    f"({stats.disk_used_gb:.1f}/{stats.disk_total_gb:.1f} GB)")
        self.disk_label.setText(disk_text)