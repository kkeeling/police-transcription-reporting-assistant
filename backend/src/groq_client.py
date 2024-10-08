import os
from dotenv import load_dotenv
from groq import Groq

class GroqClient:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set. Please check your backend/.env file.")
        self.client = Groq(api_key=api_key)

    def transcribe_audio(self, audio_file, language=None):
        try:
            # Create a transcription request
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model="distil-whisper-large-v3-en",
                prompt="Transcribe the following audio for a police report",
                response_format="json",
                language=language or "en",
                temperature=0.0
            )
            
            # Extract the transcription from the response
            return transcription.text
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            raise  # Re-raise the exception to be handled by the caller
