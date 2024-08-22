from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List
import os
import asyncio
import tempfile
from dotenv import load_dotenv
from .groq_client import GroqClient

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Police Transcription & Report Generation API",
    description="API for transcribing audio and generating police reports",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

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

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'mp4', 'mpeg', 'mpga', 'webm'}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

groq_client = None

def initialize_groq_client():
    global groq_client
    try:
        groq_client = GroqClient()
        logger.info("GroqClient initialized successfully")
    except ValueError as e:
        logger.error(f"Error initializing GroqClient: {str(e)}")
        print("ERROR: GROQ_API_KEY environment variable is not set. Please set it in the backend/.env file and restart the application.")

initialize_groq_client()

if not groq_client:
    print("WARNING: The application is running without a valid GROQ_API_KEY. Some features may not work correctly.")

def get_groq_client():
    if not groq_client:
        raise HTTPException(status_code=500, detail="GroqClient is not initialized. Please check your GROQ_API_KEY.")
    return groq_client

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Police Transcription & Report Generation API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if groq_client else "unhealthy",
        "details": "GroqClient not initialized" if not groq_client else None,
        "api_version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.post("/api/v1/upload-audio", response_model=TranscriptionResponse)
async def upload_audio(file: UploadFile = File(...), groq_client: GroqClient = Depends(get_groq_client)):
    logger.info(f"Received file: {file.filename}")
    if not allowed_file(file.filename):
        logger.warning(f"Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file format. Only supported audio files are allowed.")
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        logger.warning(f"File size exceeds limit: {len(content)} bytes")
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 25 MB.")
    
    # Save the file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(content)
    logger.info(f"Temporary file saved: {temp_file_path}")
    
    try:
        logger.info("Starting transcription")
        with open(temp_file_path, "rb") as audio_file:
            transcription = groq_client.transcribe_audio(audio_file, language="en")
        logger.info("Transcription completed")
        
        # Prepare response
        response = TranscriptionResponse(
            text=transcription,
            segments=[]  # Groq API doesn't provide segments, so we're leaving this empty
        )
        
        logger.info(f"Transcription result: {transcription}")
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

@app.websocket("/api/v1/stream-audio")
async def stream_audio(websocket: WebSocket, groq_client: GroqClient = Depends(get_groq_client)):
    await websocket.accept()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file_path = temp_file.name
            logger.info(f"Created temporary file: {temp_file_path}")

            while True:
                audio_chunk = await websocket.receive_bytes()
                if not audio_chunk:
                    break
                temp_file.write(audio_chunk)
                temp_file.flush()

                # Transcribe the accumulated audio
                with open(temp_file_path, "rb") as audio_file:
                    transcription = groq_client.transcribe_audio(audio_file, language="en")

                # Send the transcription back to the client
                await websocket.send_text(transcription)

    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}", exc_info=True)
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Temporary file removed: {temp_file_path}")
        await websocket.close()

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
                with open(temp_file_path, "rb") as audio_file:
                    transcription = groq_client.transcribe_audio(audio_file)
                
                if transcription is None:
                    raise Exception("Transcription failed")
                
                # Prepare and send response
                response = TranscriptionResponse(
                    text=transcription,
                    segments=[]  # Groq API doesn't provide segments, so we're leaving this empty
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

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(title="Police Transcription & Report Generation API", version="1.0.0", routes=app.routes)

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(openapi_url="/openapi.json", title="API Documentation")
