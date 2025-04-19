import argparse
import os
import subprocess
import sys


def run_command(command, cwd=None):
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, check=True, cwd=cwd)


def process_dataset(benchmark_dataset_name, image_type):
    print("==============================================")
    print(f"Processing MODEL_DATASET: {benchmark_dataset_name} with IMAGE_TYPE: {image_type}")
    print("==============================================")

    project_path = f"data/{benchmark_dataset_name}"
    database_path = f"{project_path}/database_{benchmark_dataset_name}.db"
    image_path = f"{project_path}/images/{image_type}"
    manual_sparse_model = f"{project_path}/manual_sparse_model"
    triangulated_model = f"{project_path}/triangulated_model_{image_type}"
    dense_workspace = f"{project_path}/undistorted_model_{image_type}"

    os.makedirs(triangulated_model, exist_ok=True)
    os.makedirs(dense_workspace, exist_ok=True)

    # Step 1: Matching
    run_command([
        "colmap", "exhaustive_matcher",
        "--database_path", database_path
    ])

    # Step 2: Triangulate sparse points
    run_command([
        "colmap", "point_triangulator",
        "--database_path", database_path,
        "--image_path", image_path,
        "--input_path", manual_sparse_model,
        "--output_path", triangulated_model
    ])

    # Step 3: Undistort images
    run_command([
        "colmap", "image_undistorter",
        "--image_path", image_path,
        "--input_path", triangulated_model,
        "--output_path", dense_workspace
    ])

    # Step 4: PatchMatch stereo
    run_command([
        "colmap", "patch_match_stereo",
        "--workspace_path", dense_workspace,
        "--PatchMatchStereo.filter", "true"
    ])

    # Step 5: Stereo fusion
    run_command([
        "colmap", "stereo_fusion",
        "--workspace_path", dense_workspace,
        "--output_path", f"{dense_workspace}/fused.ply"
    ])

    print(f"Finished processing {benchmark_dataset_name} with {image_type}.\n")


def main():
    parser = argparse.ArgumentParser(description="Run COLMAP pipeline on benchmark dataset.")
    parser.add_argument("benchmark_dataset_name", help="Name of the benchmark dataset under 'data/'")
    parser.add_argument("name", help="Subdirectory inside images/ that identifies the image type")

    args = parser.parse_args()

    dataset_dir = os.path.join("data", args.benchmark_dataset_name)
    images_dir = os.path.join(dataset_dir, "images", args.name)

    # Check if required directories exist
    if not os.path.isdir(dataset_dir):
        print(f"Error: Dataset directory '{dataset_dir}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(images_dir):
        print(f"Error: Image directory '{images_dir}' does not exist.")
        sys.exit(1)

    # Process the dataset
    process_dataset(args.benchmark_dataset_name, args.name)


if __name__ == "__main__":
    main()
