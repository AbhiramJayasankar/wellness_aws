import cv2
import numpy as np
import logging
from typing import Tuple, Optional

from config import Configuration

logger = logging.getLogger(__name__)


class VideoCapture:
    def __init__(self, config: Configuration):
        self.config = config
        self.cap = None
        self.is_initialized = False
        self._initialize_camera()
    
    def _initialize_camera(self) -> None:
        try:
            self.cap = cv2.VideoCapture(self.config.CAMERA_INDEX)
            if not self.cap.isOpened():
                raise RuntimeError(f"Cannot open camera {self.config.CAMERA_INDEX}")
            
            # Optimize camera settings
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.config.CAMERA_BUFFER_SIZE)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Test read to ensure camera is working
            ret, frame = self.cap.read()
            if not ret or frame is None:
                raise RuntimeError("Camera read test failed")
            
            self.is_initialized = True
            logger.info(f"Camera {self.config.CAMERA_INDEX} initialized successfully")
            
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            self.is_initialized = False
            if self.cap:
                self.cap.release()
                self.cap = None
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        if not self.is_initialized or not self.cap:
            return False, None
        
        try:
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("Failed to read frame from camera")
                return False, None
            return ret, frame
        except Exception as e:
            logger.error(f"Frame read error: {e}")
            return False, None
    
    def release(self) -> None:
        if self.cap:
            self.cap.release()
            self.cap = None
        self.is_initialized = False
        logger.info("Camera released")