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
            # Read the audio file content
            audio_content = audio_file.read()
            
            # Create a chat completion request with the audio content
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that transcribes audio. The user will provide audio content, and you should return the transcription."
                    },
                    {
                        "role": "user",
                        "content": f"Please transcribe the following audio content: {audio_content}"
                    }
                ],
                model="mixtral-8x7b-32768",
                max_tokens=1024,
            )
            
            # Extract the transcription from the response
            transcription = chat_completion.choices[0].message.content
            return transcription
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None
