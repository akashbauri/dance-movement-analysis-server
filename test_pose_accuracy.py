import cv2
import mediapipe as mp
import numpy as np
import unittest

from analyze_dance import process_video

class TestPoseDetection(unittest.TestCase):
    def test_pose_landmark_detection(self):
        test_input = "sample_videos/test_dance.mp4"
        test_output = "sample_videos/output_test.mp4"
        process_video(test_input, test_output)

        cap = cv2.VideoCapture(test_output)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.assertGreater(frame_count, 0, "No frames processed.")
        cap.release()

if __name__ == "__main__":
    unittest.main()
