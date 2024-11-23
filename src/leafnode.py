from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None) -> None:
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value.")
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
