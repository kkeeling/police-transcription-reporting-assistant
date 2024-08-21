from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import asyncio
import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

app = FastAPI()

# We'll initialize the model in the transcription function

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

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/v1/upload-audio", response_model=TranscriptionResponse)
async def upload_audio(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    if not allowed_file(file.filename):
        logger.warning(f"Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file format. Only MP3 and WAV files are allowed.")
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        logger.warning(f"File size exceeds limit: {len(content)} bytes")
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 10 MB.")
    
    # Save the file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(content)
    logger.info(f"Temporary file saved: {temp_file_path}")
    
    try:
        logger.info("Initializing pipeline")
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3",
            torch_dtype=torch.float16,
            device="cuda:0" if torch.cuda.is_available() else "cpu",
            model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
        )

        logger.info("Starting transcription")
        result = pipe(
            temp_file_path,
            chunk_length_s=30,
            batch_size=24,
            return_timestamps=True,
            language='en',  # Always translate to English
        )
        logger.info("Transcription completed")
        
        # Prepare response
        response = TranscriptionResponse(
            text=result["text"],
            segments=[{
                "start": segment["timestamp"][0],
                "end": segment["timestamp"][1],
                "text": segment["text"]
            } for segment in result["chunks"]]
        )
        
        logger.info("Returning response")
        return response
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Temporary file removed: {temp_file_path}")

@app.websocket("/api/v1/transcribe-stream")
async def transcribe_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        # Initialize the pipeline
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3",
            torch_dtype=torch.float16,
            device="cuda:0" if torch.cuda.is_available() else "cpu",
            model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
        )

        while True:
            audio_data = await websocket.receive_bytes()
            
            # Save the audio data to a temporary file
            temp_file_path = "temp_audio.wav"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(audio_data)
            
            try:
                # Transcribe audio
                result = pipe(
                    temp_file_path,
                    chunk_length_s=30,
                    batch_size=24,
                    return_timestamps=True,
                    language='en',  # Always translate to English
                )
                
                # Prepare and send response
                response = TranscriptionResponse(
                    text=result["text"],
                    segments=[{
                        "start": segment["timestamp"][0],
                        "end": segment["timestamp"][1],
                        "text": segment["text"]
                    } for segment in result["chunks"]]
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
