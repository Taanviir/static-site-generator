import unittest
from src import (
    HTMLNode,
    LeafNode,
    TextNode,
    TextType,
    text_node_to_html_node,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_leafnode(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_invalid_type(self):
        with self.assertRaises(Exception) as context:
            TextNode("Invalid type", "unknown")
        self.assertIn("Invalid type used for text node", str(context.exception))


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        """Test with plain text without any special formatting."""
        text = "This is a plain text."
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is a plain text.", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_bold_text(self):
        """Test text with bold formatting."""
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_italic_text(self):
        """Test text with italic formatting."""
        text = "This is *italic* text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_code_text(self):
        """Test text with inline code formatting."""
        text = "This is `code` text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_image(self):
        """Test text with an embedded image."""
        text = "This is an image ![alt text](url)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_link(self):
        """Test text with a hyperlink."""
        text = "This is a [link](http://example.com)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_combined_formatting(self):
        """Test text with multiple formatting types."""
        text = "This is **bold** and *italic* with a `code` example."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" example.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)


class TestGetMarkdownBlocks(unittest.TestCase):
    def test_basic_markdown(self):
        """Test splitting a basic Markdown string with multiple blocks."""
        markdown = """\
# Heading

This is a paragraph.

* List item 1
* List item 2
"""
        expected = ["# Heading", "This is a paragraph.", "* List item 1\n* List item 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_markdown(self):
        """Test an empty Markdown string."""
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_only_whitespace(self):
        """Test a Markdown string with only whitespace."""
        markdown = "   \n\n  \n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_trailing_newlines(self):
        """Test a Markdown string with trailing newlines."""
        markdown = """\
# Heading

Paragraph with text.

"""
        expected = ["# Heading", "Paragraph with text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_empty_lines(self):
        """Test a Markdown string with multiple consecutive empty lines."""
        markdown = """\
# Heading


This is a paragraph.


* List item 1


* List item 2
"""
        expected = [
            "# Heading",
            "This is a paragraph.",
            "* List item 1",
            "* List item 2",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_no_double_newlines(self):
        """Test a Markdown string without any double newlines."""
        markdown = """\
# Heading
This is a paragraph.
* List item 1
* List item 2
"""
        expected = ["# Heading\nThis is a paragraph.\n* List item 1\n* List item 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), "heading")
        self.assertEqual(block_to_block_type("### Subheading"), "heading")

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), "code")

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> Quote\n> Another line"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\n3. Third"), "ordered_list"
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a normal paragraph."), "paragraph"
        )
        self.assertEqual(
            block_to_block_type("Random text\nwith multiple lines"), "paragraph"
        )


def node_to_dict(node):
    """Convert an HTMLNode or LeafNode to a dictionary for comparison."""
    if isinstance(node, LeafNode):
        return {
            "type": "LeafNode",
            "tag": node.tag,
            "value": node.value,
            "props": node.props,
        }
    elif isinstance(node, HTMLNode):
        return {
            "type": "HTMLNode",
            "tag": node.tag,
            "value": node.value,
            "children": [node_to_dict(child) for child in node.children],
        }
    return None


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_simple_heading(self):
        """Test a simple heading without inline formatting."""
        markdown = "# Simple Heading"
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            None,
            children=[
                HTMLNode("h1", children=[LeafNode(None, "Simple Heading")]),
            ],
        )
        self.assertEqual(node_to_dict(html_node), node_to_dict(expected))

    def test_heading_with_inline_formatting(self):
        """Test a heading with inline formatting."""
        markdown = "# This is **bold** and *italic*"
        html_node = markdown_to_html_node(markdown)
        expected = HTMLNode(
            "div",
            None,
            children=[
                HTMLNode(
                    "h1",
                    children=[
                        LeafNode(None, "This is "),
                        LeafNode("b", "bold"),
                        LeafNode(None, " and "),
                        LeafNode("i", "italic"),
                    ],
                )
            ],
        )
        self.assertEqual(node_to_dict(html_node), node_to_dict(expected))


if __name__ == "__main__":
    unittest.main()
