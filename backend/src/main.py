from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import openai_whisper as whisper
import asyncio

app = FastAPI()

# Load Whisper model globally
model = whisper.load_model("base")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TranscriptionResponse(BaseModel):
    text: str
    segments: List[dict]

ALLOWED_EXTENSIONS = {'mp3', 'wav'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Police Transcription & Report Generation API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/upload-audio", response_model=TranscriptionResponse)
async def upload_audio(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format. Only MP3 and WAV files are allowed.")
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 10 MB.")
    
    # Save the file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(content)
    
    try:
        # Load Whisper model
        model = whisper.load_model("base")
        
        # Transcribe audio
        result = model.transcribe(temp_file_path)
        
        # Prepare response
        response = TranscriptionResponse(
            text=result["text"],
            segments=[{
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            } for segment in result["segments"]]
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.websocket("/api/v1/transcribe-stream")
async def transcribe_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            
            # Save the audio data to a temporary file
            temp_file_path = "temp_audio.wav"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(audio_data)
            
            try:
                # Transcribe audio
                result = model.transcribe(temp_file_path)
                
                # Prepare and send response
                response = TranscriptionResponse(
                    text=result["text"],
                    segments=[{
                        "start": segment["start"],
                        "end": segment["end"],
                        "text": segment["text"]
                    } for segment in result["segments"]]
                )
                await websocket.send_json(response.dict())
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            
            # Small delay to prevent overwhelming the server
            await asyncio.sleep(0.1)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
