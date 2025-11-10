import cv2
import mediapipe as mp
import os
import numpy as np
import time

# Initialize MediaPipe pose and drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def process_video(input_path, output_path):
    """
    Detects body landmarks in a dance video (up to 2 minutes, ≤25 MB)
    Adds FPS and Pose Confidence overlay on the output video.
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError("Input video not found!")

    cap = cv2.VideoCapture(input_path)

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

    # Limit processing to 2 minutes max (~120 seconds)
    max_frames = int(2 * 60 * fps)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    prev_time = time.time()
    frame_count = 0
    confidence_values = []  # Store confidence per frame

    with mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        while True:
            ret, frame = cap.read()
            if not ret or frame_count >= max_frames:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            # Draw landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

                # Calculate confidence: average visibility of landmarks
                conf = np.mean([lm.visibility for lm in results.pose_landmarks.landmark])
                confidence_values.append(conf)
            else:
                conf = 0.0
                confidence_values.append(conf)

            # Calculate FPS
            curr_time = time.time()
            fps_calc = 1 / (curr_time - prev_time)
            prev_time = curr_time

            # Add overlays (FPS + Confidence)
            cv2.putText(frame, f"FPS: {fps_calc:.1f}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
            cv2.putText(frame, f"Pose Confidence: {conf:.2f}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0) if conf > 0.5 else (0, 0, 255), 2)

            # Draw a small confidence graph at bottom
            graph_h = 100
            graph_y = height - graph_h
            graph_x = 20
            graph_w = min(400, width - 40)

            cv2.rectangle(frame, (graph_x, graph_y - 10),
                          (graph_x + graph_w, height - 10),
                          (255, 255, 255), 1)
            if len(confidence_values) > 1:
                norm_conf = np.array(confidence_values[-int(graph_w/3):])
                norm_conf = np.clip(norm_conf, 0, 1)
                points = [
                    (int(graph_x + i * 3), int(height - 10 - c * (graph_h - 20)))
                    for i, c in enumerate(norm_conf)
                ]
                for i in range(1, len(points)):
                    cv2.line(frame, points[i - 1], points[i], (0, 255, 0), 2)

            out.write(frame)
            frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return output_path
