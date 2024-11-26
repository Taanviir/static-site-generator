from markdown_parser import markdown_to_html_node
from copytree import copytree
import os


def main():
    src_dir = "./static/"
    copytree(src_dir, "./public/")


if __name__ == "__main__":
    main()
