import os
import shutil

def move_images_to_input(base_directory):
    # Iterate over all directories within the base directory
    for root, dirs, files in os.walk(base_directory):
        # Create a list to store subdirectories that are to be ignored in the next walk
        ignore_dirs = []
        
        for directory in dirs:
            # Define the path of the current directory
            current_dir = os.path.join(root, directory)
            
            # Skip any 'input' directories
            if directory == 'input':
                continue
            
            # Create an 'input' directory within the current directory
            input_dir = os.path.join(current_dir, 'input')
            if not os.path.exists(input_dir):
                os.makedirs(input_dir)
            
            # Move all files from the current directory to the 'input' directory
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                
                # Check if it is a file (and not the 'input' directory itself)
                if os.path.isfile(item_path):
                    shutil.move(item_path, os.path.join(input_dir, item))
            
            # Add the created input_dir to the ignore list
            ignore_dirs.append('input')
        
        # Update the dirs list to exclude the input directories in the next walk
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

base_directory = './datasets/tandt_db_degraded'
move_images_to_input(base_directory)
