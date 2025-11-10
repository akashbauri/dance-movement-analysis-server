from fastapi import FastAPI, UploadFile, File
import uvicorn
import shutil
from analyze_dance import process_video

app = FastAPI(title="AI Dance Movement API", description="Body pose and movement analysis API", version="1.0")

@app.post("/analyze/")
async def analyze_video(file: UploadFile = File(...)):
    input_path = f"uploads/{file.filename}"
    output_path = f"outputs/processed_{file.filename}"

    # Save uploaded video
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run analysis
    process_video(input_path, output_path)

    return {"message": "Analysis complete", "output_file": output_path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
