import logging
from datetime import datetime, timedelta
from typing import Optional
from plyer import notification
from config import Configuration

logger = logging.getLogger(__name__)


class NotificationManager:
    def __init__(self, config: Configuration):
        self.config = config
        self.last_blink_count = 0
        self.last_check_time = datetime.now()
        self.notification_cooldown = timedelta(minutes=5)  # Prevent spam notifications
        self.last_notification_time: Optional[datetime] = None
        
    def check_blink_rate_and_notify(self, current_blink_count: int) -> None:
        current_time = datetime.now()
        time_elapsed = (current_time - self.last_check_time).total_seconds()
        
        # Only check if enough time has passed (based on config interval)
        if time_elapsed >= (self.config.NOTIFICATION_CHECK_INTERVAL / 1000):
            blinks_in_interval = current_blink_count - self.last_blink_count
            blinks_per_minute = (blinks_in_interval / time_elapsed) * 60
            
            logger.info(f"Blink rate check: {blinks_per_minute:.1f} blinks/min (threshold: {self.config.MIN_BLINKS_PER_MINUTE})")
            
            # Check if blink rate is below threshold
            if blinks_per_minute < self.config.MIN_BLINKS_PER_MINUTE:
                self._send_low_blink_notification(blinks_per_minute)
            
            # Reset for next interval
            self.last_blink_count = current_blink_count
            self.last_check_time = current_time
    
    def _send_low_blink_notification(self, current_rate: float) -> None:
        # Check cooldown to prevent notification spam
        current_time = datetime.now()
        if (self.last_notification_time and 
            current_time - self.last_notification_time < self.notification_cooldown):
            return
        
        try:
            notification.notify(
                title="Eye Health Alert",
                message=f"Low blink rate detected: {current_rate:.1f} blinks/min\n"
                       f"Recommended: {self.config.MIN_BLINKS_PER_MINUTE}+ blinks/min\n"
                       "Consider taking a break and blinking more frequently.",
                app_name="WaW Eyetracker",
                timeout=10  # Notification stays for 10 seconds
            )
            
            self.last_notification_time = current_time
            logger.info(f"Low blink rate notification sent: {current_rate:.1f} blinks/min")
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    def reset_tracking(self) -> None:
        """Reset tracking data (useful for new sessions)"""
        self.last_blink_count = 0
        self.last_check_time = datetime.now()
        self.last_notification_time = None
        logger.info("Notification tracking reset")