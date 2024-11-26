import unittest
from src import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is an image: ![Alt text](https://example.com/image.jpg)"
        expected = [("Alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = """
        Here is the first image: ![Image 1](https://example.com/image1.jpg).
        Here is the second image: ![Image 2](https://example.com/image2.jpg).
        """
        expected = [
            ("Image 1", "https://example.com/image1.jpg"),
            ("Image 2", "https://example.com/image2.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This text contains no images or Markdown image syntax."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_image_syntax(self):
        text = """
        Malformed image syntax: ![Alt text](https://example.com/image.jpg.
        Missing alt text: ![](https://example.com/image.jpg).
        """
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_text_with_special_characters(self):
        text = """
        Special characters in alt text: ![Alt!@#$%^&*()_+](https://example.com/image.jpg).
        Special characters in URL: ![Alt text](https://example.com/im@g3.jpg).
        """
        expected = [
            ("Alt!@#$%^&*()_+", "https://example.com/image.jpg"),
            ("Alt text", "https://example.com/im@g3.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_text(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "Here is a link: [Example](https://example.com)."
        expected = [("Example", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = """
        Here is the first link: [Google](https://google.com).
        Here is another: [GitHub](https://github.com).
        """
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "This text contains no Markdown links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_images_not_included(self):
        text = """
        This is an image: ![Alt text](https://example.com/image.jpg).
        This is a link: [Link text](https://example.com).
        """
        expected = [("Link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_malformed_link_syntax(self):
        text = """
        Malformed link: [Example](https://example.com.
        Missing text: [](https://example.com).
        """
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_special_characters_in_links(self):
        text = """
        Special characters: [Check this! @#$%^&*()](https://example.com/special?param=value&other=1).
        """
        expected = [
            ("Check this! @#$%^&*()", "https://example.com/special?param=value&other=1")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_text(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_without_url(self):
        text = """
        Missing URL: [Example]().
        """
        expected = [("Example", "")]
        self.assertEqual(extract_markdown_links(text), expected)


if __name__ == "__main__":
    unittest.main()
