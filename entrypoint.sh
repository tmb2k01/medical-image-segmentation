#!/bin/bash

if [ -t 0 ]; then
    echo "Running in interactive mode. Skipping CMD."
    exec bash
else
    echo "Running in non-interactive mode. Executing CMD..."
    exec python src/main.py
fi
