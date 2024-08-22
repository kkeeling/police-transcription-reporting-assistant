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
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                language=language,
                response_format="text"
            )
            return transcription.text
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None
