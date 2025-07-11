import os
import sys
import shutil
from util import copy_contents_from_src_to_dest, generate_pages_recursive

root_dir_path = os.path.dirname(os.path.abspath(__file__)) + "/.."
dir_path_static = root_dir_path + "/static"
dir_path_docs = root_dir_path + "/docs"
dir_path_content = root_dir_path + "/content"
dir_path_template = root_dir_path + "/template.html"

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    """
    Main function to generate the static site.

    This function performs the following steps:
    1. Deletes the existing 'docs' directory if it exists.
    2. Copies static files from the static directory to the 'docs' directory.
    3. Generates HTML files from markdown content using the provided templates.

    Assumes the following variables are defined in the global scope:
    - dir_path_docs: Path to the output 'docs' directory.
    - dir_path_static: Path to the static files directory.
    - dir_path_content: Path to the markdown content directory.
    - dir_path_template: Path to the HTML templates directory.
    - basepath: Base path for the generated site.
    """
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