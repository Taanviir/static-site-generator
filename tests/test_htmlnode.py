import unittest
from src import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_simple_node(self):
        """Test a basic node with a tag and value, but no children or attributes."""
        node = HTMLNode(tag="p", value="Hello, world!")
        expected = "HTMLNode(p, Hello, world!, children: [], {})"
        self.assertEqual(repr(node), expected)

    def test_node_with_attributes(self):
        """Test a node with attributes and no children."""
        node = HTMLNode(
            tag="div", value="Content", props={"class": "container", "id": "main"}
        )
        expected = (
            "HTMLNode(div, Content, children: [], {'class': 'container', 'id': 'main'})"
        )
        self.assertEqual(repr(node), expected)

    def test_node_with_children(self):
        """Test a node with children but no value."""
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(
            tag="div", children=[child1, child2], props={"class": "parent"}
        )
        expected = "HTMLNode(div, None, children: [HTMLNode(span, Child 1, children: [], {}), HTMLNode(span, Child 2, children: [], {})], {'class': 'parent'})"
        self.assertEqual(repr(parent), expected)

    def test_nested_children(self):
        """Test a node with nested children."""
        nested_child = HTMLNode(tag="i", value="Nested")
        child = HTMLNode(tag="span", children=[nested_child])
        parent = HTMLNode(tag="div", children=[child])
        expected = "HTMLNode(div, None, children: [HTMLNode(span, None, children: [HTMLNode(i, Nested, children: [], {})], {})], {})"
        self.assertEqual(repr(parent), expected)

    def test_empty_node(self):
        """Test an empty node (no tag, value, children, or attributes)."""
        node = HTMLNode()
        expected = "HTMLNode(None, None, children: [], {})"
        self.assertEqual(repr(node), expected)

    def test_node_with_value_and_children(self):
        """Test a node that has both value and children."""
        child = HTMLNode(tag="span", value="Child")
        parent = HTMLNode(tag="div", value="Parent", children=[child])
        expected = "HTMLNode(div, Parent, children: [HTMLNode(span, Child, children: [], {})], {})"
        self.assertEqual(repr(parent), expected)


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_tag_value_and_props(self):
        """Test LeafNode with a tag, value, and props."""
        node = LeafNode(tag="span", value="Leaf content", props={"class": "leaf-class"})
        self.assertEqual(
            repr(node), "LeafNode(span, Leaf content, {'class': 'leaf-class'})"
        )

    def test_leaf_node_without_props(self):
        """Test LeafNode with only a tag and value, no props."""
        node = LeafNode(tag="p", value="Leaf content")
        self.assertEqual(repr(node), "LeafNode(p, Leaf content, {})")

    def test_leaf_node_repr_with_attributes(self):
        """Test repr output includes attributes when props are provided."""
        node = LeafNode(
            tag="a",
            value="Link",
            props={"href": "https://example.com", "target": "_blank"},
        )
        self.assertEqual(
            repr(node),
            "LeafNode(a, Link, {'href': 'https://example.com', 'target': '_blank'})",
        )

    def test_leaf_node_empty_props(self):
        """Test LeafNode with empty props."""
        node = LeafNode(tag="p", value="Empty props", props={})
        self.assertEqual(repr(node), "LeafNode(p, Empty props, {})")


class TestParentNode(unittest.TestCase):
    def test_parentnode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parentnode_grandchild(self):
        grandchild_node = LeafNode("a", "Click here", {"href": "https://www.boot.dev/"})
        child_node = ParentNode("h1", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><h1><a href="https://www.boot.dev/">Click here</a></h1></div>',
        )

    def test_parentnode_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parentnode_mixed_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = ParentNode("span", [LeafNode(None, "Nested span text")])
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>Bold text</b><span>Nested span text</span></div>",
        )

    def test_parentnode_missing_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "Text")]).to_html()
        with self.assertRaises(ValueError):
            ParentNode("", [LeafNode("b", "Text")]).to_html()

    def test_parentnode_with_attributes(self):
        attributes = {"class": "container", "id": "main"}
        parent_node = ParentNode("div", [LeafNode(None, "Text")], attributes)
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main">Text</div>',
        )

    def test_large_tree(self):
        children = [LeafNode(None, f"Text {i}") for i in range(1000)]
        parent_node = ParentNode("div", children)
        expected_output = "<div>" + "".join(f"Text {i}" for i in range(1000)) + "</div>"
        self.assertEqual(parent_node.to_html(), expected_output)

    def test_whitespace_in_content(self):
        parent_node = ParentNode("div", [LeafNode(None, "    Text with spaces   ")])
        self.assertEqual(
            parent_node.to_html(),
            "<div>    Text with spaces   </div>",
        )


if __name__ == "__main__":
    unittest.main()
