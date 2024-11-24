from textnode import TextNode, TextType
from split_textnode import split_nodes_delimiter


def main():
    node = TextNode(
        "This is text with a `code block` word. Here is another `code block` to test.",
        TextType.TEXT,
    )
    node = TextNode("This is text with a `code block` word.", TextType.TEXT)

    try:
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        for i, node in enumerate(nodes):
            print(f"{i+1}. {node}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
