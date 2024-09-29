#!/bin/bash

TAG="latest"

if [ "$1" ]; then
    TAG="$1"
fi

./build.sh "$TAG"

if [ $? -eq 0 ]; then
    ./run.sh
else
    echo "Error: Docker image build failed. Aborting."
    exit 1
fi
