from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import json
from typing import Dict, List
import uvicorn
import os

app = FastAPI(title="Dance Movement Analysis API", version="1.0.0")

# Initialize MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5
)

class DanceAnalyzer:
    def __init__(self):
        self.dance_poses = {
            "arms_up": "Arms raised above shoulders",
            "side_stretch": "Arms extended to sides", 
            "forward_bend": "Torso bent forward",
            "balance_pose": "Single leg standing",
            "jumping": "Both feet off ground",
            "squat": "Knees bent, low position"
        }

    def analyze_pose(self, landmarks) -> List[str]:
        """Analyze detected landmarks to identify dance poses"""
        detected_poses = []

        if not landmarks:
            return detected_poses

        # Get key points
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]

        # Arms up detection
        if (left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y):
            detected_poses.append("arms_up")

        # Side stretch detection  
        if (abs(left_wrist.x - left_shoulder.x) > 0.2 and 
            abs(right_wrist.x - right_shoulder.x) > 0.2):
            detected_poses.append("side_stretch")
