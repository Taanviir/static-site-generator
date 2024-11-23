import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_to_leafnode(self):
        node = TextNode("Normal text", TextType.TEXT)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("", "Normal text"))

    def test_bold_to_leafnode(self):
        node = TextNode("Bold text", TextType.BOLD)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("b", "Bold text"))

    def test_italic_to_leafnode(self):
        node = TextNode("Italic text", TextType.ITALIC)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("i", "Italic text"))

    def test_code_to_leafnode(self):
        node = TextNode("Code snippet", TextType.CODE)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf, LeafNode("code", "Code snippet"))

    def test_link_to_leafnode(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        leaf = text_node_to_html_node(node)
        self.assertEqual(
            leaf, LeafNode("a", "Click here", {"href": "https://example.com"})
        )

    def test_image_to_leafnode(self):
        node = TextNode("An image", TextType.IMAGE, "https://example.com/image.png")
        leaf = text_node_to_html_node(node)
        self.assertEqual(
            leaf,
            LeafNode(
                "img", "", {"src": "https://example.com/image.png", "alt": "An image"}
            ),
        )

    def test_invalid_type(self):
        with self.assertRaises(Exception) as context:
            TextNode("Invalid type", "unknown")
        self.assertIn("Invalid type used for text node", str(context.exception))


if __name__ == "__main__":
    unittest.main()
