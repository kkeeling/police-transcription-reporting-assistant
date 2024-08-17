# Police Transcription & Report Generation Frontend

This is the frontend for the Police Transcription & Report Generation application.

## Prerequisites

- Docker
- Docker Compose

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

3. Build and run the Docker container:
   ```
   docker-compose up --build
   ```

4. Once the container is running, you can access the application at:
   ```
   http://localhost:5173
   ```

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
