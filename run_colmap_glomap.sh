#!/bin/bash

# Set the base directories
DATA_DIR="./output_glomap/"
OUTPUT_DIR="./output_glomap/"

# Create output directory if it doesn't exist
# mkdir -p "$OUTPUT_DIR"

# Iterate over each dataset in the data directory
for dataset in "$DATA_DIR"/*; do
  if [ -d "$dataset" ]; then
    # Define paths
    DATASET_NAME=$(basename "$dataset")
    IMAGE_PATH="$dataset/input"
    DATABASE_PATH="$dataset/database.db"
    OUTPUT_PATH="$OUTPUT_DIR/$DATASET_NAME/sparse"
    
    # Run COLMAP feature extraction
    colmap feature_extractor \
      --image_path "$IMAGE_PATH" \
      --database_path "$DATABASE_PATH"

    # Run COLMAP exhaustive matcher
    colmap exhaustive_matcher \
      --database_path "$DATABASE_PATH"
    
    # Run GloMap mapper
    # glomap mapper \
      # --database_path "$DATABASE_PATH" \
      # --image_path "$IMAGE_PATH" \
      # --output_path "$OUTPUT_PATH"
    
    echo "Processing completed for $DATASET_NAME"
  fi
done

echo "All datasets have been processed."
