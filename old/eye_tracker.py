import cv2
import mediapipe as mp
import numpy as np
import logging
from dataclasses import dataclass
from typing import Optional, List, Tuple, Protocol
from weakref import WeakSet

from config import Configuration

logger = logging.getLogger(__name__)


class EyeTrackingObserver(Protocol):
    def on_blink_detected(self, blink_count: int) -> None:
        ...

    def on_eye_data_updated(self, left_ear: float, right_ear: float, avg_ear: float) -> None:
        ...


@dataclass
class EyeTrackingData:
    blink_count: int = 0
    left_ear: float = 0.0
    right_ear: float = 0.0
    avg_ear: float = 0.0
    left_eye_landmarks: Optional[List[Tuple[int, int]]] = None
    right_eye_landmarks: Optional[List[Tuple[int, int]]] = None


class EyeTracker:
    def __init__(self, config: Configuration):
        self.config = config
        self.mp_face_mesh = mp.solutions.face_mesh
        
        try:
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=config.MAX_FACES,
                refine_landmarks=True,
                static_image_mode=False,  # Optimize for video streams
                min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
            )
        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe FaceMesh: {e}")
            raise RuntimeError(f"MediaPipe initialization failed: {e}")
        
        self.data = EyeTrackingData()
        self.frame_counter = 0
        self.observers: WeakSet[EyeTrackingObserver] = WeakSet()
        self._frame_skip_counter = 0
        self._last_valid_landmarks = None
    
    def add_observer(self, observer: EyeTrackingObserver) -> None:
        self.observers.add(observer)
    
    def remove_observer(self, observer: EyeTrackingObserver) -> None:
        self.observers.discard(observer)
    
    def _notify_blink_detected(self) -> None:
        # Create a copy to avoid issues if observers are modified during iteration
        observers_copy = list(self.observers)
        for observer in observers_copy:
            try:
                observer.on_blink_detected(self.data.blink_count)
            except Exception as e:
                logger.warning(f"Observer notification failed: {e}")
    
    def _notify_eye_data_updated(self) -> None:
        observers_copy = list(self.observers)
        for observer in observers_copy:
            try:
                observer.on_eye_data_updated(self.data.left_ear, self.data.right_ear, self.data.avg_ear)
            except Exception as e:
                logger.warning(f"Observer notification failed: {e}")
    
    @staticmethod
    def _euclidean_dist(pt1: Tuple[int, int], pt2: Tuple[int, int]) -> float:
        return np.linalg.norm(np.array(pt1) - np.array(pt2))
    
    def _calculate_ear(self, eye_landmarks: List[Tuple[int, int]]) -> float:
        A = self._euclidean_dist(eye_landmarks[1], eye_landmarks[5])
        B = self._euclidean_dist(eye_landmarks[2], eye_landmarks[4])
        C = self._euclidean_dist(eye_landmarks[0], eye_landmarks[3])
        return (A + B) / (2.0 * C)
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, EyeTrackingData]:
        try:
            # Frame skipping for performance
            self._frame_skip_counter += 1
            should_process = self._frame_skip_counter >= self.config.MAX_FRAME_SKIP
            
            if should_process:
                self._frame_skip_counter = 0
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(rgb)
                
                if results.multi_face_landmarks:
                    h, w = frame.shape[:2]
                    face_landmarks = results.multi_face_landmarks[0]  # Use first face only
                    
                    # Extract and cache eye landmarks
                    left_eye = [(int(face_landmarks.landmark[i].x * w), 
                              int(face_landmarks.landmark[i].y * h)) 
                             for i in self.config.LEFT_EYE_INDICES]
                    right_eye = [(int(face_landmarks.landmark[i].x * w), 
                               int(face_landmarks.landmark[i].y * h)) 
                              for i in self.config.RIGHT_EYE_INDICES]
                    
                    self._last_valid_landmarks = (left_eye, right_eye)
                    self.data.left_eye_landmarks = left_eye
                    self.data.right_eye_landmarks = right_eye
                    
                    # Calculate EAR
                    self.data.left_ear = self._calculate_ear(left_eye)
                    self.data.right_ear = self._calculate_ear(right_eye)
                    self.data.avg_ear = (self.data.left_ear + self.data.right_ear) / 2.0
                    
                    # Blink detection logic
                    self._update_blink_detection()
                    
                elif self._last_valid_landmarks:
                    # Use cached landmarks when face detection fails temporarily
                    left_eye, right_eye = self._last_valid_landmarks
                    self.data.left_eye_landmarks = left_eye
                    self.data.right_eye_landmarks = right_eye
            
            # Always draw current landmarks and stats
            self._draw_overlays(frame)
            self._notify_eye_data_updated()
            
        except Exception as e:
            logger.error(f"Frame processing error: {e}")
            # Return original frame on error
        
        return frame, self.data
    
    def _update_blink_detection(self) -> None:
        if self.data.avg_ear < self.config.EAR_THRESHOLD:
            self.frame_counter += 1
        else:
            if self.frame_counter >= self.config.CONSECUTIVE_FRAMES:
                self.data.blink_count += 1
                self._notify_blink_detected()
            self.frame_counter = 0
    
    def _draw_overlays(self, frame: np.ndarray) -> None:
        # Draw eye landmarks if available
        if self.data.left_eye_landmarks and self.data.right_eye_landmarks:
            all_landmarks = self.data.left_eye_landmarks + self.data.right_eye_landmarks
            for pt in all_landmarks:
                cv2.circle(frame, pt, 2, (0, 255, 0), -1)
        
        # Draw blink count with better formatting
        text = f'Blinks: {self.data.blink_count}'
        font_scale = 1.0
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
        )
        
        # Add background rectangle for better readability
        cv2.rectangle(frame, (25, 25), (35 + text_width, 35 + text_height), 
                     (0, 0, 0), -1)
        cv2.putText(frame, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, (0, 0, 255), thickness)
    
    def close(self) -> None:
        self.face_mesh.close()