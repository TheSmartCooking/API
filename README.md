# Smart Cooking API

This is the backend API for the Smart Cooking website, providing essential services and data to support website functionality.

## Getting Started

To run the API locally, you’ll need:

- **Docker** to build and run the application in a container.

### Setup Steps

1. **Build the Docker Image**:
   ```bash
   docker build -t smartcooking-flask_api .
   ```
2. **Run the Docker Container**:
   ```bash
   docker run -d -p 5000:5000 --name Smart-Cooking_API smartcooking-flask_api
   ```
3. **Access the API**:
   Open your browser or API client to `http://localhost:5000`.
