import unittest
from src import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_simple_node(self):
        """Test a basic node with a tag and value, but no children or attributes."""
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(repr(node), "<p>Hello, world!</p>")

    def test_node_with_attributes(self):
        """Test a node with attributes and no children."""
        node = HTMLNode(
            tag="div", value="Content", props={"class": "container", "id": "main"}
        )
        self.assertEqual(repr(node), '<div class="container" id="main">Content</div>')

    def test_node_with_children(self):
        """Test a node with children but no value."""
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(
            tag="div", children=[child1, child2], props={"class": "parent"}
        )
        expected = '<div class="parent"><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(repr(parent), expected)

    def test_nested_children(self):
        """Test a node with nested children."""
        nested_child = HTMLNode(tag="i", value="Nested")
        child = HTMLNode(tag="span", children=[nested_child])
        parent = HTMLNode(tag="div", children=[child])
        expected = "<div><span><i>Nested</i></span></div>"
        self.assertEqual(repr(parent), expected)

    def test_empty_node(self):
        """Test an empty node (no tag, value, children, or attributes)."""
        node = HTMLNode()
        self.assertEqual(repr(node), "<None></None>")

    def test_node_with_value_and_children(self):
        """Test a node that has both value and children."""
        child = HTMLNode(tag="span", value="Child")
        parent = HTMLNode(tag="div", value="Parent", children=[child])
        expected = "<div>Parent<span>Child</span></div>"
        self.assertEqual(repr(parent), expected)


if __name__ == "__main__":
    unittest.main()
