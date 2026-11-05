"""
Feature Extraction Module
Computes EAR, MAR, and head pose for drowsiness detection.
"""

import cv2
import numpy as np
from scipy.spatial import distance as dist


class FeatureExtractor:
    """Extracts facial features for drowsiness detection."""
    
    def __init__(self):
        """Initialize feature extractor."""
        # Eye aspect ratio threshold
        self.EAR_THRESHOLD = 0.23
        # Mouth aspect ratio threshold
        self.MAR_THRESHOLD = 0.5
        
        # MediaPipe Landmark Indices
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.MOUTH = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
        self.INNER_MOUTH = [13, 14, 78, 308] # For MAR

    def calculate_ear(self, landmarks, eye_indices):
        """
        Calculate EAR using MediaPipe landmarks.
        """
        try:
            # Vertical distances
            v1 = dist.euclidean(landmarks[eye_indices[1]], landmarks[eye_indices[5]])
            v2 = dist.euclidean(landmarks[eye_indices[2]], landmarks[eye_indices[4]])
            # Horizontal distance
            h = dist.euclidean(landmarks[eye_indices[0]], landmarks[eye_indices[3]])
            
            if h > 0:
                return (v1 + v2) / (2.0 * h)
            return 0.0
        except Exception as e:
            print(f"EAR calculation error: {e}")
            return 0.0

    def calculate_mar(self, landmarks):
        """
        Calculate MAR using MediaPipe landmarks (Inner Mouth).
        """
        try:
            # Vertical distance (Top lip to bottom lip)
            v = dist.euclidean(landmarks[13], landmarks[14])
            # Horizontal distance (Left corner to right corner)
            h = dist.euclidean(landmarks[78], landmarks[308])
            
            if h > 0:
                return v / h
            return 0.0
        except Exception as e:
            print(f"MAR calculation error: {e}")
            return 0.0

    def estimate_head_pose(self, landmarks, image_shape):
        """
        Estimate head pose using MediaPipe landmarks.
        Returns: "STRAIGHT", "UP", "DOWN", "LEFT", "RIGHT"
        """
        try:
            h, w = image_shape[:2]
            # Nose tip (1), Chin (152), Left Eye (33), Right Eye (263), Left Mouth (61), Right Mouth (291)
            # Simplified pose estimation based on relative positions
            nose_tip = landmarks[1]
            
            # Check for horizontal rotation (Yaw)
            left_eye_center = np.mean([landmarks[i] for i in self.LEFT_EYE], axis=0)
            right_eye_center = np.mean([landmarks[i] for i in self.RIGHT_EYE], axis=0)
            mouth_center = np.mean([landmarks[i] for i in self.MOUTH], axis=0)
            
            face_center_x = (left_eye_center[0] + right_eye_center[0]) / 2
            face_center_y = (left_eye_center[1] + right_eye_center[1] + mouth_center[1]) / 3
            
            # Yaw (Left/Right)
            yaw_diff = (nose_tip[0] - face_center_x) / w
            if yaw_diff < -0.08: return "LEFT"
            if yaw_diff > 0.08: return "RIGHT"
            
            # Pitch (Up/Down)
            pitch_diff = (nose_tip[1] - face_center_y) / h
            if pitch_diff < -0.06: return "UP"
            if pitch_diff > 0.06: return "DOWN"
            
            return "STRAIGHT"
        except Exception as e:
            return "STRAIGHT"

    def calculate_blink_rate(self, ear_history, time_window=60):
        # Implementation remains similar but adjusted for consistency
        if not ear_history or len(ear_history) < 2:
            return 0.0
        
        blinks = 0
        in_blink = False
        for timestamp, ear in ear_history:
            if ear < self.EAR_THRESHOLD and not in_blink:
                blinks += 1
                in_blink = True
            elif ear >= self.EAR_THRESHOLD:
                in_blink = False
        
        time_span = ear_history[-1][0] - ear_history[0][0]
        if time_span > 0:
            return (blinks / time_span) * 60
        return 0.0

