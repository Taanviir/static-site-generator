import unittest
from textnode import TextNode, TextType
from src.split_textnode import split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()
