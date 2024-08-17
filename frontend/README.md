# Police Transcription & Report Generation Frontend

This is the frontend for the Police Transcription & Report Generation application.

## Prerequisites

- Docker

## Setup and Running

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Navigate to the frontend directory:
   ```
   cd frontend
   ```

3. Build the Docker image:
   ```
   docker build -t police-transcription-frontend .
   ```

4. Run the Docker container:
   ```
   docker run -p 5173:5173 police-transcription-frontend
   ```

5. Once the container is running, you can access the application at:
   ```
   http://localhost:5173
   ```

Note: If you have Docker Compose installed, you can use the following command instead of steps 3 and 4:
```
docker-compose up --build
```

If you don't have Docker Compose and want to install it, follow these steps:
1. Visit the official Docker Compose installation guide: https://docs.docker.com/compose/install/
2. Follow the instructions for your operating system to install Docker Compose.

## Development

The application is set up with hot-reloading. Any changes you make to the source files will automatically trigger a rebuild, and you'll see the changes reflected in the browser.

## Project Structure

- `src/`: Contains the source code for the React application
  - `components/`: Reusable React components
  - `pages/`: React components that represent entire pages or views
  - `services/`: Service files for API calls, data processing, etc.
- `public/`: Contains static assets
- `Dockerfile`: Defines the Docker image for the frontend
- `package.json`: Lists the project dependencies and scripts

## Additional Information

For more detailed information about the project structure and conventions, please refer to the CONVENTIONS.md file in the root directory of the project.
