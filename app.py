import gradio as gr
from analyze_dance import process_video
import os
import shutil

# Function to analyze dance and return downloadable output
def analyze_dance(video_path):
    output_path = "output.mp4"
    process_video(video_path, output_path)

    # Create downloadable copy
    download_path = "analyzed_dance.mp4"
    shutil.copy(output_path, download_path)

    return output_path, "✅ Dance analysis complete! Pose landmarks visualized successfully.", download_path


# Create Gradio interface
with gr.Blocks(title="💃 AI Dance Movement Analyzer") as demo:
    gr.Markdown(
        """
        # 💃 **Dance Movement Analysis with AI**
        Upload your dance video (≤ 2 minutes, ≤ 25 MB) to visualize pose detection and motion accuracy using **MediaPipe Pose**.
        This app:
        - Detects body landmarks in real-time
        - Displays FPS (performance)
        - Shows pose confidence graph per frame
        - Generates downloadable analyzed video

        🧠 **Powered by:** OpenCV + MediaPipe + Gradio  
        👨‍💻 **Created by:** [Akash Bauri](https://huggingface.co/akashbauri)
        """
    )

    with gr.Row():
        video_input = gr.Video(label="🎥 Upload MP4 Dance Video (≤2 minutes, ≤25 MB)")
        output_video = gr.Video(label="🧩 Processed Output with Pose Analysis")

    status = gr.Textbox(label="📊 Processing Status", interactive=False)
    download_btn = gr.File(label="⬇️ Download Processed Video")

    analyze_button = gr.Button("🚀 Start Analysis", variant="primary")

    analyze_button.click(
        fn=analyze_dance,
        inputs=[video_input],
        outputs=[output_video, status, download_btn],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
