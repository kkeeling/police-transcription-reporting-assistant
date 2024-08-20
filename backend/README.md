# Police Transcription & Report Generation Backend

This is the backend for the Police Transcription & Report Generation project. It's built using FastAPI and Python 3.11.

## Setup

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda or Anaconda)

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

(Add information about running tests once they are set up)

## Deployment

(Add information about deployment process once it's established)
