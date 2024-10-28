import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("IS EQUAL?")
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        print("IS EQUAL? URL")
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        print("IS NOT EQUAL? URL")
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        print("IS NOT EQUAL? : TEXT_TYPE")
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_cont(self):
        print("IS NOT EQUAL? : TEXT_CONT")
        node = TextNode("This is a dank text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()