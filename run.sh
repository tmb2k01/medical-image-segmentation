#!/bin/bash

IMAGE_NAME="medical-image-segmentation"
TAG="latest"
CONTAINER_NAME="medical-image-segmentation-container"
PORT=8080

if [ "$1" ]; then
    PORT="$1"
fi

# Stop any existing container with the same name
docker stop "$CONTAINER_NAME" 2>/dev/null
docker rm "$CONTAINER_NAME" 2>/dev/null

echo "Running Docker container from image: $IMAGE_NAME:$TAG"
docker run -d --name "$CONTAINER_NAME" -p "$PORT":8080 "$IMAGE_NAME:$TAG"

if [ $? -eq 0 ]; then
    echo "Docker container $CONTAINER_NAME is running on port $PORT."
else
    echo "Error: Failed to run Docker container."
    exit 1
fi
