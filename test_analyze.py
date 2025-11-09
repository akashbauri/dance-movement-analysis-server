# test_analyze.py
import os
import tempfile
import cv2
from analyze_dance import process_video

def create_test_video(path: str, frames=10, w=320, h=240, fps=10):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(path, fourcc, fps, (w, h))
    for i in range(frames):
        frame = 255 * ( ( (i % 2) * 1 ) * ( (i + 1) % 2 ) ) * 0 + (np.zeros((h, w, 3), dtype='uint8'))
        # Simpler: draw moving circle
        frame = (np.ones((h, w, 3), dtype='uint8') * 10)
        center = (int(w * (i / frames)), int(h / 2))
        cv2.circle(frame, center, 15, (0, 255, 0), -1)
        out.write(frame)
    out.release()

import numpy as np

def test_process_creates_output(tmp_path):
    inp = tmp_path / "in.mp4"
    out = tmp_path / "out.mp4"
    create_test_video(str(inp), frames=12)
    frames_processed, fps = process_video(str(inp), str(out), max_frames=10)
    assert frames_processed > 0
    assert out.exists()
    # Basic sanity: file size non-zero
    assert out.stat().st_size > 0
