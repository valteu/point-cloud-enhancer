#!/bin/bash

# Directory containing point cloud files
POINT_CLOUD_DIR="point_clouds"
# Directory to save analysis results
ANALYSIS_OUTPUT_DIR="analysis_results"

# Create the analysis output directory if it doesn't exist
mkdir -p "$ANALYSIS_OUTPUT_DIR"

# Function to analyze a point cloud
analyze_point_cloud() {
    local point_cloud_file=$1
    local output_file=$2

    colmap model_analyzer \
        --path "$point_cloud_file" > "$output_file"

    if [ $? -ne 0 ]; then
        echo "model_analyzer failed for $point_cloud_file" >&2
        return 1
    fi
}

# Loop through each PLY file in the point cloud directory
for point_cloud_file in "$POINT_CLOUD_DIR"/*.ply; do
    # Get the base name of the point cloud file (without the directory and extension)
    base_name=$(basename "$point_cloud_file" .ply)
    # Set the output file path
    output_file="$ANALYSIS_OUTPUT_DIR/${base_name}_analysis.txt"

    # Analyze the point cloud and save the results
    analyze_point_cloud "$point_cloud_file" "$output_file"
done

# Merge all analysis results into a single file
cat "$ANALYSIS_OUTPUT_DIR"/*_analysis.txt > "$ANALYSIS_OUTPUT_DIR/combined_analysis.txt"

echo "All point cloud analyses have been saved to $ANALYSIS_OUTPUT_DIR/combined_analysis.txt"
