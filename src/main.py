from text_to_textnodes import text_to_textnodes


def main():
    text = "This is an image ![alt text](url)."
    nodes = text_to_textnodes(text)
    for node in nodes:
        print(node)


if __name__ == "__main__":
    main()
