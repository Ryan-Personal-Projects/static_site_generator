import os
from pathlib import Path
import shutil
from markdown_block import markdown_to_html_node, extract_title

def copy_contents_from_src_to_dest(src, dest):
    """
    Recursively copies the contents of the source directory (`src`) to the destination directory (`dest`).

    If the destination directory does not exist, it is created. All files and subdirectories from the source
    are copied to the destination, preserving the directory structure.

    Args:
        src (str): Path to the source directory.
        dest (str): Path to the destination directory.

    Raises:
        FileNotFoundError: If the source directory does not exist.
        PermissionError: If the operation lacks the necessary permissions.
        OSError: For other OS-related errors during file or directory operations.
    """
    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(src):
        src_full_path = os.path.join(src, item)
        dest_full_path = os.path.join(dest, item)
        print(f"{src_full_path} -> {dest_full_path}")
        if os.path.isfile(src_full_path):
            shutil.copy(src_full_path, dest_full_path)
        else:
            copy_contents_from_src_to_dest(src_full_path, dest_full_path)

def generate_page(from_path, template_path, dest_path, basepath):
    """
    Generates an HTML page from a Markdown source file using a specified HTML template.

    Args:
        from_path (str): Path to the source Markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Destination path for the generated HTML file.
        basepath (str): Base path to use for resolving absolute URLs in href and src attributes.

    The function reads the Markdown content, converts it to HTML, extracts the title,
    and injects both into the template. It also rewrites absolute URLs in the template
    to use the provided basepath. The resulting HTML is written to the destination path,
    creating directories as needed.
    """
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as file_reader:
        md_content = file_reader.read()

    with open(template_path, "r", encoding="utf-8") as file_reader:
        template_content = file_reader.read()

    html_content = markdown_to_html_node(md_content).to_html()
    html_title = extract_title(md_content)

    template_content = template_content.replace("{{ Title }}", html_title)
    template_content = template_content.replace("{{ Content }}", html_content)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file_writer:
        file_writer.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """
    Recursively generates HTML pages from Markdown files in a directory tree using a specified template.
    Args:
        dir_path_content (str): Path to the root directory containing Markdown files and subdirectories.
        template_path (str): Path to the HTML template file to use for page generation.
        dest_dir_path (str): Path to the destination directory where generated HTML files will be saved.
        basepath (str): Base path to be used for relative links or other purposes in page generation.
    Raises:
        FileNotFoundError: If the content directory or template file does not exist.
    """
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError("Invalid path for contents given")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError("Invalid path for template given")

    for item in os.listdir(dir_path_content):
        src_full_path = os.path.join(dir_path_content, item)
        dest_full_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_full_path) and Path(item).suffix == ".md":
            dest_full_path = Path(dest_full_path).with_suffix(".html")
            generate_page(src_full_path, template_path, dest_full_path, basepath)
        else:
            generate_pages_recursive(src_full_path, template_path, dest_full_path, basepath)
    


    