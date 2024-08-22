# Police Transcription & Report Generation Backend

This is the backend for the Police Transcription & Report Generation project. It's built using FastAPI and Python 3.11.

## Setup

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda or Anaconda)
- [Groq API Key](https://console.groq.com/) (for accessing Groq services)

### Setting up the development environment

1. Clone the repository and navigate to the backend directory:
   ```
   git clone <repository-url>
   cd <repository-name>/backend
   ```

2. Create the Conda environment:
   ```
   conda env create -f environment.yml
   ```

3. Activate the Conda environment:
   ```
   conda activate police-transcription-backend
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`:
     ```
     cp .env.example .env
     ```
   - Open the `.env` file and replace `your_groq_api_key_here` with your actual Groq API key.

## Running the backend

1. Ensure you're in the backend directory and the Conda environment is activated.

2. Make sure your `.env` file is properly configured with your Groq API key.

3. Start the FastAPI server:
   ```
   uvicorn src.main:app --reload
   ```

   The `--reload` flag enables hot reloading, which is useful during development.

4. The API will be available at `http://127.0.0.1:8000`.

5. You can access the automatic API documentation at `http://127.0.0.1:8000/docs`.

## Development

- The main application file is `src/main.py`.
- Add new routes and functionality in separate files within the `src` directory and import them in `main.py`.
- Update `environment.yml` if you add new dependencies.

## Testing

To run the test script for Insanely Fast Whisper:
```
python tests/test_whisper.py
```

## Deployment

(Add information about deployment process once it's established)

## Using the Groq API

The Groq API is used for audio transcription. The `GroqClient` class in `src/groq_client.py` handles the interaction with the Groq API. Here's a basic example of how it's used in the code:

```python
from src.groq_client import GroqClient

groq_client = GroqClient()

# Transcribe an audio file
with open("audio_file.mp3", "rb") as audio_file:
    transcription = groq_client.transcribe_audio(audio_file)

print(transcription)
```

Make sure your Groq API key is correctly set in the `.env` file for this to work.

## Environment Variables

The following environment variables are used in this project:

- `GROQ_API_KEY`: Your Groq API key for accessing Groq services.

These should be set in the `.env` file in the backend directory. Never commit the `.env` file with actual API keys to version control.
