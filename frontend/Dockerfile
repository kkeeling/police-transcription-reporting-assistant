# Use an official Node runtime as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Create a new Vite React project
RUN npm create vite@latest . -- --template react-ts

# Install project dependencies
RUN npm install

# Install additional dependencies
RUN npm install react-router-dom @types/react-router-dom

# Expose the port the app runs on
EXPOSE 5173

# Define the command to run the app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
