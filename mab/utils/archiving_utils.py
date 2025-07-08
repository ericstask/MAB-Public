import os
import shutil

def safe_move(source_path, destination_folder):
    base_name = os.path.basename(source_path)
    name, extension = os.path.splitext(base_name)

    destination = os.path.join(destination_folder, base_name)
    counter = 2

    while os.path.exists(destination):
        new_name = f"{name} ({counter}){extension}"
        destination = os.path.join(destination_folder, new_name)
        counter += 1

    shutil.move(source_path, destination)
