import os
import shutil

from generate_page import generate_pages_recursive
from copytree import copytree


def main():
    src_dir = "./static"
    dest_dir = "./public"
    template_path = "./template.html"

    print("Deleting public directory...")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    print("Copying static files to public directory...")
    copytree(src_dir, dest_dir)

    dir_path_content = "./content"
    template_path = "./template.html"
    generate_pages_recursive(dir_path_content, template_path, dest_dir)


if __name__ == "__main__":
    main()
