# Police Transcription & Report Generation Frontend

This is the frontend for the Police Transcription & Report Generation application, built with React and Vite.

## Prerequisites

- Docker

## Setup and Running

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Build the Docker image:
   ```
   docker build -t police-transcription-frontend .
   ```

3. Run the Docker container:
   ```
   docker run -p 5173:5173 police-transcription-frontend
   ```

4. Once the container is running, you can access the application at:
   ```
   http://localhost:5173
   ```

Note: If you have Docker Compose installed, you can use the following command:
```
docker-compose up --build
```

## Development

The application is set up with Vite, which provides fast hot module replacement (HMR). Any changes you make to the source files will be immediately reflected in the browser without a full page reload.

## Project Structure

- `src/`: Contains the source code for the React application
  - `components/`: Reusable React components
  - `pages/`: React components that represent entire pages or views
  - `services/`: Service files for API calls, data processing, etc.
- `public/`: Contains static assets
- `Dockerfile`: Defines the Docker image for the frontend
- `vite.config.ts`: Vite configuration file
- `tsconfig.json`: TypeScript configuration file
- `package.json`: Lists the project dependencies and scripts

## Additional Information

For more detailed information about the project structure and conventions, please refer to the CONVENTIONS.md file in the root directory of the project.

## Vite and React

This project uses Vite as the build tool and development server. Vite offers extremely fast cold starts and instant hot module replacement (HMR). 

React is set up with TypeScript for type safety and better developer experience. The project structure follows React best practices and is ready for scalable application development.
