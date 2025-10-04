Dance Movement Analysis Server
🎯 Project Overview
A cloud-deployed AI/ML server that analyzes body movements from uploaded dance videos using MediaPipe and OpenCV. Built with Streamlit for the Callus Company Inc. AI ML Server Engineer competency assessment.

The system detects dance poses, tracks body keypoints, and provides detailed movement analysis through an interactive web interface.

🏗️ Architecture
Frontend: Streamlit web application with file upload

AI/ML Engine: MediaPipe pose detection + OpenCV video processing

Cloud Deployment: Streamlit Community Cloud (100% free)

Processing: Real-time video analysis with progress tracking

⚡ Quick Start
Local Development
bash
# Clone repository
git clone https://github.com/akashbauri/dance-movement-analysis-server.git
cd dance-movement-analysis-server

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
Access Local App
Open browser to: http://localhost:8501

Upload dance videos and get instant analysis

🌐 Live Demo
Streamlit Cloud URL: [Your app will be deployed here]

Features Available:
Video Upload: Drag & drop or browse for dance videos

Real-time Processing: Live progress tracking during analysis

Interactive Results: Visual pose detection summaries

JSON Export: Download detailed analysis results

API Documentation: Complete technical specifications

🔧 Technical Implementation
AI/ML Processing Pipeline:
Video Upload → Streamlit file uploader

Validation → Check file format and size

MediaPipe Analysis → 33-point body landmark detection

Pose Classification → Custom algorithm for dance poses

Results Display → Interactive metrics and visualizations

JSON Export → Structured analysis data

Detected Dance Poses:
Arms Up: Arms raised above shoulders

Side Stretch: Arms extended to sides

Squat: Kn
