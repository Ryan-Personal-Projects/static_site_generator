import os
import shutil
from util import copy_contents_from_src_to_dest, generate_pages_recursive

root_dir_path = os.path.dirname(os.path.abspath(__file__)) + "/.."
dir_path_static = root_dir_path + "/static"
dir_path_public = root_dir_path + "/public"
dir_path_content = root_dir_path + "/content"
dir_path_template = root_dir_path + "/template.html"


def main():
    """
    Main function to generate the static site.

    This function performs the following steps:
    1. Deletes the existing public directory if it exists.
    2. Copies static files from the static directory to the public directory.
    3. Recursively generates HTML pages from markdown content using the specified template.
    """
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_contents_from_src_to_dest(dir_path_static, dir_path_public)

    print("Creating html file from markdown...")
    generate_pages_recursive(
        dir_path_content, 
        dir_path_template, 
        dir_path_public
    )

if __name__ == "__main__":
    main()