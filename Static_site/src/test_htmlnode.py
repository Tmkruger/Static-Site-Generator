import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

	def test_eq(self):
		print("IS EQUAL? HTML")
		node = HTMLNode("p", "This is a Paragraph")
		node2 = HTMLNode("p", "This is a Paragraph")
		self.assertEqual(node, node2)

	def test_eq_link(self):
		print("IS EQUAL? HTML LINK")
		link1 = HTMLNode("a", "Link to Boot.dev", props={"href": "https://www.boot.dev"})
		link2 = HTMLNode("a", "Link to Boot.dev", props={"href": "https://www.boot.dev"})
		self.assertEqual(link1, link2)

	def test_eq_div_child(self):
		print("IS EQUAL? HTML CHILD")
		link1 = HTMLNode("a", "Link to Boot.dev", props={"href": "https://www.boot.dev"})
		link2 = HTMLNode("a", "Link to Boot.dev", props={"href": "https://www.boot.dev"})
		div_container = HTMLNode("div", children=link1)
		div_container2 = HTMLNode("div", children=link2)
		self.assertEqual(div_container, div_container2)

	def test_not_eq_div_child(self):
		print("IS NOT EQUAL? HTML CHILD")
		link1 = HTMLNode("a", "Link to Boot.dev", props={"href": "https://www.boot.dev"})
		link3 = HTMLNode("a", "Link to Youtube.com", props={"href": "https://www.youtube.com/"})
		div_container = HTMLNode("div", children=link1)
		div_container3 = HTMLNode("div", children=link3)
		self.assertNotEqual(div_container, div_container3)	