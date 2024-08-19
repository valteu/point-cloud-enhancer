#!/bin/bash

SOURCE_DIR="./output_glomap/"
BACKUP_DIR="./output_glomap_colmap_stage/"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Monitor all directories and subdirectories for file creation and moves
inotifywait -m -r -e create -e moved_to "$SOURCE_DIR" --format '%w%f' | while read NEW_FILE
do
    # Ensure that the directory structure is replicated in the backup directory
    DIR_PATH=$(dirname "$NEW_FILE")
    RELATIVE_PATH="${DIR_PATH#$SOURCE_DIR}"
    BACKUP_PATH="$BACKUP_DIR$RELATIVE_PATH"

    # Create the same subdirectory structure in the backup directory
    mkdir -p "$BACKUP_PATH"

    # Copy the new or moved file to the corresponding location in the backup directory
    cp -r "$NEW_FILE" "$BACKUP_PATH"
done
