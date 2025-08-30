import sys
import psutil
from dataclasses import dataclass
from typing import Optional
from PySide6.QtCore import QThread, Signal


@dataclass
class SystemStats:
    cpu_usage: float = 0.0
    ram_percent: float = 0.0
    ram_used_gb: float = 0.0
    ram_total_gb: float = 0.0
    battery_percent: Optional[float] = None
    power_status: str = "Unknown"
    disk_percent: float = 0.0
    disk_used_gb: float = 0.0
    disk_total_gb: float = 0.0


class SystemMonitor(QThread):
    stats_updated = Signal(SystemStats)
    
    def __init__(self, update_interval: int = 1000):
        super().__init__()
        self.update_interval = update_interval
        self.running = False
    
    def start_monitoring(self) -> None:
        self.running = True
        self.start()
    
    def stop_monitoring(self) -> None:
        self.running = False
        self.wait()
    
    def run(self) -> None:
        while self.running:
            stats = self._collect_stats()
            self.stats_updated.emit(stats)
            self.msleep(self.update_interval)
    
    def _collect_stats(self) -> SystemStats:
        stats = SystemStats()
        
        try:
            # CPU Usage
            stats.cpu_usage = psutil.cpu_percent(interval=None)
            
            # RAM Usage
            ram = psutil.virtual_memory()
            stats.ram_percent = ram.percent
            stats.ram_used_gb = ram.used / (1024**3)
            stats.ram_total_gb = ram.total / (1024**3)
            
            # Battery/Power Info
            battery = psutil.sensors_battery()
            if battery:
                stats.battery_percent = battery.percent
                stats.power_status = "Charging" if battery.power_plugged else "Discharging"
            else:
                stats.power_status = "AC Connected"
            
            # Disk Usage
            disk = psutil.disk_usage('C:' if sys.platform == 'win32' else '/')
            stats.disk_percent = (disk.used / disk.total) * 100
            stats.disk_used_gb = disk.used / (1024**3)
            stats.disk_total_gb = disk.total / (1024**3)
            
        except Exception as e:
            print(f"Error collecting system stats: {e}")
        
        return stats