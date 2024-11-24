from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode needs a tag.")
        if not self.children:
            raise ValueError("ParentNode needs at least one children node.")

        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
