import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import json
import os
from typing import Dict, List
import time

# Configure page
st.set_page_config(
    page_title="Dance Movement Analysis Server",
    page_icon="💃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize MediaPipe
@st.cache_resource
def load_pose_model():
    """Load MediaPipe pose detection model"""
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5
    )
    return pose, mp_pose

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

    def analyze_pose(self, landmarks, mp_pose) -> List[str]:
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
