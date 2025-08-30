from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Configuration:
    # Eye tracking settings
    EAR_THRESHOLD: float = 0.21
    CONSECUTIVE_FRAMES: int = 2
    MAX_FACES: int = 1
    MIN_DETECTION_CONFIDENCE: float = 0.5
    MIN_TRACKING_CONFIDENCE: float = 0.5
    
    # UI settings
    VIDEO_UPDATE_INTERVAL: int = 30  # ms
    STATS_UPDATE_INTERVAL: int = 1000  # ms
    STATS_PANEL_MIN_WIDTH: int = 200
    STATS_PANEL_MAX_WIDTH: int = 300
    VIDEO_MIN_SIZE: Tuple[int, int] = (320, 240)
    
    # Camera settings
    CAMERA_INDEX: int = 0
    CAMERA_BUFFER_SIZE: int = 1
    
    # Performance settings
    MAX_FRAME_SKIP: int = 0
    ENABLE_GPU_ACCELERATION: bool = True
    
    # Backend API settings
    BACKEND_URL: str = "http://3.90.152.193:8000"
    
    # Notification settings
    MIN_BLINKS_PER_MINUTE: int = 15  # Minimum blinks per minute threshold
    NOTIFICATION_CHECK_INTERVAL: int = 60000  # Check interval in ms (1 minute)
    
    # Eye landmark indices (MediaPipe face mesh indices)
    LEFT_EYE_INDICES: List[int] = field(default_factory=lambda: [33, 160, 158, 133, 153, 144])
    RIGHT_EYE_INDICES: List[int] = field(default_factory=lambda: [362, 385, 387, 263, 373, 380])
    
    def __post_init__(self) -> None:
        # Validate configuration values
        if not (0.0 <= self.EAR_THRESHOLD <= 1.0):
            raise ValueError("EAR_THRESHOLD must be between 0.0 and 1.0")
        if not (0.0 <= self.MIN_DETECTION_CONFIDENCE <= 1.0):
            raise ValueError("MIN_DETECTION_CONFIDENCE must be between 0.0 and 1.0")
        if not (0.0 <= self.MIN_TRACKING_CONFIDENCE <= 1.0):
            raise ValueError("MIN_TRACKING_CONFIDENCE must be between 0.0 and 1.0")