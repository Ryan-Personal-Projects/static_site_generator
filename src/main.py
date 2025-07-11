import os
import sys
import shutil
from util import copy_contents_from_src_to_dest, generate_pages_recursive

root_dir_path = os.path.dirname(os.path.abspath(__file__)) + "/.."
dir_path_static = root_dir_path + "/static"
dir_path_docs = root_dir_path + "/docs"
dir_path_content = root_dir_path + "/content"
dir_path_template = root_dir_path + "/template.html"
default_basepath = "/"

def main():
    """
    Main entry point for the static site generator.

    - Determines the base path from command-line arguments or uses the default.
    - Deletes the existing 'docs' directory if it exists.
    - Copies static files from the static directory to the 'docs' directory.
    - Generates HTML pages from markdown content using the specified template.

    Raises:
        Any exceptions raised by file operations or page generation functions.
    """
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_contents_from_src_to_dest(dir_path_static, dir_path_docs)

    print("Creating html file from markdown...")
    generate_pages_recursive(
        dir_path_content, 
        dir_path_template, 
        dir_path_docs,
        basepath
    )

if __name__ == "__main__":
    main()