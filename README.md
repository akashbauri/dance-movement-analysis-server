---
title: "💃 Dance Movement Analysis"
emoji: 💫
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: "5.49.1"
app_file: app.py
pinned: false
license: mit
short_description: "AI-based dance pose and movement visualization."
---

# 💃 AI Dance Movement Analysis

Welcome to the **Dance Movement Analysis App**, built using **MediaPipe**, **OpenCV**, and **Gradio**.  
This AI tool detects human body movements and visualizes pose landmarks on dance videos in real time.  

---

## 🧩 **What It Does**
- Detects **33 human body landmarks** using MediaPipe Pose  
- Displays **pose confidence graph** dynamically  
- Shows **real-time FPS (frames per second)**  
- Adds color-coded overlays for accuracy  
- Lets you **download the processed video**

---

## 🎥 **How To Use**
1. Upload your dance video (≤ **2 minutes**, ≤ **25 MB**, MP4 format)  
2. The app analyzes your video frame-by-frame  
3. It highlights your pose, FPS, and confidence live  
4. Download the final analyzed video instantly  

---

## ⚙️ **Tech Stack**
| Tool | Purpose |
|------|----------|
| 🧠 MediaPipe | Pose detection & body landmarks |
| 🎥 OpenCV | Frame processing & visualization |
| 🌐 Gradio | Frontend web interface |
| ⚡ FastAPI + Uvicorn | Backend serving |
| ☁️ Hugging Face Spaces | Hosting & deployment |

---

## 🧠 **How It Works**
1. Each video frame is processed via **MediaPipe Pose**  
2. Landmarks (e.g., elbows, knees, shoulders) are detected  
3. Confidence levels are computed and displayed  
4. FPS and graph overlays show stability and motion flow  
5. The result video can be downloaded via the UI  

---

## 📦 **Requirements**
```bash
gradio==5.49.1
mediapipe==0.10.14
opencv-python==4.9.0.80
numpy==1.26.4
fastapi==0.115.2
uvicorn==0.29.0
spaces
