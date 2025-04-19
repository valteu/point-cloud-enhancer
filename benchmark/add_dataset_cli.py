import argparse
import os
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description="Prepare image dataset.")
    parser.add_argument("name", help="Name of the new dataset (subdirectory under images/)")
    parser.add_argument("images_dir", help="Path to the directory containing images to copy")
    parser.add_argument("benchmark_dataset_name", help="Name of the benchmark dataset under 'data/'")

    args = parser.parse_args()

    dataset_path = os.path.join("data", args.benchmark_dataset_name)
    images_target_dir = os.path.join(dataset_path, "images", args.name)

    if not os.path.isdir(dataset_path):
        print(f"Error: Benchmark dataset directory '{dataset_path}' does not exist.")
        sys.exit(1)

    if os.path.exists(images_target_dir):
        print(f"Error: The directory '{images_target_dir}' already exists.")
        sys.exit(1)

    os.makedirs(images_target_dir, exist_ok=False)

    if not os.path.isdir(args.images_dir):
        print(f"Error: Provided images directory '{args.images_dir}' does not exist.")
        sys.exit(1)

    for filename in os.listdir(args.images_dir):
        src_file = os.path.join(args.images_dir, filename)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, images_target_dir)

    print(f"Images copied successfully to '{images_target_dir}'.")


if __name__ == "__main__":
    main()
