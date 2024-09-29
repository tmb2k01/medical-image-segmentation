#!/bin/bash

IMAGE_NAME="medical-image-segmentation"
TAG="latest"
CONTAINER_NAME="medical-image-segmentation-container"
INTERACTIVE_MODE="false"

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
    --interactive) INTERACTIVE_MODE="true" ;;
    --tag)
        TAG="$2"
        shift
        ;;
    --port)
        PORT="$2"
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

# Stop any existing container with the same name
docker stop "$CONTAINER_NAME" 2>/dev/null
docker rm "$CONTAINER_NAME" 2>/dev/null

if [ "$INTERACTIVE_MODE" == "true" ]; then
    echo "Running Docker container in interactive mode..."
    docker run -it --rm --name "$CONTAINER_NAME" "$IMAGE_NAME:$TAG"
else
    echo "Running Docker container..."
    docker run --name "$CONTAINER_NAME" "$IMAGE_NAME:$TAG"
fi

if [ $? -eq 0 ]; then
    echo "Docker container $CONTAINER_NAME is running."
    if [ "$INTERACTIVE_MODE" != "true" ]; then
        echo "Check the logs with: docker logs -f $CONTAINER_NAME"
    fi
else
    echo "Error: Failed to run Docker container."
    exit 1
fi
