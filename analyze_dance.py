# analyze_dance.py
import os
from typing import Tuple
import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def process_video(input_path: str, output_path: str, max_frames: int = None) -> Tuple[int, int]:
    """
    Process input video to overlay skeletons detected by MediaPipe Pose.
    Args:
      input_path: path to input video file.
      output_path: path where output video with skeleton overlay will be saved.
      max_frames: if provided, limit processing to this many frames (helpful for tests).
    Returns:
      (frame_count_processed, fps)
    Raises:
      FileNotFoundError if input_path doesn't exist.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Could not open video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    with mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            if max_frames and frame_count > max_frames:
                break

            # Convert BGR to RGB for Mediapipe
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            # Draw skeleton if landmarks found
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
                )

            out.write(frame)

    cap.release()
    out.release()
    return frame_count, int(fps)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python analyze_dance.py <input_video> <output_video>")
        sys.exit(1)
    inp = sys.argv[1]
    outp = sys.argv[2]
    frames, fps = process_video(inp, outp)
    print(f"Processed {frames} frames at {fps} fps -> {outp}")
