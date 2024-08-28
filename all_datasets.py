import os
import argparse
import subprocess

def process_datasets(datasets_dir, operation):
    # Check if the datasets directory exists
    if not os.path.exists(datasets_dir):
        raise ValueError(f"Datasets directory {datasets_dir} does not exist.")

    # Iterate through all the directories in the datasets directory
    for dataset_name in os.listdir(datasets_dir):
        dataset_path = os.path.join(datasets_dir, dataset_name)

        # Ensure it's a directory
        if os.path.isdir(dataset_path):
            print(f"Processing dataset: {dataset_name}")
            # Define the command to run Dataset.py with the appropriate arguments
            command = [
                'python3', 'Dataset.py',
                '--path', dataset_path,
                '--operation', operation,
                '--output_path', dataset_path
            ]

            # Run the command using subprocess
            try:
                subprocess.run(command, check=True)
                print(f"Finished processing dataset: {dataset_name}\n")
            except subprocess.CalledProcessError as e:
                print(f"Error processing dataset {dataset_name}: {e}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Dataset Processing Tool")
    parser.add_argument('--datasets_dir', type=str,
                        default=os.path.join(os.path.dirname(__file__), 'datasets'),
                        help="The path to the directory containing all datasets (default: 'datasets' in the script's directory).")
    parser.add_argument('--operation', type=str, required=True,
                        choices=['convert', 'create_ply', 'train_gs', 'edge_enhance', 'exposure_correct'],
                        help="The operation to perform on all datasets.")

    args = parser.parse_args()
    process_datasets(args.datasets_dir, args.operation)
