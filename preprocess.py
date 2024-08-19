import os
import shutil
import subprocess

def run_matlab_script(input_image_path, output_image_path, method):
    """Run the MATLAB script for edge enhancement."""
    matlab_cmd = f"matlab -batch \"smooth_image('{input_image_path}', '{output_image_path}', '{method}')\""
    subprocess.run(matlab_cmd, shell=True)

def run_exposure_correction(dataset_name, lcdpnet_dir, models_dir):
    """Run the exposure correction."""
    config_file_path = os.path.join(lcdpnet_dir, "src/config/ds/test.yml")
    
    # Update the test.yml configuration file
    with open(config_file_path, 'r') as file:
        config_content = file.readlines()
    
    for i, line in enumerate(config_content):
        if 'input:' in line:
            config_content[i + 1] = f"  - {dataset_name}/input/*\n"
        if 'GT:' in line:
            config_content[i + 1] = f"  - {dataset_name}/input/*\n"
    
    with open(config_file_path, 'w') as file:
        file.writelines(config_content)

    # Run the exposure correction model
    os.chdir(lcdpnet_dir)
    os.environ['HYDRA_FULL_ERROR'] = '1'
    subprocess.run(f"python3 src/test.py checkpoint_path={models_dir}/LCDPNet.ckpt", shell=True)

    # Move the results to the dataset directory
    results_dir = os.path.join(lcdpnet_dir, 'test_results/LCDPNet.ckpt@lcdp_data.test', dataset_name)
    if os.path.exists(results_dir):
        target_dir = os.path.join('datasets', dataset_name + '_exposure_corrected')
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.move(results_dir, target_dir)
    else:
        raise FileNotFoundError("Expected results not found. Check if the model ran correctly.")

def process_dataset(dataset_name, datasets_dir, lcdpnet_dir, models_dir):
    input_dir = os.path.join(datasets_dir, dataset_name, 'input')
    
    # Create directories for enhanced datasets
    enhanced_edge_dir = os.path.join(datasets_dir, dataset_name + '_edge_enhanced')
    os.makedirs(enhanced_edge_dir, exist_ok=True)
    
    both_enhanced_dir = os.path.join(datasets_dir, dataset_name + '_both_enhanced')
    os.makedirs(both_enhanced_dir, exist_ok=True)
    
    # Process each image in the input directory
    for image_name in os.listdir(input_dir):
        input_image_path = os.path.join(input_dir, image_name)
        edge_enhanced_image_path = os.path.join(enhanced_edge_dir, image_name)
        both_enhanced_image_path = os.path.join(both_enhanced_dir, image_name)
        
        # Apply edge enhancement
        run_matlab_script(input_image_path, edge_enhanced_image_path, method='LNorm')
        
        # Apply both edge enhancement and exposure correction
        run_matlab_script(input_image_path, both_enhanced_image_path, method='LNorm')
    
    # Apply exposure correction and save results
    run_exposure_correction(dataset_name, lcdpnet_dir, models_dir)

    # Move exposure corrected images to their respective folders
    exposure_corrected_dir = os.path.join(datasets_dir, dataset_name + '_exposure_corrected')
    os.makedirs(exposure_corrected_dir, exist_ok=True)

    for image_name in os.listdir(enhanced_edge_dir):
        image_path = os.path.join(enhanced_edge_dir, image_name)
        shutil.copy(image_path, both_enhanced_dir)

def main():
    datasets_dir = './datasets'
    lcdpnet_dir = './LCDPNet'
    models_dir = os.path.join(lcdpnet_dir, 'models')
    
    for dataset_name in os.listdir(datasets_dir):
        dataset_path = os.path.join(datasets_dir, dataset_name)
        if os.path.isdir(dataset_path):
            process_dataset(dataset_name, datasets_dir, lcdpnet_dir, models_dir)

if __name__ == "__main__":
    main()
