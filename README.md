# Dance Movement Analysis — AI/ML Server

**Goal:** upload a short dance video → server returns a processed video with skeleton overlay (MediaPipe pose).

---

## Files in this repo
- `analyze_dance.py` — core processing using MediaPipe + OpenCV
- `app.py` — FastAPI server exposing `/upload` and `/download/{file_name}`
- `Dockerfile` — containerization
- `requirements.txt`
- `test_analyze.py` — pytest unit test
- `uploads/` and `output/` directories created at runtime

---

## Run locally (quick)
1. Create virtual env and install:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
