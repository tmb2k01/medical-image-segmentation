#!/bin/bash

IMAGE_NAME="medical-image-segmentation"
TAG="latest"
CONTAINER_NAME="medical-image-segmentation-container"
INTERACTIVE_MODE=""

show_help() {
    echo "Usage: ./run.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --interactive          Run the container in interactive mode."
    echo "  --tag <tag>            Specify the image tag (default: latest)."
    echo "  -h, --help             Show this help message."
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
    --interactive) INTERACTIVE_MODE="-it" ;;
    --tag)
        TAG="$2"
        shift
        ;;
    -h | --help)
        show_help
        exit 0
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
    shift
done

docker stop "$CONTAINER_NAME" 2>/dev/null
docker rm "$CONTAINER_NAME" 2>/dev/null

if [ -n "$INTERACTIVE_MODE" ]; then
    echo "Running Docker container in interactive mode..."
else
    echo "Running Docker container..."
fi

docker run $INTERACTIVE_MODE --shm-size=4g \
    -v $(pwd)/data:/medical-image-segmentation/data \
    -v $(pwd)/model:/medical-image-segmentation/model \
    --rm --name "$CONTAINER_NAME" "$IMAGE_NAME:$TAG"

if [ $? -eq 0 ]; then
    echo "Docker container $CONTAINER_NAME is running."
else
    echo "Error: Failed to run Docker container."
    exit 1
fi
