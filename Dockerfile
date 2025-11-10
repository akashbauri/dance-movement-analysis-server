# Use lightweight Python image
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 git && \
    rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for both Gradio and FastAPI
EXPOSE 7860
EXPOSE 8080

# Start both Gradio app and API server (in background)
CMD ["bash", "-c", "python3 app.py & uvicorn api_server:app --host 0.0.0.0 --port 8080"]

