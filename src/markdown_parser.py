from split_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Invalid type used for text node: {text_node.text_type}")


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
    elif all(
        line.strip().startswith(f"{i}. ")
        for i, line in enumerate(block.splitlines(), start=1)
    ):
        return "ordered_list"
    return "paragraph"


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        leaf_nodes.append(html_node)
    return leaf_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                heading_level = block.count("#", 0, block.index(" "))
                text = block[heading_level + 1 :].strip()
                node = HTMLNode(f"h{heading_level}", children=text_to_children(text))
            case "code":
                code_content = block.strip("```").strip()
                code = HTMLNode("code", children=text_to_children(code_content))
                node = HTMLNode("pre", children=[code])
            case "quote":
                quote_content = "\n".join(
                    line[1:].strip() for line in block.splitlines()
                )
                node = HTMLNode("blockquote", children=text_to_children(quote_content))
            case "unordered_list":
                items = [line.strip() for line in block.splitlines()]
                list_items = [
                    HTMLNode("li", children=text_to_children(item[2:]))
                    for item in items
                ]
                node = HTMLNode("ul", children=list_items)
            case "ordered_list":
                items = [line.strip() for line in block.splitlines()]
                list_items = [
                    HTMLNode(
                        "li", children=text_to_children(item[item.index(".") + 2 :])
                    )
                    for item in items
                ]
                node = HTMLNode("ol", children=list_items)
            case "paragraph":
                node = HTMLNode("p", children=text_to_children(block))
        nodes.append(node)

    return HTMLNode("div", None, nodes)
