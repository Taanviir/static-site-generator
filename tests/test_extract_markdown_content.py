from src.extract_markdown_content import extract_markdown_images, extract_markdown_links

import unittest


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
