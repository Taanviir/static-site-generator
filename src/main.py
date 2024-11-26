import os
import shutil

from generate_page import generate_page
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

    from_dir = "./content"
    template_path = "./template.html"

    generate_page(
        os.path.join(from_dir, "index.md"),
        template_path,
        os.path.join(dest_dir, "index.html"),
    )


if __name__ == "__main__":
    main()
