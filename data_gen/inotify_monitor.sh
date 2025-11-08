#!/bin/bash

# Directory to watch
WATCH_DIR="/data/data_gen/file"

# Use inotifywait to get the latest file moved into the directory
LATEST_FILE=$(inotifywait -q -e moved_to --format '%w%f' "$WATCH_DIR" | head -n 1)

# Print the latest file path
echo "$LATEST_FILE"
