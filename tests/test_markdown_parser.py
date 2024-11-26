import unittest
from src import text_to_textnodes, TextNode, TextType, markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
