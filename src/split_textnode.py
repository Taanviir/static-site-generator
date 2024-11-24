from textnode import TextNode, TextType


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
