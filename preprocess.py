import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 12  # Set the maximum number of threads to use

def run_matlab_script(input_image_path, output_image_path, method):
    """Run the MATLAB script for edge enhancement."""
    matlab_script_dir = "/home/valteu/study/point-cloud-enhancer/image-smoother"  # Set this to the directory containing the smooth_image.m file
    matlab_cmd = (
        f"matlab -batch \"addpath('{matlab_script_dir}'); "
        f"smooth_image('{input_image_path}', '{output_image_path}', '{method}'); "
        f"rmpath('{matlab_script_dir}');\""  # Optionally remove the path after execution
    )
    subprocess.run(matlab_cmd, shell=True)

def run_exposure_correction(dataset_name, lcdpnet_dir, models_dir, input_dir, output_dir):
    """Run the exposure correction."""
    config_file_path = os.path.join(lcdpnet_dir, "src/config/ds/test.yaml")  # Corrected to match your file extension
    
    # Update the test.yaml configuration file
    with open(config_file_path, 'r') as file:
        config_content = file.readlines()
    
    for i, line in enumerate(config_content):
        if 'input:' in line:
            config_content[i + 1] = f"  - ../{input_dir}/*\n"
        if 'GT:' in line:
            config_content[i + 1] = f"  - ../{input_dir}/*\n"
    
    with open(config_file_path, 'w') as file:
        file.writelines(config_content)

    # Run the exposure correction model
    os.chdir(lcdpnet_dir)
    os.environ['HYDRA_FULL_ERROR'] = '1'
    subprocess.run(f"python3 src/test.py checkpoint_path={models_dir}/LCDPNet.ckpt", shell=True)

    # Move the results to the output directory
    results_dir = os.path.join(lcdpnet_dir, 'test_results/LCDPNet.ckpt@lcdp_data.test', dataset_name)
    if os.path.exists(results_dir):
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        shutil.move(results_dir, output_dir)
    else:
        raise FileNotFoundError("Expected results not found. Check if the model ran correctly.")

def process_dataset(dataset_name, datasets_dir, lcdpnet_dir, models_dir):
    # Identify the original dataset directory name
    original_dataset_name = dataset_name
    for suffix in ['_edge_enhanced', '_both_enhanced', '_exposure_corrected']:
        if suffix in dataset_name:
            original_dataset_name = dataset_name.replace(suffix, '')
            break
    
    input_dir = os.path.join(datasets_dir, original_dataset_name, 'input')
    
    # Create directories for enhanced datasets
    enhanced_edge_dir = os.path.join(datasets_dir, original_dataset_name + '_edge_enhanced')
    enhanced_input_dir = os.path.join(enhanced_edge_dir, 'input')
    both_enhanced_dir = os.path.join(datasets_dir, original_dataset_name + '_both_enhanced')
    
    if not os.path.exists(enhanced_input_dir):
        os.makedirs(enhanced_input_dir, exist_ok=True)
    
    # Process each image in the input directory for edge enhancement
    for image_name in os.listdir(input_dir):
        input_image_path = os.path.join(input_dir, image_name)
        edge_enhanced_image_path = os.path.join(enhanced_input_dir, image_name)
        
        # Only process the image if it doesn't already exist in the enhanced directory
        if not os.path.exists(edge_enhanced_image_path):
            print(f"Processing image: {image_name}")
            run_matlab_script(input_image_path, edge_enhanced_image_path, method='LNorm')
        else:
            print(f"Skipping already processed image: {image_name}")
    
    # Use edge enhanced images for exposure correction and store results in both_enhanced_dir
    if not os.path.exists(both_enhanced_dir):
        os.makedirs(both_enhanced_dir, exist_ok=True)
        run_exposure_correction(original_dataset_name, lcdpnet_dir, models_dir, enhanced_input_dir, both_enhanced_dir)


def main():
    datasets_dir = 'datasets'
    lcdpnet_dir = 'LCDPNet'
    models_dir = os.path.join(lcdpnet_dir, 'models')

    dataset_names = [name for name in os.listdir(datasets_dir) if os.path.isdir(os.path.join(datasets_dir, name))]
    max_threads = min(MAX_THREADS, len(dataset_names))  # Replace 4 with your desired number of threads

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_dataset = {executor.submit(process_dataset, name, datasets_dir, lcdpnet_dir, models_dir): name for name in dataset_names}

        for future in as_completed(future_to_dataset):
            dataset_name = future_to_dataset[future]
            try:
                future.result()
                print(f"Processing of dataset {dataset_name} completed successfully.")
            except Exception as exc:
                print(f"Dataset {dataset_name} generated an exception: {exc}")

if __name__ == "__main__":
    main()
