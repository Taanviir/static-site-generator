from split_textnode import *


def main():
    old_nodes = [
        TextNode(
            "Here's an image: ![example](https://example.com/image.jpg)",
            TextType.TEXT,
        )
    ]
    new_nodes = split_nodes_image(old_nodes)
    for node in new_nodes:
        print(node)


if __name__ == "__main__":
    main()
