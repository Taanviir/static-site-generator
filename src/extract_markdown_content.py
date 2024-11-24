import re


def extract_markdown_images(text: str) -> list[tuple]:
    pattern = r"!\[([^\[\]]+)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    pattern = r"(?<!!)\[([^\[\]]+)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
