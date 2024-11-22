import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_tag_value_and_props(self):
        """Test LeafNode with a tag, value, and props."""
        node = LeafNode(tag="span", value="Leaf content", props={"class": "leaf-class"})
        self.assertEqual(repr(node), '<span class="leaf-class">Leaf content</span>')

    def test_leaf_node_without_props(self):
        """Test LeafNode with only a tag and value, no props."""
        node = LeafNode(tag="p", value="Leaf content")
        self.assertEqual(repr(node), "<p>Leaf content</p>")

    def test_leaf_node_repr_with_attributes(self):
        """Test repr output includes attributes when props are provided."""
        node = LeafNode(
            tag="a",
            value="Link",
            props={"href": "https://example.com", "target": "_blank"},
        )
        self.assertEqual(
            repr(node), '<a href="https://example.com" target="_blank">Link</a>'
        )

    def test_leaf_node_empty_props(self):
        """Test LeafNode with empty props."""
        node = LeafNode(tag="p", value="Empty props", props={})
        self.assertEqual(repr(node), "<p>Empty props</p>")


if __name__ == "__main__":
    unittest.main()
