from extract_markdown_content import extract_markdown_images


def main():
    text = """
        Malformed image syntax: ![Alt text](https://example.com/image.jpg.
        Missing alt text: ![](https://example.com/image.jpg).
        """
    print(extract_markdown_images(text))


if __name__ == "__main__":
    main()
