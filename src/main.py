from textwrap import dedent
from markdown_parser import markdown_to_blocks
from split_textnode import *


def main():
    old_nodes = [
        TextNode("Visit [OpenAI](https://openai.com) for AI research.", TextType.TEXT)
    ]
    nodes = split_nodes_link(old_nodes)
    print(nodes)


if __name__ == "__main__":
    main()
