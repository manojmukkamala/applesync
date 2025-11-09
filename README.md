# applesync
A REST API server to store data (Messages and Health app etc) fetched from Apple devices

## Docker Deployment

You can run the application using Docker:

```bash
# Pull the image from GitHub Container Registry
docker pull ghcr.io/manojmukkamala/applesync:latest

# Run the container
docker run -p 8000:8000 ghcr.io/manojmukkamala/applesync:latest
```

The application will be accessible at `http://localhost:8000`.

FastAPI swagger docs will be accessible at `http://localhost:8000/docs`.

## CI/CD

The application is automatically built and published to GitHub Container Registry on every tagged release on the main branch.
