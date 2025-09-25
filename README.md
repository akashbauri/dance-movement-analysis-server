Dance Movement Analysis Server
🎯 Project Overview
A cloud-deployed AI/ML server that analyzes body movements from uploaded dance videos using MediaPipe and OpenCV. The system detects dance poses, tracks body keypoints, and provides detailed movement analysis through REST API endpoints.

🏗️ Architecture
Backend: FastAPI with MediaPipe pose detection

Containerization: Docker with multi-stage optimization

Cloud Deployment: Google Cloud Compute Engine (Free Tier)

AI/ML Stack: MediaPipe + OpenCV + NumPy

⚡ Quick Start
Local Development
# Clone repository
git clone <your-repo-url>
cd dance-analysis-server

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
Docker Deployment
bash
# Build container
docker build -t dance-analyzer .

# Run container
docker run -p 8000:8000 dance-analyzer
🌐 API Endpoints
Health Check
text
GET /health
Response: {"status": "healthy", "service": "dance-analysis"}
Video Analysis
text
POST /analyze-dance/
Content-Type: multipart/form-data
Body: video file (mp4, avi, mov)

Response: {
  "video_analysis": {
    "total_frames": 120,
    "frames_with_poses": 85,
    "unique_poses_detected": ["arms_up", "side_stretch", "squat"],
    "pose_descriptions": {...}
  },
  "summary": {
    "analysis_quality": "high",
    "dominant_poses": [...],
    "movement_complexity": "high"
  }
}
🧪 Testing
bash
# Run unit tests
python -m unittest test_analyzer.py

# Test API endpoint
curl -X POST "http://localhost:8000/analyze-dance/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@dance_video.mp4"
🚀 Cloud Deployment
Google Cloud Setup
Create GCP free tier account

Launch e2-micro VM instance (Ubuntu 20.04)

Install Docker on VM

Clone repository and build container

Run with port 8000 exposed

Deployment Commands
bash
# On GCP VM
git clone <repo-url>
cd dance-analys
