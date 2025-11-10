import gradio as gr
import cv2
import mediapipe as mp
import tempfile
import shutil
import os


def process_video(input_path, output_path):
    """Detects dance poses and saves the overlayed output video."""
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(3)), int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                )
            out.write(frame)

    cap.release()
    out.release()
    return fps


def analyze_dance(video):
    """Gradio wrapper — processes uploaded dance video."""
    if not video:
        return None, "⚠️ Please upload a short MP4 dance video."
    try:
        temp_input = os.path.join(tempfile.gettempdir(), "dance_input.mp4")
        temp_output = os.path.join(tempfile.gettempdir(), "dance_output.mp4")
        shutil.copy(video, temp_input)

        fps = process_video(temp_input, temp_output)
        return temp_output, f"✅ Dance video processed successfully at {fps:.1f} FPS."
    except Exception as e:
        return None, f"❌ Error while processing: {str(e)}"


# -------- GRADIO INTERFACE --------
demo = gr.Interface(
    fn=analyze_dance,
    inputs=gr.Video(label="🎥 Upload your dance video (≤10 s, MP4)"),
    outputs=[
        gr.Video(label="🩰 Pose Overlay"),
        gr.Textbox(label="📜 Processing Status")
    ],
    title="💃 Dance Movement Analysis",
    description="AI-powered pose detection using MediaPipe for short dance videos.",
    theme="soft",
    allow_flagging="never",
)

if __name__ == "__main__":
    # Disable analytics/schema generation to prevent ASGI internal bool errors
    os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
    demo.queue()
    # share=True allows Hugging Face to publicly expose the app (fixes 500 error)
    demo.launch(server_name="0.0.0.0", server_port=7860, show_api=False, share=True)
