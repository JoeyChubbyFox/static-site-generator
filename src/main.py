from textnode import TextNode, TextType

import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

"""
def copy_directory_recursive(src, dest):
    # Recursively copies all contents from src (static) to dest (public).
    # It first deletes all contents in the destination directory to ensure a clean copy.
    # Logs each copied file.
    
    # Ensure the source directory exists
    if not os.path.exists(src):
        print(f"Source directory does not exist: {src}")
        return
    
    # Remove destination directory to ensure a clean copy
    if os.path.exists(dest):
        print(f"Deleting existing destination directory: {dest}")
        shutil.rmtree(dest)

    # Create the destination directory
    os.mkdir(dest)

    # Iterate through all items in the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            # Copy file and log the action
            shutil.copy(src_path, dest_path)
            print(f"Copied file: {src_path} -> {dest_path}")

        elif os.path.isdir(src_path):
            # Recursively copy the subdirectory
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_directory_recursive(src_path, dest_path)
"""

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

if __name__ == "__main__":
    main()
