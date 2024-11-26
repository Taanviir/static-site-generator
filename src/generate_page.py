import os
import pathlib
from markdown_parser import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)

    template = template.replace(" {{ Title }} ", title, 1)
    template = template.replace("{{ Content }}", html, 1)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as index_file:
        index_file.write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(file_path):
            dest_path = pathlib.Path(dest_path).with_suffix(".html")
            generate_page(file_path, template_path, dest_path)
        else:
            generate_pages_recursive(file_path, template_path, dest_path)
