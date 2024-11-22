class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict[str, str] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        attributes = ""
        if self.props:
            for key, value in self.props.items():
                attributes += f' {key}="{value}"'
        return attributes

    def __repr__(self) -> str:
        children_repr = "".join([repr(child) for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{self.value or ''}{children_repr}</{self.tag}>"
