import unittest
import json
from app import DanceAnalyzer

class TestDanceAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DanceAnalyzer()

    def test_analyzer_initialization(self):
        """Test if analyzer initializes properly"""
        self.assertIsInstance(self.analyzer.dance_poses, dict)
        self.assertGreater(len(self.analyzer.dance_poses), 0)

    def test_pose_detection(self):
        """Test pose detection with mock landmarks"""
        # Mock landmarks for arms up pose
        class MockLandmark:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        # Create mock landmarks dict
        landmarks = [MockLandmark(0, 0) for _ in range(33)]  # 33 MediaPipe landmarks

        # Set specific poses - arms up
        landmarks[11] = MockLandmark(0.3, 0.3)  # LEFT_SHOULDER
        landmarks[12] = MockLandmark(0.7, 0.3)  # RIGHT_SHOULDER  
        landmarks[15] = MockLandmark(0.2, 0.1)  # LEFT_WRIST (higher)
        landmarks[16] = MockLandmark(0.8, 0.1)  # RIGHT_WRIST (higher)
        landmarks[23] = MockLandmark(0.4, 0.6)  # LEFT_HIP
        landmarks[24] = MockLandmark(0.6, 0.6)  # RIGHT_HIP
        landmarks[25] = MockLandmark(0.4, 0.8)  # LEFT_KNEE
        landmarks[26] = MockLandmark(0.6, 0.8)  # RIGHT_KNEE

        detected_poses = self.analyzer.analyze_pose(landmarks)
        self.assertIn("arms_up", detected_poses)

    def test_empty_landmarks(self):
        """Test handling of empty landmarks"""
        result = self.analyzer.analyze_pose(None)
        self.assertEqual(result, [])

    def test_video_processing_error_handling(self):
        """Test error handling for invalid video file"""
        with self.assertRaises(Exception):
            self.analyzer.process_video("nonexistent_file.mp4")

if __name__ == '__main__':
    unittest.main()
