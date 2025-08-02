import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    # Test 1 Default Case
    def test_props_to_html(self):
        node = HtmlNode("a", "google", None, {"href" : "https://www.google.com", "target": "_blank"})
        string = node.props_to_html()
        self.assertEqual(string, ' href="https://www.google.com" target="_blank"')

    # Test 2 No properties?
    def test_props_no_prop(self):
        node = HtmlNode()
        string = node.props_to_html()
        self.assertEqual(string, ValueError)
    # Test 3 One property
    def test_props_one_prop(self):
        node = HtmlNode(tag="a")
        node2 = HtmlNode(props={"href": "https://www.google.com"})
        string = node.props_to_html()
        string2 = node2.props_to_html()
        self.assertEqual(string, ValueError)
        self.assertEqual(string2, ' href="https://www.google.com"')
    # Test 4 Propertys are numbers or booleans(not strings)
    def test_props_wrong_values(self):
        node = HtmlNode("a", "google", None, True)
        string = node.props_to_html()
        node2 = HtmlNode("a", "google", None, {"href": True})
        string2 = node2.props_to_html()
        self.assertEqual(string, ValueError)
        self.assertEqual(string2, ' href="True"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is a Header", None)
        self.assertEqual(node.to_html(), "<h1>This is a Header</h1>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is plain text", None)
        self.assertEqual(node.to_html(), "This is plain text")


class TestParentNode(unittest.TestCase):
    def test_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        #print(f"PARENT TO HTML: {parent_node.to_html()}")
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_none_children(self):
        parent_node = ParentNode("div", children=None)
        with self.assertRaises(ValueError) as error:
            parent_node.to_html()
        self.assertTrue(str(error.exception) == "No Children")

    def test_none_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as error:
            parent_node.to_html()
        self.assertTrue(str(error.exception) == "No Tag found in Node(Required for parent)")

    def test_empty_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as error:
            parent_node.to_html()
        self.assertTrue(str(error.exception) == "Unknown Error")
    # multiple children
    def test_multiple_children(self):
        child_node1 = LeafNode("b", "node1")
        child_node2 = LeafNode("p", "node2")
        child_node3 = LeafNode("p", "node3")
        child_node4 = LeafNode("b", "node4")
        parent_node = ParentNode("div", [child_node1,child_node2,child_node3,child_node4])
        self.assertEqual(parent_node.to_html(), "<div><b>node1</b><p>node2</p><p>node3</p><b>node4</b></div>")
    # deeply nested parents
    def test_deeply_nested_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("body", [parent_node])
        self.assertEqual(parent_node2.to_html(), "<body><div><span><b>grandchild</b></span></div></body>")
    # mixed children
    def test_mixed_children(self):
        node = LeafNode("p", "node_2_is_my_parent")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("body", [parent_node, node])
        self.assertEqual(parent_node2.to_html(), "<body><div><span><b>grandchild</b></span></div><p>node_2_is_my_parent</p></body>")
    # parents with props
    # nested nodes with props
    # list structure
    # table structure


if __name__ == "__main__":
    unittest.main()
