import os
import subprocess
import sys
import shutil
from itertools import product
from gaussian_splatting.convert_optimization import run_conversion

# Paths
DATASETS_DIR = 'output_glomap'
POINT_CLOUD_METRICS_DIR = './point_cloud_metrics'
CREATE_FEATURES_SCRIPT = os.path.join(POINT_CLOUD_METRICS_DIR, 'create_features.py')
# PROCESSED_DATASETS_DIR = 'processed_datasets'
PROCESSED_DATASETS_DIR = 'output_glomap_processed'
GAUSSIAN_SPLATTING_SCRIPT = 'gaussian_splatting/train.py'

# Create the output directories if they don't exist
os.makedirs(PROCESSED_DATASETS_DIR, exist_ok=True)

# Desired combinations and corresponding datasets
desired_combinations = {
    'bin_new_medium': [
        (False, False, False),
    ],
    'both_pingpong': [
        (False, False, False),
    ],
    'both_playroom': [
        (False, False, False),
    ],
    'drjohnson': [
        (False, False, False),
    ],
    'exposure_pingpong': [
        (False, False, False),
    ]
}

def copy_all_data(source_dir, dest_dir):
    """Copy all necessary images and files to the destination directory."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        if os.path.isdir(source_item):
            # If it's a directory, manually merge the directories
            if not os.path.exists(dest_item):
                shutil.copytree(source_item, dest_item)
            else:
                copy_all_data(source_item, dest_item)
        else:
            # If it's a file, simply copy it
            shutil.copy2(source_item, dest_item)

def run_create_features(directory):
    create_features_command = [sys.executable, CREATE_FEATURES_SCRIPT, directory]
    result = subprocess.run(create_features_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"create_features.py failed for {directory} with error: {result.stderr}")
    return result.returncode

def run_gaussian_splatting(dataset_dir, output_dir):
    subprocess.run(['python3', GAUSSIAN_SPLATTING_SCRIPT, '-s', dataset_dir, '--eval', '-m', output_dir])

def main():
    dataset_dirs = [os.path.join(DATASETS_DIR, d) for d in os.listdir(DATASETS_DIR) if os.path.isdir(os.path.join(DATASETS_DIR, d))]

    for dataset_dir in dataset_dirs:
        dataset_name = os.path.basename(dataset_dir)
        if dataset_name not in desired_combinations:
            continue
        
        print(f"Processing dataset: {dataset_dir}")

        for param_set in desired_combinations[dataset_name]:
            guided_matching, estimate_affine_shape, domain_size_pooling = param_set
            param_str = f"guided_{guided_matching}_affine_{estimate_affine_shape}_dsp_{domain_size_pooling}"
            processed_dir = os.path.join(PROCESSED_DATASETS_DIR, f"{dataset_name}_{param_str}")

            print(f"Running conversion with parameters: {param_str}")
            
            # Step 1: Copy all necessary data to the new directory
            copy_all_data(dataset_dir, processed_dir)
            
            # Step 2: Run convert_optimization.py to create the point clouds in the new directory
            if run_conversion(processed_dir, "colmap", "magick", "OPENCV", False, False, guided_matching, estimate_affine_shape, domain_size_pooling, False) != 0:
                continue
            
            # Step 3: Run create_features.py to compute metrics in the new directory
            # if run_create_features(processed_dir) != 0:
                # continue
            
            # Step 4: Run Gaussian splatting on the created dataset
            # run_gaussian_splatting(processed_dir, processed_dir)

if __name__ == '__main__':
    main()
