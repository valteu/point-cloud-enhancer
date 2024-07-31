import os
import subprocess
import sys

# Paths
DATASETS_DIR = 'datasets'
CONVERT_SCRIPT = './gaussian-splatting/convert_optimization.py'
POINT_CLOUD_METRICS_DIR = './point_cloud_metrics'
CREATE_FEATURES_SCRIPT = os.path.join(POINT_CLOUD_METRICS_DIR, 'create_features.py')
TEST_MODEL_SCRIPT = os.path.join(POINT_CLOUD_METRICS_DIR, 'test_model.py')

def run_convert(source_path):
    convert_command = [
        sys.executable, CONVERT_SCRIPT,
        "--source_path", source_path,
        "--colmap_executable", "colmap",
        "--magick_executable", "magick",
        "--camera", "OPENCV"
    ]
    result = subprocess.run(convert_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"convert_optimization.py failed for {source_path} with error: {result.stderr}")
    return result.returncode

def run_create_features(directory):
    create_features_command = [sys.executable, CREATE_FEATURES_SCRIPT, directory]
    result = subprocess.run(create_features_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"create_features.py failed for {directory} with error: {result.stderr}")
    return result.returncode

def run_test_model(directory):
    test_model_command = [sys.executable, TEST_MODEL_SCRIPT, directory]
    result = subprocess.run(test_model_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"test_model.py failed for {directory} with error: {result.stderr}")
    return result.returncode

def main():
    dataset_dirs = [os.path.join(DATASETS_DIR, d) for d in os.listdir(DATASETS_DIR) if os.path.isdir(os.path.join(DATASETS_DIR, d))]

    for dataset_dir in dataset_dirs:
        print(f"Processing dataset: {dataset_dir}")
        
        # Step 1: Run convert_optimization.py to create the point clouds
        # if run_convert(dataset_dir) != 0:
            # continue
        
        # Step 2: Run create_features.py to compute metrics
        if run_create_features(dataset_dir) != 0:
            continue
        
        # Step 3: Run test_model.py to test the model and get scores
        if run_test_model(dataset_dir) != 0:
            continue

if __name__ == '__main__':
    main()
