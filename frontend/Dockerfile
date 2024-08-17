# Use an official Node runtime as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Install Vite globally
RUN npm install -g create-vite

# Create a new Vite project with React and TypeScript
RUN create-vite frontend --template react-ts

# Set the working directory to the new project
WORKDIR /app/frontend

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the app
RUN npm run build

# Expose the port the app runs on
EXPOSE 5173

# Define the command to run the app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
