#!/bin/bash

TAG="latest"
PORT=8080

if [ "$1" ]; then
    TAG="$1"
fi
if [ "$2" ]; then
    PORT="$2"
fi

./build.sh "$TAG"

if [ $? -eq 0 ]; then
    ./run.sh "$PORT"
else
    echo "Error: Docker image build failed. Aborting."
    exit 1
fi
