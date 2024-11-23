import unittest
from parentnode import ParentNode
from leafnode import LeafNode


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
