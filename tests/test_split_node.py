import unittest
from textnode import TextNode, TextType
from src.split_textnode import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
)


class TestSplitNodeFunction(unittest.TestCase):
    def test_split_single_node(self):
        # Test splitting a single node
        node = TextNode("This is text with a `code block` word.", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_no_delimiter(self):
        # Test input with no delimiter
        node = TextNode("This text has no delimiters.", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("This text has no delimiters.", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_multiple_delimiters(self):
        # Test input with multiple delimiters
        node = TextNode("Text with `code1` and `code2` here.", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_unclosed_delimiter(self):
        # Test unclosed delimiter (should raise an exception)
        node = TextNode("Text with `unclosed code block.", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(str(context.exception), "Open delimiter detected!")

    def test_mixed_nodes(self):
        # Test mixed text types
        nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("`code1`", TextType.CODE),
            TextNode(" and more text.", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        # Since the second node is already of type CODE, it should not be split.
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("`code1`", TextType.CODE),
            TextNode(" and more text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_input(self):
        # Test empty input
        nodes = []
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_only_delimiters(self):
        # Test input with only delimiters
        node = TextNode("```", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(str(context.exception), "Open delimiter detected!")


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        old_nodes = [
            TextNode(
                "Visit [OpenAI](https://openai.com) for AI research.", TextType.TEXT
            )
        ]
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            TextNode(" for AI research.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    def test_multiple_links(self):
        old_nodes = [
            TextNode(
                "Links: [Google](https://google.com) and [GitHub](https://github.com).",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode("Links: ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    def test_no_links(self):
        old_nodes = [TextNode("This text has no links.", TextType.TEXT)]
        expected = [TextNode("This text has no links.", TextType.TEXT)]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    def test_text_with_nested_and_incorrect_links(self):
        old_nodes = [
            TextNode(
                "Check [this link](https://example.com and some broken text.",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode(
                "Check [this link](https://example.com and some broken text.",
                TextType.TEXT,
            )
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        old_nodes = [
            TextNode(
                "Here's an image: ![example](https://example.com/image.jpg)",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode("Here's an image: ", TextType.TEXT),
            TextNode("example", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    def test_multiple_images(self):
        old_nodes = [
            TextNode(
                "Images: ![img1](https://example.com/1.jpg) and ![img2](https://example.com/2.jpg).",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode("Images: ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/2.jpg"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    def test_no_images(self):
        old_nodes = [TextNode("This text has no images.", TextType.TEXT)]
        expected = [TextNode("This text has no images.", TextType.TEXT)]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    def test_text_with_nested_and_incorrect_images(self):
        old_nodes = [
            TextNode(
                "Here's a broken image syntax: ![alt text(https://example.com).",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode(
                "Here's a broken image syntax: ![alt text(https://example.com).",
                TextType.TEXT,
            )
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)


if __name__ == "__main__":
    unittest.main()
