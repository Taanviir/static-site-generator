from split_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    split_functions = [
        lambda n: split_nodes_delimiter(n, "**", TextType.BOLD),
        lambda n: split_nodes_delimiter(n, "*", TextType.ITALIC),
        lambda n: split_nodes_delimiter(n, "`", TextType.CODE),
        split_nodes_image,
        split_nodes_link,
    ]

    for function in split_functions:
        nodes = function(nodes)

    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks


def block_to_block_type(block: str) -> str:
    if block.startswith(tuple("#" * i + " " for i in range(1, 7))):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in block.splitlines()):
        return "quote"
    elif all(line.startswith(("- ", "* ")) for line in block.splitlines()):
        return "unordered_list"
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(block.splitlines(), start=1)):
        return "ordered_list"
    return "paragraph"
