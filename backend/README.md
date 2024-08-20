# Police Transcription & Report Generation Backend

This is the backend for the Police Transcription & Report Generation project. It's built using FastAPI and Python 3.11.

## Setup

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda or Anaconda)
- [Ollama](https://ollama.com/download) (for running language models)

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

4. Install Ollama:
   - Visit https://ollama.com/download and follow the instructions for your operating system.
   - After installation, run `ollama run llama3.1` to download and test the Llama 3.1 model.

## Running the backend

1. Ensure you're in the backend directory and the Conda environment is activated.

2. Start the FastAPI server:
   ```
   uvicorn src.main:app --reload
   ```

   The `--reload` flag enables hot reloading, which is useful during development.

3. The API will be available at `http://127.0.0.1:8000`.

4. You can access the automatic API documentation at `http://127.0.0.1:8000/docs`.

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

## Configuring Insanely Fast Whisper

Insanely Fast Whisper is already included in the Conda environment. To use it in your code:

```python
from transformers import pipeline
from optimum.bettertransformer import BetterTransformer

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3", device="cuda")
pipe.model = BetterTransformer.transform(pipe.model)

# Use the pipeline for transcription
result = pipe("audio.mp3")
```

## Configuring Ollama

Ollama is installed separately. To use it in your Python code:

```python
import requests

def query_ollama(prompt, model="llama3.1"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt
    })
    return response.json()["response"]

# Example usage
result = query_ollama("Summarize this transcript: ...")
```

Remember to start the Ollama service before using it in your code.
