from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        if text_type not in TextType:
            raise Exception(f"Invalid type used for text node: {text_type}")

        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        rep_string = f'TextNode("{self.text}", TextType.{self.text_type.value.upper()}'
        if self.url:
            rep_string += f", {self.url}"
        rep_string += ")"
        return rep_string
