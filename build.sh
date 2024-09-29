#!/bin/bash

IMAGE_NAME="medical-image-segmentation"
TAG="latest"

if [ "$1" ]; then
    TAG="$1"
fi

EXISTING_IMAGE=$(docker images -q "$IMAGE_NAME:$TAG")
if [ -n "$EXISTING_IMAGE" ]; then
    echo "Removing Docker image: $IMAGE_NAME:$TAG"
    docker rmi -f "$IMAGE_NAME:$TAG" 2>/dev/null
fi

echo "Building Docker image: $IMAGE_NAME:$TAG"
docker build -t "$IMAGE_NAME:$TAG" .

if [ $? -eq 0 ]; then
    echo "Docker image $IMAGE_NAME:$TAG built successfully."
else
    echo "Error: Failed to build Docker image."
    exit 1
fi
