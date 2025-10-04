import unittest
import tempfile
import cv2
import numpy as np
from streamlit_app import DanceAnalyzer
import mediapipe as mp

class TestDanceAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DanceAnalyzer()
        # Initialize MediaPipe for testing
        self.mp_pose = mp.solutions.pose

    def test_analyzer_initialization(self):
        """Test if analyzer initializes properly"""
        self.assertIsInstance(self.analyzer.dance_poses, dict)
        self.assertGreater(len(self.analyzer.dance_poses), 0)

    def test_pose_detection_logic(self):
        """Test pose detection with mock landmarks"""
        # Mock landmarks for arms up pose
        class MockLandmark:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        # Create mock landmarks list (33 MediaPipe landmarks)
        landmarks = [MockLandmark(0, 0) for _ in range(33)]

        # Set specific poses - arms up
        landmarks[11] = MockLandmark(0.3, 0.3)  # LEFT_SHOULDER
        landmarks[12] = MockLandmark(0.7, 0.3)  # RIGHT_SHOULDER  
        landmarks[15] = MockLandmark(0.2, 0.1)  # LEFT_WRIST (higher)
        landmarks[16] = MockLandmark(0.8, 0.1)  # RIGHT_WRIST (higher)
        landmarks[23] = MockLandmark(0.4, 0.6)  # LEFT_HIP
        landmarks[24] = MockLandmark(0.6, 0.6)  # RIGHT_HIP
        landmarks[25] = MockLandmark(0.4, 0.8)  # LEFT_KNEE
        landmarks[26] = MockLandmark(0.6, 0.8)  # RIGHT_KNEE

        detected_poses = self.analyzer.analyze_pose(landmarks, self.mp_pose)
        self.assertIn("arms_up", detected_poses)

    def test_empty_landmarks(self):
        """Test handling of empty landmarks"""
        result = self.analyzer.analyze_pose(None, self.mp_pose)
        self.assertEqual(result, [])

    def test_pose_descriptions(self):
        """Test pose descriptions are available"""
        for pose in self.analyzer.dance_poses:
            self.assertIsInstance(self.analyzer.dance_poses[pose], str)
        
