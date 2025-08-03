import unittest

from textnode import TextNode, TextType
from nodemanager import split_nodes_delmiter




class TestSplitNodeDelimiter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is plain text node", TextType.TEXT)
        new_nodes = split_nodes_delmiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])
    def test_bold(self):
        pass
    def test_italic(self):
        pass
    def test_code(self):
        pass
    def test_delim_beg(self):
        pass
    def test_delim_end(self):
        pass
    def test_multi_delim_same(self):
        pass
    def test_multi_delim_diff(self):
        pass
    def test_no_delim(self):
        pass
    def test_mixed_node_type(self):
        pass