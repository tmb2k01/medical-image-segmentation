#!/bin/bash

IMAGE_NAME="medical-image-segmentation"
TAG="latest"

if [ "$1" ]; then
    TAG="$1"
fi

echo "Building Docker image: $IMAGE_NAME:$TAG"
docker build -t "$IMAGE_NAME:$TAG" .

if [ $? -eq 0 ]; then
    echo "Docker image $IMAGE_NAME:$TAG built successfully."
else
    echo "Error: Failed to build Docker image."
    exit 1
fi
