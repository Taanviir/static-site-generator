from textnode import TextNode, TextType
from extract_markdown_content import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:

    new_nodes = []

    def split_node(node: TextNode) -> None:
        text = node.text
        while delimiter in text:
            before, wanted, after = text.split(delimiter, 2)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            if wanted:
                new_nodes.append(TextNode(wanted, text_type))
            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("Open delimiter detected!")
            split_node(node)
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_by_pattern(
    old_nodes: list[TextNode], extract_func: callable, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        if not text:
            continue

        matches = extract_func(node.text)
        if not matches:
            new_nodes.append(node)
        else:
            start = 0
            for match in matches:
                if text_type == TextType.LINK:
                    link_syntax = f"[{match[0]}]({match[1]})"
                elif text_type == TextType.IMAGE:
                    link_syntax = f"![{match[0]}]({match[1]})"
                else:
                    raise ValueError("Unsupported text type passed.")

                match_start = text.find(link_syntax, start)

                if match_start == -1:
                    continue

                match_end = match_start + len(link_syntax)

                if start < match_start:
                    before_text = text[start:match_start]
                    new_nodes.append(TextNode(before_text, TextType.TEXT))

                new_nodes.append(TextNode(match[0], text_type, match[1]))

                start = match_end

            if start < len(text):
                after_text = text[start:]
                new_nodes.append(TextNode(after_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_pattern(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_pattern(old_nodes, extract_markdown_links, TextType.LINK)
