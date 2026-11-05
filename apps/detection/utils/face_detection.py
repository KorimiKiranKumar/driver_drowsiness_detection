"""
Face Detection Module
Handles face detection using Haar Cascade or Dlib.
"""

import cv2
import numpy as np
import os
from django.conf import settings


class FaceDetector:
    """Face detection using Haar Cascade classifier."""
    
    def __init__(self):
        """Initialize face detector with Haar Cascade."""
        # Load Haar Cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Load Haar Cascade for eye detection
        eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
        self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        
        # Check if cascades loaded successfully
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face cascade classifier")
        if self.eye_cascade.empty():
            raise RuntimeError("Failed to load eye cascade classifier")
    
    def detect_face(self, frame):
        """
        Detect face in the frame.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            tuple: (face_region, face_coords) or (None, None) if no face detected
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(faces) == 0:
            return None, None
        
        # Get the largest face (assuming it's the driver)
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        # Extract face region
        face_region = frame[y:y+h, x:x+w]
        face_gray = gray[y:y+h, x:x+w]
        
        return face_region, (x, y, w, h), face_gray
    
    def detect_eyes(self, face_gray):
        """
        Detect eyes in the face region.
        
        Args:
            face_gray: Grayscale face region
            
        Returns:
            list: List of eye coordinates [(x, y, w, h), ...]
        """
        eyes = self.eye_cascade.detectMultiScale(
            face_gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Sort eyes by x-coordinate (left to right)
        eyes = sorted(eyes, key=lambda rect: rect[0])
        
        return eyes
    
    def get_eye_regions(self, face_gray, eyes):
        """
        Extract eye regions from face.
        
        Args:
            face_gray: Grayscale face region
            eyes: List of eye coordinates
            
        Returns:
            tuple: (left_eye_region, right_eye_region)
        """
        if len(eyes) < 2:
            return None, None
        
        # Get left and right eyes
        left_eye = eyes[0]
        right_eye = eyes[1]
        
        # Extract eye regions with padding
        padding = 5
        left_eye_region = face_gray[
            max(0, left_eye[1]-padding):left_eye[1]+left_eye[3]+padding,
            max(0, left_eye[0]-padding):left_eye[0]+left_eye[2]+padding
        ]
        right_eye_region = face_gray[
            max(0, right_eye[1]-padding):right_eye[1]+right_eye[3]+padding,
            max(0, right_eye[0]-padding):right_eye[0]+right_eye[2]+padding
        ]
        
        return left_eye_region, right_eye_region

