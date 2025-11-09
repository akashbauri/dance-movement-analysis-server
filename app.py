# app.py
import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from analyze_dance import process_video

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Dance Movement Analysis API")


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Accepts a video file, saves it, runs the pose overlay processing,
    and returns the path to the processed video.
    """
    # Basic validation
    if not file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use mp4/mov/avi/mkv.")

    uid = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"{uid}_{file.filename}"
    output_path = OUTPUT_DIR / f"{uid}_processed.mp4"

    # Save uploaded file
    with input_path.open("wb") as f:
        content = await file.read()
        f.write(content)

    # Process
    try:
        frames, fps = process_video(str(input_path), str(output_path))
    except Exception as e:
        # remove input file to save space on failure
        try:
            input_path.unlink(missing_ok=True)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

    return {"status": "success", "frames_processed": frames, "fps": fps, "download": f"/download/{output_path.name}"}


@app.get("/download/{file_name}")
def download_result(file_name: str):
    path = OUTPUT_DIR / file_name
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="video/mp4", filename=file_name)


@app.get("/")
def root():
    return {"message": "Dance Movement Analysis API. POST /upload with form-data 'file'."}
