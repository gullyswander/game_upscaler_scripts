import json
import os
from pathlib import Path


def get_file_creation_time(file_path):
    return os.path.getctime(file_path)


def find_nearest_file(file_path
                      , directory_path):
    target_time = get_file_creation_time(file_path)
    min_diff = float('inf')
    nearest_file = None
    for filename in os.listdir(directory_path):
        current_file_path = os.path.join(directory_path, filename)
        current_time = get_file_creation_time(current_file_path)
        time_diff = abs(target_time - current_time)

        if time_diff < min_diff and current_file_path != file_path:
            min_diff = time_diff
            nearest_file = current_file_path

    return nearest_file


def scan_directory_for_images(directory_path):
    """
    Scans the specified directory for PNG and JPG files.

    :param directory_path: Path to the directory to scan.
    :return: A list of paths to the detected image files.
    """
    image_files = []
    valid_extensions = ('.png', '.jpg', '.jpeg')

    # Convert the directory_path to a Path object if it's not already one
    directory = Path(directory_path)

    # Iterate over all files in the directory
    for file_path in directory.iterdir():
        # Check if the file has a valid extension and is a file, not a directory
        if file_path.suffix.lower() in valid_extensions and file_path.is_file():
            # Append the file path to the list
            image_files.append(str(file_path))

    return image_files


def open_ignore_file(textures_to_ignore_filepath):
    if os.path.isfile(textures_to_ignore_filepath):
        with open(textures_to_ignore_filepath, 'r') as f:
            files_to_ignore = set(json.load(f))
    else:
        files_to_ignore = set()
    return files_to_ignore

def write_ignore_file(textures_to_ignore_filepath, files_to_ignore):
    with open(textures_to_ignore_filepath, 'w') as f:
        json.dump(list(files_to_ignore), f)

import pkgutil
import importlib

def list_modules_in_package(package_name):
    try:
        # Import the package
        package = importlib.import_module(package_name)

        # List all modules in the package
        modules = []
        for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            modules.append(module_name)

        return modules
    except ImportError as e:
        print(f"Error importing package: {e}")
        return []
