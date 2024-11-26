from markdown_parser import extract_title


def main():
    markdown = "# Title\n\nSome text\n\nAnother line"
    title = extract_title(markdown)
    print(title)


if __name__ == "__main__":
    main()
