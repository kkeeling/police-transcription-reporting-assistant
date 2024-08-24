from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, Depends, Request, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import List
import os
import asyncio
import tempfile
from dotenv import load_dotenv
from .groq_client import GroqClient
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import json
import wave
import io

# Load environment variables
load_dotenv()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Police Transcription & Report Generation API",
    description="API for transcribing audio and generating police reports",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


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
@limiter.limit("10/minute")
async def read_root(request: Request):
    return {"message": "Welcome to the Police Transcription & Report Generation API"}

@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    return {
        "status": "healthy" if groq_client else "unhealthy",
        "details": "GroqClient not initialized" if not groq_client else None,
        "api_version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.post("/api/v1/upload-audio", response_model=TranscriptionResponse)
@limiter.limit("5/minute")
async def upload_audio(request: Request, file: UploadFile = File(...), groq_client: GroqClient = Depends(get_groq_client)):
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
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            retry_after = http_exc.headers.get("Retry-After", "60")
            logger.warning(f"Rate limit exceeded. Retry after: {retry_after} seconds")
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded", "retry_after": retry_after}
            )
        raise
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
    temp_file_path = None
    try:
        while True:
            try:
                audio_chunk = await asyncio.wait_for(websocket.receive_bytes(), timeout=5.0)
                if not audio_chunk:
                    break

                # Convert the audio chunk to WAV format
                wav_data = io.BytesIO()
                with wave.open(wav_data, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(16000)  # 16kHz
                    wav_file.writeframes(audio_chunk)

                # Create a new temporary file for each chunk
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file_path = temp_file.name
                    logger.info(f"Created temporary file: {temp_file_path}")
                    temp_file.write(wav_data.getvalue())
                    temp_file.flush()

                # Transcribe the audio chunk
                with open(temp_file_path, "rb") as audio_file:
                    transcription = groq_client.transcribe_audio(audio_file, language="en")

                # Send the transcription back to the client
                if transcription.strip():  # Only send non-empty transcriptions
                    await websocket.send_json({"status": "success", "transcription": transcription})

                # Clean up temporary file
                os.remove(temp_file_path)
                logger.info(f"Temporary file removed: {temp_file_path}")

            except asyncio.TimeoutError:
                # No data received for 5 seconds, send a keep-alive message
                await websocket.send_json({"status": "keep-alive"})
            except HTTPException as http_exc:
                if http_exc.status_code == 429:
                    retry_after = http_exc.headers.get("Retry-After", "60")
                    logger.warning(f"Rate limit exceeded. Retry after: {retry_after} seconds")
                    await websocket.send_json({
                        "status": "error",
                        "detail": "Rate limit exceeded",
                        "retry_after": retry_after
                    })
                else:
                    raise

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}", exc_info=True)
        await websocket.send_json({"status": "error", "message": str(e)})
    finally:
        # Ensure any remaining temporary file is cleaned up
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Temporary file removed: {temp_file_path}")

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

