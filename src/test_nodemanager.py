import unittest

from textnode import TextNode, TextType
from nodemanager import split_nodes_delmiter




class TestSplitNodeDelimiter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is plain text node", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])
    def test_bold(self):
        node = TextNode("This is a **bold** text node", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text node", TextType.TEXT)])
    def test_italic(self):
        node = TextNode("This is a *italic* text node", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text node", TextType.TEXT)])
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])
    def test_delim_beg(self):
        node = TextNode("*italic* is at the start", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic", TextType.ITALIC), TextNode(" is at the start", TextType.TEXT)])
    def test_delim_end(self):
        node = TextNode("italic is at the *end*", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic is at the ", TextType.TEXT), TextNode("end", TextType.ITALIC)])
    def test_multi_delim_same(self):
        node = TextNode("*italic* is at the start and *end*", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic", TextType.ITALIC), TextNode(" is at the start and ", TextType.TEXT), TextNode("end", TextType.ITALIC)])
    def test_multi_delim_diff(self):
        node = TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("italic", TextType.ITALIC), TextNode(" is at the start and an ending **bold**", TextType.TEXT)])
    def test_no_delim(self):
        node = TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)])
    def test_mixed_node_type(self):
        node = TextNode("*italic* is at the start and an ending **bold**", TextType.TEXT)
        node2 = TextNode("end", TextType.ITALIC)
        node3 = TextNode("code block", TextType.CODE)
        nodes = [node,node2,node3]
        new_nodes = split_nodes_delmiter(nodes, "", TextType.ITALIC)
        self.assertEqual(new_nodes, nodes)
