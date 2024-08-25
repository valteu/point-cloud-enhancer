import os
import argparse
import subprocess
import shutil

class Dataset:
    def __init__(self, path):
        self.path = path

    def convert(self, output_path=None):
        print(f"Converting dataset at {self.path}.")
        convert_script = os.path.join(os.path.dirname(__file__), "convert.py")
        subprocess.run(f"python3 {convert_script}", shell=True)

    def create_ply(self, output_path=None):
        print(f"Creating PLY files for dataset at {self.path}.")
        create_ply_script = os.path.join(os.path.dirname(__file__), "create_ply.py")
        if output_path is None:
            output_path = self.path
        subprocess.run(f"python3 {create_ply_script} -s {self.path} -m {output_path}", shell=True)

    def train_gs(self, output_path=None):
        print(f"Training Gaussian Splatting on dataset at {self.path}.")
        train_script = os.path.join(os.path.dirname(__file__), "train.py")
        if output_path is None:
            output_path = self.path
        subprocess.run(f"python3 {train_script} -s {self.path} -m {output_path}", shell=True)

    def edge_enhance(self, output_path=None):
        print(f"Enhancing edges on dataset at {self.path}.")
        if output_path is None:
            output_path = self.path

        # Ensure the output directory exists
        input_dir = os.path.join(output_path, 'input')
        os.makedirs(input_dir, exist_ok=True)

        # Run the MATLAB script for edge enhancement
        matlab_script_dir = os.path.join(os.path.dirname(__file__), "image_smoother")
        matlab_cmd = (
            f"matlab -batch \"addpath('{matlab_script_dir}'); "
            f"smooth_image('{os.path.join(self.path, 'input')}', '{input_dir}', 'LNorm'); "
            f"rmpath('{matlab_script_dir}');\""
        )
        subprocess.run(matlab_cmd, shell=True)

    @staticmethod
    def update_config(input_dir, config_path):
        with open(config_path, 'r') as file:
            config_content = file.readlines()

        for i, line in enumerate(config_content):
            if 'input:' in line:
                config_content[i + 1] = f"  - {input_dir}/*\n"
            if 'GT:' in line:
                config_content[i + 1] = f"  - {input_dir}/*\n"

        with open(config_path, 'w') as file:
            file.writelines(config_content)

    def exposure_correct(self, output_path=None):
        try:
            os.environ['HYDRA_FULL_ERROR'] = '1'

            # Update paths to be relative to the script directory
            script_dir = os.path.dirname(__file__)
            config_path = os.path.join(script_dir, 'LCDPNet', 'src', 'config', 'ds', 'test.yaml')
            output_subdir = os.path.join(script_dir, 'models', 'test_result', 'lcdpnet_models_LCDPNet.ckpt@lcdp_data.test')

            # Determine input and output directories
            input_dir = os.path.join(self.path, 'input')
            if output_path is None:
                output_path = self.path

            output_input_dir = os.path.join(output_path, 'input')

            # Update the config file
            self.update_config(input_dir, config_path)

            # Remove the test_result directory if it exists
            if os.path.exists(output_subdir):
                shutil.rmtree(output_subdir)

            # Print the current input and output dataset name
            print(f"Running exposure correction pipeline with input: {input_dir} and output: {output_input_dir}")

            # Run the subprocess command for LCDPNet with automated "ENTER" input
            subprocess.run("python3 LCDPNet/src/test.py checkpoint_path=models/LCDPNet.ckpt", shell=True, check=True, input='\n', text=True)

            # Create output directory if it does not exist
            if not os.path.exists(output_input_dir):
                os.makedirs(output_input_dir)

            # Copy results directly from output_subdir to output_dir
            for file in os.listdir(output_subdir):
                if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    shutil.copy(os.path.join(output_subdir, file), output_input_dir)

            # Optional: Delete the test_result directory after processing
            if os.path.exists(output_subdir):
                shutil.rmtree(output_subdir)

        except subprocess.CalledProcessError as e:
            print(f"Error running exposure correction for {self.path}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Dataset Processing Tool")

    parser.add_argument('--name', type=str, help="The name of the dataset.")
    parser.add_argument('--path', type=str, help="The full path to the dataset.")
    parser.add_argument('--operation', type=str, required=True, choices=['convert', 'create_ply', 'train_gs', 'edge_enhance', 'exposure_correct'], help="The operation to perform on the dataset.")
    parser.add_argument('--output_path', type=str, help="Optional: The output path for the operation results.")

    args = parser.parse_args()

    # Determine the dataset path
    if args.path:
        dataset_path = args.path
    elif args.name:
        dataset_path = os.path.join(*[os.path.dirname(__file__), 'datasets', args.name])
    else:
        raise ValueError("You must specify either --name or --path to locate the dataset.")

    # Create the Dataset instance
    dataset = Dataset(dataset_path)

    # Map operations to class methods
    operation_map = {
        'convert': dataset.convert,
        'create_ply': dataset.create_ply,
        'train_gs': dataset.train_gs,
        'edge_enhance': dataset.edge_enhance,
        'exposure_correct': dataset.exposure_correct,
    }

    # Execute the requested operation
    operation_func = operation_map[args.operation]
    operation_func(args.output_path)

if __name__ == '__main__':
    main()
